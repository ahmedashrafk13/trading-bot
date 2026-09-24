"""evt_squeeze - SQUEEZE HARVEST (family G, idea c).  PRE-REGISTERED 2026-09-24 before any
walk-forward run.  Screen evidence: _evt_screens/screen1.py (funding-only, 2020-01..2021-12: gross
+1..3%/event but NEGATIVE once BTC-hedged -> plain beta in a bull market) and _evt_screens/screen3.py (with crowd
metrics, 2021-12-01..2023-11-30 = exactly the first train window of this walk-forward; F3<=-0.1%
& global-L/S z<=-1, 3d hold: +2.0%/event net, t=3.35, hedged +1.2%).  12 + 16 screen configs counted.

Hypothesis
  When shorts are paying longs heavily (deeply negative funding), the crowd is short-heavy by
  account count (low global long/short z) or by top-trader positions, or open interest is
  building, and yet price is HOLDING above its 7-day low, the shorts are trapped: they bleed
  funding to longs every 8h and are fuel for a squeeze.  Go long, collect the funding, stop
  below the 7d low (the level whose break would prove the shorts right), exit when funding
  normalises or after H days.

Event (decided at a 6h close i, filled next open)
  entry_ok (PIT top-50, valid bar)  AND  F3 (3d funding sum) <= fth  AND  close >= 1.05 x lo7
  AND confirmation conf:
     "none" : no metrics (funding-only control)
     "lsz"  : global L/S account-ratio 30d z <= -1
     "tlsz" : top-trader L/S position-ratio 30d z <= -1
     "oi"   : OI 3d change >= +5%
  side LONG; one event per coin per H days (causal cooldown).
  stop  = max(0.99 x lo7, 0.70 x close)  (resting server-side stop, below the 7d low, <= 30% away)
  exits = time stop H days; if exit_norm: close at the next open once the 1d funding sum >= 0.
  size  = min(SIZE_MAX, vol_target * SIZE_K / sig30), sig floored at SIGMA_FLOOR.

GRID (32): fth {-0.001, -0.003} x conf {none, lsz, tlsz, oi} x H {3, 7} days x exit_norm {F, T}
Fixed: SIZE_K 0.30, SIZE_MAX 0.50, SIGMA_FLOOR 0.5, MAX_CONCURRENT 12, hold margin 5%.
Walk-forward: rolling 730d / 182d from 2021-12-01 (metrics era) -> OOS 2023-12..2025-06 (1.5y).
Nulls: random_coin = same bar/side/size/stop/time on a random PIT top-50 coin; sign_flip.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _evt_crowd as C  # noqa: E402

NAME = "evt_squeeze"
DESCRIPTION = ("Long coins with deeply negative 3d funding, a short-crowded account/position ratio or rising OI, "
               "while price holds >= 5% above its 7d low; stop below the 7d low, exit on funding normalisation / time.")
MECHANISM = ("Trapped shorts pay funding to longs and are squeeze fuel while price refuses to break down; the "
             "long collects funding plus the squeeze and is stopped out if the 7d low breaks.")
PANEL = dict(timeframe="6h", universe="pit_top50", start="2021-12-01")
USES_METRICS = True
KIND = "events"
HOLD_WHEN_NOT_MEMBER = True
MAX_CONCURRENT = 12
NEEDS_HOURLY_RUNS = False
SIZE_K, SIZE_MAX, SIGMA_FLOOR = 0.30, 0.50, 0.5
HOLD_MARGIN = 0.05
BPD = 4

GRID = [dict(fth=fth, conf=cf, H=H, exit_norm=en, vol_target=0.20)
        for fth in (-0.001, -0.003) for cf in ("none", "lsz", "tlsz", "oi") for H in (3, 7) for en in (False, True)]
FROZEN = dict(fth=-0.003, conf="lsz", H=3, exit_norm=True, vol_target=0.20)   # WF stability pick (results/evt_squeeze.json)

CAVEATS = ["Crowd metrics exist for 53 coins only (and top-trader ratio has archive holes); conf != 'none' "
           "restricts the book to those coins.",
           "OOS is only 1.5 years (metrics start 2021-12, 730d train)."]


def _mask(F, params):
    fth, cf = float(params["fth"]), params["conf"]
    m = F["ok"] & (C.nn(F["F3"], 9) <= fth) & (F["c"] >= F["lo7"] * (1 + HOLD_MARGIN))
    if cf == "lsz":
        m &= C.nn(F["lsz"], 9) <= -1.0
    elif cf == "tlsz":
        m &= C.nn(F["tlsz"], 9) <= -1.0
    elif cf == "oi":
        m &= C.nn(F["oich"], -9) >= 0.05
    return m


def events(panel, params, metrics=None):
    F = C.features(panel)
    F["c"] = np.nan_to_num(panel.c, nan=-1.0)
    H = int(params["H"])
    vt = float(params.get("vol_target", 0.20))
    ev = []
    for i, j in C.dedupe(_mask(F, params), H * BPD):
        cl = float(panel.c[i, j])
        stop = max(0.99 * float(F["lo7"][i, j]), 0.70 * cl)
        sg = F["sig"][i, j]
        sg = SIGMA_FLOOR if not np.isfinite(sg) else max(sg, SIGMA_FLOOR)
        ev.append({"i": i, "j": j, "side": 1, "size": float(round(min(SIZE_MAX, vt * SIZE_K / sg), 10)),
                   "stop": float(round(stop, 12)), "time_stop": H * BPD})
    out = {"entries": ev}
    if params.get("exit_norm"):
        out["exits"] = C.nn(F["F1"], -9) >= 0.0
    else:
        out["exits"] = None
    return out


def null_pool(panel):
    return np.asarray(panel.meta.get("entry_ok", panel.tradable), bool) & np.isfinite(panel.c)


def live_targets(panel, params=None):
    params = params or FROZEN or GRID[0]
    sig = events(panel, params)
    last = len(panel.t) - 1
    ex = sig["exits"]
    return {"open": [{"symbol": panel.symbols[e["j"]], "side": "long", "size_frac_equity": e["size"],
                      "stop_loss_price": e["stop"], "time_exit_hours": e["time_stop"] * 6}
                     for e in sig["entries"] if e["i"] == last],
            "close_if_held": [] if ex is None else [panel.symbols[j] for j in np.flatnonzero(ex[last])]}
