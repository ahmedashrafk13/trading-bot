#!/usr/bin/env bash
# Universe screener. Ranks ALL tradable non-stablecoin crypto USD pairs on
# momentum, trend position and volatility, so entry decisions start from data
# rather than from whichever coin the news happened to mention.
#
# Usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|all]
#
# Prints a ranked table plus a PASS/FAIL verdict per sleeve's technical filters.
# Read-only: no orders, no writes.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FORMAT="table"; SLEEVE="all"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) FORMAT="json"; shift ;;
    --sleeve) SLEEVE="${2:?}"; shift 2 ;;
    *) echo "usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|all]" >&2; exit 1 ;;
  esac
done

# Each sleeve is judged on its own timeframe. CORE filters are only meaningful
# on daily bars, TACTICAL only on hourly, so the sleeve picks the timeframe and
# the irrelevant column is suppressed.
if [[ "$SLEEVE" == "all" ]]; then
  "$0" --sleeve core     ${FORMAT:+$([[ $FORMAT == json ]] && echo --json)}
  echo
  "$0" --sleeve tactical ${FORMAT:+$([[ $FORMAT == json ]] && echo --json)}
  exit 0
fi
case "$SLEEVE" in
  core)     TF="1D" ;;
  tactical) TF="1H" ;;
  *) echo "unknown sleeve: $SLEEVE (core|tactical|all)" >&2; exit 1 ;;
esac
export TF

STABLES="USDC USDT USDG"

symbols="$(bash scripts/alpaca.sh assets crypto | python -c "
import json,sys
a=json.load(sys.stdin)
st=set('$STABLES'.split())
out=[x['symbol'] for x in a
     if x.get('tradable') and x['symbol'].endswith('/USD')
     and x['symbol'].split('/')[0] not in st]
print(','.join(sorted(out)))
")"

# 33 symbols x ~46 bars is far too large to pass as an argv string
# ("Argument list too long"), so hand the payloads to python as files.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
TF="${TF:-1D}"
# crypto-bars `limit` is 10000 TOTAL across symbols. 33 coins x 45 days of
# hourly bars would be ~35k, so shorten the window for intraday timeframes.
case "$TF" in
  1D|1Day) START="$(python -c "import datetime as d;print((d.datetime.now(d.timezone.utc)-d.timedelta(days=45)).strftime('%Y-%m-%d'))")" ;;
  *)       START="$(python -c "import datetime as d;print((d.datetime.now(d.timezone.utc)-d.timedelta(days=7)).strftime('%Y-%m-%d'))")" ;;
esac
# Follow pagination until exhausted, then merge. Without this the screen
# silently sees only the first few coins.
page=""; n=0
: > "$TMP/pages.ndjson"
while :; do
  bash scripts/alpaca.sh crypto-bars "$symbols" "$TF" "$START" 10000 "$page" > "$TMP/page.json"
  python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print(json.dumps(d.get('bars',{})))
" "$TMP/page.json" >> "$TMP/pages.ndjson"
  page="$(python -c "
import json,sys
print(json.load(open(sys.argv[1],encoding='utf-8')).get('next_page_token') or '')
" "$TMP/page.json")"
  n=$((n+1))
  # 1H over 33 symbols already needs ~29 pages; 15Min would need ~112. A silent
  # break here reproduces the original bug (a partial universe that looks fine),
  # so the cap is generous AND exceeding it is a hard error, never a truncation.
  if [[ $n -ge 200 ]]; then
    echo "SCREEN ERROR: pagination exceeded 200 pages and next_page_token is still set." >&2
    echo "  The universe would be INCOMPLETE. Shorten the window or the symbol list." >&2
    exit 1
  fi
  [[ -z "$page" ]] && break
done
python -c "
import json,sys
merged={}
for line in open(sys.argv[1],encoding='utf-8'):
    for k,v in json.loads(line).items():
        merged.setdefault(k,[]).extend(v)
json.dump({'bars':merged}, open(sys.argv[2],'w',encoding='utf-8'))
print('fetched ' + sys.argv[3] + ' page(s), ' + str(len(merged)) + ' symbols', file=sys.stderr)
" "$TMP/pages.ndjson" "$TMP/bars.json" "$n"
bash scripts/alpaca.sh crypto-quote "$symbols"     > "$TMP/quotes.json"

FORMAT="$FORMAT" SLEEVE="$SLEEVE" python -c "
import json, os, statistics as st, sys

bars   = json.load(open(sys.argv[1], encoding='utf-8')).get('bars', {})
quotes = json.load(open(sys.argv[2], encoding='utf-8')).get('quotes', {})
fmt, sleeve = os.environ['FORMAT'], os.environ['SLEEVE']

rows = []
for sym, b in bars.items():
    c = [x['c'] for x in b]
    if len(c) < 21:
        continue                      # not enough history to judge trend
    last  = c[-1]
    sma20 = sum(c[-20:]) / 20
    prev_sma20 = sum(c[-21:-1]) / 20
    sma_rising = sma20 > prev_sma20
    rets  = [(c[i] / c[i-1] - 1) for i in range(1, len(c))]
    vol   = st.pstdev(rets[-14:]) * 100 if len(rets) >= 14 else float('nan')
    m7    = (last / c[-8]  - 1) * 100 if len(c) >  8 else float('nan')
    m30   = (last / c[-31] - 1) * 100 if len(c) > 31 else float('nan')
    dsma  = (last / sma20 - 1) * 100

    q = quotes.get(sym, {})
    ap, bp = q.get('ap'), q.get('bp')
    spread = ((ap - bp) / ((ap + bp) / 2) * 100) if (ap and bp) else float('nan')

    # --- technical entry filters (see memory/TRADING-STRATEGY.md) ---
    # CORE (daily bars): established uptrend, priced above a rising SMA20, not
    # extended. Demanding a rising SMA and dsma>0 is what makes this selective —
    # a 30d>0 test alone passed 32 of 33 coins and screened nothing.
    core_ok, core_why = True, []
    if not (m30 > 0):            core_ok, _ = False, core_why.append('30p<=0')
    if not (dsma > 0):           core_ok, _ = False, core_why.append('below SMA20')
    if not sma_rising:           core_ok, _ = False, core_why.append('SMA20 falling')
    if not (dsma <= 20):         core_ok, _ = False, core_why.append('>20% over SMA20')
    if not (spread <= 1.0):      core_ok, _ = False, core_why.append('spread>1%')

    # TACTICAL (hourly bars): short-horizon push that is not yet extended, with
    # enough movement to reach a ~12% target and a spread cheap enough that
    # ~0.5% round-trip fees do not eat the edge.
    tac_ok, tac_why = True, []
    if not (m7 > 0):             tac_ok, _ = False, tac_why.append('short-mom<=0')
    if not (-8 <= dsma <= 8):    tac_ok, _ = False, tac_why.append('too far from SMA20')
    if not (0.4 <= vol <= 6.0):  tac_ok, _ = False, tac_why.append('vol outside band')
    if not (spread <= 0.5):      tac_ok, _ = False, tac_why.append('spread>0.5%')

    rows.append(dict(symbol=sym, last=last, m7=m7, m30=m30, dsma=dsma, vol=vol,
                     spread=spread, sma20_rising=sma20 > prev_sma20,
                     core_pass=core_ok, core_fail=core_why,
                     tactical_pass=tac_ok, tactical_fail=tac_why))

dropped = [sym for sym, b in bars.items() if len([x['c'] for x in b]) < 21]
if dropped:
    print(f'WARNING: {len(dropped)} coin(s) skipped for <21 periods of history: '
          + ' '.join(sorted(s.replace('/USD','') for s in dropped)), file=sys.stderr)
expected = len(bars)
if expected and len(rows) < expected * 0.8:
    print(f'WARNING: only {len(rows)} of {expected} symbols scored — the screen may be '
          'working from incomplete data. Check pagination before trusting it.', file=sys.stderr)

rows.sort(key=lambda r: (r['m7'] if r['m7'] == r['m7'] else -999), reverse=True)

if fmt == 'json':
    print(json.dumps(rows, indent=2)); raise SystemExit

print(f'UNIVERSE SCREEN [{os.environ.get('TF', '1D')}] — {len(rows)} coins with >=21 periods')
print(f\"{'coin':7}{'last':>12}{'7d%':>8}{'30d%':>8}{'vsSMA20':>9}{'vol%':>7}{'spr%':>7}  {'CORE':<6}{'TACTICAL':<9}\")
print('-' * 88)
for r in rows:
    c = 'PASS' if r['core_pass'] else 'fail'
    t = 'PASS' if r['tactical_pass'] else 'fail'
    print(f\"{r['symbol'].replace('/USD',''):7}{r['last']:>12,.4f}{r['m7']:>8.1f}{r['m30']:>8.1f}\"
          f\"{r['dsma']:>9.1f}{r['vol']:>7.1f}{r['spread']:>7.2f}  {c:<6}{t:<9}\")
print()
key = 'core_pass' if sleeve == 'core' else 'tactical_pass'
passes = [r['symbol'] for r in rows if r[key]]
print(f'{sleeve.upper()} SHORTLIST ({len(passes)}):', ' '.join(s.replace('/USD','') for s in passes) or '(none)')
" "$TMP/bars.json" "$TMP/quotes.json"
