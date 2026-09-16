#!/usr/bin/env python3
"""Market-neutral long/short on perpetuals.

WHY THIS ENGINE EXISTS

research.py found a real, strong cross-sectional signal: low-volatility coins
outperform, IC +0.065 at 168h with t=+16 against a random null of 0.002. That is
not noise. Yet feeding it into the long-only engine still returned -44%.

The reason is structural, not a bug. A cross-sectional IC says "the coins I rank
highest beat the coins I rank lowest". It does NOT say "the coins I rank highest
go up". In a market where everything falls together — and crypto coins are ~0.8
correlated — being long the best faller still loses money. A long-only book can
only express half of the signal, and it is the half that does not pay.

A market-neutral book expresses both halves: long the top of the ranking, short
the bottom, sized so the two legs cancel. What remains is the SPREAD between
them, which is exactly what the IC measures. Direction stops mattering.

  * Perps are required, because spot cannot short.
  * Gross exposure is capped at 2x (1x long + 1x short) by default. This is NOT
    a leveraged directional bet: net exposure is ~0, so a 50% market crash moves
    the book very little. Leverage here buys symmetry, not amplification.
  * Funding is charged on the short leg. On Bybit perps the funding rate is paid
    every 8h and is usually positive, meaning shorts are PAID. It is modelled as
    a cost anyway, so the result is conservative rather than flattering.

WHAT WOULD MAKE THIS FAIL
  Shorting costs more than longing (borrow, funding spikes), small caps are hard
  to short at size, and a crowded short can squeeze violently. The backtest sees
  none of that. Treat a positive result here as "worth a small live test", never
  as a finished system.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from engine import Universe, _pct_change, _roll_std


@dataclass
class NParams:
    # --- signal ---
    signal: str = "lowvol"        # lowvol | reversion | lowvol_reversion | momentum
    lookback_days: int = 14
    quantile: float = 0.20        # top/bottom 20% form the two legs

    # --- book construction ---
    gross: float = 2.0            # 1.0 long + 1.0 short
    net_cap: float = 0.10         # |long - short| may not exceed this
    max_weight: float = 0.10      # per-coin cap, each side
    min_names: int = 6            # below this the book is too concentrated to trade
    risk_weight: bool = True      # size each leg by INVERSE VOL, not equal dollars

    # --- costs ---
    fee_bps: float = 5.5          # Bybit perp taker
    slip_bps: float = 5.0
    funding_bps_8h: float = 1.0   # charged on the SHORT leg, conservative

    # --- mechanics ---
    rebalance_days: int = 7
    start_equity: float = 1000.0
    vol_target: float = 0.0       # 0 = off; else scale the whole book to this vol


def _rank_norm(a):
    """Cross-sectional rank per bar, scaled to [-1, 1]; NaN where too few names."""
    out = np.full(a.shape, np.nan)
    for i in range(a.shape[1]):
        col = a[:, i]
        m = ~np.isnan(col)
        n = int(m.sum())
        if n < 5:
            continue
        out[m, i] = np.argsort(np.argsort(col[m])) / (n - 1) * 2 - 1
    return out


def build_signal(u, p):
    c = u.mark
    bpd = u.bars_per_day
    lb = max(2, p.lookback_days * bpd)
    if p.signal == "lowvol":
        raw = -_roll_std(_pct_change(c, 1), lb)
    elif p.signal == "reversion":
        raw = -(c / _sma(c, lb) - 1.0)
    elif p.signal == "momentum":
        raw = _pct_change(c, lb)
    elif p.signal == "lowvol_reversion":
        a = _rank_norm(-_roll_std(_pct_change(c, 1), lb))
        b = _rank_norm(-(c / _sma(c, lb) - 1.0))
        return np.nanmean(np.stack([a, b]), axis=0)
    else:
        raise SystemExit(f"unknown signal {p.signal!r}")
    return _rank_norm(raw)


def _sma(a, w):
    out = np.full(a.shape, np.nan)
    if a.shape[1] < w:
        return out
    cs = np.nancumsum(a, axis=1)
    pad = np.zeros((a.shape[0], 1))
    out[:, w - 1:] = (cs[:, w - 1:] - np.concatenate([pad, cs[:, :-w]], axis=1)) / w
    return out


def run_neutral(u, p):
    n = len(u.t)
    c = u.mark
    nsym = len(u.symbols)
    bpd = u.bars_per_day
    sig = build_signal(u, p)
    # realized vol per name, used to risk-weight each leg
    vol = _roll_std(_pct_change(c, 1), max(2, p.lookback_days * bpd))

    cost = (p.fee_bps + p.slip_bps) / 10000.0
    # funding accrues every 8h; convert to a per-bar rate on the short leg
    fund_per_bar = (p.funding_bps_8h / 10000.0) * (24.0 / 8.0) / bpd

    step = max(1, p.rebalance_days * bpd)
    warm = max(2, p.lookback_days * bpd) + bpd

    w = np.zeros(nsym)          # signed weights: + long, - short
    eq = p.start_equity
    equity = np.full(n, np.nan)
    rebalances = 0
    turnover = 0.0
    gross_hist = []

    for i in range(n):
        if i > 0:
            prev = c[:, i - 1]
            ret = np.where(np.isnan(c[:, i]) | np.isnan(prev) | (prev == 0),
                           0.0, c[:, i] / np.where(prev == 0, np.nan, prev) - 1.0)
            ret = np.nan_to_num(ret)
            # A short leg earns the NEGATIVE of the return; w already carries the
            # sign, so one dot product covers both legs.
            gain = float((w * ret).sum())
            # funding is paid on the absolute size of the short book only
            short_gross = float(np.abs(w[w < 0]).sum())
            gain -= short_gross * fund_per_bar
            eq *= (1.0 + gain)
            if eq <= 0:
                equity[i:] = 0.0
                break
            w = w * (1.0 + ret) / max(1e-12, 1.0 + gain)
        equity[i] = eq
        gross_hist.append(float(np.abs(w).sum()))

        if i < warm or i % step != 0 or i + 1 >= n:
            continue

        vol_now = vol[:, i]
        s = sig[:, i].copy()
        s[np.isnan(c[:, i])] = np.nan
        valid = ~np.isnan(s)
        k = int(valid.sum())
        if k < p.min_names * 2:
            target = np.zeros(nsym)
        else:
            vals = s[valid]
            hi = np.quantile(vals, 1 - p.quantile)
            lo = np.quantile(vals, p.quantile)
            longs = valid & (s >= hi)
            shorts = valid & (s <= lo)
            if longs.sum() < p.min_names or shorts.sum() < p.min_names:
                target = np.zeros(nsym)
            else:
                target = np.zeros(nsym)
                if p.risk_weight:
                    # Equal DOLLARS across the two legs is a trap for a low-vol
                    # signal: the long leg is calm by construction and the short
                    # leg is wild, so the short dominates the P&L and a bull
                    # market destroys the book even while the RANKING is
                    # correct. Sizing each name by inverse vol makes the two
                    # legs contribute comparable RISK, which is what
                    # "market-neutral" has to mean for this signal.
                    iv = 1.0 / np.where((vol_now > 0) & ~np.isnan(vol_now),
                                        vol_now, np.nan)
                    lw = np.where(longs, iv, 0.0)
                    sw = np.where(shorts, iv, 0.0)
                    lw = np.nan_to_num(lw)
                    sw = np.nan_to_num(sw)
                    if lw.sum() <= 0 or sw.sum() <= 0:
                        target = np.zeros(nsym)
                        w_ok = False
                    else:
                        target = (p.gross / 2.0) * (lw / lw.sum() - sw / sw.sum())
                        w_ok = True
                    if not w_ok:
                        target = np.zeros(nsym)
                else:
                    target[longs] = (p.gross / 2.0) / longs.sum()
                    target[shorts] = -(p.gross / 2.0) / shorts.sum()
                target = np.clip(target, -p.max_weight, p.max_weight)
                # Re-balance the legs so the book is actually neutral: clipping
                # can leave one side larger, and an unintended net is a
                # directional bet the strategy never agreed to take.
                lsum, ssum = target[target > 0].sum(), -target[target < 0].sum()
                if lsum > 0 and ssum > 0:
                    avg = (lsum + ssum) / 2
                    target[target > 0] *= avg / lsum
                    target[target < 0] *= avg / ssum
                net = target.sum()
                if abs(net) > p.net_cap:
                    target -= net / max(1, (target != 0).sum()) * (target != 0)

        delta = target - w
        turn = float(np.abs(delta).sum())
        if turn > 0.001:
            eq *= (1.0 - turn * cost)
            turnover += turn
            rebalances += 1
            w = target

    diag = {"rebalances": rebalances, "total_turnover": turnover,
            "avg_gross": float(np.mean(gross_hist[warm:])) if n > warm else 0.0}
    return equity, diag


def nmetrics(u, equity, diag):
    eq = equity[~np.isnan(equity)]
    if len(eq) < 2:
        return {}
    r = np.diff(eq) / np.where(eq[:-1] == 0, np.nan, eq[:-1])
    r = r[~np.isnan(r)]
    years = (u.t[-1] - u.t[0]) / (365.25 * 86400)
    total = eq[-1] / eq[0] - 1
    peak = np.maximum.accumulate(eq)
    maxdd = float(np.min(eq / peak - 1))
    ann = math.sqrt(365 * u.bars_per_day)
    sd = float(np.std(r))
    sharpe = float(np.mean(r) / sd * ann) if sd > 0 else 0.0
    bsym = next((s for s in ("BTCUSDT", "BTC/USD") if s in u.symbols), None)
    bench = None
    if bsym:
        b = u.mark[u.symbols.index(bsym)]
        b = b[~np.isnan(b)]
        bench = float(b[-1] / b[0] - 1) if len(b) > 1 else None
    cagr = (1 + total) ** (1 / years) - 1 if years > 0 and total > -1 else float("nan")
    return {"total_return": float(total), "cagr": float(cagr), "max_drawdown": maxdd,
            "sharpe": sharpe, "calmar": float(cagr / abs(maxdd)) if maxdd < 0 else float("nan"),
            "end_equity": float(eq[-1]), "btc": bench, **diag}
