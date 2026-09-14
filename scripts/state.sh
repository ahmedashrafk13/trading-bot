#!/usr/bin/env bash
# Computes the numbers every guardrail depends on, so no run has to do
# arithmetic over markdown. Read-only apart from refreshing memory/LEDGER.json.
#
# Usage: bash scripts/state.sh
#
# Emits: UTC now (from the BYBIT SERVER clock, never the local machine clock),
# the $200 book's equity/cash/deployment, open positions with age and stop
# coverage, the weekly fee budget, today's realized P&L for the circuit breaker,
# and the count of closed trades since the last applied amendment.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

bash scripts/bybit.sh orders  > "$TMP/orders.json"
bash scripts/bybit.sh tickers > "$TMP/tickers.json"

cursor=""; page=0; files=()
while :; do
  out="$TMP/fills.$page.json"
  bash scripts/bybit.sh fills 100 "$cursor" > "$out"
  files+=("$out")
  cursor="$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print((d.get('result') or {}).get('nextPageCursor') or '')
" "$out")"
  page=$((page+1))
  [[ -z "$cursor" || $page -ge 50 ]] && break
done

PYTHONPATH="$ROOT/scripts/lib" python "$ROOT/scripts/lib/state.py" \
  "$TMP/orders.json" "$TMP/tickers.json" "${files[@]}"
