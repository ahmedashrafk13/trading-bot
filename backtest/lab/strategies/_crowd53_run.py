"""Runner for the family-F crowd composite modules: harness evaluation + family-F diagnostics.

python backtest/lab/strategies/_crowd53_run.py crowd_ts53|crowd_xs53

Dev data only (panel end 2025-06-30, pre_lockbox). Writes results/<name>.json.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import metrics as M, sim as S, wf  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _crowd53_common as CC  # noqa: E402

TRAIN_DAYS = 365
FAMILY_TRIALS = 60


def _f(x, nd=4):
    return HX._fmt(x, nd)


def fold_bars(P):
    return wf.make_folds(P.t, P.dt, TRAIN_DAYS, 182, 182, "rolling", None, 30)


def stitched(P, folds, chosen, fn):
    """OOS weights using each fold's chosen params, computed on the panel cut at the test end."""
    T, N = P.c.shape
    W = np.zeros((T, N))
    for (ia, ib, ic), prm in zip(folds, chosen):
        sub = S.slice_panel(P, 0, ic)
        W[ib:ic] = np.asarray(fn(sub, prm), float)[ib:ic]
    return W


def run_slice(P, W, a, b, **kw):
    sub = S.slice_panel(P, a, b)
    return sub, S.run_weights(sub, W[a:b], **kw)


def summ(res):
    m = M.equity_metrics(res.t, res.dt, res.equity, res.initial_equity)
    return {"sharpe": _f(m["sharpe"], 3), "cagr": _f(m["cagr"]), "maxdd": _f(m["max_drawdown"]),
            "fee_drag_per_year": _f((res.fees_paid + res.slippage_paid) / max(float(np.mean(res.equity)), 1e-9)
                                    / max(len(res.t) * res.dt / 3.15576e7, 1e-9)),
            "fee_drag_def": "(fees+slippage) / mean equity / years"}


def by_year_from_daily(dates, rets):
    s = pd.Series(rets, index=pd.to_datetime(dates))
    out = {}
    for y, g in s.groupby(s.index.year):
        out[int(y)] = {"return": _f(float(np.prod(1 + g) - 1)),
                       "sharpe": _f(g.mean() / g.std(ddof=1) * np.sqrt(365) if g.std(ddof=1) > 0 else np.nan, 3)}
    h1 = s[(s.index >= "2025-01-01") & (s.index < "2025-07-01")]
    out["2025H1"] = {"return": _f(float(np.prod(1 + h1) - 1))} if len(h1) else None
    return out


def daily_rets(res):
    k, e = M.daily_equity(res.t, res.dt, res.equity, res.initial_equity)
    d = pd.to_datetime(np.asarray(k, np.int64) * 86400, unit="s")
    return pd.Series(e[1:] / e[:-1] - 1, index=d)


def corr_block(mine_dev: pd.Series, mine_oos: pd.Series, P):
    out = {}
    for other in ("micro_crowd", "micro_flowxs"):
        o = json.load(open(os.path.join(HX.RESULTS, other + ".json")))
        fd = pd.Series(o["frozen_dev_daily"]["returns"], index=pd.to_datetime(o["frozen_dev_daily"]["dates"]))
        oe = pd.Series(o["oos_daily"]["equity"], index=pd.to_datetime(o["oos_daily"]["dates"]))
        oo = oe.pct_change().dropna()
        a = pd.concat([mine_dev, fd], axis=1, join="inner").dropna()
        a = a[(a.iloc[:, 0] != 0) | (a.iloc[:, 1] != 0)]
        b = pd.concat([mine_oos, oo], axis=1, join="inner").dropna()
        out[other] = {"dev_frozen": _f(a.corr().iloc[0, 1], 3), "n_days_dev": int(len(a)),
                      "oos_stitched": _f(b.corr().iloc[0, 1], 3), "n_days_oos": int(len(b))}
    j = P.symbols.index("BTCUSDT")
    btc = pd.Series(P.c[:, j], index=pd.to_datetime(P.t + P.dt - 1, unit="s").floor("D")).groupby(level=0).last().pct_change()
    a = pd.concat([mine_dev, btc], axis=1, join="inner").dropna()
    out["btc"] = {"dev_frozen": _f(a.corr().iloc[0, 1], 3), "n_days_dev": int(len(a))}
    return out


def worst_eq(res):
    tr = res.trades.df()
    if not len(tr):
        return None
    eq = np.asarray(res.equity)
    fr = tr["pnl"].to_numpy() / np.maximum(eq[np.clip(tr["open_bar"].to_numpy().astype(int) - 1, 0, len(eq) - 1)], 1e-9)
    k = int(np.argmin(fr))
    return {"frac": _f(float(fr[k])), "symbol": str(tr["symbol"].iloc[k]),
            "open": pd.to_datetime(int(res.t[int(tr["open_bar"].iloc[k])]), unit="s").strftime("%Y-%m-%d %H:%M")}


def pnl_concentration(res):
    tr = res.trades.df()
    if not len(tr):
        return {}
    g = tr.groupby("symbol")["pnl"].sum().sort_values(ascending=False)
    tot = float(g.sum())
    top5 = g.head(5)
    return {"total_pnl_usd": round(tot, 2), "top5": {k: round(float(v), 2) for k, v in top5.items()},
            "top5_share_of_total": _f(float(top5.sum()) / tot if tot else np.nan, 3),
            "bottom5": {k: round(float(v), 2) for k, v in g.tail(5).items()},
            "n_symbols_traded": int(len(g)), "share_symbols_positive": _f(float((g > 0).mean()), 3)}


def main(name, null_n=200):
    t0 = time.time()
    mod = importlib.import_module(f"lab.strategies.{name}")
    P = HX.load_for(mod)
    out = HX.evaluate(mod, train_days=TRAIN_DAYS, null_n=null_n, family_trials=FAMILY_TRIALS, panel=P, write=False)
    frozen = out["frozen"]
    folds = fold_bars(P)
    chosen = [f["chosen"] for f in out["wf"]["folds"]]
    assert len(chosen) == len(folds), (len(chosen), len(folds))
    a, b = folds[0][1], folds[-1][2]
    print(name, "harness done", round(time.time() - t0), "s; OOS sharpe", out["wf"]["oos_metrics"].get("sharpe"), flush=True)

    base_fn = lambda p, prm, **k: mod.weights(p, prm, **k)   # noqa: E731
    # ---- OOS base (stitched), with stop events for the fill correction
    W0 = stitched(P, folds, chosen, lambda p, prm: mod.weights(p, prm))
    sub, r0 = run_slice(P, W0, a, b)
    ev = []
    mod.weights(P, frozen, events=ev)                              # events on the frozen dev run
    rfro = S.run_weights(P, mod.weights(P, frozen))
    stop_corr_dev = CC.stop_fill_correction(P, rfro, ev)
    # OOS stop events (per fold)
    ev_oos = []
    for (ia, ib, ic), prm in zip(folds, chosen):
        e = []
        mod.weights(S.slice_panel(P, 0, ic), prm, events=e)
        ev_oos += [(i - a, j, s, px) for (i, j, s, px) in e if ib <= i < ic]
    stop_corr_oos = CC.stop_fill_correction(sub, r0, ev_oos)

    # ---- leave-one-out and single-feature (OOS stitched with each fold's chosen params, and dev frozen)
    feat_diag = {}
    for f in CC.FEATS:
        rest = tuple(x for x in CC.FEATS if x != f)
        Wl = stitched(P, folds, chosen, lambda p, prm: mod.weights(p, prm, feats=rest))
        _, rl = run_slice(P, Wl, a, b)
        Ws = stitched(P, folds, chosen, lambda p, prm: mod.weights(p, dict(prm, feats=(f,))))
        _, rs = run_slice(P, Ws, a, b)
        dl = S.run_weights(P, mod.weights(P, frozen, feats=rest))
        ds = S.run_weights(P, mod.weights(P, dict(frozen, feats=(f,))))
        feat_diag[f] = {"oos_without": summ(rl), "oos_alone": summ(rs),
                        "dev_frozen_without": summ(dl), "dev_frozen_alone": summ(ds)}
        print(name, f, feat_diag[f]["oos_without"]["sharpe"], feat_diag[f]["oos_alone"]["sharpe"], flush=True)
    feat_diag["ALL"] = {"oos": summ(r0), "dev_frozen": summ(rfro)}

    # ---- stops / caps
    Wn = stitched(P, folds, chosen, lambda p, prm: mod.weights(p, prm, k_stop=0))
    _, rn = run_slice(P, Wn, a, b)
    dn = S.run_weights(P, mod.weights(P, frozen, k_stop=0))
    stop_effect = {"oos_with_stops": summ(r0), "oos_no_stops": summ(rn),
                   "dev_frozen_with_stops": summ(rfro), "dev_frozen_no_stops": summ(dn),
                   "worst_trade_no_stops_dev": _f(float(dn.trades.df()["ret"].min())) if len(dn.trades.df()) else None,
                   "worst_trade_with_stops_dev": _f(float(rfro.trades.df()["ret"].min())) if len(rfro.trades.df()) else None,
                   "stop_fill_correction_dev_frozen": stop_corr_dev,
                   "stop_fill_correction_oos": stop_corr_oos,
                   "worst_trade_equity_frac_dev_with_stops": worst_eq(rfro), "worst_trade_equity_frac_dev_no_stops": worst_eq(dn),
                   "worst_trade_equity_frac_oos_with_stops": worst_eq(r0), "worst_trade_equity_frac_oos_no_stops": worst_eq(rn),
                   "k_stop": mod.K_STOP, "stop_max_dist": CC.STOP_MAX, "name_cap": mod.NAME_CAP,
                   "note": "lab exits a stopped name at the next 6h open; correction = what a resting stop at the "
                           "stop price (or the open on a gap) would have changed, qty from the simulated account"}
    if name == "crowd_xs53":
        dc = S.run_weights(P, mod.weights(P, frozen, cap=0))
        dnc = S.run_weights(P, mod.weights(P, frozen, cap=0, k_stop=0))
        stop_effect["dev_frozen_no_cap"] = summ(dc)
        stop_effect["dev_frozen_no_cap_no_stops"] = summ(dnc)

    # ---- robustness (dev, frozen)
    wfz = mod.weights(P, frozen)
    lag = np.vstack([np.zeros((1, wfz.shape[1])), wfz[:-1]])
    rob = {"double_fee_dev": summ(S.run_weights(P, wfz, fee=0.0011)),
           "triple_slippage_dev": summ(S.run_weights(P, wfz, slippage_bps=np.where(
               np.isin(P.symbols, ["BTCUSDT", "ETHUSDT"]), 3.0, np.where(np.isin(P.symbols, CC.data.MAJORS), 9.0, 24.0)))),
           "extra_6h_lag_dev": summ(S.run_weights(P, lag)),
           "no_funding_dev": summ(S.run_weights(P, wfz, funding=False)),
           "base_dev": summ(rfro)}
    out["robustness_dev_frozen"] = rob
    if name == "crowd_xs53":
        wl, ws = np.where(wfz > 0, wfz, 0.0), np.where(wfz < 0, wfz, 0.0)
        out["leg_split_dev"] = {"long_leg": summ(S.run_weights(P, wl)), "short_leg": summ(S.run_weights(P, ws))}
    else:
        net = wfz.sum(1)
        out["net_exposure_dev"] = {"mean": _f(net.mean()), "mean_abs": _f(np.abs(net).mean()),
                                   "mean_gross": _f(np.abs(wfz).sum(1).mean()),
                                   "share_bars_active": _f(float((np.abs(wfz).sum(1) > 0).mean()))}

    # ---- decay, correlation, concentration
    dser = daily_rets(rfro)
    oser = daily_rets(r0)
    out["dev_frozen_by_year"] = by_year_from_daily(dser.index, dser.values)
    out["oos_by_year_incl_2025H1"] = by_year_from_daily(oser.index, oser.values)
    out["correlation_to"] = corr_block(dser, oser, P)
    out["pnl_concentration_oos"] = pnl_concentration(r0)
    out["pnl_concentration_dev_frozen"] = pnl_concentration(rfro)
    out["feature_diagnostics"] = feat_diag
    out["feature_correlations_pooled"] = feature_corrs(P)
    out["stop_effect"] = stop_effect
    out["max_gross_oos"] = _f(float(np.max(r0.gross_leverage)), 3)
    out["n_liquidations_oos"] = int(r0.n_liquidations)
    out["eligible_coins_per_bar_by_year"] = elig_by_year(P)
    v, cav = HX.default_verdict(out)
    out["verdict"] = v
    out["caveats"] = list(dict.fromkeys(list(getattr(mod, "CAVEATS", [])) + cav))
    out["verdict_rule"] = HX.default_verdict.__doc__
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HX.RESULTS, f"{name}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=HX._json_default)
    om = out["wf"]["oos_metrics"]
    print(name, "DONE", v, om.get("sharpe"), om.get("cagr"), om.get("max_drawdown"), out["verdict_inputs"], flush=True)
    return out


def feature_corrs(P):
    F = CC.features(P)
    st = {f: CC.signed(F, f, 1.0) for f in CC.FEATS}
    df = pd.DataFrame({f: st[f][F["elig"]] for f in CC.FEATS})
    return {"note": "pooled over eligible coin-bars, oi with +1 sign", "corr": df.corr().round(3).to_dict(),
            "availability": df.notna().mean().round(3).to_dict()}


def elig_by_year(P):
    F = CC.features(P)
    yr = pd.to_datetime(P.t, unit="s").year
    return {int(k): round(float(v), 1) for k, v in pd.Series(F["elig"].sum(1)).groupby(yr).mean().items()}


if __name__ == "__main__":
    main(sys.argv[1], null_n=int(sys.argv[2]) if len(sys.argv) > 2 else 200)
