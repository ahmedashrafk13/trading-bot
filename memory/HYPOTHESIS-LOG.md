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
| Short-horizon momentum (the TACTICAL rule) is INVERTED | IC -0.050 test, t=-13, vs null 0.002 | CONFIRMED |
| 30-day momentum (the CORE rule) is INVERTED | IC -0.037 test, t=-10 | CONFIRMED |
| Low volatility predicts higher forward return | IC +0.065 @168h, t=+16 | CONFIRMED |
| Trailing stops harvest noise; wider is always better | -44.8% -> -5.8% as trail widens to none | CONFIRMED |
| Higher trade frequency is strictly worse | 5.9 trades/day = -95.9%; -49.4% even at ZERO fees | CONFIRMED |
| Cross-sectional selection cannot be monetized long-only | lowvol signal has real IC, still returns -44% in the engine | CONFIRMED |
| Nothing tested beats buy-and-hold BTC | 5.7y: BTC +157.4%, best variant +27.3% | CONFIRMED |
| The altcoin universe has a negative median | median coin -21.2% vs BTC +157.4% over 5.7y | CONFIRMED |

## Log

| # | date | drawn from | hypothesis | test to run | status | result |
|---|------|-----------|------------|-------------|--------|--------|
| 1 | 2026-09-16 | DOT/UNI/XRP, 3 straight stop-outs | A 6% trail is inside hourly crypto noise, so stops fire on wiggle rather than on a broken thesis | `run.py --set tac_trail=0.20` vs `0.06` | CONFIRMED | Wider is better at every step; best is no stop at all (-5.8% vs -44.8%) |
| 2 | 2026-09-16 | 11 research HOLDs out of 11 | The research gate rejects every candidate, so CORE can never originate | count originations with the gate modelled off | CONFIRMED | The screen passes a median of 8 coins/hour; the gate, not the screen, is the constraint |
