"""Evaluation runner for ml_ranker_ew -> results/ml_ranker_ew.json (DEV data only)."""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import metrics as M, sim as S  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _ml_ranker_run as RR  # noqa: E402  (patches wf.walk_forward start=2021-01-01)
from lab.strategies import ml_ranker as MR  # noqa: E402
from lab.strategies import ml_ranker_ew as EW  # noqa: E402
from lab.strategies import _micro_stats as ST  # noqa: E402

GROUPS = {"price": ["r1", "r3", "r7", "r14", "r30", "r60", "dhi", "dlo"], "risk": ["rv7", "rv30", "volvol"],
          "volume": ["vz7", "vz30"], "flow": ["tb1", "tb7"], "carry": ["f1", "f7", "df"],
          "crowd": ["zG", "zT", "D", "oi1", "oi7"]}


def ew_subset(P, feats):
    X, _ = MR.ranked_features(P)
    T, N = P.c.shape
    acc, cnt = np.zeros((T, N)), np.zeros((T, N))
    for k in feats:
        v = X[k]
        ok = np.isfinite(v)
        acc[ok] += MR.SIGNS[k] * v[ok]
        cnt[ok] += 1
    with np.errstate(invalid="ignore", divide="ignore"):
        pred = np.where(cnt > 0, acc / cnt, np.nan)
    avail = np.isfinite(X["r1"]) & np.isfinite(X["r7"]) & np.isfinite(X["rv30"])
    pred[~avail] = np.nan
    return pred


def corr_block(dates, rets, P):
    s_me = pd.Series(rets, index=pd.to_datetime(dates))
    s_me = s_me[s_me.index >= pd.Timestamp("2021-01-01")]
    out = {}
    for other in ("micro_crowd", "micro_flowxs"):
        oj = json.load(open(os.path.join(HX.RESULTS, other + ".json")))
        so = pd.Series(oj["frozen_dev_daily"]["returns"], index=pd.to_datetime(oj["frozen_dev_daily"]["dates"]))
        jj = pd.concat([s_me, so], axis=1, join="inner").dropna()
        out[other] = HX._fmt(jj.corr().iloc[0, 1], 3)
        out[other + "_n_days"] = int(len(jj))
    jb = P.symbols.index("BTCUSDT")
    btc = pd.Series(P.c[:, jb], index=pd.to_datetime(P.t, unit="s")).pct_change()
    jj = pd.concat([s_me, btc], axis=1, join="inner").dropna()
    out["btc"] = HX._fmt(jj.corr().iloc[0, 1], 3)
    return out


def main():
    RR.log("load")
    P = MR.load()
    o = HX.evaluate(EW, train_days=MR.OUTER_TRAIN_DAYS, test_days=182, step_days=182, null_n=200,
                    family_trials=RR.N_TRIALS_TOTAL, write=False, panel=P)
    RR.log("evaluated", o["wf"]["oos_metrics"].get("sharpe"), o["frozen"])
    fl = RR.oos_bars(P, o)
    W = HX._oos_weights(P, EW, fl)
    a, b = fl[0]["bars"][1], fl[-1]["bars"][2]
    sub = S.slice_panel(P, a, b)
    base = S.run_weights(sub, W[a:b])
    cost = {"base": RR.mrow(base),
            "double_fee": RR.mrow(S.run_weights(sub, W[a:b], fee=0.0011)),
            "double_fee_and_slippage": RR.mrow(S.run_weights(sub, W[a:b], fee=0.0011,
                                                             slippage_bps=2 * S.default_slippage_bps(sub.symbols))),
            "triple_slippage": RR.mrow(S.run_weights(sub, W[a:b], slippage_bps=3 * S.default_slippage_bps(sub.symbols))),
            "gross_no_costs": RR.mrow(S.run_weights(sub, W[a:b], fee=0.0, slippage_bps=0.0)),
            "no_funding": RR.mrow(S.run_weights(sub, W[a:b], funding=False))}
    lagW = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])
    cost["extra_1d_decision_lag"] = RR.mrow(S.run_weights(sub, lagW[a:b]))
    fz = o["frozen"]
    wfz = EW.weights(P, fz)
    o["robustness_dev_frozen"] = {"double_fee_dev": RR.mrow(S.run_weights(P, wfz, fee=0.0011)),
                                  "base_dev": RR.mrow(S.run_weights(P, wfz))}
    # legs
    legs = {"long_leg": RR.mrow(S.run_weights(sub, np.clip(W[a:b], 0, None))),
            "short_leg": RR.mrow(S.run_weights(sub, np.clip(W[a:b], None, 0)))}
    net = W[a:b].sum(1)
    legs["mean_net_weight"] = HX._fmt(float(net.mean()))
    # concentration
    tr = base.trades.df()
    by = tr.groupby("symbol")["pnl"].sum().sort_values()
    tot = float(by.sum())
    conc = {"total_pnl_usd": round(tot, 2), "n_symbols": int(len(by)),
            "top5": {k: round(float(v), 2) for k, v in by[::-1][:5].items()},
            "bottom5": {k: round(float(v), 2) for k, v in by[:5].items()},
            "top5_share_of_total": HX._fmt(float(by[::-1][:5].sum()) / tot if tot else None, 3),
            "pnl_ex_top5_usd": round(tot - float(by[::-1][:5].sum()), 2)}
    shorts = tr[tr["side"] < 0]
    conc["worst_short_trade_ret"] = HX._fmt(float(shorts["ret"].min())) if len(shorts) else None
    conc["worst_short_trade"] = (shorts.sort_values("ret").iloc[0][["symbol", "open_t", "ret", "pnl"]].to_dict()
                                 if len(shorts) else None)
    RR.log("legs/conc done")
    # stops
    stops = [{"stop": None, **{k: cost["base"][k] for k in ("sharpe", "cagr", "max_drawdown")}}]
    stops += [RR.stop_overlay(P, W, a, b, s, {}) for s in (0.10, 0.15, 0.25)]
    # ablation (post-hoc diagnostics, frozen H/k, OOS window; NOT used for selection)
    abl = {}
    allf = [f for g in GROUPS.values() for f in g]
    def run_pred(pred):
        w = MR.weights_from_pred(P, pred, fz)
        r = S.run_weights(sub, w[a:b])
        m = RR.mrow(r)
        return {k: m[k] for k in ("sharpe", "cagr", "max_drawdown", "turnover_per_year", "funding_per_year")}
    abl["all"] = run_pred(ew_subset(P, allf))
    for g, fs in GROUPS.items():
        abl["only_" + g] = run_pred(ew_subset(P, fs))
        abl["without_" + g] = run_pred(ew_subset(P, [f for f in allf if f not in fs]))
    abl["textbook_priors_only(price,risk,volume,carry)"] = run_pred(
        ew_subset(P, GROUPS["price"] + GROUPS["risk"] + GROUPS["volume"] + GROUPS["carry"]))
    abl["phase2_derived_only(flow,crowd)"] = run_pred(ew_subset(P, GROUPS["flow"] + GROUPS["crowd"]))
    RR.log("ablation done")
    ic, _ = RR.ic_by_year(P, dict(model="ew", H=int(fz["H"])), a)
    fd = o["frozen_dev_daily"]
    o["correlation_to"] = corr_block(fd["dates"], fd["returns"], P)
    # OOS-window correlation of the stitched OOS book vs micro_flowxs OOS equity
    oj = json.load(open(os.path.join(HX.RESULTS, "micro_flowxs.json")))
    fx = pd.Series(oj["oos_daily"]["equity"], index=pd.to_datetime(oj["oos_daily"]["dates"])).pct_change()
    me = pd.Series(o["oos_daily"]["equity"], index=pd.to_datetime(o["oos_daily"]["dates"])).pct_change()
    jj = pd.concat([me, fx], axis=1, join="inner").dropna()
    o["correlation_to"]["micro_flowxs_oos_books"] = HX._fmt(jj.corr().iloc[0, 1], 3)
    om = o["wf"]["oos_metrics"]
    rd = RR.daily_ret(base)
    o["n_trials"] = len(EW.GRID)
    o["n_trials_family_H"] = RR.N_TRIALS_TOTAL
    o["deflated_sharpe_4_only"] = o["deflated_sharpe"]
    o["deflated_sharpe"] = HX._fmt(M.deflated_sharpe(om["sharpe"], RR.N_TRIALS_TOTAL, max(len(rd), 2),
                                                     om["skew"], om["kurtosis"]))
    o["cost_sensitivity_oos"] = cost
    o["legs_oos"] = legs
    o["concentration_oos"] = conc
    o["protective_stops"] = stops
    o["ablation_post_hoc"] = abl
    o["oos_ic_by_year"] = ic
    o["oos_2025h1_return"] = o["wf"]["oos_by_year"].get(2025, {}).get("return")
    o["live_retrain_cadence"] = "none (no model); daily decision at the 00:07 UTC run on the closed 1d bar"
    v, cav = HX.default_verdict(o)
    o["verdict"] = v
    o["caveats"] = list(EW.CAVEATS) + [
        "Signs of the taker-flow (tb1, tb7 +) and crowd (zG -, D +) features were informed by phase-2 results on the SAME 2022-2025H1 dev data: those components are not a clean OOS test; see ablation_post_hoc (textbook-priors-only row).",
        "This was pre-registered as the sanity BASELINE for the ML ranker, not as a strategy; promoting it after it won is itself a selection step (counted: 14 family-H trials).",
    ] + cav
    with open(os.path.join(HX.RESULTS, "ml_ranker_ew.json"), "w") as f:
        json.dump(o, f, indent=1, default=HX._json_default)
    RR.log("DONE", v, om.get("sharpe"), om.get("cagr"), om.get("max_drawdown"))


if __name__ == "__main__":
    main()
