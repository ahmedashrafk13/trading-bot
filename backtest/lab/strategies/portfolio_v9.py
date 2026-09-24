"""portfolio_v9 - the frozen live book: micro_crowd + micro_flowts in ONE netted perp account.

Built by the final-exam agent from walk-forward OOS streams only (see results/PORTFOLIO.json,
results/REPORT.md). Nothing here was tuned on the lockbox (>= 2025-07-01).

  target notional_j / equity = m * ( rw_crowd * w_crowd_j + rw_flowts * w_flowts_j )
    w_crowd  = micro_crowd.weights(panel, FROZEN_crowd)        (12 majors, vol_target 0.20)
    w_flowts = micro_flowts.weights(BTC column, FROZEN_flowts)  (BTC only, vol_target 0.20)
    rw       = inverse-vol risk weights from the WF-OOS streams (2022-12-01..2025-06-27)
    m        = book multiplier; m = 1.4133 is the recommended 25% annual-vol level
               (menu: 0.15 -> 0.8480, 0.25 -> 1.4133, 0.35 -> 1.9786, 0.50 -> 2.8051, 0.70 -> 4.0133)

PANEL: 6h Binance USDT-M bars, the 12 metrics majors, from 2020-01-01, with taker-buy volume
(meta["tbqv"]) and data.load_metrics(...) attached as panel.meta["metrics"].
Decisions only at the 6h closes (00/06/12/18 UTC -> the :07 runs); market orders; no resting entries.
"""
from __future__ import annotations

import dataclasses
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data  # noqa: E402
from lab.strategies import micro_crowd as CR  # noqa: E402
from lab.strategies import micro_flowts as FT  # noqa: E402

NAME = "portfolio_v9"
SYMBOLS = list(data.MAJORS[:12])
PANEL = dict(timeframe="6h", symbols=SYMBOLS, start="2020-01-01", with_taker=True)
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False
RISK_WEIGHTS = {"micro_crowd": 0.477942, "micro_flowts": 0.522058}
SLEEVE_PARAMS = {"micro_crowd": dict(CR.FROZEN), "micro_flowts": dict(FT.FROZEN)}
M_BY_VOL = {0.15: 0.847991, 0.25: 1.413318, 0.35: 1.978646, 0.50: 2.805109, 0.70: 4.013277}
FROZEN = dict(rw=RISK_WEIGHTS, params=SLEEVE_PARAMS, m=M_BY_VOL[0.25])
GRID = [FROZEN]            # nothing searched at the portfolio level (rule-based weights)


def load(end=None):
    p = data.load_panel("6h", symbols=SYMBOLS, start="2020-01-01", end=end, with_taker=True)
    p.meta["metrics"] = data.load_metrics(SYMBOLS, "6h", start="2020-01-01", end=end)
    return p


def _colsub(p, idx):
    T, N = p.c.shape

    def cut(v):
        if isinstance(v, np.ndarray) and v.ndim == 2 and v.shape == (T, N):
            return v[:, idx]
        if isinstance(v, dict):
            return {k: cut(x) for k, x in v.items()}
        return v
    kw = {f.name: ([p.symbols[j] for j in idx] if f.name == "symbols" else cut(getattr(p, f.name)))
          for f in dataclasses.fields(p)}
    return dataclasses.replace(p, **kw)


def sleeve_weights(panel, params=None):
    params = params or FROZEN
    T, N = panel.c.shape
    wc = np.asarray(CR.weights(panel, params["params"]["micro_crowd"]), float)
    j = panel.symbols.index("BTCUSDT")
    wf = np.zeros((T, N))
    wf[:, j] = np.asarray(FT.weights(_colsub(panel, [j]), params["params"]["micro_flowts"]), float)[:, 0]
    return {"micro_crowd": wc, "micro_flowts": wf}


def weights(panel, params=None, metrics=None):
    params = params or FROZEN
    if metrics is not None:
        panel.meta["metrics"] = metrics
    sw = sleeve_weights(panel, params)
    W = sum(params["rw"][s] * sw[s] for s in sw)
    return float(params["m"]) * W


def live_targets(panel, params=None, metrics=None, equity=200.0, instruments=None):
    """Targets as of the LAST bar of `panel` (its close = the decision time)."""
    params = params or FROZEN
    if metrics is not None:
        panel.meta["metrics"] = metrics
    sw = sleeve_weights(panel, params)
    W = weights(panel, params)
    i = len(panel.t) - 1
    g = float(np.abs(W[i]).sum())
    stop = min(0.15, 0.5 / max(g, 1.0))
    ins = instruments or {}
    rows = {}
    for j, s in enumerate(panel.symbols):
        if W[i, j] == 0 and all(sw[k][i, j] == 0 for k in sw):
            continue
        px = float(panel.c[i, j])
        notional = float(W[i, j]) * equity
        step = float((ins.get(s) or {}).get("qtyStep") or 0) or None
        qty = None if step is None else float(np.floor(abs(notional) / px / step) * step) * np.sign(notional)
        rows[s] = {"weight": float(W[i, j]), "notional_usd": notional, "qty_rounded": qty,
                   "sleeves": {k: float(params["rw"][k] * params["m"] * sw[k][i, j]) for k in sw},
                   "stop_loss_price": (px * (1 - stop) if notional > 0 else px * (1 + stop)) if notional else None}
    return {"as_of_bar_open": int(panel.t[i]), "decision_time": int(panel.t[i] + panel.dt),
            "gross_after": g, "stop_distance": stop, "targets": rows,
            "orders": "market orders at the :07 run to move each perp to target (reduceOnly for cuts/closes); "
                      "skip an order below max($5, minOrderQty*price) unless it closes the position; "
                      "every open position carries a mark-price stopLoss at stop_distance from the fill"}
