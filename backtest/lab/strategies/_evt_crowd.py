"""Shared, causal feature builder for the crowd-confirmed event modules (evt_squeeze, evt_pumpfade).

All features at bar i use bars <= i only (rolling windows end at i; cross-sectional ranks use row i).
  F3    : sum of funding settled over the last 12 x 6h bars (3 days); > 0 = longs paid shorts
  F1    : same over the last 4 bars (1 day)
  R7    : 7d close-to-close return (28 bars), NaN across missing closes
  lo7   : min low over the last 28 bars (incl. i)
  rk7   : cross-sectional percentile of R7 among entry_ok coins at bar i
  oich  : OI (USD value) 3d change
  lsz   : 30d (120-bar) z-score of ln(global long/short ACCOUNT ratio); tlsz: same, top-trader ratio
  sig   : annualised 30d vol of 6h log returns
"""
from __future__ import annotations

import numpy as np
import pandas as pd

BPD = 4


def _z(x, n=120, minp=60):
    with np.errstate(invalid="ignore", divide="ignore"):
        lx = np.log(x)
    d = pd.DataFrame(lx)
    return ((d - d.rolling(n, min_periods=minp).mean()) / d.rolling(n, min_periods=minp).std()).to_numpy()


def features(panel):
    c, l, f = panel.c, panel.l, panel.funding
    ok = np.asarray(panel.meta.get("entry_ok", panel.tradable), bool)
    F = pd.DataFrame(f)
    out = {"F3": F.rolling(12, min_periods=12).sum().to_numpy(),
           "F1": F.rolling(4, min_periods=4).sum().to_numpy()}
    with np.errstate(invalid="ignore", divide="ignore"):
        R7 = np.full_like(c, np.nan)
        R7[28:] = c[28:] / c[:-28] - 1
        lr = np.full_like(c, np.nan)
        lr[1:] = np.log(c[1:] / c[:-1])
    out["R7"] = R7
    out["lo7"] = pd.DataFrame(l).rolling(28, min_periods=20).min().to_numpy()
    out["rk7"] = pd.DataFrame(np.where(ok, R7, np.nan)).rank(axis=1, pct=True).to_numpy()
    out["sig"] = pd.DataFrame(lr).rolling(120, min_periods=40).std().to_numpy() * np.sqrt(BPD * 365.25)
    m = panel.meta.get("metrics")
    if m is not None:
        oi = m["oi_value"]
        with np.errstate(invalid="ignore", divide="ignore"):
            oich = np.full_like(oi, np.nan)
            oich[12:] = oi[12:] / oi[:-12] - 1
        out["oich"] = oich
        out["lsz"] = _z(m["ls_ratio"])
        out["tlsz"] = _z(m["top_ls_ratio"])
    else:
        nan = np.full_like(c, np.nan)
        out["oich"] = out["lsz"] = out["tlsz"] = nan
    out["ok"] = ok & np.isfinite(c)
    return out


def dedupe(mask, gap):
    """Causal event list from a [T, N] candidate mask: a coin fires at most once per `gap` bars,
    counted from the start of the panel given (walk_forward always passes panels starting at bar 0)."""
    ii, jj = np.nonzero(mask)
    order = np.lexsort((jj, ii))
    last = {}
    out = []
    for i, j in zip(ii[order], jj[order]):
        if i - last.get(j, -10 ** 9) >= gap:
            out.append((int(i), int(j)))
            last[j] = i
    return out


def nn(a, v):
    return np.nan_to_num(a, nan=v, posinf=v, neginf=v)
