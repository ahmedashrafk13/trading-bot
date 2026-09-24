"""micro_flowxs - cross-sectional taker-flow imbalance, residualised CROSS-SECTIONALLY (family E, signal a variant).

POST-HOC VARIANT - read before using. The pre-registered cross-sectional signal (imbalance
residualised per coin in TIME, z-scored, then ranked) FAILED the screen (test-half FM t -0.4..-1.9).
What passed (results/_screen_a.json, xs_pit_top20, 't_fm_rawimb_ctl') was the control regression:
rank(imb_W) in a per-period Fama-MacBeth regression next to rank(r_W) and rank(r7d), i.e. flow
residualised on the same-window return CROSS-SECTIONALLY. Train/test FM t: W24 24h 6.47/2.08,
W24 72h 5.94/3.34, W4 24h 6.18/2.12, W4 72h 5.43/3.15. It keeps the per-coin LEVEL of the taker-buy
share, which the time-series z removes - so part of it may be a persistent coin characteristic.

Signal at each 6h close on the PIT top-20: e = per-row OLS residual of rank(imb24) on rank(r24),
rank(r7d) (resid="cs") or rank(imb24) itself (resid="none"). Long top q, short bottom q, equal weight,
dollar neutral, overlapping hold of H bars, book vol-targeted to params["vol_target"].
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _micro_harness as HX  # noqa: E402

NAME = "micro_flowxs"
DESCRIPTION = ("PIT top-20 perps, cross-sectional long/short on 24h taker-flow imbalance residualised "
               "cross-sectionally on the 24h and 7d return, 6h decisions, overlapping hold, vol-targeted.")
MECHANISM = ("Coins whose takers are net buyers beyond what their own price move explains attract "
             "continued demand (flow persistence / informed flow); the same-window return is controlled "
             "because it reverses at <=1d.")
PANEL = dict(timeframe="6h", universe="pit_top20", start="2020-01-01", with_taker=True)
USES_METRICS = False
KIND = "weights"
NEEDS_HOURLY_RUNS = False

GRID = []
for resid in ("cs", "none"):
    for q in (0.2, 0.33):
        for H in (4, 12, 28):
            GRID.append(dict(resid=resid, q=q, H=H, vol_target=0.20))
FROZEN = dict(resid="none", q=0.2, H=28, vol_target=0.20)   # stability pick, see results/micro_flowxs.json

CAVEATS = [
    "POST-HOC: the pre-registered time-series-residualised XS signal failed; this is the control regression that passed. Family trial count includes the whole screen.",
    "Needs Binance taker-buy volume for ~20 coins live (public fapi klines); Bybit symbol mapping for 1000x tickers.",
    "Long/short alt book: short legs on small caps can squeeze; slippage tier 8 bp for non-majors may be optimistic in stress.",
]


def _features(panel):
    tb = pd.DataFrame(panel.meta["tbqv"])
    qv = pd.DataFrame(panel.qv)
    tbs = tb.rolling(4, min_periods=4).sum().to_numpy()
    qvs = qv.rolling(4, min_periods=4).sum().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        imb = 2.0 * tbs / np.where(qvs > 0, qvs, np.nan) - 1.0
        lc = np.log(panel.c)
    r24 = np.full_like(lc, np.nan)
    r24[4:] = lc[4:] - lc[:-4]
    r7 = np.full_like(lc, np.nan)
    r7[28:] = lc[28:] - lc[:-28]
    rel = panel.meta.get("relisted")
    if rel is not None:
        relwin = pd.DataFrame(np.asarray(rel, float)).rolling(29, min_periods=1).max().to_numpy() > 0
        for a in (imb, r24, r7):
            a[relwin] = np.nan
    trad = panel.tradable
    for a in (imb, r24, r7):
        a[~trad] = np.nan
    return imb, r24, r7


def score(panel, params):
    imb, r24, r7 = _features(panel)
    ri = HX.cs_rank(imb)
    if params.get("resid", "cs") == "cs":
        return HX.cs_resid(ri, [HX.cs_rank(r24), HX.cs_rank(r7)])
    return ri


def weights(panel, params, metrics=None):
    sc = score(panel, params)
    w = HX.xs_longshort(sc, float(params.get("q", 0.2)))
    w = HX.stagger(w, int(params.get("H", 12)))
    w = HX.vol_scale_book(panel, w, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params)
    tg = {panel.symbols[j]: float(w[-1, j]) for j in np.flatnonzero(w[-1] != 0)}
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "targets": tg, "orders": "market orders to move each perp to target notional/equity at the 6h run; no resting orders"}


def run(null_n=100):
    # family trials: whole screen (a) = TS 24 cells + XS 12 cells x 3 statistics, plus this grid
    return HX.evaluate(sys.modules[__name__], null_n=null_n, family_trials=60 + len(GRID),
                       extra={"screen": "results/_screen_a.json (xs_pit_top20, t_fm_rawimb_ctl)",
                              "post_hoc_variant": True})


if __name__ == "__main__":
    o = run()
    print({k: o[k] for k in ("frozen", "verdict", "deflated_sharpe", "trades_per_day")})
    print(o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"), o["wf"]["oos_metrics"].get("max_drawdown"))
    print(o["null"]); print(o["null_secondary"])
    print(o["wf"]["oos_by_year"])
