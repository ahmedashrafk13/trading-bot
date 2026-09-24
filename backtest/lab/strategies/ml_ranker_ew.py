"""ml_ranker_ew - the NO-FITTING control of family H: equal-weight average of pre-signed,
cross-sectionally ranked features on the PIT top-50 perps, 1d decisions.

Everything (features, signs, portfolio, grid, walk-forward) is exactly the 'ew' model that was
PRE-REGISTERED in strategies/ml_ranker.py on 2026-09-24 as the sanity baseline the ML models had to
beat. It was not designed to be a strategy; it is promoted to its own module only because it beat
both fitted models out of sample (see results/ml_ranker.json "comparison").

Signal: mean over available features of sign * centred cross-sectional rank, signs (pre-registered):
  r1 -, r3 -, r7 +, r14 +, r30 +, r60 +, rv7 -, rv30 -, volvol -, dhi +, dlo +, vz7 -, vz30 -,
  tb1 +, tb7 +, f1 -, f7 -, df -, zG -, zT +, D +, oi1 -, oi7 -.
Portfolio: long top-k / short bottom-k, +-0.5/k, rank buffer 2k, stagger H, vol target (60d, gross
  <= 3), |w| <= 0.25 per name, 0.02 band. GRID: H in {1, 3} x k in {5, 10} (4 of the 12 family-H
  trials; the family counts 14 incl. two lgbm variants).

IMPORTANT CAVEAT: the signs of tb1/tb7 (+), zG (-) and D (+) were informed by phase-2 results that
used the same 2022..2025-06 dev data, so for those components this is not a clean out-of-sample
test. results/ml_ranker_ew.json "ablation" separates the textbook-prior groups from them.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import ml_ranker as MR  # noqa: E402

NAME = "ml_ranker_ew"
DESCRIPTION = ("PIT top-50 perps, 1d decisions: equal-weight composite of 23 pre-signed cross-sectional "
               "ranks (reversal, momentum, low vol, volume, taker flow, funding carry, crowd L/S, OI); "
               "long top-k / short bottom-k, dollar neutral, vol-targeted. No fitting.")
MECHANISM = ("Diversified multi-factor composite: each factor is weak and fee-dominated alone; averaging "
             "ranks cancels much of their idiosyncratic noise while keeping turnover low (~60x/yr). About "
             "a third of the return is funding received (long negative-funding, short positive-funding).")
PANEL = MR.PANEL
USES_METRICS = True
KIND = "weights"
NEEDS_HOURLY_RUNS = False
GRID = [g for g in MR.GRID if g["model"] == "ew"]
FROZEN = dict(model="ew", H=1, k=10, vol_target=0.20)     # stability pick, see results/ml_ranker_ew.json
CAVEATS = list(MR.CAVEATS)


def weights(panel, params, metrics=None):
    return MR.weights(panel, dict(params, model="ew"), metrics)


def live_targets(panel, params=None, metrics=None):
    """Daily at the 00:07 UTC run on a 1d panel ending with the just-closed bar (metrics attached).
    No model, no retrain."""
    return MR.live_targets(panel, dict(params or FROZEN, model="ew"), metrics)
