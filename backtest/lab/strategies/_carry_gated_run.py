"""Research run for strategies/carry_gated.py -> results/carry_gated.json.

    cd backtest && python -m lab.strategies._carry_gated_run

Dev period only (panel end 2025-06-30; the lockbox is never loaded).
"""
from __future__ import annotations

import dataclasses
import json
import math
import os
import sys
import time
from collections import Counter

import numpy as np
import pandas as pd

from lab import metrics as M
from lab import sim as S
from lab import wf as WF
from lab import data as D
from lab.strategies import carry_gated as C

END = "2025-06-30"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results",
                   "carry_gated.json")
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)


def jsafe(o):
    if isinstance(o, dict):
        return {str(k): jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsafe(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if math.isfinite(v) else None
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


KEYS = ("cagr", "sharpe", "sortino", "max_drawdown", "calmar", "vol_annual", "total_return",
        "final_equity", "n_trades", "win_rate", "profit_factor", "avg_hold_hours",
        "trades_per_week", "exposure", "turnover_per_year", "fee_drag_per_year",
        "funding_per_year", "n_liquidations", "n_delistings", "skew", "kurtosis", "psr",
        "pct_positive_months", "worst_month", "best_month", "start", "end", "years")


def pick(m):
    return {k: m.get(k) for k in KEYS if k in m}


def daily(res, initial=None):
    ini = res.initial_equity if initial is None else initial
    keys, eq = M.daily_equity(res.t, res.dt, res.equity, ini)
    dates = [time.strftime("%Y-%m-%d", time.gmtime(int(k) * 86400)) for k in keys]
    return dates, eq[1:]


def by_year(res):
    s = pd.Series(res.equity, index=pd.to_datetime(res.t + res.dt, unit="s"))
    out = {}
    prev = res.initial_equity
    for y, g in s.groupby(s.index.year):
        e = g.values
        r = e / np.r_[prev, e[:-1]] - 1
        dd = float((e / np.maximum.accumulate(np.r_[prev, e])[1:] - 1).min())
        out[str(y)] = {"return": float(e[-1] / prev - 1), "max_drawdown": dd,
                       "days": int(len(e))}
        prev = e[-1]
    return out


def pair_trips(res, Np, symbols):
    """Pair-level round trips: legs of the same coin opened on the same bar."""
    td = res.trades.df()
    if td.empty:
        return td
    td["coin"] = td["symbol"].str.replace("@SPOT", "", regex=False)
    g = td.groupby(["coin", "open_bar"]).agg(pnl=("pnl", "sum"), open_t=("open_t", "first"),
                                             close_t=("close_t", "max"),
                                             notional=("entry_notional", "max"),
                                             fees=("fees", "sum"), funding=("funding", "sum"),
                                             legs=("symbol", "count"),
                                             is_open=("is_open", "max")).reset_index()
    g["hold_h"] = (g["close_t"] - g["open_t"]) / 3600.0
    return g


def stitched_weights(P, fold_info, params_fn):
    T, N = len(P.t), len(P.symbols)
    W = np.zeros((T, N))
    for fi in fold_info:
        ia, ib, ic = fi["bars"]
        sub = S.slice_panel(P, 0, ic)
        W[ib:ic] = C.weights(sub, params_fn(fi["params"]))[ib:ic]
    a, b = fold_info[0]["bars"][1], fold_info[-1]["bars"][2]
    return W, a, b


def main():
    log("loading panel")
    P = C.load_panel(end=END)
    Np = P.meta["n_pairs"]
    SK = C.sim_kwargs(P)
    log(f"panel {len(P.t)} bars x {len(P.symbols)} cols ({Np} pairs), last bar open "
        f"{time.strftime('%Y-%m-%d', time.gmtime(int(P.t[-1])))}")

    # ------------------------------------------------------------ walk-forward
    log(f"walk-forward over {len(C.GRID)} configs")
    wf = WF.walk_forward(P, C.weights, C.GRID, train_days=730, test_days=182, step_days=182,
                         objective="sharpe", sim_kwargs=SK, causality_checks=2,
                         compute_pbo=True, label="carry_gated")
    oos = wf["oos_result"]
    om = oos.metrics()
    log("OOS", {k: om[k] for k in ("cagr", "sharpe", "max_drawdown", "vol_annual")})
    folds = [{"train": [f["train_start"], f["test_start"]], "test": [f["test_start"], f["test_end"]],
              "chosen": f["params"], "train_score": f["train_score"],
              "test_metrics": pick(f["test_metrics"])} for f in wf["folds"]]
    cnt = Counter(json.dumps(f["params"], sort_keys=True) for f in wf["folds"])
    # FROZEN: most chosen; tie -> best median train-rank across folds
    ranks = np.argsort(np.argsort(-np.nan_to_num(wf["scores"], nan=-1e9), axis=1), axis=1)
    med_rank = {json.dumps(g, sort_keys=True): float(np.median(ranks[:, k]))
                for k, g in enumerate(C.GRID)}
    best = sorted(cnt.items(), key=lambda kv: (-kv[1], med_rank[kv[0]]))[0][0]
    frozen = json.loads(best)
    log("chosen counts", dict(cnt), "FROZEN", frozen)

    # --------------------------------------------------------- frozen on dev
    Wf = C.weights(P, frozen)
    rf = S.run_weights(P, Wf, **SK)
    mf = rf.metrics()
    fd_dates, fd_eq = daily(rf)
    fd_ret = M.daily_returns(rf.t, rf.dt, rf.equity, rf.initial_equity)
    log("FROZEN dev", {k: mf[k] for k in ("cagr", "sharpe", "max_drawdown", "vol_annual")})
    # frozen over the OOS span only (for the null / like-for-like)
    a_oos = wf["folds"][0]["bars"][1]
    rf_oos = S.run_weights(S.slice_panel(P, a_oos, len(P.t)), Wf[a_oos:], **SK)
    mf_oos = rf_oos.metrics()

    # ------------------------------------------------------------ causality
    caus = WF.check_causality(P, C.weights, frozen, n_checks=6)
    caus_vt = WF.check_causality(P, C.weights, dict(frozen, vol_target=0.20), n_checks=4, seed=1)
    log("causality", caus["ok"], caus_vt["ok"])

    # ------------------------------------------------------------ null
    # Pair-level random timing: each coin's holding runs (same count, same
    # lengths) are placed at random inside that coin's HEDGEABLE span (perp in
    # top-30, both legs valid), both legs together, same sizing / drift control.
    # (The lab's random_timing_null permutes each COLUMN independently, which
    # would un-hedge the pairs - meaningless for carry.)
    log("null (pair random timing)")
    st, H = C._run(P, frozen)
    span = st["mem"] & st["pv"] & st["sv"] & (st["page"] >= 30) & (st["sage"] >= 30)
    a0 = a_oos

    def sharpe_of(Hx, a):
        W = C._weights_from_H(st, Hx)
        r = S.run_weights(S.slice_panel(P, a, len(P.t)), W[a:], **dict(SK, record_positions=False))
        return M.equity_metrics(r.t, r.dt, r.equity, r.initial_equity)["sharpe"]

    def runs(col):
        x = np.r_[0, col.astype(int), 0]
        d = np.diff(x)
        return np.flatnonzero(d == 1), np.flatnonzero(d == -1)

    rng = np.random.default_rng(0)
    null_s = []
    NNULL = 200
    for k in range(NNULL):
        Hn = np.zeros_like(H)
        for j in range(Np):
            s0, e0 = runs(H[a0:, j])
            if not s0.size:
                continue
            lens = e0 - s0
            ok = np.flatnonzero(span[a0:, j])
            if ok.size == 0:
                continue
            for L in rng.permutation(lens):
                for _try in range(20):
                    st_i = int(rng.choice(ok))
                    seg = slice(a0 + st_i, a0 + st_i + L)
                    if a0 + st_i + L <= len(P.t) and not Hn[seg, j].any():
                        Hn[seg, j] = True
                        break
        null_s.append(sharpe_of(Hn, a0))
    null_s = np.array(null_s)
    s_str = mf_oos["sharpe"]
    null = {"kind": "pair_random_timing (both legs moved together, per-coin run lengths "
                    "kept, placed inside the coin's hedgeable+top30 span; FROZEN, OOS span "
                    "2022-01..2025-06)",
            "n": NNULL, "strategy_sharpe": s_str, "null_mean": float(null_s.mean()),
            "null_p95": float(np.percentile(null_s, 95)),
            "percentile": float((null_s < s_str).mean() * 100),
            "p_value": float((1 + (null_s >= s_str).sum()) / (NNULL + 1))}
    log("null", null)

    # --------------------------------------------------------- deflated sharpe
    r_oos = M.daily_returns(oos.t, oos.dt, oos.equity, oos.initial_equity)
    grid_sr = []
    for g in C.GRID:
        rr = S.run_weights(S.slice_panel(P, a_oos, len(P.t)), C.weights(P, g)[a_oos:],
                           **dict(SK, record_positions=False))
        grid_sr.append(M.equity_metrics(rr.t, rr.dt, rr.equity, rr.initial_equity)["sharpe"])
    grid_sr = np.array(grid_sr)
    dsr_null = om["dsr"] if "dsr" in om else wf["oos_metrics"]["dsr"]
    dsr_grid = M.deflated_sharpe(om["sharpe"], len(C.GRID), r_oos.size, om["skew"],
                                 om["kurtosis"], trials_sr_std_annual=float(grid_sr.std(ddof=1)))

    # ------------------------------------------------------------ sensitivity
    sens = []

    def neigh(param, vals):
        cur = frozen[param]
        if cur not in vals:
            return []
        k = vals.index(cur)
        return [vals[x] for x in (k - 1, k + 1) if 0 <= x < len(vals)]

    variants = [("h", v) for v in neigh("h", C._H)] + [("K", v) for v in neigh("K", [5, 8])]
    variants += [("gate", v) for v in ([None] if frozen["gate"] is not None else [0.6])]
    variants += [("gate_exit", not frozen["gate_exit"])] if frozen["gate"] is not None else []
    # non-grid fixed choices, for information (not searched)
    extra = [("cost_mult", 1.0), ("cost_mult", 2.0), ("band", 0.15), ("band", 0.5),
             ("stress_abs", 0.003), ("basis_in", 0.03), ("K", 3), ("K", 12)]
    for (pname, v), tag in [(x, "grid") for x in variants] + [(x, "fixed-choice") for x in extra]:
        g = dict(frozen); g[pname] = v
        W = C.weights(P, g)
        rr = S.run_weights(S.slice_panel(P, a_oos, len(P.t)), W[a_oos:], **dict(SK, record_positions=False))
        mm = M.equity_metrics(rr.t, rr.dt, rr.equity, rr.initial_equity)
        sens.append({"param": pname, "value": v, "kind": tag, "span": "2022-01..2025-06 (frozen, not WF)",
                     "oos_or_dev_sharpe": mm["sharpe"], "cagr": mm["cagr"], "maxdd": mm["max_drawdown"]})
    log("sensitivity done")

    # ------------------------------------------------ implementability ($200)
    inst = dict(D.load_bybit_instruments())
    sp = json.load(open(os.path.join(D.HIST, "spot", "bybit_spot_instruments.json")))["instruments"]
    scales = {}
    for s in P.symbols[:Np]:
        fp = os.path.join(C.SPOT_DIR, s + ".npz")
        if os.path.exists(fp):
            with np.load(fp) as z:
                scales[s] = float(z["scale"])
    traded = sorted({P.symbols[j] for j in np.flatnonzero((np.abs(Wf[:, :Np]) > 0).any(0))})
    miss_perp, miss_spot, spot_names = [], [], {}
    for s in traded:
        if s not in inst:
            miss_perp.append(s)
        nm = P.meta["spot_symbols"][P.symbols.index(s)]
        spot_names[s] = nm
        x = sp.get(nm)
        if not x:
            miss_spot.append(nm)
            continue
        sc = scales.get(s, 1.0)
        inst[s + "@SPOT"] = {"qtyStep": x["basePrecision"] / sc, "minOrderQty": x["minOrderQty"] / sc,
                             "minNotionalValue": x["minOrderAmt"]}
    rq = S.run_weights(P, Wf, **dict(SK, instruments=inst, round_to_qty=True))
    mq = rq.metrics()
    # dropped-order share: orders (weight changes) whose notional is below the minimum
    eq_ref = np.r_[200.0, rf.equity[:-1]]
    dW = np.abs(np.diff(np.vstack([np.zeros((1, Wf.shape[1])), Wf]), axis=0))
    n_ord = n_drop = 0
    for j in np.flatnonzero((dW > 0).any(0)):
        ins = inst.get(P.symbols[j])
        if not ins:
            continue
        for i in np.flatnonzero(dW[:, j] > 0):
            if i + 1 >= len(P.t):
                continue
            closing = Wf[i, j] == 0
            n_ord += 1
            notional = dW[i, j] * eq_ref[i + 1]
            px = P.o[i + 1, j]
            if not closing and (notional < ins.get("minNotionalValue", 0) or
                                (np.isfinite(px) and notional / px < ins.get("minOrderQty", 0))):
                n_drop += 1
    impl = {"metrics_round_to_qty": pick(mq),
            "metrics_unrounded": pick(mf),
            "orders": n_ord, "dropped_orders": n_drop,
            "dropped_share": n_drop / max(n_ord, 1),
            "traded_perps": len(traded),
            "perps_missing_on_bybit_linear_today": miss_perp,
            "spot_missing_on_bybit_spot_today": miss_spot,
            "spot_name_map_nonidentity": {k: v for k, v in spot_names.items() if k != v},
            "note": "Bybit spot rules from public instruments-info (basePrecision/minOrderQty/"
                    "minOrderAmt), converted to perp price units; instruments are TODAY's, "
                    "applied to history."}
    log("impl", impl["dropped_share"], mq["cagr"])

    # ------------------------------------------------ vol-target (scaled) variant
    log("vol-target variant (20%, lev_cap 2.5/leg, 8% borrow)")
    vt_fn = lambda p: dict(p, vol_target=0.20)
    Wv, a, b = stitched_weights(P, wf["folds"], vt_fn)
    Pb = C.borrow_panel(P, Wv)
    rv = S.run_weights(S.slice_panel(Pb, a, b), Wv[a:b], **SK)
    mv = rv.metrics()
    Wvd = C.weights(P, vt_fn(frozen))
    rvd = S.run_weights(C.borrow_panel(P, Wvd), Wvd, **SK)
    mvd = rvd.metrics()
    Wv0, _, _ = stitched_weights(P, wf["folds"], lambda p: dict(p, vol_target=0.20))
    rv_nb = S.run_weights(S.slice_panel(P, a, b), Wv0[a:b], **SK)     # borrow NOT charged
    # liquidation diagnostics under harsher mark conventions
    liq = {}
    for marks in ("body", "raw"):
        Pm = C.load_panel(end=END, hedge_marks=marks)
        r1 = S.run_weights(S.slice_panel(Pm, a, b),
                           stitched_weights(Pm, wf["folds"], lambda p: p)[0][a:b], **SK)
        r2 = S.run_weights(S.slice_panel(C.borrow_panel(Pm, Wv), a, b), Wv[a:b], **SK)
        liq[marks] = {"1x_oos_liquidations": r1.n_liquidations,
                      "1x_oos_cagr": r1.metrics()["cagr"],
                      "voltarget_oos_liquidations": r2.n_liquidations,
                      "voltarget_oos_cagr": r2.metrics()["cagr"],
                      "voltarget_liq_events": [time.strftime("%Y-%m-%d", time.gmtime(int(x["t"])))
                                               for x in r2.liquidations][:5]}
        Pm_full = Pm
    # raw marks, frozen over the whole dev period at 1x (the 2021-05-19 false liquidation)
    r_raw_dev = S.run_weights(Pm_full, C.weights(Pm_full, frozen), **SK)
    liq["raw_frozen_dev_1x"] = {"liquidations": r_raw_dev.n_liquidations,
                                "events": [time.strftime("%Y-%m-%d", time.gmtime(int(x["t"])))
                                           for x in r_raw_dev.liquidations][:5]}
    del Pm, Pm_full
    L_used = (Wv[a:b, Np:].sum(1))
    vt = {"params": "fold-chosen params + vol_target=0.20, lev_cap=2.5 per leg (gross 5x), "
                    "L changed only on >25% moves, borrow 8% APR on spot notional above 1x equity",
          "oos_metrics": pick(mv), "oos_by_year": by_year(rv),
          "oos_metrics_if_borrow_free": pick(rv_nb.metrics()),
          "frozen_dev_metrics": pick(mvd),
          "mean_spot_notional_over_equity": float(L_used.mean()),
          "max_spot_notional_over_equity": float(L_used.max()),
          "share_days_borrowing": float((L_used > 1.0).mean()),
          "realised_vol_oos": mv["vol_annual"],
          "liquidation_checks": liq}
    vd_dates, vd_eq = daily(rvd)
    vt["frozen_dev_daily"] = {"dates": fd_dates,
                              "returns": M.daily_returns(rvd.t, rvd.dt, rvd.equity, rvd.initial_equity).tolist()}
    log("vt OOS", {k: mv[k] for k in ("cagr", "sharpe", "max_drawdown", "vol_annual")})

    # ------------------------------------------------ basis / hedge diagnostics
    Hh = np.abs(Wf[:, Np:]) > 0
    basis = st["basis"]
    Hprev = np.vstack([np.zeros((1, Np), bool), Hh[:-1]])
    with np.errstate(invalid="ignore"):
        pr = np.vstack([np.zeros((1, Np)), P.c[1:, :Np] / P.c[:-1, :Np] - 1])
        sr = np.vstack([np.zeros((1, Np)), P.c[1:, Np:] / P.c[:-1, Np:] - 1])
    hedge_err = np.where(Hprev, sr - pr, np.nan)
    Praw = P  # closes are identical in every mark mode
    diag = {"held_pair_days": int(Hprev.sum()),
            "abs_basis_at_close_held_p99": float(np.nanpercentile(np.abs(np.where(Hh, basis, np.nan)), 99)),
            "abs_basis_at_close_held_max": float(np.nanmax(np.abs(np.where(Hh, basis, np.nan)))),
            "daily_hedge_error_spot_minus_perp_ret_std": float(np.nanstd(hedge_err)),
            "daily_hedge_error_worst": float(np.nanmin(hedge_err)),
            "daily_hedge_error_best": float(np.nanmax(hedge_err))}

    # ------------------------------------------------ activity / regime
    yrs = pd.to_datetime(P.t, unit="s").year.values
    gate_on = st["gate_share"] > (frozen["gate"] if frozen["gate"] is not None else -1)
    act = {}
    for y in np.unique(yrs):
        k = yrs == y
        act[str(y)] = {"share_days_any_pair": float((Hh[k].sum(1) > 0).mean()),
                       "avg_pairs": float(Hh[k].sum(1).mean()),
                       "share_days_gate_on": float(gate_on[k].mean()),
                       "median_gate_share": float(np.median(st["gate_share"][k]))}
    # pair trips over OOS
    trips = pair_trips(oos, Np, P.symbols)
    closed = trips[~trips["is_open"].astype(bool)] if len(trips) else trips
    days_oos = (oos.t[-1] + oos.dt - oos.t[0]) / 86400
    tpd = len(trips) / days_oos if days_oos else 0.0
    leg_orders = int((np.abs(np.diff(wf["oos_result"].positions, axis=0)) > 0).sum())
    wins = closed["pnl"] > 0 if len(closed) else pd.Series(dtype=bool)
    avg_w = closed.loc[wins, "pnl"].mean() if wins.any() else 0.0
    avg_l = -closed.loc[~wins, "pnl"].mean() if (~wins).any() else 0.0
    coin_pnl = trips.groupby("coin")["pnl"].sum().sort_values() if len(trips) else pd.Series(dtype=float)
    top3 = float(coin_pnl.tail(3).sum() / coin_pnl.sum()) if len(coin_pnl) and coin_pnl.sum() > 0 else None

    # live targets as of the last DEV bar (illustration of the interface)
    lt = C.live_targets(P, frozen)

    res = {
        "name": "carry_gated",
        "description": "Delta-neutral funding carry: long Binance-spot-modelled SPOT + short USDT "
                       "perp in the same coin and notional, entered when the trailing 7d funding "
                       "is high and persistent enough to beat the 4-leg round trip, gated by "
                       "market-wide funding breadth, excluding cap-stressed / 1h-settlement names.",
        "mechanism": "Leveraged-long demand from retail plus scarce arbitrage capital keeps perps "
                     "above spot, so perp shorts are paid funding; the spot leg removes price "
                     "exposure. Paid for crash/basis/exchange risk (BIS WP1087).",
        "universe": "Binance USDT-M perps in the PIT top-30 (daily re-ranked, survivorship-aware), "
                    "only where a Binance SPOT USDT pair exists (Binance spot first kline = PIT "
                    "hedgeability proxy); 246 of 263 perps ever in the dev top-30 have a spot pair",
        "timeframe": "1d (decision at the 00:00 UTC close = the 00:07 run; fills next open)",
        "panel": {"loader": "lab.strategies.carry_gated.load_panel(end=...)", **{k: v for k, v in C.PANEL.items() if k != "loader"},
                  "hedge_marks": "close", "sim_kwargs": "carry_gated.sim_kwargs(panel) (per-column slippage; "
                                                          "spot = perp tier + 4.5 bps for the 0.10% spot fee)"},
        "n_trials": len(C.GRID),
        "grid_summary": {"h": C._H, "K": [5, 8], "gate": "[None, 0.6 entry-only, 0.6 entry+exit]",
                         "fixed": {k: v for k, v in C.DEFAULTS.items() if k not in ("h", "K", "gate", "gate_exit", "vol_target")},
                         "oos_span_sharpe_by_config": [{"params": g, "sharpe_2022_2025H1": float(s)}
                                                       for g, s in zip(C.GRID, grid_sr)],
                         "note": "for most coins the cost condition (14*f7 > 1.5*RT, RT 0.35-0.63%) "
                                 "binds before h: it implies ~17-25%/yr, so h in {8,12,15}% changes little"},
        "frozen": frozen,
        "frozen_rule": "most-chosen config across the walk-forward folds; ties broken by the best "
                       "median train-rank across folds",
        "wf": {"folds": folds, "oos_metrics": pick(om), "oos_by_year": by_year(oos),
               "dsr_lab": wf["oos_metrics"].get("dsr"), "pbo": wf.get("pbo"),
               "train_days": 730, "test_days": 182, "objective": "sharpe"},
        "oos_daily": {"dates": daily(oos)[0], "equity": daily(oos)[1].tolist()},
        "frozen_dev_daily": {"dates": fd_dates, "returns": fd_ret.tolist()},
        "frozen_dev_metrics": pick(mf),
        "frozen_oos_span_metrics": pick(mf_oos),
        "null": null,
        "deflated_sharpe": dsr_null,
        "deflated_sharpe_grid_variance": dsr_grid,
        "sensitivity": sens,
        "implementability_200": impl,
        "vol_target_variant": vt,
        "natural_vol_note": "The main stream (wf, oos_daily, frozen_dev_daily) is the NATURAL 1x book "
                            "(vol_target=None): spot notional <= 1x equity, realised vol ~2%/yr. "
                            "vol_target_variant is the 20%-target request, capped at 2.5x per leg.",
        "trades_per_day": tpd,
        "leg_orders_per_day": leg_orders / days_oos if days_oos else 0.0,
        "avg_hold_hours": float(trips["hold_h"].mean()) if len(trips) else None,
        "win_rate": float(wins.mean()) if len(closed) else None,
        "payoff": float(avg_w / avg_l) if avg_l else None,
        "expectancy_per_trade": float(closed["pnl"].mean()) if len(closed) else None,
        "expectancy_per_trade_units": "USD per pair round trip on the $200-start OOS book",
        "worst_trade": float(closed["pnl"].min()) if len(closed) else None,
        "top3_coin_pnl_share": top3,
        "top_coins_pnl": {k: float(v) for k, v in coin_pnl.tail(5).items()},
        "exposure": om["exposure"],
        "fee_drag_per_year": om["fee_drag_per_year"],
        "funding_per_year": om["funding_per_year"],
        "funding_sign_note": "negative funding_per_year = funding RECEIVED (lab convention + = paid)",
        "activity_by_year": act,
        "hedge_diagnostics": diag,
        "causality": {"frozen": caus, "frozen_vol_target_0.20": caus_vt},
        "live_targets_example_last_dev_bar": lt,
        "needs_hourly_runs": False,
        "data_end": wf["data_end"],
    }
    json.dump(jsafe(res), open(OUT, "w"), indent=1)
    log("wrote", OUT)


if __name__ == "__main__":
    main()
