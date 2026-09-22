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
    # Universe now resolves <BARS_ROOT>/<timeframe>, so the ROOT is what
    # the harness must redirect; patching the old BARS constant silently
    # did nothing and every test read the real cache instead.
    engine.BARS_ROOT = tmp
    return Universe(timeframe="1H")


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
    orig = engine.BARS_ROOT
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

        # ---------------------------------------------------------------- 4b
        # v3 TACTICAL 72h time stop: a position that never earns +5% must be
        # closed and its slot returned, or the 6-slot sleeve fills and the
        # daily quota becomes unreachable.
        n = 24 * 60
        # rise enough to trigger entry, then go flat well under +5%
        bars = ramp(24 * 35, 100.0, 0.1) + flat(n - 24 * 35, 103.4)
        u = make_universe({"AAA/USD": bars, "BTC/USD": flat(n, 1000.0)}, tmp)
        # The tactical screen has a volatility band that a smooth synthetic
        # ramp cannot pass, so relax the SCREEN here — this test targets the
        # time stop, not entry selection.
        # v4: the limit is 24 HOURS and these synthetic bars are hourly, so the
        # engine must convert it to 24 bars. Pinned explicitly because the old
        # code compared HOURS to a BAR index, which silently made the rule mean
        # 72 DAYS on the daily cache (HYPOTHESIS-LOG #10, "UNTESTABLE").
        p = Params(core_slots=0, tac_slots=6, start_equity=200.0,
                   tac_vol_lo=0.0, tac_vol_hi=9.9, tac_ext_band=9.9)
        eq, trades = run(u, p)
        ts = [t for t in trades if t.reason == "time_stop"]
        check("TACTICAL 24h time stop fires on a flat position",
              bool(ts), f"{len(ts)} time_stop exit(s)")
        check("time stop never fires before 24 hourly bars",
              all(t.bars_held >= 24 for t in ts),
              f"earliest={min((t.bars_held for t in ts), default=None)}")
        # and it must NOT fire on a position that is up >= 5%
        bars_up = ramp(24 * 35, 100.0, 0.1) + ramp(n - 24 * 35, 103.4, 0.05)
        u2 = make_universe({"AAA/USD": bars_up, "BTC/USD": flat(n, 1000.0)}, tmp)
        _eq2, trades2 = run(u2, Params(core_slots=0, tac_slots=6, start_equity=200.0,
                                       tac_vol_lo=0.0, tac_vol_hi=9.9, tac_ext_band=9.9))
        early = [t for t in trades2 if t.reason == "time_stop" and t.ret >= 0.05]
        check("time stop spares a position already >= +5%",
              not early, f"{len(early)} winner(s) cut by the time stop")

        # ---------------------------------------------------------------- 5
        # Deployment ceiling and slot caps must hold at every instant.
        n = 24 * 90
        series = {f"C{i}/USD": ramp(n, 100.0, 0.05) for i in range(8)}
        series["BTC/USD"] = flat(n, 1000.0)
        u = make_universe(series, tmp)
        # LIVE sleeve geometry (v3): CORE 1 slot, TACTICAL 6, deployment 50%.
        p = Params(start_equity=200.0, max_deploy=0.50, core_slots=1, tac_slots=6)
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
        check("CORE slot cap of 1 never exceeded", worst["CORE"] <= 1, f"peak={worst['CORE']}")
        check("TACTICAL slot cap of 6 never exceeded", worst["TACTICAL"] <= 6, f"peak={worst['TACTICAL']}")

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

        # ---------------------------------------------------------------- 8
        # SHORT sleeve (v4, 2026-09-22). A sign error in a short book does not
        # crash — it silently invents profit, which is the single most dangerous
        # bug class in a backtester. Each check below pins one sign.
        n = 24 * 90

        # 8a. Shorts must MAKE money in a falling market...
        u = make_universe({"AAA/USD": ramp(n, 300.0, -0.1), "BTC/USD": flat(n, 1000.0)}, tmp)
        p = Params(start_equity=200.0, core_slots=0, tac_slots=0,
                   short_enabled=True, short_slots=6, regime_filter=False,
                   tac_vol_lo=0.0, tac_vol_hi=9.9, tac_ext_band=9.9,
                   short_funding_bps_8h=0.0)
        eq_s, tr_s = run(u, p)
        shorts = [t for t in tr_s if t.sleeve == "SHORT"]
        check("SHORT sleeve opens positions in a falling market",
              bool(shorts), f"{len(shorts)} short trade(s)")
        check("a short that falls to its target is profitable",
              all(t.pnl > 0 for t in shorts if t.exit < t.entry) if shorts else False,
              f"{[round(t.pnl,3) for t in shorts if t.exit < t.entry][:5]}")
        check("SHORT return is reported in the position's own direction",
              all((t.ret > 0) == (t.exit < t.entry) for t in shorts) if shorts else False,
              "ret must be POSITIVE when a short's exit is below its entry")

        # 8b. ...and must LOSE money in a rising one. The mirror check is what
        # catches a sign flip that 8a alone would pass.
        u2 = make_universe({"AAA/USD": ramp(n, 100.0, 0.1), "BTC/USD": flat(n, 1000.0)}, tmp)
        eq_r, tr_r = run(u2, p)
        rising = [t for t in tr_r if t.sleeve == "SHORT"]
        check("a short cannot profit in a monotonically RISING market",
              all(t.pnl <= 0 for t in rising) if rising else True,
              f"{[round(t.pnl,3) for t in rising][:5]}")

        # 8c. A short's stop sits ABOVE entry and may only ratchet DOWN.
        check("SHORT never exits above its initial stop level",
              all(t.exit <= t.entry * (1 + p.short_trail) * 1.02
                  for t in shorts if t.reason == "trail_stop") if shorts else True,
              "a short stopping out far above entry means the stop widened")

        # 8d. Equity must stay positive with a short book open.
        check("equity never goes negative with shorts enabled",
              bool(np.nanmin(eq_s) > 0), f"min={np.nanmin(eq_s):.2f}")

        # 8e. Shorts are OFF by default, so every pre-v4 result stays reproducible.
        check("short sleeve is opt-in (off by default)",
              Params().short_enabled is False, "Params().short_enabled")

    finally:
        engine.BARS_ROOT = orig
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if FAILS:
        print(f"{len(FAILS)} FAILED: " + ", ".join(FAILS))
        sys.exit(1)
    print("all invariants hold")


if __name__ == "__main__":
    main()
