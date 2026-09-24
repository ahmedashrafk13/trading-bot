"""
strategies/xsmom.py -- cross-sectional momentum / residual momentum / CTREND-lite
(family C, research #7). Market-neutral or BTC-hedged, vol-targeted, daily bars,
point-in-time top-30 Binance USDT-M perps (delisted coins included).

Scores at the close of rebalance bar i (data <= close i only):
  mom     sum of daily log returns over (i-skip-L, i-skip]
  resid   same sum of BTC-residual returns r - beta*r_btc (beta: trailing 60d OLS)
  ctrend  mean cross-sectional percentile rank of close/SMA_k - 1 for
          k in (5,10,20,50,100,200) plus a volume trend log(SMA5(qv)/SMA50(qv))
          (CTREND-lite; Fieberg et al. 2025 combine ~28 such signals by regression)
  rev     minus the L-day return (short-term reversal; used by strategies/xsrev.py)
Book (constant weights until the next rebalance; units drift in between):
  ls_beta   long the top-k, short the bottom-k, equal notional per name, then a BTC
            position that sets the book's trailing 60d beta to BTC to zero
  ls_dollar long top-k / short bottom-k, equal notional, no BTC overlay
  long_btc  long the top-k, equal notional, BTC short = -(portfolio beta)
The whole book is scaled so its trailing 60d covariance-implied vol equals
params["vol_target"] (default 0.20), gross capped at max_gross (3.0).
Rebalance: every 7 days at Monday 00:00 UTC, or every 3 days / every day at
00:00 UTC -- all of them 6h decision points, so needs_hourly_runs = False.
Returns never cross a relisting (meta["relisted"]) or a missing bar.
"""
from __future__ import annotations

import math

import numpy as np

PANEL = dict(timeframe="1d", universe="pit_top30", start="2020-01-01")
USES_METRICS = False
KIND = "weights"

WEEK = 7 * 86400
DAY = 86400
MONDAY_OFFSET = 4 * 86400
CT_WINDOWS = (5, 10, 20, 50, 100, 200)

_BASE = dict(vol_target=0.20, max_gross=3.0, cov_days=60, beta_days=60, skip=0)

_SIGNALS = ([dict(signal="mom", lookback=L, skip=0) for L in (7, 14, 30, 60)]
            + [dict(signal="mom", lookback=L, skip=1) for L in (14, 30)]
            + [dict(signal="resid", lookback=L, skip=0) for L in (14, 30)]
            + [dict(signal="ctrend", lookback=0, skip=0)])

GRID = [dict(_BASE, **s, k=k, hedge=h, rebalance_days=rb)
        for s in _SIGNALS for k in (3, 5) for h in ("ls_beta", "long_btc") for rb in (7, 3)]

FROZEN = dict(_BASE, signal="ctrend", lookback=0, skip=0, k=3, hedge="ls_beta",
              rebalance_days=7)                    # WF: most chosen (2/7 folds, the last two)


# --------------------------------------------------------------------------- #
# building blocks (all causal: row i uses rows <= i)
# --------------------------------------------------------------------------- #
def _valid(panel):
    v = panel.meta.get("valid") if isinstance(panel.meta, dict) else None
    if v is None:
        v = np.isfinite(panel.c) & (np.nan_to_num(panel.v) > 0)
    return v


def log_returns(panel) -> np.ndarray:
    c = panel.c
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log(c[1:] / c[:-1])
    r = np.vstack([np.full((1, c.shape[1]), np.nan), r])
    rel = panel.meta.get("relisted") if isinstance(panel.meta, dict) else None
    if rel is not None:
        r[np.asarray(rel, bool)] = np.nan
    r[~np.isfinite(r)] = np.nan
    return r


def _rolling_sum(x: np.ndarray, L: int, min_frac: float = 0.8):
    """Sum of the last L rows (rows i-L+1..i), NaN where < min_frac*L finite."""
    T = x.shape[0]
    f = np.isfinite(x)
    z = np.where(f, x, 0.0)
    cs = np.vstack([np.zeros((1, x.shape[1])), np.cumsum(z, axis=0)])
    cn = np.vstack([np.zeros((1, x.shape[1])), np.cumsum(f, axis=0)])
    out = np.full(x.shape, np.nan)
    if T >= L:
        s = cs[L:] - cs[:-L]
        n = cn[L:] - cn[:-L]
        out[L - 1:] = np.where(n >= math.ceil(min_frac * L), s, np.nan)
    return out


def _rolling_mean(x, L, min_frac=1.0):
    s = _rolling_sum(x, L, min_frac)
    return s / L


def _shift(x, s):
    if s == 0:
        return x
    out = np.full(x.shape, np.nan)
    out[s:] = x[:-s]
    return out


def rolling_beta(r: np.ndarray, rb: np.ndarray, L: int) -> np.ndarray:
    """OLS beta of every column of r on rb over the last L rows (pairwise-complete)."""
    m = np.isfinite(r) & np.isfinite(rb)[:, None]
    x = np.where(m, rb[:, None], 0.0)
    y = np.where(m, r, 0.0)

    def rs(a):
        cs = np.vstack([np.zeros((1, a.shape[1])), np.cumsum(a, axis=0)])
        o = np.full(a.shape, np.nan)
        o[L - 1:] = cs[L:] - cs[:-L]
        return o
    n = rs(m.astype(float))
    sx, sy, sxx, sxy = rs(x), rs(y), rs(x * x), rs(x * y)
    with np.errstate(invalid="ignore", divide="ignore"):
        cov = sxy / n - sx * sy / n ** 2
        var = sxx / n - (sx / n) ** 2
        b = cov / var
    b[n < 0.8 * L] = np.nan
    return b


def _xs_rank(x: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Cross-sectional percentile rank (0..1) per row among mask & finite."""
    out = np.full(x.shape, np.nan)
    for i in range(x.shape[0]):
        m = mask[i] & np.isfinite(x[i])
        n = int(m.sum())
        if n < 2:
            continue
        v = x[i, m]
        rk = np.argsort(np.argsort(v, kind="mergesort"), kind="mergesort")
        out[i, np.flatnonzero(m)] = rk / (n - 1)
    return out


def rebalance_bars(panel, every_days: int) -> np.ndarray:
    close = np.asarray(panel.t, np.int64) + int(panel.dt)
    if every_days == 7:
        return close % WEEK == MONDAY_OFFSET
    if every_days == 1:
        return close % DAY == 0
    return (close % DAY == 0) & ((close // DAY) % every_days == 0)


def score(panel, params, r=None, btc_beta=None) -> np.ndarray:
    p = dict(_BASE)
    p.update(params)
    if r is None:
        r = log_returns(panel)
    sig, L, s = p["signal"], int(p.get("lookback", 0)), int(p.get("skip", 0))
    if sig == "mom":
        return _shift(_rolling_sum(r, L), s)
    if sig == "rev":
        return -_shift(_rolling_sum(r, L, 1.0), s)
    if sig == "resid":
        jb = panel.symbols.index("BTCUSDT")
        if btc_beta is None:
            btc_beta = rolling_beta(r, r[:, jb], p["beta_days"])
        # beta known at i-1 applied to return i (no same-bar beta estimation)
        eps = r - _shift(btc_beta, 1) * r[:, [jb]]
        return _shift(_rolling_sum(eps, L), s)
    if sig == "ctrend":
        c = np.where(_valid(panel), panel.c, np.nan)
        mask = panel.tradable
        comps = []
        for k in CT_WINDOWS:
            ma = _rolling_mean(c, k, 0.9)
            comps.append(_xs_rank(c / ma - 1.0, mask))
        qv = np.where(_valid(panel), panel.qv, np.nan)
        vt = np.log(_rolling_mean(qv, 5, 1.0) / _rolling_mean(qv, 50, 0.9))
        comps.append(_xs_rank(vt, mask))
        st = np.stack(comps)
        cnt = np.isfinite(st).sum(0)
        with np.errstate(invalid="ignore"):
            out = np.nanmean(np.where(np.isfinite(st), st, np.nan), axis=0) \
                if cnt.any() else np.full(c.shape, np.nan)
        out[cnt < 4] = np.nan                     # need at least 4 of the 7 components
        return out
    raise ValueError(f"unknown signal {sig!r}")


def build(panel, params, rng=None) -> np.ndarray:
    """Target weights. rng given -> NULL book: the same eligible set, k, hedge,
    rebalance dates and vol targeting, but longs/shorts drawn at random."""
    p = dict(_BASE)
    p.update(params)
    T, N = panel.c.shape
    W = np.zeros((T, N))
    if "BTCUSDT" not in panel.symbols or T < 3:
        return W
    jb = panel.symbols.index("BTCUSDT")
    r = log_returns(panel)
    beta = rolling_beta(r, r[:, jb], p["beta_days"])
    sc = score(panel, p, r=r, btc_beta=beta)
    reb = rebalance_bars(panel, int(p["rebalance_days"]))
    nvalid = _rolling_sum(np.isfinite(r).astype(float), p["cov_days"], 0.0)
    k = int(p["k"])
    hedge = p["hedge"]
    cur = np.zeros(N)
    started = False
    Lc = int(p["cov_days"])
    for i in range(T):
        if reb[i]:
            elig = (panel.tradable[i] & np.isfinite(sc[i]) & np.isfinite(beta[i])
                    & (np.nan_to_num(nvalid[i]) >= 0.8 * Lc))
            if hedge == "long_btc":
                elig[jb] = False                  # BTC is the hedge leg
            idx = np.flatnonzero(elig)
            need = k if hedge == "long_btc" else 2 * k
            new = np.zeros(N)
            if idx.size >= need and panel.tradable[i, jb]:
                if rng is None:
                    o = idx[np.argsort(sc[i, idx], kind="mergesort")]
                    longs, shorts = o[-k:], o[:k]
                else:
                    o = rng.permutation(idx)
                    longs, shorts = o[:k], o[k:2 * k]
                new[longs] += 1.0 / k
                if hedge in ("ls_beta", "ls_dollar"):
                    new[shorts] -= 1.0 / k
                if hedge in ("ls_beta", "long_btc"):
                    nb = float(np.nansum(new * beta[i]))
                    new[jb] -= nb
                # vol target from the trailing covariance (rows i-Lc+1..i)
                act = np.flatnonzero(new)
                R = r[max(0, i - Lc + 1):i + 1, act]
                R = np.where(np.isfinite(R), R, 0.0)
                if R.shape[0] >= 20:
                    cv = np.cov(R, rowvar=False)
                    cv = np.atleast_2d(cv)
                    v = float(new[act] @ cv @ new[act])
                    if v > 0:
                        sc_ = p["vol_target"] / math.sqrt(v * 365.0)
                        g = np.abs(new).sum() * sc_
                        if g > p["max_gross"]:
                            sc_ *= p["max_gross"] / g
                        new *= sc_
                    else:
                        new[:] = 0.0
                else:
                    new[:] = 0.0
            cur = new
            started = True
        if started:
            W[i] = cur
    return W


# --------------------------------------------------------------------------- #
# contract
# --------------------------------------------------------------------------- #
def weights(panel, params, metrics=None) -> np.ndarray:
    return build(panel, params)


def null_weights(panel, params, seed: int) -> np.ndarray:
    return build(panel, params, rng=np.random.default_rng(seed))


def live_targets(panel, params, metrics=None) -> dict:
    W = build(panel, params)
    last = W[-1]
    reb = rebalance_bars(panel, int(dict(_BASE, **params)["rebalance_days"]))
    lr = np.flatnonzero(reb)
    return {"as_of": str(np.datetime64(int(panel.t[-1]) + int(panel.dt), "s")),
            "last_rebalance": (str(np.datetime64(int(panel.t[lr[-1]]) + int(panel.dt), "s"))
                               if lr.size else None),
            "is_rebalance_bar": bool(reb[-1]),
            "targets": {panel.symbols[j]: float(last[j]) for j in np.flatnonzero(last)},
            "resting_orders": [],
            "note": "market orders at the 00:07 UTC run on rebalance days only; hold "
                    "units (no re-sizing) between rebalances"}
