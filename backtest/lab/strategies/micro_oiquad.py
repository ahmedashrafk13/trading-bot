"""micro_oiquad - open-interest x price quadrant on the 12 metrics majors (family E, signal b).

Screen (results/_screen_bc.json, quadrant):
  * time-series, pooled Driscoll-Kraay: fwd ~ r24 + r24*1[dOI24<0] + 1[dOI24>0] + r7d. The interaction
    (a 24h move made while OI FELL reverses relative to one made on rising OI) has t -1.24/-1.70 (6h),
    -1.18/-0.84 (24h), -1.36/-2.18 (72h) train/test: passes the gate ONLY at 72h.
  * cross-sectional FM, rank(r24*sign(dOI24)) next to rank(r24), rank(dOI24), rank(r7d):
    t -0.74/-2.51 (6h), -2.59/-2.16 (24h), -1.90/-1.34 (72h).
  The OI FLUSH reversal (1h dOI <= -3 sigma) FAILED (see results/micro_oiflush.json).
Rules (decided at each 6h close, metrics knowable at the close incl. 5-min lag):
  mode "ts": s_j = -sign(r24_j) when dOI24_j <= -thr * sigma30d(dOI24_j) and |r24_j| >= rmin * sigma30d(r24_j),
             else 0; per-coin inverse vol, net exposure allowed.
  mode "xs": score = -rank(r24 * sign(dOI24)); long top 3 / short bottom 3.
Overlapping hold of H bars; book vol-targeted to params["vol_target"].
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402

NAME = "micro_oiquad"
DESCRIPTION = ("12 Binance-metrics majors: fade 24h moves made on FALLING open interest (short covering / "
               "long liquidation) - time-series and cross-sectional variants, 6h decisions, vol-targeted.")
MECHANISM = ("A price move carried by positions CLOSING (OI down) is forced/one-off flow with no new "
             "conviction behind it and tends to give back; a move on OPENING positions (OI up) carries "
             "information and persists.")
PANEL = dict(timeframe="6h", symbols=list(data.MAJORS[:12]), start="2021-12-01")
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False

GRID = []
for H in (4, 12):
    for thr in (0.0, 1.0):
        for rmin in (0.0, 1.0):
            GRID.append(dict(mode="ts", H=H, thr=thr, rmin=rmin, vol_target=0.20))
for H in (4, 12):
    GRID.append(dict(mode="xs", H=H, thr=0.0, rmin=0.0, vol_target=0.20))
FROZEN = dict(mode="ts", H=4, thr=1.0, rmin=0.0, vol_target=0.20)   # stability pick, see results/micro_oiquad.json

CAVEATS = [
    "Metrics from 2021-12: 365d training windows, OOS starts 2022-12.",
    "The TS interaction passed the gate at 72h only (train |t| 1.36); the XS form at 6h/24h. Weak, multiple-tested evidence.",
    "Live OI: Bybit tickers openInterestValue (venue differs from the Binance history used here).",
]


def _feats(panel, metrics):
    m = HX.get_metrics(panel, metrics)
    lc = np.log(panel.c)
    with np.errstate(invalid="ignore", divide="ignore"):
        loi = np.log(m["oi_value"])
    r24 = np.full_like(lc, np.nan)
    r24[4:] = lc[4:] - lc[:-4]
    d24 = np.full_like(loi, np.nan)
    d24[4:] = loi[4:] - loi[:-4]
    sr = pd.DataFrame(r24).rolling(120, min_periods=60).std().to_numpy()
    so = pd.DataFrame(d24).rolling(120, min_periods=60).std().to_numpy()
    return r24, d24, sr, so


def weights(panel, params, metrics=None):
    r24, d24, sr, so = _feats(panel, metrics)
    tgt = float(params.get("vol_target", 0.20))
    if params.get("mode", "ts") == "ts":
        thr, rmin = float(params.get("thr", 0.0)), float(params.get("rmin", 0.0))
        with np.errstate(invalid="ignore"):
            cond = (d24 <= -thr * so) & (d24 < 0) & (np.abs(r24) >= rmin * sr)
        s = np.where(cond, -np.sign(r24), 0.0)
        s = np.nan_to_num(s)
        s[~panel.tradable] = 0.0
        s = HX.stagger(s, int(params.get("H", 12)))
        vol = HX.asset_vol(panel, 120)
        with np.errstate(invalid="ignore", divide="ignore"):
            raw = np.where(np.isfinite(vol) & (vol > 0), s / vol, 0.0) / panel.c.shape[1]
    else:
        x = r24 * np.sign(d24)
        x[~panel.tradable] = np.nan
        sc = -HX.cs_rank(x, min_n=6)
        raw = HX.stagger(HX.xs_longshort(sc, 0.25, min_n=6), int(params.get("H", 4)))
    w = HX.vol_scale_book(panel, raw, tgt, lb=120, cap=3.0)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params, metrics)
    tg = {panel.symbols[j]: float(w[-1, j]) for j in np.flatnonzero(w[-1] != 0)}
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "targets": tg, "orders": "market orders to target notional/equity at the 6h run; no resting orders"}


def run(null_n=200):
    # family trials: quadrant screen (3 TS + 3 XS stats x 3 horizons = 18) + this grid
    return HX.evaluate(sys.modules[__name__], train_days=365, null_n=null_n, family_trials=18 + len(GRID),
                       extra={"screen": "results/_screen_bc.json (quadrant)"})


if __name__ == "__main__":
    o = run()
    print({k: o[k] for k in ("frozen", "verdict", "deflated_sharpe", "trades_per_day")})
    print(o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"), o["wf"]["oos_metrics"].get("max_drawdown"))
    print(o["null"]); print(o["null_secondary"])
    print(o["wf"]["oos_by_year"])
