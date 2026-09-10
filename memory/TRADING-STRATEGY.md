# Trading Strategy — Crypto

## Mission
Grow a ~$200 Alpaca crypto account. CRYPTO ONLY — no stocks, no options, ever.
Benchmark is BTC/USD buy-and-hold, not the S&P 500: beating a rising BTC is the
only result that justifies active trading.

## Capital & Constraints
- Starting capital: ~$200
- Platform: Alpaca crypto (`crypto_status: ACTIVE`, `crypto_tier: 0`)
- Instruments: Alpaca tradable crypto USD pairs ONLY (36 available)
- Account type: cash, long only. Alpaca does NOT support shorting crypto.
- Max position size: 20% of equity = ~$40 at $200 equity
- Fractional is native (min order sizes are ~$1 equivalent), so there is NO
  whole-share ceiling and any of the 36 pairs is reachable at this size.
- NO PDT rule and NO T+1 settlement — crypto settles instantly. Proceeds from a
  sale are immediately reusable.

## Fees — the thing that punishes churn
`crypto_tier: 0` is Alpaca's highest fee band. A market round trip costs roughly
0.5% of the position. On $40 that is ~$0.20 per round trip, and it is charged
whether the trade wins or loses. Consequences that are part of the strategy:
- Every stop-out costs the spread AND the fees. Frequent small stops bleed.
- The 3-trades-per-week cap is a FEE control, not just a discipline rule.
- Require a minimum 2:1 reward:risk AFTER assuming 0.5% friction.

## Core Rules
1. CRYPTO ONLY — no stocks, no options, ever
2. Long only — never attempt a short
3. 75-85% deployed
4. Max 5 positions at a time, max 20% each (~$40)
5. Every position carries a resting `stop_limit` GTC sell order at the broker
6. Hard cut at -15% from entry
7. Trailing stop = 20% below the high-water mark, ratcheted UP only
8. Tighten the trail to 14% once up +30%; to 10% once up +40%
9. Never place a stop within 5% of current price; NEVER move a stop down
10. Max 3 new trades per week
11. Follow narrative momentum (see below); exit a narrative after 2 consecutive
    failed trades in it
12. Never hold a stablecoin as a position (USDC/USDT have no upside)
13. Patience > activity. A week with zero trades is often correct.

## Stops — how they actually work here (READ THIS)
Alpaca REJECTS `trailing_stop` and `stop` for crypto:
`{"code":40010001,"message":"invalid order type for crypto order"}`
Only `stop_limit` is accepted. So Core Rule 5 is implemented as:

    {"symbol":"BTC/USD","qty":"<frac>","side":"sell","type":"stop_limit",
     "stop_price":"<trigger>","limit_price":"<trigger * 0.98>","time_in_force":"gtc"}

- `limit_price` is set 2% BELOW `stop_price` so it can still fill while price is
  falling. A limit equal to the stop will often not fill at all.
- KNOWN RISK: a stop_limit can be gapped through. In a violent drop price can
  pass the limit without filling, leaving the position open and unprotected.
  This is the price of crypto having no stop-market order. Every run must
  therefore verify the stop actually exists and force-close anything that
  breached -15% without filling.
- "Trailing" is EMULATED. There is no trailing order type, so each run cancels
  the existing stop_limit and re-places it higher when the high-water mark rises.
  Never re-place lower.

## Narrative momentum (the crypto analogue of sectors)
Group holdings by narrative and apply the 2-consecutive-failures rule per group.
This covers ALL 33 non-stablecoin tradable pairs — every position must map to a
group, or the failure rule silently does not apply to it.
- Majors: BTC, ETH
- Payments/legacy: XRP, LTC, BCH
- L1/L2: SOL, AVAX, DOT, ADA, ARB, POL, XTZ
- DeFi: UNI, AAVE, LINK, CRV, LDO, SUSHI, ONDO, SKY, YFI
- Memes: DOGE, SHIB, PEPE, BONK, TRUMP, WIF
- Infra/AI: RENDER, GRT, FIL, HYPE, BAT
- Commodity-backed: PAXG
EXCLUDED as positions (stablecoins, no upside): USDC, USDG, USDT

## Entry Checklist (document all before placing)
- What is the specific catalyst? (unlock, upgrade, listing, ETF flow, macro)
- Is the narrative in momentum, or is it rolling over?
- Where is the -15% hard cut in dollars?
- Where is the initial stop_limit (trigger and limit)?
- What is the target, minimum 2:1 R:R after 0.5% fees?

## Buy-Side Gate (ALL must pass, else skip and log the reason)
- Total positions after this fill <= 5
- Trades placed this week (including this one) <= 3
- Position cost <= 20% of equity (~$40 at $200)
- Position cost <= available cash
- Pair is in the Alpaca tradable crypto USD list (`alpaca.sh assets crypto`)
- Pair is NOT a stablecoin
- qty >= that pair's `min_order_size`
- Quoted spread <= 1% (BTC/ETH run ~0.02-0.04%; a wide spread means thin book)
- `time_in_force` is `gtc` — `day` is REJECTED for crypto
  (`{"code":42210000,"message":"invalid crypto time_in_force"}`)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The instrument is crypto (never a stock, never an option)

## Sell-Side Rules
- Unrealized P&L <= -15% -> close immediately at market, cancel the resting stop
- Thesis broken (catalyst invalidated, narrative rolling over, exploit/depeg/
  delisting news) -> close, even if not yet at -15%
- Up >= +40% -> ratchet the stop to 10% below the high-water mark
- Up >= +30% -> ratchet the stop to 14% below the high-water mark
- Otherwise -> keep the stop 20% below the high-water mark
- Narrative with 2 consecutive failed trades -> exit all positions in it
- Any position found WITHOUT a resting stop_limit -> place one immediately

## Every-Run Invariants
Because crypto trades 24/7 and runs are 6h apart, every run (not just one of
them) must:
1. Reconcile live positions against TRADE-LOG (a fill may have happened between runs)
2. Verify every position has a resting stop_limit; place one if missing
3. Close anything at or below -15% that the stop failed to catch
4. Ratchet stops upward where the high-water mark has risen
