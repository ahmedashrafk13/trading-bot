"""Shared evaluation harness for the family-E micro_* strategy modules.

evaluate(mod, ...) runs, on DEV data only (panel end 2025-06-30, wf cuts at the
lockbox anyway):
  * wf.walk_forward over mod.GRID (rolling), stitched OOS result
  * reconstruction of the OOS weights (chosen params per fold) -> null test
  * FROZEN run over the whole dev period (daily returns for correlations)
  * +/-1 grid-step sensitivity around FROZEN (dev-period, in-sample numbers)
  * $200 implementability (round_to_qty with Bybit instruments)
  * wf.check_causality on the FROZEN params
and writes results/<name>.json in the agreed contract.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data, metrics as M, nulls, sim as S, wf  # noqa: E402

DEV_END = "2025-06-30"
RESULTS = os.path.join(os.path.dirname(HERE), "results")


# --------------------------------------------------------------------------- #
# building blocks used by the modules
# --------------------------------------------------------------------------- #
def bars_per_year(panel):
    return 365.25 * 86400.0 / float(panel.dt)


def close_ret(panel):
    """Simple close-to-close return of bar i (NaN-safe: 0 where missing)."""
    c = panel.c
    r = np.zeros_like(c)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = c[1:] / c[:-1] - 1.0
    r[~np.isfinite(r)] = 0.0
    return r


def asset_vol(panel, lb):
    """Trailing annualised vol of each asset from bar returns (window incl. current)."""
    r = close_ret(panel)
    r[~panel.tradable] = np.nan
    sd = pd.DataFrame(r).rolling(lb, min_periods=max(10, lb // 2)).std().to_numpy()
    return sd * np.sqrt(bars_per_year(panel))


def vol_scale_book(panel, w_raw, target, lb=120, cap=4.0):
    """Scale a raw book so its trailing realised vol (of the UNSCALED book, held
    from close i-1 to close i) hits `target`. Scale at bar i uses returns up to
    and including bar i only (causal). Gross capped at `cap`."""
    w_raw = np.nan_to_num(np.asarray(w_raw, float))
    r = close_ret(panel)
    pr = np.zeros(len(r))
    pr[1:] = (w_raw[:-1] * r[1:]).sum(1)
    active = np.zeros(len(r), bool)
    active[1:] = np.abs(w_raw[:-1]).sum(1) > 0
    s = pd.Series(np.where(active, pr, np.nan))
    sd = s.rolling(lb, min_periods=max(20, lb // 3)).std().to_numpy() * np.sqrt(bars_per_year(panel))
    sd = pd.Series(sd).ffill().to_numpy()
    k = np.where(np.isfinite(sd) & (sd > 1e-6), target / np.maximum(sd, 1e-6), 0.0)
    w = w_raw * k[:, None]
    g = np.abs(w).sum(1)
    over = g > cap
    w[over] *= (cap / g[over])[:, None]
    return w


def band(w, width):
    """Hysteresis per symbol: keep the previous weight unless the new target
    moves by more than `width` (absolute, fraction of equity), crosses zero or
    goes flat. Sequential and causal."""
    w = np.nan_to_num(np.asarray(w, float))
    if width <= 0:
        return w
    out = np.zeros_like(w)
    prev = np.zeros(w.shape[1])
    for i in range(w.shape[0]):
        x = w[i]
        chg = (np.abs(x - prev) > width) | (x == 0) | (np.sign(x) != np.sign(prev))
        prev = np.where(chg, x, prev)
        out[i] = prev
    return out


def stagger(sig, H):
    """Average of the last H decisions' signals (overlapping-portfolio hold of H bars)."""
    sig = np.nan_to_num(np.asarray(sig, float))
    if H <= 1:
        return sig
    cs = np.cumsum(sig, axis=0)
    out = cs.copy()
    out[H:] = cs[H:] - cs[:-H]
    return out / H


def attach_metrics(panel, symbols, timeframe, start, end):
    m = data.load_metrics(symbols, timeframe, start=start, end=end)
    panel.meta["metrics"] = m
    return panel


def get_metrics(panel, metrics):
    if metrics is not None:
        return metrics
    m = panel.meta.get("metrics")
    if m is None:
        raise ValueError("this strategy needs metrics: pass metrics= or attach_metrics(panel)")
    return m


def load_for(mod, end=DEV_END):
    kw = dict(mod.PANEL)
    kw["end"] = end
    tf = kw.pop("timeframe")
    p = data.load_panel(tf, **kw)
    if getattr(mod, "USES_METRICS", False):
        attach_metrics(p, p.symbols, tf, kw.get("start"), end)
    return wf.pre_lockbox(p)


# --------------------------------------------------------------------------- #
# evaluation
# --------------------------------------------------------------------------- #
def _fmt(x, nd=4):
    try:
        if x is None:
            return None
        x = float(x)
        return round(x, nd) if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def _daily(res):
    t, eq = M.daily_equity(res.t, res.dt, res.equity, res.initial_equity)
    return t, eq


def _daily_series(res):
    d = M.daily_equity(res.t, res.dt, res.equity, res.initial_equity)
    return d


def _sel_frozen(grid, scores):
    """Stability pick: best median across folds of the within-fold rank."""
    sc = np.where(np.isfinite(scores), scores, -1e9)
    ranks = np.argsort(np.argsort(-sc, axis=1), axis=1).astype(float)
    med = np.median(ranks, axis=0)
    mean_sc = np.nanmean(np.where(np.isfinite(scores), scores, np.nan), axis=0)
    order = np.lexsort((-np.nan_to_num(mean_sc, nan=-1e9), med))
    return int(order[0]), med, mean_sc


def _neighbours(grid, k0):
    base = grid[k0]
    out = []
    keys = [k for k in base if k != "vol_target"]
    for key in keys:
        vals = sorted({g[key] for g in grid if all(g.get(o) == base.get(o) for o in base if o != key)},
                      key=lambda v: (str(type(v)), v))
        if len(vals) < 2:
            continue
        i = vals.index(base[key])
        for d in (-1, 1):
            if 0 <= i + d < len(vals):
                v = vals[i + d]
                for g in grid:
                    if g.get(key) == v and all(g.get(o) == base.get(o) for o in base if o != key):
                        out.append((key, v, g))
                        break
    return out


def _metrics_row(res):
    m = M.equity_metrics(res.t, res.dt, res.equity, res.initial_equity)
    return m


def _oos_weights(P, mod, folds):
    T, N = len(P.t), len(P.symbols)
    W = np.zeros((T, N))
    for fi in folds:
        ia, ib, ic = fi["bars"]
        sub = S.slice_panel(P, 0, ic)
        w = np.asarray(mod.weights(sub, fi["params"]), float)
        W[ib:ic] = w[ib:ic]
    return W


def _implementability(P, W, a, b, sim_kwargs, base_res):
    ins = data.load_bybit_instruments()
    sub = S.slice_panel(P, a, b)
    Ws = W[a:b]
    missing = [s for s in P.symbols if s not in ins]
    # symbols actually traded that are missing on Bybit
    traded = [P.symbols[j] for j in range(len(P.symbols)) if np.any(Ws[:, j] != 0)]
    traded_missing = [s for s in traded if s not in ins]
    res = S.run_weights(sub, Ws, instruments=ins, round_to_qty=True, **(sim_kwargs or {}))
    m = res.metrics()
    # estimated share of order CHANGES too small for Bybit minimums
    eq = base_res.equity
    dW = np.abs(np.diff(np.vstack([np.zeros((1, Ws.shape[1])), Ws]), axis=0))
    minnot = np.array([float(ins.get(s, {}).get("minNotionalValue") or 5.0) for s in P.symbols])
    minq = np.array([float(ins.get(s, {}).get("minOrderQty") or 0.0) for s in P.symbols])
    px = np.nan_to_num(sub.c)
    need = np.maximum(minnot[None, :], minq[None, :] * px)
    notional = dW * eq[:, None]
    chg = (dW > 1e-12) & (np.abs(Ws) > 0)        # opening/resizing orders (closes always allowed)
    small = chg & (notional < need)
    return {"metrics": {k: _fmt(m.get(k)) for k in ("cagr", "sharpe", "max_drawdown", "total_return",
                                                  "final_equity", "n_trades", "fee_drag_per_year",
                                                  "funding_per_year", "exposure")},
            "dropped_order_share_est": _fmt(small.sum() / max(chg.sum(), 1)),
            "n_order_changes": int(chg.sum()),
            "bybit_missing_symbols_in_panel": missing[:50],
            "bybit_missing_symbols_traded": traded_missing,
            "note": "round_to_qty=True with load_bybit_instruments() on the stitched OOS weights; "
                    "dropped share is an estimate (orders whose |delta notional| < max(minNotionalValue, "
                    "minOrderQty*price) at the unrounded equity)."}


def evaluate(mod, *, train_days=730, test_days=182, step_days=182, sim_kwargs=None,
             null_n=200, null_kind="sign_flip", null_secondary_on=True, extra=None, family_trials=None,
             verdict_fn=None, write=True, panel=None):
    t0 = time.time()
    P = panel if panel is not None else load_for(mod)
    kw = dict(sim_kwargs or {})
    fn = lambda p, prm: mod.weights(p, prm)        # noqa: E731  (metrics via panel.meta)
    res = wf.walk_forward(P, fn, mod.GRID, train_days=train_days, test_days=test_days,
                          step_days=step_days, objective="sharpe", mode="rolling",
                          kind="weights", sim_kwargs=kw, causality_checks=2)
    oos = res["oos_result"]
    om = res["oos_metrics"]
    folds = res["folds"]
    a, b = folds[0]["bars"][1], folds[-1]["bars"][2]
    # --- OOS weights + null
    W = _oos_weights(P, mod, folds)
    sub = S.slice_panel(P, a, b)
    chk = S.run_weights(sub, W[a:b], **kw)
    chk_sh = M.fast_sharpe(chk)
    def _null(kind, n):
        if kind == "sign_flip":
            nl = nulls.sign_flip_null(sub, W[a:b], n=n, seed=0, sim_kwargs=kw)
        else:
            nl = nulls.random_timing_null(sub, W[a:b], n=n, seed=0, sim_kwargs=kw)
        return {"kind": f"{kind} ({nl['method']}) on stitched OOS weights", "n": n,
                "strategy_sharpe": _fmt(nl["strategy"]), "null_p95": _fmt(np.percentile(nl["null"], 95)),
                "null_median": _fmt(np.median(nl["null"])),
                "percentile": _fmt(nl["percentile"], 2), "p_value": _fmt(nl["p_value"]),
                "strategy_turnover": _fmt(nl["strategy_turnover"], 1),
                "null_turnover_mean": _fmt(nl["null_turnover_mean"], 1)}
    null = _null(null_kind, null_n)
    other = "random_timing" if null_kind == "sign_flip" else "sign_flip"
    null_secondary = _null(other, max(50, null_n // 2)) if null_secondary_on else None
    # --- FROZEN
    k0, med_rank, mean_sc = _sel_frozen(mod.GRID, res["scores"])
    frozen = mod.GRID[k0]
    wfro = np.asarray(mod.weights(P, frozen), float)
    rfro = S.run_weights(P, wfro, **kw)
    dfro = M.daily_equity(rfro.t, rfro.dt, rfro.equity, rfro.initial_equity)
    fm = rfro.metrics()
    # --- sensitivity
    sens = []
    for key, v, g in _neighbours(mod.GRID, k0):
        rr = S.run_weights(P, np.asarray(mod.weights(P, g), float), **kw)
        mm = M.equity_metrics(rr.t, rr.dt, rr.equity, rr.initial_equity)
        sens.append({"param": key, "value": v, "oos_or_dev_sharpe": _fmt(mm["sharpe"], 3),
                     "cagr": _fmt(mm["cagr"]), "maxdd": _fmt(mm["max_drawdown"]), "basis": "dev (in-sample)"})
    sens.append({"param": "FROZEN", "value": json.dumps(frozen), "oos_or_dev_sharpe": _fmt(fm["sharpe"], 3),
                 "cagr": _fmt(fm["cagr"]), "maxdd": _fmt(fm["max_drawdown"]), "basis": "dev (in-sample)"})
    # --- causality
    caus = wf.check_causality(P, fn, frozen, n_checks=6, seed=0)
    caus = {"ok": bool(caus["ok"]), "mismatches": caus["mismatches"], "cuts": caus["cuts"],
            "plus_walk_forward_guard": "passed (walk_forward causality_checks=2 per fold raised nothing)"}
    # --- implementability
    impl = _implementability(P, W, a, b, kw, chk)
    # --- trade stats from OOS
    tr = oos.trades.df()
    closed = tr[~tr["is_open"]] if len(tr) else tr
    if len(closed):
        wins = closed[closed["pnl"] > 0]["ret"]
        losses = closed[closed["pnl"] <= 0]["ret"]
        payoff = float(wins.mean() / abs(losses.mean())) if len(wins) and len(losses) and losses.mean() != 0 else None
        expct = float(closed["pnl"].mean())
        worst = float(closed["ret"].min())
    else:
        payoff = expct = worst = None
    years = om.get("years") or ((b - a) * P.dt / (365.25 * 86400))
    # by-year OOS
    dser = M.daily_equity(oos.t, oos.dt, oos.equity, oos.initial_equity)
    oos_dates, oos_eq = _to_dates(dser)
    by_year = {}
    s_eq = pd.Series(oos_eq[1:], index=pd.to_datetime(oos_dates[1:]))
    prev = 200.0
    for y, g in s_eq.groupby(s_eq.index.year):
        rets = g.pct_change().dropna()
        first_ret = g.iloc[0] / prev - 1
        rr = np.r_[first_ret, rets.to_numpy()]
        by_year[int(y)] = {"return": _fmt(g.iloc[-1] / prev - 1),
                           "sharpe": _fmt(rr.mean() / rr.std(ddof=1) * np.sqrt(365) if rr.std(ddof=1) > 0 else np.nan, 3),
                           "maxdd": _fmt(float((g / g.cummax() - 1).min()))}
        prev = float(g.iloc[-1])
    fd_dates, fd_eq = _to_dates(dfro)
    fd_dates = fd_dates[1:]
    fd_ret = (fd_eq[1:] / fd_eq[:-1] - 1).tolist()
    nd = len(oos_eq)
    fam = family_trials or len(mod.GRID)
    dsr_family = M.deflated_sharpe(om["sharpe"], fam, max(nd, 2), om["skew"], om["kurtosis"])
    out = {
        "name": mod.NAME, "description": mod.DESCRIPTION, "mechanism": mod.MECHANISM,
        "universe": mod.PANEL.get("universe") or mod.PANEL.get("symbols"),
        "timeframe": mod.PANEL["timeframe"], "panel": dict(mod.PANEL, end=DEV_END),
        "uses_metrics": bool(getattr(mod, "USES_METRICS", False)),
        "n_trials": len(mod.GRID), "family_trials_incl_screen": fam,
        "grid_summary": {"n": len(mod.GRID), "params": sorted({k for g in mod.GRID for k in g}),
                         "values": {k: sorted({json.dumps(g[k]) for g in mod.GRID if k in g}) for k in mod.GRID[0]},
                         "median_fold_rank": [float(x) for x in med_rank],
                         "mean_train_sharpe": [_fmt(x, 3) for x in mean_sc],
                         "objective": "sharpe (lab score, dd_limit -0.30)"},
        "frozen": frozen, "frozen_rule": "config with the best MEDIAN within-fold train rank across walk-forward folds (tie: mean train Sharpe)",
        "wf": {"train_days": train_days, "test_days": test_days, "step_days": step_days, "mode": "rolling",
               "folds": [{"train": [f["train_start"], f["test_start"]], "test": [f["test_start"], f["test_end"]],
                          "chosen": f["params"], "train_score": _fmt(f["train_score"], 3),
                          "test_metrics": {k: _fmt(f["test_metrics"].get(k)) for k in ("sharpe", "cagr", "max_drawdown", "total_return")}}
                         for f in folds],
               "oos_metrics": {k: _fmt(v) for k, v in om.items() if isinstance(v, (int, float, np.floating, np.integer))},
               "oos_by_year": by_year,
               "oos_sharpe_recheck_from_reconstructed_weights": _fmt(chk_sh, 4)},
        "oos_daily": {"dates": oos_dates, "equity": [round(float(x), 4) for x in oos_eq]},
        "frozen_dev_daily": {"dates": fd_dates, "returns": [round(float(x), 6) for x in fd_ret]},
        "frozen_dev_metrics": {k: _fmt(fm.get(k)) for k in ("sharpe", "cagr", "max_drawdown", "n_trades", "win_rate",
                                                            "trades_per_week", "avg_hold_hours", "exposure",
                                                            "fee_drag_per_year", "funding_per_year")},
        "null": null,
        "null_secondary": null_secondary,
        "deflated_sharpe": _fmt(om.get("dsr")),
        "deflated_sharpe_family": _fmt(dsr_family),
        "sensitivity": sens,
        "implementability_200": impl,
        "trades_per_day": _fmt((om.get("trades_per_week") or 0) / 7.0, 3),
        "avg_hold_hours": _fmt(om.get("avg_hold_hours"), 1),
        "win_rate": _fmt(om.get("win_rate")),
        "payoff": _fmt(payoff, 3),
        "expectancy_per_trade": _fmt(expct, 4),
        "expectancy_units": "USD per closed round trip on the $200 OOS account",
        "worst_trade": _fmt(worst),
        "exposure": _fmt(om.get("exposure")),
        "fee_drag_per_year": _fmt(om.get("fee_drag_per_year")),
        "funding_per_year": _fmt(om.get("funding_per_year")),
        "needs_hourly_runs": bool(getattr(mod, "NEEDS_HOURLY_RUNS", False)),
        "causality": caus,
        "sim_kwargs": {k: v for k, v in kw.items()},
        "runtime_s": round(time.time() - t0, 1),
    }
    if extra:
        out.update(extra)
    v, cav = verdict_fn(out) if verdict_fn else default_verdict(out)
    out["verdict"] = v
    out["caveats"] = list(getattr(mod, "CAVEATS", [])) + cav
    if write:
        with open(os.path.join(RESULTS, f"{mod.NAME}.json"), "w") as f:
            json.dump(out, f, indent=1, default=_json_default)
    return out


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


def _to_dates(d):
    """metrics.daily_equity output (day keys [n], equity [n+1] incl. the initial
    value) -> (dates [n+1] with the day before the first key for the initial
    value, equity [n+1])."""
    keys, e = d
    keys = np.asarray(keys, np.int64)
    keys = np.r_[keys[0] - 1, keys]
    dates = [pd.Timestamp(int(k) * 86400, unit="s").strftime("%Y-%m-%d") for k in keys]
    return dates, np.asarray(e, float)


def default_verdict(o):
    """Family-E verdict rule (applied identically to every module):
      p_used = the LARGER p-value of the two nulls, ignoring a random-timing 'runs' null whose
               mean turnover is > 1.5x the strategy's (the shuffled continuous weights then pay
               far more costs, which biases that null DOWN - see lab_bugs_found).
      promising: OOS Sharpe >= 0.8, p_used <= 0.05, deflated Sharpe (grid trials) >= 0.9 and
                 >= 60% of OOS calendar years positive.
      marginal : OOS Sharpe >= 0.5 and p_used <= 0.10.
      fails    : otherwise.
      Fragility downgrade (one level): any +/-1 grid-step neighbour of FROZEN with a negative
      dev Sharpe, or a dev Sharpe below 0.25 when fees are doubled (robustness_dev_frozen)."""
    om = o["wf"]["oos_metrics"]
    sh = om.get("sharpe") or 0.0
    ps, notes = [], []
    for key in ("null", "null_secondary"):
        nl = o.get(key)
        if not nl or nl.get("p_value") is None:
            continue
        st, nt = nl.get("strategy_turnover") or 0.0, nl.get("null_turnover_mean") or 0.0
        if "runs" in nl.get("kind", "") and st > 0 and nt > 1.5 * st:
            notes.append(f"{key} ignored for the verdict: runs-null turnover {nt:.0f} vs strategy {st:.0f}")
            continue
        ps.append(nl["p_value"])
    p = max(ps) if ps else 1.0
    dsr = o.get("deflated_sharpe") or 0.0
    yrs = [v.get("return") for v in o["wf"].get("oos_by_year", {}).values() if v.get("return") is not None]
    pos = (sum(1 for x in yrs if x > 0) / len(yrs)) if yrs else 0.0
    o["verdict_inputs"] = {"oos_sharpe": sh, "p_used": p, "deflated_sharpe": dsr, "share_years_positive": round(pos, 3),
                           "notes": notes}
    cav = []
    if sh > 2:
        cav.append("OOS Sharpe > 2: presumed bug until hunted")
    if sh >= 0.8 and p <= 0.05 and dsr >= 0.9 and pos >= 0.6:
        v = "promising"
    elif sh >= 0.5 and p <= 0.10:
        v = "marginal"
    else:
        v = "fails"
    nb = [x.get("oos_or_dev_sharpe") for x in o.get("sensitivity", []) if x.get("param") != "FROZEN"]
    neg_nb = any(x is not None and x < 0 for x in nb)
    rob = (o.get("robustness_dev_frozen") or {}).get("double_fee_dev", {}).get("sharpe")
    fee_frag = rob is not None and rob < 0.25
    if neg_nb or fee_frag:
        why = []
        if neg_nb:
            why.append("a +/-1-step neighbour has negative dev Sharpe")
        if fee_frag:
            why.append(f"dev Sharpe with 2x fees is {rob:.2f}")
        o["verdict_inputs"]["fragility_downgrade"] = "; ".join(why)
        v = {"promising": "marginal", "marginal": "fails", "fails": "fails"}[v]
        cav.append("Verdict downgraded for fragility: " + "; ".join(why))
    return v, cav


# --------------------------------------------------------------------------- #
# cross-sectional helpers
# --------------------------------------------------------------------------- #
def cs_rank(A, min_n=5):
    """Centred cross-sectional pct rank per row; NaN kept; rows with < min_n names -> NaN."""
    df = pd.DataFrame(A)
    r = df.rank(axis=1, pct=True)
    r = r.sub(r.mean(axis=1), axis=0)
    r[df.notna().sum(1) < min_n] = np.nan
    return r.to_numpy()


def cs_resid(y, Xs, min_n=6):
    """Per-row OLS residual of y on a constant + Xs (all [T,N]); NaN where missing."""
    T, N = y.shape
    out = np.full((T, N), np.nan)
    for i in range(T):
        Xi = np.column_stack([x[i] for x in Xs])
        ok = np.isfinite(y[i]) & np.isfinite(Xi).all(1)
        if ok.sum() < max(min_n, len(Xs) + 3):
            continue
        A = np.column_stack([np.ones(ok.sum()), Xi[ok]])
        b, *_ = np.linalg.lstsq(A, y[i, ok], rcond=None)
        out[i, ok] = y[i, ok] - A @ b
    return out


def xs_longshort(score, q, min_n=6, n_min_side=1):
    """Long the top q fraction, short the bottom q fraction of score per row,
    equal weight, +0.5 / -0.5 gross per side (dollar neutral). NaN -> excluded."""
    T, N = score.shape
    w = np.zeros((T, N))
    for i in range(T):
        ok = np.flatnonzero(np.isfinite(score[i]))
        if ok.size < min_n:
            continue
        k = max(n_min_side, int(np.floor(q * ok.size)))
        o = ok[np.argsort(score[i, ok], kind="stable")]
        w[i, o[-k:]] += 0.5 / k
        w[i, o[:k]] -= 0.5 / k
    return w


def roll_resid_multi(y, Xs, n, minp):
    """Per-column trailing rolling OLS residual of y on constant + 2 regressors
    (window n incl. current), divided by the window residual std. Causal."""
    x1, x2 = Xs
    bad = ~(np.isfinite(y) & np.isfinite(x1) & np.isfinite(x2))
    Y, A, B = (np.where(bad, np.nan, v) for v in (y, x1, x2))
    r = lambda v: pd.DataFrame(v).rolling(n, min_periods=minp).mean().to_numpy()   # noqa: E731
    my, ma, mb = r(Y), r(A), r(B)
    caa = r(A * A) - ma * ma
    cbb = r(B * B) - mb * mb
    cab = r(A * B) - ma * mb
    cay = r(A * Y) - ma * my
    cby = r(B * Y) - mb * my
    cyy = r(Y * Y) - my * my
    det = caa * cbb - cab * cab
    with np.errstate(invalid="ignore", divide="ignore"):
        ba = (cay * cbb - cby * cab) / det
        bb = (cby * caa - cay * cab) / det
        e = (Y - my) - ba * (A - ma) - bb * (B - mb)
        rv = cyy - ba * cay - bb * cby
        z = e / np.sqrt(np.where(rv > 1e-18, rv, np.nan))
    z[~np.isfinite(det) | (np.abs(det) < 1e-24)] = np.nan
    return z
