"""micro_crowd - time-series contrarian positioning on the 12 metrics majors (family E, signal c).

Binance 5-min metrics (load_metrics, value knowable at the 6h close incl. a 5-min publication lag):
  zG = 30d (120 x 6h) z-score of ln(global long/short ACCOUNT ratio)
  zT = same for the top-trader long/short ratio (NaN for most of 2022 in the archive)
  D  = zT - zG   (large accounts relative to the crowd)
Signals (per coin, decided each 6h close):
  "mzG"     : s = -zG                     (fade the crowd)
  "D"       : s = D                       (side with the top 20% accounts against the crowd)
  "mzG_res" : s = -(residual z of zG on r24 and r7d, trailing 90d per-coin OLS) - the partial
              signal the screen tested (Kogan et al.: retail L/S follows past returns)
Position: continuous clip(s/2) or threshold sign(s)*1[|s|>=1.5]; overlapping hold of H bars;
per-coin inverse-vol, book vol-targeted to params["vol_target"]. Net exposure allowed (TS).

Screen (results/_screen_bc.json, crowding, Driscoll-Kraay pooled TS, partial on r24 + r7d):
  -zG : 6h 1.95 / 2.83, 24h 2.49 / 2.00 (train/test t);  D : 6h 2.19 / 3.28, 24h 1.80 / 2.79.
  72h fails the test half. Unconditional (non-partial) test t is weaker (1.97 / 1.28 for -zG).
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

NAME = "micro_crowd"
DESCRIPTION = ("12 Binance-metrics majors, time-series contrarian to the retail long/short account ratio "
               "(and/or with top traders vs retail), 6h decisions, vol-targeted.")
MECHANISM = ("Crowded retail positioning (high global L/S) is fuel for liquidations against it; top "
             "accounts leaning the other way are better informed. Retail L/S chases past returns, so the "
             "part not explained by momentum is the candidate signal.")
PANEL = dict(timeframe="6h", symbols=list(data.MAJORS[:12]), start="2021-12-01")
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False

GRID = []
for sig in ("mzG", "D", "mzG_res"):
    for mode in ("cont", "thr"):
        for H in (1, 4):
            GRID.append(dict(signal=sig, mode=mode, H=H, vol_target=0.20))
FROZEN = dict(signal="mzG", mode="thr", H=1, vol_target=0.20)   # stability pick, see results/micro_crowd.json

CAVEATS = [
    "Metrics history starts 2021-12 (11 of 12 coins): walk-forward uses 365d training windows, OOS starts 2022-12.",
    "Top-trader ratio is NaN for most of 2022 in the Binance archive; 'D' variants hold nothing then.",
    "Live: Bybit has the account ratio (/v5/market/account-ratio) but no top-trader ratio; Binance public fapi needed for zT.",
    "The 12 majors are highly correlated: this is mostly a single market-timing bet, not 12 independent ones.",
]


def _signal_raw(panel, metrics, which):
    m = HX.get_metrics(panel, metrics)
    with np.errstate(invalid="ignore", divide="ignore"):
        lnG = np.log(m["ls_ratio"])
        lnT = np.log(m["top_ls_ratio"])
    zG = ST.roll_z(lnG, 120, 60)
    if which == "mzG":
        return -zG
    if which == "D":
        return ST.roll_z(lnT, 120, 60) - zG
    lc = np.log(panel.c)
    r24 = np.full_like(lc, np.nan)
    r24[4:] = lc[4:] - lc[:-4]
    r7 = np.full_like(lc, np.nan)
    r7[28:] = lc[28:] - lc[:-28]
    return -HX.roll_resid_multi(zG, (r24, r7), 360, 180)


def weights(panel, params, metrics=None):
    s = _signal_raw(panel, metrics, params.get("signal", "mzG"))
    if params.get("mode", "cont") == "cont":
        pos = np.clip(s / 2.0, -1.0, 1.0)
    else:
        pos = np.where(np.abs(s) >= 1.5, np.sign(s), 0.0)
    pos = np.nan_to_num(pos)
    pos[~panel.tradable] = 0.0
    pos = HX.stagger(pos, int(params.get("H", 1)))
    vol = HX.asset_vol(panel, 120)
    with np.errstate(invalid="ignore", divide="ignore"):
        raw = np.where(np.isfinite(vol) & (vol > 0), pos / vol, 0.0) / panel.c.shape[1]
    w = HX.vol_scale_book(panel, raw, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params, metrics)
    tg = {panel.symbols[j]: float(w[-1, j]) for j in np.flatnonzero(w[-1] != 0)}
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "targets": tg, "orders": "market orders to target notional/equity at the 6h run; no resting orders"}


def run(null_n=200):
    # family trials: crowding screen 4 signals x 3 horizons x (TS + XS) = 24, plus this grid
    return HX.evaluate(sys.modules[__name__], train_days=365, null_n=null_n, family_trials=24 + len(GRID),
                       extra={"screen": "results/_screen_bc.json (crowding)"})


if __name__ == "__main__":
    o = run()
    print({k: o[k] for k in ("frozen", "verdict", "deflated_sharpe", "trades_per_day")})
    print(o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"), o["wf"]["oos_metrics"].get("max_drawdown"))
    print(o["null"]); print(o["null_secondary"])
    print(o["wf"]["oos_by_year"])
