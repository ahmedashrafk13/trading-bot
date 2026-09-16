#!/usr/bin/env python3
"""Signal bake-off: which entry rule, if any, actually predicts?

Runs every candidate in signals.py against forward returns at several horizons,
in-sample and out-of-sample, alongside a random null baseline.

    python backtest/research.py

Reading the output: compare every row to the RANDOM row, not to zero. The
random signal will not score exactly 0.00 - it wanders, and how far it wanders
IS the noise floor for this dataset. A candidate that does not clearly exceed it
has no demonstrated edge.
"""
from __future__ import annotations

import numpy as np

from engine import Universe
from signals import CANDIDATES, forward_return, information_coefficient

HORIZONS = [6, 24, 24 * 7]     # hours: intraday, daily, weekly
WARM = 24 * 31


def main():
    u = Universe()
    n = len(u.t)
    split = int(n * 0.6)
    print(f"universe: {len(u.symbols)} symbols, {n} hourly bars")
    print(f"train: bars {WARM}-{split}   test: bars {split}-{n}")
    print("\nInformation coefficient = per-hour rank correlation of signal vs")
    print("forward return. Compare every row to RANDOM, not to zero.\n")

    fwd = {h: forward_return(u, h) for h in HORIZONS}

    head = f"{'signal':30}" + "".join(f"{'IC@' + str(h) + 'h':>22}" for h in HORIZONS)
    print(head)
    print(f"{'':30}" + "".join(f"{'train':>11}{'test':>11}" for _ in HORIZONS))
    print("-" * len(head))

    rows = {}
    for name, fn in CANDIDATES.items():
        sig = fn(u)
        cells, rec = "", {}
        for h in HORIZONS:
            ic_tr, t_tr, _ = information_coefficient(sig[:, :split], fwd[h][:, :split], WARM)
            ic_te, t_te, _ = information_coefficient(sig[:, split:], fwd[h][:, split:], 0)
            rec[h] = (ic_tr, ic_te, t_tr, t_te)
            cells += f"{ic_tr:>+11.4f}{ic_te:>+11.4f}"
        rows[name] = rec
        mark = "  <- NULL" if "RANDOM" in name else ""
        print(f"{name:30}{cells}{mark}")

    null = rows["RANDOM (null baseline)"]
    print("\n" + "=" * len(head))
    print("VERDICT — a candidate must beat the null on BOTH train and test,")
    print("with the same sign, to count as anything at all.")
    print("=" * len(head))

    survivors = []
    for name, rec in rows.items():
        if "RANDOM" in name:
            continue
        for h in HORIZONS:
            ic_tr, ic_te, t_tr, t_te = rec[h]
            n_tr, n_te = null[h][0], null[h][1]
            floor = max(abs(n_tr), abs(n_te), 0.005)
            # same sign in both halves, and bigger than the noise floor in both
            if (abs(ic_tr) > floor and abs(ic_te) > floor
                    and np.sign(ic_tr) == np.sign(ic_te) and abs(t_te) > 2.0):
                survivors.append((name, h, ic_tr, ic_te, t_te))

    if not survivors:
        print("\n  NOTHING SURVIVED.")
        print("  No candidate predicts forward returns out of sample better than")
        print("  a random number. That includes both signals the live bot uses.")
        print("\n  This is the real finding: the problem is not the trail width,")
        print("  the position sizing, the trade frequency or the fees. There is")
        print("  no predictive signal for any of that machinery to exploit.")
        print("  Trading it more often converts the same non-edge into losses faster.")
    else:
        print()
        for name, h, ic_tr, ic_te, t_te in sorted(survivors, key=lambda x: -abs(x[3])):
            d = "as-is" if ic_te > 0 else "INVERTED (the rule is backwards)"
            print(f"  {name:30} @{h:>4}h   train {ic_tr:+.4f}  test {ic_te:+.4f}"
                  f"  t={t_te:+.1f}   use {d}")
        print("\n  These are candidates, NOT conclusions. An IC this small still")
        print("  has to survive fees before it is worth trading.")

    print()


if __name__ == "__main__":
    main()
