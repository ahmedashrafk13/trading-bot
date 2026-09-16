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
