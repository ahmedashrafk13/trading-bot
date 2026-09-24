"""Runner: python backtest/lab/strategies/_evt_run.py <module> [null_n] [family_trials]"""
import importlib, json, os, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import sim as S, wf  # noqa: E402
from lab.strategies import _evt_harness as H  # noqa: E402

name = sys.argv[1]
null_n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
fam = int(sys.argv[3]) if len(sys.argv) > 3 else None
mod = importlib.import_module(f"lab.strategies.{name}")


def extra(P, oos, rfro, out):
    a = out["wf"]["folds"][0]
    ia = int(np.searchsorted(P.t, np.datetime64(a["test"][0]).astype("datetime64[s]").astype(np.int64)))
    x = {}
    tr = oos.trades.df()
    closed = tr[~tr["is_open"]]
    # stop / time exits: a trade that closed before its time stop was stopped (or data ended)
    hold_bars = (closed["close_bar"] - closed["open_bar"]).to_numpy()
    x["exit_mix_oos"] = {"share_closed_before_min_time_stop": H._fmt(float(np.mean(hold_bars < min(g.get("H", 3) for g in mod.GRID) * 4)))}
    sub = S.slice_panel(P, ia, ia + len(oos.t))
    try:
        x["btc_hedge_overlay_oos"] = H.hedge_overlay(sub, oos, beta=1.0)
        x["btc_hedge_overlay_frozen_dev"] = H.hedge_overlay(P, rfro, beta=1.0)
    except Exception as e:  # noqa: BLE001
        x["btc_hedge_overlay_error"] = repr(e)
    if hasattr(mod, "extra_report"):
        x.update(mod.extra_report(P, oos, rfro, out))
    return x


t0 = time.time()
out = H.evaluate(mod, null_n=null_n, family_trials=fam, extra=extra)
om = out["wf"]["oos_metrics"]
print(json.dumps({k: out[k] for k in ("frozen", "verdict", "oos_events", "deflated_sharpe", "trades_per_day", "win_rate",
                                       "payoff", "worst_trade", "correlation_to", "robustness_dev_frozen")}, default=str))
print("OOS", {k: om.get(k) for k in ("sharpe", "cagr", "max_drawdown", "vol_annual", "n_trades", "fee_drag_per_year", "funding_per_year")})
print("by_year", out["wf"]["oos_by_year"])
print("null", out["null"])
print("folds", [(f["test"][0][:10], f["chosen"], f["test_metrics"]["sharpe"]) for f in out["wf"]["folds"]])
print("sens", [(s["param"], s["value"], s["oos_or_dev_sharpe"]) for s in out["sensitivity"]])
print("hedge", out.get("btc_hedge_overlay_oos"))
print("impl", out["implementability_200"])
print("trade_stats", json.dumps(out["trade_stats_oos"], default=str))
print("caveats", out["caveats"])
print("runtime", round(time.time() - t0, 1))
