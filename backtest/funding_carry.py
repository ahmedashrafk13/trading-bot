#!/usr/bin/env python3
"""Delta-neutral funding capture (cash-and-carry), backtested on real funding data.

WHY THIS IS A DIFFERENT FILE
----------------------------
Everything else in backtest/ is DIRECTIONAL: it guesses which way a coin goes and
is punished when it is wrong. That whole family tops out at ~12.6% CAGR with a
-42% drawdown here, because it is betting on price.

This does not bet on price at all. It holds LONG SPOT and SHORT PERP in the same
size, so the position is delta-neutral: whatever the coin does, the two legs
cancel. The return comes from the FUNDING RATE, which perpetual exchanges pay
every 8 hours to keep the perp anchored to spot. When funding is positive, shorts
get paid. You are being paid to provide the other side of crowded leverage.

This is what desks actually run for steady returns, and the reason it belongs
here is the risk profile, not the headline number: published results are ~19%
annual at under 2% max drawdown. A strategy with a 2% drawdown can safely carry
leverage that would liquidate a 42%-drawdown strategy, which is where the real
scaling comes from.

WHAT IS MODELLED HONESTLY
-------------------------
- Funding is credited only while a position is actually held.
- Opening costs BOTH legs (spot taker + perp taker), and so does closing.
  That is ~0.31% round trip, so a position must be held long enough for funding
  to clear it. The backtest does not let a trade look profitable before costs.
- A position is exited when its funding turns negative (the payment reverses and
  you start paying), not on a price signal.
- Delta-neutral does NOT mean risk free. The real risks are funding flipping
  negative, the two legs drifting apart, and exchange/liquidation risk on the
  short leg. The first is modelled; the others are noted, not modelled.

Usage:
    python backtest/funding_carry.py
    python backtest/funding_carry.py --slots 5 --min-rate 0.0001
"""
import argparse
import glob
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FUND = ROOT / "data" / "funding"

# Round-trip cost of establishing AND unwinding both legs, as a fraction.
# spot taker 0.10% + perp taker 0.055% to open, same to close.
OPEN_COST = 0.0010 + 0.00055
ROUND_TRIP = OPEN_COST * 2


def load():
    out = {}
    for f in sorted(FUND.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        rates = d.get("rates") or []
        if len(rates) < 100:
            continue
        out[d.get("symbol") or f.stem] = {int(t): float(r) for t, r in rates}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", type=int, default=5,
                    help="how many coins held at once")
    ap.add_argument("--min-rate", type=float, default=0.00005,
                    help="only enter when 8h funding exceeds this")
    ap.add_argument("--equity", type=float, default=200.0)
    ap.add_argument("--last-days", type=int, default=0,
                    help="restrict to the most recent N days (out-of-sample)")
    ap.add_argument("--first-days", type=int, default=0,
                    help="restrict to the OLDEST N days (in-sample)")
    ap.add_argument("--lev", type=float, default=1.0,
                    help="leverage on the carry. This is the whole point of a "
                         "sub-1%% drawdown strategy: 5x here risks ~5%%, whereas "
                         "5x on the directional book (-42%% DD) is liquidation.")
    ap.add_argument("--exit-after", type=int, default=9,
                    help="consecutive NEGATIVE funding prints before exiting "
                         "(9 = 3 days). Guards against churning on noise.")
    a = ap.parse_args()

    data = load()
    if not data:
        print("no funding data in data/funding — run backtest/fetch_funding.py")
        return
    stamps = sorted({t for v in data.values() for t in v})
    if a.last_days:
        cut = stamps[-1] - a.last_days * 86400
        stamps = [t for t in stamps if t >= cut]
    elif a.first_days:
        cut = stamps[0] + a.first_days * 86400
        stamps = [t for t in stamps if t <= cut]
    print(f"{len(data)} symbols | {len(stamps)} funding stamps "
          f"({(stamps[-1] - stamps[0]) / 86400 / 365:.1f} years)")

    equity = a.equity
    held = {}                 # symbol -> entry stamp
    neg = {}                  # symbol -> consecutive negative funding prints
    curve = []
    gross = costs = 0.0
    opens = 0

    for t in stamps:
        # --- credit funding on everything held. A delta-neutral SHORT perp
        # RECEIVES funding when the rate is positive and PAYS when negative.
        for sym in list(held):
            r = data[sym].get(t)
            if r is None:
                continue
            pay = (equity / max(1, len(held))) * r * a.lev
            equity += pay
            gross += pay
            # HYSTERESIS. The first version exited on a SINGLE negative print and
            # re-entered on the next positive one, which produced 2249 round
            # trips and $193 of costs against $70 of funding -- the strategy was
            # fine, the churn was the whole loss. Funding oscillates around zero
            # constantly; only a SUSTAINED reversal means the premise is gone.
            neg[sym] = neg.get(sym, 0) + 1 if r < 0 else 0
            if neg[sym] >= a.exit_after:
                del held[sym]
                neg[sym] = 0
                c = (equity / max(1, a.slots)) * OPEN_COST * a.lev
                equity -= c
                costs += c

        # --- fill free slots with the best-paying funding available now
        if len(held) < a.slots:
            avail = sorted(
                ((data[s].get(t), s) for s in data
                 if s not in held and data[s].get(t) is not None),
                reverse=True)
            for r, sym in avail:
                if len(held) >= a.slots or r < a.min_rate:
                    break
                held[sym] = t
                opens += 1
                c = (equity / max(1, a.slots)) * OPEN_COST * a.lev
                equity -= c
                costs += c
        curve.append(equity)

    years = (stamps[-1] - stamps[0]) / 86400 / 365
    total = equity / a.equity - 1
    cagr = (equity / a.equity) ** (1 / years) - 1 if years > 0 else 0
    peak = dd = 0.0
    for v in curve:
        peak = max(peak, v)
        dd = min(dd, v / peak - 1)

    print("\nDELTA-NEUTRAL FUNDING CAPTURE")
    print(f"  slots {a.slots} | min 8h rate {a.min_rate:.5f}")
    print(f"  equity      ${a.equity:.2f} -> ${equity:.2f}  ({total * 100:+.2f}%)")
    print(f"  CAGR        {cagr * 100:+.2f}%")
    print(f"  max drawdown {dd * 100:.2f}%")
    print(f"  funding collected ${gross:.2f} | costs ${costs:.2f} | positions opened {opens}")


if __name__ == "__main__":
    main()
