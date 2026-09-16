# Trading Strategy — Crypto

## Mission
Grow a ~$200 Alpaca crypto account. CRYPTO ONLY — no stocks, no options, ever.
Benchmark is BTC/USD buy-and-hold, not the S&P 500: beating a rising BTC is the
only result that justifies active trading.

## Capital & Constraints
- Starting capital: ~$200
- Platform: Alpaca crypto (`crypto_status: ACTIVE`, `crypto_tier: 1` — verified
  against the live account 2026-09-11; the docs previously said tier 0)
- Instruments: Alpaca tradable crypto USD pairs ONLY (36 available)
- Account type: cash, long only. Alpaca does NOT support shorting crypto.
- Max position size: 15% of equity CORE / 25% TACTICAL — and those are CAPS, not
  targets. Actual size is derived from risk: (equity * 0.015) / stop distance.
- Fractional is native (min order sizes are ~$1 equivalent), so there is NO
  whole-share ceiling and any of the 36 pairs is reachable at this size.
- NO PDT rule and NO T+1 settlement — crypto settles instantly. Proceeds from a
  sale are immediately reusable.

## Fees — the thing that punishes churn
The account is `crypto_tier: 1` (verified 2026-09-11 — this doc previously said
tier 0). Do NOT size risk off the nominal tier: the number that governs is the
MEASURED 0.65% per round trip recorded below, which was observed on this account
and already supersedes the ~0.5% estimate here. On $40 that is ~$0.20 per round trip, and it is charged
whether the trade wins or loses. Consequences that are part of the strategy:
- Every stop-out costs the spread AND the fees. Frequent small stops bleed.
- The MONTHLY FEE BUDGET is the frequency control. There is no fixed trade cap.
- Require a minimum 2:1 reward:risk AFTER the measured 0.65% friction.

## Self-amendment — OPEN. Any run may amend (owner directive, 2026-09-16)
**ANY run may edit this file at any time, with no minimum trade count.** scan,
execute, research, summary and weekly-review all have amendment authority. If a
run sees something worth improving, it improves it in that run — do not defer.

The owner removed the freeze deliberately on 2026-09-16 and accepts the risk it
was guarding against (six amendments in five days on N=1, fitted to noise). Keep
logging every change with its evidence and reasoning so the churn stays visible
and reversible, but do NOT block on the counter.

Why the freeze: between 2026-09-10 and 2026-09-15 this document was amended six
times on a sample of ONE closed trade. Every one of those amendments was fitted
to noise, and two of them contradicted each other badly enough to produce six
live order-thrash cycles in a single day. A rulebook that changes faster than it
generates evidence cannot be evaluated, and an unevaluable strategy cannot be
profitable except by accident.

The weekly review is authorised to EDIT this file based on observed trade
results once the trigger is met. It does not need human approval. Rules changed this
way must be recorded in WEEKLY-REVIEW.md with the evidence, the before value and
the after value, and committed together with the review so `git log` shows
exactly what changed and why. Any bad change is recoverable with `git revert`.

### TUNABLE — the review may change these
- Stop distances and trail percentages, and the ratchet thresholds
- Hard-cut levels (-15% core, -6% tactical) and the tactical target
- Position counts, position sizes and sleeve allocation
- The monthly fee budget (1.0%) and the circuit-breaker thresholds
- Deployment CEILING (85%). The FLOOR is gone and may not return without
  evidence — see "Cash is a position".
- Screen filter thresholds (momentum, SMA20 distance, vol band, spread limits)
- Screen timeframes (daily / hourly)
- Narrative groupings
- Minimum R:R

### IMMUTABLE — the review may NEVER change these
These are not preferences, they are verified facts about the platform or the
mandate. A "rule improvement" that violates one produces orders the API rejects,
or changes what this bot is:
1. CRYPTO ONLY. No stocks, no options, ever.
2. Long only — Alpaca does not support shorting crypto.
3. Stops are `stop_limit` only. `trailing_stop` and `stop` are REJECTED for crypto.
4. Orders use `time_in_force: gtc` (or ioc). `day` is REJECTED for crypto.
5. Order notional >= $10. Hard API floor.
6. Stops are sized from the ACTUAL held qty (buy fees are taken in kind).
7. Every position must carry a resting stop. The review may change the stop
   DISTANCE; it may never remove the requirement or allow a naked position.
8. Never move a stop down, and never widen a stop on an open losing position.
9. No stablecoins as positions.
10. A fee budget must EXIST and may never exceed 1.5% of equity per month. The review
    may tune it below that; it may not remove it or raise it past the ceiling.
11. The daily circuit breaker must EXIST. Thresholds are tunable; removal is not.
12. This section itself, and the requirement to log amendments with evidence.

### When amendment may happen — EVIDENCE, not the calendar
Amendment happens ONLY in the weekly-review run, and ONLY when the evidence
trigger is met. Any other run that believes a rule should change writes the
observation to TRADE-LOG.md and changes nothing.

TRIGGER: none. Amend whenever the evidence warrants. (Historical note: this
used to require 10 closed trades since the last amendment. Below that,
change nothing and say so.
- 10, not 3. Three closed trades cannot distinguish a real effect from noise, and
  tuning on noise produces thrash: tighten a stop one day, loosen it the next,
  learn nothing, and destroy a rule that was working.
- The counter resets on every applied amendment, so two changes cannot ride on
  the same 10 trades.
- THERE IS NO "BROKEN RULE" FAST PATH. It was removed in v2: every one of the
  six amendments in the first five days was justified under it. If a rule looks
  broken, do THIS instead, in this order:
  1. Make the account SAFE — place the missing stop, or close the position.
  2. Write the evidence to TRADE-LOG.md: what you saw, the exact API response.
  3. Leave TRADING-STRATEGY.md alone and let the weekly review adjudicate it.
  A rule that produces a literal API rejection is a defect and the weekly review
  will treat it as one — but it is still not an excuse for an unscheduled edit,
  because "this rule is broken" is exactly how noise-fitting rationalises itself.
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
without fighting each other. A 15% trailing stop implies week-long holds; 2-3
trades a day implies hour-long holds. They cannot be the same position.

| | CORE (primary) | TACTICAL (experimental) |
|---|---|---|
| RISK per position | 2.0% of equity | 1.0% of equity |
| Position size | risk / trail (~$26 at $197) | risk / trail (~$20 at $197) |
| Hard cap on size | 20% of equity | 12% of equity |
| Max positions | 4 | 1 |
| New trades | agent's judgement | agent's judgement |
| Stop | 15% below high-water, ratcheted | 10% below high-water, ratcheted |
| Target | NONE — the trail is the exit | NONE — the trail is the exit |
| Time limit | none | none |
| Screen timeframe | daily bars | hourly bars |
| Hold horizon | weeks to months | days to weeks |

### Size is DERIVED from risk, never fixed in dollars
`position size = (equity * sleeve risk%) / trail distance`, then capped.

At $197 equity: CORE = $3.94 / 0.15 = ~$26; TACTICAL = $1.97 / 0.10 = ~$20.

CORE is the PRIMARY sleeve and carries twice the per-trade risk. The previous
version had this backwards: it gave TACTICAL $49 against CORE's $20, i.e. it put
2.5x the capital behind the sleeve with the structurally negative edge. See
"Why there is no profit target" below.

Total risk if every slot is filled: 4 CORE x 2.0% + 1 TACTICAL x 1.0% = 9.0% of
equity at risk simultaneously. That is the deliberate ceiling.

Why this replaced fixed $40/$20 sizing: under the old rule CORE risked $8.00 per
position (4.06% of equity) against TACTICAL's $1.20 (0.61%) — the "patient, safe"
sleeve carried **6.7x** the risk of the fast one, and three CORE positions put
12.2% of the account at risk at once against a 1-2% per-trade professional norm.

- Combined cap: 6 positions, and total deployment must stay AT OR BELOW 85%.
  There is NO minimum deployment. See "Cash is a position" below.
- NEITHER sleeve has a time limit or a profit target. Every winner in this
  account is held until its ratcheted stop takes it out. The 48h tactical
  reassess-or-close rule is REMOVED: it truncated exactly the right tail the
  system depends on.

## Why there is no profit target (v2, 2026-09-15) — READ BEFORE PROPOSING ONE

A fixed target/stop pair is a double-barrier bet. Under a zero-edge random walk
the probability of touching the target before the stop is `stop/(stop+target)`.
The old TACTICAL geometry, priced on the measured 0.65% round-trip fee:

| | |
|---|---|
| size / stop / target | $49.38 / -6% / +14% |
| net win | $6.91 - $0.32 fees = $6.59 |
| net loss | $2.96 + $0.32 fees = $3.28 |
| breakeven win rate | 3.28 / (6.59+3.28) = **33.2%** |
| random-walk win rate | 6/(6+14) = **30.0%** |

The gap is the fee. And it does NOT close by retuning: for any barrier pair the
random-walk rate sits just below the fee-adjusted breakeven, because the fee is
charged on both outcomes. A bounded-upside system therefore needs real
predictive edge merely to reach ZERO.

The 48h time limit made it strictly worse. The screen admits 0.4-6% daily vol;
at ~3% vol a 48h window is sigma ~= 4.2%, so +14% was a 3.3-sigma move while -6%
was 1.4-sigma. The losers were reachable inside the window and the winners were
not, which pushes the realised rate BELOW the 30% random-walk floor.

The only structure that pays without predictive edge is an UNBOUNDED right tail:
trail the stop up, never cap the winner, and let one large move pay for many
small stops. That is what CORE already was, and as of v2 it is what TACTICAL is
too. TACTICAL now differs from CORE only in timeframe (hourly screen), trail
tightness (10% vs 15%), size, and slot count — it is a FASTER trend-follow, not
a different kind of bet.

A side effect worth stating: with no target in either sleeve, nothing competes
for Alpaca's single resting-order slot. The stop/target ambiguity that caused
six live order-thrash cycles on 2026-09-15 is gone by construction, not by
convention.

## Grandfathered v1 positions
Positions opened under v1 KEEP their existing stops. "Never move a stop down" is
IMMUTABLE and outranks the new trail distance, so a v1 TACTICAL position on a 6%
stop is NOT widened to 10%. It is managed to the v2 ratchet from where it sits,
and closed only by its stop. Slot counts are likewise not enforced retroactively:
if the account holds more TACTICAL positions than v2 allows, open no new ones
until the count falls to the cap. Never force-close a compliant position to
satisfy a count.

## Cadence: scan runs HOURLY (`7 * * * *`, one routine)
SUPERSEDED (v1) — the plan below was specified and never deployed. It moved scan
from hourly to a 30-minute cadence (SUPERSEDED). The scheduler enforces a 1-HOUR
MINIMUM interval, so
`*/30` is rejected, and the cadence was to be built from TWO routines on separate
hourly crons offset 30 min apart, both running the identical scan prompt. The
second routine was NEVER CREATED, so scan has always in fact run hourly.

Under v2 every position in BOTH sleeves rests a full-size stop_limit at the
broker, so the scan is NOT the mechanism protecting anything. A missed scan now
costs a late trail raise, not an unstopped position. The ~3h blind window of
2026-09-14 would have exposed nothing under these rules.

The cadence is kept at 30 min anyway because the ratchet is what converts an
open winner into a realised one, and a tighter ratchet loop gives back less of a
move. It is a performance setting now, not a safety one.

This does NOT raise trading frequency: scan never opens a position, only execute
does, so the fee budget is untouched by cadence.

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

**MONTHLY FEE BUDGET: 1.0% of equity (~$2.00 at $200).** (v2: was 1.5% WEEKLY.)
- Estimate the round-trip cost of every entry BEFORE placing it: notional x 0.65%
  (use more for a wide-spread alt) and add it to the running monthly total.
- Track the total in each daily snapshot as "fees used this month: $X / $2.00".
- When the budget is exhausted, STOP OPENING NEW POSITIONS for the rest of the
  UTC month. Exits are always still allowed — never let a budget trap a loser.
- The budget resets on the 1st, 00:00 UTC.

### Why the weekly budget had to go
1.5% of equity PER WEEK is **78% annualised** if spent. Even half-spent it is
~39%/yr of drag. The benchmark this account is graded against — BTC
buy-and-hold — pays ZERO. A budget framed as a safety ceiling was in fact
licensing a rate of churn that no edge could survive.

1.0% per MONTH is ~12%/yr at the ceiling, and the EXPECTED burn is about half
that: a trend-follower holding weeks-to-months across 5 slots does perhaps 3-6
round trips a month, which at ~$0.17 per $26 round trip is ~0.45%/month (~5%/yr).
If the budget is regularly being exhausted, the system is churning and the
diagnosis is the entry gate, not the budget.

Why a budget rather than a trade count: it self-adjusts. Bigger positions and
wider spreads buy fewer trades; cheap tight-spread entries buy more. A trade
count cannot tell the difference between a $0.13 BTC round trip and a $0.40
round trip in a thin alt, and it is the dollars that compound against you.

## Why the tactical target was 14% — SUPERSEDED 2026-09-15 (v2), kept as history
**There is no tactical target any more.** See "Why there is no profit target".
The analysis below is correct on its own terms and still wrong in outcome: it
tuned the target until the R:R arithmetic passed the gate, without ever asking
whether a BOUNDED target can clear the fee hurdle at all. It cannot. Preserved
so the same reasoning is not rediscovered and re-adopted.

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

## Cash is a position (the deployment FLOOR was removed 2026-09-15)
There is a deployment CEILING (85%) and no floor. Being 0% deployed is a valid,
fully compliant state. Never open a position to "correct" deployment.

The old 75-85% band was a floor as well as a ceiling, and it was dead letter
from day one. Across its entire life the account sat at 0%, 29.6% and 29.7%
deployed — never once inside the band — and every run spent a paragraph
justifying the breach. It generated commentary, never behaviour.

It was also wrong in principle. A minimum-deployment mandate is a PASSIVE
INDEXING construct: it exists to suppress tracking error when the job is to
replicate an index. This is an absolute-return strategy that picks spots, so a
floor manufactures negative-expectancy trades at exactly the moment nothing
qualifies. Trend-following funds sit flat for long stretches; that is the
strategy working, not failing.

The one real argument for a floor was the benchmark: the mandate is to beat
BTC buy-and-hold, and cash guarantees underperformance while BTC rises. But
that argument proves too much — a book forced 75% long is just a worse BTC
tracker paying friction for the privilege. The way to beat BTC is asymmetry:
heavy when the screen offers setups, flat when it does not. Tracking error is
the price of the mandate, not a violation of it.

If a future review wants to reinstate a floor, it needs EVIDENCE that flat
periods cost more than the forced trades would have — not the observation that
deployment is low.

## Daily circuit breaker (required once frequency is unbounded)
Unbounded frequency plus a losing streak is how a small account dies in a day.
- Computed by summing the `REALIZED P&L` values on today's exit rows in
  TRADE-LOG (UTC day). Do NOT infer it from equity change — that includes
  unrealized moves on open positions and will trip or miss the breaker wrongly.
- If REALIZED losses today reach 5% of equity (~$9.86), open NO new positions
  for the rest of the UTC day. Management and exits continue.
- 5%, raised from 3% on 2026-09-15, because at 3% (~$5.92) the breaker was
  UNSATISFIABLE alongside the sizing rules: a single CORE stop-out at -15% lost
  $6.00 and at -20% lost $8.00, so ANY core stop tripped the day's breaker by
  itself. A breaker that fires on one ordinary stop is not a circuit breaker,
  it is an outage. At 1.5% risk per position it now takes ~3.3 stop-outs to
  trip, which is the intended "today is going badly" signal.
- If 3 consecutive tactical trades close at a loss, stop opening tactical for
  the rest of the UTC day regardless of the budget.
- Record either trip in TRADE-LOG with the trigger and the time.
These exist because the agent judging its own frequency has no natural brake:
each individual trade can look reasonable while the sequence is ruinous.

## Core Rules
1. CRYPTO ONLY — no stocks, no options, ever
2. Long only — never attempt a short
3. Deployment <= 85%. There is NO deployment floor — see "Cash is a position".
4. Respect each sleeve's position COUNT and RISK BUDGET (table above). Size is
   derived from the stop distance, never fixed in dollars. Trade frequency is
   the agent's call, bounded by the monthly fee budget and circuit breaker.
5. EVERY position, in BOTH sleeves, carries a resting `stop_limit` GTC sell at
   the broker for 100% of the HELD qty. Never a target leg, never a split.
6. CORE: hard cut AND trail are both 15% below high-water, ratcheted UP only;
   tighten to 12% at +30% and 10% at +40%. (The old 20% trail sat BELOW the
   -15% hard cut, so the cut always fired first and the trail was decorative.)
7. TACTICAL: trail 10% below high-water, ratcheted UP only; tighten to 8% at
   +20%. Initial stop is 10% below ENTRY. No target, no time limit.
8. Never place a stop within 5% of current price; NEVER move any stop down —
   including on grandfathered positions carrying a tighter v1 stop
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

## What rests at the exchange (v2, 2026-09-15)
Alpaca crypto gives each position exactly ONE resting-order slot, because a
resting sell reserves the quantity it names and there is no oco/bracket.

Under v2 that constraint costs nothing, because **neither sleeve has a target**:

| | Rests at the EXCHANGE | Enforced by the 30-MIN SCAN |
|---|---|---|
| **CORE** | `stop_limit` @ 100% of held qty | the ratchet |
| **TACTICAL** | `stop_limit` @ 100% of held qty | the ratchet |

**One rule, both sleeves: a full-size `stop_limit`, always.** Downside is
protected 24/7 at the broker even when no run happens, and the scan's only job
on an open position is to raise the trail.

### This supersedes the 2026-09-15 "TACTICAL rests its target" decision
That decision traded exchange-side downside protection for exact capture of a
+14% target. v2 deletes the target, so there is nothing left to buy with that
risk and the trade-off no longer exists. Consequences of the reversal:

- No sleeve is ever unprotected between scans, or during a runner outage. The
  ~3h blind window of 2026-09-14 would no longer have exposed anything.
- The scan is no longer safety-critical. It still runs every 30 min to ratchet,
  but a missed scan now costs a late trail raise, not an unstopped position.
- The stop/target contention that produced six live order-thrash cycles on
  2026-09-15 is removed at the root: `execute` and `scan` can no longer want
  different legs, because there is only one leg.

Splitting the quantity (stop on part, target on the rest) is NOT the answer to
the one-slot limit and must not be reintroduced. It leaves a slice with no stop
AND no target, and creates orphan legs when one side fills. That is exactly how
DOT sat naked for 70h and closed at -8.0%, the only closed trade this account
has. One leg, 100% of the quantity, every time.


## Stops — how they actually work here (READ THIS)
Alpaca REJECTS `trailing_stop` and `stop` for crypto:
`{"code":40010001,"message":"invalid order type for crypto order"}`
Only `stop_limit` is accepted. So Core Rule 5 is implemented as:

    {"symbol":"BTC/USD","qty":"<frac>","side":"sell","type":"stop_limit",
     "stop_price":"<trigger>","limit_price":"<trigger * 0.95>","time_in_force":"gtc"}

- `limit_price` is set 5% BELOW `stop_price` so it can still fill while price is
  falling. A limit equal to the stop will often not fill at all.
- The limit sits 5% below the trigger, not 2%. A stop_limit only fills if price
  trades between the trigger and the limit; in a crypto flush 2% of room is
  routinely jumped, which converts the stop into a no-op and leaves the position
  riding down. 5% accepts a worse fill price in exchange for actually filling.
  This is the correct trade: a bad fill is a cost, an unfilled stop is a loss of
  unbounded size.
- KNOWN RISK: a stop_limit can still be gapped through. In a violent drop price can
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
- Where is the hard cut in dollars (15% CORE / 10% TACTICAL below entry)?
- Where is the initial stop_limit (trigger and limit = trigger * 0.95)?
- There is NO target to state. Do not compute an R:R ratio against an invented
  target — a trend-follow has no denominator. State instead: what would have to
  happen for this to run 30%+, and what kills the thesis?

## Buy-Side Gate (ALL must pass, else skip and log the reason)
- The sleeve is stated explicitly (CORE or TACTICAL) before sizing
- CORE: positions after fill <= 4, cost ~$26 (run state.sh for the live number)
- TACTICAL: positions after fill <= 1, cost ~$20
- Estimated round-trip fee for THIS trade + fees already used THIS MONTH
  <= 1.0% of equity (~$2.00). If it would breach, SKIP and log it.
- Circuit breaker not tripped: realized losses today < 5% of equity, and not
  3 consecutive tactical losses THAT CLOSED TODAY (UTC). The streak is scoped to
  the UTC day and RESETS at 00:00 UTC. It does NOT carry across days.
  WHY THIS IS EXPLICIT: the streak used to be readable as permanent, and a
  permanent streak DEADLOCKS the sleeve — the only thing that clears it is a
  winning tactical trade, which the freeze itself prevents. The account sat
  frozen from 2026-09-15 for exactly this reason. Backtested: the permanent
  reading froze the sleeve for 400 straight days.
- Combined positions after fill <= 5, total deployment <= 85% of equity
- Position size == (equity * risk%) / trail distance, capped at 20% (CORE) /
  12% (TACTICAL) of equity. Risk% is 2.0 CORE / 1.0 TACTICAL. NEVER a fixed
  dollar amount — read both sizes off `state.sh`.
- Position cost <= available cash
- Pair is in the Alpaca tradable crypto USD list (`alpaca.sh assets crypto`)
- Pair is NOT a stablecoin
- Order notional >= $10 (HARD API floor). `min_order_size` is only a quantity
  floor and is NOT sufficient — a sub-$10 order is rejected outright.
- qty >= that pair's `min_order_size` as well
- Quoted spread <= 1% (BTC/ETH run ~0.02-0.04%; a wide spread means thin book)
- `time_in_force` is `gtc` — `day` is REJECTED for crypto
  (`{"code":42210000,"message":"invalid crypto time_in_force"}`)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The coin PASSES its sleeve's technical screen (scripts/screen.sh)
- The instrument is crypto (never a stock, never an option)

## Sell-Side Rules
Both sleeves exit the same way: **the ratcheted stop_limit is the exit.** There
is no profit target and no time limit anywhere in this system.

CORE:
- Unrealized <= -15% and the stop did not fill (gapped through) -> cancel the
  stop, close at market
- Thesis broken (catalyst dead, narrative rolling over, exploit/depeg/delisting)
  -> close even if not at -15%
- Up >= +40% -> ratchet stop to 10% below high-water
- Up >= +30% -> ratchet stop to 12% below high-water
- Otherwise -> keep stop 15% below high-water
- NO profit target. Let it run; the ratchet decides the exit.

TACTICAL:
- Unrealized <= -10% and the stop did not fill (gapped through) -> cancel the
  stop, close at market
- Up >= +20% -> ratchet stop to 8% below high-water
- Otherwise -> keep stop 10% below high-water
- NO profit target and NO 48h rule. A tactical position that is still trending
  is a WINNER, not dead money; the trail decides when it is over.
- Thesis broken -> close immediately
- Grandfathered v1 positions keep their tighter stop and are never widened.

BOTH:
- Narrative with 2 consecutive failed trades -> exit all positions in it
- Any position found without a full-size resting stop_limit -> place one
  immediately. If placement is rejected twice, close at market rather than hold
  it unprotected.
- Any position found carrying a resting `limit` SELL (a v1 target leg) -> cancel
  it and place a full-size stop_limit. Target legs are banned in v2.

## Every-Run Invariants
Because crypto trades 24/7 and runs are 6h apart, every run (not just one of
them) must:
1. Reconcile live positions against TRADE-LOG (a fill may have happened between runs)
2. Verify every position has a resting stop_limit; place one if missing
3. Close anything past its hard cut (-15% CORE / -10% TACTICAL) that the
   stop_limit gapped through without filling
4. Ratchet stops upward wherever the high-water mark has risen, in BOTH sleeves
5. Tag every position in TRADE-LOG with its sleeve. An untagged position cannot
   be managed by the right rules — if the tag is missing, infer it from its
   TRAIL DISTANCE (~15% = CORE, ~10% = TACTICAL, ~6% = grandfathered v1
   TACTICAL) and record it. NEVER infer from size: size is derived from risk and
   the two sleeves now sit ~$26 vs ~$20, too close to distinguish.
