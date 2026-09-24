"""evt_newlist - NEW-LISTING FADE (family G, idea a).  PRE-REGISTERED 2026-09-24 before any
walk-forward run.  Screen evidence came from the FIRST train window only (2020-01..2021-12,
strategies/_evt_screens/screen1.py, screen2.py, 39 (a)-configs looked at, all counted as trials).

Hypothesis
  A newly listed Binance USDT-M perp that is liquid enough to enter the point-in-time top-60 by
  30d quote volume shortly after launch tends to bleed over the following 1-3 months: launch hype
  decays, locked supply unlocks / airdrop recipients sell, market makers unload loan inventory,
  and the perp is the only venue where the late crowd can be faded.  Shorts usually RECEIVE
  funding on these names (train median +1.5..4.8% per 30d), but squeezes are violent, so every
  short carries a protective stop.

Event (decided at a 6h close i, filled at the next open by sim.run_events)
  L_j   = first bar with data of symbol j in the panel.  Listings before 2020-04-01 are the
          initial Binance USDT-M roll-out of legacy coins (ADA, XRP, LTC ... in Jan-Mar 2020,
          which also coincide with the COVID crash) and are NOT new tokens -> excluded.
          Relistings after a dead period are not counted (only the first listing).
  entry = first 6h bar i with  age = i - L_j in [d0*4, (d0+14)*4]  AND  the coin is a PIT
          top-60 member at i (meta["entry_ok"] = original tradable mask)  AND  trailing 2d
          funding sum >= FUND_FLOOR (-0.2%: shorts would be over-paying -> skip).
  side  = SHORT (sign -1).  One event per coin, ever.
  size  = min(SIZE_MAX, vol_target * SIZE_K / sigma), sigma = annualised vol of 6h log returns
          since listing (last <= 28 bars, >= 6 bars, floored at SIGMA_FLOOR).
  exits = protective stop at entry*(1+stop) (resting server-side stop: fires intrabar),
          time stop after H days.  Holding continues if the coin later drops out of the top-60
          (tradable for holding = valid bar; entries need membership).

GRID (27 configs) - vol_target fixed at 0.20:
  d0   in {2, 7, 14} days after the first bar
  H    in {30, 60, 90} days
  stop in {0.25, 0.40, 0.60} (fraction above the fill)
Fixed a-priori constants (not searched): FUND_FLOOR=-0.002, SIZE_K=0.30, SIZE_MAX=0.25,
  SIGMA_FLOOR=0.8, MAX_CONCURRENT=25, entry window 14 days, K=60 (whole PIT store).
Walk-forward: rolling 730d train / 182d test from 2020-01-01 -> OOS 2022-01..2025-06.
Nulls: (1) matched "random mature coin" null - every event is replaced by a random PIT top-60
  coin listed >= 365d earlier, same bar, same side/size/stop/H; (2) sign flip per event.
Variant reported (not selected on): BTC-beta hedge overlay (long BTC = beta x short notional).
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

NAME = "evt_newlist"
DESCRIPTION = ("Short newly listed USDT-M perps that reach the PIT top-60 within weeks of launch, "
               "from d0 days after the first bar for H days, per-name protective stop, small inverse-vol size.")
MECHANISM = ("Launch hype decay, supply unlocks / airdrop selling and market-maker inventory release make "
             "new tokens underperform for 1-3 months; the perp lets the late crowd be faded while shorts "
             "usually receive funding.")
PANEL = dict(timeframe="6h", universe="pit_top60", start="2020-01-01")
USES_METRICS = False
KIND = "events"
HOLD_WHEN_NOT_MEMBER = True
MAX_CONCURRENT = 25
NEEDS_HOURLY_RUNS = False

FUND_FLOOR = -0.002
SIZE_K = 0.30
SIZE_MAX = 0.25
SIGMA_FLOOR = 0.8
LISTING_MIN_T = 1585699200          # 2020-04-01 00:00 UTC
ENTRY_WINDOW_D = 14
BPD = 4                              # 6h bars per day

GRID = [dict(d0=d0, H=H, stop=s, vol_target=0.20)
        for d0 in (2, 7, 14) for H in (30, 60, 90) for s in (0.25, 0.40, 0.60)]
FROZEN = dict(d0=2, H=60, stop=0.25, vol_target=0.20)   # stability pick of the walk-forward (results/evt_newlist.json)

CAVEATS = [
    "Universe = coins that EVER reached the PIT top-60 (download union). Entries require PIT top-60 "
    "membership at the decision bar, so the tradable set is point-in-time complete; listings that never "
    "reached the top-60 are simply never traded (by construction, not by hindsight).",
    "Bybit availability at entry time is not known historically (instrument snapshot is current, delisted "
    "names missing); see implementability_200.bybit_listed_at_entry_share.",
]


def _sigma(panel):
    c = panel.c
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.log(c[1:] / c[:-1])
    r = np.vstack([np.full((1, c.shape[1]), np.nan), r])
    return r


def events(panel, params, metrics=None):
    d0, H, stop = int(params["d0"]), int(params["H"]), float(params["stop"])
    vt = float(params.get("vol_target", 0.20))
    t = np.asarray(panel.t, np.int64)
    T, N = panel.c.shape
    ok = panel.meta.get("entry_ok", panel.tradable)
    valid = panel.meta.get("valid", panel.tradable)
    fin = np.isfinite(panel.c)
    f = panel.funding
    r = _sigma(panel)
    out = []
    for j, s in enumerate(panel.symbols):
        if s in ("BTCUSDT", "ETHUSDT"):
            continue
        idx = np.flatnonzero(fin[:, j])
        if not len(idx):
            continue
        L = int(idx[0])
        if L == 0 or t[L] < LISTING_MIN_T:
            continue
        lo, hi = L + d0 * BPD, min(L + (d0 + ENTRY_WINDOW_D) * BPD, T - 1)
        for i in range(lo, hi + 1):
            if i >= T:
                break
            if not (ok[i, j] and valid[i, j]):
                continue
            if f[max(0, i - 7):i + 1, j].sum() < FUND_FLOOR:
                continue
            w = r[max(L + 1, i - 27):i + 1, j]
            w = w[np.isfinite(w)]
            sig = np.std(w, ddof=1) * np.sqrt(BPD * 365.25) if len(w) >= 6 else np.nan
            sig = SIGMA_FLOOR if not np.isfinite(sig) else max(sig, SIGMA_FLOOR)
            size = min(SIZE_MAX, vt * SIZE_K / sig)
            out.append({"i": int(i), "j": j, "side": -1, "size": float(round(size, 10)),
                        "stop_pct": stop, "time_stop": H * BPD})
            break
    out.sort(key=lambda e: (e["i"], e["j"]))
    return out


def live_targets(panel, params=None, now_i=None):
    """Live use at a 6h run: return the events whose decision bar is the LAST closed bar, i.e. new
    shorts to open now, with the protective stop to attach server-side (stopLoss = fill*(1+stop))
    and the planned exit time.  Positions opened earlier keep their resting stop; the time exit is
    executed at the first 6h run at/after entry + H days."""
    params = params or FROZEN or GRID[0]
    ev = events(panel, params)
    last = len(panel.t) - 1 if now_i is None else int(now_i)
    res = []
    for e in ev:
        if e["i"] == last:
            res.append({"symbol": panel.symbols[e["j"]], "side": "short", "size_frac_equity": e["size"],
                        "stop_loss_pct_above_fill": e["stop_pct"], "time_exit_hours": e["time_stop"] * 6})
    return res


def null_pool(panel):
    """Matched null pool: PIT top-60 coins (entry_ok) listed >= 365 days before the bar, not BTC/ETH."""
    ok = np.asarray(panel.meta.get("entry_ok", panel.tradable), bool).copy()
    fin = np.isfinite(panel.c)
    T = len(panel.t)
    for j, s in enumerate(panel.symbols):
        idx = np.flatnonzero(fin[:, j])
        if s in ("BTCUSDT", "ETHUSDT") or not len(idx):
            ok[:, j] = False
            continue
        ok[:min(T, idx[0] + 365 * BPD), j] = False
    return ok


def extra_report(P, oos, rfro, out):
    """Pre-registered extras: BTC-hedged variant nulls, delistings, vol-scaled view."""
    from lab.strategies import _evt_harness as H
    L = H.LAST
    x = {"btc_hedge_overlay_oos_nulls": H.hedged_nulls(L["P"], sys.modules[__name__], L["ents"], L["a"], L["b"],
                                                        L["kw"], n=int(os.environ.get("EVT_HEDGE_NULL_N", 100)), exits=L.get("exits"))}
    x["oos_delistings"] = len(oos.delistings)
    x["oos_liquidations"] = int(oos.n_liquidations)
    om = out["wf"]["oos_metrics"]
    vol = om.get("vol_annual") or 0
    if vol > 0:
        k = 0.20 / vol
        x["oos_scaled_to_20pct_vol"] = {"scale": round(k, 3), "approx_arith_return": round(k * (om["cagr"] or 0), 4),
                                        "note": "linear scaling of the realised OOS book (sizes fixed a priori gave "
                                                "a lower vol than the 20% target); drawdown scales ~linearly too"}
    return x
