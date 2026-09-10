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
- PDT: 3 day trades per 5 rolling business days under $25k. Check daytrade_count before buying.
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
- Trailing stops only work during market hours. Overnight gaps can blow through them.
- Env var is ALPACA_API_KEY; the HTTP header is APCA-API-KEY-ID. The wrapper translates.
- Alpaca timestamps are UTC. Crons are in the routine's timezone. Convert carefully.
