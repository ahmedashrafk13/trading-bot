"""Shared helpers for the family-E (order-flow / positioning) screens and modules.

Not a strategy module (leading underscore). numpy/pandas only.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

H6 = 21600
TRAIN_END = pd.Timestamp("2024-01-01", tz="UTC").value // 10**9     # train < this
TEST_END = pd.Timestamp("2025-07-01", tz="UTC").value // 10**9      # lockbox start


# --------------------------------------------------------------------------- #
# regressions
# --------------------------------------------------------------------------- #
def ols_nw(y, X, lags):
    """OLS of y on X (X already contains a constant if wanted) with Newey-West
    (Bartlett) standard errors. Rows with any NaN dropped (order preserved)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X = y[ok], X[ok]
    n, k = X.shape
    if n <= k + 5:
        return None
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    S = u.T @ u
    L = int(max(0, lags))
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        G = u[l:].T @ u[:-l]
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(V), 1e-300))
    return {"b": b, "t": b / se, "n": int(n)}


def mean_nw_t(x, lags):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < 10:
        return np.nan, np.nan, int(x.size)
    r = ols_nw(x, np.ones((x.size, 1)), lags)
    return float(r["b"][0]), float(r["t"][0]), int(x.size)


def rank_cs(A):
    """Cross-sectional rank transform to [-0.5, 0.5] per row (NaN kept)."""
    df = pd.DataFrame(A)
    r = df.rank(axis=1, pct=True)
    cnt = df.notna().sum(1)
    # centre: pct ranks in (0,1]; subtract row mean
    r = r.sub(r.mean(axis=1), axis=0)
    r[cnt < 5] = np.nan
    return r.to_numpy()


def fama_macbeth(y, Xs, lags, min_n=8):
    """Per-row cross-sectional OLS of y[T,N] on regressors Xs (list of [T,N])
    with a constant; returns per-coefficient mean and NW t over rows."""
    T, N = y.shape
    K = len(Xs)
    coefs = np.full((T, K), np.nan)
    for i in range(T):
        yi = y[i]
        Xi = np.column_stack([x[i] for x in Xs])
        ok = np.isfinite(yi) & np.isfinite(Xi).all(1)
        if ok.sum() < max(min_n, K + 3):
            continue
        A = np.column_stack([np.ones(ok.sum()), Xi[ok]])
        b, *_ = np.linalg.lstsq(A, yi[ok], rcond=None)
        coefs[i] = b[1:]
    out = []
    for k in range(K):
        m, t, n = mean_nw_t(coefs[:, k], lags)
        out.append({"coef": m, "t": t, "n_periods": n})
    return out, coefs


def cs_ic(sig, fwd, lags, min_n=8):
    """Mean cross-sectional Spearman IC with NW t."""
    rs = rank_cs(sig)
    rf = rank_cs(fwd)
    ok = np.isfinite(rs) & np.isfinite(rf)
    ics = np.full(sig.shape[0], np.nan)
    for i in range(sig.shape[0]):
        k = ok[i]
        if k.sum() >= min_n:
            a, b = rs[i, k], rf[i, k]
            sa, sb = a.std(), b.std()
            if sa > 0 and sb > 0:
                ics[i] = np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb)
    m, t, n = mean_nw_t(ics, lags)
    return {"ic": m, "t": t, "n_periods": n}


# --------------------------------------------------------------------------- #
# rolling helpers (on 1-D or [T,N] sampled series, causal, window incl. current)
# --------------------------------------------------------------------------- #
def roll_mean(A, n, minp):
    return pd.DataFrame(A).rolling(n, min_periods=minp).mean().to_numpy()


def roll_z(A, n, minp):
    df = pd.DataFrame(A)
    m = df.rolling(n, min_periods=minp).mean()
    s = df.rolling(n, min_periods=minp).std(ddof=0)
    return np.array(((df - m) / s.where(s > 0)).to_numpy(), copy=True)


def roll_resid_z(y, x, n, minp):
    """Residual of a trailing rolling OLS y ~ a + b x (window of n samples
    INCLUDING the current one), divided by the window residual std. Causal."""
    y = np.asarray(y, float).copy()
    x = np.asarray(x, float).copy()
    bad = ~(np.isfinite(y) & np.isfinite(x))
    y[bad] = np.nan
    x[bad] = np.nan
    Y, X = pd.DataFrame(y), pd.DataFrame(x)
    r = lambda D: D.rolling(n, min_periods=minp).mean()
    mx, my = r(X), r(Y)
    vx = r(X * X) - mx * mx
    vy = r(Y * Y) - my * my
    cxy = r(X * Y) - mx * my
    b = cxy / vx.where(vx > 1e-18)
    a = my - b * mx
    e = Y - a - b * X
    rv = vy - b * cxy
    z = e / np.sqrt(rv.where(rv > 1e-18))
    return np.array(z.to_numpy(), copy=True)


def fwd_log_ret(c, h):
    """fwd[i] = ln c[i+h] - ln c[i] (NaN at the end)."""
    lc = np.log(c)
    out = np.full_like(lc, np.nan)
    out[:-h] = lc[h:] - lc[:-h]
    return out


def back_log_ret(c, h):
    lc = np.log(c)
    out = np.full_like(lc, np.nan)
    out[h:] = lc[h:] - lc[:-h]
    return out


def halves(t):
    """Boolean masks (train, test) on sample times t (decision time = bar close)."""
    t = np.asarray(t)
    return t < TRAIN_END, (t >= TRAIN_END) & (t < TEST_END)


def fmt(x, nd=4):
    try:
        return None if x is None or not np.isfinite(x) else round(float(x), nd)
    except TypeError:
        return x


def ols_dk(y, Xs, lags):
    """Pooled OLS of y[T,N] on a constant + regressors Xs ([T,N] each) with
    Driscoll-Kraay standard errors: per-period moment sums over symbols, then
    Newey-West over time (robust to cross-sectional AND serial correlation)."""
    y = np.asarray(y, float)
    T, N = y.shape
    X = np.stack([np.ones((T, N))] + [np.asarray(x, float) for x in Xs], axis=2)  # T,N,K
    ok = np.isfinite(y) & np.isfinite(X).all(2)
    K = X.shape[2]
    if ok.sum() <= K + 5:
        return None
    Xf, yf = X[ok], y[ok]
    XtX_inv = np.linalg.pinv(Xf.T @ Xf)
    b = XtX_inv @ Xf.T @ yf
    e = np.where(ok, y - np.einsum("tnk,k->tn", np.nan_to_num(X), b), 0.0)
    h = np.einsum("tnk,tn->tk", np.nan_to_num(X) * ok[:, :, None], e)     # T,K
    h = h[ok.any(1)]
    S = h.T @ h
    L = int(max(0, lags))
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        G = h[l:].T @ h[:-l]
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(V), 1e-300))
    return {"b": b, "t": b / se, "n": int(ok.sum())}
