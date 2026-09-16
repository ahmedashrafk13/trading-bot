#!/usr/bin/env python3
"""Candidate entry signals, and an honest test of whether any of them predict.

WHY THIS EXISTS

Backtesting a full strategy is slow and confounded: sizing, trails, slot caps
and fees all sit between the signal and the result, so a losing backtest cannot
tell you WHICH part was wrong. This module strips all of that away and asks the
only question that matters first:

    does the signal, at time t, carry any information about the return from
    t to t+h?

That is measured as an information coefficient (IC) - the rank correlation
between the signal and the forward return, computed across every symbol at
every hour. Over 400 days and 33 coins that is ~250,000 observations per
horizon, which is the "lots of trades so it improves faster" the account will
never deliver live: a live trade costs money and two days, an observation here
costs nothing and there are a quarter of a million of them.

HOW TO READ AN IC

  |IC| < 0.01   noise. No edge. No amount of position sizing rescues it.
  |IC| ~ 0.02   weak but potentially real if it survives out of sample.
  |IC| > 0.05   strong for hourly crypto. Be suspicious; check for lookahead.

A NEGATIVE IC is just as useful as a positive one - it means the rule is
backwards and should be inverted.

THE NULL BASELINE IS NOT OPTIONAL. A random signal is included and evaluated
identically. Any candidate that does not clearly beat the random column is
indistinguishable from luck, no matter how good its number looks in isolation.
"""
from __future__ import annotations

import json
import os

import numpy as np

from engine import _pct_change, _sma, _roll_std, ROOT

FUNDING_DIR = os.path.join(ROOT, "data", "funding")


def _load_funding(u):
    """Align cached Bybit perp funding rates onto u's hourly grid.

    Funding prints every 8h; the value is held flat (step function) until the
    next print, matching how a live signal would actually see it — you only
    know the CURRENT funding rate, not the next one. Symbols with no perp
    (no cached file) stay all-NaN, which _rank_normalize already handles by
    ranking only the symbols quoting that hour.
    """
    out = np.full((len(u.symbols), len(u.t)), np.nan)
    if not os.path.isdir(FUNDING_DIR):
        return out
    for si, sym in enumerate(u.symbols):
        # bars may be named either Bybit-style ("BTCUSDT") or legacy-cache
        # ("BTC-USD"); funding is always cached Bybit-style.
        bybit_sym = sym if sym.endswith("USDT") else sym.replace("-USD", "USDT").replace("/USD", "USDT")
        path = os.path.join(FUNDING_DIR, bybit_sym + ".json")
        if not os.path.exists(path):
            continue
        rates = json.load(open(path, encoding="utf-8"))["rates"]
        if not rates:
            continue
        ts = np.array([r[0] for r in rates], dtype=np.int64)
        rv = np.array([r[1] for r in rates], dtype=np.float64)
        # searchsorted: for each grid hour, the most recent funding print at or
        # before it (no lookahead — a print at 08:00 is unknown until then).
        pos = np.searchsorted(ts, u.t, side="right") - 1
        valid = pos >= 0
        out[si, valid] = rv[pos[valid]]
    return out


_FUNDING_CACHE = {}


def _funding_for(u):
    key = id(u)
    if key not in _FUNDING_CACHE:
        _FUNDING_CACHE.clear()   # one universe at a time is all this needs
        _FUNDING_CACHE[key] = _load_funding(u)
    return _FUNDING_CACHE[key]


def _rank_normalize(a):
    """Cross-sectional rank within each hour, scaled to [-1, 1].

    Ranking per hour is what makes the IC a fair test of 'which coin should I
    buy right now' rather than 'is the whole market up', which is the question
    a long-only bot with limited slots actually faces. It also makes the measure
    immune to outliers and to each coin's own scale.
    """
    out = np.full(a.shape, np.nan)
    for i in range(a.shape[1]):
        col = a[:, i]
        m = ~np.isnan(col)
        n = int(m.sum())
        if n < 5:                 # too few coins quoting to rank meaningfully
            continue
        order = np.argsort(np.argsort(col[m]))
        out[m, i] = order / (n - 1) * 2 - 1
    return out


# ------------------------------------------------------------------ signals
# Each returns a raw score where HIGHER is expected to mean HIGHER forward
# return. Every one uses only data up to and including column i.

def sig_momentum_7h(u):
    """The bot's current TACTICAL rule: 7-hour price momentum."""
    return _pct_change(u.mark, 7)


def sig_momentum_30d(u):
    """The bot's current CORE rule: 30-day momentum, on hourly bars."""
    return _pct_change(u.mark, 24 * 30)


def sig_mean_reversion_24h(u):
    """Inverse of 24h momentum - buy what fell. The opposite of the bot."""
    return -_pct_change(u.mark, 24)


def sig_dist_from_sma(u):
    """Negative distance from SMA20: buy what is stretched BELOW its mean."""
    return -(u.mark / _sma(u.mark, 20) - 1.0)


def sig_rel_strength_btc(u):
    """7-day return relative to BTC - is this coin beating the market?

    A long-only bot with 5 slots is really making a cross-sectional choice, and
    absolute momentum answers the wrong question in a market where everything
    moves together. This asks the right one.
    """
    r = _pct_change(u.mark, 24 * 7)
    if "BTC/USD" not in u.symbols:
        return r
    return r - r[u.symbols.index("BTC/USD")]


def sig_breakout_20d(u):
    """Position within the 20-day high/low range. 1.0 = at the range high."""
    c = u.mark
    w = 24 * 20
    out = np.full(c.shape, np.nan)
    for i in range(w, c.shape[1]):
        win = c[:, i - w:i]
        hi = np.nanmax(win, axis=1)
        lo = np.nanmin(win, axis=1)
        rng = hi - lo
        with np.errstate(invalid="ignore", divide="ignore"):
            out[:, i] = np.where(rng > 0, (c[:, i] - lo) / rng, np.nan)
    return out


def sig_low_vol(u):
    """Negative 14-hour volatility - prefer the calm coins.

    Low-volatility outperformance is one of the few anomalies that survives
    across asset classes, so it is worth testing here rather than assuming
    crypto is different.
    """
    return -_roll_std(_pct_change(u.mark, 1), 14)


def sig_vol_contraction(u):
    """Short-term vol divided by long-term vol, inverted.

    High when a coin has gone quiet relative to its own history - the classic
    coiled-spring setup that precedes a range expansion.
    """
    r = _pct_change(u.mark, 1)
    short = _roll_std(r, 12)
    long = _roll_std(r, 24 * 7)
    with np.errstate(invalid="ignore", divide="ignore"):
        return -np.where(long > 0, short / long, np.nan)


def sig_funding_contrarian(u):
    """Negative current perp funding rate — fade the crowded side.

    Positive funding means longs are paying shorts: leveraged longs are
    crowded, which the "extreme funding precedes squeezes" thesis says should
    front-run a pullback. Signal is NEGATIVE funding so higher score = less
    crowded = expected higher forward return.
    """
    return -_funding_for(u)


def sig_momentum_if_funding_calm(u):
    """30d momentum signal, but only where funding is NOT stretched.

    Tests the "combination" idea from learn.md STEP 4B: a weak momentum signal
    conditioned on low crowding (funding near zero) might beat momentum alone,
    since a crowded trade is more likely to be late/exhausted momentum.
    """
    mom = _pct_change(u.mark, 24 * 30)
    fund = _funding_for(u)
    # rank-normalize funding's absolute value per hour, keep only the calmer half
    absf = np.abs(fund)
    calm = _rank_normalize(absf) < 0.0   # bottom half = calmer than the cross-sectional median
    out = np.where(calm, mom, np.nan)
    return out


def sig_random(u):
    """THE NULL. Any candidate that cannot beat this is luck."""
    rng = np.random.default_rng(0)
    return rng.standard_normal(u.mark.shape)


CANDIDATES = {
    "momentum_7h (bot TACTICAL)": sig_momentum_7h,
    "momentum_30d (bot CORE)": sig_momentum_30d,
    "mean_reversion_24h": sig_mean_reversion_24h,
    "below_sma20": sig_dist_from_sma,
    "rel_strength_vs_btc": sig_rel_strength_btc,
    "breakout_20d": sig_breakout_20d,
    "low_volatility": sig_low_vol,
    "vol_contraction": sig_vol_contraction,
    "funding_contrarian": sig_funding_contrarian,
    "momentum_if_funding_calm": sig_momentum_if_funding_calm,
    "RANDOM (null baseline)": sig_random,
}


# ------------------------------------------------------------------ the test
def forward_return(u, h):
    """Return from the close of hour i to the close of hour i+h."""
    c = u.mark
    out = np.full(c.shape, np.nan)
    if c.shape[1] > h:
        out[:, :-h] = c[:, h:] / c[:, :-h] - 1.0
    return out


def information_coefficient(sig, fwd, warm):
    """Mean per-hour rank correlation between signal and forward return.

    Averaging the per-hour correlation (rather than pooling every observation)
    keeps hours with many quoting coins from dominating, and matches how the
    bot actually decides: pick the best coin available THIS hour.
    """
    s = _rank_normalize(sig)[:, warm:]
    f = _rank_normalize(fwd)[:, warm:]
    ics = []
    for i in range(s.shape[1]):
        m = ~np.isnan(s[:, i]) & ~np.isnan(f[:, i])
        if m.sum() < 5:
            continue
        a, b = s[m, i], f[m, i]
        sa, sb = a.std(), b.std()
        if sa > 0 and sb > 0:
            ics.append(float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb)))
    if not ics:
        return 0.0, 0.0, 0
    ics = np.array(ics)
    # t-stat of the mean IC: with N hours this says whether the mean is
    # distinguishable from zero at all.
    t = float(ics.mean() / (ics.std() / np.sqrt(len(ics)))) if ics.std() > 0 else 0.0
    return float(ics.mean()), t, len(ics)


# ------------------------------------------------------- composite for engine
COMPOSITES = {
    # The two rules research.py found positive and consistent in BOTH halves.
    # Combined by per-hour rank so neither dominates on scale.
    "lowvol_reversion": ["low_volatility", "below_sma20"],
    # Single-signal variants, for attributing any result to one rule.
    "lowvol": ["low_volatility"],
    "reversion": ["below_sma20"],
    # The bot's own rule, INVERTED - its measured IC is negative, so flipping it
    # is the most direct test of whether the sign is the whole problem.
    "momentum_inverted": ["-momentum_7h (bot TACTICAL)"],
}

_BY_NAME = {
    "low_volatility": sig_low_vol,
    "below_sma20": sig_dist_from_sma,
    "momentum_7h (bot TACTICAL)": sig_momentum_7h,
    "mean_reversion_24h": sig_mean_reversion_24h,
    "rel_strength_vs_btc": sig_rel_strength_btc,
    "breakout_20d": sig_breakout_20d,
}


def composite_score(u, name):
    """Average of per-hour rank-normalized component signals.

    A leading '-' on a component inverts it. Rank-normalizing each component
    before averaging is what stops volatility (a small number) from being
    drowned out by momentum (a large one).
    """
    if name not in COMPOSITES:
        raise SystemExit(f"unknown entry_signal '{name}'. "
                         f"choose from: momentum, {', '.join(COMPOSITES)}")
    parts = []
    for comp in COMPOSITES[name]:
        neg = comp.startswith("-")
        key = comp[1:] if neg else comp
        s = _rank_normalize(_BY_NAME[key](u))
        parts.append(-s if neg else s)
    return np.nanmean(np.stack(parts), axis=0)
