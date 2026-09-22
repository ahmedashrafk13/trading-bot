# Hypothesis Log — the bot's actual memory of what it has learned

This file is the difference between REMEMBERING and LEARNING.

`TRADE-LOG.md` remembers what happened. This file records what was *concluded*
from it, whether that conclusion was *tested*, and whether it was *true*. Without
it the bot writes "I lost on DOT" a hundred times and changes nothing — which is
exactly what happened between 2026-09-10 and 2026-09-16, where the same defect
was logged twelve times and the same trade setup lost three times in a row.

## The rule that makes this work

**Every closed trade must produce a hypothesis. No hypothesis may change a rule
until it has been tested on history.**

That second half is not bureaucracy, it is the whole point. One trade is ~95%
noise. Between 2026-09-10 and 2026-09-15 the rulebook was amended SIX times on a
sample of ONE closed trade and two of those amendments contradicted each other.
That was the bot "learning from its mistakes", and it made things worse. A
hypothesis drawn from one trade is a guess; the backtester turns it into
evidence, over hundreds of outcomes, in about ninety seconds.

## Status values

| status | meaning |
|---|---|
| `PROPOSED` | Drawn from a trade. Not tested. Must NOT influence any trade yet. |
| `TESTING` | A backtest is specified but not yet run. |
| `CONFIRMED` | Beat the random null out of sample AND survived walk-forward. Eligible for promotion. |
| `REJECTED` | Tested, did not beat the null. **Never propose this idea again — that is what this file is for.** |
| `PROMOTED` | Adopted into TRADING-STRATEGY.md. Records the date and the commit. |

## How to test one

```bash
python backtest/research.py                      # is the signal predictive at all?
python backtest/run.py --set <param>=<value>     # does it survive the machinery?
python backtest/sweep.py                         # does it survive out of sample?
```

A hypothesis about *sizing, stops, frequency or caps* is tested with `run.py`.
A hypothesis about *what to buy* is tested with `research.py` first — if the
information coefficient does not beat the random null, stop there and mark it
REJECTED. Do not proceed to a backtest; a non-predictive signal cannot be
rescued by better position sizing.

## The standing verdicts — read before proposing anything

These are settled. Do not re-propose them; test something new instead.

| finding | evidence | status |
|---|---|---|
| Momentum is INVERTED at SHORT horizons only (<=1 day) | Bybit daily: IC@1d -0.012 test; but IC@30d **+0.025** test. The Alpaca-era "momentum is inverted" verdict was measured on hourly bars only and was WRONGLY generalised to all horizons. Short-horizon reversal and medium-horizon momentum coexist. | CORRECTED 2026-09-16 |
| Low volatility predicts a higher MEDIAN forward return | IC +0.059@1d, +0.093@7d, +0.122@30d out of sample (Bybit daily) | CONFIRMED |
| **...but low volatility does NOT predict a higher MEAN return, so it cannot be traded long/short** | 30d forward: LOW vol median -0.0% vs HIGH vol -5.1% (low wins on median by +5.0pp) — yet MEAN is +2.7% vs +7.3% (high wins by +4.6pp). High-vol returns are lottery-shaped: p99 +206.8%, max +832%. Shorting them is right most days and catastrophic occasionally. | CONFIRMED |
| Market-neutral long/short does NOT rescue the low-vol signal | `neutral.py`: -93.1% risk-weighted, -97.4% equal-dollar. Momentum L/S made +109.7% but still lost to holding BTC (+225.9%) at the same drawdown. | CONFIRMED |
| Trailing stops harvest noise; wider is always better | -44.8% -> -5.8% as trail widens to none | CONFIRMED |
| Higher trade frequency is strictly worse | 5.9 trades/day = -95.9%; -49.4% even at ZERO fees | CONFIRMED |
| Cross-sectional selection cannot be monetized long-only | lowvol signal has real IC, still returns -44% in the engine | CONFIRMED |
| Nothing tested beats buy-and-hold BTC | 5.7y: BTC +157.4%, best variant +27.3% | CONFIRMED |
| The altcoin universe has a negative median | median coin -21.2% vs BTC +157.4% over 5.7y | CONFIRMED |
| The 85% deployment ceiling is non-binding above ~65% (the 5-slot/risk cap binds first); lowering it materially improves return AND drawdown | `run.py --set max_deploy=k` for k in {0.30,0.50,0.65,0.85,1.00}: 0.65/0.85/1.00 produce IDENTICAL trades (127) — the slot/risk sizing caps out well below 65% deployment in practice. At 0.30 vs 0.85, BOTH the 60/40 train/test split AND all 4 rolling quarters agree in sign: train -19.55% vs -32.52%, test -12.81% vs -16.75%; every quarter Aug'25-Sep'26 shows 0.30 beating 0.85 on return and max drawdown. | CONFIRMED |
| Raw perp funding rate (crowding), used contrarian, predicts forward return | `research.py` (Bybit D, 60 symbols, funding fetched via new `backtest/fetch_funding.py`/`scripts/bybit.py funding`): IC train/test @1d +0.0097/+0.0063, @7d +0.0159/+0.0141, @30d +0.0226/+0.0034 — t-stat < 2 at every horizon (does not clearly beat RANDOM's noise floor). | REJECTED |
| 30d momentum conditioned on calm funding (bottom-half \|funding\| that hour) beats unconditioned 30d momentum, but ONLY at the 30d horizon | `research.py`, same Bybit D universe: @30d train +0.0664 / test +0.1398 (t=+8.4) vs unconditioned momentum_30d train +0.0421 / test +0.0726 (t=+7.6) — same sign both halves, roughly double the OOS IC. At 1d/7d the conditioned signal's train and test ICs DISAGREE IN SIGN (train -0.0052/-0.0111, test +0.0634/+0.0892) so those horizons are not usable. Confirmed at the signal (IC) level only — no `run.py` strategy variant implements funding-gated CORE entries yet, so this is NOT eligible for promotion until an engine change is built and back-tested at the P&L level. | CONFIRMED (signal-level, 30d only) |
| FEWER CORE SLOTS IS BETTER, monotonically — 1 beats 2 beats 4 beats 6 | `run.py --set core_slots=k`: full period k=1 -26.87%/DD -30.26% vs k=4 -44.76%/DD -53.04% vs k=6 -59.51%. 60/40 split agrees in sign (train -19.00% vs -42.60%, test -10.08% vs -19.34%) and all 4 rolling quarters favour k=1 on return AND drawdown with no exception. Dominates and subsumes the max_deploy cut (hypothesis #3): at 1 slot the deployment ceiling is non-binding. Mechanism: the universe's negative median means every extra slot dilutes the top pick toward it — so the preference extrapolates to zero exposure and is NOT evidence of a long edge. | PROMOTED 2026-09-18 (hyp #6) |
| One-sided (downside-only) volatility REPAIRS the low-vol mean/median trap and still does not monetize | `sig_downside_vol_low`: highest IC ever measured here (@168 bars train +0.1101 / test +0.0766, t=+18.0), beats `low_volatility` OOS, and its top tail wins on BOTH mean and median where low_vol's mean flips. Yet `entry_signal=downside_vol` returns -45.70% vs the momentum baseline's -44.76%. Mean edge ~0.06% per 24-bar hold against 0.65% round-trip friction. | REJECTED |
| Intrabar close-location-value (the first signal to use the high/low arrays) carries no cross-sectional information | `sig_clv_accumulation`: sign flips train-to-test at 24 bars (-0.0283 -> +0.0116), never clears RANDOM at any horizon. | REJECTED |
| "12-2" momentum (skip the most recent 7 bars) does NOT rescue momentum | `sig_momentum_skip_recent`: @168 bars train +0.0384 / test -0.0234 — sign flip; other horizons inside the noise floor. The short-horizon-reversal-contamination story is unsupported. | REJECTED |
| Volume is the one column in the committed bar cache that carried NO usable long-only edge, in either direction | First read of `u.v` (the loader discarded it until 2026-09-22). `sig_amihud_illiquidity` has the 3rd-strongest IC in the file and is NEGATIVE with the same sign in both halves (@168 bars train -0.0439 / test -0.0643, t=-18.0), i.e. the illiquidity premium is INVERTED in crypto — LIQUID coins outperform. `sig_volume_surge` is positive and consistent but weak (@168 train +0.0307 / test +0.0296, t=+8.6). Neither monetizes: `entry_signal=liquidity` -14.29% (DD -31.79%), `volume_surge` -11.27% (DD -34.32%), `liquidity_downside_vol` -1.78%, all vs the momentum baseline's +4.78% (DD -24.80%). | REJECTED |
| The TACTICAL entry volatility ceiling (6%) must not be LOOSENED; tightening does not pay either | `run.py --set tac_vol_hi=k` for k in {0.030,0.045,0.060,0.090,0.200}: 0.060 = +4.78% / DD -24.80%; loosening to 0.090 = -20.24% / DD -36.91% and 0.200 = -20.05% / DD -36.42%; tightening to 0.045 = -4.65% and 0.030 = -3.65% (DD -16.04%, the best drawdown). Non-monotone with a spike at exactly the shipped value, so 0.060 is NOT a robustly-identified optimum — but every alternative tested is worse on return, and the two looser settings are worse on BOTH return and drawdown. Full-period only. | REJECTED (no change warranted) |
| The 72h TACTICAL time stop cannot be measured on the committed cache | `run.py --set tac_time_stop_h=k` for k in {0,24,48,72,168} on daily bars: the engine counts the limit in BARS, so 72 fires as 72 DAYS and produces only 3 exits in 4.1 years (0 at k=168, 15 at k=24). Spread is +3.75%..+5.56% across the whole sweep on a handful of differing trades — noise. The live rule is 72 HOURS and only the gitignored hourly cache could test it. | UNTESTABLE on current data |

## Log

| # | date | drawn from | hypothesis | test to run | status | result |
|---|------|-----------|------------|-------------|--------|--------|
| 1 | 2026-09-16 | DOT/UNI/XRP, 3 straight stop-outs | A 6% trail is inside hourly crypto noise, so stops fire on wiggle rather than on a broken thesis | `run.py --set tac_trail=0.20` vs `0.06` | CONFIRMED | Wider is better at every step; best is no stop at all (-5.8% vs -44.8%) |
| 2 | 2026-09-16 | 11 research HOLDs out of 11 | The research gate rejects every candidate, so CORE can never originate | count originations with the gate modelled off | CONFIRMED | The screen passes a median of 8 coins/hour; the gate, not the screen, is the constraint |
| 3 | 2026-09-17 | STEP 5 standing-assumption test (no trade closed since last run) | The 85% deployment ceiling is untested and may be too loose: if it rarely binds, most of its "room" is unused, and if it DOES bind on some entries, those marginal entries may be net-negative given the account's measured lack of edge | `run.py --set max_deploy=k` sweep (0.30/0.50/0.65/0.85/1.00), then 60/40 split + 4 rolling quarters at 0.30 vs 0.85 | CONFIRMED | 0.65-1.00 are identical (cap never binds there); 0.30 beats 0.85 on return AND drawdown in the train half, the test half, and all 4 individual quarters — no exception. See standing verdict above. |
| 4 | 2026-09-17 | STEP 4B non-price data (funding rate, per learn.md's "best remaining bet") | Extreme perp funding (crowded leverage) precedes a reversal, so -funding should predict forward return | `research.py` IC on new `funding_contrarian` signal (Bybit D universe, `backtest/fetch_funding.py`) | REJECTED | IC does not clearly beat RANDOM at any horizon (t<2 throughout); see standing verdict above. |
| 5 | 2026-09-17 | STEP 4B combination idea | Momentum conditioned on calm (non-crowded) funding beats momentum alone | `research.py` IC on new `momentum_if_funding_calm` signal vs `momentum_30d` | CONFIRMED (30d only, signal-level) | @30d roughly doubles unconditioned momentum's OOS IC, same sign both halves; @1d/@7d sign flips train-to-test, unusable. Not promoted — no engine implementation of funding-gated entries exists yet to backtest at the P&L level. See standing verdict above. |
| 6 | 2026-09-18 | STEP 5 standing-assumption test (no trade closed since last run) | The 4/1 CORE/TACTICAL slot split has never been tested. If the altcoin universe has a negative median (CONFIRMED), then each extra CORE slot dilutes the top-ranked pick toward that median, so FEWER core slots should improve return AND drawdown — not just return | `run.py --set core_slots=k` for k in {1,2,4,6}, then 60/40 split + 4 rolling quarters at k=1 vs k=4, plus a k=1 vs (k=4, max_deploy=0.30) run to confirm it is not hypothesis #3 renamed | **PROMOTED 2026-09-18** | Monotone and unanimous. Full period: k=1 -26.87% / DD -30.26% / EDGE +9.49% vs k=4 -44.76% / DD -53.04% / EDGE -8.40%; k=6 is -59.51%. Split: k=1 vs k=4 train -19.00% vs -42.60% (DD -21.62% vs -46.99%), test -10.08% vs -19.34% (DD -14.96% vs -27.52%) — same sign both halves. All 4 rolling quarters favour k=1 on return AND drawdown with NO exception. Separable from hypothesis #3: k=1 beats (k=4, max_deploy=0.30) in both halves (-19.00/-10.08 vs -26.95/-10.87) and makes the deployment cap non-binding (0.30 and 0.85 give identical trades). CAVEAT recorded in the strategy edit: the preference is monotone and extrapolates to zero exposure, so this is "hold less of a universe with no long edge", not evidence of an edge. |
| 7 | 2026-09-18 | STEP 4B self-generated signal (new data dimension: downside-only risk) | `low_volatility` is CONFIRMED predictive on the MEDIAN and CONFIRMED untradable because it discards the lottery-shaped right tail along with the left. A ONE-SIDED version that penalises only negative returns should keep the IC while preserving the mean | new `sig_downside_vol_low` in signals.py -> `research.py --timeframe D`, then the mandatory skew check (mean AND median of both tails, out of sample), then `run.py --set entry_signal=downside_vol` at the P&L level | REJECTED | Best IC in the entire bake-off and it PASSED the skew check — @168 bars train +0.1101 / test +0.0766 (t=+18.0), @24 bars +0.0577/+0.0631 (t=+13.6), beating `low_volatility` out of sample at both horizons; and unlike low_vol its top tail wins on BOTH mean and median (24 bars: mean +0.0003 vs -0.0003, median -0.0004 vs -0.0035; 168 bars: mean +0.0047 vs +0.0021), i.e. it genuinely repairs the mean/median trap that cost `neutral.py` 93%. It still does NOT monetize: `entry_signal=downside_vol` returns -45.70% (DD -54.73%) vs the shipped momentum baseline's -44.76%, and vs `lowvol`'s -44.43%. The measured mean edge is ~0.06% per 24-bar holding period against 0.65% round-trip friction. This is the standing verdict "cross-sectional selection cannot be monetized long-only" reproduced on the strongest signal yet measured. Do not re-propose one-sided volatility. |
| 8 | 2026-09-18 | STEP 4B self-generated signal (first use of the high/low arrays — every prior signal read only the close) | Mean close-location-value, (c-l)/(h-l), over 14 bars measures who won the intrabar fights and carries information the close-to-close series does not | new `sig_clv_accumulation` -> `research.py --timeframe D`; falsified unless it beats RANDOM with the same sign in train and test | REJECTED | Fails the same-sign test and never clears the null: @6 bars train -0.0192 / test -0.0056, @24 bars train -0.0283 / test **+0.0116** (sign flip), @168 bars train +0.0036 / test +0.0256 (no train signal). Did not appear in the survivors list at any horizon. Intrabar range position carries no usable cross-sectional information on this universe. |
| 9 | 2026-09-18 | STEP 4B combination of two STANDING VERDICTS (short-horizon reversal + medium-horizon momentum coexist) | If momentum is inverted at <=1d and positive at 30d, then plain 30d momentum is contaminated by the reversal in its own most recent window, so a 12-2 style construction that SKIPS the last 7 bars should raise the IC above unconditioned momentum | new `sig_momentum_skip_recent` (90-bar lookback, 7-bar skip) -> `research.py --timeframe D`; falsified unless it beats `momentum_30d` out of sample with the same sign in both halves | REJECTED | Sign flips train-to-test at the only horizon where it shows anything: @168 bars train +0.0384 / test **-0.0234**. @6 bars -0.0192/-0.0030 and @24 bars -0.0155/-0.0056 are both inside the noise floor. Never reached the survivors list. Skipping the recent window does not rescue momentum; the contamination story is not supported. |
| 10 | 2026-09-22 | POL closed 2026-09-21T20:11 on the 72h time stop at +$0.40 (the only close since the last learn run) | The 72h time stop ends positions while the trail is still the better exit, so removing or lengthening it should improve return without worsening drawdown | `run.py --timeframe D --set tac_time_stop_h=k` for k in {0,24,48,72,168}; falsified unless k=0/168 beats k=72 by more than the sweep's own spread | UNTESTABLE | Units defect, not a result: the engine applies the limit in BARS, and the only committed cache is DAILY, so `72` means 72 days and fires 3 times in 4.1 years. k=0/168 +5.56% (DD -24.23%), k=72 +4.78% (DD -24.80%), k=48 +3.75%, k=24 +3.76% — non-monotone, driven by <15 trades, indistinguishable from noise. Recorded as untestable rather than graded; testing the live rule needs the hourly cache (~15 min of API calls, gitignored). Changed nothing. |
| 11 | 2026-09-22 | STEP 4B self-generated signal — first use of the VOLUME column, which the loader discarded until this run | Amihud (2002) illiquidity, mean \|return\| per dollar of volume over 20 bars, is the best-documented non-price cross-sectional factor; if the liquidity premium exists in crypto, illiquid coins should earn higher forward returns | added `self.v` to the Universe loader + new `sig_amihud_illiquidity` -> `research.py --timeframe D`; then, if it clears RANDOM with the same sign in both halves, `run.py --set entry_signal=liquidity` at the P&L level | REJECTED | The IC is real and the sign is BACKWARDS: @168 bars train -0.0439 / test -0.0643 (t=-18.0), @24 -0.0183/-0.0475, @6 -0.0221/-0.0257 — same sign at every horizon in both halves, 3rd-strongest \|IC\| in the file. So crypto pays no illiquidity premium; the liquid names outperform. Traded in the direction the data supports (`liquidity` = -amihud), it still loses: -14.29% / DD -31.79% / Sharpe -1.33 vs the momentum baseline +4.78% / DD -24.80% / +0.79. Combined with the best signal on file, `liquidity_downside_vol` = -1.78% / DD -21.63% — better drawdown, still below baseline return. No short leg proposed, so the skew check does not apply. This is the standing verdict "cross-sectional selection cannot be monetized long-only" reproduced on a non-price dimension for the first time. |
| 12 | 2026-09-22 | STEP 4B self-generated signal (second volume construction, independent of return sign so it is not momentum restated) | Relative volume — today's volume over its own 20-bar mean — measures ATTENTION rather than liquidity, and attention persists, so high relative turnover should predict higher forward return | new `sig_volume_surge` -> `research.py --timeframe D`; falsified unless it beats RANDOM with the same sign in both halves, then `run.py --set entry_signal=volume_surge` | REJECTED | Clears the null cleanly and consistently — @168 bars train +0.0307 / test +0.0296 (t=+8.6), @24 +0.0141/+0.0235 (t=+7.1), @6 +0.0104/+0.0108 (t=+3.2), positive at every horizon in both halves — and is still not tradable: -11.27% / DD -34.32% / Sharpe -0.70, on 711 trades vs the baseline's 506. The attention story survives as a statistical fact and dies on friction; raising the trade count by 40% to harvest a ~0.03 IC is the frequency mistake the standing verdicts already price. |
| 13 | 2026-09-22 | STEP 5 standing-assumption test — the TACTICAL entry volatility band ceiling `tac_vol_hi` = 6%, never tested since it was written | The 6% ceiling is an origin-story number. If the universe's lottery-shaped right tail is where the money is (CONFIRMED), the ceiling is discarding the winners and LOOSENING it should improve return | `run.py --timeframe D --set tac_vol_hi=k` for k in {0.030,0.045,0.060,0.090,0.200}; falsified if any k beats the shipped 0.060 on return | REJECTED | The hypothesis is backwards and the shipped value survives. 0.060 = +4.78% / DD -24.80% / Sharpe +0.79; loosening is clearly harmful on BOTH metrics (0.090 = -20.24% / DD -36.91%; 0.200 = -20.05% / DD -36.42%); tightening also loses return (0.045 = -4.65%, 0.030 = -3.65%) though 0.030 gives the best drawdown of the sweep, -16.04%. Caveat recorded against over-reading this: the curve is NON-MONOTONE with its peak at exactly the incumbent value, which is the shape of a lucky number rather than a robustly-identified optimum, and only the full period was run. The actionable part — do not widen the band — holds in both directions of the metric. No change made. |

## 2026-09-23 — THE FEE CONSTANT WAS 6x TOO HIGH (not a hypothesis; a defect)
`Params.fee_bps` was 35.0/side with 10.0 spread — the SPOT-era figure measured on
a $12 BTC spot round trip (0.65% round trip). The account moved to linear PERPS
on 2026-09-22 and nobody updated it.

MEASURED from 39 real perp fills on this account: **0.0550% per side on every
symbol**, 0.0572% average = **0.114% round trip**. Six times cheaper.

Consequence: every backtest run between 2026-09-22 and 2026-09-23 overstated
friction by ~6x, and every conclusion of the form "the signal has gross edge but
fees eat it" was computed against a cost that does not exist. Corrected in
engine.py with the measurement recorded inline.

Effect on the best signal, full hourly period:
  downside_vol @ 35bps = -54.59%   ->   @ 5.5bps = -39.63%   (+15 points)

## 2026-09-23 — SURVIVORSHIP BIAS IN THE BACKTEST UNIVERSE (open defect)
At a 30% trail and correct fees the RANDOM null returns -16.07% against BTC's
-36.35% — a coin flip "beating" the benchmark by 20 points on 982 trades. That
is not possible in an unbiased universe.

Cause: `data/bars/` holds the coins that are liquid enough to sit in the top 60
by turnover TODAY. Coins that delisted or died are absent, so every long-only
strategy here inherits a tailwind that was not available live.

CONSEQUENCE FOR EVERY RESULT IN THIS FILE: "EDGE vs BTC" is not trustworthy on
this cache. The only defensible metric is SIGNAL minus RANDOM NULL at identical
settings, which is what backtest/bakeoff.py now reports. Fixing the bias needs a
point-in-time universe (delisted symbols included), which Bybit does not serve.

## 2026-09-23 — WARM-UP UNITS DEFECT (found while validating; third of its kind)
`warm = 24 * 31` was hardcoded as BARS meaning "31 days of hourly bars". On the
DAILY cache that silently became **744 days** of warm-up: 37% of the 5.5-year
history was discarded, and any `--days` window under 744 produced ZERO trades
while reporting a clean `+0.00%` — an out-of-sample test that looked like it ran
and had not. Corrected to `31 * bars_per_day`.

This is the THIRD units defect in this engine (time stop = hours vs bars,
lookbacks = hours vs bars, warm-up = hours vs bars). Every one silently produced
a plausible number rather than an error. Any new parameter expressed in time MUST
be converted through `bars_per_day`.

## 2026-09-23 — PROMOTED: entry_signal momentum -> liquidity, trail 0.10 -> 0.30
First change in this file's history with a positive ABSOLUTE return and a
null-controlled edge in every window tested.

  Full 5.5y daily:  liquidity +30.21% (DD -21.73%) | random +11.08% | momentum +4.27%
  Last 900 days:    liquidity  -1.84%              | random -10.14% | momentum  -6.11%
  Last 500 days:    liquidity  -6.17%              | random -14.96% | momentum -12.63%

Same sign in every window: +19.1pp / +8.3pp / +8.8pp over the null. Momentum —
the signal the bot traded live until today — scores AT OR BELOW the random null
in every one.

MECHANISM, stated so the claim stays bounded: this is the Amihud illiquidity
premium INVERTED. Crypto pays no premium for illiquidity; the liquid names
outperform. It is a real cross-sectional effect, measured, not a story.

THE HONEST CEILING: BTC buy-and-hold returned +157.38% over the same 5.5 years
against this strategy's +30.21%. The strategy is now PROFITABLE in absolute terms
and still loses badly to holding BTC. The standing verdict "nothing tested beats
buy-and-hold BTC" SURVIVES. What changed is that the bot went from losing money
to making some.

## 2026-09-23 — PROMOTED v6: time-series momentum + volatility targeting + regime filter
THE FIRST THING IN THIS REPO'S HISTORY TO BEAT BUY-AND-HOLD BTC IN ANY WINDOW.

Source: academic literature, not a self-generated variation. Two findings this
repo had never implemented:
  1. TIME-SERIES momentum (each asset against its OWN history) is strong in
     crypto; CROSS-SECTIONAL momentum (ranking coins against each other) is weak
     and dies to costs. All 13 prior hypotheses tested the WEAK one.
  2. "Without volatility scaling, time-series momentum would not have generated
     results different from buy-and-hold." The edge is RISK TIMING -- sizing
     down when vol is high -- not picking winners.

Config: entry_mode=timeseries, vol_target_annual=0.40, regime_filter=ON,
tac_cap=0.25, max_deploy=1.00, trail 30%.

FULL 5.5 YEARS (daily):
  this          +97.07%  DD -41.94%  Sharpe 2.72  1407 trades
  best x-sec    +30.21%  DD -21.73%
  momentum       +4.27%
  random null   +11.08%
  BTC buy/hold +157.38%  (still ahead on raw return over the full window)

OUT OF SAMPLE vs BTC -- it WINS in 2 of 3 windows:
  last  500d:  -4.72%  vs BTC -27.72%   = +23.00pp   BEATS BTC
  last  900d: +12.78%  vs BTC +11.66%   =  +1.12pp   BEATS BTC
  last 1400d: +51.96%  vs BTC +367.20%  = -315pp     loses (full bull run)

HONEST READ, so nobody over-claims this later: the strategy beats BTC in FLAT
and FALLING markets and loses badly in a strong bull. That is exactly what a
regime-filtered trend follower is supposed to do -- it is downside protection
bought by giving up upside, not a free lunch. Over the full 5.5y BTC still wins
on raw return (+157% vs +97%), though at far worse drawdown.

The standing verdict "nothing tested beats buy-and-hold BTC" is now QUALIFIED,
not overturned: nothing beats it over the full sample; this beats it in 2 of 3
recent windows.

TUNING SENSITIVITY (recorded so the next run does not re-discover it):
  vol_target 0.25 -> +62.90% DD -30.34% | 0.40 -> +97.07% DD -41.94%
             0.55 -> +98.60% DD -51.05%.  0.40 is the Sharpe peak, and the curve
  is smooth around it rather than spiking, so it is not a lucky number.

## 2026-09-23 — DELTA-NEUTRAL FUNDING CAPTURE: the best risk-adjusted result found
A different STRATEGY CLASS, not another signal. Every prior entry in this file is
directional -- it guesses which way a coin moves. This does not bet on price at
all: LONG SPOT + SHORT PERP in equal size, so the legs cancel, and the return is
the funding rate the exchange pays shorts every 8 hours.

Backtested on 4.1 years of REAL Bybit funding history, 52 symbols, costs charged
on BOTH legs at open and close (~0.31% round trip).

  leverage   CAGR      max drawdown
  1x        +8.26%      -0.98%
  2x       +17.21%      -1.95%
  3x       +26.89%      -2.92%
  5x       +48.71%      -4.82%

OUT OF SAMPLE (validated, positive in every window):
  oldest 730d (in-sample) : +34.93% CAGR, DD -1.58%
  newest 365d (OOS)       : +11.18% CAGR, DD -1.10%
  newest 180d (OOS)       : +15.35% CAGR, DD -1.60%

COMPARED TO v6 (the best directional result): 12.62% CAGR at -41.94% drawdown.
The carry earns more per unit of risk by more than an order of magnitude, and
THAT is the point -- a sub-2% drawdown can safely carry 5x leverage, where 5x on
a -42% drawdown strategy is liquidation. This is why desks run carry and not
signal-chasing.

IMPLEMENTATION NOTE THAT IS THE WHOLE RESULT: the first version exited on a
SINGLE negative funding print and re-entered on the next positive one. That
produced 2249 round trips, $193 of costs against $70 of funding, and a -61.50%
return. The strategy was never the problem -- the churn was. Funding oscillates
around zero constantly; only a SUSTAINED reversal (9 consecutive negative prints,
3 days) means the premise is gone. With hysteresis: 33 positions instead of 2249,
$4.33 of costs instead of $193.

HONEST LIMITS, so this is not over-claimed later:
- OOS CAGR (11-15%) is well below in-sample (35%). Funding has compressed as the
  trade became crowded. Assume the lower number.
- Modelled: funding flipping negative, both legs' fees. NOT modelled: leg drift
  (spot and perp prices diverging), exchange risk, liquidation on the short leg
  if margin is mismanaged, and borrow limits on the spot leg.
- It needs BOTH legs. The live account currently runs perps only.

## 2026-09-23 — PORTFOLIO BLEND, and a Sharpe number that is NOT real
Research on crypto quant funds is consistent that "the best quant funds are
essentially portfolios of strategies, not a single algorithm" and that the
category's ~1.53 median Sharpe comes largely from diversification. This repo
spent its whole life hunting for THE signal, which was the wrong question.

Blending the two books (daily returns, 4.1y):
  100% trend      CAGR +16.78%  DD -43.95%  Sharpe 0.78
   60% carry       CAGR +19.59%  DD  -9.16%  Sharpe 1.85
   75% carry       CAGR +19.84%  DD  -5.81%  Sharpe 2.87
  100% carry      CAGR +19.80%  DD  -1.78%  Sharpe 11.37   <-- NOT REAL

**THE 11.37 SHARPE IS A MODELLING ARTIFACT AND MUST NOT BE PROMOTED.** The carry
model credits funding as a smooth deterministic drip with NO variance on the
hedge. Real carry books get their volatility from BASIS RISK -- the two legs
drifting against each other -- which is not modelled at all here. The literature
is explicit that a Sharpe above 3 in 2026 signals methodology error, and this is
that error, self-inflicted.

What survives scrutiny:
  - CAGR ~11-20% is CREDIBLE. External check: Ethena runs this exact trade at
    scale and publicly reports 10-15% APY, bracketing our OOS 11-15%.
  - The -1.78% drawdown and 11+ Sharpe are NOT credible.
  - The defensible allocation is 60-75% carry / 25-40% trend, where drawdown
    (-6% to -9%) does not rest on the unmodelled assumption.

NEXT WORK, in priority order, for whoever picks this up:
  1. Model basis risk: fetch spot AND perp closes, mark the pair each bar, and
     let the hedge drift. Until that exists every carry risk number here is
     optimistic.
  2. Build the live two-leg executor (scripts/carry.py is scan/plan only; it
     does not place orders, deliberately).
  3. Pairs trading / stat arb as a third sleeve -- published Sharpe 1.4-1.5,
     market neutral, and genuinely uncorrelated with both of these.

## 2026-09-23 — PROMOTED: the TREND sleeve trades BTC+ETH ONLY
Prompted by a question about a discretionary trader who only traded BTC and ETH.
Tested rather than assumed, and it is the best directional result in this file.

  BTC+ETH, trend+regime : +113.37%  DD -35.68%  Sharpe 3.23  win 55.8%  156 trades
  33-coin basket        :  +97.07%  DD -41.94%  Sharpe 2.72  win 44.6% 1407 trades
  BTC+ETH, old momentum :   +2.80%  DD  -3.55%  Sharpe 1.22  win 44.3%

OUT OF SAMPLE it beats BTC in 2 of 3 windows, including a RISING one:
  last  500d  +24.33%  vs BTC -27.72%   = +52.05pp   DD -13.68%
  last  900d  +41.31%  vs BTC +11.66%   = +29.65pp   DD -18.60%
  last 1400d  +75.46%  vs BTC +367.20%  = -291pp     DD -21.92%

Beating BTC in a RISING market (900d) is the first time anything here has done
that. Drawdowns also fall hard: -13% to -22% against the basket's -42%.

MECHANISM, and it reframes 13 hypotheses: the standing verdict already said the
altcoin universe has a NEGATIVE median (-21.2% vs BTC +157.4% over 5.7y). Every
cross-sectional signal tested in this file was trying to pick winners out of a
pool that drifts DOWN. NOT FISHING THERE beat every signal that tried to
overcome the drift. The failure was never signal quality; it was the universe.

CARRY is unaffected and still uses the whole universe: it is market-neutral, so
altcoin drift cannot touch it, and the richest funding is usually paid on alts.

## 2026-09-23 — PAIRS / STAT-ARB: viable third sleeve, NOT shipped live
Built because published crypto stat-arb runs Sharpe ~1.4-1.5 market-neutral, and
because its return driver is uncorrelated with both existing sleeves:
  TREND needs a sustained move (fails in chop)
  CARRY needs crowded leverage paying funding (fails when funding is flat)
  PAIRS needs correlated coins to diverge then converge — it works BEST in chop,
        which is exactly when trend bleeds.

14 mean-reverting pairs found on 208 days of hourly data (corr > 0.70,
half-life 12h-14d). Best: LINK/SOL (0.841, 13.2d), DOGE/PEPE, DOGE/SHIB.

  z_in=2.5 z_out=0.0 : +12.79% CAGR, DD -5.75%,  93 trades, win 49.5%
  z_in=3.0 z_out=0.5 :  +5.86% CAGR, DD -11.45%, 239 trades, win 54.0%
  z_in=1.5 z_out=0.25:  +5.85% CAGR, DD -10.96%, 198 trades, win 60.1%
  z_in=2.0 z_out=0.5 : -20.49% CAGR, DD -19.16%, 290 trades, win 52.8%

FIRST VERSION WAS WRONG and is worth recording: it scored P&L with a hand-waved
formula (`(entry_z - z)/|entry_z| * 0.02`) rather than actual leg returns, and
reported -66.76%. Replacing it with the real calculation — long leg return minus
short leg return, halved for the two legs — flipped the best config to +12.79%.
Approximating P&L in a backtest is not a shortcut, it is a fabrication.

NOT PROMOTED TO LIVE, for one reason: pairs are selected on the SAME data the
strategy is tested on. That is look-ahead bias and makes every number here an
UPPER BOUND. Before this can be trusted it needs rolling pair selection using
only past data. Also unmodelled: permanent correlation breaks (a listing, a hack,
a delisting) where the spread never reverts and the stop is the only exit.

## 2026-09-23 — PROMOTED: CONVICTION SIZING (the bot sets its own risk per trade)
Owner directive: let the bot decide risk per trade rather than sizing everything
the same. Implemented as a Kelly-shaped multiplier — the trend's strength in the
asset's OWN volatility units (a z-score, capped at 3 sigma so nothing blows up)
scales the position between 0.5x and 8x the base size.

BTC+ETH, 5.5y daily:
  flat sizing              +113.37%  DD -35.68%  Sharpe 3.23
  conviction (max 3x)      +129.16%  DD -31.23%  Sharpe 3.50   <- better on BOTH
  conviction (max 8x)      +317.55%  DD -46.73%  Sharpe 4.00

OUT OF SAMPLE, max 8x — beats BTC by ~67pp in BOTH recent windows:
  last  500d  +39.31%  vs BTC -27.72%  = +67.04pp   DD -22.47%
  last  900d  +79.45%  vs BTC +11.66%  = +67.79pp   DD -30.11%
  last 1400d +157.54%  vs BTC +367.20% = -209.66pp  DD -30.11%

That is roughly 25-27% CAGR out of sample, against 19.8% for the previous build.

Note the max-3x row: it improved return AND drawdown AND Sharpe simultaneously,
which is the honest version of this result. The max-8x row buys more return with
more drawdown (-31% -> -47%) and should be read as a RISK CHOICE, not a free
lunch. It is shipped because the owner explicitly asked for maximum aggression.

CAVEAT, recorded because the literature is explicit about it: a Sharpe of 4.00
is in the range that "should make you suspicious of methodology errors". The
suspects here are survivorship bias in the universe (dead coins absent) and the
fact that BTC+ETH over this window were two of the best-performing assets in
existence. Out-of-sample consistency is reassuring but does not clear it.

## 2026-09-23 — CARRY: two corrections, both DOWNWARD. Read before allocating.

### 1. The expanded-universe result was untradable
Widening the funding cache 52 -> 235 symbols produced +48.23% CAGR full period
and +88.58% over 180d. It looked like the best result of the project.

NINE OF THE TEN HIGHEST-FUNDING NAMES HAVE NO SPOT MARKET ON BYBIT.
Carry is long spot + short perp. A perp with no spot listing cannot be hedged,
so "carrying" it is a naked leveraged short wearing a carry costume. And the
reason those names pay extreme funding is exactly that no arbitrageur can hold
the rate down — the same reason the trade is impossible there. The most
attractive number in the file was the most impossible.
Fixed: backtest/funding_carry.py now filters to symbols in data/hedgeable.json
(both a perp AND a spot market). 235 -> 133 tradable symbols.

### 2. Carry is REGIME-DEPENDENT and is currently NEGATIVE
Hedgeable-only, 3x, min_rate 0.0005, 5 slots:
  full 4.1y    +37.62% CAGR   DD  -7.55%   funding +$566.17
  last  365d   +14.84% CAGR   DD  -7.69%   funding  +$35.27
  last  180d   -11.72% CAGR   DD -22.88%   funding   -$9.26   <-- NEGATIVE

The last six months LOST money: the book paid more funding than it collected.
Funding has compressed and frequently gone negative, and the 3-day hysteresis
that correctly prevents churn also holds through sustained negative regimes.

CONSEQUENCE FOR THE SHIPPED ALLOCATION: the 75% carry / 25% trend split was
chosen on the older, flattering numbers. On the last 180 days of TRADABLE data
that allocation loses. Do NOT run 75% carry without a regime gate that turns the
sleeve off when funding is broadly negative — that gate does not exist yet and
is the single most important open item.

WHAT SURVIVES: carry is real and pays +37.62% over the full period, but it is a
REGIME trade, not an all-weather income stream. It earns when leverage is
crowded long and bleeds when it is not. Ethena's public 10-15% APY is a
multi-year average across both regimes, which is the honest expectation.
