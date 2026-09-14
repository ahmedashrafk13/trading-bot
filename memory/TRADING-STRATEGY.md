# Trading Strategy — Crypto

## Mission
Grow a $200 BOOK on Bybit SPOT. CRYPTO ONLY — no stocks, no options, ever.
Benchmark is BTCUSDT buy-and-hold, not the S&P 500: beating a rising BTC is the
only result that justifies active trading.

## Capital & Constraints
- Starting capital: $200 — a VIRTUAL BOOK, not the account balance.
- Platform: Bybit V5 SPOT, Demo Trading host `https://api-demo.bybit.com`
  (verified 2026-09-15: these keys are rejected by `api.bybit.com` with 10003,
  so the bot CANNOT touch real funds).
- THE ACCOUNT IS NOT THE BOOK. The demo account carries ~$181k equity, leftover
  coin balances, stale resting orders and an open KITEUSDT perp position from
  prior use, and Bybit demo funds can only be ADDED, never withdrawn — so the
  account can never be shrunk to $200. Every bot order therefore carries an
  `orderLinkId` prefixed `tb-`, and ALL accounting counts only tagged fills.
  Read `bash scripts/pnl.sh`, never the raw account equity.
- Every equity-relative rule (fee budget, circuit breaker, deployment %) is
  measured against the $200 BOOK. Against account equity the fee budget would be
  ~$2,700/week and the circuit breaker ~$5,400 — i.e. both would be disabled.
- Instruments: Bybit SPOT USDT pairs (388 live, vs 36 on Alpaca). Spot only —
  no perps, no leverage, no liquidation risk.
- Account type: spot, long only. Shorting would require derivatives, which this
  strategy does not use.
- Max position size: 20% of the book = $40.
- Fractional is native, but each symbol has its OWN `basePrecision`,
  `minOrderQty` and `minOrderAmt` (`bash scripts/bybit.sh instruments SYM`).
  `minOrderAmt` is commonly 5 USDT — check before sizing, not after a rejection.

## Fees — the thing that punishes churn
Bybit spot charges ~0.1% per side. MEASURED on this account 2026-09-15: a $10
XRPUSDT round trip cost $0.02 = **0.20% per round trip**, materially cheaper
than Alpaca's measured 0.65%. On $40 that is ~$0.08 per round trip, charged
whether the trade wins or loses. Consequences that are part of the strategy:
- Every stop-out costs the spread AND the fees. Frequent small stops bleed.
- The WEEKLY FEE BUDGET is the frequency control, not a trade count.
- Require a minimum 2:1 reward:risk AFTER friction.
- Spread is now the bigger half of friction, not fees. Bybit lists 388 USDT
  pairs and the long tail is where a $200 book quietly bleeds: majors quote
  0.00-0.01%, but mid-caps run 0.1-0.3%. The screen's spread caps
  (CORE 0.10%, TACTICAL 0.15%) exist for this and are not negotiable downward
  without evidence.

## Self-amendment (the weekly review MAY change this document)
The Friday/Sunday weekly review is authorised to EDIT this file directly based
on observed trade results. It does not need human approval. Rules changed this
way must be recorded in WEEKLY-REVIEW.md with the evidence, the before value and
the after value, and committed together with the review so `git log` shows
exactly what changed and why. Any bad change is recoverable with `git revert`.

### TUNABLE — the review may change these
- Stop distances and trail percentages, and the ratchet thresholds
- Hard-cut levels (-15% core, -6% tactical) and the tactical target
- Position counts, position sizes and sleeve allocation
- The weekly fee budget (1.5%) and the circuit-breaker thresholds
- Deployment band (75-85%)
- Screen filter thresholds (momentum, SMA20 distance, vol band, spread limits)
- Screen timeframes (daily / hourly)
- Narrative groupings
- Minimum R:R

### IMMUTABLE — the review may NEVER change these
These are not preferences, they are verified facts about the platform or the
mandate. A "rule improvement" that violates one produces orders the API rejects,
or changes what this bot is:
1. CRYPTO ONLY. No stocks, no options, ever.
2. SPOT ONLY, long only. Never `category: linear`/`inverse`, never leverage.
   The account HAS an open perp position from prior use — it is not ours, do not
   manage it, do not close it, do not count it.
3. EVERY order carries `orderLinkId` = `tb-<sleeve>-<SYMBOL>-<epoch_ms>`
   (`cor`/`tac`). An untagged order is invisible to the book and therefore
   untracked, unstopped and unaccounted. No exceptions.
4. The BOOK is $200 and is independent of account equity. Every percentage rule
   is measured against the book. Read `bash scripts/pnl.sh` for the truth.
5. Stops are `orderType: Limit` + `triggerPrice` (spot TP/SL). Bybit spot has no
   `trailing_stop` order type — trailing is done by AMENDING the trigger upward.
6. Orders use `timeInForce: GTC` for resting orders, `IOC` for market entries.
7. Respect each symbol's `minOrderAmt` / `minOrderQty` / `basePrecision` from
   `bash scripts/bybit.sh instruments SYM`. `minOrderAmt` is often 5 USDT.
8. Sell quantity comes from the ACTUAL WALLET BALANCE floored to
   `basePrecision`, NEVER from the buy's `execQty`. Spot buy fees are deducted
   in the BASE coin, so the wallet always holds less than was executed —
   measured: bought 6.936737 XRP, wallet held 6.92980022, and selling 6.93
   failed with `170131 Insufficient balance`.
9. Market BUY qty is in QUOTE currency and needs `marketUnit: "quoteCoin"`;
   market SELL qty is in BASE and needs `marketUnit: "baseCoin"`.
10. Every position must carry a resting stop. The review may change the stop
    DISTANCE; it may never remove the requirement or allow a naked position.
11. Never move a stop down, and never widen a stop on an open losing position.
12. No stablecoins as positions. Memes are TACTICAL-only, never CORE.
13. A weekly fee budget must EXIST and may never exceed 3% of the book. The
    review may tune it below that; it may not remove it or raise it past that.
14. The daily circuit breaker must EXIST. Thresholds are tunable; removal is not.
15. This section itself, and the requirement to log amendments with evidence.

### When amendment may happen — EVIDENCE, not the calendar
Amendment is NOT tied to the weekly review. It may happen in ANY run that
computes the trigger, including daily, because with unbounded tactical frequency
a week is an arbitrary unit — 15 trades can happen in two days or in a month.

TRIGGER: at least **10 closed trades since the last amendment**. Below that,
change nothing and say so.
- 10, not 3. Three closed trades cannot distinguish a real effect from noise, and
  tuning on noise produces thrash: tighten a stop one day, loosen it the next,
  learn nothing, and destroy a rule that was working.
- The counter resets on every applied amendment, so two changes cannot ride on
  the same 10 trades.
- EXCEPTION — a single rule may be amended immediately, on fewer trades, if it is
  demonstrably BROKEN rather than underperforming: it produced an API rejection
  every time it was applied, or it is arithmetically unsatisfiable (as the 12%
  target was against a 2:1-after-fees requirement). A broken rule is a defect,
  not a hypothesis, and waiting for 10 trades to fix it is pointless when it
  blocks all 10.
- The weekly review still ALWAYS runs and always reports. It just may conclude
  "insufficient evidence, nothing changed", which is a valid and common outcome.

### Amendment limits (so the experiment stays legible)
- At most 2 tunable rules changed per amendment. Changing everything at once makes
  it impossible to attribute the next week's result to anything.
- Each change needs stated evidence from the logs, not a hunch.
- A parameter may not move more than 50% of its current value in one step.
- If a change is reverted twice, stop proposing it and record that it was tried.

## Two sleeves
Capital is split so that "more trades" and "let good trades run" can coexist
without fighting each other. A 20% trailing stop implies week-long holds; 2-3
trades a day implies hour-long holds. They cannot be the same position.

| | CORE | TACTICAL |
|---|---|---|
| Allocation | ~$120 (60%) | ~$80 (40%) |
| Position size | $40 (20% of equity) | $20 (10% of equity) |
| Max positions | 3 | 3 |
| New trades | agent's judgement | agent's judgement |
| Stop | 20% below high-water, ratcheted | 6% below entry, to breakeven at +6% |
| Target | none — let winners run, no time limit | +14% (2:1 AFTER fees) |
| Screen timeframe | daily bars | hourly bars |
| Hold horizon | weeks to months | hours to ~2 days |

- Combined cap: 6 positions, and total deployment stays in the 75-85% band
  (e.g. 3 core + 2 tactical = $160 = 80%).
- CORE is where "long trades if it is good" lives: there is NO time limit and NO
  profit target. A core winner is held until its ratcheted stop takes it out.
- TACTICAL positions that have neither hit target nor stop within ~48h are
  reassessed and closed unless the setup is still valid. Dead money pays fees.

## Cadence change 2026-09-14: execute now runs every 6h (NOT a rule change)
The sleeve design above targets "2-3 trades a day" in TACTICAL, but TACTICAL can
only be ORIGINATED in an execute run, and execute ran once a day. One entry
window per day cannot produce 2-3 entries per day no matter what the rules allow,
so observed frequency sat near zero-to-one while the rulebook was blameless.
Execute moved from `7 12 * * *` to `7 */6 * * *` (00:07/06:07/12:07/18:07 UTC) —
four entry windows, matching the hours-to-2-days tactical hold horizon.

NOTHING about the gate, the 2:1-after-fees requirement, the fee budget, the
circuit breaker or the position caps changed. This buys OPPORTUNITY, not looser
standards: each run still re-screens on fresh hourly bars and applies the full
gate. The fee budget still binds at ~23 round trips/week at $20 size.

The weekly review MUST NOT read a rise in trade count as evidence that the
strategy improved or degraded. Frequency rose because the bot was asked more
often. Grade expectancy per trade, not volume.

## Trade frequency: the agent decides, the FEE BUDGET binds
There is no fixed trades-per-day or trades-per-week cap. Open as many positions
as the setups justify. What is capped is the thing that actually does the damage:
cumulative friction.

MEASURED friction: 0.65% per round trip (verified — a $12.31 BTC round trip cost
$0.08, taker fee both ways plus spread). BTC has the tightest spread in the
universe, so 0.65% is a FLOOR and alts cost more.

**WEEKLY FEE BUDGET: 1.5% of equity (~$3.00 at $200).**
- Estimate the round-trip cost of every entry BEFORE placing it: notional x 0.65%
  (use more for a wide-spread alt) and add it to the running weekly total.
- Track the total in each daily snapshot as "fees used this week: $X / $3.00".
- When the budget is exhausted, STOP OPENING NEW POSITIONS for the rest of the
  UTC week. Exits are always still allowed — never let a budget trap a loser.
- The budget resets Monday 00:00 UTC.

Why a budget rather than a trade count: it self-adjusts. Bigger positions and
wider spreads buy fewer trades; cheap tight-spread entries buy more. A trade
count cannot tell the difference between a $0.13 BTC round trip and a $0.40
round trip in a thin alt, and it is the dollars that compound against you.
At $20 tactical positions, 1.5%/week is roughly 23 round trips — more than the
3/day this replaced, and it flexes with what you actually trade.

## Why the tactical target is 14% and not 12%
Set 2026-09-10 after the gate refused every tactical trade. A 6% stop with a 12%
target is 2:1 GROSS, but the 0.65% round-trip fee is charged on both legs, so the
real ratio was 1.71:1 against a required 2:1 — a failure produced by the
parameters themselves, so no candidate at any size could ever pass.
  risk  = notional*0.06 + fee      reward = notional*0.14 - fee
  at $20: risk $1.33, reward $2.67 -> 2.01:1  PASS (was 1.71:1 FAIL)
The stop stayed at 6% rather than tightening to 5% because 5% is barely outside
normal crypto session noise, and being shaken out of winners by too-tight stops
is the documented failure of the previous iteration of this strategy.
LESSON: state R:R requirements NET of fees, or the parameters silently
contradict the gate.

## Daily circuit breaker (required once frequency is unbounded)
Unbounded frequency plus a losing streak is how a small account dies in a day.
- Computed by summing the `REALIZED P&L` values on today's exit rows in
  TRADE-LOG (UTC day). Do NOT infer it from equity change — that includes
  unrealized moves on open positions and will trip or miss the breaker wrongly.
- If REALIZED losses today reach 3% of equity (~$6.00), open NO new positions
  for the rest of the UTC day. Management and exits continue.
- If 3 consecutive tactical trades close at a loss, stop opening tactical for
  the rest of the UTC day regardless of the budget.
- Record either trip in TRADE-LOG with the trigger and the time.
These exist because the agent judging its own frequency has no natural brake:
each individual trade can look reasonable while the sequence is ruinous.

## Core Rules
1. CRYPTO ONLY — no stocks, no options, ever
2. Long only — never attempt a short
3. 75-85% deployed across both sleeves
4. Respect each sleeve's position COUNT and SIZE (table above). Trade frequency
   is the agent's call, bounded by the weekly fee budget and circuit breaker.
5. EVERY position carries a resting trigger sell (`orderType: Limit` +
   `triggerPrice`, `orderFilter: tpslOrder`) GTC at the broker
6. CORE: hard cut at -15%; trail 20% below high-water, ratcheted UP only;
   tighten to 14% at +30% and 10% at +40%
7. TACTICAL: hard stop 6% below entry; raise to breakeven once +6%; exit at
   +14% target; never widen a tactical stop
8. Never place a stop within 5% of current price (2% for tactical); NEVER move
   any stop down
9. Never hold a stablecoin as a position
10. Follow narrative momentum; exit a narrative after 2 consecutive failed
    trades in it (counted per sleeve)
11. Patience > activity. Zero trades is a valid day, especially in CORE. "As many
    trades as the setups justify" is NOT a mandate to trade — an empty screen
    means no trades, and the fee budget is a ceiling, never a target to spend.

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

## Stop + take-profit: split the quantity (state-dependent)
VERIFIED 2026-09-10:
- `order_class: oco` and bracket are REJECTED for crypto, so one order cannot
  carry both legs.
- A resting order reserves only the QTY IT NAMES. A full-size stop leaves
  nothing unreserved, so a second sell fails with `available: 0` — but a
  trigger sell on part of the position and a plain limit on the rest both rest
  fine.
So a stop and a take-profit CAN coexist. The price is that the slice carrying
the take-profit has no stop and is unprotected on the downside.

Which structure applies depends on whether the position is in profit:

**IF NO SCAN CADENCE IS RUNNING -> SPLIT AT ENTRY, regardless of P&L.**
The rungs below assume an hourly scan exists to move them. When no routine is
scheduled (as of 2026-09-10 none is — the org GitHub entitlement is still
blocking), a position that waits for +6% to gain its target leg will NEVER get
one, so upside capture is permanently zero while downside is covered. In that
state, split at entry: half stop, half resting limit at the target. The cost is
an unstopped half; the alternative is a guaranteed-zero upside, which is worse.
Re-evaluate this clause the moment routines are live.

**THIS APPLIES TO CORE TOO — amended 2026-09-11 under the BROKEN-rule exception.**
CORE nominally has no profit target because "the ratchet decides the exit". But the
ratchet is EMULATED: it only moves when a RUN cancels the stop and re-places it
higher. With no cadence scheduled, no run ever happens, so a CORE position has a
static stop and NO upside exit mechanism whatsoever — it can run +50%, round-trip
all the way back through entry to -20%, and the stop never moves once. That is not
"letting a winner run", it is holding a winner with no way to ever realise it.
So while no cadence is running, a CORE entry ALSO splits at entry:
  ~75% on the stop / ~25% on a resting limit at +30% above fill.
+30% is used because it is CORE's own first ratchet threshold — the level at which a
run WOULD have tightened the trail to 14%. Since no run will, the exchange banks a
quarter of the position there instead. Stop-heavy per the weighting rule below.
REVERT — who does it, concretely. "Reverts when routines are live" named no
actor, so nothing would ever have performed it. The rule is:
- NEW CORE entries stop getting a target leg as soon as the hourly scan is live,
  because the ratchet works again. The execute run owns this: before placing a
  CORE stop it must check whether an hourly scan has actually run (look for a
  recent `scan <timestamp>` commit in `git log`), and if so place a FULL-SIZE
  stop with no target leg.
- EXISTING split CORE positions are LEFT ALONE. No run retro-strips a resting
  target leg. Cancelling it costs fees, and the ratchet will overtake the target
  anyway if the position runs far enough.
- NEW TACTICAL entries likewise stop getting a target leg at entry once the
  hourly scan is live — added 2026-09-14, the day the cadence actually went
  live. The CORE revert above named CORE only, which left TACTICAL silently
  running the no-cadence workaround while the "flat or at a loss AND a scan
  cadence is running -> FULL-SIZE STOP" rule below said the opposite. That is a
  contradiction, not a judgement call. A new tactical entry is by definition at
  0% and below the +6% split threshold, so it takes a FULL-SIZE stop and gains
  its target leg only when the ratchet reaches breakeven, exactly as the +6%
  rung specifies. Same actor, same check: the execute run looks for a recent
  `scan <timestamp>` commit before sizing the stop.
- EXISTING split TACTICAL positions are LEFT ALONE, for the same reason as CORE:
  no run retro-strips a resting leg. XRP is 50/50 from before the cadence and
  stays that way.
So the clause expires forward, not retroactively, and a specific run owns it.
This was caught by the user after the ETH entry was opened with a full-size stop and
no target — the same defect the DOT clause above already described, missed on CORE
because CORE's "no target by design" wording hid it.

**While flat or at a loss AND a scan cadence is running -> FULL-SIZE STOP, no take-profit.**
100% of the position is covered. Protection outranks upside capture; there is no
gain to bank and an unstopped slice could ride a drop all the way down.

**Once ratcheted to breakeven or better (i.e. at +6% or more) -> SPLIT:**
- the legs must SUM to 100% of the position — a resting order reserves the qty it
  names, so 100% stop + 100% target is 200% and is rejected. This is a forced
  trade-off, not a preference.
- WEIGHT IT STOP-HEAVY (~75% stop / ~25% target). The two failure modes are not
  symmetric: if the stop fires, the un-stopped slice keeps falling with no
  protection at all; if the target fires, the un-targeted slice keeps running
  WITH its stop intact and is still captured later by the ratchet. Under-weighting
  the stop risks an unprotected position in a falling market; under-weighting the
  target only costs precision on a winner.
- The current DOT position is 50/50 because it was split before this reasoning
  was worked out. Leave it; rebalancing costs fees for a marginal gain.
- NOTE: a very small target leg may fall under an exchange minimum. Sells appear
  exempt from the $10 cost-basis floor (~$9.97 sells were accepted) but a ~$5 leg
  is UNTESTED. Verify before relying on a 25% leg at a $20 notional.
Now the target is enforced by the EXCHANGE, 24/7, with no run required — which
is the whole point, since a spike that reverses between runs was otherwise
invisible. The unstopped half is acceptable here ONLY because the ratchet has
already moved the exit to entry or above: the worst case on that half is giving
back an unrealised gain, not taking a loss.
- Every run must check for an ORPHANED leg: if one side filled, cancel the other
  and re-place a full-size stop on whatever qty remains.

TACTICAL ratchet ladder (each step AMENDS the resting trigger higher — amend,
not cancel+replace, which leaves a naked window):
- at +6%  -> stop to BREAKEVEN, and SPLIT: half stop / half limit at +14%
- at +10% -> stop leg to entry +4%
- at +14% -> the resting limit should fill on its own; if a run sees >= +14% and
  the limit has not filled, close at market
- above +14% -> trail the stop leg 5% below the high-water mark

## Stops — how they actually work here (READ THIS)
Bybit spot implements a stop as an ordinary order carrying a `triggerPrice`.
There is no `trailing_stop` order type on spot. Core Rule 5 is implemented as:

    {"category":"spot","symbol":"XRPUSDT","side":"Sell","orderType":"Limit",
     "qty":"<wallet balance floored to basePrecision>",
     "triggerPrice":"<trigger>","price":"<trigger * 0.95>",
     "orderFilter":"tpslOrder","timeInForce":"GTC",
     "orderLinkId":"tb-<sleeve>-<SYMBOL>-<epoch_ms>"}

- `qty` comes from the WALLET BALANCE, never from the entry's `execQty` — the
  buy fee was taken in the base coin. See IMMUTABLE #8.
- `price` sits 5% BELOW `triggerPrice` so it can still fill while price is
  falling. A limit equal to the trigger will often not fill at all.
- 5%, not 2%. A triggered limit only fills if price trades between the trigger
  and the limit; in a crypto flush 2% of room is routinely jumped, which turns
  the stop into a no-op and leaves the position riding down. 5% accepts a worse
  fill in exchange for actually filling. A bad fill is a cost; an unfilled stop
  is a loss of unbounded size.
- KNOWN RISK: it can still be gapped through. Every run must verify the stop
  exists and force-close anything that breached -15% without filling.
- "Trailing" is EMULATED, but BETTER than on Alpaca: Bybit supports
  `/v5/order/amend`, so raising a stop is ONE amend call
  (`bash scripts/bybit.sh amend '{...,"triggerPrice":"<higher>"}'`) instead of
  cancel-then-replace. That matters — cancel/replace has a window where the
  position is naked, and a run that crashed between the two steps left it
  unprotected. Amend has no such window. Never amend a trigger downward.

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
- Where is the initial stop (triggerPrice and limit price)?
- What is the target, minimum 2:1 R:R after 0.20% measured friction?

## Buy-Side Gate (ALL must pass, else skip and log the reason)
- The sleeve is stated explicitly (CORE or TACTICAL) before sizing
- CORE: positions after fill <= 3, cost ~$40
- TACTICAL: positions after fill <= 3, cost ~$20
- Estimated round-trip fee for THIS trade + fees already used this week
  <= 1.5% of equity (~$3.00). If it would breach, SKIP and log the budget state.
- Circuit breaker not tripped: realized losses today < 3% of equity, and not
  3 consecutive tactical losses today
- Combined positions after fill <= 6, total deployment <= 85% of the $200 BOOK
- Position cost <= available cash
- Pair is a live Bybit SPOT USDT pair (`bybit.sh instruments SYMUSDT`)
- Pair is NOT a stablecoin
- Order notional >= that pair's `minOrderAmt` (commonly 5 USDT) AND
  qty >= `minOrderQty`, rounded to `basePrecision`. Violations reject with
  `170136` / `170140`.
- Quoted spread <= 0.10% CORE / 0.15% TACTICAL. Bybit lists 388 USDT pairs and
  the long tail is where a $200 book bleeds (BTC/ETH 0.000%, MOG 0.293%).
- 24h turnover >= $20M CORE / $5M TACTICAL.
- Memes are TACTICAL-only, never CORE.
- `timeInForce` is `GTC` for resting orders, `IOC` for market entries
- `orderLinkId` is set to `tb-<sleeve>-<SYMBOL>-<epoch_ms>` — an untagged order
  is invisible to the $200 book
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
- Up >= +6% -> ratchet stop to BREAKEVEN, then SPLIT the qty: half on the stop,
  half on a resting limit sell at the +14% target (exchange-enforced upside)
- Up >= +10% -> move the stop leg to entry +4%
- Up >= +14% -> the resting limit fills itself; close at market only if a run
  sees >= +14% with the limit unfilled
- Above +14% -> trail the stop leg 5% below the high-water mark
- ORPHAN CHECK every run: if one leg filled, cancel the other and re-place a
  full-size stop on the remaining qty
- Open > ~48h without hitting target or stop -> reassess; close unless the
  hourly screen still PASSES
- Thesis broken -> close immediately

BOTH:
- Narrative with 2 consecutive failed trades -> exit all positions in it
- Any position found WITHOUT a resting trigger sell -> place one immediately

## Every-Run Invariants
Because crypto trades 24/7 and runs are 6h apart, every run (not just one of
them) must:
1. Reconcile live positions against TRADE-LOG (a fill may have happened between runs)
2. Verify every book position has a resting trigger sell; place one if missing
3. Close anything at or below -15% that the stop failed to catch
4. Ratchet stops upward where the high-water mark has risen (CORE), and raise
   tactical stops to breakeven once +6%
5. Tag every position in TRADE-LOG with its sleeve. An untagged position cannot
   be managed by the right rules — if the tag is missing, infer it from position
   size ($40 = CORE, $20 = TACTICAL) and record it.
