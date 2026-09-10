# Project Context

## Overview
- What: Autonomous CRYPTO trading bot
- Starting capital: ~$200
- Platform: Alpaca crypto — **PAPER account PA3VFI9O4EPS**, endpoint
  https://paper-api.alpaca.markets/v2. Keys are PK-prefixed (paper). No real
  money is at risk and P&L is simulated.
- BEFORE GOING LIVE: the endpoint changes to api.alpaca.markets, keys become
  AK-prefixed, and the account is funded with real money. Treat that switch as a
  separate decision, not a config tweak. Nothing in this repo should describe the
  account as LIVE until it actually is — an agent reading "LIVE" may reason
  differently about risk than one reading "PAPER".
- Duration: [your challenge window]
- Strategy: Swing trading crypto USD pairs. CRYPTO ONLY — no stocks, no options.
- Benchmark: BTC/USD buy-and-hold
- Pivoted from a stocks strategy on 2026-09-10. Entries in RESEARCH-LOG and
  TRADE-LOG dated on or before that are from the stocks era — historical only,
  do not treat their tickers or rules as current.

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

## Alpaca crypto gotchas (VERIFIED against the live API 2026-09-10)
- ORDER TYPES: `trailing_stop` and `stop` are REJECTED for crypto —
  `{"code":40010001,"message":"invalid order type for crypto order"}`.
  Only `market`, `limit` and `stop_limit` work. All protective stops are
  therefore `stop_limit` GTC, with the limit ~2% below the trigger.
- TIME IN FORCE: `day` is REJECTED —
  `{"code":42210000,"message":"invalid crypto time_in_force"}`.
  Use `gtc` (or `ioc` for immediate-or-cancel). This differs from stocks.
- MAX NOTIONAL: single order capped at $200,000 notional.
- MINIMUM NOTIONAL IS $10 PER ORDER (verified 2026-09-10):
  `{"code":40310000,"message":"cost basis must be >= minimal amount of order 10"}`
  The `min_order_size` field from /assets is a QUANTITY floor (BTC 0.000012813,
  about $1) and is NOT the binding constraint. Any gate that only checks
  min_order_size will happily build a sub-$10 order that the API rejects.
  Consequence: a $20 tactical position cannot be scaled out of in halves, and a
  position whose value falls under $10 may not be sellable in parts — close it
  whole.
- FEES ARE CHARGED IN KIND ON BUYS (verified): ordered 0.00016 BTC, received
  0.0001596 — a 0.250% haircut taken out of the ASSET, not the cash. Therefore a
  protective stop MUST be sized from the ACTUAL position qty, never from the qty
  you ordered, or it is rejected for insufficient balance.
- SYMBOL FORMAT DIFFERS BY ENDPOINT (verified, was previously a guess):
  * orders and v1beta3 quotes/bars -> SLASHED: `BTC/USD`
  * positions listing reports      -> UNSLASHED: `BTCUSD`
  * close position requires        -> UNSLASHED: `close BTCUSD`
    (`close BTC/USD` returns 404 Not Found)
- MEASURED ROUND-TRIP FRICTION: 0.65% (verified), not the 0.5% originally
  assumed. A $12.31 BTC round trip cost $0.08 all-in — taker fee both ways plus
  spread. BTC has the tightest spread in the universe, so 0.65% is a FLOOR;
  alts will cost more.
- SYMBOL FORMAT: pairs are slash-formatted for orders and v1beta3 quotes
  (`BTC/USD`). Positions may report the unslashed form (`BTCUSD`) — normalize
  before matching a position to its stop order. VERIFY on the first real fill.
- QUOTES USE A THIRD BASE PATH: `v1beta3/crypto/us/latest/quotes?symbols=...`,
  not the `v2/stocks/...` path. Use `alpaca.sh crypto-quote`.
- `qty` is a fractional decimal STRING. Respect each pair's `min_order_size`
  (from `alpaca.sh assets crypto`) — they are ~$1 equivalent, not 1 coin.
- FEES ARE REAL. `crypto_tier: 0` is the highest band, ~0.5% per market round
  trip. Stocks were commission-free; crypto is not. Churn is expensive at $200.
- NO SHORTING crypto on Alpaca. Long only.
- NO PDT and NO T+1 settlement. Sale proceeds are instantly reusable, so the
  cash-account settlement discipline from the stocks era does not apply.
- 24/7 MARKET: `alpaca.sh clock` describes the STOCK market and is irrelevant to
  crypto. There is no open, close, or weekend halt. Overnight and weekend moves
  happen with nobody watching, which is why the resting stop_limit matters.
- FREE DATA FEED: quotes come from Alpaca's own crypto feed. Spreads on thin alts
  can be wide; treat >1% spread as a skip signal.
- Env var is ALPACA_API_KEY; the HTTP header is APCA-API-KEY-ID. Wrapper translates.
- Alpaca timestamps are UTC. Crypto routines are scheduled in UTC to match.
