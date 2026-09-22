#!/usr/bin/env python3
"""Statistical arbitrage (pairs trading) — the third, uncorrelated sleeve.

WHY
---
Published crypto stat-arb runs a Sharpe of roughly 1.4-1.5 while staying
market-neutral, and crucially its returns are driven by something neither of the
other two sleeves touch:

  TREND  needs a sustained directional move.       Fails in chop.
  CARRY  needs crowded leverage paying funding.    Fails when funding is flat.
  PAIRS  needs two correlated coins to DIVERGE and then converge.
         It works BEST in chop, which is exactly when trend bleeds.

That is the diversification argument in one line: pairs earns in the regime the
trend book hates.

HOW IT WORKS
------------
Take two coins whose log-price ratio mean-reverts. When the spread stretches
beyond z standard deviations, short the rich one and buy the cheap one in equal
notional. The position is direction-neutral: if the whole market drops, both
legs drop and the spread is unaffected. Close when the spread reverts to its
mean, or cut if it keeps widening past a stop.

Pairs are selected by correlation of returns AND a mean-reversion half-life in a
tradable band -- a spread that takes six months to revert ties up capital, and
one that reverts in an hour is noise being eaten by fees.

HONEST LIMITS
-------------
- Pair selection is done on the SAME data the strategy is tested on, which is
  look-ahead bias. A live implementation must re-select pairs on a rolling
  window using only past data. The number here is therefore optimistic.
- Correlation breaks. Two coins that tracked each other for a year can decouple
  permanently on a listing, a hack, or a delisting -- the spread never reverts
  and the stop is the only exit.
- Both legs pay fees and both can slip.
"""
import argparse
import glob
import itertools
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BARS = os.path.join(os.path.dirname(HERE), "data", "bars", "1H")
FEE = 0.000575          # perp taker per side, both legs charged


def load():
    px = {}
    for f in sorted(glob.glob(os.path.join(BARS, "*.json"))):
        d = json.load(open(f))
        rows = d if isinstance(d, list) else (d.get("bars") or [])
        if len(rows) < 2000:
            continue
        px[os.path.basename(f).replace(".json", "")] = {
            int(r[0]): float(r[4]) for r in rows}
    if not px:
        return [], {}
    common = sorted(set.intersection(*[set(v) for v in px.values()]))
    return common, {s: np.array([px[s][t] for t in common]) for s in px}


def find_pairs(M, min_corr=0.70, hl_lo=12, hl_hi=24 * 14):
    out = []
    for a, b in itertools.combinations(sorted(M), 2):
        ra, rb = np.diff(np.log(M[a])), np.diff(np.log(M[b]))
        c = np.corrcoef(ra, rb)[0, 1]
        if not np.isfinite(c) or c < min_corr:
            continue
        sp = np.log(M[a] / M[b])
        beta = np.polyfit(sp[:-1], np.diff(sp), 1)[0]
        if beta >= 0:
            continue
        hl = -math.log(2) / beta
        if hl_lo < hl < hl_hi:
            out.append((c, hl, a, b))
    out.sort(reverse=True)
    return out


def backtest(M, pairs, z_in, z_out, z_stop, lookback, equity=200.0, max_pos=4):
    """Trade the spread. Each position is one long leg + one short leg."""
    n = len(next(iter(M.values())))
    eq = equity
    open_pos = {}
    curve, trades, wins = [], 0, 0
    for i in range(lookback, n):
        for (a, b) in list(open_pos):
            sp = np.log(M[a][:i + 1] / M[b][:i + 1])
            mu, sd = sp[-lookback:].mean(), sp[-lookback:].std()
            if sd <= 0:
                continue
            z = (sp[-1] - mu) / sd
            side, entry_z, pa, pb = open_pos[(a, b)]
            hit = (abs(z) <= z_out) or (abs(z) >= z_stop)
            if hit:
                # REAL leg P&L, not an approximation. side=+1 means the spread
                # was BELOW its mean, so we are long A and short B; side=-1 is
                # the mirror. Each leg is half the position's notional.
                ra = M[a][i] / pa - 1.0
                rb = M[b][i] / pb - 1.0
                pnl_frac = side * (ra - rb) / 2.0
                notional = eq / max_pos
                gross = notional * pnl_frac
                eq += gross - notional * FEE * 4
                trades += 1
                wins += 1 if gross > 0 else 0
                del open_pos[(a, b)]
        if len(open_pos) < max_pos:
            for _c, _hl, a, b in pairs:
                if (a, b) in open_pos or len(open_pos) >= max_pos:
                    continue
                sp = np.log(M[a][:i + 1] / M[b][:i + 1])
                mu, sd = sp[-lookback:].mean(), sp[-lookback:].std()
                if sd <= 0:
                    continue
                z = (sp[-1] - mu) / sd
                if abs(z) >= z_in:
                    open_pos[(a, b)] = (-1 if z > 0 else 1, z,
                                        M[a][i], M[b][i])
        curve.append(eq)
    years = n / (24 * 365)
    cagr = (eq / equity) ** (1 / years) - 1 if years > 0 else 0
    peak = dd = 0.0
    for v in curve:
        peak = max(peak, v)
        dd = min(dd, v / peak - 1)
    return eq, cagr, dd, trades, (wins / trades if trades else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--z-in", type=float, default=2.0)
    ap.add_argument("--z-out", type=float, default=0.5)
    ap.add_argument("--z-stop", type=float, default=4.0)
    ap.add_argument("--lookback", type=int, default=24 * 14)
    a = ap.parse_args()

    common, M = load()
    if not M:
        print("no hourly bars")
        return
    pairs = find_pairs(M)
    print(f"{len(M)} symbols, {len(common)} bars ({len(common) / 24:.0f} days)")
    print(f"{len(pairs)} mean-reverting pairs")
    eq, cagr, dd, tr, wr = backtest(M, pairs, a.z_in, a.z_out, a.z_stop, a.lookback)
    print(f"\nPAIRS / STAT-ARB  z_in={a.z_in} z_out={a.z_out} z_stop={a.z_stop}")
    print(f"  equity  $200.00 -> ${eq:.2f}")
    print(f"  CAGR    {cagr * 100:+.2f}%   max drawdown {dd * 100:.2f}%")
    print(f"  trades  {tr}   win rate {wr * 100:.1f}%")
    print("\n  NOTE: pairs were selected on the same data they are tested on.")
    print("  That is look-ahead bias, so treat this as an UPPER BOUND.")


if __name__ == "__main__":
    main()
