"""Evaluation runner for ml_ranker (family H). Writes results/ml_ranker.json (headline = lgbm family)
and results/_ml_ranker_families.json (ridge / ew / full-12 comparison). DEV data only (end 2025-06-30).
"""
from __future__ import annotations

import json
import os
import sys
import time
import types

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import metrics as M, sim as S, wf  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import ml_ranker as MR  # noqa: E402

RES = HX.RESULTS
N_TRIALS_TOTAL = len(MR.GRID) + 2       # 12 grid configs + 2 pre-registered robustness variants
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


_orig_wf = wf.walk_forward


def _wf(*a, **k):
    k.setdefault("start", MR.WF_START)
    return _orig_wf(*a, **k)


wf.walk_forward = _wf          # runtime patch in this process only: first train window 2021-01-01


def shim(name, grid):
    return types.SimpleNamespace(NAME=name, DESCRIPTION=MR.DESCRIPTION, MECHANISM=MR.MECHANISM, PANEL=MR.PANEL,
                                 USES_METRICS=True, KIND="weights", NEEDS_HOURLY_RUNS=False, GRID=grid,
                                 weights=MR.weights, CAVEATS=list(MR.CAVEATS))


def ts(s):
    return int(pd.Timestamp(s, tz="UTC").value // 10**9)


def oos_bars(P, out):
    fl = []
    for f in out["wf"]["folds"]:
        ib = int(np.searchsorted(P.t, ts(f["test"][0])))
        ic = int(np.searchsorted(P.t, ts(f["test"][1])))
        fl.append({"bars": (0, ib, ic), "params": f["chosen"]})
    return fl


def mrow(res):
    m = res.metrics()
    return {k: HX._fmt(m.get(k)) for k in ("sharpe", "cagr", "max_drawdown", "total_return", "turnover_per_year",
                                          "fee_drag_per_year", "funding_per_year", "exposure", "win_rate",
                                          "trades_per_week", "avg_hold_hours")}


def daily_ret(res):
    return M.daily_returns(res.t, res.dt, res.equity, res.initial_equity)


def by_year_ret(res):
    keys, eq = M.daily_equity(res.t, res.dt, res.equity, res.initial_equity)
    s = pd.Series(np.asarray(eq[1:]), index=pd.to_datetime(np.asarray(keys, np.int64) * 86400, unit="s"))
    prev, out = float(eq[0]), {}
    for y, g in s.groupby(s.index.year):
        out[int(y)] = HX._fmt(g.iloc[-1] / prev - 1)
        prev = float(g.iloc[-1])
    return out


# --------------------------------------------------------------------------- #
def stop_overlay(P, W, a, b, stop, kw):
    """Approximate per-name protective stop re-armed at each daily run at `stop` from the run (open)
    price. Stop-out: fill at the level with fee + 3x tier slippage; flat for the rest of the bar;
    re-enter at the next open if the book still holds the name (extra round trip). Applied as a
    return adjustment to the simulated equity path."""
    sub = S.slice_panel(P, a, b)
    res = S.run_weights(sub, W[a:b], record_positions=True, **kw)
    q = res.positions
    o, h, l, c = sub.o, sub.h, sub.l, sub.c
    fee = kw.get("fee", 0.00055)
    slip = S.default_slippage_bps(sub.symbols) / 1e4
    eq = res.equity
    T = len(eq)
    adj = np.zeros(T)
    n_stops = 0
    for i in range(1, T):
        qi = q[i]
        held = qi != 0
        if not held.any():
            continue
        oi = np.nan_to_num(o[i])
        lo, hi, ci = np.nan_to_num(l[i]), np.nan_to_num(h[i]), np.nan_to_num(c[i])
        lvl_l = oi * (1 - stop)
        lvl_s = oi * (1 + stop)
        hitL = held & (qi > 0) & (lo <= lvl_l) & (oi > 0)
        hitS = held & (qi < 0) & (hi >= lvl_s) & (oi > 0)
        hit = hitL | hitS
        if not hit.any():
            continue
        n_stops += int(hit.sum())
        lvl = np.where(hitL, lvl_l, lvl_s)
        qn = q[i + 1] if i + 1 < T else np.zeros_like(qi)
        on = np.nan_to_num(o[i + 1]) if i + 1 < T else ci
        d = 0.0
        for j in np.flatnonzero(hit):
            # stop path minus sim path over open i -> next open (see docstring)
            d += (qi[j] * (lvl[j] - on[j]) - abs(qi[j]) * lvl[j] * (fee + 3 * slip[j])
                  - (abs(qn[j]) - abs(qn[j] - qi[j])) * on[j] * (fee + slip[j]))
        base = eq[i - 1] if eq[i - 1] > 0 else res.initial_equity
        adj[i] = d / base
    r_sim = np.r_[eq[0] / res.initial_equity - 1, eq[1:] / eq[:-1] - 1]
    eq2 = res.initial_equity * np.cumprod(1 + r_sim + adj)
    m = M.equity_metrics(res.t, res.dt, eq2, res.initial_equity)
    return {"stop": stop, "sharpe": HX._fmt(m["sharpe"]), "cagr": HX._fmt(m["cagr"]),
            "max_drawdown": HX._fmt(m["max_drawdown"]), "n_stop_outs": n_stops,
            "stop_outs_per_year": HX._fmt(n_stops / max((b - a) / 365.25, 1e-9), 1)}


def ic_by_year(P, params, a):
    pred = MR.predictions(P, params)
    _, raw = MR.label(P, int(params["H"]))
    rp = HX.cs_rank(pred, min_n=MR.MIN_NAMES)
    ry = HX.cs_rank(np.where(np.isfinite(pred), raw, np.nan), min_n=MR.MIN_NAMES)
    T = len(P.t)
    ic = np.full(T, np.nan)
    for i in range(T):
        k = np.isfinite(rp[i]) & np.isfinite(ry[i])
        if k.sum() >= MR.MIN_NAMES:
            x, y = rp[i, k], ry[i, k]
            if x.std() > 0 and y.std() > 0:
                ic[i] = np.corrcoef(x, y)[0, 1]
    yr = pd.to_datetime(P.t, unit="s").year
    out = {}
    from lab.strategies import _micro_stats as ST
    for y in sorted(set(yr[np.isfinite(ic)])):
        sel = (yr == y) & np.isfinite(ic)
        m_, t_, n_ = ST.mean_nw_t(ic[sel], max(1, int(params["H"])))
        out[int(y)] = {"ic": HX._fmt(m_), "t_nw": HX._fmt(t_, 2), "n_days": n_}
    sel = np.isfinite(ic) & (np.arange(T) >= a)
    m_, t_, n_ = ST.mean_nw_t(ic[sel], max(1, int(params["H"])))
    out["oos_window"] = {"ic": HX._fmt(m_), "t_nw": HX._fmt(t_, 2), "n_days": n_}
    return out, ic


def importance_stability(model, H):
    rows = {k[-1]: v for k, v in MR._IMPORTANCE.items() if k[0] == model and k[1] == H and k[2] == "rank"
            and k[3] == "rolling"}
    if not rows:
        return None
    dates = sorted(rows)
    feats = [f for f in rows[dates[0]] if f != "const"]
    A = np.array([[rows[d].get(f, np.nan) for f in feats] for d in dates])
    out = {"n_fits": len(dates), "fit_dates": [pd.Timestamp(d, unit="s").strftime("%Y-%m-%d") for d in dates]}
    if model == "lgbm":
        rk = pd.DataFrame(A.T).rank().to_numpy()
        C = np.corrcoef(rk.T)
        iu = np.triu_indices(len(dates), 1)
        adj = [float(C[i, i + 1]) for i in range(len(dates) - 1)]
        mean = A.mean(0)
        order = np.argsort(-mean)
        out.update({"mean_gain_share": {feats[i]: round(float(mean[i]), 4) for i in order},
                    "gain_share_std": {feats[i]: round(float(A[:, i].std()), 4) for i in order},
                    "top5_per_fit": {out["fit_dates"][n]: [feats[i] for i in np.argsort(-A[n])[:5]] for n in range(len(dates))},
                    "mean_pairwise_spearman_of_importance": round(float(np.nanmean(C[iu])), 3),
                    "mean_adjacent_fit_spearman": round(float(np.nanmean(adj)), 3)})
    else:
        sg = np.sign(A)
        maj = np.sign(np.nansum(sg, 0))
        out.update({"mean_coef": {f: round(float(A[:, i].mean()), 4) for i, f in enumerate(feats)},
                    "sign_agreement_share": {f: round(float((sg[:, i] == maj[i]).mean()), 2) for i, f in enumerate(feats)},
                    "prereg_sign_vs_mean_coef": {f: int(np.sign(A[:, i].mean()) == MR.SIGNS[f]) for i, f in enumerate(feats)
                                                 if f in MR.SIGNS}})
    return out


def main():
    log("loading")
    P = MR.load()
    fam = {m: [g for g in MR.GRID if g["model"] == m] for m in ("lgbm", "ridge", "ew")}
    outs, Ws = {}, {}
    for m in ("lgbm", "ew", "ridge"):
        log("evaluate family", m)
        o = HX.evaluate(shim(f"ml_ranker_{m}" if m != "lgbm" else "ml_ranker", fam[m]), train_days=MR.OUTER_TRAIN_DAYS,
                        test_days=182, step_days=182, null_n=200 if m == "lgbm" else 100,
                        family_trials=N_TRIALS_TOTAL, write=False, panel=P)
        outs[m] = o
        fl = oos_bars(P, o)
        Ws[m] = HX._oos_weights(P, shim("x", fam[m]), fl)
        log(m, "OOS", o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"),
            o["wf"]["oos_metrics"].get("max_drawdown"), "frozen", o["frozen"], "verdict", o["verdict"])
    main_o = outs["lgbm"]
    fl = oos_bars(P, main_o)
    a, b = fl[0]["bars"][1], fl[-1]["bars"][2]
    kw = {}
    sub = S.slice_panel(P, a, b)
    # ---- costs
    cost = {}
    for m in ("lgbm", "ridge", "ew"):
        cost[m] = {"base": mrow(S.run_weights(sub, Ws[m][a:b])),
                   "double_fee": mrow(S.run_weights(sub, Ws[m][a:b], fee=0.0011)),
                   "double_fee_and_slippage": mrow(S.run_weights(sub, Ws[m][a:b], fee=0.0011,
                                                                 slippage_bps=2 * S.default_slippage_bps(sub.symbols))),
                   "gross_no_costs": mrow(S.run_weights(sub, Ws[m][a:b], fee=0.0, slippage_bps=0.0)),
                   "no_funding": mrow(S.run_weights(sub, Ws[m][a:b], funding=False))}
    log("costs done")
    # ---- frozen dev robustness (for the verdict rule)
    fz = main_o["frozen"]
    wfz = MR.weights(P, fz)
    rob = {"double_fee_dev": mrow(S.run_weights(P, wfz, fee=0.0011)),
           "base_dev": mrow(S.run_weights(P, wfz))}
    main_o["robustness_dev_frozen"] = rob
    # ---- ML vs baseline, paired
    rL = daily_ret(S.run_weights(sub, Ws["lgbm"][a:b]))
    rE = daily_ret(S.run_weights(sub, Ws["ew"][a:b]))
    rR = daily_ret(S.run_weights(sub, Ws["ridge"][a:b]))
    n = min(len(rL), len(rE), len(rR))
    from lab.strategies import _micro_stats as ST
    dm, dt_, _ = ST.mean_nw_t(rL[:n] - rE[:n], 5)
    dmR, dtR, _ = ST.mean_nw_t(rR[:n] - rE[:n], 5)
    comp = {"oos_sharpe": {m: outs[m]["wf"]["oos_metrics"].get("sharpe") for m in outs},
            "oos_cagr": {m: outs[m]["wf"]["oos_metrics"].get("cagr") for m in outs},
            "oos_maxdd": {m: outs[m]["wf"]["oos_metrics"].get("max_drawdown") for m in outs},
            "oos_by_year": {m: outs[m]["wf"]["oos_by_year"] for m in outs},
            "daily_corr": {"lgbm_ew": HX._fmt(np.corrcoef(rL[:n], rE[:n])[0, 1], 3),
                           "lgbm_ridge": HX._fmt(np.corrcoef(rL[:n], rR[:n])[0, 1], 3),
                           "ridge_ew": HX._fmt(np.corrcoef(rR[:n], rE[:n])[0, 1], 3)},
            "lgbm_minus_ew_daily_mean_ann": HX._fmt(dm * 365), "lgbm_minus_ew_nw_t": HX._fmt(dt_, 2),
            "ridge_minus_ew_daily_mean_ann": HX._fmt(dmR * 365), "ridge_minus_ew_nw_t": HX._fmt(dtR, 2),
            "frozen_by_family": {m: outs[m]["frozen"] for m in outs},
            "verdict_by_family": {m: outs[m]["verdict"] for m in outs}}
    # fixed-config (no outer selection) OOS-window runs for all 12 configs
    fixed = []
    for g in MR.GRID:
        w = MR.weights(P, g)
        r = S.run_weights(sub, w[a:b])
        fixed.append(dict(g, **{k: v for k, v in mrow(r).items() if k in ("sharpe", "cagr", "max_drawdown", "turnover_per_year")}))
    comp["fixed_config_oos_window"] = fixed
    log("comparison done")
    # ---- full 12-config selection
    fn = lambda p, prm: MR.weights(p, prm)   # noqa: E731
    full = wf.walk_forward(P, fn, MR.GRID, train_days=MR.OUTER_TRAIN_DAYS, test_days=182, step_days=182,
                           objective="sharpe", mode="rolling", kind="weights", causality_checks=1)
    comp["full12_selection"] = {"oos_metrics": {k: HX._fmt(full["oos_metrics"].get(k)) for k in
                                                ("sharpe", "cagr", "max_drawdown", "dsr")},
                                "chosen": [f["params"] for f in full["folds"]]}
    log("full12 done", comp["full12_selection"]["oos_metrics"])
    # ---- IC by year
    ics, icser = {}, {}
    for m in ("lgbm", "ridge", "ew"):
        for H in (1, 3):
            ics[f"{m}_H{H}"], icser[(m, H)] = ic_by_year(P, dict(model=m, H=H), a)
    log("ic done")
    # ---- importance stability
    imp = {"lgbm_H1": importance_stability("lgbm", 1), "lgbm_H3": importance_stability("lgbm", 3),
           "ridge_H1": importance_stability("ridge", 1), "ridge_H3": importance_stability("ridge", 3)}
    # ---- stops on the headline OOS book
    stops = [stop_overlay(P, Ws["lgbm"], a, b, s, kw) for s in (0.10, 0.15, 0.25)]
    stops.insert(0, {"stop": None, **{k: v for k, v in cost["lgbm"]["base"].items() if k in ("sharpe", "cagr", "max_drawdown")}})
    log("stops done")
    # ---- pre-registered robustness variants on the frozen lgbm config (fixed params, OOS window)
    var = {}
    for name, extra in (("frozen_rolling", {}), ("expanding_window", {"window": "expanding"}),
                        ("signcost_target", {"target": "signcost"})):
        w = MR.weights(P, dict(fz, **extra))
        var[name] = mrow(S.run_weights(sub, w[a:b]))
        var[name]["by_year"] = by_year_ret(S.run_weights(sub, w[a:b]))
    log("variants done")
    # ---- correlations (frozen dev daily returns, common window)
    fd = main_o["frozen_dev_daily"]
    s_me = pd.Series(fd["returns"], index=pd.to_datetime(fd["dates"]))
    s_me = s_me[s_me.index >= pd.Timestamp("2021-01-01")]
    corr = {}
    for other in ("micro_crowd", "micro_flowxs"):
        oj = json.load(open(os.path.join(RES, other + ".json")))
        so = pd.Series(oj["frozen_dev_daily"]["returns"], index=pd.to_datetime(oj["frozen_dev_daily"]["dates"]))
        so = so.groupby(so.index.normalize()).apply(lambda x: float(np.prod(1 + x) - 1))
        jj = pd.concat([s_me, so], axis=1, join="inner").dropna()
        corr[other] = HX._fmt(jj.corr().iloc[0, 1], 3)
        corr[other + "_n_days"] = int(len(jj))
    jb = P.symbols.index("BTCUSDT")
    btc = pd.Series(P.c[:, jb], index=pd.to_datetime(P.t + P.dt, unit="s") - pd.Timedelta(days=1)).pct_change()
    btc.index = btc.index.normalize()
    jj = pd.concat([s_me, btc], axis=1, join="inner").dropna()
    corr["btc"] = HX._fmt(jj.corr().iloc[0, 1], 3)
    # OOS-window correlation of stitched books too
    main_o["correlation_to"] = corr
    # ---- assemble
    om = main_o["wf"]["oos_metrics"]
    rd = daily_ret(main_o_res := S.run_weights(sub, Ws["lgbm"][a:b]))   # noqa: F841
    main_o["n_trials"] = len(MR.GRID)
    main_o["n_trials_total_incl_variants"] = N_TRIALS_TOTAL
    main_o["deflated_sharpe_4_family_only"] = main_o["deflated_sharpe"]
    main_o["deflated_sharpe"] = HX._fmt(M.deflated_sharpe(om["sharpe"], N_TRIALS_TOTAL, max(len(rd), 2),
                                                          om["skew"], om["kurtosis"]))
    main_o["grid_full"] = MR.GRID
    main_o["headline"] = "lgbm family (4 configs) walk-forward; trials counted over all 12 grid configs + 2 variants"
    main_o["comparison"] = comp
    main_o["cost_sensitivity_oos"] = cost
    main_o["oos_ic_by_year"] = ics
    main_o["feature_importance_stability"] = imp
    main_o["protective_stops"] = stops
    main_o["robustness_variants_frozen_oos_window"] = var
    main_o["live_retrain_cadence"] = ("model refit on the latest absolute 91-day grid close (anchor 2020-01-01) "
                                     "on the trailing 730d, embargo 2H; one refit per quarter; decisions daily "
                                     "at the 00:07 UTC run; no saved model")
    main_o["lightgbm"] = "installed with python -m pip install --user lightgbm (4.7.0); native lgb.train API (no scikit-learn)"
    main_o["oos_2025h1_return"] = main_o["wf"]["oos_by_year"].get(2025, {}).get("return")
    v, cav = HX.default_verdict(main_o)
    lg, ew = comp["oos_sharpe"]["lgbm"] or -9, comp["oos_sharpe"]["ew"] or -9
    if lg <= ew:
        v = {"promising": "marginal", "marginal": "fails", "fails": "fails"}[v]
        cav.append(f"Downgraded: lgbm OOS Sharpe {lg:.2f} does not beat the no-fit ew baseline {ew:.2f}")
    main_o["verdict"] = v
    main_o["caveats"] = list(MR.CAVEATS) + cav
    with open(os.path.join(RES, "ml_ranker.json"), "w") as f:
        json.dump(main_o, f, indent=1, default=HX._json_default)
    fam_out = {m: {k: outs[m][k] for k in ("frozen", "wf", "null", "null_secondary", "deflated_sharpe", "sensitivity",
                                           "trades_per_day", "fee_drag_per_year", "funding_per_year", "verdict",
                                           "causality")} for m in ("ridge", "ew")}
    fam_out["full12_selection"] = comp["full12_selection"]
    with open(os.path.join(RES, "_ml_ranker_families.json"), "w") as f:
        json.dump(fam_out, f, indent=1, default=HX._json_default)
    log("DONE", v, om.get("sharpe"), om.get("cagr"), om.get("max_drawdown"))


if __name__ == "__main__":
    main()
