"""
strategies/pairs.py -- rolling CAUSAL cointegration pairs (family C, research #3).

Mechanism: coins with the same factor exposure drift apart on idiosyncratic flow
and converge again. Pairs are re-selected every Monday 00:00 UTC from the
point-in-time top-30 using ONLY the past L days; they are then traded for the
next 7 days. Nothing about the trading week is known at selection time (the old
repo pairs.py chose pairs on the test data; this one cannot).

Formation (bar i whose CLOSE is Monday 00:00 UTC, data <= close i):
  * candidates: tradable (PIT top-30) at bar i, >= 95% valid bars over the window,
    no relisting inside the window;
  * every unordered pair, both orderings: OLS  log a = alpha + beta log b  (beta in
    [0.25, 4]); ADF(1) on the residual (no constant); Engle-Granger 5% critical
    value, MacKinnon (2010) N=2 with constant, finite-sample corrected; the ordering
    with the more negative t is kept;
  * OU half-life from the AR(1) of the residual, 0.5..10 days;
  * rank by ADF t, take up to max_pairs with no coin used twice.
Trading (decisions at every 6h close of the week, market orders at the next open):
  * z = (resid - mean) / sd with the formation mean/sd (fixed for the week);
  * enter when |z| > entry (short the spread when z > 0), exit when z crosses back
    through +-exit, stop when |z| > z_stop, time stop after `time_stop_days`;
  * no re-entry of a pair in the same week after a stop;
  * at the next formation an open pair is kept (same weights, same clock) only if it
    is re-selected; otherwise it is closed.
Sizing: equal risk. Leg-a notional s = pair_vol / (annualised vol of the spread's
bar-to-bar change in the formation window); leg b = -beta * s. pair_vol =
vol_target / sqrt(max_pairs), i.e. the book runs at vol_target when all slots are
full and the pair spreads are independent (it runs lower when slots are empty).
Weights are constant while a pair is open (no churn); fees, slippage and funding on
BOTH legs are charged by the simulator.

Cadence: z-scores cannot trigger server-side, so everything happens at the 6h runs;
needs_hourly_runs = False.
"""
from __future__ import annotations

import math

import numpy as np

PANEL = dict(timeframe="6h", universe="pit_top30", start="2020-01-01")
USES_METRICS = False
KIND = "weights"

WEEK = 7 * 86400
MONDAY_OFFSET = 4 * 86400            # epoch 0 was a Thursday; Monday 00:00 = t % WEEK == 4 days

_BASE = dict(pvalue="5%", hl_min_days=0.5, hl_max_days=10.0, z_stop=4.0,
             time_stop_days=5.0, max_pairs=5, vol_target=0.20, top_n=30,
             beta_min=0.25, beta_max=4.0, max_pair_gross=1.5, min_valid=0.95)

GRID = [dict(_BASE, lookback_days=L, entry_z=e, exit_z=x)
        for L in (21, 42, 90) for e in (1.5, 2.0, 2.5) for x in (0.0, 0.5)]

FROZEN = dict(_BASE, lookback_days=90, entry_z=2.5, exit_z=0.0)   # WF: most chosen (2/7 folds); verdict FAILS

# MacKinnon (2010) response-surface coefficients, N=2 variables, constant term
_MK = {"1%": (-3.89644, -10.9519, -22.527),
       "5%": (-3.33613, -6.1101, -6.823),
       "10%": (-3.04445, -4.2412, -2.720)}


def eg_critical(nobs: int, level: str = "5%") -> float:
    b0, b1, b2 = _MK[level]
    return b0 + b1 / nobs + b2 / nobs ** 2


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _bars_per_day(panel) -> float:
    return 86400.0 / float(panel.dt)


def _formation_bars(panel) -> np.ndarray:
    close = np.asarray(panel.t, np.int64) + int(panel.dt)
    return np.flatnonzero(close % WEEK == MONDAY_OFFSET)


def _valid(panel):
    v = panel.meta.get("valid") if isinstance(panel.meta, dict) else None
    if v is None:
        v = np.isfinite(panel.c) & (np.nan_to_num(panel.v) > 0)
    return v


_FORM_CACHE: dict = {}


def _formation(panel, i: int, p: dict, rng=None):
    """Select pairs at bar i using bars (i - W, i] only. Returns a list of dicts.
    rng given -> RANDOM pairs (null): same candidates, same OLS hedge, same beta
    bounds, but no cointegration / half-life test."""
    bpd = _bars_per_day(panel)
    W = int(round(p["lookback_days"] * bpd))
    if i + 1 < W:
        return []
    a0 = i + 1 - W
    trad = panel.tradable[i]
    valid = _valid(panel)[a0:i + 1]
    fr = valid.mean(axis=0)
    rel = panel.meta.get("relisted") if isinstance(panel.meta, dict) else None
    relw = rel[a0 + 1:i + 1].any(axis=0) if rel is not None else np.zeros(len(trad), bool)
    cand = np.flatnonzero(trad & (fr >= p["min_valid"]) & ~relw
                          & np.isfinite(panel.c[a0:i + 1]).all(axis=0))
    if cand.size < 2:
        return []
    key = None
    if rng is None:
        C = panel.c[a0:i + 1, cand]
        key = (tuple(panel.symbols[j] for j in cand), int(panel.t[i]), int(panel.dt), W,
               float(np.nansum(C)), p["pvalue"], p["hl_min_days"], p["hl_max_days"],
               p["beta_min"], p["beta_max"], p["max_pairs"])
        hit = _FORM_CACHE.get(key)
        if hit is not None:
            return hit
    X = np.log(panel.c[a0:i + 1, cand])                # [W, n]
    n = cand.size
    ia, ib = np.triu_indices(n, 1)
    A = np.concatenate([ia, ib])                        # both orderings
    B = np.concatenate([ib, ia])
    if rng is not None:
        perm = rng.permutation(A.size)
        A, B = A[perm], B[perm]
    Xm = X - X.mean(axis=0)
    var = (Xm ** 2).sum(axis=0)
    cov = Xm[:, A] * Xm[:, B]
    beta = cov.sum(axis=0) / np.where(var[B] > 0, var[B], np.nan)
    E = Xm[:, A] - beta * Xm[:, B]                      # residual (mean 0 by OLS)
    dE = np.diff(E, axis=0)
    y = dE[1:]                                          # ADF(1): dE_t = g E_{t-1} + d dE_{t-1}
    x1 = E[1:-1]
    x2 = dE[:-1]
    s11, s22, s12 = (x1 * x1).sum(0), (x2 * x2).sum(0), (x1 * x2).sum(0)
    s1y, s2y = (x1 * y).sum(0), (x2 * y).sum(0)
    det = s11 * s22 - s12 ** 2
    with np.errstate(invalid="ignore", divide="ignore"):
        g = (s22 * s1y - s12 * s2y) / det
        d = (s11 * s2y - s12 * s1y) / det
        res = y - g * x1 - d * x2
        dof = y.shape[0] - 2
        s2 = (res ** 2).sum(0) / dof
        tstat = g / np.sqrt(s2 * s22 / det)
        # AR(1) half-life of the residual
        ga = (x1 * dE[1:]).sum(0) / s11
        hl_days = -math.log(2) / np.log1p(ga) / bpd
    ok_beta = (beta >= p["beta_min"]) & (beta <= p["beta_max"]) & np.isfinite(beta)
    if rng is None:
        crit = eg_critical(W, p["pvalue"])
        ok = ok_beta & (tstat < crit) & (ga < 0) & (hl_days >= p["hl_min_days"]) \
            & (hl_days <= p["hl_max_days"])
        order = np.argsort(tstat)
    else:
        ok = ok_beta
        order = np.arange(A.size)                        # already shuffled
    used, out = set(), []
    for k in order:
        if not ok[k]:
            continue
        ja, jb = int(cand[A[k]]), int(cand[B[k]])
        if ja in used or jb in used:
            continue
        e = E[:, k]
        mu, sd = float(e.mean()), float(e.std(ddof=1))
        alpha = float(X[:, A[k]].mean() - beta[k] * X[:, B[k]].mean())
        sv = float(np.std(np.diff(e), ddof=1) * math.sqrt(365.0 * bpd))
        if not (sd > 0 and sv > 0):
            continue
        out.append(dict(a=ja, b=jb, beta=float(beta[k]), alpha=alpha, mu=mu, sd=sd,
                        spread_vol=sv, t=float(tstat[k]), hl=float(hl_days[k])))
        used.update((ja, jb))
        if len(out) >= p["max_pairs"]:
            break
    if key is not None:
        if len(_FORM_CACHE) > 20000:
            _FORM_CACHE.clear()
        _FORM_CACHE[key] = out
    return out


def _simulate_pairs(panel, params, rng=None, log=None):
    """Core: weights [T, N]; optional trade log (list) for live_targets/diagnostics."""
    p = dict(_BASE)
    p.update(params or {})
    T, N = panel.c.shape
    Wt = np.zeros((T, N))
    if T < 2:
        return Wt
    bpd = _bars_per_day(panel)
    tstop = int(round(p["time_stop_days"] * bpd))
    pair_vol = p["vol_target"] / math.sqrt(p["max_pairs"])
    logc = np.log(np.where(panel.c > 0, panel.c, np.nan))
    valid = _valid(panel)
    fbars = _formation_bars(panel)
    open_pos = {}          # (a, b) -> dict(side, wa, wb, start, pair)
    for fi, i in enumerate(fbars):
        end = fbars[fi + 1] if fi + 1 < len(fbars) else T      # decisions on bars [i, end)
        sel = _formation(panel, int(i), p, rng)
        selkey = {(q["a"], q["b"]): q for q in sel}
        # carry re-selected open pairs, close the rest
        open_pos = {k: dict(v, pair=selkey[k]) for k, v in open_pos.items() if k in selkey}
        stopped = set()
        for k in range(int(i), int(end)):
            for key, q in selkey.items():
                a, b = key
                if not (valid[k, a] and valid[k, b]):
                    z = np.nan
                else:
                    e = logc[k, a] - q["alpha"] - q["beta"] * logc[k, b]
                    z = (e - q["mu"]) / q["sd"]
                pos = open_pos.get(key)
                if pos is not None:
                    side = pos["side"]
                    close = False
                    if not (panel.tradable[k, a] and panel.tradable[k, b]):
                        # the simulator force-closes a non-tradable leg (left the PIT
                        # top-30 / no bar); never leave the other leg naked
                        close, why = True, "untradable"
                    elif not np.isfinite(z):
                        close, why = True, "nodata"
                    else:
                        if abs(z) > p["z_stop"]:
                            close, why = True, "stop"
                            stopped.add(key)
                        elif (side < 0 and z <= p["exit_z"]) or (side > 0 and z >= -p["exit_z"]):
                            close, why = True, "exit"
                        elif k - pos["start"] >= tstop:
                            close, why = True, "time"
                    if close:
                        del open_pos[key]
                        if log is not None:
                            log.append(dict(kind="close", bar=k, a=a, b=b, z=float(z)))
                    continue
                if key in stopped or not np.isfinite(z):
                    continue
                if not (panel.tradable[k, a] and panel.tradable[k, b]):
                    continue
                if abs(z) > p["entry_z"] and abs(z) < p["z_stop"]:
                    side = -1 if z > 0 else 1              # long spread = long a, short beta*b
                    s = pair_vol / q["spread_vol"]
                    g = s * (1.0 + q["beta"])
                    if g > p["max_pair_gross"]:
                        s *= p["max_pair_gross"] / g
                    open_pos[key] = dict(side=side, wa=side * s, wb=-side * s * q["beta"],
                                         start=k, pair=q)
                    if log is not None:
                        log.append(dict(kind="open", bar=k, a=a, b=b, z=float(z), side=side))
            row = Wt[k]
            for key, pos in open_pos.items():
                row[key[0]] += pos["wa"]
                row[key[1]] += pos["wb"]
        if end == T:
            break
    # bars before the first formation stay flat
    return Wt


# --------------------------------------------------------------------------- #
# contract
# --------------------------------------------------------------------------- #
def weights(panel, params, metrics=None) -> np.ndarray:
    return _simulate_pairs(panel, params)


def random_pairs_weights(panel, params, seed: int) -> np.ndarray:
    """Null: random disjoint pairs each week (OLS hedge, same beta bounds, same
    entry/exit/stop/time rules and sizing), no cointegration or half-life test."""
    return _simulate_pairs(panel, params, rng=np.random.default_rng(seed))


def live_targets(panel, params, metrics=None) -> dict:
    """Target notional/equity per symbol after the LAST bar + the active pairs."""
    p = dict(_BASE)
    p.update(params or {})
    W = _simulate_pairs(panel, p)
    last = W[-1]
    fb = _formation_bars(panel)
    fb = fb[fb <= len(panel.t) - 1]
    pairs = []
    if fb.size:
        for q in _formation(panel, int(fb[-1]), p):
            pairs.append(dict(long_leg_if_spread_long=panel.symbols[q["a"]],
                              short_leg_if_spread_long=panel.symbols[q["b"]],
                              beta=q["beta"], alpha=q["alpha"], mu=q["mu"], sd=q["sd"],
                              adf_t=q["t"], half_life_days=q["hl"]))
    return {"as_of": str(np.datetime64(int(panel.t[-1]) + int(panel.dt), "s")),
            "targets": {panel.symbols[j]: float(last[j]) for j in np.flatnonzero(last)},
            "resting_orders": [],
            "selected_pairs": pairs,
            "note": "market orders at the next 6h run; no server-side trigger possible "
                    "for a spread z-score; each leg should carry a wide catastrophe stopLoss"}
