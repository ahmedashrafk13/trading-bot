"""micro_topxs - cross-sectional contrarian to the TOP-TRADER long/short ratio, 12 metrics majors (family E, signal c).

Screen (results/_screen_bc.json, crowding, 'minus_zT', Fama-MacBeth on ranks with rank(r24), rank(r7d)
controls): train/test t 0.48 / 3.61 (6h), 0.19 / 3.11 (24h), 0.87 / 2.68 (72h). Same sign, test |t|>=2,
so it passes the family gate - but the TRAIN half is flat (the top-trader ratio is NaN for most of 2022,
so 'train' is essentially 2021-12 + 2023) and the pooled time-series version is the wrong sign. Treat as
weak prior.

Signal at each 6h close: zT = 30d z of ln(top-trader L/S) per coin; score = -zT, residualised per row
on rank(r24), rank(r7d) (resid="cs") or raw rank (resid="none"); long top 3 / short bottom 3 of the
available names (q=0.25), overlapping hold H bars, book vol-targeted.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _micro_stats as ST  # noqa: E402

NAME = "micro_topxs"
DESCRIPTION = ("12 Binance-metrics majors, cross-sectional long/short against the coins where top "
               "accounts are most crowded long (30d z of top-trader L/S), 6h decisions, vol-targeted.")
MECHANISM = ("Where the largest accounts have piled into longs relative to their own history, "
             "the marginal buyer is exhausted and the positioning must unwind; relative to other majors "
             "those coins underperform.")
PANEL = dict(timeframe="6h", symbols=list(data.MAJORS[:12]), start="2021-12-01")
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False

GRID = []
for resid in ("cs", "none"):
    for H in (1, 4, 12):
        GRID.append(dict(resid=resid, H=H, q=0.25, vol_target=0.20))
FROZEN = dict(resid="none", H=12, q=0.25, vol_target=0.20)   # stability pick, see results/micro_topxs.json

CAVEATS = [
    "Top-trader ratio missing for most of 2022 -> no positions then; walk-forward training windows that fall in 2022 are empty.",
    "Screen train-half t was 0.2-0.9: the gate passed on the test half only.",
    "Live needs Binance public fapi topLongShortPositionRatio (Bybit has no top-trader ratio).",
]


def score(panel, metrics, params):
    m = HX.get_metrics(panel, metrics)
    with np.errstate(invalid="ignore", divide="ignore"):
        lnT = np.log(m["top_ls_ratio"])
    s = -ST.roll_z(lnT, 120, 60)
    s[~panel.tradable] = np.nan
    rs = HX.cs_rank(s, min_n=6)
    if params.get("resid", "cs") != "cs":
        return rs
    lc = np.log(panel.c)
    r24 = np.full_like(lc, np.nan)
    r24[4:] = lc[4:] - lc[:-4]
    r7 = np.full_like(lc, np.nan)
    r7[28:] = lc[28:] - lc[:-28]
    return HX.cs_resid(rs, [HX.cs_rank(r24, 6), HX.cs_rank(r7, 6)], min_n=6)


def weights(panel, params, metrics=None):
    sc = score(panel, metrics, params)
    w = HX.xs_longshort(sc, float(params.get("q", 0.25)), min_n=6)
    w = HX.stagger(w, int(params.get("H", 4)))
    w = HX.vol_scale_book(panel, w, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params, metrics)
    tg = {panel.symbols[j]: float(w[-1, j]) for j in np.flatnonzero(w[-1] != 0)}
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "targets": tg, "orders": "market orders to target notional/equity at the 6h run; no resting orders"}


def run(null_n=200):
    return HX.evaluate(sys.modules[__name__], train_days=365, null_n=null_n, family_trials=24 + len(GRID),
                       extra={"screen": "results/_screen_bc.json (crowding minus_zT, XS)"})


if __name__ == "__main__":
    o = run()
    print({k: o[k] for k in ("frozen", "verdict", "deflated_sharpe", "trades_per_day")})
    print(o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"), o["wf"]["oos_metrics"].get("max_drawdown"))
    print(o["null"]); print(o["null_secondary"])
    print(o["wf"]["oos_by_year"])
