"""Strategy family A on a point-in-time liquid universe: the trend ensemble of
trend_ens.py traded on pit_top20 membership with new entries restricted to the
10 most liquid coins (trailing-30d quote volume) at each bar; an open position
is kept (frozen size) while its coin remains a top-20 member.  Includes
delisted coins (survivorship-aware).  See trend_ens.py for the signal/sizing.
"""
from __future__ import annotations

try:
    from . import trend_ens as _te
except ImportError:                      # imported as a top-level module
    import trend_ens as _te

PANEL = dict(timeframe="6h", universe="pit_top20", start="2020-01-01")
USES_METRICS = False
KIND = "weights"
TOPK = 10
BASE = dict(_te.BASE, topk=TOPK)
GRID = [dict(g, topk=TOPK) for g in _te.GRID]
# FROZEN = best MEDIAN train Sharpe across the 7 walk-forward folds
# (pit_top20 / top-10 entries, 6h, dev 2020-01..2025-06); see results/trend_ens_alts.json
FROZEN = dict(family="donch", direction="lo", band=0.05, gate=0.0, topk=TOPK)


def _q(params):
    q = dict(params or {})
    q.setdefault("topk", TOPK)
    return q


def weights(panel, params, metrics=None):
    return _te.weights(panel, _q(params))


def live_targets(panel, params, metrics=None):
    return _te.live_targets(panel, _q(params))
