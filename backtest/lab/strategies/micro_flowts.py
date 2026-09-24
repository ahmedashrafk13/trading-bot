"""micro_flowts - BTC time-series residualised taker-flow imbalance (family E, signal a).

Signal (decided at each 6h close, 00/06/12/18 UTC):
  imb24 = 2 * tbqv_24h / qv_24h - 1           (Binance USDT-M taker-buy share, last 24h)
  r24   = ln(c / c_24h_ago)
  e     = residual of a trailing 90d (360 x 6h samples, window incl. now) OLS imb24 ~ a + b*r24
  z     = e / std(residual in the window)
Position: s = clip(z / zscale, -1, 1) (continuous) or sign(z) * 1[|z| >= k] (threshold),
held as an overlapping portfolio over the last H decisions (H bars of 6h),
optionally long-only, inverse-vol and then book-scaled to params["vol_target"] on the trailing 30d
realised vol of the raw book (gross cap 3x).

Screen (results/_screen_a.json, train 2020-01..2023-12, test 2024-01..2025-06): BTC W=24h,
controls r24 + r7d: 6h horizon t 2.25 / 2.49, 24h horizon t 2.92 / 3.83 (NW), same sign.
ETH same sign but |t| < 2 in both halves, so ETH is NOT traded here.
Live data: Binance public fapi /fapi/v1/klines (field 'taker buy quote asset volume');
Bybit klines have no taker split. Execution on Bybit BTCUSDT perp.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _micro_stats as ST  # noqa: E402

NAME = "micro_flowts"
DESCRIPTION = ("BTC perp, time-series: residualised 24h taker-flow imbalance z (flow not explained "
               "by the same-window return), 6h decisions, overlapping hold, vol-targeted.")
MECHANISM = ("Aggressive (taker) buying that did NOT move price yet signals informed / persistent demand "
             "absorbed by passive liquidity; price catches up over the next 6-24h. Raw flow is "
             "confounded with the contemporaneous return (which itself reverses), so only the residual "
             "is used (Anastasopoulos et al. 2024).")
PANEL = dict(timeframe="6h", symbols=["BTCUSDT"], start="2020-01-01", with_taker=True)
USES_METRICS = False
KIND = "weights"
NEEDS_HOURLY_RUNS = False

GRID = []
for mode in ("cont", "k0.5", "k1.0"):
    for H in (1, 4, 12):
        for lo in (False, True):
            GRID.append(dict(mode=mode, H=H, long_only=lo, vol_target=0.20))
FROZEN = dict(mode="k0.5", H=12, long_only=True, vol_target=0.20)   # stability pick, see results/micro_flowts.json

CAVEATS = [
    "Signal needs Binance taker-buy volume live (public, no key); Bybit has no taker split - basis/venue mismatch risk.",
    "Single asset: the whole edge rides on ~5.5 years of one coin; screen cell chosen from 12 (2 coins x 2 windows x 3 horizons).",
]


def _z(panel):
    tb = panel.meta["tbqv"][:, 0]
    qv = panel.qv[:, 0]
    c = panel.c[:, 0]
    tbs = pd.Series(tb).rolling(4, min_periods=4).sum().to_numpy()
    qvs = pd.Series(qv).rolling(4, min_periods=4).sum().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        imb = 2.0 * tbs / np.where(qvs > 0, qvs, np.nan) - 1.0
    r24 = ST.back_log_ret(c, 4)
    return ST.roll_resid_z(imb, r24, 360, 180).reshape(-1)


def signal(panel, params):
    z = _z(panel)
    mode = params.get("mode", "cont")
    if mode == "cont":
        s = np.clip(z / 2.0, -1.0, 1.0)
    else:
        k = float(mode[1:])
        s = np.where(np.abs(z) >= k, np.sign(z), 0.0)
    s = np.nan_to_num(s)
    if params.get("long_only"):
        s = np.maximum(s, 0.0)
    return HX.stagger(s[:, None], int(params.get("H", 4)))


def weights(panel, params, metrics=None):
    s = signal(panel, params)
    s[~panel.tradable] = 0.0
    vol = HX.asset_vol(panel, 120)            # 30d of 6h bars: inverse-vol raw position
    with np.errstate(invalid="ignore", divide="ignore"):
        raw = np.where(np.isfinite(vol) & (vol > 0), s / vol, 0.0)
    # book-level scaling on the trailing realised vol of the raw book (30d), so the
    # stream runs at ~vol_target even when the staggered signal is only partly on
    w = HX.vol_scale_book(panel, raw, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = HX.band(w, 0.05)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params)
    z = _z(panel)
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "targets": {"BTCUSDT": float(w[-1, 0])}, "z_now": float(z[-1]) if np.isfinite(z[-1]) else None,
            "orders": "market (or post-only near touch) to move BTCUSDT perp to target notional/equity at the 6h run; "
                      "no resting orders; protective stop per sleeve rules (not modelled in the backtest)"}


def run(null_n=200):
    return HX.evaluate(sys.modules[__name__], null_n=null_n, family_trials=12 + len(GRID),
                       extra={"screen": "results/_screen_a.json (ts_btc_eth)"})


if __name__ == "__main__":
    o = run()
    print({k: o[k] for k in ("frozen", "verdict", "deflated_sharpe", "trades_per_day")})
    print(o["wf"]["oos_metrics"].get("sharpe"), o["wf"]["oos_metrics"].get("cagr"), o["wf"]["oos_metrics"].get("max_drawdown"))
    print(o["null"])
    print(o["wf"]["oos_by_year"])
