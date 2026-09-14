#!/usr/bin/env bash
# The $200 book performance panel: what has the bot actually made?
#
# Usage: bash scripts/pnl.sh [--json]
#
# Counts ONLY orders the bot tagged with the BOT_TAG orderLinkId prefix, so the
# demo account's pre-existing balances, stale orders and perp position are
# excluded. See scripts/lib/book.py for why the account's own equity cannot be
# used as the denominator.
#
# Side effect: refreshes memory/LEDGER.json with any newly-seen fills. That file
# is the durable record — /v5/execution/list has a retention window, and once a
# fill ages out of the API the ledger is the only thing keeping the book honest.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# Follow the cursor to exhaustion; a truncated fill list silently misstates P&L.
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

bash scripts/bybit.sh tickers > "$TMP/tickers.json"

PYTHONPATH="$ROOT/scripts/lib" python "$ROOT/scripts/lib/panel.py" \
  "${files[@]}" --tickers "$TMP/tickers.json" "$@"
