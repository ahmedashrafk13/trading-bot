"""
backtest/lab/nulls.py -- "could a monkey have done this?" tests.

Both nulls keep WHAT the strategy holds (how often, how big, how long) and
destroy WHEN / WHICH WAY it holds it, then re-run the same simulator with the
same costs. A real edge should sit in the far right tail of the null.

random_timing_null(panel, weights, n=200, seed=0, method="auto")
    Per symbol, inside the span where it is tradable:
      "runs"  -- cut the weight series into runs of constant value and
                 shuffle the ORDER of the runs (same holding lengths, same
                 values, same number of changes; turnover approximately kept).
      "shift" -- circularly shift the whole series by a random offset
                 (exact turnover and exposure; for continuously varying
                 weights, where "runs" would shred the autocorrelation and
                 explode turnover).
      "auto"  -- "runs" when the average run is >= 3 bars, else "shift".
sign_flip_null(panel, weights, n=200, seed=0)
    Per symbol, each maximal run of same-signed non-zero weight has its sign
    flipped with probability 1/2: |weights| is unchanged, so gross exposure
    and holding periods are identical; only direction is randomised.

Both return {"stat", "strategy", "null" (array), "p_value", "percentile",
"method", "strategy_turnover", "null_turnover_mean", "strategy_exposure",
"null_exposure_mean"}. p_value = (1 + #null >= strategy) / (n + 1).
"""
from __future__ import annotations

import numpy as np

try:
    from . import metrics as M
    from . import sim as S
except ImportError:
    import metrics as M
    import sim as S


def _clean(panel, weights) -> np.ndarray:
    W = np.array(weights, dtype=float, copy=True)
    W[~np.isfinite(W)] = 0.0
    W[~S._tradable(panel)] = 0.0
    return W


def _spans(panel):
    tr = S._tradable(panel)
    out = []
    for j in range(tr.shape[1]):
        k = np.flatnonzero(tr[:, j])
        out.append((int(k[0]), int(k[-1]) + 1) if k.size else (0, 0))
    return out


def _runs(x: np.ndarray):
    """values, lengths of runs of equal consecutive values."""
    if x.size == 0:
        return x, np.array([], dtype=int)
    br = np.flatnonzero(np.diff(x) != 0) + 1
    starts = np.r_[0, br]
    lens = np.diff(np.r_[starts, x.size])
    return x[starts], lens


def _stat(res, stat):
    if stat == "sharpe":
        return M.fast_sharpe(res)
    if callable(stat):
        return float(stat(res))
    return float(M.equity_metrics(res.t, res.dt, res.equity, res.initial_equity)[stat])


def _null_loop(panel, W, make, n, seed, sim_kwargs, stat, method):
    kw = dict(sim_kwargs or {})
    kw["record_positions"] = False
    base = S.run_weights(panel, W, **kw)
    s0 = _stat(base, stat)
    rng = np.random.default_rng(seed)
    null = np.empty(n)
    to, ex = np.empty(n), np.empty(n)
    for k in range(n):
        res = S.run_weights(panel, make(rng), **kw)
        null[k] = _stat(res, stat)
        to[k], ex[k] = res.turnover, float(np.mean(res.gross_leverage))
    return {"stat": stat if isinstance(stat, str) else "custom", "strategy": s0,
            "null": null, "p_value": float((1 + np.sum(null >= s0)) / (n + 1)),
            "percentile": float(100.0 * np.mean(null < s0)), "method": method,
            "strategy_turnover": base.turnover, "null_turnover_mean": float(to.mean()),
            "strategy_exposure": float(np.mean(base.gross_leverage)),
            "null_exposure_mean": float(ex.mean()), "n": n, "seed": seed}


def random_timing_null(panel, weights, n: int = 200, seed: int = 0, *,
                       method: str = "auto", sim_kwargs: dict | None = None,
                       stat="sharpe") -> dict:
    W = _clean(panel, weights)
    spans = _spans(panel)
    T, N = W.shape
    runs = [_runs(W[a:b, j]) for j, (a, b) in enumerate(spans)]
    if method == "auto":
        lens = np.concatenate([r[1] for r in runs if r[1].size] or [np.array([1])])
        method = "runs" if lens.mean() >= 3 else "shift"
    if method not in ("runs", "shift"):
        raise ValueError("method must be auto|runs|shift")

    def make(rng):
        out = np.zeros_like(W)
        for j, (a, b) in enumerate(spans):
            if b - a < 2:
                continue
            if method == "runs":
                vals, lens = runs[j]
                p = rng.permutation(len(vals))
                out[a:b, j] = np.repeat(vals[p], lens[p])
            else:
                out[a:b, j] = np.roll(W[a:b, j], int(rng.integers(1, b - a)))
        return out

    return _null_loop(panel, W, make, n, seed, sim_kwargs, stat, method)


def sign_flip_null(panel, weights, n: int = 200, seed: int = 0, *,
                   sim_kwargs: dict | None = None, stat="sharpe") -> dict:
    W = _clean(panel, weights)
    sg = np.sign(W)
    # run id per symbol: increments whenever the sign changes
    brk = np.vstack([np.ones((1, W.shape[1]), bool), sg[1:] != sg[:-1]])
    rid = np.cumsum(brk, axis=0) - 1                  # [T, N] run index within column
    nruns = rid[-1] + 1

    def make(rng):
        out = W.copy()
        for j in range(W.shape[1]):
            flip = rng.random(int(nruns[j])) < 0.5
            out[:, j] *= np.where(flip[rid[:, j]], -1.0, 1.0)
        return out

    return _null_loop(panel, W, make, n, seed, sim_kwargs, stat, "sign_flip")
