#!/usr/bin/env bash
# Alpaca API wrapper. All trading API calls go through here.
# Usage: bash scripts/alpaca.sh <subcommand> [args...]

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

# env.template ships "your_..._here" placeholders. They are NON-EMPTY, so a naive
# -z check would pass them through to the API and produce a 401 instead of the
# intended graceful fallback. Normalize any placeholder value to empty.
for _v in ALPACA_API_KEY ALPACA_SECRET_KEY PERPLEXITY_API_KEY PERPLEXITY_MODEL           CLICKUP_API_KEY CLICKUP_WORKSPACE_ID CLICKUP_CHANNEL_ID; do
  case "${!_v:-}" in
    your_*_here) unset "$_v" ;;
  esac
done
unset _v

: "${ALPACA_API_KEY:?ALPACA_API_KEY not set in environment}"
: "${ALPACA_SECRET_KEY:?ALPACA_SECRET_KEY not set in environment}"

API="${ALPACA_ENDPOINT:-https://api.alpaca.markets/v2}"
DATA="${ALPACA_DATA_ENDPOINT:-https://data.alpaca.markets/v2}"

H_KEY="APCA-API-KEY-ID: $ALPACA_API_KEY"
H_SEC="APCA-API-SECRET-KEY: $ALPACA_SECRET_KEY"

cmd="${1:-}"
shift || true

case "$cmd" in
  account)
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/account"
    ;;
  positions)
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/positions"
    ;;
  position)
    sym="${1:?usage: position SYM}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/positions/$sym"
    ;;
  quote)
    sym="${1:?usage: quote SYM}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$DATA/stocks/$sym/quotes/latest"
    ;;
  assets)
    class="${1:-crypto}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/assets?asset_class=$class&status=active"
    ;;
  crypto-quote)
    sym="${1:?usage: crypto-quote BTC/USD}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC"       --get --data-urlencode "symbols=$sym"       "${ALPACA_CRYPTO_DATA_ENDPOINT:-https://data.alpaca.markets/v1beta3/crypto/us}/latest/quotes"
    ;;
  crypto-bars)
    # NOTE: `limit` is a TOTAL across all requested symbols, not per symbol, AND
    # the response is PAGINATED regardless of limit. A multi-symbol request
    # returns only the first page (symbols are filled in order, so later symbols
    # come back short or empty) plus a next_page_token. Callers MUST follow the
    # token or they will silently score an incomplete universe.
    sym="${1:?usage: crypto-bars 'BTC/USD[,ETH/USD]' [timeframe] [start] [limit] [page_token]}"
    tf="${2:-1D}"; start="${3:-}"; lim="${4:-10000}"; page="${5:-}"
    if [[ -z "$start" ]]; then
      start="$(python -c "import datetime;print((datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=45)).strftime('%Y-%m-%d'))")"
    fi
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC"       --get --data-urlencode "symbols=$sym"             --data-urlencode "timeframe=$tf"             --data-urlencode "start=$start"             --data-urlencode "limit=$lim"             ${page:+--data-urlencode "page_token=$page"}       "${ALPACA_CRYPTO_DATA_ENDPOINT:-https://data.alpaca.markets/v1beta3/crypto/us}/bars"
    ;;
  clock)
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/clock"
    ;;
  orders)
    status="${1:-open}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" "$API/orders?status=$status"
    ;;
  order)
    body="${1:?usage: order '<json>'}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" -H "Content-Type: application/json" \
      -X POST -d "$body" "$API/orders"
    ;;
  cancel)
    oid="${1:?usage: cancel ORDER_ID}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" -X DELETE "$API/orders/$oid"
    ;;
  cancel-all)
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" -X DELETE "$API/orders"
    ;;
  close)
    sym="${1:?usage: close SYM}"
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" -X DELETE "$API/positions/$sym"
    ;;
  close-all)
    curl --fail-with-body -sS -H "$H_KEY" -H "$H_SEC" -X DELETE "$API/positions"
    ;;
  *)
    echo "Usage: bash scripts/alpaca.sh <account|positions|position|quote|crypto-quote|crypto-bars|assets|clock|orders|order|cancel|cancel-all|close|close-all> [args]" >&2
    exit 1
    ;;
esac
echo
