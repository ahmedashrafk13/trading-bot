"""crowd_ts53 - per-coin TIME-SERIES crowd composite on the 53-coin Binance-metrics universe (family F).

PRE-REGISTERED (written before any walk-forward / return-based look at this composite; 2026-09-24).

Hypothesis: each crowd/positioning measure that survived phase 2 is weak alone (micro_crowd Sharpe 1.25 on
12 majors and decaying, micro_flowxs 1.17 post-hoc). Five nearly independent crowding measures averaged
per coin, over ~30 PIT-eligible coins instead of 12, should raise the signal-to-noise per decision and the
number of independent bets, and dilute the decay seen on the 12 majors.

Features (see _crowd53_common; all trailing / causal, z clipped +/-3) and PRE-SET SIGNS:
  -zG   fade the retail account long/short ratio (30d z)                                   [sign -]
  +D    side with top traders against retail: z(top position ratio) - zG                   [sign +]
  +flow 24h taker-buy share, XS residual on rank(r24), rank(r7d), row-standardised           [sign +]
  -fz   7d funding vs its trailing 90d (crowded longs pay)                                  [sign -]
  oi_sign * z(7d dln OI) * sign(r7d)   new money chasing the 7d move: sign NOT pre-set, it is a GRID
        parameter so each walk-forward fold picks it on its TRAIN window only               [sign +/-]
Composite C_raw = mean of the available signed features (>= 3 of 5 required), then C = C_raw divided by
its trailing 360-bar (90d) RMS per coin (scale only, no demeaning) -> unit-ish scale.
Position per coin at each 6h close: sign(C) if |C| >= thr else 0 (eligible coins only), overlapping hold
of H bars (stagger), divided by the coin's trailing 30d vol, optional cross-sectional demeaning over the
eligible coins (neutral="demean"), book vol-targeted to params["vol_target"] (gross cap 3), per-name
|w| cap 0.25, hysteresis band 0.02, then a per-name protective stop at 3 x the 14d-average daily range
(k_stop=3 fixed, cooldown H bars) - required live (stopLoss within half the liquidation distance).
Eligibility: PIT top-50 member AND valid bar AND ls_ratio + oi_value fresh (<= one 6h bar old) AND not
within 7d of a relisting.

GRID (36): thr {0.75, 1.25, 1.75} x H {1, 2, 4} bars (6h/12h/24h) x oi_sign {-1, +1}
           x neutral {"none", "demean"}; vol_target 0.20. k_stop = 3 fixed (no-stop run = diagnostic).
Walk-forward: rolling 365d train / 182d test (metrics start 2021-12), objective Sharpe, FROZEN = best
median within-fold rank (harness rule). Family trials counted = 36 (this grid) + 24 (crowd_xs53) = 60.
Diagnostics (not selection): leave-one-feature-out and single-feature runs of FROZEN, by-year decay,
fee drag, no-stop run, stop-fill correction, correlation to micro_crowd / micro_flowxs / BTC.

AMENDMENT (after run 1, rule-driven, not return-driven): the protective stop distance is capped at 15%
(_crowd53_common.STOP_MAX) because the live gate requires every perp stop within half the liquidation
distance (~16% at 3x); run 1 used uncapped 3xATR stops, some 50-80% away (results/_crowd_ts53_run1_uncapped_stops.json).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _crowd53_common as CC  # noqa: E402

NAME = "crowd_ts53"
DESCRIPTION = ("53-coin Binance-metrics universe (PIT top-50 eligible), per-coin time-series composite of five "
               "crowding measures (retail L/S, top-vs-retail, taker flow, funding z, OI-chase), threshold entry, "
               "6-24h hold, 6h decisions, vol-targeted, 3xATR protective stops.")
MECHANISM = ("Crowded positioning (retail long, paying funding, new OI chasing the move) is unwound against "
             "the crowd; informed flow (top accounts, aggressive takers beyond the price move) persists. "
             "Averaging nearly independent crowd readings across ~30 coins raises breadth.")
PANEL = dict(CC.PANEL53)
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False
K_STOP = 3.0
NAME_CAP = 0.25

GRID = []
for thr in (0.75, 1.25, 1.75):
    for H in (1, 2, 4):
        for oi_sign in (-1, 1):
            for neutral in ("none", "demean"):
                GRID.append(dict(thr=thr, H=H, oi_sign=oi_sign, neutral=neutral, vol_target=0.20))
FROZEN = dict(thr=0.75, H=4, oi_sign=1, neutral="none", vol_target=0.20)   # stability pick (run 2), results/crowd_ts53.json; verdict: fails

CAVEATS = [
    "The 53-coin metrics list was assembled in 2026 (current/recent top coins): coins that died or were renamed "
    "before 2025 (LUNA, FTT, MATIC, FTM, EOS, 1000SHIB ...) are absent, so ~20 of the 50 PIT members at each date "
    "are missing - a survivorship tilt in the universe even though trading is PIT-gated.",
    "Top-trader ratio is NaN for most of 2022 in the Binance archive; D is missing then (composite uses >= 3 of 5).",
    "Live: Bybit exposes an account ratio but no top-trader ratio or taker-buy volume; zT and flow need Binance public fapi.",
    "Stops are modelled as 'exit at the next 6h open after the bar that touched the stop'; the real resting stop fills "
    "at the stop price - the difference is estimated separately (stop_effect).",
]


def composite(panel, params, metrics=None, feats=None):
    F = CC.features(panel, metrics)
    feats = tuple(feats or params.get("feats") or CC.FEATS)
    st = [CC.signed(F, f, float(params.get("oi_sign", 1))) for f in feats]
    min_n = min(3, len(feats))
    c = CC.nanmean_min(st, min_n)
    rms = np.sqrt(pd.DataFrame(c * c).rolling(360, min_periods=120).mean().to_numpy())
    with np.errstate(invalid="ignore", divide="ignore"):
        C = c / np.where(rms > 1e-9, rms, np.nan)
    C[~F["elig"]] = np.nan
    return C, F


def weights(panel, params, metrics=None, feats=None, k_stop=None, events=None):
    C, F = composite(panel, params, metrics, feats)
    thr = float(params.get("thr", 1.25))
    pos = np.where(np.abs(np.nan_to_num(C)) >= thr, np.sign(np.nan_to_num(C)), 0.0)
    pos[~F["elig"]] = 0.0
    pos = HX.stagger(pos, int(params.get("H", 1)))
    vol = F["vol"]
    with np.errstate(invalid="ignore", divide="ignore"):
        raw = np.where(np.isfinite(vol) & (vol > 0), pos / vol, 0.0)
    raw[~F["elig"]] = 0.0
    if params.get("neutral", "none") == "demean":
        n = F["elig"].sum(1)
        mu = np.where(n > 0, raw.sum(1) / np.maximum(n, 1), 0.0)
        raw = np.where(F["elig"], raw - mu[:, None], 0.0)
    w = HX.vol_scale_book(panel, raw, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = CC.cap_names(w, NAME_CAP)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    k = K_STOP if k_stop is None else k_stop
    w = CC.apply_stops(panel, w, F["atr_pct"], k, cool=int(params.get("H", 1)), events=events)
    w[~panel.tradable] = 0.0
    return w


def live_targets(panel, params, metrics=None):
    w = weights(panel, params, metrics)
    F = CC.features(panel, metrics)
    tg = {}
    for j in np.flatnonzero(w[-1] != 0):
        side = np.sign(w[-1, j])
        d = min(K_STOP * float(F["atr_pct"][-1, j]), CC.STOP_MAX)
        tg[panel.symbols[j]] = {"w": float(w[-1, j]),
                                "stop_loss_px": float(panel.c[-1, j] * (1 - side * d))}
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt), "targets": tg,
            "orders": "market orders to target notional/equity at the 6h run; each perp carries an attached "
                      "stopLoss at entry*(1 -/+ min(3 x 14d mean daily range, 15%)) (re-anchor to the fill price)"}
