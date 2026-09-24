"""
backtest/lab/wf.py -- walk-forward optimisation, the lockbox, causality check.

walk_forward(panel, strategy_fn, grid, ...)
    For each fold: every params dict in `grid` is scored on the TRAIN window
    only, the best is chosen, and that single choice is run on the TEST
    window. The test windows are stitched into ONE out-of-sample simulation
    (capital and open positions carry across fold boundaries; a params change
    at a boundary simply changes the targets).

    What the harness guarantees (pinned by test_lab.py):
      * During selection, strategy_fn receives a panel TRUNCATED at the end of
        the train window -- it cannot see a single test bar, even if it is
        not causal.
      * During the test run, strategy_fn receives a panel truncated at the
        end of the test fold. The strategy must be CAUSAL (weights[i] may
        only use bars <= i). This is ENFORCED: every fold recomputes the
        chosen strategy on `causality_checks` panels cut inside the test
        fold and raises ValueError if any earlier signal changes.
      * Truncation includes the [T, ...] arrays inside panel.meta (valid,
        member, tbqv, n_hours): they used to be passed whole, handing the
        train folds the future (and the lockbox).
      * LOCKBOX: bars whose close is after 2025-07-01 00:00 UTC are cut off
        before strategy_fn ever sees the panel. Asking for end > lockbox
        raises unless allow_lockbox=True, and such a run is logged to
        lockbox.log like evaluate_lockbox. Direct sim/null calls cannot see
        the lockbox boundary: give them pre_lockbox(panel).

evaluate_lockbox(panel, strategy_fn, params, label)
    ONE evaluation on [lockbox, end]. Appends a line to lockbox.log every time
    it is called so the number of looks is auditable.

Strategy signature
    kind="weights": strategy_fn(panel, params) -> weights [T, N] for the panel
                    it was GIVEN (same T as that panel).
    kind="events":  strategy_fn(panel, params) -> list of entry dicts
                    (see sim.run_events), 'i' indexing the panel it was given;
                    or a dict {"entries": [...], "exits": bool [T, N]}.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

try:
    from . import metrics as M
    from . import sim as S
except ImportError:                       # run as a plain script directory
    import metrics as M
    import sim as S

DAY = 86400
LOCKBOX_ISO = "2025-07-01T00:00:00"
LOCKBOX_TS = int(np.datetime64(LOCKBOX_ISO, "s").astype(np.int64))
LOCKBOX_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lockbox.log")


def to_ts(x) -> int:
    """epoch seconds from int / ISO string / numpy datetime64 / pandas Timestamp."""
    if x is None:
        return None
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, str):
        return int(np.datetime64(x.replace("Z", ""), "s").astype(np.int64))
    if isinstance(x, np.datetime64):
        return int(x.astype("datetime64[s]").astype(np.int64))
    if hasattr(x, "timestamp"):
        return int(x.timestamp())
    raise TypeError(f"cannot interpret {x!r} as a time")


def _iso(ts: int) -> str:
    return str(np.datetime64(int(ts), "s"))


# --------------------------------------------------------------------------- #
# objectives
# --------------------------------------------------------------------------- #
def score(m: dict, objective, dd_limit: float = -0.30) -> float:
    """Higher is better.
      sharpe  -- daily Sharpe
      calmar  -- cagr / |maxDD|
      cagr_dd -- CAGR among configs whose maxDD is no worse than dd_limit;
                 configs breaching it rank below every feasible one (by calmar).
      callable(metrics) -> float also accepted."""
    if callable(objective):
        return float(objective(m))
    if objective == "sharpe":
        v = m["sharpe"]
    elif objective == "calmar":
        v = m["calmar"]
        v = 1e6 if math.isinf(v) else v
    elif objective == "cagr_dd":
        if m["max_drawdown"] >= dd_limit:
            v = m["cagr"]
        else:
            v = -1e6 + max(min(m["calmar"], 1e5), -1e5)
    else:
        raise ValueError(f"unknown objective {objective!r}")
    return float(v) if np.isfinite(v) else -1e9


def _light_metrics(res) -> dict:
    """Equity-only metrics (no trade reconstruction) for scoring grids."""
    m = M.equity_metrics(res.t, res.dt, res.equity, res.initial_equity)
    m["n_liquidations"] = res.n_liquidations
    return m


# --------------------------------------------------------------------------- #
# plumbing
# --------------------------------------------------------------------------- #
def _call(strategy_fn, panel, params, kind):
    out = strategy_fn(panel, params)
    if kind == "weights":
        w = np.asarray(out, dtype=float)
        if w.shape != (len(panel.t), len(panel.symbols)):
            raise ValueError(f"strategy_fn returned {w.shape}, expected "
                             f"{(len(panel.t), len(panel.symbols))}")
        return w
    if isinstance(out, dict):
        return {"entries": list(S._normalise_entries(out.get("entries"), panel)),
                "exits": out.get("exits")}
    return {"entries": list(S._normalise_entries(out, panel)), "exits": None}


def _run_slice(panel, sig, a, b, kind, sim_kwargs, record=False):
    """Simulate bars [a, b) of `panel` using signals computed on panel[:>=b]."""
    sub = S.slice_panel(panel, a, b)
    kw = dict(sim_kwargs or {})
    kw.setdefault("record_positions", record)
    if kind == "weights":
        return S.run_weights(sub, sig[a:b], **kw)
    ents = [dict(e, i=e["i"] - a) for e in sig["entries"] if a <= e["i"] < b - 1]
    ex = sig.get("exits")
    ex = None if ex is None else np.asarray(ex, bool)[a:b]
    return S.run_events(sub, ents, exits=ex, **kw)


def _cut_at(panel, end_ts: int):
    """Keep bars whose CLOSE is <= end_ts."""
    t = np.asarray(panel.t, dtype=np.int64)
    n = int(np.searchsorted(t + int(panel.dt), end_ts, side="right"))
    return S.slice_panel(panel, 0, n)


def make_folds(t, dt, train_days, test_days, step_days, mode, start_ts=None,
               min_test_days=30):
    """List of (train_start, train_end=test_start, test_end) as bar indices."""
    t = np.asarray(t, dtype=np.int64)
    end = int(t[-1]) + int(dt)
    t0 = int(t[0]) if start_ts is None else int(start_ts)
    folds, k = [], 0
    while True:
        test_start = t0 + train_days * DAY + k * step_days * DAY
        if mode == "rolling":
            train_start = test_start - train_days * DAY
        elif mode == "anchored":
            train_start = t0
        else:
            raise ValueError("mode must be 'rolling' or 'anchored'")
        test_end = min(test_start + test_days * DAY, end)
        if test_end - test_start < min_test_days * DAY:
            break
        ia = int(np.searchsorted(t, train_start))
        ib = int(np.searchsorted(t, test_start))
        ic = int(np.searchsorted(t, test_end))
        if ib - ia < 2 or ic - ib < 1:
            break
        folds.append((ia, ib, ic))
        k += 1
    return folds


# --------------------------------------------------------------------------- #
# walk-forward
# --------------------------------------------------------------------------- #
def walk_forward(panel, strategy_fn, grid, *, train_days: int = 730,
                 test_days: int = 182, step_days: int = 182,
                 objective="sharpe", mode: str = "rolling", kind: str = "weights",
                 sim_kwargs: dict | None = None, start=None, end=None,
                 allow_lockbox: bool = False, min_test_days: int = 30,
                 dd_limit: float = -0.30, compute_pbo: bool = False,
                 pbo_S: int = 16, verbose: bool = False, causality_checks: int = 2,
                 lockbox_log_path: str | None = None, label: str = "") -> dict:
    """Walk-forward with parameter selection on train folds only.

    start: first train window start (default: first bar; earlier bars stay
           available to the strategy as warm-up history).
    end:   exclusive end time (default: the lockbox, or the panel end if
           earlier). end > lockbox raises unless allow_lockbox=True; a run
           that does reach into the lockbox is appended to lockbox.log (it IS
           a look).
    causality_checks: per fold, recompute the chosen strategy on this many
           panels truncated inside the test fold and require identical
           signals on the common bars; a mismatch raises ValueError (the
           strategy peeks at later bars -- in-fold look-ahead the fold split
           cannot stop). 0 disables.
    Returns dict:
      oos_result   sim.Result of the stitched out-of-sample run
      oos_equity, oos_t
      oos_metrics  full metrics + 'dsr' (deflated Sharpe with n_trials=len(grid))
      folds        per fold: train/test dates, chosen params, train score,
                   test metrics (from the stitched equity)
      chosen_params, scores [n_folds, len(grid)], n_trials
      pbo          (compute_pbo=True) CSCV PBO of the grid's daily returns on
                   the whole pre-lockbox sample
    """
    if not grid:
        raise ValueError("grid is empty")
    end_ts = to_ts(end)
    lock_end = None if allow_lockbox else LOCKBOX_TS
    if end_ts is not None and lock_end is not None and end_ts > lock_end:
        raise ValueError(f"walk_forward end {_iso(end_ts)} is inside the lockbox "
                         f"(>= {LOCKBOX_ISO}); pass allow_lockbox=True deliberately")
    cut = min(x for x in (end_ts, lock_end, int(panel.t[-1]) + int(panel.dt)) if x is not None)
    P = _cut_at(panel, cut)          # strategy_fn never sees anything past `cut`
    T = len(P.t)
    folds = make_folds(P.t, P.dt, train_days, test_days, step_days, mode,
                       to_ts(start), min_test_days)
    if not folds:
        raise ValueError("no folds fit: panel too short for train_days + min_test_days")
    kw = dict(sim_kwargs or {})
    scores = np.full((len(folds), len(grid)), np.nan)
    chosen, fold_info = [], []

    if kind == "weights":
        oos_sig = np.zeros((T, len(P.symbols)))
    else:
        oos_sig = {"entries": [], "exits": np.zeros((T, len(P.symbols)), bool)}
    oos_a, oos_b = folds[0][1], folds[-1][2]

    for f, (ia, ib, ic) in enumerate(folds):
        train_panel = S.slice_panel(P, 0, ib)            # NOTHING at/after test start
        for g, params in enumerate(grid):
            sig = _call(strategy_fn, train_panel, params, kind)
            res = _run_slice(train_panel, sig, ia, ib, kind, kw)
            scores[f, g] = score(_light_metrics(res), objective, dd_limit)
        best = int(np.nanargmax(scores[f]))
        chosen.append(grid[best])
        test_panel = S.slice_panel(P, 0, ic)
        sig = _call(strategy_fn, test_panel, grid[best], kind)
        if causality_checks:
            _guard_causal(strategy_fn, P, grid[best], kind, sig, ib, ic,
                          causality_checks, seed=f)
        if kind == "weights":
            oos_sig[ib:ic] = sig[ib:ic]
        else:
            oos_sig["entries"].extend(e for e in sig["entries"] if ib <= e["i"] < ic)
            if sig.get("exits") is not None:
                oos_sig["exits"][ib:ic] = np.asarray(sig["exits"], bool)[ib:ic]
        fold_info.append({"fold": f, "train_start": _iso(P.t[ia]), "test_start": _iso(P.t[ib]),
                          "test_end": _iso(int(P.t[ic - 1]) + int(P.dt)),
                          "bars": (ia, ib, ic), "params": grid[best],
                          "train_score": float(scores[f, best])})
        if verbose:
            print(f"fold {f}: test {fold_info[-1]['test_start']}..{fold_info[-1]['test_end']} "
                  f"params={grid[best]} train_score={scores[f, best]:.3f}")

    # one stitched out-of-sample simulation
    oos = _run_slice(P, oos_sig, oos_a, oos_b, kind, kw, record=True)
    om = oos.metrics()
    r = M.daily_returns(oos.t, oos.dt, oos.equity, oos.initial_equity)
    om["n_trials"] = len(grid)
    om["dsr"] = M.deflated_sharpe(om["sharpe"], len(grid), max(r.size, 2),
                                  om["skew"], om["kurtosis"])
    # per-fold test metrics from the stitched curve
    for fi in fold_info:
        _, ib, ic = fi["bars"]
        a, b = ib - oos_a, ic - oos_a
        start_eq = oos.initial_equity if a == 0 else float(oos.equity[a - 1])
        fi["test_metrics"] = M.equity_metrics(oos.t[a:b], oos.dt, oos.equity[a:b], start_eq)
    out = {"oos_result": oos, "oos_equity": oos.equity, "oos_t": oos.t,
           "oos_metrics": om, "folds": fold_info, "chosen_params": chosen,
           "scores": scores, "n_trials": len(grid), "objective": str(objective),
           "mode": mode, "data_end": _iso(cut)}
    if compute_pbo and len(grid) >= 2:
        cols = []
        for params in grid:
            sig = _call(strategy_fn, P, params, kind)
            res = _run_slice(P, sig, 0, T, kind, kw)
            cols.append(M.daily_returns(res.t, res.dt, res.equity, res.initial_equity))
        out["pbo"] = M.pbo_cscv(np.column_stack(cols), S=pbo_S)
    if int(oos.t[-1]) + int(oos.dt) > LOCKBOX_TS:           # this run looked inside
        out["lockbox_counter"] = _log_look(
            lockbox_log_path, f"walk_forward(allow_lockbox=True) {label}".strip(),
            {"grid": grid, "chosen": chosen}, om)
    return out


# --------------------------------------------------------------------------- #
# lockbox
# --------------------------------------------------------------------------- #
_LOG_KEYS = ("cagr", "max_drawdown", "sharpe", "sortino", "calmar", "total_return",
             "final_equity", "n_trades", "win_rate", "trades_per_week", "exposure",
             "n_liquidations", "fee_drag_per_year", "funding_per_year", "start", "end")


def lockbox_count(log_path: str | None = None) -> int:
    path = log_path or LOCKBOX_LOG
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as fh:
        return sum(1 for ln in fh if ln.strip())


def evaluate_lockbox(panel, strategy_fn, params, label: str, *, kind: str = "weights",
                     sim_kwargs: dict | None = None, log_path: str | None = None,
                     causality_checks: int = 3) -> dict:
    """Run ONE evaluation on bars from 2025-07-01 onward. The strategy gets the
    full panel (history before the lockbox is warm-up); the simulation starts
    flat at the first lockbox bar. Every call appends a line to the log:
        <counter>\\t<label>\\t<params json>\\t<metrics json>"""
    t = np.asarray(panel.t, dtype=np.int64)
    a = int(np.searchsorted(t, LOCKBOX_TS))
    if a >= len(t) - 1:
        raise ValueError("panel has no bars inside the lockbox")
    sig = _call(strategy_fn, panel, params, kind)
    if causality_checks:
        _guard_causal(strategy_fn, panel, params, kind, sig, a, len(t), causality_checks,
                      seed=0)
    res = _run_slice(panel, sig, a, len(t), kind, sim_kwargs, record=True)
    m = res.metrics()
    n = _log_look(log_path, label, params, m)
    return {"result": res, "metrics": m, "counter": n, "log_path": log_path or LOCKBOX_LOG}


def _log_look(log_path, label, params, m) -> int:
    path = log_path or LOCKBOX_LOG
    n = lockbox_count(path) + 1
    line = "\t".join([str(n), str(label).replace("\t", " "),
                      json.dumps(params, sort_keys=True, default=str),
                      json.dumps({k: m.get(k) for k in _LOG_KEYS}, default=str)])
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return n


# --------------------------------------------------------------------------- #
# causality check
# --------------------------------------------------------------------------- #
def pre_lockbox(panel):
    """The panel cut to bars whose close is <= the lockbox. Use this for ANY
    research call that does not go through walk_forward (direct run_weights,
    nulls, check_causality, PBO): those functions cannot tell that the panel
    handed to them reaches into the lockbox."""
    return _cut_at(panel, LOCKBOX_TS)


def _entry_keys(entries, a, b):
    keys = []
    for e in entries:
        if a <= e["i"] < b:
            keys.append(tuple((k, round(v, 10) if isinstance(v, float) else v)
                              for k, v in sorted(e.items()) if k != "n"))
    return sorted(keys, key=repr)


def _guard_causal(strategy_fn, panel, params, kind, sig, a, b, n_checks, seed=0):
    """Raise ValueError if the signals for bars [a, cut) change when the panel
    is truncated at `cut` (a < cut < b): the strategy used bars >= cut.
    The truncated panel's LAST bar is compared too -- that is the only bar
    where a one-bar look-ahead (shift(-1), c[i+1]) shows. Consequence: a
    strategy must treat its last bar like any other (no "skip the final
    bar" special cases), or it is indistinguishable from a peek."""
    if b - a < 3:
        return
    rng = np.random.default_rng(1_000_003 + int(seed))
    cuts = sorted(set(int(x) for x in rng.integers(a + 1, b, size=int(n_checks))))
    for cut in cuts:
        cut_ = cut
        s2 = _call(strategy_fn, S.slice_panel(panel, 0, cut), params, kind)
        if kind == "weights":
            x, y = sig[a:cut], s2[a:cut]
            same = (np.isclose(x, y, atol=1e-10, rtol=0) | (np.isnan(x) & np.isnan(y))).all(axis=1)
            if not same.all():
                bad = a + int(np.flatnonzero(~same)[0])
                raise ValueError(f"strategy_fn is not causal: weights at bar {bad} "
                                 f"({_iso(panel.t[bad])}) change when bars >= {cut_} "
                                 f"are removed (params={params})")
        else:
            if _entry_keys(sig["entries"], a, cut) != _entry_keys(s2["entries"], a, cut):
                raise ValueError(f"strategy_fn is not causal: entries in bars [{a}, {cut}) "
                                 f"change when bars >= {cut_} are removed (params={params})")
            e1, e2 = sig.get("exits"), s2.get("exits")
            if (e1 is None) != (e2 is None) or (
                    e1 is not None and not np.array_equal(np.asarray(e1, bool)[a:cut],
                                                          np.asarray(e2, bool)[a:cut])):
                raise ValueError(f"strategy_fn is not causal: exits in bars [{a}, {cut}) "
                                 f"change when bars >= {cut_} are removed (params={params})")


def check_causality(panel, strategy_fn, params, n_checks: int = 6, seed: int = 0,
                    atol: float = 1e-10) -> dict:
    """Recompute the weights on truncated copies of the panel and compare them
    with the full-panel weights on the common bars. A causal strategy gives
    identical weights; anything that peeks (full-sample normalisation, centred
    windows, shift(-1) ...) shows up as a mismatch.
    Returns {"ok": bool, "mismatches": [(cut, first_bad_bar), ...]}."""
    T = len(panel.t)
    full = np.asarray(strategy_fn(panel, params), float)
    rng = np.random.default_rng(seed)
    cuts = sorted(set(int(x) for x in rng.integers(max(2, T // 4), T, size=n_checks)))
    bad = []
    for cut in cuts:
        w = np.asarray(strategy_fn(S.slice_panel(panel, 0, cut), params), float)
        a, b = full[:cut], w
        same = (np.isclose(a, b, atol=atol, rtol=0) | (np.isnan(a) & np.isnan(b))).all(axis=1)
        if not same.all():
            bad.append((cut, int(np.flatnonzero(~same)[0])))
    return {"ok": not bad, "mismatches": bad, "cuts": cuts}
