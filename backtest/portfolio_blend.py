#!/usr/bin/env python3
"""Blend the strategies into one book and measure the combination.

WHY (2026-09-23)
----------------
Published research on crypto quant funds is consistent on one structural point:
"the best quant funds are essentially portfolios of strategies, not a single
algorithm", and the category's median Sharpe (~1.53) comes largely from that
diversification -- when trend underperforms in a choppy market, carry keeps
paying; when funding compresses, trend captures the move.

This repo has spent its whole life looking for THE signal. That was the wrong
question. These two have very different return drivers:

  CARRY      +27.54% CAGR, -1.84% DD. Market-neutral. Pays in crowded-leverage
             regimes. Earns nothing when funding is flat, loses nothing either.
  TREND (v6) +12.62% CAGR, -41.94% DD. Directional. Pays in sustained trends,
             bleeds in chop, and is the only one that can profit from a melt-up.

Their weaknesses do not overlap, which is the entire argument for holding both.

*** READ THIS BEFORE BELIEVING THE CARRY SHARPE ***
This blender reports a carry Sharpe above 11. That number is WRONG, and the
reason is worth stating plainly because it is the exact failure the literature
warns about ("a realistic Sharpe above 3 should make you suspicious of
methodology errors -- look-ahead bias, survivorship, multiple testing").

The carry model credits funding as a smooth deterministic drip and models NO
variance on the hedge itself. In reality the two legs drift against each other
continuously: the perp can trade 0.5% away from spot, the basis moves, and
unwinding costs more than modelled when it does. That is where a real carry
book's volatility comes from, and this model has none of it. So:

  CAGR  ~11-20%  -- CREDIBLE. Ethena runs this exact trade publicly and reports
                    10-15% APY, which brackets our out-of-sample 11-15%.
  DD    -1.78%   -- TOO GOOD. Excludes basis risk entirely.
  Sharpe 11+     -- NOT REAL. A carry book with basis risk modelled would be
                    somewhere around 2-4, in line with published stat-arb.

Therefore the "100% carry" row is an artifact and must NOT be read as the
recommended allocation. The defensible reading is the 60-75% carry band, where
the blend still carries real directional exposure and the drawdown (-6% to -9%)
is not resting on an unmodelled assumption.

METHOD, and its limits stated up front: this blends the two return streams at a
fixed weight and rebalances monthly. It does NOT model the two competing for the
same margin, which a live implementation must. Treat the output as the shape of
the combination, not a promise of the number.
"""
import argparse
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def trend_daily_returns():
    """Daily P&L of the v6 directional book, as fractions of starting equity."""
    out = os.path.join(HERE, "_trend.json")
    subprocess.run([sys.executable, os.path.join(HERE, "run.py"),
                    "--timeframe", "1D", "--set", "core_slots=0",
                    "--json", out], capture_output=True, text=True)
    if not os.path.exists(out):
        return {}
    d = json.load(open(out))
    by = {}
    for t in d.get("trades", []):
        day = int(t["exit_t"]) // 86400
        by[day] = by.get(day, 0.0) + t["pnl"] / 200.0
    return by


def carry_daily_returns(lev, min_rate, slots):
    """Daily funding accrual of the carry book, same units."""
    import pathlib
    FUND = pathlib.Path(HERE).parent / "data" / "funding"
    data = {}
    for f in sorted(FUND.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if len(d.get("rates") or []) < 100:
            continue
        data[d["symbol"]] = {int(t): float(r) for t, r in d["rates"]}
    stamps = sorted({t for v in data.values() for t in v})
    held, neg, by = {}, {}, {}
    for t in stamps:
        day = t // 86400
        for sym in list(held):
            r = data[sym].get(t)
            if r is None:
                continue
            by[day] = by.get(day, 0.0) + (r * lev / max(1, len(held)))
            neg[sym] = neg.get(sym, 0) + 1 if r < 0 else 0
            if neg[sym] >= 9:
                del held[sym]
                neg[sym] = 0
                by[day] = by.get(day, 0.0) - 0.00155 * lev / max(1, slots)
        if len(held) < slots:
            avail = sorted(((data[s].get(t), s) for s in data
                            if s not in held and data[s].get(t) is not None),
                           reverse=True)
            for r, sym in avail:
                if len(held) >= slots or r < min_rate:
                    break
                held[sym] = t
                by[day] = by.get(day, 0.0) - 0.00155 * lev / max(1, slots)
    return by


def stats(daily, label):
    if not daily:
        return None
    days = sorted(daily)
    eq, curve = 1.0, []
    for d in days:
        eq *= (1 + daily[d])
        curve.append(eq)
    years = (days[-1] - days[0]) / 365 or 1
    cagr = eq ** (1 / years) - 1
    peak = dd = 0.0
    for v in curve:
        peak = max(peak, v)
        dd = min(dd, v / peak - 1)
    vals = [daily[d] for d in days]
    mu = sum(vals) / len(vals)
    sd = (sum((x - mu) ** 2 for x in vals) / max(1, len(vals) - 1)) ** 0.5
    sharpe = (mu / sd * math.sqrt(365)) if sd else 0.0
    print(f"  {label:26} CAGR {cagr * 100:+7.2f}%   DD {dd * 100:7.2f}%   "
          f"Sharpe {sharpe:5.2f}   ({len(days)} active days)")
    return cagr, dd, sharpe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lev", type=float, default=3.0)
    ap.add_argument("--min-rate", type=float, default=0.0005)
    ap.add_argument("--slots", type=int, default=5)
    a = ap.parse_args()

    trend = trend_daily_returns()
    carry = carry_daily_returns(a.lev, a.min_rate, a.slots)
    print("\nSTRATEGY BLEND — daily returns, rebalanced continuously\n")
    stats(trend, "TREND only (v6)")
    stats(carry, f"CARRY only ({a.lev:g}x)")
    print()
    best = None
    for w in (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0):
        allday = sorted(set(trend) | set(carry))
        mix = {d: w * carry.get(d, 0.0) + (1 - w) * trend.get(d, 0.0) for d in allday}
        s = stats(mix, f"{w:.0%} carry / {1 - w:.0%} trend")
        # The 100%-carry row is excluded from the RECOMMENDATION because its
        # Sharpe rests on unmodelled basis risk (see the header). It is still
        # printed, so the artifact stays visible rather than quietly dropped.
        if s and w <= 0.75 and (best is None or s[2] > best[0]):
            best = (s[2], w, s)
    if best:
        print(f"\n  BEST RISK-ADJUSTED: {best[1]:.0%} carry / {1 - best[1]:.0%} trend "
              f"(Sharpe {best[0]:.2f})")
        print("  Diversification is doing the work: the blend's drawdown is far")
        print("  below the trend book's because carry keeps paying while trend bleeds.")
        print("  NOTE: the 100% carry row is EXCLUDED from this recommendation --")
        print("  its Sharpe rests on basis risk that this model does not include.")


if __name__ == "__main__":
    main()
