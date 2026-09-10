# Trading Strategy

## Mission
Beat the S&P 500 over the challenge window. Stocks only — no options, ever.

## Capital & Constraints
- Starting capital: ~$200
- Platform: Alpaca
- Instruments: Stocks ONLY
- PDT limit: 3 day trades per 5 rolling days (account < $25k)
- Max position size: 20% of equity = ~$40 at $200 equity

### Share-price ceiling (consequence of the $200 account)
WHOLE SHARES ONLY. Alpaca does not accept `stop`, `stop_limit` or
`trailing_stop` orders for fractional quantities, and fractional orders
cannot use `time_in_force: gtc` — they are market/limit + day only. So a
fractional position CANNOT carry the mandatory stop from Core Rule 4.

Therefore: only trade tickers where at least 1 whole share fits inside the
20% cap. At $200 equity that means a share price of **<= ~$40**. If a
candidate trades above that, SKIP IT and log "share price exceeds 20% cap".
Do NOT buy a fractional share and do NOT hold any position without a stop.

Practical shape of the book at $200: 4 positions of ~$40 each = 80% deployed,
which sits inside the 75-85% target. Under $40/share, 5-6 smaller positions
also work.

## Core Rules
1. NO OPTIONS — ever
2. 75-85% deployed
3. 5-6 positions at a time, max 20% each
4. 10% trailing stop on every position as a real GTC order
5. Cut losers at -7% manually
6. Tighten trail: 7% at +15%, 5% at +20%
7. Never within 3% of current price; never move a stop down
8. Max 3 new trades per week
9. Follow sector momentum
10. Exit a sector after 2 consecutive failed trades
11. Patience > activity

## Entry Checklist
- Specific catalyst?
- Sector in momentum?
- Stop level (7-10% below entry)
- Target (min 2:1 R:R)

## Buy-Side Gate (all must pass, else skip and log the reason)
- Total positions after this fill <= 6
- Trades placed this week (including this one) <= 3
- Position cost <= 20% of account equity (~$40 at $200)
- Position cost <= available cash
- qty is a WHOLE number >= 1 (never fractional — a fractional position cannot
  carry the mandatory GTC stop)
- Share price <= 20% of equity, so 1 whole share fits the cap
- daytrade_count leaves room (< 3 on a sub-$25k account)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The instrument is a stock

## Sell-Side Rules
- Unrealized P&L <= -7% -> close immediately
- Thesis broken (catalyst invalidated, sector rolling over, news event) -> close, even above -7%
- Up >= +20% -> tighten trailing stop to 5%
- Up >= +15% -> tighten trailing stop to 7%
- Sector with 2 consecutive failed trades -> exit all positions in that sector
