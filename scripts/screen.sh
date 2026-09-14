#!/usr/bin/env bash
# Universe screener. Ranks tradable Bybit SPOT USDT pairs on momentum, trend
# position, volatility and spread, so entry decisions start from data rather
# than from whichever coin the news happened to mention.
#
# Usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|all] [--top N]
#
# Prints a ranked table plus a PASS/FAIL verdict per sleeve's technical filters.
# Read-only: no orders, no writes. Uses only PUBLIC endpoints — the screen still
# works when the API keys are missing or rejected.
#
# Bybit vs Alpaca, two structural differences that shaped this rewrite:
#   1. /v5/market/tickers returns the ENTIRE spot universe (~538 pairs) with
#      bid/ask/turnover in ONE call. There is no page-token maze to get wrong.
#   2. Klines are ONE SYMBOL PER CALL. 397 USDT pairs is far too many, so we
#      gate on 24h turnover FIRST and only pull bars for the survivors. That
#      gate is not merely a performance trick — an illiquid coin is untradable
#      on a $200 book no matter how good its momentum looks.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FORMAT="table"; SLEEVE="all"; TOP="${SCREEN_TOP:-60}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) FORMAT="json"; shift ;;
    --sleeve) SLEEVE="${2:?}"; shift 2 ;;
    --top) TOP="${2:?}"; shift 2 ;;
    *) echo "usage: bash scripts/screen.sh [--json] [--sleeve core|tactical|all] [--top N]" >&2; exit 1 ;;
  esac
done

if [[ "$SLEEVE" == "all" ]]; then
  "$0" --sleeve core     --top "$TOP" $([[ $FORMAT == json ]] && echo --json)
  echo
  "$0" --sleeve tactical --top "$TOP" $([[ $FORMAT == json ]] && echo --json)
  exit 0
fi
# Each sleeve is judged on its own timeframe. CORE filters are only meaningful
# on daily bars, TACTICAL only on hourly.
case "$SLEEVE" in
  core)     IV="D"  ;;
  tactical) IV="60" ;;
  *) echo "unknown sleeve: $SLEEVE (core|tactical|all)" >&2; exit 1 ;;
esac

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

bash scripts/bybit.sh tickers > "$TMP/tickers.json"

# --- liquidity gate: pick the universe worth pulling bars for ------------------
TOP="$TOP" python "$ROOT/scripts/lib/universe.py" "$TMP/tickers.json" "$TMP/universe.txt"

# --- fetch bars, one call per symbol ------------------------------------------
: > "$TMP/bars.ndjson"
n=0
while read -r sym; do
  [[ -z "$sym" ]] && continue
  # A single dead symbol must not abort the whole screen; skip and carry on.
  if bash scripts/bybit.sh bars "$sym" "$IV" 200 > "$TMP/k.json" 2>/dev/null; then
    python "$ROOT/scripts/lib/klines.py" "$sym" "$TMP/k.json" >> "$TMP/bars.ndjson" || true
    n=$((n+1))
  fi
done < "$TMP/universe.txt"
echo "fetched bars for $n symbols [$IV]" >&2

FORMAT="$FORMAT" SLEEVE="$SLEEVE" IV="$IV" \
  python "$ROOT/scripts/lib/score.py" "$TMP/bars.ndjson" "$TMP/tickers.json"
