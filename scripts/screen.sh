#!/usr/bin/env bash
# Universe screener. Ranks tradable non-stablecoin Bybit USDT spot pairs on
# momentum, trend position and volatility, so entry decisions start from data
# rather than from whichever coin the news happened to mention.
#
# Usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|short|all] [--top N]
#
# Prints a ranked table plus a PASS/FAIL verdict per sleeve's technical filters.
# Read-only: no orders, no writes.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FORMAT="table"; SLEEVE="all"; TOP="60"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) FORMAT="json"; shift ;;
    --sleeve) SLEEVE="${2:?}"; shift 2 ;;
    --top) TOP="${2:?}"; shift 2 ;;
    *) echo "usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|short|all] [--top N]" >&2; exit 1 ;;
  esac
done

# Each sleeve is judged on its own timeframe. CORE filters are only meaningful
# on daily bars, TACTICAL only on hourly, so the sleeve picks the timeframe and
# the irrelevant column is suppressed.
if [[ "$SLEEVE" == "all" ]]; then
  "$0" --sleeve core     --top "$TOP" $([[ $FORMAT == json ]] && echo --json)
  echo
  "$0" --sleeve tactical --top "$TOP" $([[ $FORMAT == json ]] && echo --json)
  echo
  "$0" --sleeve short    --top "$TOP" $([[ $FORMAT == json ]] && echo --json)
  exit 0
fi
case "$SLEEVE" in
  core)     TF="D"  ;;
  tactical) TF="60" ;;
  short)    TF="60" ;;
  *) echo "unknown sleeve: $SLEEVE (core|tactical|short|all)" >&2; exit 1 ;;
esac

FORMAT="$FORMAT" SLEEVE="$SLEEVE" TF="$TF" TOP="$TOP" python - <<'PY'
import importlib.util, json, os, statistics as st, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.getcwd()
# bybit.py is a script, not a package, so it is loaded by path. Going through it
# rather than re-implementing signing keeps ONE place where the API is spoken to.
_spec = importlib.util.spec_from_file_location("bybit", os.path.join(ROOT, "scripts", "bybit.py"))
bybit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bybit)

fmt    = os.environ["FORMAT"]
sleeve = os.environ["SLEEVE"]
TF     = os.environ["TF"]
TOP    = int(os.environ["TOP"])

# Stablecoins and wrapped-dollar tokens are never positions — TRADING-STRATEGY
# forbids holding one — so they are dropped before ranking rather than after.
STABLES = {"USDC", "USDT", "USDG", "USDE", "DAI", "TUSD", "FDUSD", "BUSD",
           "USDD", "PYUSD", "EURT", "EURS",
           # added 2026-09-17 weekly review: RLUSD reached a live CORE
           # SHORTLIST on 2026-09-17, which immutable rule 9 forbids holding.
           "RLUSD", "USD1", "USDS", "USDY", "USDP", "GUSD", "LUSD", "FRAX",
           "SUSD", "USDF", "USDO", "EURC"}

# Bybit lists ~394 USDT spot pairs. A bigger universe is NOT automatically
# better: the wide end of the list is illiquid junk whose spread alone exceeds
# the edge. Rank by 24h turnover and keep the top TOP, which is where anything
# tradable at this account size actually lives.
tickers = bybit.request("GET", "/v5/market/tickers", {"category": "spot"}) \
              .get("result", {}).get("list", [])

def _f(x, default=float("nan")):
    try: return float(x)
    except (TypeError, ValueError): return default

cands = []
for t in tickers:
    sym = t.get("symbol") or ""
    if not sym.endswith("USDT"):
        continue
    coin = sym[:-4]
    if coin in STABLES or not coin:
        continue
    turnover = _f(t.get("turnover24h"), 0.0)
    if turnover != turnover:
        turnover = 0.0
    cands.append((turnover, sym, coin, t))
cands.sort(reverse=True, key=lambda x: x[0])
cands = cands[:TOP]
if not cands:
    print("SCREEN ERROR: Bybit returned no USDT spot tickers.", file=sys.stderr)
    raise SystemExit(1)

# Bybit has no batch-bars endpoint — one kline call per symbol — so the fetch is
# parallel. 8 is well inside the public rate limit and keeps a 60-coin screen
# under ~5s. `limit` is capped at 1000 server-side; 60 periods is plenty for a
# 30-period momentum and a 20-period SMA.
BARS = 60
def klines(sym):
    r = bybit.request("GET", "/v5/market/kline",
                      {"category": "spot", "symbol": sym,
                       "interval": TF, "limit": BARS})
    rows = r.get("result", {}).get("list", [])
    rows.sort(key=lambda x: int(x[0]))          # Bybit returns NEWEST first
    return sym, [_f(x[4]) for x in rows]        # index 4 = close

with ThreadPoolExecutor(max_workers=8) as ex:
    closes = dict(ex.map(klines, [c[1] for c in cands]))

rows = []
for turnover, sym, coin, t in cands:
    c = [x for x in closes.get(sym, []) if x == x]
    if len(c) < 21:
        continue                      # not enough history to judge trend
    last  = c[-1]
    sma20 = sum(c[-20:]) / 20
    prev_sma20 = sum(c[-21:-1]) / 20
    sma_rising = sma20 > prev_sma20
    rets  = [(c[i] / c[i-1] - 1) for i in range(1, len(c)) if c[i-1]]
    vol   = st.pstdev(rets[-14:]) * 100 if len(rets) >= 14 else float('nan')
    m7    = (last / c[-8]  - 1) * 100 if len(c) >  8 and c[-8]  else float('nan')
    m30   = (last / c[-31] - 1) * 100 if len(c) > 31 and c[-31] else float('nan')
    dsma  = (last / sma20 - 1) * 100 if sma20 else float('nan')

    ap, bp = _f(t.get("ask1Price")), _f(t.get("bid1Price"))
    spread = ((ap - bp) / ((ap + bp) / 2) * 100) if (ap == ap and bp == bp and ap and bp) else float('nan')

    # --- technical entry filters (see memory/TRADING-STRATEGY.md) ---
    # CORE (daily bars): established uptrend, priced above a rising SMA20, not
    # extended. Demanding a rising SMA and dsma>0 is what makes this selective —
    # a 30d>0 test alone passed nearly the whole universe and screened nothing.
    core_ok, core_why = True, []
    if not (m30 > 0):            core_ok, _ = False, core_why.append('30p<=0')
    if not (dsma > 0):           core_ok, _ = False, core_why.append('below SMA20')
    if not sma_rising:           core_ok, _ = False, core_why.append('SMA20 falling')
    if not (dsma <= 20):         core_ok, _ = False, core_why.append('>20% over SMA20')
    if not (spread <= 1.0):      core_ok, _ = False, core_why.append('spread>1%')

    # TACTICAL (hourly bars): short-horizon push that is not yet extended, with
    # enough movement to be worth taking and a spread cheap enough that the
    # ~0.11% Bybit round trip does not eat the edge.
    tac_ok, tac_why = True, []
    if not (m7 > 0):             tac_ok, _ = False, tac_why.append('short-mom<=0')
    if not (-8 <= dsma <= 8):    tac_ok, _ = False, tac_why.append('too far from SMA20')
    if not (0.4 <= vol <= 6.0):  tac_ok, _ = False, tac_why.append('vol outside band')
    if not (spread <= 0.5):      tac_ok, _ = False, tac_why.append('spread>0.5%')

    # SHORT (hourly bars): the exact mirror of TACTICAL. Perps let this account
    # sell weakness, so a name failing TACTICAL for being DOWN is not a reject —
    # it is the other side of the book. Same vol band and same spread ceiling,
    # because the friction is direction-blind.
    shrt_ok, shrt_why = True, []
    if not (m7 < 0):             shrt_ok, _ = False, shrt_why.append('short-mom>=0')
    if not (-8 <= dsma <= 8):    shrt_ok, _ = False, shrt_why.append('too far from SMA20')
    if not (0.4 <= vol <= 6.0):  shrt_ok, _ = False, shrt_why.append('vol outside band')
    if not (spread <= 0.5):      shrt_ok, _ = False, shrt_why.append('spread>0.5%')

    rows.append(dict(symbol=sym, coin=coin, last=last, m7=m7, m30=m30, dsma=dsma,
                     vol=vol, spread=spread, turnover24h=turnover,
                     sma20_rising=sma_rising,
                     core_pass=core_ok, core_fail=core_why,
                     tactical_pass=tac_ok, tactical_fail=tac_why,
                     short_pass=shrt_ok, short_fail=shrt_why))

dropped = [c[2] for c in cands if len([x for x in closes.get(c[1], []) if x == x]) < 21]
if dropped:
    print(f'WARNING: {len(dropped)} coin(s) skipped for <21 periods of history: '
          + ' '.join(sorted(dropped)), file=sys.stderr)
expected = len(cands)
if expected and len(rows) < expected * 0.8:
    print(f'WARNING: only {len(rows)} of {expected} symbols scored — the screen may be '
          'working from incomplete data. Check the kline fetch before trusting it.', file=sys.stderr)

rows.sort(key=lambda r: (r['m7'] if r['m7'] == r['m7'] else -999), reverse=True)

if fmt == 'json':
    print(json.dumps(rows, indent=2)); raise SystemExit

print(f'UNIVERSE SCREEN [{TF}] — {len(rows)} of the top {TOP} coins by 24h turnover, >=21 periods')
print(f"{'coin':9}{'last':>13}{'7p%':>8}{'30p%':>8}{'vsSMA20':>9}{'vol%':>7}{'spr%':>7}  {'CORE':<6}{'TACTICAL':<9}{'SHORT':<6}")
print('-' * 98)
for r in rows:
    cf = 'PASS' if r['core_pass'] else 'fail'
    tf_ = 'PASS' if r['tactical_pass'] else 'fail'
    sf = 'PASS' if r['short_pass'] else 'fail'
    print(f"{r['coin']:9}{r['last']:>13,.4f}{r['m7']:>8.1f}{r['m30']:>8.1f}"
          f"{r['dsma']:>9.1f}{r['vol']:>7.1f}{r['spread']:>7.2f}  {cf:<6}{tf_:<9}{sf:<6}")
print()
key = {'core': 'core_pass', 'short': 'short_pass'}.get(sleeve, 'tactical_pass')
passes = [r['coin'] for r in rows if r[key]]
if sleeve == 'short':
    # Weakest first: the short book is ranked by how NEGATIVE the momentum is,
    # so rank 1 is the worst performer, not the best.
    passes = [r['coin'] for r in sorted(rows, key=lambda r: (r['m7'] if r['m7'] == r['m7'] else 999))
              if r['short_pass']]
print(f'{sleeve.upper()} SHORTLIST ({len(passes)}):', ' '.join(passes) or '(none)')

# Both directions in one call, so an execute run does not have to re-screen to
# find the other side of the book.
_longs  = [r['coin'] for r in rows if r['tactical_pass']]
_shorts = [r['coin'] for r in sorted(rows, key=lambda r: (r['m7'] if r['m7'] == r['m7'] else 999))
           if r['short_pass']]
print(f'  -> LONG candidates ({len(_longs)}):', ' '.join(_longs) or '(none)')
print(f'  -> SHORT candidates ({len(_shorts)}):', ' '.join(_shorts) or '(none)')
PY
