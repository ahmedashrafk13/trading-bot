# Backtester

Replays the v2 two-sleeve rulebook (`memory/TRADING-STRATEGY.md`) over historical
Alpaca crypto bars, so strategy questions can be answered in minutes instead of
at the live rate of roughly one closed trade every two days.

Stdlib + numpy only. No pandas, no new dependencies.

## Quick start

```bash
python backtest/fetch.py --days 400      # download + cache hourly bars (~15 min)
python backtest/test_engine.py           # verify the engine is not cheating
python backtest/run.py                   # backtest the shipped defaults
python backtest/run.py --trades          # ...and list every closed trade
python backtest/sweep.py --quick         # parameter search with an OOS verdict
```

## Files

| file | what it does |
|---|---|
| `fetch.py` | Downloads hourly bars per symbol, follows pagination to exhaustion, caches to `data/bars/1H/`. |
| `engine.py` | The rule replay: screen, sizing, trails, ratchets, hard cuts, fees, slot caps, circuit breaker. Plus metrics. |
| `run.py` | One backtest, one report. `--set key=val` overrides any parameter. |
| `sweep.py` | Parameter search with train/test split, top-N stability and walk-forward. |
| `test_engine.py` | Invariant tests on synthetic bars with known answers. |
| `signals.py` | Candidate entry signals + the information-coefficient machinery. |
| `research.py` | Signal bake-off: which rule predicts, in-sample and out, vs a random null. |
| `portfolio.py` | Time-series momentum + volatility targeting. A different engine, built on what the evidence and the literature both point to. |

## What the engine refuses to do

A backtester's failure mode is not a crash — it is a plausible number that is
wrong in the optimistic direction. These are pinned by `test_engine.py`:

- **No lookahead.** Signals are computed from bars up to and including the close
  of hour `i`; the order fills at the **open of hour `i+1`**.
- **Stops use the level resting before the bar**, checked against the intrabar
  low, and the trail is ratcheted only *after* that check. Ratcheting first
  would let a stop rise and fill within the same bar.
- **Gaps fill at the open, not the stop price.** Assuming you always get your
  stop price is the single most common way a backtest invents money.
- **Fees on both sides**, buy fees taken in kind exactly as Alpaca does. A flat
  round trip must lose money, and the test asserts it.
- **Slot caps, the 85% deployment ceiling and the circuit breaker** are enforced
  every bar, and reconstructed from the trade list to verify.

## Known limitations — read before trusting a number

1. **No historical spreads.** The bars endpoint does not carry bid/ask, so the
   screen's live spread filter (`<=1.0%` CORE, `<=0.5%` TACTICAL) cannot be
   replayed. It is approximated by a flat `spread_bps` cost. Results are
   therefore **optimistic for thin coins** the live screen would have rejected.
2. **Survivorship bias.** The universe is today's tradable list. Coins Alpaca
   delisted are absent, so the historical universe is slightly too healthy.
3. **The agent's judgement is not modelled.** Live, CORE and TACTICAL entries
   need a research-plan catalyst and the agent's discretion. The engine takes
   the top-ranked screen pass instead. It backtests the *mechanical* strategy,
   which is a floor on — not a forecast of — live behaviour.
4. **One regime.** 400 days of crypto is one macro environment. A result that
   only works on this slice is not a result.

## Start here: does the signal predict anything?

```bash
python backtest/research.py
```

Backtesting a whole strategy is confounded - sizing, trails, slots and fees all
sit between the signal and the result, so a losing backtest cannot tell you which
part was wrong. `research.py` strips all of it away and measures only whether the
signal at time `t` says anything about the return from `t` to `t+h`, as a rank
correlation (information coefficient) across ~250,000 symbol-hours.

This is also the honest answer to "I want more trades so it improves faster": a
live trade costs money and two days, an observation here costs nothing and there
are a quarter of a million of them.

Read every row against the RANDOM row, never against zero. The null wanders, and
how far it wanders IS the noise floor.

### What it found (2025-08 to 2026-09)

| signal | IC@24h train | IC@24h test | verdict |
|---|---|---|---|
| `momentum_7h` (bot TACTICAL) | -0.056 | -0.019 | **backwards** |
| `momentum_30d` (bot CORE) | -0.018 | -0.037 | **backwards** |
| `low_volatility` | +0.069 | +0.055 | best found (t=+12) |
| `below_sma20` | +0.073 | +0.013 | positive, decays fast |
| RANDOM (null) | +0.000 | +0.002 | the noise floor |

Both signals the bot trades on have NEGATIVE information coefficients in both
halves of the data. They are not edgeless, they are inverted.

But — and this is the important part — **feeding the good signals into the engine
does not make money either**:

| entry_signal | return | vs BTC |
|---|---|---|
| `momentum` (shipped) | -44.8% | -8.4pp |
| `lowvol` | -44.4% | -8.1pp |
| `reversion` | -58.0% | -21.7pp |
| `lowvol` + no stops + regime gate | -5.8% | +30.6pp |
| **cash (0 slots)** | **0.0%** | **+36.4pp** |

The reason is structural: an information coefficient is a *cross-sectional*
measure - it says you picked better coins than average. The bot is *long-only and
directional*. Picking the best-falling coin in a market where everything falls
still loses money. The edge that exists cannot be expressed by this vehicle.

The second structural finding: every widening of the trail improves the result,
monotonically, all the way to disabling stops entirely. The trailing stops are
harvesting noise, not protecting capital.

## Reading a sweep

`sweep.py` deliberately never reports an in-sample winner as an improvement.
With a few hundred combinations, the best in-sample result looks good by luck
alone. It reports instead:

- **In-sample best** — what the tuner found on the training slice. Ignore it.
- **Out-of-sample** — that same set on data the tuner never saw. Act on this.
- **Overfit gap** — the difference. Large gap = the tuner fitted noise.
- **Top-10 stability** — if the ten best in-sample sets straddle zero out of
  sample, the parameter surface is noise and tuning harder will not help.
- **Walk-forward** — retune on the past, trade the next slice, repeat. This is
  the only thing that answers "would this have worked live", because live you
  only ever have the past.

If walk-forward mean edge vs BTC is <= 0, the problem is the **signal**, not the
parameters, and no amount of retuning will fix it.

## Parameters

Every field of `engine.Params` is settable from the CLI:

```bash
python backtest/run.py --set tac_trail=0.20 --set core_risk=0.03
python backtest/run.py --set breaker_streak_resets_daily=true
```

That last one resolves the circuit-breaker day-boundary ambiguity logged in
`memory/OBSERVATIONS.md` — you can now measure which reading is better instead
of arguing about it.


## The strategy research, and where it ended (2026-09-16)

Grounded in the academic literature (see Sources at the bottom), which says two
things that match what this repo measured independently:

  * There is **hardly any cross-sectional momentum in crypto** - coins are ~0.8
    correlated, so ranking them barely helps. Time-series momentum (is THIS coin
    trending?) is the robust version.
  * **Volatility targeting** with inverse-vol sizing is the single largest
    risk-adjusted improvement available, because volatility is autocorrelated.

`portfolio.py` implements exactly that: per-asset trend signal, inverse-vol
weights scaled to a portfolio vol target, cash when the trend is off, no stops,
and costs charged on turnover rather than per round trip.

### Result over 400 days (2025-08 to 2026-09, a bear market)

| config | return | vs BTC | maxDD |
|---|---|---|---|
| shipped slot strategy | -44.8% | -8.4pp | -53.0% |
| tsmom 50d + BTC regime 100d | **+4.3%** | **+40.6pp** | -13.9% |

That looks like a win. **It is not.** It is a regime artifact.

### Result over 5.7 years (2021-01 to 2026-09, bull AND bear)

| config | return | CAGR | maxDD | Sharpe |
|---|---|---|---|---|
| **buy and hold BTC** | **+157.4%** | **+17.5%** | - | - |
| tsmom 50d + regime 100d | +7.0% | +1.2% | -48.3% | +0.19 |
| tsmom 50d + reg100, weekly rebal | +27.3% | +4.3% | -51.7% | +0.29 |
| tsmom 50d + reg100, vol target 30% | +17.2% | +2.8% | -32.5% | +0.24 |
| tsmom on BTC only, 50d | +52.3% | - | -60.2% | +0.39 |
| tsmom 50d, no regime | -50.5% | -11.6% | -75.3% | -0.13 |

**Nothing beat buying BTC and doing nothing.** Not the bot, not the fixed bot,
not the literature-best design, not even trend-following BTC itself.

### Why: the altcoin universe is the problem

Per-coin total return, 2021-01 to 2026-09, on the *survivorship-biased* list
(delisted coins are missing, so reality was worse):

| | |
|---|---|
| best | SOL +5147%, DOGE +1291%, ETH +227% |
| BTC | +157% |
| **median coin** | **-21.2%** |
| worst | SUSHI -97.6%, GRT -97.1%, TRUMP -95.0% |

The median altcoin lost a fifth of its value while BTC more than doubled. A
long-only bot drawing from this universe is picking from a pool with a deeply
negative median. Skill in selection has to overcome that before it earns a cent,
and no signal tested here is remotely strong enough.

### Honest limits of this conclusion

1. One asset class, one 5.7-year sample, ending in a drawdown.
2. Survivorship bias flatters every result above.
3. Long-only is assumed throughout. A market-neutral long/short book could in
   principle monetize the cross-sectional IC that `research.py` does find - that
   is a genuinely different vehicle, not a parameter change, and Alpaca crypto
   cannot express it.

## Sources

- [Time-Series and Cross-Sectional Momentum in the Cryptocurrency Market (Han, Kang, Ryu)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4675565)
- [Cryptocurrency momentum has (not) its moments](https://link.springer.com/article/10.1007/s11408-025-00474-9)
- [An Introduction to Volatility Targeting - QuantPedia](https://quantpedia.com/an-introduction-to-volatility-targeting/)
- [The Impact of Volatility Targeting - Man Group](https://www.man.com/insights/the-impact-of-volatility-targeting)
- [Catching Crypto Trends - Concretum Group](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/)
