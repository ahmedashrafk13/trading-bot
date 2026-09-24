"""crowd_xs53 - CROSS-SECTIONAL crowd composite, long/short quintiles on the 53-coin metrics universe (family F).

PRE-REGISTERED (written before any walk-forward / return-based look at this composite; 2026-09-24).

Hypothesis: the same five crowding measures as crowd_ts53, used RELATIVELY: coins whose crowd is more
offside than the other coins' (retail longer than usual, top traders shorter, takers selling beyond
their price move, funding richer than usual, new OI chasing the move) underperform the rest over
1-7 days. Relative use removes the common market-timing bet that dominates the TS version on majors.

Features (see _crowd53_common) per 6h close, each cross-sectionally ranked (centred) among ELIGIBLE coins,
multiplied by its pre-set sign (-zG, +D, +flow, -fz; oi sign = GRID param chosen on train only), averaged
(>= 3 of 5 required) = score. Long the top quintile, short the bottom quintile (q = 0.2, >= 8 eligible coins,
>= 1 name per side).
Leg weighting: "eq" (equal) or "iv" (inverse 30d vol within each leg). Neutrality: "dollar" (0.5 / 0.5 gross)
or "beta" (legs scaled so sum w*beta = 0 with gross 1; beta = trailing 30d beta to the equal-weight eligible
basket, clipped [0.3, 3]). Staggered overlapping hold of H bars, book vol-targeted to params["vol_target"]
(gross cap 3), per-name |w| cap 0.15 (squeeze tail), hysteresis band 0.02, per-name protective stop at
3 x the 14d-average daily range (k_stop = 3 fixed; cooldown H bars).

GRID (24): H {4, 12, 28} bars (24h/72h/168h) x weighting {"eq", "iv"} x neutral {"dollar", "beta"}
           x oi_sign {-1, +1}; q = 0.2, vol_target 0.20.
Walk-forward: rolling 365d train / 182d test, objective Sharpe, FROZEN = best median within-fold rank.
Family trials counted = 60 (with crowd_ts53).
Diagnostics (not selection): leave-one-feature-out and single-feature runs of FROZEN, by-year decay,
fee drag, no-stop / no-cap run, stop-fill correction, correlation to micro_crowd / micro_flowxs / BTC.

AMENDMENT (after run 1, rule-driven, not return-driven): the protective stop distance is capped at 15%
(_crowd53_common.STOP_MAX) because the live gate requires every perp stop within half the liquidation
distance (~16% at 3x); run 1 used uncapped 3xATR stops, some 50-80% away (results/_crowd_xs53_run1_uncapped_stops.json).
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _micro_harness as HX  # noqa: E402
from lab.strategies import _crowd53_common as CC  # noqa: E402

NAME = "crowd_xs53"
DESCRIPTION = ("53-coin Binance-metrics universe (PIT top-50 eligible), cross-sectional quintile long/short on a "
               "composite of five crowding ranks, staggered 1-7d hold, 6h decisions, vol-targeted, per-name cap "
               "and 3xATR protective stops.")
MECHANISM = ("Relative crowding: coins where retail and funding are more one-sided than elsewhere, and where "
             "informed flow disagrees, mean-revert against the crowd relative to the cross-section.")
PANEL = dict(CC.PANEL53)
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False
K_STOP = 3.0
NAME_CAP = 0.15
Q = 0.2

GRID = []
for H in (4, 12, 28):
    for wt in ("eq", "iv"):
        for neutral in ("dollar", "beta"):
            for oi_sign in (-1, 1):
                GRID.append(dict(H=H, weighting=wt, neutral=neutral, oi_sign=oi_sign, vol_target=0.20))
FROZEN = dict(H=28, weighting="iv", neutral="dollar", oi_sign=-1, vol_target=0.20)   # stability pick (run 2), results/crowd_xs53.json; verdict: fails

CAVEATS = list(__import__("lab.strategies.crowd_ts53", fromlist=["CAVEATS"]).CAVEATS)


def score(panel, params, metrics=None, feats=None):
    F = CC.features(panel, metrics)
    feats = tuple(feats or params.get("feats") or CC.FEATS)
    st = [HX.cs_rank(CC.signed(F, f, float(params.get("oi_sign", 1))), min_n=8) for f in feats]
    s = CC.nanmean_min(st, min(3, len(feats)))
    s[~F["elig"]] = np.nan
    return s, F


def _book(sc, F, weighting, neutral, q=Q, min_n=8):
    T, N = sc.shape
    w = np.zeros((T, N))
    vol, beta = F["vol"], F["beta"]
    for i in range(T):
        ok = np.flatnonzero(np.isfinite(sc[i]) & np.isfinite(vol[i]) & (vol[i] > 0))
        if ok.size < min_n:
            continue
        k = max(1, int(np.floor(q * ok.size)))
        o = ok[np.argsort(sc[i, ok], kind="stable")]
        L, S = o[-k:], o[:k]
        if weighting == "iv":
            wl, ws = 1.0 / vol[i, L], 1.0 / vol[i, S]
        else:
            wl, ws = np.ones(k), np.ones(k)
        wl, ws = wl / wl.sum(), ws / ws.sum()
        gL = gS = 0.5
        if neutral == "beta":
            bL = float(np.nansum(wl * np.nan_to_num(beta[i, L], nan=1.0)))
            bS = float(np.nansum(ws * np.nan_to_num(beta[i, S], nan=1.0)))
            if bL > 0 and bS > 0:
                gL = bS / (bL + bS)
                gS = 1.0 - gL
        w[i, L] += gL * wl
        w[i, S] -= gS * ws
    return w


def weights(panel, params, metrics=None, feats=None, k_stop=None, events=None, cap=None):
    sc, F = score(panel, params, metrics, feats)
    w = _book(sc, F, params.get("weighting", "eq"), params.get("neutral", "dollar"))
    H = int(params.get("H", 12))
    w = HX.stagger(w, H)
    w = HX.vol_scale_book(panel, w, float(params.get("vol_target", 0.20)), lb=120, cap=3.0)
    w = CC.cap_names(w, NAME_CAP if cap is None else cap)
    w = HX.band(w, 0.02)
    w[~panel.tradable] = 0.0
    k = K_STOP if k_stop is None else k_stop
    w = CC.apply_stops(panel, w, F["atr_pct"], k, cool=H, events=events)
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
                      "stopLoss at entry*(1 -/+ min(3 x 14d mean daily range, 15%)); a stopped name is not re-entered on "
                      "the same side for H bars"}
