#!/usr/bin/env python3
"""Time-series momentum with volatility targeting — a portfolio engine.

WHY THIS IS A SEPARATE ENGINE

engine.py faithfully replays the bot's current design: discrete positions, a
fixed number of slots, entries ranked cross-sectionally, exits driven by
trailing stops. Three measured facts say that design cannot work here, and none
of them are fixable by tuning it:

  1. Cross-sectional ranking picks the best coin, but crypto coins are ~0.8
     correlated, so "best of a falling market" still falls. research.py measures
     a real cross-sectional IC (low_volatility, +0.065) that the long-only slot
     engine still turns into -44%. The academic literature reaches the same
     conclusion: there is hardly any cross-sectional momentum in crypto, while
     time-series momentum is robust.
  2. Trailing stops harvest noise. In engine.py, every widening of the trail
     improves the result monotonically, all the way to switching stops off
     (-44.8% -> -5.8%). A stop is a random exit, and random exits cost fees.
  3. Equal-dollar sizing over-risks the volatile coins. Volatility is
     autocorrelated, so a fixed position size systematically takes the most risk
     exactly when the next move is largest.

So this engine asks a different question per asset - "is THIS coin trending up,
and how much of it should I hold given its volatility" - instead of "which coin
is the best right now".

  * SIGNAL is time-series: hold a coin only while its own price is above its own
    N-day moving average. Otherwise hold cash. Cash is a real position.
  * SIZING is inverse-volatility, scaled to a target portfolio volatility. A
    calm coin gets more dollars than a wild one so each contributes comparable
    risk.
  * EXIT is the signal turning off at the next rebalance. There are no stops.
  * COSTS are charged on TURNOVER, not per trade: rebalancing from 20% to 22% of
    a coin costs fees on the 2% traded, not on a whole round trip. This is why a
    portfolio engine can rebalance often without the fee death spiral that kills
    the slot engine at high frequency.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from engine import Universe, _pct_change, _roll_std, HOUR


@dataclass
class PParams:
    # --- signal ---
    trend_days: int = 50          # hold while price > its own SMA over this window
    trend_confirm_days: int = 0   # optional 2nd, slower filter; 0 disables

    # --- sizing ---
    target_vol: float = 0.50      # annualized portfolio vol target
    vol_lookback_days: int = 30
    max_weight: float = 0.25      # per-coin cap
    max_gross: float = 1.00       # total deployment cap; 1.0 = no leverage

    # --- regime overlay ---
    regime_symbol: str = "BTC/USD"
    regime_days: int = 0          # 0 = off; else require BTC > its SMA to hold ANY risk

    # --- mechanics ---
    rebalance_hours: int = 24
    start_equity: float = 200.0
    fee_bps: float = 35.0
    spread_bps: float = 10.0
    min_trade_frac: float = 0.005  # skip rebalancing dust; a no-op trade is pure fee


def run_portfolio(u: Universe, p: PParams):
    """Returns (equity curve, diagnostics dict). Weights are decided on the
    close of bar i and executed at the open of bar i+1, same as engine.py."""
    n = len(u.t)
    c = u.mark
    nsym = len(u.symbols)
    # bpd = bars per day. All windows below are expressed in DAYS and converted
    # here, so the same parameters mean the same thing on 1H and 1D data.
    bpd = getattr(u, "bars_per_day", 24)
    ann = math.sqrt(365 * bpd)

    # --- signals, all computed from data up to and including column i ---
    trend_w = max(2, p.trend_days * bpd)
    sma = _rolling_mean(c, trend_w)
    long_ok = c > sma
    if p.trend_confirm_days:
        long_ok = long_ok & (c > _rolling_mean(c, max(2, p.trend_confirm_days * bpd)))

    # Volatility in ANNUALIZED terms, from hourly returns.
    bar_vol = _roll_std(_pct_change(c, 1), max(2, p.vol_lookback_days * bpd))
    ann_vol = bar_vol * ann

    regime_ok = np.ones(n, dtype=bool)
    if p.regime_days and p.regime_symbol in u.symbols:
        ri = u.symbols.index(p.regime_symbol)
        rsma = _rolling_mean(c[ri:ri + 1], max(2, p.regime_days * bpd))[0]
        regime_ok = c[ri] > rsma

    cost = (p.fee_bps + p.spread_bps) / 10000.0
    warm = max(trend_w, p.vol_lookback_days * bpd,
               (p.regime_days or 0) * bpd, p.trend_confirm_days * bpd) + bpd

    equity = np.full(n, np.nan)
    w = np.zeros(nsym)            # current weights, by value
    eq = p.start_equity
    target = np.zeros(nsym)
    turnover_total = 0.0
    fees_total = 0.0
    rebalances = 0
    exposure = []

    for i in range(n):
        # mark to market: each holding moves with its own bar return
        if i > 0:
            ret = np.where(np.isnan(c[:, i]) | np.isnan(c[:, i - 1]), 0.0,
                           c[:, i] / np.where(c[:, i - 1] == 0, np.nan, c[:, i - 1]) - 1.0)
            ret = np.nan_to_num(ret)
            gain = float((w * ret).sum())
            eq *= (1.0 + gain)
            # weights drift with price
            w = w * (1.0 + ret)
            s = w.sum()
            if s > 0:
                w = w / max(1e-12, 1.0 + gain)
        equity[i] = eq
        exposure.append(float(w.sum()))

        if i < warm or i + 1 >= n:
            continue

        # ---- execute the target decided on the PREVIOUS bar
        if target is not None and np.any(target != w):
            tradable = ~np.isnan(u.o[:, i + 1]) if i + 1 < n else ~np.isnan(c[:, i])
            desired = np.where(tradable, target, w)
            delta = desired - w
            delta[np.abs(delta) < p.min_trade_frac] = 0.0
            turn = float(np.abs(delta).sum())
            if turn > 0:
                fee = turn * cost
                eq *= (1.0 - fee)
                fees_total += fee * eq
                turnover_total += turn
                rebalances += 1
                w = w + delta
            target = w.copy()

        # ---- decide new target weights on this close
        if (i % max(1, p.rebalance_hours * bpd // 24)) != 0:
            continue

        ok = long_ok[:, i] & ~np.isnan(c[:, i]) & (ann_vol[:, i] > 0) & ~np.isnan(ann_vol[:, i])
        if not regime_ok[i]:
            ok = np.zeros(nsym, dtype=bool)

        k = int(ok.sum())
        if k == 0:
            target = np.zeros(nsym)
            continue

        # Inverse-vol weights, scaled so the PORTFOLIO targets p.target_vol.
        # Assuming zero correlation would badly under-risk (crypto is ~0.8
        # correlated), so the naive sum-of-risks form is used: it treats the
        # book as if it moves together, which for this universe is much closer
        # to the truth and errs toward holding less.
        raw = np.zeros(nsym)
        raw[ok] = 1.0 / ann_vol[ok, i]
        raw = raw / raw.sum()                      # risk-parity proportions
        port_vol = float((raw[ok] * ann_vol[ok, i]).sum())
        scale = p.target_vol / port_vol if port_vol > 0 else 0.0
        tw = np.clip(raw * scale, 0.0, p.max_weight)
        gross = tw.sum()
        if gross > p.max_gross:
            tw = tw * (p.max_gross / gross)
        target = tw

    diag = {
        "rebalances": rebalances,
        "total_turnover": turnover_total,
        "avg_exposure": float(np.mean(exposure[warm:])) if n > warm else 0.0,
        "pct_time_in_cash": float(np.mean(np.array(exposure[warm:]) < 0.01)) if n > warm else 0.0,
        "est_fee_drag": fees_total,
    }
    return equity, diag


def _rolling_mean(a, w):
    out = np.full(a.shape, np.nan)
    if a.shape[1] < w or w < 1:
        return out
    cs = np.nancumsum(a, axis=1)
    pad = np.zeros((a.shape[0], 1))
    out[:, w - 1:] = (cs[:, w - 1:] - np.concatenate([pad, cs[:, :-w]], axis=1)) / w
    return out


def pmetrics(u, equity, diag):
    eq = equity[~np.isnan(equity)]
    if len(eq) < 2:
        return {}
    r = np.diff(eq) / eq[:-1]
    years = (u.t[-1] - u.t[0]) / (365.25 * 86400)
    total = eq[-1] / eq[0] - 1
    peak = np.maximum.accumulate(eq)
    maxdd = float(np.min(eq / peak - 1))
    sd = float(np.std(r))
    ann = math.sqrt(365 * getattr(u, "bars_per_day", 24))
    sharpe = float(np.mean(r) / sd * ann) if sd > 0 else 0.0
    dn = r[r < 0]
    sortino = (float(np.mean(r) / np.std(dn) * ann)
               if len(dn) and np.std(dn) > 0 else 0.0)
    # The benchmark symbol differs by venue: Alpaca quoted BTC/USD, Bybit uses
    # BTCUSDT. Hardcoding one silently reports a MISSING benchmark as "no edge"
    # rather than as an error, which is how a strategy gets compared to nothing.
    bench = None
    bsym = next((s for s in ("BTC/USD", "BTCUSDT", "BTCUSD") if s in u.symbols), None)
    if bsym:
        b = u.mark[u.symbols.index(bsym)]
        b = b[~np.isnan(b)]
        if len(b) > 1:
            bench = float(b[-1] / b[0] - 1)
    cagr = (1 + total) ** (1 / years) - 1 if years > 0 and total > -1 else float("nan")
    return {
        "total_return": float(total), "cagr": float(cagr),
        "max_drawdown": maxdd, "sharpe": sharpe, "sortino": sortino,
        "calmar": float(cagr / abs(maxdd)) if maxdd < 0 else float("nan"),
        "end_equity": float(eq[-1]),
        "btc_buyhold": bench,
        "edge_vs_btc": (total - bench) if bench is not None else None,
        **diag,
    }
