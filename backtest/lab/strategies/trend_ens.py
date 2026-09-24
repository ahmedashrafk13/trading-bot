"""Strategy family A: multi-speed TREND ENSEMBLE + funding-crowding gate.

Research shortlist #1 (Zarattini/Pagani/Barbon 2025 style) + signal #2.

Signal (per asset, per lookback N in days {5,10,20,30,60,90,150,250,360}):
  donch : Donchian state machine on CLOSES. Long when close > max of the prior
          N closes; the long's trailing stop = max(prev stop, channel midpoint
          (maxN+minN)/2 of the prior N closes); exit when close < stop.
          Short is the mirror (close < min prior N; stop = min(prev, mid);
          exit when close > stop).  Exits and entries are evaluated only at bar
          closes (6h routine cadence) - no intrabar resting stops are modelled.
  tsmom : sign(close / close N days ago - 1).
  Ensemble signal s in [-1, 1] = mean over the 9 lookbacks (a lookback without
  N days of history counts as 0).
Direction: "lo" long-only (clip at 0); "ls" full long/short; "ls_ma" long/short
  but the short part only while close < its 200d simple MA.
Sizing: w_j = s_j / sigma_j (sigma = realised vol, `vol_days`), then the whole
  book is scaled so that the FULL-CONVICTION book (|s|=1 on every asset with a
  non-zero signal, same signs) has ex-ante vol = params["vol_target"]
  (covariance = trailing `bvol_days` of bar returns).  Conviction is therefore
  kept: realised vol is below vol_target when signals are partial.  Per-asset
  cap |w| <= asset_cap, gross cap sum|w| <= gross_cap.
Funding gate (gate < 1): F7 = trailing 7d mean funding (8h-normalised), P = its
  percentile inside the trailing 365d.  P >= gate_p or annualised F7 >= gate_ann
  -> NEW long exposure (above the currently held long) is multiplied by `gate`
  (0.5 = halve, 0 = no new longs).  Mirror for shorts: P <= 100-gate_p or
  annualised F7 <= -gate_ann.
Rebalance band (RELATIVE): a symbol is traded only when |target - held| >
  band * max(|target|, |held|), on a sign change, on an entry from 0 or on a
  close to 0; otherwise the held TARGET is repeated, so
  sim.run_weights(rebalance="on_change") does not trade.  (The spec's absolute
  band of 5-20% of equity would block almost every entry: at a 20% book vol
  target a single coin's weight is only ~1-8% of equity.)
PIT universe (topk=10 on pit_top20): new positions only in the 10 coins with
  the largest trailing-30d quote volume among current top-20 members; an open
  position is kept (frozen size) while the coin stays a top-20 member and the
  signal keeps its sign.

All computations at bar i use data <= close of bar i (checked with
wf.check_causality).
"""
from __future__ import annotations

import hashlib
import math
from collections import OrderedDict

import numpy as np
import pandas as pd

LOOKBACKS_D = (5, 10, 20, 30, 60, 90, 150, 250, 360)

PANEL = dict(timeframe="6h", universe="majors", start="2020-01-01")
USES_METRICS = False
KIND = "weights"

BASE = dict(family="donch", direction="ls_ma", band=0.10, gate=1.0,
            vol_target=0.20, asset_cap=2.0, gross_cap=3.0, vol_days=60,
            bvol_days=90, gate_p=90.0, gate_ann=0.30, topk=None,
            lookbacks=LOOKBACKS_D)


def _grid():
    g = []
    for fam in ("donch", "tsmom"):
        for d in ("lo", "ls", "ls_ma"):
            for band in (0.05, 0.10, 0.20):
                for gate in (1.0, 0.5, 0.0):
                    g.append(dict(family=fam, direction=d, band=band, gate=gate))
    return g


GRID = _grid()                     # 54 configs
# FROZEN = the grid config with the best MEDIAN train Sharpe across the 7
# walk-forward folds (majors, 6h, dev 2020-01..2025-06); see results/trend_ens.json
FROZEN = dict(family="donch", direction="ls_ma", band=0.20, gate=0.0)


def P(params):
    q = dict(BASE)
    q.update(params or {})
    return q


# --------------------------------------------------------------------------- #
# caching of the param-independent heavy parts (keyed on the panel CONTENT)
# --------------------------------------------------------------------------- #
_CACHE: "OrderedDict[tuple, object]" = OrderedDict()
_CACHE_MAX = 16


def _pkey(panel):
    c = np.nan_to_num(np.asarray(panel.c, float), nan=-1.0)
    h = hashlib.md5(c.tobytes()).hexdigest()
    f = hashlib.md5(np.asarray(panel.funding, float).tobytes()).hexdigest()
    tr = hashlib.md5(np.asarray(panel.tradable, bool).tobytes()).hexdigest()
    return (len(panel.t), int(panel.t[0]), int(panel.dt), tuple(panel.symbols), h, f, tr)


def _cached(key, fn):
    if key in _CACHE:
        _CACHE.move_to_end(key)
        return _CACHE[key]
    v = fn()
    _CACHE[key] = v
    while len(_CACHE) > _CACHE_MAX:
        _CACHE.popitem(last=False)
    return v


def _bpd(panel):
    return 86400 // int(panel.dt)


def _ffill_close(panel):
    return pd.DataFrame(np.asarray(panel.c, float)).ffill().to_numpy()


def _base(panel):
    """ffilled close, log returns, per-asset sigma, 200d MA, eligibility, rank."""
    bpd = _bpd(panel)
    cf = _ffill_close(panel)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log(cf[1:] / cf[:-1])
    r = np.vstack([np.full((1, cf.shape[1]), np.nan), r])
    ann = math.sqrt(365.0 * bpd)
    out = {"cf": cf, "r": r, "ann": ann, "bpd": bpd}
    df = pd.DataFrame(r)
    out["sig"] = {}
    for vd in (60,):
        W = vd * bpd
        out["sig"][vd] = df.rolling(W, min_periods=W // 3).std().to_numpy() * ann
    out["ma200"] = pd.DataFrame(cf).rolling(200 * bpd, min_periods=200 * bpd).mean().to_numpy()
    # eligible = tradable (valid bar & PIT member) at the decision bar
    out["member"] = np.asarray(panel.tradable, bool)
    # trailing 30d quote volume rank among current members (0 = most liquid)
    qv = pd.DataFrame(np.nan_to_num(np.asarray(panel.qv, float)))
    q30 = qv.rolling(30 * bpd, min_periods=1).sum().to_numpy()
    q30 = np.where(out["member"], q30, -np.inf)
    order = np.argsort(-q30, axis=1, kind="stable")
    rank = np.empty_like(order)
    rows = np.arange(order.shape[0])[:, None]
    rank[rows, order] = np.arange(order.shape[1])[None, :]
    out["rank"] = rank
    return out


def _states(panel, family, lookbacks, return_stop=False):
    """[K, T, N] per-lookback states in {-1, 0, 1} (+ [K, N] trailing stops at the
    last bar when return_stop=True, donch only)."""
    B = _cached((_pkey(panel), "base"), lambda: _base(panel))
    cf = B["cf"]
    bpd = B["bpd"]
    T, N = cf.shape
    Ns = [int(d * bpd) for d in lookbacks]
    K = len(Ns)
    df = pd.DataFrame(cf)
    if family == "tsmom":
        st = np.zeros((K, T, N), np.int8)
        for k, n in enumerate(Ns):
            prev = df.shift(n).to_numpy()
            with np.errstate(invalid="ignore"):
                s = np.sign(cf - prev)
            st[k] = np.nan_to_num(s).astype(np.int8)
        return st
    if family != "donch":
        raise ValueError(family)
    st = np.zeros((K, T, N), np.int8)
    last_stop = np.full((K, N), np.nan)
    for k, n in enumerate(Ns):
        hi = df.rolling(n, min_periods=n).max().shift(1).to_numpy()
        lo = df.rolling(n, min_periods=n).min().shift(1).to_numpy()
        mid = 0.5 * (hi + lo)
        pos = np.zeros(N, np.int8)
        stop = np.full(N, np.nan)
        for i in range(T):
            c = cf[i]
            h, l, m = hi[i], lo[i], mid[i]
            ok = np.isfinite(h) & np.isfinite(c)
            L = pos == 1
            S_ = pos == -1
            # ratchet the trailing stops with this bar's channel midpoint
            mm = np.where(np.isfinite(m), m, stop)
            stop = np.where(L, np.fmax(stop, mm), stop)
            stop = np.where(S_, np.fmin(stop, mm), stop)
            # exits
            ex = (L & (c < stop)) | (S_ & (c > stop))
            pos = np.where(ex, 0, pos)
            # entries (also directly after an exit in the same bar)
            flat = pos == 0
            enL = flat & ok & (c > h)
            enS = flat & ok & (c < l)
            pos = np.where(enL, 1, np.where(enS, -1, pos))
            stop = np.where(enL | enS, m, stop)
            pos = np.where(ok, pos, 0).astype(np.int8)
            stop = np.where(pos == 0, np.nan, stop)
            st[k, i] = pos
        last_stop[k] = stop
    if return_stop:
        return st, last_stop
    return st


def _signal(panel, family, direction, lookbacks):
    st = _cached((_pkey(panel), "st", family, tuple(lookbacks)),
                 lambda: _states(panel, family, lookbacks))
    B = _cached((_pkey(panel), "base"), lambda: _base(panel))
    longp = np.clip(st, 0, 1).mean(axis=0)
    shortp = np.clip(st, -1, 0).mean(axis=0)
    if direction == "lo":
        return longp
    if direction == "ls":
        return longp + shortp
    if direction == "ls_ma":
        below = B["cf"] < B["ma200"]           # NaN MA -> False -> no shorts
        return longp + np.where(below, shortp, 0.0)
    raise ValueError(direction)


def _gate_state(panel, gate_p, gate_ann):
    """(long_blocked, short_blocked) [T, N] bool."""
    B = _cached((_pkey(panel), "base"), lambda: _base(panel))
    bpd = B["bpd"]
    f = np.asarray(panel.funding, float)
    s7 = pd.DataFrame(f).rolling(7 * bpd, min_periods=7 * bpd).sum().to_numpy()
    ann = s7 * 365.0 / 7.0
    T, N = f.shape
    W = 365
    pct = np.full((T, N), 50.0)
    for i in range(T):
        idx = np.arange(i, max(-1, i - W * bpd), -bpd)       # same time of day, trailing 365d
        if idx.size < 90:
            continue
        win = s7[idx]
        x = s7[i]
        valid = np.isfinite(win)
        cnt = valid.sum(axis=0)
        le = (np.where(valid, win, np.inf) <= x[None, :]).sum(axis=0)
        p = np.where((cnt >= 90) & np.isfinite(x), 100.0 * le / np.maximum(cnt, 1), 50.0)
        pct[i] = p
    with np.errstate(invalid="ignore"):
        lb = (pct >= gate_p) | (ann >= gate_ann)
        sb = (pct <= 100.0 - gate_p) | (ann <= -gate_ann)
    return np.nan_to_num(lb).astype(bool), np.nan_to_num(sb).astype(bool), pct, ann


def _pre_band(panel, q):
    """Target weights before band / gate / PIT-entry filter, and hold-only mask."""
    s = _signal(panel, q["family"], q["direction"], q["lookbacks"])
    B = _cached((_pkey(panel), "base"), lambda: _base(panel))
    sig = B["sig"][int(q["vol_days"])] if int(q["vol_days"]) in B["sig"] else None
    if sig is None:
        W = int(q["vol_days"]) * B["bpd"]
        sig = pd.DataFrame(B["r"]).rolling(W, min_periods=W // 3).std().to_numpy() * B["ann"]
    elig = B["member"] & np.isfinite(sig) & (sig > 0)
    if q.get("topk"):
        entry_ok = elig & (B["rank"] < int(q["topk"]))
    else:
        entry_ok = elig
    s = np.where(elig, s, 0.0)
    inv = np.where(elig, 1.0 / np.where(elig, sig, 1.0), 0.0)
    R = np.nan_to_num(B["r"])
    T, N = s.shape
    Wb = int(q["bvol_days"]) * B["bpd"]
    ann = B["ann"]
    vt = float(q.get("vol_target", 0.20))
    w = np.zeros((T, N))
    for i in range(T):
        act = entry_ok[i] & (s[i] != 0)
        if not act.any():
            continue
        idx = np.flatnonzero(act)
        wf_ = np.sign(s[i, idx]) * inv[i, idx]
        a = max(0, i - Wb + 1)
        x = R[a:i + 1, idx] @ wf_
        if x.size < 20:
            continue
        sd = x.std(ddof=1) * ann
        if not (sd > 0):
            continue
        k = vt / sd
        ww = k * s[i, idx] * inv[i, idx]
        ww = np.clip(ww, -q["asset_cap"], q["asset_cap"])
        g = np.abs(ww).sum()
        if g > q["gross_cap"]:
            ww *= q["gross_cap"] / g
        w[i, idx] = ww
    # hold-only candidates: members with a signal that are outside the entry set
    hold_ok = elig & ~entry_ok
    return w, s, hold_ok


def weights(panel, params, metrics=None):
    q = P(params)
    key = (_pkey(panel), "pre", q["family"], q["direction"], tuple(q["lookbacks"]),
           q["vol_days"], q["bvol_days"], q["asset_cap"], q["gross_cap"],
           q.get("vol_target", 0.2), q.get("topk"))
    w0, s, hold_ok = _cached(key, lambda: _pre_band(panel, q))
    gate = float(q["gate"])
    if gate < 1.0:
        lb, sb, _, _ = _cached((_pkey(panel), "gate", q["gate_p"], q["gate_ann"]),
                               lambda: _gate_state(panel, q["gate_p"], q["gate_ann"]))
    T, N = w0.shape
    band = float(q["band"])
    out = np.zeros((T, N))
    held = np.zeros(N)
    for i in range(T):
        tgt = w0[i].copy()
        # PIT: keep a held position (frozen) while its coin is still a member
        # outside the entry set and the signal keeps its sign
        ho = hold_ok[i]
        if ho.any():
            keep = ho & (np.sign(s[i]) == np.sign(held)) & (held != 0)
            tgt = np.where(keep, held, np.where(ho, 0.0, tgt))
        if gate < 1.0:
            base_l = np.maximum(held, 0.0)
            m = lb[i] & (tgt > base_l)
            tgt = np.where(m, base_l + gate * (tgt - base_l), tgt)
            base_s = np.minimum(held, 0.0)
            m = sb[i] & (tgt < base_s)
            tgt = np.where(m, base_s + gate * (tgt - base_s), tgt)
        chg = ((tgt == 0) & (held != 0)) | (np.sign(tgt) * np.sign(held) < 0) \
            | (np.abs(tgt - held) > band * np.maximum(np.abs(tgt), np.abs(held)))
        held = np.where(chg, tgt, held)
        out[i] = held
    return out


def live_targets(panel, params, metrics=None):
    """Targets as of the LAST bar (decided at its close, to be executed now)."""
    q = P(params)
    w = weights(panel, q)
    if q["family"] == "donch":
        st, lstop = _states(panel, "donch", q["lookbacks"], return_stop=True)
    else:
        st, lstop = _states(panel, "tsmom", q["lookbacks"]), None
    s = _signal(panel, q["family"], q["direction"], q["lookbacks"])
    lb, sb, pct, ann = _gate_state(panel, q["gate_p"], q["gate_ann"])
    B = _cached((_pkey(panel), "base"), lambda: _base(panel))
    cf = B["cf"]
    bpd = B["bpd"]
    out = {"as_of_bar_open": int(panel.t[-1]), "decided_at": int(panel.t[-1]) + int(panel.dt),
           "params": {k: (list(v) if isinstance(v, tuple) else v) for k, v in q.items()},
           "targets": {}, "resting_orders": [],
           "note": "target = signed notional / equity; place/resize at the next routine run; "
                   "the backtest checks Donchian entries/exits on 6h CLOSES only; each "
                   "lookback's trailing stop for the next bar is max(trailing_stop, next_mid) "
                   "for a long (min for a short). Server-side resting stops were NOT modelled."}
    i = len(panel.t) - 1
    for j, sym in enumerate(panel.symbols):
        if w[i, j] == 0 and s[i, j] == 0:
            continue
        levels = []
        for k, d in enumerate(q["lookbacks"]):
            n = int(d * bpd)
            if i - n < 0:
                continue
            win = cf[i - n + 1:i + 1, j]
            ts_ = None if lstop is None or not np.isfinite(lstop[k, j]) else float(lstop[k, j])
            levels.append({"lookback_d": d, "state": int(st[k, i, j]), "trailing_stop": ts_,
                           "next_entry_long_above": float(np.nanmax(win)),
                           "next_entry_short_below": float(np.nanmin(win)),
                           "next_mid": float(0.5 * (np.nanmax(win) + np.nanmin(win)))})
        out["targets"][sym] = {"weight": float(w[i, j]), "signal": float(s[i, j]),
                               "funding_pct": float(pct[i, j]),
                               "funding_ann": float(ann[i, j]) if np.isfinite(ann[i, j]) else None,
                               "long_gate": bool(lb[i, j]), "short_gate": bool(sb[i, j]),
                               "lookbacks": levels}
    return out
