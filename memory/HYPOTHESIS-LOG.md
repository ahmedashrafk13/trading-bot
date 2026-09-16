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

## Log

| # | date | drawn from | hypothesis | test to run | status | result |
|---|------|-----------|------------|-------------|--------|--------|
| 1 | 2026-09-16 | DOT/UNI/XRP, 3 straight stop-outs | A 6% trail is inside hourly crypto noise, so stops fire on wiggle rather than on a broken thesis | `run.py --set tac_trail=0.20` vs `0.06` | CONFIRMED | Wider is better at every step; best is no stop at all (-5.8% vs -44.8%) |
| 2 | 2026-09-16 | 11 research HOLDs out of 11 | The research gate rejects every candidate, so CORE can never originate | count originations with the gate modelled off | CONFIRMED | The screen passes a median of 8 coins/hour; the gate, not the screen, is the constraint |
| 3 | 2026-09-17 | STEP 5 standing-assumption test (no trade closed since last run) | The 85% deployment ceiling is untested and may be too loose: if it rarely binds, most of its "room" is unused, and if it DOES bind on some entries, those marginal entries may be net-negative given the account's measured lack of edge | `run.py --set max_deploy=k` sweep (0.30/0.50/0.65/0.85/1.00), then 60/40 split + 4 rolling quarters at 0.30 vs 0.85 | CONFIRMED | 0.65-1.00 are identical (cap never binds there); 0.30 beats 0.85 on return AND drawdown in the train half, the test half, and all 4 individual quarters — no exception. See standing verdict above. |
| 4 | 2026-09-17 | STEP 4B non-price data (funding rate, per learn.md's "best remaining bet") | Extreme perp funding (crowded leverage) precedes a reversal, so -funding should predict forward return | `research.py` IC on new `funding_contrarian` signal (Bybit D universe, `backtest/fetch_funding.py`) | REJECTED | IC does not clearly beat RANDOM at any horizon (t<2 throughout); see standing verdict above. |
| 5 | 2026-09-17 | STEP 4B combination idea | Momentum conditioned on calm (non-crowded) funding beats momentum alone | `research.py` IC on new `momentum_if_funding_calm` signal vs `momentum_30d` | CONFIRMED (30d only, signal-level) | @30d roughly doubles unconditioned momentum's OOS IC, same sign both halves; @1d/@7d sign flips train-to-test, unusable. Not promoted — no engine implementation of funding-gated entries exists yet to backtest at the P&L level. See standing verdict above. |
