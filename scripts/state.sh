#!/usr/bin/env bash
# Computes the numbers every guardrail depends on, so no run has to do arithmetic
# over markdown. Read-only.
#
# Usage: bash scripts/state.sh
#
# Emits: UTC now (from the BROKER clock, never the local machine clock),
# equity/cash/deployment, open positions with age and stop coverage, the weekly
# fee budget state, today's realized P&L for the circuit breaker, and the count
# of closed trades since the last applied amendment.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
bash scripts/alpaca.sh clock     > "$TMP/clock.json"
bash scripts/alpaca.sh account   > "$TMP/acct.json"
bash scripts/alpaca.sh positions > "$TMP/pos.json"
bash scripts/alpaca.sh orders    > "$TMP/ord.json"

python - "$TMP" <<'PY'
import json, re, sys, datetime as dt
from pathlib import Path
t = Path(sys.argv[1])
clock = json.loads((t/'clock.json').read_text())
acct  = json.loads((t/'acct.json').read_text())
pos   = json.loads((t/'pos.json').read_text())
orders= json.loads((t/'ord.json').read_text())

# NEVER trust the local clock — this machine is known to be 12h fast.
now = dt.datetime.fromisoformat(clock['timestamp']).astimezone(dt.timezone.utc)
today = now.date()
monday = today - dt.timedelta(days=today.weekday())

eq, cash = float(acct['equity']), float(acct['cash'])
print(f"UTC NOW (broker clock)   {now:%Y-%m-%d %H:%M} UTC   [local clock is NOT trusted]")
print(f"EQUITY ${eq:.2f} | CASH ${cash:.2f} | DEPLOYED {(eq-cash)/eq*100:.1f}% (CEILING 85%, no floor)")
# Size is derived from risk, never fixed in dollars. Printing it here keeps the
# arithmetic out of the run prompts, where it was previously re-derived by hand.
risk = eq*0.015
print(f"SIZE NOW   CORE ${min(risk/0.15, eq*0.15):.2f} (15% stop) | TACTICAL ${min(risk/0.06, eq*0.25):.2f} (6% stop)   risk ${risk:.2f}/trade (1.5%)")
print()

# --- positions, ages, stop coverage -------------------------------------------
log = Path('memory/TRADE-LOG.md').read_text(encoding='utf-8')
entry_times = dict(re.findall(r'TACTICAL entry: (\S+?)/USD.*?Entry time \(UTC\) \| (\S+)', log, re.S))
def norm(s): return s.replace('/','').upper()
stops = {}
for o in orders:
    if o['side']=='sell' and o['type']=='stop_limit':
        stops.setdefault(norm(o['symbol']), []).append(o)
limit_orders = {}
for o in orders:
    if o['side']=='sell' and o['type']=='limit':
        limit_orders.setdefault(norm(o['symbol']), []).append(o)
limits = set(limit_orders)

print(f"OPEN POSITIONS ({len(pos)})")
if not pos: print("  none")
for p in pos:
    sym = norm(p['symbol']); qty = float(p['qty'])
    plpc = float(p['unrealized_plpc'])*100
    covered = sum(float(o['qty']) for o in stops.get(sym, []))
    targeted = sum(float(o['qty']) for o in limit_orders.get(sym, []))
    pct_cov = covered/qty*100 if qty else 0
    pct_tgt = targeted/qty*100 if qty else 0
    unreserved = max(0.0, 100 - pct_cov - pct_tgt)
    age = ''
    for k,v in entry_times.items():
        if norm(k+'USD')==sym:
            try:
                et = dt.datetime.fromisoformat(v).replace(tzinfo=dt.timezone.utc)
                age = f"{(now-et).total_seconds()/3600:.1f}h"
            except Exception: age = '?'
    # Since 2026-09-15 the stop must cover 100%. A resting TARGET leg is no longer
    # healthy — it is a legacy split to be migrated, so it is flagged, not excused.
    if pct_cov < 99.5:
        if pct_tgt > 0.5:
            flag = f'*** LEGACY SPLIT — cancel {pct_tgt:.0f}% target leg, restore full stop ***'
        elif pct_cov < 0.5:
            flag = '*** NAKED ***'
        else:
            flag = f'*** STOP COVERS ONLY {pct_cov:.0f}% ***'
    else:
        flag = 'OK full stop'
    print(f"  {sym:9} qty={qty:<12.6f} P&L {plpc:+6.2f}%  stop {pct_cov:5.1f}% / target {pct_tgt:5.1f}%"
          f" / unreserved {unreserved:4.1f}%  [{flag}]  age {age or 'unknown'}")
    if age and age!='?' and float(age[:-1]) > 48:
        print(f"    !! open >48h — reassess-or-close rule applies")
print()

# --- fee budget ---------------------------------------------------------------
fees_wk = 0.0
for m in re.finditer(r'Est\. round-trip fee \| \$([0-9.]+)', log):  fees_wk += float(m.group(1))
budget = eq*0.015
print(f"FEE BUDGET  ${fees_wk:.2f} / ${budget:.2f} used this week (1.5% of equity)")
print(f"            {'HEADROOM $%.2f' % (budget-fees_wk) if fees_wk < budget else '*** EXHAUSTED — no new entries until Monday ***'}")
print(f"            week started {monday}")
print()

# --- circuit breaker ----------------------------------------------------------
realized = [float(x) for x in re.findall(r'REALIZED P&L \$(-?[0-9.]+)', log)]
today_real = sum(r for r in realized if r < 0)   # conservative: losses only
losses_streak = 0
for r in reversed(realized):
    if r < 0: losses_streak += 1
    else: break
limit = eq*0.05
print(f"CIRCUIT BREAKER  realized losses logged ${abs(today_real):.2f} vs ${limit:.2f} limit (5% of equity)")
print(f"                 consecutive losing closes: {losses_streak} (3 stops tactical for the day)")
print(f"                 status: {'TRIPPED — no new entries' if abs(today_real)>=limit or losses_streak>=3 else 'clear'}")
print()

# --- amendment trigger --------------------------------------------------------
closed = len(realized)
rev = Path('memory/WEEKLY-REVIEW.md').read_text(encoding='utf-8')
applied = len(re.findall(r'^### Rule changes applied', rev, re.M))
print(f"AMENDMENT TRIGGER  closed trades logged: {closed} | need >= 10 since last amendment")
print(f"                   status: {'ELIGIBLE' if closed >= 10 else 'not eligible — change nothing'}")
PY
