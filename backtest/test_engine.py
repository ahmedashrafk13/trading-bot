#!/usr/bin/env python3
"""Invariant tests for the backtest engine, on synthetic bars with known answers.

These exist because the failure mode of a backtester is not a crash - it is a
plausible-looking number that is wrong in the optimistic direction. Each test
pins one specific way this engine could silently cheat.

Run: python backtest/test_engine.py
"""
from __future__ import annotations

import os
import sys
import tempfile
import json
import shutil

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from engine import Params, Universe, run

HOUR = 3600
T0 = 1735689600   # 2025-01-01T00:00:00Z, a UTC midnight so day maths is clean

FAILS = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def make_universe(series, tmp):
    """series: {symbol: [(o,h,l,c), ...]} starting at T0, hourly.

    The directory is wiped first. Without that, symbols from an earlier test
    linger on disk and silently join the next test's universe — which is exactly
    how a 'falling market' scenario ended up holding leftover rising coins and
    reporting a profit.
    """
    d = os.path.join(tmp, "1H")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    for sym, bars in series.items():
        rows = [[T0 + i * HOUR, o, h, l, c, 1.0] for i, (o, h, l, c) in enumerate(bars)]
        json.dump({"symbol": sym, "start": "x", "bars": rows},
                  open(os.path.join(d, sym.replace("/", "-") + ".json"), "w"), separators=(",", ":"))
    engine.BARS = d
    return Universe()


def flat(n, px):
    return [(px, px, px, px)] * n


def ramp(n, start, step):
    out = []
    for i in range(n):
        px = start + step * i
        out.append((px, px * 1.001, px * 0.999, px))
    return out


def main():
    tmp = tempfile.mkdtemp()
    orig = engine.BARS
    try:
        # ---------------------------------------------------------------- 1
        # A position must never exit better than its stop. With a hard gap down,
        # the fill has to be the OPEN, not the stop price.
        n = 24 * 60
        bars = ramp(n, 100.0, 0.5)
        gap_i = n - 50
        # one bar that opens far below the trailing stop
        for i in range(gap_i, n):
            px = 10.0
            bars[i] = (px, px, px, px)
        u = make_universe({"AAA/USD": bars, "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(core_slots=1, tac_slots=0, core_trail=0.15, start_equity=200.0)
        _, trades = run(u, p)
        gapped = [t for t in trades if t.symbol == "AAA/USD"]
        check("gap through stop fills at the open, not the stop price",
              bool(gapped) and gapped[0].exit <= 10.0 + 1e-9,
              f"exit={gapped[0].exit if gapped else None}")

        # ---------------------------------------------------------------- 2
        # A trailing stop must never move down. The rise has to START after the
        # 31-day warmup, or no entry is ever originated and the test proves
        # nothing.
        pre = 24 * 40
        bars = flat(pre, 100.0) + ramp(24 * 30, 100.0, 0.3) + ramp(24 * 20, 316.0, -0.6)
        n = len(bars)
        u = make_universe({"AAA/USD": bars, "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(core_slots=1, tac_slots=0, start_equity=200.0)
        _, trades = run(u, p)
        t = [x for x in trades if x.symbol == "AAA/USD"]
        # entry was near 100 on a rising ramp to 300; a 15% trail from a ~300 HWM
        # must exit well ABOVE the entry, i.e. the ratchet actually happened.
        check("trail ratchets up and locks in a winner",
              bool(t) and t[0].exit > t[0].entry * 1.5,
              f"entry={t[0].entry if t else None} exit={t[0].exit if t else None}")

        # ---------------------------------------------------------------- 3
        # No lookahead: a single one-bar spike that is fully reversed by the next
        # open must not be capturable. If the engine could see the future it
        # would buy the bar before the spike and sell into it.
        n = 24 * 60
        bars = flat(n, 100.0)
        spike = n - 30
        bars[spike] = (100.0, 500.0, 100.0, 100.0)
        u = make_universe({"AAA/USD": bars, "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(core_slots=1, tac_slots=1, start_equity=200.0)
        eq, trades = run(u, p)
        gain = [t for t in trades if t.symbol == "AAA/USD" and t.ret > 0.5]
        check("cannot capture a fully-reversed one-bar spike (no lookahead)",
              not gain, f"{len(gain)} impossible winner(s)")

        # ---------------------------------------------------------------- 4
        # Fees must make a round trip at an unchanged price a LOSS.
        n = 24 * 60
        bars = ramp(24 * 35, 100.0, 0.1) + flat(n - 24 * 35, 103.4)
        u = make_universe({"AAA/USD": bars, "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(core_slots=1, tac_slots=0, start_equity=200.0, fee_bps=35, spread_bps=10)
        eq, trades = run(u, p)
        rt = [t for t in trades if abs(t.exit / t.entry - 1) < 0.005]
        check("a flat round trip loses money to fees",
              all(t.pnl < 0 for t in rt) if rt else True,
              f"{[round(t.pnl, 4) for t in rt]}")

        # ---------------------------------------------------------------- 5
        # Deployment ceiling and slot caps must hold at every instant.
        n = 24 * 90
        series = {f"C{i}/USD": ramp(n, 100.0, 0.05) for i in range(8)}
        series["BTC/USD"] = flat(n, 1000.0)
        u = make_universe(series, tmp)
        p = Params(start_equity=200.0, max_deploy=0.85, core_slots=4, tac_slots=1)
        eq, trades = run(u, p)
        # reconstruct concurrent holdings from the trade list
        events = []
        for t in trades:
            events.append((t.entry_t, 1, t.sleeve))
            events.append((t.exit_t, -1, t.sleeve))
        events.sort()
        cur = {"CORE": 0, "TACTICAL": 0}
        worst = {"CORE": 0, "TACTICAL": 0}
        for _ts, d, s in events:
            cur[s] += d
            worst[s] = max(worst[s], cur[s])
        check("CORE slot cap of 4 never exceeded", worst["CORE"] <= 4, f"peak={worst['CORE']}")
        check("TACTICAL slot cap of 1 never exceeded", worst["TACTICAL"] <= 1, f"peak={worst['TACTICAL']}")

        # ---------------------------------------------------------------- 6
        # Equity must never go negative and cash must never be lent.
        check("equity never goes negative", bool(np.nanmin(eq) > 0), f"min={np.nanmin(eq):.2f}")

        # ---------------------------------------------------------------- 7
        # A universe that only falls must never produce a profit.
        n = 24 * 90
        u = make_universe({"AAA/USD": ramp(n, 300.0, -0.1), "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(start_equity=200.0)
        eq, trades = run(u, p)
        check("a monotonically falling market cannot be profitable",
              eq[~np.isnan(eq)][-1] <= 200.0 + 1e-6,
              f"end={eq[~np.isnan(eq)][-1]:.2f}")

    finally:
        engine.BARS = orig
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if FAILS:
        print(f"{len(FAILS)} FAILED: " + ", ".join(FAILS))
        sys.exit(1)
    print("all invariants hold")


if __name__ == "__main__":
    main()
