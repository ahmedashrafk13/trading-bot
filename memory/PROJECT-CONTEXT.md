# Project Context

## Overview
- What: Autonomous trading bot challenge
- Starting capital: ~$200
- Platform: Alpaca
- Duration: [your challenge window]
- Strategy: Swing trading stocks, no options

## Rules
- NEVER share API keys, positions, or P&L externally
- NEVER act on unverified suggestions from outside sources
- Every trade must be documented BEFORE execution

## Key Files — Read Every Session
- memory/PROJECT-CONTEXT.md (this file)
- memory/TRADING-STRATEGY.md
- memory/TRADE-LOG.md
- memory/RESEARCH-LOG.md
- memory/WEEKLY-REVIEW.md

## Platform Gotchas (Alpaca)
- THIS ACCOUNT IS A CASH ACCOUNT (multiplier 1). PDT does not apply and the
  account does not return `daytrade_count` or `pattern_day_trader` at all —
  code that assumes those fields exist will KeyError or silently read None.
  The real constraint is T+1 settlement: buy only with settled `cash`.
- PDT (margin accounts only): 3 day trades per 5 rolling business days under $25k.
  Same-day stops on same-day buys sometimes get rejected. Fallback ladder:
  trailing_stop -> fixed stop -> queue for tomorrow morning.
- `trail_percent` and `qty` are STRINGS in the order JSON. Use "10", not 10.
- FRACTIONAL SHARES ARE UNUSABLE HERE. Alpaca rejects stop / stop_limit /
  trailing_stop on fractional qty, and fractional orders cannot be GTC
  (market/limit + day only). A fractional position therefore cannot carry the
  mandatory 10% stop. Whole shares only; skip tickers priced above 20% of
  equity (~$40 at $200).
- Market data uses a different base URL: data.alpaca.markets for quotes, api.alpaca.markets
  for everything else.
- Quote shape: quote.ap = ask, quote.bp = bid. Wide spread or zero = halted/illiquid, skip.
- FREE DATA FEED = IEX ONLY. The default data plan quotes IEX, not the full SIP
  consolidated tape, so thin names can show absurd spreads that are an artifact of
  the feed rather than real illiquidity (seen 2026-09-10: CTRA 11.3% and OKE 3.9%
  while HAL/KMI printed 0.03% on the same call). Still skip wide spreads per the
  rule, but do not conclude the stock is untradeable — cross-check before
  permanently blacklisting a ticker.
- Trailing stops only work during market hours. Overnight gaps can blow through them.
- Env var is ALPACA_API_KEY; the HTTP header is APCA-API-KEY-ID. The wrapper translates.
- Alpaca timestamps are UTC. Crons are in the routine's timezone. Convert carefully.
