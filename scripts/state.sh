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
core_risk, tac_risk = eq*0.020, eq*0.010
core_sz = min(core_risk/0.15, eq*0.20)
tac_sz  = min(tac_risk/0.10, eq*0.12)
print(f"SIZE NOW   CORE ${core_sz:.2f} (15% trail, risk ${core_risk:.2f} = 2.0%, max 4)"
      f" | TACTICAL ${tac_sz:.2f} (10% trail, risk ${tac_risk:.2f} = 1.0%, max 1)")
print(f"           BOTH SLEEVES TRAIL. No profit target, no time limit, no target leg.")
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
    # ONE resting leg per position and it is ALWAYS a stop_limit at 100% of the
    # held qty, in BOTH sleeves. Targets were removed 2026-09-15 (v2): neither
    # sleeve has a profit target any more, so nothing competes for the slot and
    # there is no stop/target ambiguity left to thrash over.
    total = pct_cov + pct_tgt
    if pct_tgt > 0.5:
        flag = f'*** TARGET LEG {pct_tgt:.0f}% — BANNED in v2: cancel it, re-place a full stop_limit ***'
    elif pct_cov < 0.5:
        flag = '*** NAKED — no resting stop at all ***'
    elif pct_cov < 99.5:
        flag = f'*** ONLY {pct_cov:.0f}% STOPPED ***'
    else:
        flag = 'OK stop @100%'
    print(f"  {sym:9} qty={qty:<12.6f} P&L {plpc:+6.2f}%  stop {pct_cov:5.1f}% / target {pct_tgt:5.1f}%"
          f" / unreserved {unreserved:4.1f}%  [{flag}]  age {age or 'unknown'}")
print()

# --- fee budget ---------------------------------------------------------------
fees_mo = 0.0
for m in re.finditer(r'Est\. round-trip fee \| \$([0-9.]+)', log):  fees_mo += float(m.group(1))
budget = eq*0.010
month_start = today.replace(day=1)
print(f"FEE BUDGET  ${fees_mo:.2f} / ${budget:.2f} used this MONTH (1.0% of equity)")
print(f"            {'HEADROOM $%.2f' % (budget-fees_mo) if fees_mo < budget else '*** EXHAUSTED — no new entries until the 1st ***'}")
print(f"            month started {month_start}  [budget is a CEILING, expected burn is ~half]")
print()

# --- closed trades ------------------------------------------------------------
# Parsed per TRADE-LOG section (a `### ` header starts one), NOT by a flat regex
# over the whole file. The flat scan this replaces looked for the literal
# `REALIZED P&L $`, which (a) MISSED every real exit — they declare results as
# `| **REALIZED P&L** | **≈ -$3.17** |` table rows or `**TOTAL REALIZED P&L:
# -$1.609**` bullets, never that form — so it reported $0.00 / 0 closed trades
# while three trades were on the books, and (b) would DOUBLE-COUNT the prose
# restatements daily summaries and later execute runs make of the same exit.
# One closed trade per section, taken only from a declaration-shaped line.
AMT = r'\**\s*(?:≈\s*)?(-?)\$\s*(-?[0-9][0-9,]*(?:\.[0-9]+)?)'

def _amt(sign, num):
    v = float(num.replace(',', ''))
    return -abs(v) if sign == '-' else v

RE_HDR   = re.compile(r'^###\s+(\d{4}-\d{2}-\d{2})', re.M)
RE_TOTAL = re.compile(r'^[-*]?\s*\**TOTAL REALIZED P&L:?\**\s*' + AMT, re.M)
RE_ROW   = re.compile(r'^\|\s*\**REALIZED P&L\**\s*\|\s*' + AMT, re.M)
RE_TODAY = re.compile(r'REALIZED TODAY \(UTC (\d{4}-\d{2}-\d{2})\):?\**\s*' + AMT)
# A fill is often DISCOVERED by a later run (XRP filled 09-15T18:41, logged in
# the 09-16T00:08 section), so the section's own header date is the WRONG day to
# charge a daily loss limit against. Prefer the stated exit timestamp.
RE_EXITTS = re.compile(r'^\|\s*Exit time \(UTC\)\s*\|\s*(\d{4}-\d{2}-\d{2})', re.M)

closed_trades = []        # (date, $) — one per section that DECLARES a close
day_amounts   = {}        # UTC date -> [amounts realized that day]
unparsed      = []

parts = RE_HDR.split(log)   # [preamble, date1, body1, date2, body2, ...]
for i in range(1, len(parts) - 1, 2):
    sec_date, body = parts[i], parts[i+1]
    m = RE_TOTAL.search(body) or RE_ROW.search(body)
    if not m:
        # A section that only TALKS about a realized figure is a restatement of
        # an earlier exit — skipping it is the point. Flag only a section whose
        # header says EXIT, because that one was supposed to declare.
        if 'EXIT' in body[:160].upper() and 'REALIZED P&L' in body:
            unparsed.append(sec_date)
        continue
    amount = _amt(*m.groups())
    # Day attribution: a trade whose legs straddle UTC days states its own split
    # (`REALIZED TODAY (UTC ...)`); otherwise the whole result lands on the
    # section's own date.
    dated = RE_TODAY.findall(body)
    for d, sg, n in dated:
        day_amounts.setdefault(d, []).append(_amt(sg, n))
    if not dated:
        ts = RE_EXITTS.search(body)
        day_amounts.setdefault(ts.group(1) if ts else sec_date, []).append(amount)
    # The trade is dated by when it actually CLOSED, not by the section that
    # happened to notice it.
    ts = RE_EXITTS.search(body)
    closed_trades.append((dated[0][0] if dated else (ts.group(1) if ts else sec_date), amount))

print("CLOSED TRADES (parsed from TRADE-LOG sections)")
for d, a in closed_trades:
    print(f"                 {d}  {a:+7.2f}")
if not closed_trades:
    print("                 none")
if unparsed:
    print(f"  *** {len(unparsed)} EXIT section(s) declare no parseable REALIZED P&L: "
          f"{', '.join(unparsed)} — figures below UNDER-report, count by hand ***")
print()

# --- circuit breaker ----------------------------------------------------------
today_real = sum(a for a in day_amounts.get(f'{today}', []) if a < 0)  # losses only
losses_streak = 0
for _, a in reversed(closed_trades):
    if a < 0: losses_streak += 1
    else: break
limit = eq*0.05
print(f"CIRCUIT BREAKER  realized losses TODAY ({today}) ${abs(today_real):.2f} vs ${limit:.2f} limit (5% of equity)")
last_loss = closed_trades[-1][0] if closed_trades and closed_trades[-1][1] < 0 else None
print(f"                 consecutive losing closes: {losses_streak} (3 stops tactical for the day)"
      f"{f'; most recent loss closed {last_loss}' if last_loss else ''}")
print(f"                 status: {'TRIPPED — no new entries' if abs(today_real)>=limit or losses_streak>=3 else 'clear'}")
print()

# --- amendment trigger --------------------------------------------------------
rev = Path('memory/WEEKLY-REVIEW.md').read_text(encoding='utf-8')
# Last amendment = the newest `## Week ending DATE` section that applied one.
amend_dates = [d for d, body in
               zip(re.findall(r'^##\s+Week ending (\d{4}-\d{2}-\d{2})', rev, re.M),
                   re.split(r'^##\s+Week ending \d{4}-\d{2}-\d{2}', rev, flags=re.M)[1:])
               if re.search(r'^### Rule changes applied', body, re.M)]
last_amend = max(amend_dates) if amend_dates else None
since = [t for t in closed_trades if last_amend is None or t[0] > last_amend]
print(f"AMENDMENT TRIGGER  closed trades since last amendment ({last_amend or 'none on record'}): "
      f"{len(since)} | need >= 10 | {len(closed_trades)} closed all-time")
print(f"                   status: {'ELIGIBLE' if len(since) >= 10 else 'not eligible — change nothing'}")
PY
