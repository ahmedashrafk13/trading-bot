"""Evaluation harness for the family-G event modules (evt_*.py, KIND = "events").

evaluate(mod) on DEV data only (panel end 2025-06-30; walk_forward cuts at the lockbox anyway):
  * wf.walk_forward(kind="events") over mod.GRID (rolling), stitched OOS result
  * matched nulls on the stitched OOS entries (mod.null_pool: random other coin at the same bar,
    same side/size/stop/time stop; and a per-event sign flip) - both re-simulated with costs
  * FROZEN (stability pick across folds) run over the whole dev period -> daily returns
  * +/-1 grid-step sensitivity around FROZEN (dev, in-sample), 2x-fee robustness
  * $200 implementability: run_events(round_to_qty=True, Bybit instruments) + Bybit launchTime check
  * causality: wf._guard_causal on 6 random cuts of the dev panel for FROZEN
  * trade statistics (hit rate, payoff, worst trade, funding paid / received separately, events per year)
  * correlation to micro_crowd / micro_flowxs (their frozen_dev_daily) and BTC (daily close returns)
The panel convention for event modules: meta["entry_ok"] = the PIT-universe tradable mask (entries
need it); if mod.HOLD_WHEN_NOT_MEMBER, panel.tradable = valid bars (a held coin that drops out of
the universe is not force-closed).
"""
from __future__ import annotations

import collections
import json
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data, metrics as M, sim as S, wf  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402

DEV_END = "2025-06-30"
RESULTS = os.path.join(os.path.dirname(HERE), "results")
_fmt = HX._fmt
LAST: dict = {}      # evaluate() leaves P, stitched OOS entries, a, b, sim kwargs here for extra reports


def load_for(mod, end=DEV_END):
    kw = dict(mod.PANEL)
    tf = kw.pop("timeframe")
    kw["end"] = end
    p = data.load_panel(tf, **kw)
    p.meta["entry_ok"] = p.tradable.copy()
    if getattr(mod, "HOLD_WHEN_NOT_MEMBER", True):
        p.tradable = p.meta["valid"].copy()
    if getattr(mod, "USES_METRICS", False):
        p.meta["metrics"] = data.load_metrics(p.symbols, tf, start=kw.get("start"), end=end)
    return wf.pre_lockbox(p)


def _sim_kw(mod, extra=None):
    kw = {"max_concurrent": getattr(mod, "MAX_CONCURRENT", 25)}
    kw.update(extra or {})
    return kw


def _run(P, entries, a, b, kw, exits=None):
    sig = {"entries": entries, "exits": exits}
    return wf._run_slice(P, sig, a, b, "events", kw, record=True)


def _sharpe(res):
    return M.equity_metrics(res.t, res.dt, res.equity, res.initial_equity)["sharpe"]


def _daily_ret_series(res):
    keys, eq = M.daily_equity(res.t, res.dt, res.equity, res.initial_equity)
    keys = np.asarray(keys, np.int64)
    r = np.asarray(eq[1:], float) / np.asarray(eq[:-1], float) - 1
    idx = pd.to_datetime(keys * 86400, unit="s").strftime("%Y-%m-%d")
    return pd.Series(r, index=idx)


def _corr_to(res_daily, P):
    out = {}
    for name in ("micro_crowd", "micro_flowxs"):
        try:
            d = json.load(open(os.path.join(RESULTS, f"{name}.json")))
            s = pd.Series(d["frozen_dev_daily"]["returns"], index=d["frozen_dev_daily"]["dates"])
            j = pd.concat([res_daily, s], axis=1, join="inner").dropna()
            out[name] = _fmt(j.iloc[:, 0].corr(j.iloc[:, 1]), 3)
            out[name + "_n_days"] = int(len(j))
        except Exception as e:           # noqa: BLE001
            out[name] = None
            out[name + "_error"] = str(e)
    bj = P.symbols.index("BTCUSDT")
    day = (np.asarray(P.t, np.int64) + P.dt) // 86400 - 1     # bar closing at 00:00 -> previous day
    c = pd.Series(P.c[:, bj], index=day).groupby(level=0).last()
    rb = c.pct_change().dropna()
    rb.index = pd.to_datetime(rb.index.to_numpy() * 86400, unit="s").strftime("%Y-%m-%d")
    j = pd.concat([res_daily, rb], axis=1, join="inner").dropna()
    out["btc"] = _fmt(j.iloc[:, 0].corr(j.iloc[:, 1]), 3)
    out["basis"] = "Pearson of daily returns: FROZEN dev-period run vs the other modules' frozen_dev_daily, and BTC close-to-close"
    return out


def _trade_stats(res, P):
    tr = res.trades.df()
    closed = tr[~tr["is_open"]] if len(tr) else tr
    o = {}
    if not len(closed):
        return {"n_closed": 0}
    wins, losses = closed[closed["pnl"] > 0], closed[closed["pnl"] <= 0]
    o["n_closed"] = int(len(closed))
    o["win_rate"] = _fmt(len(wins) / len(closed))
    o["payoff"] = _fmt(wins["ret"].mean() / abs(losses["ret"].mean())) if len(wins) and len(losses) else None
    o["expectancy_ret_on_notional"] = _fmt(closed["ret"].mean())
    o["median_ret_on_notional"] = _fmt(closed["ret"].median())
    o["expectancy_usd"] = _fmt(closed["pnl"].mean())
    o["worst_trade_ret"] = _fmt(closed["ret"].min())
    o["best_trade_ret"] = _fmt(closed["ret"].max())
    w = closed.loc[closed["ret"].idxmin()]
    o["worst_trade"] = {"symbol": str(w["symbol"]), "open": str(pd.to_datetime(int(w["open_t"]), unit="s")),
                        "ret": _fmt(w["ret"]), "pnl_usd": _fmt(w["pnl"])}
    f = closed["funding"]
    o["funding_paid_usd"] = _fmt(f[f > 0].sum())
    o["funding_received_usd"] = _fmt(-f[f < 0].sum())
    o["funding_net_usd_(+=paid)"] = _fmt(f.sum())
    o["fees_usd"] = _fmt(closed["fees"].sum())
    o["pnl_usd"] = _fmt(closed["pnl"].sum())
    hold = (closed["close_bar"] - closed["open_bar"]) * P.dt / 3600.0
    o["avg_hold_hours"] = _fmt(hold.mean(), 1)
    yrs = pd.to_datetime(tr["open_t"], unit="s").dt.year
    o["events_opened_per_year"] = {int(k): int(v) for k, v in yrs.value_counts().sort_index().items()}
    g = closed.assign(y=pd.to_datetime(closed["open_t"], unit="s").dt.year).groupby("y")
    o["by_year_trades"] = {int(k): {"n": int(len(v)), "win_rate": _fmt((v["pnl"] > 0).mean()),
                                    "mean_ret": _fmt(v["ret"].mean()), "pnl_usd": _fmt(v["pnl"].sum())}
                           for k, v in g}
    top = closed.groupby("symbol")["pnl"].sum().sort_values()
    o["pnl_top5_symbols_usd"] = {k: _fmt(v) for k, v in top.tail(5).items()}
    o["pnl_bottom5_symbols_usd"] = {k: _fmt(v) for k, v in top.head(5).items()}
    tot = closed["pnl"].sum()
    o["top5_share_of_pnl"] = _fmt(top.tail(5).sum() / tot) if tot > 0 else None
    return o


def _nulls(P, mod, entries, a, b, kw, n, seed=0, exits=None):
    rng = np.random.default_rng(seed)
    base = _sharpe(_run(P, entries, a, b, kw, exits))
    out = {"strategy_sharpe": _fmt(base, 4)}
    pool = mod.null_pool(P) if hasattr(mod, "null_pool") else None
    kinds = []
    if pool is not None:
        kinds.append("random_coin")
    kinds.append("sign_flip")
    for kind in kinds:
        vals = []
        for k in range(n):
            ne = []
            for e in entries:
                e2 = dict(e)
                if kind == "random_coin":
                    cand = np.flatnonzero(pool[e["i"]])
                    cand = cand[cand != e["j"]]
                    if not len(cand):
                        continue
                    e2["j"] = int(rng.choice(cand))
                else:
                    if rng.random() < 0.5:
                        e2["side"] = -e["side"]
                ne.append(e2)
            vals.append(_sharpe(_run(P, ne, a, b, kw, exits)))
        vals = np.asarray(vals, float)
        vals = vals[np.isfinite(vals)]
        out[kind] = {"n": int(len(vals)), "null_median": _fmt(np.median(vals)), "null_p95": _fmt(np.percentile(vals, 95)),
                     "p_value": _fmt((1 + (vals >= base).sum()) / (len(vals) + 1)),
                     "percentile": _fmt((vals < base).mean() * 100, 1)}
    out["kind"] = ("random_coin = same OOS entry bars/side/size/stop/time stop on a random coin from mod.null_pool "
                   "(see module docstring); sign_flip = each OOS event's side flipped with p=1/2. Re-simulated with costs.")
    return out


def _implementability(P, entries, a, b, kw, exits=None):
    ins = data.load_bybit_instruments()
    res = _run(P, entries, a, b, dict(kw, instruments=ins, round_to_qty=True), exits)
    m = res.metrics()
    rej = collections.Counter(x["reason"] for x in res.rejected)
    listed_at = []
    for e in entries:
        if not (a <= e["i"] < b - 1):
            continue
        s = P.symbols[e["j"]]
        lt = (ins.get(s) or {}).get("launchTime")
        listed_at.append(bool(lt is not None and int(lt) <= int(P.t[e["i"]]) + P.dt))
    return {"metrics": {k: _fmt(m.get(k)) for k in ("cagr", "sharpe", "max_drawdown", "total_return", "final_equity",
                                                  "n_trades", "fee_drag_per_year", "funding_per_year", "exposure")},
            "rejected": dict(rej),
            "bybit_listed_at_entry_share": _fmt(np.mean(listed_at)) if listed_at else None,
            "note": "run_events(round_to_qty=True, instruments=Bybit snapshot) on the stitched OOS entries. Symbols "
                    "missing from the Bybit snapshot (mostly delisted) are NOT rounded/dropped. "
                    "bybit_listed_at_entry_share = share of OOS entries whose symbol is in today's Bybit list with "
                    "launchTime <= the decision close (lower bound on historical availability)."}


def _by_year(oos):
    dates, eq = HX._to_dates(M.daily_equity(oos.t, oos.dt, oos.equity, oos.initial_equity))
    s_eq = pd.Series(eq[1:], index=pd.to_datetime(dates[1:]))
    prev, out = float(oos.initial_equity), {}
    for y, g in s_eq.groupby(s_eq.index.year):
        rr = np.r_[g.iloc[0] / prev - 1, g.pct_change().dropna().to_numpy()]
        out[int(y)] = {"return": _fmt(g.iloc[-1] / prev - 1),
                       "sharpe": _fmt(rr.mean() / rr.std(ddof=1) * np.sqrt(365) if rr.std(ddof=1) > 0 else np.nan, 3),
                       "maxdd": _fmt(float((g / g.cummax() - 1).min()))}
        prev = float(g.iloc[-1])
    return out, dates, eq


def hedge_overlay(Psub, res, beta=1.0):
    """BTC long overlay = beta x the book's net SHORT notional / equity (long books get a BTC short),
    decided at each close and filled next open (run_weights on BTC).  Psub must be the panel slice
    the Result `res` was simulated on.  Returned as combined daily returns r_events + r_hedge (two
    sub-accounts on the same capital base; an approximation)."""
    bj = Psub.symbols.index("BTCUSDT")
    pos = res.positions
    net = (pos * np.nan_to_num(Psub.c)).sum(1)
    w_btc = np.clip(-beta * net / np.maximum(res.equity, 1e-9), -5, 5)
    sel = [bj]
    sub = data.Panel(t=Psub.t, dt=Psub.dt, symbols=["BTCUSDT"], o=Psub.o[:, sel], h=Psub.h[:, sel], l=Psub.l[:, sel],
                     c=Psub.c[:, sel], v=Psub.v[:, sel], qv=Psub.qv[:, sel], funding=Psub.funding[:, sel],
                     tradable=Psub.meta["valid"][:, sel], meta={})
    rh = S.run_weights(sub, w_btc[:, None], min_trade_frac=0.02)
    r1, r2 = _daily_ret_series(res), _daily_ret_series(rh)
    j = pd.concat([r1, r2], axis=1, join="inner").fillna(0.0)
    comb = j.iloc[:, 0] + j.iloc[:, 1]
    eq = 200.0 * np.cumprod(1 + comb.to_numpy())
    m = M.equity_metrics(np.arange(len(eq)) * 86400, 86400, eq, 200.0)
    return {"beta": beta, "sharpe": _fmt(m["sharpe"], 3), "cagr": _fmt(m["cagr"]), "max_drawdown": _fmt(m["max_drawdown"]),
            "vol": _fmt(m["vol_annual"]), "by_year": {int(y): _fmt(float(np.prod(1 + g) - 1))
                                                       for y, g in comb.groupby(pd.to_datetime(comb.index).year)},
            "hedge_fees_usd": _fmt(rh.fees_paid + rh.slippage_paid), "hedge_funding_paid_usd": _fmt(rh.funding_paid),
            "note": "approximation: hedge sized on the event book equity, simulated as a separate BTC sub-account"}


def hedged_nulls(P, mod, entries, a, b, kw, n, seed=1, beta=1.0, exits=None):
    """Same two nulls as _nulls, but every simulation gets the BTC hedge overlay before its Sharpe is taken."""
    rng = np.random.default_rng(seed)
    sub = S.slice_panel(P, a, b)
    base = hedge_overlay(sub, _run(P, entries, a, b, kw, exits), beta)["sharpe"]
    pool = mod.null_pool(P) if hasattr(mod, "null_pool") else None
    out = {"strategy_sharpe": base}
    for kind in (["random_coin"] if pool is not None else []) + ["sign_flip"]:
        vals = []
        for k in range(n):
            ne = []
            for e in entries:
                e2 = dict(e)
                if kind == "random_coin":
                    cand = np.flatnonzero(pool[e["i"]])
                    cand = cand[cand != e["j"]]
                    if not len(cand):
                        continue
                    e2["j"] = int(rng.choice(cand))
                elif rng.random() < 0.5:
                    e2["side"] = -e["side"]
                ne.append(e2)
            vals.append(hedge_overlay(sub, _run(P, ne, a, b, kw, exits), beta)["sharpe"])
        vals = np.asarray([v for v in vals if v is not None and np.isfinite(v)], float)
        out[kind] = {"n": int(len(vals)), "null_median": _fmt(np.median(vals)), "null_p95": _fmt(np.percentile(vals, 95)),
                     "p_value": _fmt((1 + (vals >= base).sum()) / (len(vals) + 1))}
    return out


def evaluate(mod, *, train_days=730, test_days=182, step_days=182, null_n=200, family_trials=None,
             extra=None, write=True, panel=None, min_oos_events=100):
    t0 = time.time()
    P = panel if panel is not None else load_for(mod)
    kw = _sim_kw(mod)
    fn = lambda p, prm: mod.events(p, prm)          # noqa: E731
    res = wf.walk_forward(P, fn, mod.GRID, train_days=train_days, test_days=test_days, step_days=step_days,
                          objective="sharpe", mode="rolling", kind="events", sim_kwargs=kw, causality_checks=2)
    oos, om, folds = res["oos_result"], res["oos_metrics"], res["folds"]
    a, b = folds[0]["bars"][1], folds[-1]["bars"][2]
    # stitched OOS entries (chosen params per fold), exactly as walk_forward built them
    ents = []
    EX, has_ex = np.zeros((len(P.t), len(P.symbols)), bool), False
    for fi in folds:
        _, ib, ic = fi["bars"]
        sig = wf._call(fn, S.slice_panel(P, 0, ic), fi["params"], "events")
        ents.extend(e for e in sig["entries"] if ib <= e["i"] < ic)
        if sig.get("exits") is not None:
            EX[ib:ic] = np.asarray(sig["exits"], bool)[ib:ic]
            has_ex = True
    EX = EX if has_ex else None
    chk = _run(P, ents, a, b, kw, EX)
    LAST.update(P=P, ents=ents, a=a, b=b, kw=kw, exits=EX)
    null = _nulls(P, mod, ents, a, b, kw, null_n, exits=EX)
    # FROZEN
    k0, med_rank, mean_sc = HX._sel_frozen(mod.GRID, res["scores"])
    frozen = mod.GRID[k0]
    efro = wf._call(fn, P, frozen, "events")
    rfro = _run(P, efro["entries"], 0, len(P.t), kw, efro.get("exits"))
    fm = rfro.metrics()
    dfro = _daily_ret_series(rfro)
    sens = []
    for key, v, g in HX._neighbours(mod.GRID, k0):
        sg = wf._call(fn, P, g, "events")
        rr = _run(P, sg["entries"], 0, len(P.t), kw, sg.get("exits"))
        mm = M.equity_metrics(rr.t, rr.dt, rr.equity, rr.initial_equity)
        sens.append({"param": key, "value": v, "oos_or_dev_sharpe": _fmt(mm["sharpe"], 3), "cagr": _fmt(mm["cagr"]),
                     "maxdd": _fmt(mm["max_drawdown"]), "basis": "dev (in-sample)"})
    sens.append({"param": "FROZEN", "value": json.dumps(frozen), "oos_or_dev_sharpe": _fmt(fm["sharpe"], 3),
                 "cagr": _fmt(fm["cagr"]), "maxdd": _fmt(fm["max_drawdown"]), "basis": "dev (in-sample)"})
    r2f = _run(P, efro["entries"], 0, len(P.t), dict(kw, fee=2 * S.DEFAULT_FEE), efro.get("exits"))
    r0f = _run(P, efro["entries"], 0, len(P.t), dict(kw, funding=False), efro.get("exits"))
    rob = {"double_fee_dev": {"sharpe": _fmt(_sharpe(r2f), 3)}, "no_funding_dev": {"sharpe": _fmt(_sharpe(r0f), 3)}}
    # causality
    try:
        wf._guard_causal(fn, P, frozen, "events", efro, 0, len(P.t), 6, seed=11)
        caus = {"ok": True, "checks": 6, "method": "wf._guard_causal on the dev panel (entries identical on 6 random cuts)",
                "plus_walk_forward_guard": "passed (causality_checks=2 per fold raised nothing)"}
    except ValueError as e:
        caus = {"ok": False, "error": str(e)}
    impl = _implementability(P, ents, a, b, kw, EX)
    ts = _trade_stats(oos, P)
    by_year, oos_dates, oos_eq = _by_year(oos)
    nd = len(oos_eq)
    fam = family_trials or len(mod.GRID)
    dsr_family = M.deflated_sharpe(om["sharpe"], fam, max(nd, 2), om["skew"], om["kurtosis"])
    corr = _corr_to(dfro, P)
    n_oos_events = int(ts.get("n_closed", 0)) + int(om.get("n_open_trades", 0) or 0)
    out = {
        "name": mod.NAME, "description": mod.DESCRIPTION, "mechanism": mod.MECHANISM,
        "universe": mod.PANEL.get("universe") or mod.PANEL.get("symbols"), "timeframe": mod.PANEL["timeframe"],
        "panel": dict(mod.PANEL, end=DEV_END), "kind": "events", "uses_metrics": bool(getattr(mod, "USES_METRICS", False)),
        "n_trials": len(mod.GRID), "family_trials_incl_screen": fam,
        "grid_summary": {"n": len(mod.GRID), "values": {k: sorted({json.dumps(g[k]) for g in mod.GRID}) for k in mod.GRID[0]},
                         "median_fold_rank": [float(x) for x in med_rank],
                         "mean_train_sharpe": [_fmt(x, 3) for x in mean_sc], "objective": "sharpe"},
        "frozen": frozen,
        "frozen_rule": "config with the best MEDIAN within-fold train rank across walk-forward folds (tie: mean train Sharpe)",
        "wf": {"train_days": train_days, "test_days": test_days, "step_days": step_days, "mode": "rolling",
               "folds": [{"train": [f["train_start"], f["test_start"]], "test": [f["test_start"], f["test_end"]],
                          "chosen": f["params"], "train_score": _fmt(f["train_score"], 3),
                          "test_metrics": {k: _fmt(f["test_metrics"].get(k)) for k in ("sharpe", "cagr", "max_drawdown", "total_return")}}
                         for f in folds],
               "oos_metrics": {k: _fmt(v) for k, v in om.items() if isinstance(v, (int, float, np.floating, np.integer))},
               "oos_by_year": by_year,
               "oos_sharpe_recheck_from_reconstructed_entries": _fmt(_sharpe(chk), 4)},
        "oos_daily": {"dates": oos_dates, "equity": [round(float(x), 4) for x in oos_eq]},
        "frozen_dev_daily": {"dates": list(dfro.index), "returns": [round(float(x), 6) for x in dfro.to_numpy()]},
        "frozen_dev_metrics": {k: _fmt(fm.get(k)) for k in ("sharpe", "cagr", "max_drawdown", "vol_annual", "n_trades", "win_rate",
                                                            "trades_per_week", "avg_hold_hours", "exposure",
                                                            "fee_drag_per_year", "funding_per_year")},
        "null": null,
        "deflated_sharpe": _fmt(om.get("dsr")), "deflated_sharpe_family": _fmt(dsr_family),
        "sensitivity": sens, "robustness_dev_frozen": rob,
        "implementability_200": impl,
        "oos_events": n_oos_events,
        "trade_stats_oos": ts,
        "trades_per_day": _fmt((om.get("trades_per_week") or 0) / 7.0, 3),
        "avg_hold_hours": _fmt(om.get("avg_hold_hours"), 1),
        "win_rate": _fmt(om.get("win_rate")), "payoff": ts.get("payoff"),
        "expectancy_per_trade": ts.get("expectancy_ret_on_notional"),
        "expectancy_units": "mean return on entry notional per closed OOS trade, net of fees+slippage+funding (USD in trade_stats_oos)",
        "worst_trade": ts.get("worst_trade_ret"),
        "exposure": _fmt(om.get("exposure")), "fee_drag_per_year": _fmt(om.get("fee_drag_per_year")),
        "funding_per_year": _fmt(om.get("funding_per_year")),
        "needs_hourly_runs": bool(getattr(mod, "NEEDS_HOURLY_RUNS", False)),
        "causality": caus, "correlation_to": corr, "sim_kwargs": kw,
    }
    if extra:
        out.update(extra(P, oos, rfro, out) if callable(extra) else extra)
    v, cav = verdict(out, min_oos_events)
    out["verdict"] = v
    out["caveats"] = list(getattr(mod, "CAVEATS", [])) + cav
    out["runtime_s"] = round(time.time() - t0, 1)
    if write:
        with open(os.path.join(RESULTS, f"{mod.NAME}.json"), "w") as f:
            json.dump(out, f, indent=1, default=HX._json_default)
    return out


def verdict(o, min_events=100):
    """Family-E rule, applied to the event nulls:
      p_used = the LARGER p of the random_coin and sign_flip nulls.
      promising: OOS Sharpe >= 0.8, p_used <= 0.05, DSR (grid trials) >= 0.9, >= 60% OOS years positive,
                 >= min_events OOS events.
      marginal : OOS Sharpe >= 0.5 and p_used <= 0.10.   fails: otherwise.
      Fragility downgrade (one level): a +/-1 neighbour with negative dev Sharpe, or 2x-fee dev Sharpe < 0.25.
      Fewer than min_events OOS events caps the verdict at marginal."""
    sh = o["wf"]["oos_metrics"].get("sharpe") or 0.0
    ps = [v["p_value"] for k, v in o["null"].items() if isinstance(v, dict) and v.get("p_value") is not None]
    p = max(ps) if ps else 1.0
    dsr = o.get("deflated_sharpe") or 0.0
    yrs = [v.get("return") for v in o["wf"]["oos_by_year"].values() if v.get("return") is not None]
    pos = sum(1 for x in yrs if x > 0) / len(yrs) if yrs else 0.0
    cav = []
    if sh > 2:
        cav.append("OOS Sharpe > 2: presumed bug until hunted")
    if sh >= 0.8 and p <= 0.05 and dsr >= 0.9 and pos >= 0.6:
        v = "promising"
    elif sh >= 0.5 and p <= 0.10:
        v = "marginal"
    else:
        v = "fails"
    why = []
    nb = [x.get("oos_or_dev_sharpe") for x in o.get("sensitivity", []) if x.get("param") != "FROZEN"]
    if any(x is not None and x < 0 for x in nb):
        why.append("a +/-1-step neighbour has negative dev Sharpe")
    rob = o.get("robustness_dev_frozen", {}).get("double_fee_dev", {}).get("sharpe")
    if rob is not None and rob < 0.25:
        why.append(f"dev Sharpe with 2x fees is {rob:.2f}")
    if why:
        v = {"promising": "marginal", "marginal": "fails", "fails": "fails"}[v]
        cav.append("Verdict downgraded for fragility: " + "; ".join(why))
    if o.get("oos_events", 0) < min_events and v == "promising":
        v = "marginal"
        cav.append(f"only {o.get('oos_events')} OOS events (< {min_events}): capped at marginal")
    o["verdict_inputs"] = {"oos_sharpe": sh, "p_used": p, "deflated_sharpe": dsr, "share_years_positive": round(pos, 3),
                           "oos_events": o.get("oos_events"), "fragility": why}
    o["verdict_rule"] = verdict.__doc__
    return v, cav
