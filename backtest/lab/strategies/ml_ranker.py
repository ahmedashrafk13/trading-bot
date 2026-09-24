"""ml_ranker - machine-learning cross-sectional ranker on the PIT top-50 perps (family H).

PRE-REGISTERED 2026-09-24 (written before any walk-forward / IC was computed on this design).

Hypothesis
  The order-flow / positioning edge found in phase 2 (taker-buy share, crowd L/S, funding) and the
  weak price effects (short-term reversal, medium-term momentum, low-vol) are each too small to pay
  the fees alone. A conservatively regularised model that COMBINES ~25 causal, cross-sectionally
  ranked features (and, for LightGBM, their interactions with the market regime) ranks next-H-day
  returns better than (a) a linear ridge fit and (b) the no-fitting equal-weight average of the
  pre-signed features. ML is only worth anything if it beats (b) out of sample.

Decisions / timing
  1d bars (decision at the 00:00 UTC close, executed at the next 6h run 00:07 = next open in the sim).
  Features at bar i use data <= close i. Target of sample i = ln(open[i+1+H] / open[i+1]) (exactly the
  execution window), converted to a centred cross-sectional pct rank among names tradable at i.

Features (each ranked cross-sectionally among tradable names at every decision -> [-0.5, 0.5])
  price : r1, r3, r7, r14, r30, r60 (log returns), rv7, rv30 (std of daily log returns),
          volvol (30d std of rv7 / its 30d mean), dhi = ln(c / 30d max high), dlo = ln(c / 30d min low)
  volume: vz7 = ln(mean qv 7d / mean qv 30d), vz30 = 30d z of ln(qv) today
  flow  : tb1 = 24h taker-buy share, tb7 = 7d taker-buy share (tbqv / qv)
  carry : f1 = funding settled in the day, f7 = 7d funding sum, df = f1 - f7/7
  crowd (load_metrics, 53 coins, from ~2021-12, max_stale 2h; NaN elsewhere):
          zG = 30d z of ln(global L/S account ratio), zT = same for the top-trader position ratio,
          D = zT - zG, oi1 / oi7 = 1d / 7d log change of OI value
  regime (NOT ranked, same for every name, LightGBM only): BTC r7, r30, rv30; day of week.
  Ridge: NaN -> 0 (the rank median) + one missing indicator per metric group (ls, top, oi).

Pre-registered signs for the no-fitting baseline 'ew' (mean of sign * rank over available features):
  r1 -, r3 -, r7 +, r14 +, r30 +, r60 +, rv7 -, rv30 -, volvol -, dhi +, dlo +, vz7 -, vz30 -,
  tb1 +, tb7 +, f1 -, f7 -, df -, zG -, zT +, D +, oi1 -, oi7 -.

Models (retrained INSIDE the strategy on an absolute 91-day grid anchored 2020-01-01; the model
used at bar i is the last one fitted at a grid close <= close i; no saved model):
  lgbm : LGBMRegressor on the rank target, num_leaves 15, min_data_in_leaf 300, feature_fraction 0.7,
         bagging 0.7 every iteration, lambda_l2 10, learning_rate 0.03, 300 trees, deterministic,
         2 threads, seed 0.
  ridge: numpy ridge, alpha = 0.05 * n_samples (on rank features), intercept.
  ew   : equal-weight pre-signed baseline (no fitting).
  Training window at retrain close r: samples i with r - 730d < close_i <= r - 2H days (label
  realised by r - H; embargo = H more days), rolling. A retrain happens only with >= 240 sample
  dates of >= 15 names; before the first fit the book is flat.

Portfolio (per decision): long top-k / short bottom-k of the prediction, equal weight +-0.5/k per
  side (dollar neutral), rank buffer (a held name stays while inside the top/bottom 2k), H-day
  overlapping hold (stagger H), book vol-targeted to params["vol_target"] (60d realised, gross <= 3),
  per-name cap |w| <= 0.25, 0.02 weight band, non-tradable -> 0.

GRID (12 configs, every one counted as a trial): model in {lgbm, ridge, ew} x H in {1, 3} x k in {5, 10}.
  Headline = the lgbm family (4 configs) walk-forward; ridge and ew families run the same way for the
  comparison, plus a full-12 selection. Outer walk-forward: rolling 365d selection window, 182d test,
  first train window 2021-01-01 (first model fit ~2020-12-30), OOS 2022-01 .. 2025-06.
  Pre-registered robustness variants (counted as 2 extra trials): expanding train window, and a
  sign(return beyond 2x round-trip cost) classification target, both on the FROZEN lgbm config.

Verdict (pre-registered): the family-E default_verdict (strategies/_micro_harness.py) on the lgbm
  family, then downgraded one level if the lgbm OOS Sharpe does not exceed the ew baseline's OOS Sharpe
  (same walk-forward, same costs): ML must beat the no-fitting baseline to count.
Protective stops: estimated with a per-name stop overlay re-armed at each daily run (10 / 15 / 25 %
  from the run price, stop fill at the level with fee + 3x tier slippage, re-entry at the next open).

Live retrain cadence: live_targets() runs weights() on the trailing panel; it refits the model on
  the last 91-day grid date (<= the current close) from the trailing 730 days, i.e. ONE refit per
  quarter (models are cached in-process; a fresh process simply refits, ~seconds). Daily 00:07 run.
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data  # noqa: E402
from lab.strategies import _micro_harness as HX  # noqa: E402

NAME = "ml_ranker"
DESCRIPTION = ("PIT top-50 perps, 1d decisions: a conservatively regularised LightGBM model, retrained "
               "quarterly on a rolling 730d window, ranks next-H-day returns from ~25 cross-sectionally "
               "ranked price / volume / taker-flow / funding / crowd-positioning features; long top-k, "
               "short bottom-k, dollar neutral, vol-targeted.")
MECHANISM = ("Combine many individually weak, fee-dominated cross-sectional effects (flow persistence, "
             "funding carry, crowd contrarian, short-term reversal, momentum, low vol) into one ranking "
             "so the combined gross edge clears the ~27 bp alt round-trip cost.")
PANEL = dict(timeframe="1d", universe="pit_top50", start="2020-01-01", with_taker=True)
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False
WF_START = "2021-01-01"
OUTER_TRAIN_DAYS = 365

GRID = []
for _m in ("lgbm", "ridge", "ew"):
    for _H in (1, 3):
        for _k in (5, 10):
            GRID.append(dict(model=_m, H=_H, k=_k, vol_target=0.20))
FROZEN = dict(model="lgbm", H=1, k=5, vol_target=0.20)   # stability pick within the lgbm family, see results/ml_ranker.json (verdict: fails)

RETRAIN_DAYS = 91
ANCHOR = 1577836800            # 2020-01-01 00:00 UTC
TRAIN_WINDOW_DAYS = 730
MIN_TRAIN_DATES = 240
MIN_NAMES = 15
NAME_CAP = 0.25
BAND = 0.02
BUFFER = 2.0

SIGNS = dict(r1=-1, r3=-1, r7=1, r14=1, r30=1, r60=1, rv7=-1, rv30=-1, volvol=-1, dhi=1, dlo=1,
             vz7=-1, vz30=-1, tb1=1, tb7=1, f1=-1, f7=-1, df=-1, zG=-1, zT=1, D=1, oi1=-1, oi7=-1)
RANKED = list(SIGNS)
REGIME = ["btc_r7", "btc_r30", "btc_rv30", "dow"]
METRIC_GROUPS = {"ls": ["zG", "D"], "top": ["zT"], "oi": ["oi1", "oi7"]}

LGB_PARAMS = dict(objective="regression", num_leaves=15, min_data_in_leaf=300, feature_fraction=0.7,
                  bagging_fraction=0.7, bagging_freq=1, lambda_l2=10.0, learning_rate=0.03,
                  max_bin=63, num_threads=2, seed=0, deterministic=True, force_row_wise=True, verbose=-1)
LGB_ROUNDS = 300
RIDGE_ALPHA = 0.05

CAVEATS = [
    "Crowd-metric features exist for 53 coins from ~2021-12 (~60% of the tradable top-50); the top-trader ratio is NaN for most of 2022.",
    "Labels of names that delist inside the label window are dropped from training (the sim still books the delisting close).",
    "Live needs Binance public data (taker-buy volume, L/S ratios, funding) for ~50 names plus a Bybit symbol map.",
]

_MODEL_CACHE = {}
_IMPORTANCE = {}          # (model_key, retrain_close_ts) -> {feature: gain}


# --------------------------------------------------------------------------- #
# features
# --------------------------------------------------------------------------- #
def _lr(lc, n):
    out = np.full_like(lc, np.nan)
    out[n:] = lc[n:] - lc[:-n]
    return out


def _roll(A, n, fn, minp=None):
    r = pd.DataFrame(A).rolling(n, min_periods=minp or n)
    return getattr(r, fn)().to_numpy()


def raw_features(panel):
    """Dict of raw (unranked) causal features [T, N] plus regime vectors [T]."""
    c, h, l, qv = panel.c, panel.h, panel.l, panel.qv
    with np.errstate(invalid="ignore", divide="ignore"):
        lc = np.log(c)
        d1 = _lr(lc, 1)
        F = {f"r{n}": _lr(lc, n) for n in (1, 3, 7, 14, 30, 60)}
        F["rv7"] = _roll(d1, 7, "std", 6)
        F["rv30"] = _roll(d1, 30, "std", 20)
        F["volvol"] = _roll(F["rv7"], 30, "std", 20) / _roll(F["rv7"], 30, "mean", 20)
        F["dhi"] = lc - np.log(_roll(h, 30, "max", 20))
        F["dlo"] = lc - np.log(_roll(l, 30, "min", 20))
        qvp = np.where(qv > 0, qv, np.nan)
        F["vz7"] = np.log(_roll(qvp, 7, "mean", 5) / _roll(qvp, 30, "mean", 20))
        lq = np.log(qvp)
        F["vz30"] = (lq - _roll(lq, 30, "mean", 20)) / _roll(lq, 30, "std", 20)
        tb = panel.meta["tbqv"]
        F["tb1"] = tb / qvp
        F["tb7"] = _roll(tb, 7, "sum", 5) / _roll(qvp, 7, "sum", 5)
        fu = np.asarray(panel.funding, float)
        F["f1"] = fu.copy()
        F["f7"] = _roll(fu, 7, "sum", 5)
        F["df"] = F["f1"] - F["f7"] / 7.0
        m = panel.meta.get("metrics")
        T, N = c.shape
        if m is not None:
            lnG = np.log(m["ls_ratio"])
            lnT = np.log(m["top_ls_ratio"])
            zG = (lnG - _roll(lnG, 30, "mean", 20)) / _roll(lnG, 30, "std", 20)
            zT = (lnT - _roll(lnT, 30, "mean", 20)) / _roll(lnT, 30, "std", 20)
            loi = np.log(m["oi_value"])
            F["zG"], F["zT"], F["D"] = zG, zT, zT - zG
            F["oi1"], F["oi7"] = _lr(loi, 1), _lr(loi, 7)
        else:
            for k in ("zG", "zT", "D", "oi1", "oi7"):
                F[k] = np.full((T, N), np.nan)
    F = {k: np.array(v, dtype=float, copy=True) for k, v in F.items()}   # pandas CoW views are read-only
    # never compute across a relisting (different token / redenomination)
    rel = panel.meta.get("relisted")
    if rel is not None:
        relwin = pd.DataFrame(np.asarray(rel, float)).rolling(61, min_periods=1).max().to_numpy() > 0
        for k in F:
            F[k][relwin] = np.nan
    trad = panel.tradable
    for k in F:
        F[k][~trad] = np.nan
        F[k][~np.isfinite(F[k])] = np.nan
    # regime (BTC)
    j = panel.symbols.index("BTCUSDT") if "BTCUSDT" in panel.symbols else None
    T = len(panel.t)
    if j is not None:
        with np.errstate(invalid="ignore", divide="ignore"):
            lb = np.log(panel.c[:, j])
        db = _lr(lb, 1)
        R = {"btc_r7": _lr(lb, 7), "btc_r30": _lr(lb, 30),
             "btc_rv30": pd.Series(db).rolling(30, min_periods=20).std().to_numpy()}
    else:
        R = {k: np.full(T, np.nan) for k in ("btc_r7", "btc_r30", "btc_rv30")}
    R["dow"] = ((np.asarray(panel.t, np.int64) + panel.dt) // 86400 + 3) % 7   # weekday of the close (0=Mon)
    return F, R


_FEAT_CACHE = {}
_PRED_CACHE = {}


def _data_key(panel):
    """Identity of the panel's data (start, length, last row checksums) for in-process memoisation."""
    m = panel.meta.get("metrics")
    ms = None if m is None else float(np.nansum(m["ls_ratio"][-1])) + float(np.nansum(m["oi_value"][-1]))
    return _panel_key(panel) + (len(panel.t), int(panel.t[-1]), float(np.nansum(panel.c[-1])),
                                float(np.nansum(panel.tradable[-1])), float(np.nansum(panel.meta["tbqv"][-1])), ms)


def ranked_features(panel):
    key = _data_key(panel)
    if key in _FEAT_CACHE:
        return _FEAT_CACHE[key]
    F, R = raw_features(panel)
    X = {k: HX.cs_rank(F[k], min_n=MIN_NAMES) for k in RANKED}
    del F
    if len(_FEAT_CACHE) >= 1:
        _FEAT_CACHE.clear()
    _FEAT_CACHE[key] = (X, R)
    return X, R


def label(panel, H):
    """Centred cross-sectional rank of ln(o[i+1+H]/o[i+1]) among names tradable at i; raw too."""
    o = panel.o
    T, N = o.shape
    raw = np.full((T, N), np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        if T > H + 1:
            raw[:T - H - 1] = np.log(o[H + 1:] / o[1:T - H])
    raw[~panel.tradable] = np.nan
    return HX.cs_rank(raw, min_n=MIN_NAMES), raw


# --------------------------------------------------------------------------- #
# models
# --------------------------------------------------------------------------- #
def _design(X, R, rows, model):
    """Stack features of bars `rows` into [n_rows*N, F]; returns (M, row_idx, col_idx)."""
    T, N = X[RANKED[0]].shape
    ii = np.repeat(rows, N)
    jj = np.tile(np.arange(N), len(rows))
    cols = [X[k][ii, jj] for k in RANKED]
    names = list(RANKED)
    if model == "lgbm":
        for k in REGIME:
            cols.append(np.asarray(R[k], float)[ii])
            names.append(k)
    elif model == "ridge":
        cols = [np.nan_to_num(cx, nan=0.0) for cx in cols]
        for g, fs in METRIC_GROUPS.items():
            cols.append((~np.isfinite(X[fs[0]][ii, jj])).astype(float))
            names.append("miss_" + g)
    return np.column_stack(cols), ii, jj, names


def _retrain_rows(panel):
    """Bar indices whose close lies on the absolute 91-day grid."""
    close = np.asarray(panel.t, np.int64) + int(panel.dt)
    step = RETRAIN_DAYS * 86400
    return np.flatnonzero(((close - ANCHOR) % step) < panel.dt)


def _panel_key(panel):
    return (int(panel.dt), int(panel.t[0]), len(panel.symbols), panel.symbols[0], panel.symbols[-1],
            str(panel.meta.get("universe")))


def _fit(model, Xtr, ytr, params):
    if model == "lgbm":
        import lightgbm as lgb
        p = dict(LGB_PARAMS)
        if params.get("target") == "signcost":
            p["objective"] = "binary"
        ds = lgb.Dataset(Xtr, label=ytr, params={"max_bin": p["max_bin"], "verbose": -1}, free_raw_data=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return lgb.train(p, ds, num_boost_round=LGB_ROUNDS)
    # ridge
    n = Xtr.shape[0]
    A = np.column_stack([np.ones(n), Xtr])
    lam = RIDGE_ALPHA * n * np.eye(A.shape[1])
    lam[0, 0] = 0.0
    return np.linalg.solve(A.T @ A + lam, A.T @ ytr)


def _predict(model, mdl, M, params):
    if model == "lgbm":
        p = mdl.predict(M, num_threads=2)
        return p - 0.5 if params.get("target") == "signcost" else p
    return np.column_stack([np.ones(M.shape[0]), M]) @ mdl


def predictions(panel, params):
    """pred[T, N] (NaN where no model / not tradable). Causal: the model used at bar i was fitted at
    a grid close r <= i on samples whose label was realised (plus an H-day embargo) before r."""
    model = params.get("model", "lgbm")
    H = int(params.get("H", 1))
    X, R = ranked_features(panel)
    T, N = X[RANKED[0]].shape
    pred = np.full((T, N), np.nan)
    avail = np.isfinite(X["r1"]) & np.isfinite(X["r7"]) & np.isfinite(X["rv30"])
    if model == "ew":
        acc = np.zeros((T, N))
        cnt = np.zeros((T, N))
        for k, s in SIGNS.items():
            v = X[k]
            ok = np.isfinite(v)
            acc[ok] += s * v[ok]
            cnt[ok] += 1
        with np.errstate(invalid="ignore", divide="ignore"):
            pred = np.where(cnt > 0, acc / cnt, np.nan)
        pred[~avail] = np.nan
        return pred
    ylab, yraw = label(panel, H)
    target = params.get("target", "rank")
    window = params.get("window", "rolling")
    rrows = _retrain_rows(panel)
    close = np.asarray(panel.t, np.int64) + int(panel.dt)
    nvalid = avail.sum(1)
    pkey = _panel_key(panel)
    mkey = (model, H, target, window)
    fitted = []
    for r in rrows:
        hi = r - 2 * H                                # sample i <= r-2H: label realised at close i+H <= r-H
        lo = 0 if window == "expanding" else max(0, r - TRAIN_WINDOW_DAYS + 1)
        rows = np.arange(lo, hi + 1)
        rows = rows[nvalid[rows] >= MIN_NAMES] if rows.size else rows
        if rows.size < MIN_TRAIN_DATES:
            continue
        ck = pkey + mkey + (int(close[r]), int(close[rows[0]]), int(rows.size))
        if ck not in _MODEL_CACHE:
            M, ii, jj, names = _design(X, R, rows, model)
            y = ylab[ii, jj] if target == "rank" else yraw[ii, jj]
            ok = np.isfinite(y) & avail[ii, jj]
            Mt, yt = M[ok], y[ok]
            if target == "signcost":
                cost = 2.0 * 2.0 * (0.00055 + 0.0008)
                keep = np.abs(yt) > cost
                Mt, yt = Mt[keep], (yt[keep] > 0).astype(int)
            mdl = _fit(model, Mt, yt, params)
            _MODEL_CACHE[ck] = mdl
            if model == "lgbm":
                g = mdl.feature_importance(importance_type="gain")
                _IMPORTANCE[mkey + (int(close[r]),)] = dict(zip(names, (g / max(g.sum(), 1e-12)).tolist()))
            else:
                _IMPORTANCE[mkey + (int(close[r]),)] = dict(zip(["const"] + names, mdl.tolist()))
        fitted.append((r, _MODEL_CACHE[ck]))
    for n_, (r, mdl) in enumerate(fitted):
        r_end = fitted[n_ + 1][0] if n_ + 1 < len(fitted) else T
        rows = np.arange(r, r_end)
        rows = rows[nvalid[rows] >= MIN_NAMES]
        if not rows.size:
            continue
        M, ii, jj, _ = _design(X, R, rows, model)
        ok = avail[ii, jj]
        p = np.full(len(ii), np.nan)
        if ok.any():
            p[ok] = _predict(model, mdl, M[ok], params)
        pred[ii, jj] = p
    pred[~avail] = np.nan
    return pred


# --------------------------------------------------------------------------- #
# portfolio
# --------------------------------------------------------------------------- #
def buffered_longshort(score, k, buffer=BUFFER, min_n=None):
    """Sequential top-k / bottom-k selection with a rank buffer: a held long stays while its rank is
    within the top buffer*k (shorts symmetric). Equal weight +-0.5/k. Causal."""
    T, N = score.shape
    w = np.zeros((T, N))
    min_n = min_n or max(MIN_NAMES, 4 * k)
    L, S = set(), set()
    kb = int(round(buffer * k))
    for i in range(T):
        ok = np.flatnonzero(np.isfinite(score[i]))
        if ok.size < min_n:
            L, S = set(), set()
            continue
        o = ok[np.argsort(-score[i, ok], kind="stable")]     # best first
        top, bot = set(o[:kb].tolist()), set(o[-kb:].tolist())
        L = {j for j in L if j in top}
        S = {j for j in S if j in bot}
        for j in o:
            if len(L) >= k:
                break
            if j not in L and j not in S:
                L.add(int(j))
        for j in o[::-1]:
            if len(S) >= k:
                break
            if j not in S and j not in L:
                S.add(int(j))
        for j in L:
            w[i, j] = 0.5 / k
        for j in S:
            w[i, j] = -0.5 / k
    return w


def weights_from_pred(panel, pred, params):
    k = int(params.get("k", 10))
    H = int(params.get("H", 1))
    w = buffered_longshort(pred, k)
    w = HX.stagger(w, H)
    w = HX.vol_scale_book(panel, w, float(params.get("vol_target", 0.20)), lb=60, cap=3.0)
    w = np.clip(w, -NAME_CAP, NAME_CAP)
    w = HX.band(w, BAND)
    w[~panel.tradable] = 0.0
    return w


def cached_predictions(panel, params):
    key = _data_key(panel) + (params.get("model", "lgbm"), int(params.get("H", 1)),
                              params.get("target", "rank"), params.get("window", "rolling"))
    if key not in _PRED_CACHE:
        if len(_PRED_CACHE) >= 8:
            _PRED_CACHE.pop(next(iter(_PRED_CACHE)))
        _PRED_CACHE[key] = predictions(panel, params)
    return _PRED_CACHE[key]


def weights(panel, params, metrics=None):
    if metrics is not None and "metrics" not in panel.meta:
        panel.meta["metrics"] = metrics
    pred = cached_predictions(panel, params)
    return weights_from_pred(panel, pred, params)


def live_targets(panel, params, metrics=None):
    """Run at the 00:07 UTC run on a panel ending with the just-closed daily bar (and metrics
    attached / passed). The model refits on the latest 91-day grid date <= that close (one refit per
    quarter, trailing 730d); the target book is the last row."""
    w = weights(panel, params, metrics)
    tg = {panel.symbols[j]: float(w[-1, j]) for j in np.flatnonzero(w[-1] != 0)}
    rr = _retrain_rows(panel)
    return {"as_of_bar_open": int(panel.t[-1]), "decision_time": int(panel.t[-1] + panel.dt),
            "model_fit_close": int(panel.t[rr[-1]] + panel.dt) if rr.size else None,
            "targets": tg,
            "orders": "market orders at the 00:07 run to move each perp to target notional/equity; attach a "
                      "stopLoss per name (see results: stop overlay) within half the liquidation distance"}


def load(end=HX.DEV_END):
    p = data.load_panel(PANEL["timeframe"], universe=PANEL["universe"], start=PANEL["start"], end=end,
                        with_taker=True)
    p.meta["metrics"] = data.load_metrics(p.symbols, PANEL["timeframe"], start=PANEL["start"], end=end,
                                          max_stale=7200)
    from lab import wf
    return wf.pre_lockbox(p)
