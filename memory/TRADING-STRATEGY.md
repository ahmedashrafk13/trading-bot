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

## Two sleeves
Capital is split so that "more trades" and "let good trades run" can coexist
without fighting each other. A 20% trailing stop implies week-long holds; 2-3
trades a day implies hour-long holds. They cannot be the same position.

| | CORE | TACTICAL |
|---|---|---|
| Allocation | ~$120 (60%) | ~$80 (40%) |
| Position size | $40 (20% of equity) | $20 (10% of equity) |
| Max positions | 3 | 3 |
| New trades | max 3 per WEEK | max 3 per DAY |
| Stop | 20% below high-water, ratcheted | 6% below entry, to breakeven at +6% |
| Target | none — let winners run, no time limit | +12% (2:1 after fees) |
| Screen timeframe | daily bars | hourly bars |
| Hold horizon | weeks to months | hours to ~2 days |

- Combined cap: 6 positions, and total deployment stays in the 75-85% band
  (e.g. 3 core + 2 tactical = $160 = 80%).
- CORE is where "long trades if it is good" lives: there is NO time limit and NO
  profit target. A core winner is held until its ratcheted stop takes it out.
- TACTICAL positions that have neither hit target nor stop within ~48h are
  reassessed and closed unless the setup is still valid. Dead money pays fees.

## Fee reality for the tactical sleeve
3 tactical trades/day at $20 = ~$0.30/day = ~$2.10/week = ~1.05% of the account
PER WEEK, or roughly 55%/yr in fees alone. That is the accepted cost of trading
this frequently on a $200 account at tier-0 pricing. It means:
- The tactical sleeve must clear ~1% per week gross just to break even.
- A tactical setup that is not clearly better than 2:1 after fees is a PASS.
- If the weekly review shows fees exceeded tactical gross profit two weeks
  running, propose cutting tactical frequency. Do not silently keep churning.

## Core Rules
1. CRYPTO ONLY — no stocks, no options, ever
2. Long only — never attempt a short
3. 75-85% deployed across both sleeves
4. Respect each sleeve's position count, size and trade cap (table above)
5. EVERY position carries a resting `stop_limit` GTC sell at the broker
6. CORE: hard cut at -15%; trail 20% below high-water, ratcheted UP only;
   tighten to 14% at +30% and 10% at +40%
7. TACTICAL: hard stop 6% below entry; raise to breakeven once +6%; exit at
   +12% target; never widen a tactical stop
8. Never place a stop within 5% of current price (2% for tactical); NEVER move
   any stop down
9. Never hold a stablecoin as a position
10. Follow narrative momentum; exit a narrative after 2 consecutive failed
    trades in it (counted per sleeve)
11. Patience > activity. Zero trades is a valid day, especially in CORE.

## Technical entry filters (run `bash scripts/screen.sh`)
Catalyst alone is not enough — news concentrates on coins that have ALREADY
moved, so a news-only bot buys strength late. Every entry must also clear its
sleeve's technical screen. The screener ranks all 33 tradable non-stablecoin
pairs and prints a PASS/fail with reasons.

CORE (daily bars):
- 30-period momentum > 0
- price ABOVE SMA20 and SMA20 RISING
- price <= 20% above SMA20 (not extended)
- spread <= 1%

TACTICAL (hourly bars):
- 7-period momentum > 0
- price within +/-8% of SMA20
- realized vol between 0.4% and 6% hourly (needs movement, not chaos)
- spread <= 0.5% (fees already cost ~0.5% round trip)

If a coin fails its screen, it is NOT tradeable this run no matter how good the
news is. Log the failure reason.

## Known limitation: no OCO on crypto
Alpaca has no bracket/OCO for crypto, so a position cannot carry an automatic
stop AND an automatic target. The resting `stop_limit` covers the downside; the
+12% tactical target is taken by whichever run next observes it. With runs 6h
apart a target can be hit and given back unseen. This is the accepted cost of
the platform, and it caps how precisely the tactical sleeve can capture gains.

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
- The sleeve is stated explicitly (CORE or TACTICAL) before sizing
- CORE: positions after fill <= 3, cost ~$40, new CORE trades this WEEK <= 3
- TACTICAL: positions after fill <= 3, cost ~$20, new TACTICAL trades TODAY <= 3
- Combined positions after fill <= 6, total deployment <= 85% of equity
- Position cost <= available cash
- Pair is in the Alpaca tradable crypto USD list (`alpaca.sh assets crypto`)
- Pair is NOT a stablecoin
- qty >= that pair's `min_order_size`
- Quoted spread <= 1% (BTC/ETH run ~0.02-0.04%; a wide spread means thin book)
- `time_in_force` is `gtc` — `day` is REJECTED for crypto
  (`{"code":42210000,"message":"invalid crypto time_in_force"}`)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The coin PASSES its sleeve's technical screen (scripts/screen.sh)
- The instrument is crypto (never a stock, never an option)

## Sell-Side Rules
CORE:
- Unrealized <= -15% -> close at market, cancel the resting stop
- Thesis broken (catalyst dead, narrative rolling over, exploit/depeg/delisting)
  -> close even if not at -15%
- Up >= +40% -> ratchet stop to 10% below high-water
- Up >= +30% -> ratchet stop to 14% below high-water
- Otherwise -> keep stop 20% below high-water
- NO profit target. Let it run; the ratchet decides the exit.

TACTICAL:
- Unrealized <= -6% -> close at market, cancel the resting stop
- Up >= +12% -> close at market, take the target
- Up >= +6% -> raise the stop to breakeven (entry price), never lower
- Open > ~48h without hitting target or stop -> reassess; close unless the
  hourly screen still PASSES
- Thesis broken -> close immediately

BOTH:
- Narrative with 2 consecutive failed trades -> exit all positions in it
- Any position found WITHOUT a resting stop_limit -> place one immediately

## Every-Run Invariants
Because crypto trades 24/7 and runs are 6h apart, every run (not just one of
them) must:
1. Reconcile live positions against TRADE-LOG (a fill may have happened between runs)
2. Verify every position has a resting stop_limit; place one if missing
3. Close anything at or below -15% that the stop failed to catch
4. Ratchet stops upward where the high-water mark has risen (CORE), and raise
   tactical stops to breakeven once +6%
5. Tag every position in TRADE-LOG with its sleeve. An untagged position cannot
   be managed by the right rules — if the tag is missing, infer it from position
   size ($40 = CORE, $20 = TACTICAL) and record it.
