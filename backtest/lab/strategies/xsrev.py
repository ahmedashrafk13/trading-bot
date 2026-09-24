"""
strategies/xsrev.py -- cross-sectional SHORT-TERM REVERSAL (family C, research #7
variant). Long the 1-3 day losers, short the 1-3 day winners among the
point-in-time top-30 perps, beta-hedged to BTC or dollar-neutral, vol-targeted.
Rebalanced daily or every 3 days at 00:00 UTC (a 6h decision point, so
needs_hourly_runs = False). Same machinery as strategies/xsmom.py (signal "rev").

Kept as its own module (not inside xsmom's GRID) so the reversal and momentum
streams each get their own walk-forward, deflated Sharpe and null, and a portfolio
can hold both: they are expected to be negatively correlated.
"""
from __future__ import annotations

import numpy as np

try:
    from . import xsmom as _X
except ImportError:                                  # plain-directory import
    import xsmom as _X

PANEL = dict(timeframe="1d", universe="pit_top30", start="2020-01-01")
USES_METRICS = False
KIND = "weights"

_BASE = dict(_X._BASE, signal="rev", skip=0)

GRID = [dict(_BASE, lookback=L, k=k, hedge=h, rebalance_days=rb)
        for L in (1, 2, 3) for k in (3, 5) for h in ("ls_beta", "ls_dollar") for rb in (1, 3)]

FROZEN = dict(_BASE, lookback=1, k=3, hedge="ls_dollar", rebalance_days=3)   # WF: most chosen; FAILS


def weights(panel, params, metrics=None) -> np.ndarray:
    return _X.build(panel, dict(params, signal="rev"))


def null_weights(panel, params, seed: int) -> np.ndarray:
    return _X.build(panel, dict(params, signal="rev"), rng=np.random.default_rng(seed))


def live_targets(panel, params, metrics=None) -> dict:
    return _X.live_targets(panel, dict(params, signal="rev"))
