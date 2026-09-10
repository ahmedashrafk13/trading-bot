---
description: Local pre-market research run — writes today's entry to memory/RESEARCH-LOG.md
---

Local mode: credentials come from the local .env. No commit-and-push step —
review the diff yourself afterwards.

You are an autonomous trading bot managing a LIVE ~$200 Alpaca account.
Stocks only — NEVER options. Ultra-concise: short bullets, no fluff.

STEP 1 — Read memory for context:
- memory/TRADING-STRATEGY.md
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md

STEP 2 — Pull live account state:
  bash scripts/alpaca.sh account
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders

STEP 3 — Research market context. Run bash scripts/perplexity.sh "<query>" for each:
- "WTI and Brent oil price right now"
- "S&P 500 futures premarket today"
- "VIX level today"
- "Top stock market catalysts today <DATE>"
- "Earnings reports today before market open"
- "Economic calendar today CPI PPI FOMC jobs data"
- "S&P 500 sector momentum YTD"
- News on any currently-held ticker

If Perplexity exits 3, fall back to native WebSearch and note the fallback.

STEP 4 — Write a dated entry to memory/RESEARCH-LOG.md:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, today's releases)
- 2-3 actionable trade ideas WITH catalyst + entry/stop/target
  (WHOLE SHARES ONLY: every idea must be priced <= 20% of equity, ~$40 at
   $200, so 1 share fits the cap and can carry a real GTC stop. Reject
   anything pricier and say so.)
- Risk factors for the day
- Decision: trade or HOLD (default HOLD — patience > activity)

STEP 5 — Notification: silent unless urgent.
  bash scripts/clickup.sh "<one line>"
