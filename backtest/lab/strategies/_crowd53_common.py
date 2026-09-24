"""Shared feature / risk code for the family-F crowd composite modules (crowd_ts53, crowd_xs53).

Not a strategy module (leading underscore). numpy/pandas only. Everything here is causal:
the value in row i uses only data knowable at the close of bar i (metrics: stamp + 300 s,
see data.load_metrics; stops: the high/low/open of bar i itself).

Features (per coin, 6h bars; windows in bars; z = trailing z incl. the current bar, clipped +/-3):
  zG   = z_120(ln global L/S account ratio)                     signed  -zG
  D    = z_120(ln top-trader position ratio) - zG               signed  +D
  flow = cross-sectional OLS residual of rank(24h taker-buy share 2*tbqv/qv-1) on rank(r24),
         rank(r7d) among ELIGIBLE coins, standardised by the row std  signed +flow
  fz   = z_360(7d summed funding)                               signed  -fz
  oi   = z_360(7d change of ln OI value) * sign(r7d)            signed  oi_sign * oi (grid)
Eligible(i, j) = tradable (valid bar AND PIT top-50 member) AND ls_ratio and oi_value fresh at the
close (load_metrics' default max_stale = one bar) AND not inside 7d of a relisting.
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
from lab.strategies import _micro_stats as ST  # noqa: E402

FEATS = ("zG", "D", "flow", "fz", "oi")
SYMS53 = list(pd.read_json(os.path.join(data.HIST, "metric_symbols_ext.json"), typ="series"))
PANEL53 = dict(timeframe="6h", symbols=SYMS53, universe="pit_top50", start="2021-12-01", with_taker=True)

_CACHE: dict = {}


def _clipz(a, c=3.0):
    return np.clip(a, -c, c)


def _key(panel):
    m = panel.meta.get("metrics") or {}
    g = m.get("ls_ratio")
    return (panel.c.shape, int(panel.t[0]), int(panel.t[-1]), float(np.nansum(panel.c)),
            float(np.nansum(panel.h)), float(np.nansum(g)) if g is not None else 0.0,
            float(np.nansum(panel.funding)), int(panel.tradable.sum()))


def features(panel, metrics=None):
    """-> dict(elig [T,N] bool, zG, D, flow, fz, oi (unsigned oi*sign(r7)), r7, atr_pct, vol, beta).
    Cached per panel object (the panel arrays are views; keyed on id + shape + first/last t)."""
    k = _key(panel)
    if k in _CACHE:
        return _CACHE[k]
    m = HX.get_metrics(panel, metrics)
    T, N = panel.c.shape
    trad = panel.tradable.copy()
    rel = panel.meta.get("relisted")
    if rel is not None:
        relwin = pd.DataFrame(np.asarray(rel, float)).rolling(29, min_periods=1).max().to_numpy() > 0
        trad &= ~relwin
    with np.errstate(invalid="ignore", divide="ignore"):
        lnG = np.log(m["ls_ratio"])
        lnT = np.log(m["top_ls_ratio"])
        lnOI = np.log(m["oi_value"])
        lc = np.log(panel.c)
    elig = trad & np.isfinite(lnG) & np.isfinite(lnOI)
    zG = _clipz(ST.roll_z(lnG, 120, 60))
    zT = _clipz(ST.roll_z(lnT, 120, 60))
    D = _clipz(zT - zG)
    r24 = np.full_like(lc, np.nan)
    r24[4:] = lc[4:] - lc[:-4]
    r7 = np.full_like(lc, np.nan)
    r7[28:] = lc[28:] - lc[:-28]
    # taker-flow imbalance, 24h
    tb = pd.DataFrame(panel.meta["tbqv"]).rolling(4, min_periods=4).sum().to_numpy()
    qv = pd.DataFrame(panel.qv).rolling(4, min_periods=4).sum().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        imb = 2.0 * tb / np.where(qv > 0, qv, np.nan) - 1.0
    E = lambda a: np.where(elig, a, np.nan)   # noqa: E731
    e = HX.cs_resid(HX.cs_rank(E(imb)), [HX.cs_rank(E(r24)), HX.cs_rank(E(r7))])
    sd = np.nanstd(e, axis=1, keepdims=True) if T else e
    with np.errstate(invalid="ignore", divide="ignore"):
        flow = _clipz(e / np.where(sd > 0, sd, np.nan))
    # funding, 7d sum vs trailing 90d
    fund = np.where(panel.meta["valid"], panel.funding, np.nan)
    f7 = pd.DataFrame(fund).rolling(28, min_periods=28).sum().to_numpy()
    fz = _clipz(ST.roll_z(f7, 360, 180))
    # OI 7d change z x sign of the 7d return
    doi = np.full_like(lnOI, np.nan)
    doi[28:] = lnOI[28:] - lnOI[:-28]
    oi = _clipz(ST.roll_z(doi, 360, 180)) * np.sign(r7)
    # risk inputs
    hh = pd.DataFrame(panel.h).rolling(4, min_periods=4).max().to_numpy()
    ll = pd.DataFrame(panel.l).rolling(4, min_periods=4).min().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        rng_d = (hh - ll) / panel.c
    rng_d[~panel.meta["valid"]] = np.nan
    atr_pct = pd.DataFrame(rng_d).rolling(56, min_periods=20).mean().to_numpy()
    vol = HX.asset_vol(panel, 120)
    r = HX.close_ret(panel)
    r = np.where(elig, r, np.nan)
    mkt = np.nanmean(r, axis=1) if T else np.zeros(0)
    mkt = np.nan_to_num(mkt)
    R = pd.DataFrame(r)
    mr = R.notna()
    mm = pd.DataFrame(np.where(mr, mkt[:, None], np.nan))
    ex = (R * mm).rolling(120, min_periods=40).mean() - R.rolling(120, min_periods=40).mean() * mm.rolling(120, min_periods=40).mean()
    vm = (mm * mm).rolling(120, min_periods=40).mean() - mm.rolling(120, min_periods=40).mean() ** 2
    with np.errstate(invalid="ignore", divide="ignore"):
        beta = np.clip((ex / vm.where(vm > 1e-12)).to_numpy(), 0.3, 3.0)
    out = dict(elig=elig, zG=np.where(elig, zG, np.nan), D=np.where(elig, D, np.nan),
               flow=np.where(elig, flow, np.nan), fz=np.where(elig, fz, np.nan),
               oi=np.where(elig, oi, np.nan), r7=r7, atr_pct=atr_pct, vol=vol, beta=beta)
    if len(_CACHE) > 24:
        _CACHE.clear()
    _CACHE[k] = out
    return out


SIGN = {"zG": -1.0, "D": 1.0, "flow": 1.0, "fz": -1.0}


def signed(F, name, oi_sign):
    if name == "oi":
        return oi_sign * F["oi"]
    return SIGN[name] * F[name]


def nanmean_min(stack, min_n):
    a = np.stack(stack, 0)
    n = np.isfinite(a).sum(0)
    with np.errstate(invalid="ignore"):
        s = np.nanmean(np.where(np.isfinite(a), a, np.nan), axis=0)
    s[n < min_n] = np.nan
    return s


STOP_MAX = 0.15   # rule: stop within half the liquidation distance (3x per-position leverage -> ~33% -> <= 16%)


def apply_stops(panel, w, atr_pct, k, cool, events=None, max_dist=STOP_MAX):
    """Per-name protective stop for a weights book, sequential and causal.

    A position whose sign is (re)established by row i-1 fills at open i: ref = o[i],
    dist = k * atr_pct[i-1] (daily range estimate). From bar i on, a long is stopped when
    l <= ref*(1-dist), a short when h >= ref*(1+dist). The weight of a stopped name is set to 0
    in the row of the touching bar (the lab sim then exits at the NEXT open - the real resting
    stop would fill intrabar at the stop price; `events` collects (bar, j, side, stop_fill_px)
    so the difference can be estimated) and the same side is blocked for `cool` bars.
    The distance is capped at max_dist (default STOP_MAX = 0.15; AMENDMENT after run 1, rule-driven:
    run 1 had no cap and some 3xATR stops were 50-80% away, outside the live gate's half-liquidation
    clearance). k <= 0 disables."""
    w = np.array(w, float)
    if k is None or k <= 0:
        return w
    T, N = w.shape
    o, h, l = panel.o, panel.h, panel.l
    out = np.zeros_like(w)
    ref = np.full(N, np.nan)
    dist = np.full(N, np.nan)
    blk_side = np.zeros(N)
    blk_until = np.full(N, -1)
    prev = np.zeros(N)
    prev2 = np.zeros(N)
    for i in range(T):
        sp, sp2 = np.sign(prev), np.sign(prev2)
        new = (sp != 0) & (sp != sp2)
        if new.any():
            ref[new] = o[i, new]
            dist[new] = k * (atr_pct[i - 1, new] if i > 0 else np.nan)
            if max_dist is not None:
                dist[new] = np.minimum(dist[new], max_dist)
        held = sp != 0
        stopped = np.zeros(N, bool)
        if held.any():
            lo_hit = (sp > 0) & (l[i] <= ref * (1 - dist))
            hi_hit = (sp < 0) & (h[i] >= ref * (1 + dist))
            stopped = held & np.nan_to_num(lo_hit | hi_hit).astype(bool)
            if stopped.any() and events is not None:
                for j in np.flatnonzero(stopped):
                    s_px = ref[j] * (1 - dist[j]) if sp[j] > 0 else ref[j] * (1 + dist[j])
                    fill = min(o[i, j], s_px) if sp[j] > 0 else max(o[i, j], s_px)   # gap through the stop
                    events.append((i, int(j), float(sp[j]), float(fill)))
        x = w[i].copy()
        x[stopped] = 0.0
        blk_side[stopped] = sp[stopped]
        blk_until[stopped] = i + cool
        b = (i <= blk_until) & (np.sign(x) == blk_side) & (blk_side != 0)
        x[b] = 0.0
        # once the raw target changes side or goes flat, the block is lifted
        lift = (np.sign(w[i]) != blk_side)
        blk_side[lift] = 0
        out[i] = x
        prev2, prev = prev, x
    return out


def stop_fill_correction(panel, res, events):
    """Estimate of the P&L difference (real resting stop filled at the stop price in bar i vs the lab
    exit at open i+1), summed in USD on the simulated account, and as a mean annual fraction of equity.
    Uses the simulated qty held during bar i."""
    if not events:
        return {"n_stop_events": 0}
    pos = res.positions
    tot = 0.0
    rel = []
    T = len(panel.t)
    for (i, j, side, fill) in events:
        if i + 1 >= T:
            continue
        q = pos[i, j] if pos is not None else 0.0
        nx = panel.o[i + 1, j]
        if not np.isfinite(nx) or q == 0:
            continue
        d = q * (fill - nx)          # real minus lab (long: sell at fill instead of nx)
        tot += d
        rel.append(d / max(res.equity[i], 1e-9))
    yrs = T * panel.dt / (365.25 * 86400)
    rel = np.asarray(rel)
    return {"n_stop_events": len(events), "n_with_position": int(rel.size),
            "sum_usd_real_minus_lab": round(float(tot), 2),
            "per_year_frac_of_equity": round(float(rel.sum() / yrs), 4) if rel.size else 0.0,
            "mean_per_event_frac_of_equity": round(float(rel.mean()), 5) if rel.size else 0.0,
            "stop_events_per_year": round(len(events) / yrs, 1)}


def cap_names(w, cap):
    if cap is None or cap <= 0:
        return w
    return np.clip(w, -cap, cap)
