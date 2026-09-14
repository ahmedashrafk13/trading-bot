#!/usr/bin/env bash
# Research wrapper. All market research goes through Perplexity.
# Usage: bash scripts/perplexity.sh "<query>"
# Exits with code 3 if PERPLEXITY_API_KEY is unset so callers can fall back.

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

query="${1:-}"
if [[ -z "$query" ]]; then
  echo "usage: bash scripts/perplexity.sh \"<query>\"" >&2
  exit 1
fi

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "WARNING: PERPLEXITY_API_KEY not set. Fall back to WebSearch." >&2
  exit 3
fi

MODEL="${PERPLEXITY_MODEL:-sonar}"

PY="$(command -v python3 || command -v python)"
: "${PY:?python or python3 required to build the request payload}"

payload="$("$PY" -c "
import json, sys
print(json.dumps({
    'model': sys.argv[1],
    'messages': [
        {'role': 'system', 'content': 'You are a precise financial research assistant. Cite every claim. Be concise.'},
        {'role': 'user', 'content': sys.argv[2]},
    ],
}))
" "$MODEL" "$query")"

curl -fsS https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$payload"
echo
