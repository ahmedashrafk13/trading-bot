#!/usr/bin/env python3
"""Signal bake-off scored against the NULL at matched exposure, not against BTC.

WHY THIS EXISTS (2026-09-23)
----------------------------
Scoring a config by "EDGE vs BTC" is worthless on a window where BTC fell 36%:
holding nothing scores +36.35%, and any change that merely reduces exposure looks
like a discovery. That is exactly what happened when this bake-off was first run
by hand -- a 1-slot/30%-trail config scored +21% and looked like an edge, until
the same config run on MOMENTUM (known-negative IC) scored +24.65% and on RANDOM
scored +20.53%. The ranking was backwards because the worse signal traded less.

So every candidate here is run twice under IDENTICAL settings: once with the
signal, once with the random null. The only number that means anything is the
DIFFERENCE, and only if it holds in both halves of the data.

Usage:
    python backtest/bakeoff.py                 # full period
    python backtest/bakeoff.py --split         # train/test halves
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SIGNALS = [
    # price/volume derived
    "momentum", "downside_vol", "lowvol", "liquidity", "reversion",
    "volume_surge", "liquidity_downside_vol",
    # NON-PRICE, added 2026-09-23: open interest and crowd positioning.
    # These are the first signals here that use data a price series cannot
    # reconstruct, which is the only category that has produced anything.
    "oi_divergence", "oi_surge", "oi_squeeze",
    "crowd_contrarian", "crowd_shift",
    "crowd_liquidity", "oi_downside_vol",
]

# Friction regimes. The whole question is whether a signal's gross edge can
# clear its trading costs, so cost is a variable, not a constant.
#   taker  - what the account actually pays today (measured 0.65% round trip)
#   maker  - limit entries, roughly half
#   zero   - no friction: isolates pure signal quality
# CORRECTED 2026-09-23 to the MEASURED linear-perp fees (0.055%/side from 39
# real fills), not the old spot-era 35bps that overstated friction ~6x.
REGIMES = {"perp_taker": (5.5, 2), "perp_maker": (2, 1), "zero": (0, 0)}


def run(signal, fee, spread, extra, days=0):
    cmd = [sys.executable, os.path.join(HERE, "run.py"), "--timeframe", "1H",
           "--set", f"entry_signal={signal}",
           "--set", f"fee_bps={fee}", "--set", f"spread_bps={spread}"]
    for k, v in extra.items():
        cmd += ["--set", f"{k}={v}"]
    if days:
        cmd += ["--days", str(days)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    ret = trades = None
    for line in out.splitlines():
        if "equity" in line and "->" in line:
            ret = float(line.split("(")[-1].split("%")[0])
        if line.strip().startswith("trades"):
            trades = int(line.split()[1])
    return ret, trades


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", action="store_true",
                    help="also run the most recent half as an out-of-sample check")
    ap.add_argument("--slots", type=int, default=6)
    ap.add_argument("--trail", type=float, default=0.10)
    a = ap.parse_args()

    extra = {"tac_slots": a.slots, "tac_trail": a.trail, "core_slots": 0}
    print(f"\nBAKE-OFF  slots={a.slots} trail={a.trail:.0%} core=0")
    print("Scored as SIGNAL minus RANDOM at identical settings. Positive = the")
    print("signal carried information. 'vs BTC' is shown but is NOT the test.\n")

    for regime, (fee, spread) in REGIMES.items():
        null_ret, null_tr = run("random", fee, spread, extra)
        if null_ret is None:
            print(f"{regime}: null failed to run")
            continue
        print(f"--- {regime} friction (fee {fee}bps/side, spread {spread}bps) "
              f"| NULL = {null_ret:+.2f}% on {null_tr} trades")
        rows = []
        for sig in SIGNALS:
            r, tr = run(sig, fee, spread, extra)
            if r is None:
                continue
            rows.append((r - null_ret, r, tr, sig))
        for d, r, tr, sig in sorted(rows, reverse=True):
            flag = "  <-- beats the null" if d > 0 else ""
            print(f"    {sig:26} {r:+8.2f}%   vs null {d:+7.2f}pp  "
                  f"({tr} trades){flag}")
        print()

    if a.split:
        print("OUT-OF-SAMPLE: most recent 180 days only")
        for regime, (fee, spread) in REGIMES.items():
            null_ret, _ = run("random", fee, spread, extra, days=180)
            if null_ret is None:
                continue
            rows = []
            for sig in SIGNALS:
                r, _ = run(sig, fee, spread, extra, days=180)
                if r is not None:
                    rows.append((r - null_ret, sig))
            best = sorted(rows, reverse=True)[:3]
            print(f"  {regime:6} null {null_ret:+7.2f}%  | top: " +
                  ", ".join(f"{s} {d:+.1f}pp" for d, s in best))


if __name__ == "__main__":
    main()
