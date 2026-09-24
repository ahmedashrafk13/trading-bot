"""evt_pumpfade - PUMP + CROWD FADE (family G, idea b).  PRE-REGISTERED 2026-09-24 before any
walk-forward run.  Screen evidence was NEGATIVE: _evt_screens/screen1.py (2020-01..2021-12, funding-z
and funding-level filters, 18 configs + price-only control: every config lost 1-4%/event net) and
screen3 (2021-12..2023-11, first train window of this WF, OI / L-S filters, 12 configs: price-only
-0.95%/event, OI filter -1.4%, only 16-event subsets positive).  Run anyway so the idea gets a
proper walk-forward verdict rather than a screen-only one.

Hypothesis
  A coin in the PIT top-50 whose 7d return is in the top decile AND whose rally is crowd-financed
  (longs paying high funding, OI building, retail accounts leaning long) is exhausted: late longs are
  the fuel for a long squeeze.  Short with a protective stop, exit on time (3-7 d).  The crowd-long
  confirmation must come from funding / OI / L-S, never price alone (plain reversal failed in phase 2).

Event (decided at a 6h close i, filled next open)
  entry_ok (PIT top-50, valid)  AND  rk7 >= 0.9 (top decile of 7d return among entry_ok coins)
  AND conf:  "fund": F3 (3d funding sum) >= 0.15%   "oi": OI 3d change >= +10%
             "lsz": global L/S account z >= +1      "oi_lsz": OI >= +10% and lsz >= +1
  side SHORT; one event per coin per H days; stop at fill x (1 + stop); time stop H days.
  size = min(SIZE_MAX, vol_target * SIZE_K / sig30).

GRID (16): conf {fund, oi, lsz, oi_lsz} x H {3, 7} days x stop {0.15, 0.25}
Fixed: SIZE_K 0.30, SIZE_MAX 0.50, SIGMA_FLOOR 0.5, MAX_CONCURRENT 12.
Walk-forward: rolling 730d / 182d from 2021-12-01 -> OOS 2023-12..2025-06.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _evt_crowd as C  # noqa: E402

NAME = "evt_pumpfade"
DESCRIPTION = ("Short top-decile 7d gainers in the PIT top-50 when the rally is crowd-financed (high funding, "
               "rising OI or long-heavy retail L/S); protective stop, 3-7d time exit.")
MECHANISM = "Crowd-financed pumps exhaust; late leveraged longs are liquidation fuel."
PANEL = dict(timeframe="6h", universe="pit_top50", start="2021-12-01")
USES_METRICS = True
KIND = "events"
HOLD_WHEN_NOT_MEMBER = True
MAX_CONCURRENT = 12
NEEDS_HOURLY_RUNS = False
SIZE_K, SIZE_MAX, SIGMA_FLOOR = 0.30, 0.50, 0.5
BPD = 4

GRID = [dict(conf=cf, H=H, stop=s, vol_target=0.20)
        for cf in ("fund", "oi", "lsz", "oi_lsz") for H in (3, 7) for s in (0.15, 0.25)]
FROZEN = dict(conf="oi_lsz", H=3, stop=0.15, vol_target=0.20)   # WF stability pick (results/evt_pumpfade.json)
CAVEATS = ["OI / L-S confirmation exists for 53 coins only; 'fund' uses every PIT top-50 coin.",
           "OOS is only 1.5 years (metrics start 2021-12, 730d train)."]


def _mask(F, cf):
    m = F["ok"] & (C.nn(F["rk7"], 0) >= 0.9)
    if cf == "fund":
        m &= C.nn(F["F3"], -9) >= 0.0015
    elif cf == "oi":
        m &= C.nn(F["oich"], -9) >= 0.10
    elif cf == "lsz":
        m &= C.nn(F["lsz"], -9) >= 1.0
    elif cf == "oi_lsz":
        m &= (C.nn(F["oich"], -9) >= 0.10) & (C.nn(F["lsz"], -9) >= 1.0)
    return m


def events(panel, params, metrics=None):
    F = C.features(panel)
    H, stop = int(params["H"]), float(params["stop"])
    vt = float(params.get("vol_target", 0.20))
    ev = []
    for i, j in C.dedupe(_mask(F, params["conf"]), H * BPD):
        sg = F["sig"][i, j]
        sg = SIGMA_FLOOR if not np.isfinite(sg) else max(sg, SIGMA_FLOOR)
        ev.append({"i": i, "j": j, "side": -1, "size": float(round(min(SIZE_MAX, vt * SIZE_K / sg), 10)),
                   "stop_pct": stop, "time_stop": H * BPD})
    return ev


def null_pool(panel):
    return np.asarray(panel.meta.get("entry_ok", panel.tradable), bool) & np.isfinite(panel.c)


def live_targets(panel, params=None):
    params = params or FROZEN or GRID[0]
    last = len(panel.t) - 1
    return [{"symbol": panel.symbols[e["j"]], "side": "short", "size_frac_equity": e["size"],
             "stop_loss_pct_above_fill": e["stop_pct"], "time_exit_hours": e["time_stop"] * 6}
            for e in events(panel, params) if e["i"] == last]
