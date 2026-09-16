#!/usr/bin/env python3
"""Parameter search with an honest out-of-sample verdict.

A grid search over a few months of crypto bars will ALWAYS find a parameter set
that would have made money. That number is worthless on its own: with ~200
combinations you expect the best in-sample result to look good by luck alone.
So this script never reports an in-sample winner as an improvement. It reports:

  1. IN-SAMPLE best      - what the tuner found on the training slice.
  2. OUT-OF-SAMPLE       - that same parameter set replayed on data the tuner
                           never saw. This is the only number worth acting on.
  3. OVERFIT GAP         - (1) minus (2). A large gap means the tuner fitted
                           noise, no matter how good (1) looks.
  4. WALK-FORWARD        - retune on a rolling window, trade the next window,
                           repeat, and stitch the out-of-sample pieces together.
                           This is what "would it have worked live" actually
                           means, because live you only ever have the past.
  5. BASELINE            - the shipped v2 defaults, same slices, so any claimed
                           improvement is measured against what you run today.

Usage:
    python backtest/sweep.py --quick          # small grid, fast sanity pass
    python backtest/sweep.py                  # full grid + walk-forward
    python backtest/sweep.py --metric sharpe  # rank on something other than return
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
from dataclasses import replace

import numpy as np

from engine import Params, Universe, run, metrics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The grid is deliberately SMALL. Every extra axis multiplies the number of ways
# the tuner can fit noise, and the out-of-sample penalty grows with it.
FULL_GRID = {
    # The trail axes run well past the shipped values on purpose: the quick grid
    # pinned core_trail at its upper boundary, which means the boundary — not the
    # data — was choosing the answer. An axis whose best value sits at the edge
    # has not been searched.
    "core_trail": [0.15, 0.25, 0.35, 0.50],
    "tac_trail": [0.10, 0.20, 0.35, 0.50],
    "core_risk": [0.015, 0.020, 0.030],
    "tac_risk": [0.005, 0.010, 0.020],
    "core_max_ext": [0.15, 0.20, 0.30],
    "tac_ext_band": [0.05, 0.08, 0.12],
}

QUICK_GRID = {
    "core_trail": [0.15, 0.25],
    "tac_trail": [0.10, 0.20],
    "core_risk": [0.020, 0.030],
}


def combos(grid):
    keys = sorted(grid)
    for vals in itertools.product(*(grid[k] for k in keys)):
        yield dict(zip(keys, vals))


def score(u, p, metric):
    eq, tr = run(u, p)
    m = metrics(u, eq, tr)
    if not m or m["trades"] < 5:
        # Too few trades to mean anything. Scoring these as terrible stops the
        # tuner from "winning" with a parameter set that simply never trades.
        return -1e9, m
    return m.get(metric, -1e9), m


def slice_universe(u, lo_frac, hi_frac):
    """A time-window view of the universe, signals recomputed for that window."""
    n = len(u.t)
    return Universe(start=int(u.t[int(n * lo_frac)]), end=int(u.t[min(n - 1, int(n * hi_frac))]))


def fmt(m):
    if not m:
        return "  (no result)"
    bh = m.get("btc_buyhold")
    return (f"  return {m['total_return']:+7.2%}   BTC {bh:+7.2%}   edge {m['edge_vs_btc']:+7.2%}\n"
            f"  sharpe {m['sharpe']:+6.2f}   maxDD {m['max_drawdown']:+7.2%}   "
            f"PF {m['profit_factor']:.2f}\n"
            f"  trades {m['trades']:3d}   win {m['win_rate']:.1%}   "
            f"expectancy ${m['expectancy']:+.2f}   avg hold {m['avg_bars_held']:.0f}h"
            if bh is not None else
            f"  return {m['total_return']:+7.2%}   sharpe {m['sharpe']:+6.2f}   "
            f"trades {m['trades']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--metric", default="total_return",
                    choices=["total_return", "sharpe", "sortino", "profit_factor", "expectancy"])
    ap.add_argument("--train", type=float, default=0.60, help="fraction of history used to tune")
    ap.add_argument("--folds", type=int, default=4, help="walk-forward folds")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "sweep-results.json"))
    a = ap.parse_args()

    grid = QUICK_GRID if a.quick else FULL_GRID
    n_combos = len(list(combos(grid)))

    full = Universe()
    span_days = (full.t[-1] - full.t[0]) / 86400
    print(f"history: {len(full.symbols)} symbols, {span_days:.0f} days, {len(full.t)} hourly bars")
    print(f"grid: {n_combos} combinations, ranked on {a.metric}\n")

    base = Params()

    # ---------------------------------------------------------------- 1) split
    train = slice_universe(full, 0.0, a.train)
    test = slice_universe(full, a.train, 1.0)

    print("=" * 72)
    print(f"BASELINE (shipped v2 defaults)")
    print("=" * 72)
    _, bm_tr = score(train, base, a.metric)
    _, bm_te = score(test, base, a.metric)
    print("IN-SAMPLE  (train)\n" + fmt(bm_tr))
    print("OUT-OF-SAMPLE (test)\n" + fmt(bm_te))

    print("\n" + "=" * 72)
    print(f"TUNED — searching {n_combos} combinations on the TRAIN slice only")
    print("=" * 72)
    results = []
    for k, ov in enumerate(combos(grid), 1):
        s, m = score(train, replace(base, **ov), a.metric)
        results.append((s, ov, m))
        if k % max(1, n_combos // 10) == 0:
            print(f"  ...{k}/{n_combos}")
    results.sort(key=lambda r: r[0], reverse=True)

    best_s, best_ov, best_m = results[0]
    tuned = replace(base, **best_ov)
    _, oos_m = score(test, tuned, a.metric)

    print("\nbest params:", json.dumps(best_ov))
    print("IN-SAMPLE  (train)\n" + fmt(best_m))
    print("OUT-OF-SAMPLE (test)\n" + fmt(oos_m))

    gap = best_m.get(a.metric, 0) - oos_m.get(a.metric, 0)
    print(f"\nOVERFIT GAP ({a.metric}): {gap:+.4f}")

    # Two separate questions, and conflating them is how a losing strategy gets
    # adopted: (a) did tuning beat the defaults, and (b) does the tuned set
    # actually MAKE MONEY. Beating a worse baseline while still losing is not an
    # improvement, it is a smaller loss.
    beat_baseline = oos_m.get(a.metric, -1e9) > bm_te.get(a.metric, -1e9)
    oos_return = oos_m.get("total_return", -1)
    oos_edge = oos_m.get("edge_vs_btc")
    if not beat_baseline:
        print("  VERDICT: the tuned set did NOT beat the shipped defaults out of sample.")
        print("  Do not adopt it. The in-sample gain was noise.")
    elif oos_return <= 0:
        print(f"  VERDICT: tuned set beat the defaults but still LOST money out of "
              f"sample ({oos_return:+.2%}).")
        print("  That is a smaller loss, not an edge. Do not adopt it as an improvement.")
    elif oos_edge is not None and oos_edge <= 0:
        print(f"  VERDICT: tuned set made money out of sample ({oos_return:+.2%}) but still")
        print(f"  underperformed simply holding BTC ({oos_edge:+.2%}). Not worth the machinery.")
    else:
        print("  VERDICT: tuned set was profitable AND beat BTC out of sample.")
        print("  Worth taking seriously — confirm on the walk-forward below before adopting.")

    # --------------------------------------------------- 2) top-N stability
    # If the top 10 in-sample sets disagree wildly out of sample, the surface is
    # noise and the single 'best' is meaningless regardless of its OOS number.
    print("\n" + "=" * 72)
    print("TOP-10 STABILITY (in-sample rank vs out-of-sample result)")
    print("=" * 72)
    oos_vals = []
    for s, ov, m in results[:10]:
        _, mo = score(test, replace(base, **ov), a.metric)
        v = mo.get(a.metric, float("nan"))
        oos_vals.append(v)
        print(f"  IS {s:+9.4f}  OOS {v:+9.4f}   {json.dumps(ov)}")
    finite = [v for v in oos_vals if v == v and v > -1e8]
    if len(finite) >= 3:
        print(f"\n  OOS spread across the top 10: {min(finite):+.4f} .. {max(finite):+.4f}")
        if min(finite) < 0 < max(finite):
            print("  WARNING: the top in-sample sets straddle zero out of sample.")
            print("  The parameter surface is noise. Tuning it harder will not help.")

    # --------------------------------------------------- 3) walk-forward
    print("\n" + "=" * 72)
    print(f"WALK-FORWARD ({a.folds} folds — retune on the past, trade the next slice)")
    print("=" * 72)
    edges, rets = [], []
    step = 1.0 / (a.folds + 1)
    for f in range(a.folds):
        tr_hi = step * (f + 1)
        tr = slice_universe(full, 0.0, tr_hi)
        te = slice_universe(full, tr_hi, tr_hi + step)
        # key= is required: scores tie often, and without it Python falls through
        # to comparing the parameter dicts and raises.
        ranked = sorted(((score(tr, replace(base, **ov), a.metric)[0], ov) for ov in combos(grid)),
                        key=lambda x: x[0])
        ov = ranked[-1][1]
        _, m = score(te, replace(base, **ov), a.metric)
        if not m:
            print(f"  fold {f + 1}: no trades")
            continue
        rets.append(m["total_return"])
        if m.get("edge_vs_btc") is not None:
            edges.append(m["edge_vs_btc"])
        print(f"  fold {f + 1}: return {m['total_return']:+7.2%}  "
              f"edge vs BTC {m.get('edge_vs_btc', float('nan')):+7.2%}  "
              f"trades {m['trades']:3d}   params {json.dumps(ov)}")

    if rets:
        print(f"\n  walk-forward mean return: {np.mean(rets):+.2%}  "
              f"({sum(1 for r in rets if r > 0)}/{len(rets)} folds positive)")
    if edges:
        print(f"  walk-forward mean edge vs BTC: {np.mean(edges):+.2%}")
        if np.mean(edges) <= 0:
            print("\n  BOTTOM LINE: even retuned every fold, the strategy does not beat")
            print("  buying and holding BTC. The problem is the signal, not the parameters.")

    json.dump({"grid": grid, "metric": a.metric, "best": best_ov,
               "baseline_test": bm_te, "tuned_test": oos_m,
               "walk_forward_returns": rets, "walk_forward_edges": edges},
              open(a.out, "w", encoding="utf-8"), indent=2, default=str)
    print(f"\nwritten -> {a.out}")


if __name__ == "__main__":
    main()
