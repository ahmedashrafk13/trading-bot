#!/usr/bin/env bash
# Computes the numbers every guardrail depends on, so no run has to do arithmetic
# over markdown. Read-only.
#
# Usage: bash scripts/state.sh
#
# Emits: UTC now (from the EXCHANGE clock, never the local machine clock),
# equity/cash/deployment, open positions with age and stop coverage, the monthly
# fee budget state, today's realized P&L for the circuit breaker, and the count
# of closed trades since the last applied amendment.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
python scripts/bybit.py time         > "$TMP/clock.json"
python scripts/bybit.py balance      > "$TMP/bal.json"
python scripts/bybit.py holdings     > "$TMP/hold.json"
python scripts/bybit.py orders spot  > "$TMP/ord.json"
python scripts/bybit.py tickers spot > "$TMP/tick.json"
# v4 2026-09-22: perps are live, so the perp book must be visible here or every
# SHORT is invisible to reconciliation. Never let this fail the whole run.
python scripts/bybit.py positions linear > "$TMP/perp.json" 2>/dev/null || echo '[]' > "$TMP/perp.json"
# 2026-09-22: a stop that TRIGGERS and is then REJECTED leaves no fill, so
# nothing in this script noticed ARB/XPL going naked for ~20h. Read order
# history so a rejected stop is impossible to miss.
python scripts/bybit.py history spot > "$TMP/hist.json" 2>/dev/null || echo '[]' > "$TMP/hist.json"

python - "$TMP" <<'PY'
import json, re, sys, datetime as dt
from pathlib import Path
t = Path(sys.argv[1])
clock  = json.loads((t/'clock.json').read_text())
bal    = json.loads((t/'bal.json').read_text())
hold   = json.loads((t/'hold.json').read_text())
orders = json.loads((t/'ord.json').read_text())
try:
    perps = json.loads((t/'perp.json').read_text())
except Exception:
    perps = []
perps = [p for p in (perps or []) if float(p.get('size') or 0) != 0]
try:
    hist = json.loads((t/'hist.json').read_text())
except Exception:
    hist = []
ticks  = json.loads((t/'tick.json').read_text())

# NEVER trust the local clock — this machine is known to be 12h fast.
now = dt.datetime.fromtimestamp(int(clock['time'])/1000, dt.timezone.utc)
today = now.date()

# Unified account: totalEquity is the single number routines treat as equity.
# Cash is the USDT leg of that account, not the free-collateral figure, so
# "deployed" means value held in coins other than USDT.
accts = bal.get('list') or []
if not accts:
    raise SystemExit("bybit balance returned no UNIFIED account — cannot compute state")
_acct = accts[0]
eq = float(_acct.get('totalEquity') or 0)
cash = 0.0
for _c in _acct.get('coin', []):
    if _c.get('coin') == 'USDT':
        cash = float(_c.get('usdValue') or _c.get('walletBalance') or 0)
if eq <= 0:
    raise SystemExit("bybit reports zero equity — refusing to derive position sizes from it")

# TRADING BUDGET CAP. The account this runs against holds far more than the
# strategy is authorised to trade. Every guardrail below is a PERCENTAGE OF
# EQUITY, so feeding it the raw account balance would size positions hundreds of
# times too large. `eq` is therefore the SIZING BASIS, not the account balance:
# capped at TRADING_BUDGET_USD. Owner-set 2026-09-18; only the owner may raise it.
import os
_budget = float(os.environ.get('TRADING_BUDGET_USD') or 200)
_account_eq = eq
if _account_eq > _budget:
    eq = _budget
    print(f"BUDGET CAP  account holds ${_account_eq:,.2f}; sizing basis capped to "
          f"${eq:,.2f} (TRADING_BUDGET_USD). All %-of-equity rules below use the CAP.")

print(f"UTC NOW (exchange clock) {now:%Y-%m-%d %H:%M} UTC   [local clock is NOT trusted]")
# Deployment is measured against the BUDGET, not the account. With the sizing
# basis capped, `eq - cash` is meaningless (the account's spare cash dwarfs the
# budget), so deployed value is summed from the non-stablecoin holdings directly.
_deployed = sum(float(_c.get('usdValue') or 0) for _c in hold
                if _c.get('coin') not in ('USDT', 'USDC'))
_free = max(0.0, eq - _deployed)
print(f"EQUITY ${eq:.2f} (budget) | FREE ${_free:.2f} | DEPLOYED ${_deployed:.2f} = "
      f"{_deployed/eq*100:.1f}% of budget (CEILING 50%, no floor)")
print(f"           account cash ${cash:,.2f} — NOT tradeable, budget is the ceiling")
# Size is derived from risk, never fixed in dollars. Printing it here keeps the
# arithmetic out of the run prompts, where it was previously re-derived by hand.
core_risk, tac_risk = eq*0.020, eq*0.005
core_sz = min(core_risk/0.15, eq*0.20)
tac_sz  = min(tac_risk/0.10, eq*0.08)
print(f"SIZE NOW   CORE ${core_sz:.2f} (15% trail, risk ${core_risk:.2f} = 2.0%, max 1)"
      f" | TACTICAL ${tac_sz:.2f} (10% trail, risk ${tac_risk:.2f} = 0.5%, max 6)")
print(f"           BOTH SLEEVES TRAIL. No profit target, no target leg.")
print(f"           CORE: no time limit | TACTICAL+SHORT: 72h time stop unless >= +5% in favour.")
print()

# --- positions, ages, stop coverage -------------------------------------------
# TRADE-LOG carries pairs as BTC/USD; Bybit spot symbols are BTCUSDT. Everything
# below keys off the BASE COIN so the two notations reconcile.
QUOTES = ('USDT', 'USDC', 'USD')
def base(s):
    s = (s or '').replace('/', '').upper()
    for q in QUOTES:
        if s.endswith(q) and len(s) > len(q):
            return s[:-len(q)]
    return s

price = {}
for _row in ticks:
    _sym = _row.get('symbol') or ''
    if _sym.endswith('USDT'):
        try: price[base(_sym)] = float(_row.get('lastPrice') or 0)
        except (TypeError, ValueError): pass

log = Path('memory/TRADE-LOG.md').read_text(encoding='utf-8')
entry_times = {base(k): v for k, v in re.findall(
    r'TACTICAL entry: ([A-Z0-9]+)(?:/USDT?|USDT)?\b.*?Entry time \(UTC\) \| (\S+)', log, re.S)}
# Sleeve per symbol, from the ENTRY section headers ("### <date> UTC - ENTRY - CORE - ETH/USD BUY").
# Later entries win, so a symbol re-entered in the other sleeve resolves to its CURRENT sleeve.
sleeves = {}
SLEEVE_RE = re.compile(
    r'###\s*(\d{4}-\d{2}-\d{2})[^\n]*?ENTRY\s*[—-]\s*(CORE|TACTICAL|SHORT)\s*[—-]\s*([A-Z0-9]+)(?:/USDT?|USDT)?\b')
for d, sl, sy in SLEEVE_RE.findall(log):
    sleeves[base(sy)] = (sl, dt.date.fromisoformat(d))

# Entry price per symbol. A spot wallet balance has NO cost basis — the exchange
# cannot tell us what we paid — so unrealised P&L, and therefore the gap-
# enforcement check, is only computable from what the entry run wrote down.
# Scanned per ENTRY section so a later re-entry supersedes an earlier one.
entry_px = {}
ENTRY_PX_RE = re.compile(r'^\|\s*(?:Fill price|Avg entry|Entry)\s*\|\s*\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)', re.M)
_chunks = re.split(r'(?=^###\s)', log, flags=re.M)
for _ch in _chunks:
    _h = SLEEVE_RE.search(_ch)
    if not _h:
        continue
    _p = ENTRY_PX_RE.search(_ch)
    if _p:
        entry_px[base(_h.group(3))] = float(_p.group(1).replace(',', ''))

# --- FALLBACK: the STEP E fills table ----------------------------------------
# Added 2026-09-18 after a live defect: the 20:07 execute run logged two real
# entries (POL, OP) entirely in prose under a "## ..." header, so SLEEVE_RE
# matched nothing and every position showed sleeve/entry/age UNKNOWN. That
# silently disables the 72h time stop, gap enforcement AND the trade-count line
# counter. The STEP E table is structured, so parse it too and let it fill any
# gap the headers left. Headers still WIN where both exist.
#   | UTC | Sleeve | Symbol | Side | Qty | Fill | Value | Fee | Stop | Target |
FILLS_RE = re.compile(
    r'^\|\s*(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})\s*\|'      # UTC date/time
    r'\s*(CORE|TACTICAL)\s*\|'                                    # sleeve
    r'\s*([A-Z0-9]+?)(?:USDT|/USDT?)?\s*\|'                       # symbol
    r'\s*(?:Buy|BUY)\s*\|'                                        # side = Buy only
    r'\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*\|'                       # qty
    r'\s*\$?\s*([0-9][0-9,]*(?:\.[0-9]+)?)', re.M)               # fill price
fills_tbl = []
for _d, _t, _sl, _sy, _q, _px in FILLS_RE.findall(log):
    fills_tbl.append((_d, _t, _sl, base(_sy), float(_px.replace(',', ''))))
for _d, _t, _sl, _sy, _px in fills_tbl:
    if _sy not in sleeves:
        sleeves[_sy] = (_sl, dt.date.fromisoformat(_d))
    if _sy not in entry_px:
        entry_px[_sy] = _px
    if _sy not in entry_times:
        entry_times[_sy] = f'{_d}T{_t}'

# On Bybit a protective stop rests as a CONDITIONAL sell: the exchange reports it
# in /v5/order/realtime carrying a non-empty stopOrderType and a triggerPrice. A
# plain limit sell with no trigger is a TARGET LEG, which v2 bans outright.
def is_sell(o): return (o.get('side') or '').lower() == 'sell'
def qty_of(o):
    try: return float(o.get('qty') or 0)
    except (TypeError, ValueError): return 0.0

stops, limit_orders = {}, {}
for o in orders:
    if not is_sell(o):
        continue
    if o.get('stopOrderType') or o.get('triggerPrice'):
        stops.setdefault(base(o.get('symbol')), []).append(o)
    else:
        limit_orders.setdefault(base(o.get('symbol')), []).append(o)

# --- SCAN GATE (advisory) -----------------------------------------------------
# Scan's only actions are STEP 2 (stop shape/coverage), STEP 3 (gap enforcement)
# and STEP 4 (ratchet). This block decides, in Python, whether ANY of them could
# fire. It FAILS OPEN by construction: every uncertainty appends a reason, and any
# reason at all means ACTION. So a bug here can only cost a wasted run, never a
# missed ratchet or an unprotected position.
V2_CUTOVER = dt.date(2026, 9, 15)
TIGHTEST   = {'CORE': 0.10, 'TACTICAL': 0.08}   # tightest legal v2 tier per sleeve
GAPCUT     = {'CORE': -14.0, 'TACTICAL': -9.0}  # 1pt EARLY of the -15/-10 hard cut
gate = []

# Spot holdings ARE the positions. USDT/USDC is cash, and dust below $1 is not a
# position worth stopping — it cannot be sold for more than the fee anyway.
DUST_USD = 1.0
pos = []
for c in hold:
    if c.get('coin') in ('USDT', 'USDC'):
        continue
    try:
        _qty = float(c.get('walletBalance') or 0)
        _usd = float(c.get('usdValue') or 0)
    except (TypeError, ValueError):
        continue
    if _usd < DUST_USD:
        continue
    pos.append((c.get('coin'), _qty, _usd))

print(f"OPEN POSITIONS ({len(pos)})")
if not pos: print("  none")
for coin, qty, usd in pos:
    sym = base(coin)
    cur = price.get(sym) or (usd/qty if qty else 0.0)
    covered = sum(qty_of(o) for o in stops.get(sym, []))
    targeted = sum(qty_of(o) for o in limit_orders.get(sym, []))
    pct_cov = covered/qty*100 if qty else 0
    pct_tgt = targeted/qty*100 if qty else 0
    unreserved = max(0.0, 100 - pct_cov - pct_tgt)
    # A spot wallet balance carries no cost basis, so entry — and therefore age —
    # is only knowable where the run recorded it in TRADE-LOG.
    age = ''
    v = entry_times.get(sym)
    if v:
        try:
            et = dt.datetime.fromisoformat(v).replace(tzinfo=dt.timezone.utc)
            age = f"{(now-et).total_seconds()/3600:.1f}h"
        except Exception: age = '?'
    # ONE resting leg per position and it is ALWAYS a conditional stop sell at
    # 100% of the held qty, in BOTH sleeves. Targets were removed 2026-09-15
    # (v2): neither sleeve has a profit target any more, so nothing competes for
    # the slot and there is no stop/target ambiguity left to thrash over.
    if pct_tgt > 0.5:
        flag = f'*** TARGET LEG {pct_tgt:.0f}% — BANNED in v2: cancel it, re-place a full stop ***'
    elif pct_cov < 0.5:
        flag = '*** NAKED — no resting stop at all ***'
    elif pct_cov < 99.5:
        flag = f'*** ONLY {pct_cov:.0f}% STOPPED ***'
    else:
        flag = 'OK stop @100%'
    print(f"  {sym:9} qty={qty:<12.6f} ${usd:>9.2f}  stop {pct_cov:5.1f}% / target {pct_tgt:5.1f}%"
          f" / unreserved {unreserved:4.1f}%  [{flag}]  age {age or 'unknown'}")
    # --- SCAN GATE evidence for this position -----------------------------
    # Fails open: anything unknown, unusual or borderline appends a reason, and
    # any reason at all makes the verdict ACTION.
    mystops = stops.get(sym, [])
    stop_px = None
    if len(mystops) == 1:
        try: stop_px = float(mystops[0].get('triggerPrice'))
        except (TypeError, ValueError): stop_px = None
    sl, ent = sleeves.get(sym, (None, None))
    # TIGHTEST tier, not the base trail: a tighter trail yields a HIGHER candidate
    # stop, so if even the tightest legal tier does not clear the resting stop,
    # no tier does. That is what makes a NO-ACTION verdict safe without knowing
    # the high-water mark -- the resting stop already encodes it.
    trail = TIGHTEST.get(sl)
    cand = cur*(1-trail) if (cur and trail) else None
    ent_px = entry_px.get(sym)
    plpc = ((cur/ent_px - 1)*100) if (ent_px and cur) else None
    print(f"            price ${cur:,.4f} | stop {('$%s' % format(stop_px, ',.4f')) if stop_px else 'NONE'}"
          f" | entry {('$%s' % format(ent_px, ',.4f')) if ent_px else 'UNKNOWN'}"
          f" | P&L {('%+.2f%%' % plpc) if plpc is not None else 'n/a'}"
          f" | sleeve {sl or 'UNKNOWN'} | ratchet due above {('$%s' % format(cand, ',.4f')) if cand else 'n/a'}")
    if flag != 'OK stop @100%':
        gate.append(f"{sym}: {flag}")
    if sl is None:
        gate.append(f"{sym}: sleeve not resolvable from TRADE-LOG")
    elif sl == 'TACTICAL' and ent and ent < V2_CUTOVER:
        gate.append(f"{sym}: pre-v2 TACTICAL entry ({ent}) - trail may be grandfathered, cannot reason")
    if len(mystops) != 1:
        gate.append(f"{sym}: expected exactly 1 resting conditional stop, found {len(mystops)}")
    elif stop_px is None:
        gate.append(f"{sym}: resting stop carries no readable triggerPrice")
    if not cur:
        gate.append(f"{sym}: exchange returned no last price")
    if plpc is None:
        gate.append(f"{sym}: no entry price in TRADE-LOG - cannot evaluate gap enforcement (STEP 3)")
    elif sl and plpc <= GAPCUT.get(sl, -999):
        gate.append(f"{sym}: {plpc:+.2f}% at/near the {sl} hard cut - gap enforcement (STEP 3)")
    if cand and stop_px and cand > stop_px:
        gate.append(f"{sym}: ratchet may be due - {trail*100:.0f}% trail on ${cur:,.4f}"
                    f" = ${cand:,.4f} > resting ${stop_px:,.4f}")
print()
# A resting sell against a coin that is no longer held is an orphan the run must
# look at; it is never a normal steady state.
open_syms = {base(c) for c, _, _ in pos}
for o in orders:
    if is_sell(o) and base(o.get('symbol')) not in open_syms:
        kind = o.get('stopOrderType') or o.get('orderType') or 'sell'
        gate.append(f"{base(o.get('symbol'))}: resting {kind} sell with no open position")

print("SCAN GATE  (advisory - SHADOW MODE, runs must NOT obey this yet)")
if gate:
    print("  SCAN-VERDICT: ACTION")
    for g in gate: print(f"    - {g}")
else:
    print("  SCAN-VERDICT: NO-ACTION")
    print("    every stop @100%, no gap-enforcement breach, and no ratchet due")
    print("    even at the tightest legal trail for each position's sleeve")
print()

# --- fee budget ---------------------------------------------------------------
fees_mo = 0.0
for m in re.finditer(r'Est\. round-trip fee \| \$([0-9.]+)', log):  fees_mo += float(m.group(1))
budget = eq*0.200   # 4.0% -> 20.0% on 2026-09-22 (OWNER DIRECTIVE, no trade ceiling)
month_start = today.replace(day=1)
print(f"FEE BUDGET  ${fees_mo:.2f} / ${budget:.2f} used this MONTH (20.0% of equity)")
print(f"            {'HEADROOM $%.2f' % (budget-fees_mo) if fees_mo < budget else '*** EXHAUSTED — no new entries until the 1st ***'}")
print(f"            month started {month_start}  [~240%/yr of drag at the ceiling — owner-accepted]")
print(f"            perps also pay FUNDING 8-hourly, which is NOT counted above")
print()

# --- REJECTED STOPS (added 2026-09-22 after the ARB/XPL naked-for-20h incident)
# A conditional stop that fires and is then REJECTED produces NO fill, so every
# fill-based check reads clean while the position is actually unprotected. This
# is the loudest thing this script prints, because it is the failure mode that
# has now cost money twice.
_rej = [o for o in (hist or [])
        if o.get('orderStatus') == 'Rejected'
        and (o.get('stopOrderType') or o.get('orderFilter') or '').startswith('Stop')]
if _rej:
    print("*** REJECTED PROTECTIVE STOPS — THESE POSITIONS WERE/ARE NAKED ***")
    for _o in _rej:
        _ts = dt.datetime.fromtimestamp(int(_o.get('updatedTime') or 0)/1000, dt.timezone.utc)
        print(f"    {_ts:%Y-%m-%d %H:%M} UTC  {_o.get('symbol'):10} qty {_o.get('qty'):>12} "
              f"trigger {_o.get('triggerPrice') or '-'}  (activated, then REJECTED — no fill)")
    print("    A rejected activation is SILENT: it leaves no fill, so nothing else catches it.")
    print("    Re-protect or close the position THIS RUN before considering any entry.")
    print()

# --- perp book (v4, 2026-09-22) -----------------------------------------------
# Longs AND shorts. A perp with no stopLoss is liquidation-exposed and is the
# single most urgent thing this script can report, so it is flagged loudly.
print(f"PERP BOOK   {len(perps)} open position(s)  [12 SHORT slots, 12 TACTICAL-long slots]")
_gross = 0.0
_naked = []
for _p in perps:
    _sym  = _p.get('symbol', '?')
    _side = _p.get('side', '?')            # Buy = long, Sell = SHORT
    _dir  = 'SHORT' if _side == 'Sell' else 'long'
    _sz   = float(_p.get('size') or 0)
    _val  = float(_p.get('positionValue') or 0)
    _lev  = _p.get('leverage') or '?'
    _sl   = (_p.get('stopLoss') or '').strip()
    _pnl  = float(_p.get('unrealisedPnl') or 0)
    _liq  = _p.get('liqPrice') or '-'
    _gross += abs(_val)
    _flag = '' if (_sl and _sl not in ('0', '0.0')) else '  *** NO STOPLOSS — LIQUIDATION EXPOSED ***'
    if _flag: _naked.append(_sym)
    print(f"            {_dir:<5} {_sym:<12} sz {_sz:<12g} ${_val:>8.2f} @{_lev}x  "
          f"SL {_sl or '(none)':<12} liq {_liq:<12} uPnL ${_pnl:+.2f}{_flag}")
_margin_cap, _notional_cap = eq*0.50, eq*3.00
print(f"            GROSS NOTIONAL ${_gross:.2f} / ${_notional_cap:.2f} (300% of budget)"
      f"{'  *** OVER ***' if _gross > _notional_cap else ''}")
if _naked:
    print(f"            *** {len(_naked)} UNPROTECTED PERP(S): {' '.join(_naked)} — "
          "attach a stopLoss THIS RUN or close them. This outranks every entry. ***")
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
# The 5-loss streak is scoped to the UTC DAY and RESETS at 00:00 UTC
# (TRADING-STRATEGY.md Buy-Side Gate: "5 consecutive tactical losses THAT
# CLOSED TODAY (UTC) ... It does NOT carry across days"). Counting it over all
# history deadlocks the sleeve permanently: only a WIN clears the streak, and
# the freeze itself prevents any trade that could produce one.
losses_streak = 0
for _, a in reversed([t for t in closed_trades if t[0] == f'{today}']):
    if a < 0: losses_streak += 1
    else: break
limit = eq*0.05
# --- daily TACTICAL quota (owner directive 2026-09-18) ------------------------
# Floor is 2 TACTICAL entries per UTC DAY. Counted from ENTRY section headers.
# v4 2026-09-22: SHORT is a tradeable sleeve and its entries count too. Before
# this, 12 shorts placed in one run reported as 0 and the line read "idle book".
_q_syms = {(_d, base(_sy)) for _d, _sl, _sy in SLEEVE_RE.findall(log)
            if _sl in ('TACTICAL', 'SHORT')}
_q_syms |= {(_d, _sy) for _d, _t, _sl, _sy, _px in fills_tbl
            if _sl in ('TACTICAL', 'SHORT')}
_q_today = sum(1 for _d, _sy in _q_syms if _d == f'{today}')
_hh = int(now.strftime('%H'))
_runs_left = sum(1 for _h in (0, 6, 12, 18) if _h >= _hh)
_backstop = _hh >= 18
# v4 2026-09-22: the 2/day QUOTA became a floor far below the intended rate.
# There is NO CEILING — this line now reports the count and the free slots, and
# treats an idle book with a live screen as the failure state.
print(f"TRADE COUNT  TACTICAL+SHORT entries today ({today}): {_q_today}  [NO CEILING]")
print(f"             floor 2/day (should never bind); target is EVERY passing name")
if _q_today < 2:
    print(f"             status: below the 2/day floor"
          f"{'  *** 18:07 BACKSTOP RUN ***' if _backstop else ''}")
    print(f"             entry windows remaining today (incl. this one): {_runs_left}")
print("             'no catalyst' / 'no conviction' / 'patience' are NOT valid misses")
print("             an idle slot + a passing screen + fee headroom = DIRECTIVE BREACH")
print()

print(f"CIRCUIT BREAKER  realized losses TODAY ({today}) ${abs(today_real):.2f} vs ${limit:.2f} limit (5% of equity)")
last_loss = closed_trades[-1][0] if closed_trades and closed_trades[-1][1] < 0 else None
print(f"                 consecutive losing closes TODAY: {losses_streak} (streak resets 00:00 UTC)"
      f"{f'; most recent loss closed {last_loss}' if last_loss else ''}")
print(f"                 status: {'TRIPPED — no new entries' if abs(today_real)>=limit or losses_streak>=5 else 'clear'}")
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
      f"{len(since)} | reference mark 10 | {len(closed_trades)} closed all-time")
# INFORMATIONAL ONLY since the owner's 2026-09-16 directive: amendment is OPEN
# to any run and this counter is not a gate. It stays because a thin sample is
# still a reason to prefer a hypothesis over an edit.
print(f"                   status: {'ample sample' if len(since) >= 10 else 'THIN sample — prefer a hypothesis over an edit'}"
      f"  [informational, NOT a gate]")
PY
