# backtest/lab — research harness

Independent of `backtest/engine.py`. numpy + pandas only (no scipy).
Run the pinned tests after ANY edit here:

    python backtest/lab/test_lab.py            # PASS/FAIL per test, exit 1 on failure
    python backtest/lab/test_lab.py -k adv     # only the adversarial section
    python backtest/lab/test_lab.py --bench    # + timing of run_weights on 50k x 20

| file | what |
|---|---|
| `data.py` | `load_panel`, `load_metrics`, `load_bybit_instruments` (data agent; read-only here) |
| `sim.py` | `run_weights`, `run_events`, `Result`, `slice_panel`, `effective_weights` |
| `metrics.py` | equity/trade statistics, deflated Sharpe, PBO (CSCV), BTC buy-and-hold |
| `wf.py` | `walk_forward`, `evaluate_lockbox`, `pre_lockbox`, `check_causality` |
| `nulls.py` | `random_timing_null`, `sign_flip_null` |
| `test_lab.py` | t01–t16 (spec) + adv01–adv26 (adversarial pass) |

## Timing contract (the one rule everything else hangs on)

* `weights[i, j]` / an entry with `i` is decided at the **close of bar i** using data `<= close i`.
* It fills at the **open of bar i+1**. Never at close i. The last row never executes.
* Positions are held in units between fills (notional drifts with price).

## sim.run_weights(panel, weights, **kw) -> Result

`weights[T, N]` = target signed notional / equity. Keywords (defaults):
`fee=0.00055` (Bybit VIP0 perp taker, per side), `slippage_bps=None` (1bp BTC/ETH,
3bp other majors, 8bp everything else; scalar or `[N]`), `funding=True`,
`max_gross_leverage=5.0`, `initial_equity=200.0`, `maint_margin=0.005`,
`instruments=None`, `round_to_qty=False`, `min_trade_frac=0.0`,
`rebalance="on_change"|"every_bar"`, `record_positions=True`.

* NaN weight or non-tradable symbol at the decision bar -> target 0 (closed at the next open).
* Each row is scaled so `sum|w| <= max_gross_leverage`. (In `on_change` mode untouched
  positions drift; the cap applies to targets, not to drifted notional.)
* Costs: `|delta notional| * (fee + slippage)` on every fill: rebalances, closes,
  liquidations, delisting closes.
* Funding: every bar with `panel.funding != 0`: `cash -= qty * close * rate` (rate > 0:
  longs pay). qty = held at the bar close.
* Liquidation (cross, pessimistic): each bar every leg is valued at its own adverse extreme
  (long at low, short at high); `worst_equity <= maint_margin * gross` -> everything closed at
  those prices minus costs, equity floored at 0, trading resumes from what is left. Also checked
  at the open before a rebalance.
* Held symbol with no price at the execution open (delisted/gap) -> closed at the last known
  close with a 2% adverse haircut, logged in `Result.delistings`.
* Equity `<= 1%` of initial at a close -> flattened at the next open, account stops.
* `round_to_qty=True` + `instruments=load_bybit_instruments()`: qty rounded down to `qtyStep`,
  orders below `minOrderQty` / `minNotionalValue` dropped (full closes always allowed).
* `min_trade_frac`: skip a symbol's trade when `|target w - current w|` is below it (closes to 0
  are never skipped).
* Note: a single missing / zero-volume bar makes the symbol non-tradable for that bar, so a held
  position is closed and re-opened (two sets of costs). That is the spec. The costs are
  pessimistic, but the price move between the two opens can go either way. Example: the
  exchange-wide 1h halt at 2024-10-28 20:00 UTC (v=0) makes a 1x BTC hold on 1h bars sell at
  69650 and buy back at 69770, and it ends 0.29% below the same hold without that round trip
  (smoke test 2026-09-24).

## sim.run_events(panel, entries, *, exits=None, max_concurrent=5, allow_flip=False, **same) -> Result

Entry dict: `i` (or `t` = bar open time), `j` (or `symbol`), `side` (+1/-1), `size` (levered
notional / equity), `stop` | `stop_pct`, `target` | `target_pct`, `time_stop` (bars; exit at the
open of entry_bar + time_stop), `trail` (fraction). `exits[T, N]` bool: close at the next open.
Per bar: (1) exits at the open (time stop, exit signal, non-tradable, <=1% kill) + gap
liquidation check; (2) entries fill at the open (rejected: not tradable / no price / already
open / max_concurrent / stop or target on the wrong side / no leverage room / below minimum;
see `Result.rejected`); (3) stops and targets, **including the entry bar** (the fill is the
bar's first price): open beyond the stop -> fill at the OPEN; open beyond the target -> fill AT
THE TARGET; stop and target both inside the range -> STOP. Liquidation is evaluated along the
pessimistic intrabar path, so a stop placed beyond the liquidation price cannot rescue the
account; (4) trailing stops ratchet after the check; (5) liquidation on what is left; (6)
funding, mark.

## Result

`t, dt, symbols, equity[T]` (marked at each close), `cash[T]`, `positions[T, N]` (qty),
`gross_leverage[T]`, `fees_paid`, `slippage_paid`, `funding_paid` (+ = paid),
`n_liquidations`, `liquidations`, `delistings`, `turnover` (sum |traded| / equity),
`notional_traded`, `rejected`, `trades` (lazy `TradeTable`: symbol, side, open_t, close_t,
open_bar, close_bar, entry, exit, qty_max, entry_notional, pnl incl. costs and funding, ret on
notional, fees, funding, is_open; `.df()` for pandas; sum of pnl == equity_end - initial),
`.metrics()`.

## metrics

`equity_metrics(t, dt, equity, initial)`: sharpe = mean/std(ddof=1) of **daily UTC** returns x
sqrt(365) (a bar closing at 00:00 belongs to the day that ended), sortino, cagr with
365.25-day years over `t[-1] + dt - t[0]`, max_drawdown (negative, on marked equity incl. the
initial value), calmar, vol, skew, Pearson kurtosis, psr, monthly stats. `compute(res)` adds
trade stats (win_rate, profit_factor, avg_win/avg_loss on notional, trades_per_week = trips
opened per week, avg_hold_hours), exposure (mean gross leverage), turnover_per_year,
fee_drag_per_year, funding_per_year, n_liquidations, n_delistings.
`deflated_sharpe(sr_annual, n_trials, n_days, skew, kurt, trials_sr_std_annual=None,
periods_per_year=365)` — Bailey & Lopez de Prado 2014 (reproduces the paper's example 0.9004;
without `trials_sr_std_annual` it uses the null estimator variance 1/(n-1)).
`pbo_cscv(returns[T, K], S=16)` — Bailey et al. CSCV. `btc_buy_hold(panel)`: a SPOT benchmark.
It buys at the open of bar 0 with one fee and no slippage, and it pays no funding. `run_weights`
cannot fill before the open of bar 1, so its numbers differ slightly: on 1d 2021-01..2025-06 the
CAGR is 33.76% here and 33.37% from run_weights.

**Perp buy-and-hold is not spot buy-and-hold.** With `funding=True` a 1x BTC perp held in units
(on_change, never re-sized) pays its funding out of cash. That pushes real leverage above 1x:
from 2021-01-01 it had paid $113 of funding on a $200 start by Nov 2022 and was LIQUIDATED on
2022-11-09. The same hold re-sized every bar (`rebalance="every_bar"`) survives: CAGR 17.5%,
max DD -78.9%, Sharpe 0.57, against 33.4% / -76.7% / 0.78 without funding. BTC funding summed
to 0.31 of notional in 2021 (0.04 to 0.12 in the later years).

## wf

`walk_forward(panel, strategy_fn, grid, train_days=730, test_days=182, step_days=182,
objective="sharpe"|"calmar"|"cagr_dd"|callable, mode="rolling"|"anchored",
kind="weights"|"events", sim_kwargs=None, start=None, end=None, allow_lockbox=False,
causality_checks=2, lockbox_log_path=None, compute_pbo=False)` -> dict with `oos_result`,
`oos_equity`, `oos_metrics` (+ `dsr` with n_trials = len(grid)), `folds` (dates, chosen params,
train score, test metrics), `chosen_params`, `scores`, `n_trials`.

* Selection sees a panel truncated at the train end (meta arrays included).
* The OOS run is ONE simulation over all test folds: capital and positions carry over.
* **Causality is enforced**: every fold re-runs the chosen strategy on panels cut inside
  the test fold; any change to an earlier signal raises `ValueError("... not causal ...")`.
  The cut panel's last bar is compared too (that is where a one-bar look-ahead shows), so a
  strategy must treat its final bar like any other bar.
* **Lockbox** = bars closing after 2025-07-01 00:00 UTC. `walk_forward` cuts them off and
  raises for `end` > lockbox unless `allow_lockbox=True`; such a run is logged.
  `evaluate_lockbox(panel, strategy_fn, params, label)` runs once on [2025-07-01, end] and
  appends `counter<TAB>label<TAB>params<TAB>metrics` to `lockbox.log`; `lockbox_count()`.
* Direct `run_weights` / nulls / `check_causality` calls cannot see the boundary: pass them
  `pre_lockbox(panel)`.

## nulls

`random_timing_null(panel, weights, n=200, seed=0, method="auto"|"runs"|"shift")` — per symbol,
permute the runs of constant weight (same values, same holding lengths, no extra changes) or
circularly shift; `sign_flip_null(panel, weights, n, seed)` — flip each same-sign run with p=1/2
(|weights| identical). Both re-simulate with the same costs and return the null distribution,
`p_value = (1 + #null >= strategy) / (n + 1)`, percentile, and turnover / exposure of both.

## Known limits (not modelled; each makes results look BETTER than reality unless noted)

* Per-symbol fees: one fee for every symbol (spot taker is 0.10% on Bybit, not 0.055%).
* Liquidation leaves the account its worst-case equity (floored at 0); a real exchange also
  keeps the maintenance margin (~0.5% of notional, ~2.5% of equity at 5x).
* On 1d bars (or coins with 1h/4h funding on 4h bars) funding settled INSIDE a bar is
  missed when a stop exits in that bar before the close (optimistic for the paying side,
  pessimistic for the receiving side).
* A trailing stop never fires inside the bar that set its new high (next-bar open instead);
  a gap up past the ratcheted stop can make that optimistic.
* No partial fills, no order-book depth beyond the flat slippage tiers.
