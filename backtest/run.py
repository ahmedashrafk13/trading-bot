#!/usr/bin/env python3
"""Run one backtest of the v2 rulebook and print a report.

Usage:
    python backtest/run.py
    python backtest/run.py --days 180
    python backtest/run.py --set tac_trail=0.20 --set core_risk=0.03
    python backtest/run.py --trades            # list every closed trade
    python backtest/run.py --json out.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import asdict, fields, replace

import numpy as np

from engine import Params, Universe, run, metrics


def coerce(name, raw):
    # dataclass field types arrive as strings under `from __future__ import
    # annotations`, so match on both the type object and its name.
    t = {f.name: f.type for f in fields(Params)}[name]
    if t is str or t == "str":
        return raw
    if t is bool or t == "bool":
        return raw.lower() in ("1", "true", "yes")
    if t is int or t == "int":
        return int(raw)
    return float(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=0, help="only backtest the last N days")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VAL")
    ap.add_argument("--trades", action="store_true")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    valid = {f.name for f in fields(Params)}
    ov = {}
    for s in a.set:
        k, _, v = s.partition("=")
        if k not in valid:
            raise SystemExit(f"unknown parameter '{k}'. valid: {', '.join(sorted(valid))}")
        ov[k] = coerce(k, v)
    p = replace(Params(), **ov)

    start = None
    if a.days:
        start = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)).timestamp())
    u = Universe(start=start)
    eq, trades = run(u, p)
    m = metrics(u, eq, trades)

    t0 = dt.datetime.fromtimestamp(int(u.t[0]), dt.timezone.utc).date()
    t1 = dt.datetime.fromtimestamp(int(u.t[-1]), dt.timezone.utc).date()
    print(f"\nBACKTEST  {t0} -> {t1}   ({m['years'] * 12:.1f} months, "
          f"{len(u.symbols)} symbols, {len(u.t)} hourly bars)")
    if ov:
        print("overrides: " + json.dumps(ov))
    print("=" * 68)
    print(f"  equity        ${m['start_equity']:.2f} -> ${m['end_equity']:.2f}"
          f"   ({m['total_return']:+.2%})")
    if m["btc_buyhold"] is not None:
        print(f"  BTC buy/hold  {m['btc_buyhold']:+.2%}"
              f"          EDGE {m['edge_vs_btc']:+.2%}")
    print(f"  CAGR          {m['cagr']:+.2%}")
    print(f"  max drawdown  {m['max_drawdown']:+.2%}")
    print(f"  Sharpe        {m['sharpe']:+.2f}        Sortino {m['sortino']:+.2f}")
    print("-" * 68)
    print(f"  trades        {m['trades']}  ({m['wins']}W / {m['losses']}L, "
          f"win rate {m['win_rate']:.1%})")
    print(f"  profit factor {m['profit_factor']:.2f}")
    print(f"  expectancy    ${m['expectancy']:+.3f} per trade")
    print(f"  avg win       ${m['avg_win']:+.2f}     avg loss ${m['avg_loss']:+.2f}")
    print(f"  avg hold      {m['avg_bars_held']:.0f} hours ({m['avg_bars_held'] / 24:.1f} days)")

    for sleeve in ("CORE", "TACTICAL"):
        st = [t for t in trades if t.sleeve == sleeve]
        if st:
            w = [t for t in st if t.pnl > 0]
            print(f"  {sleeve:9} {len(st):3d} trades, {len(w)}W/{len(st) - len(w)}L "
                  f"({len(w) / len(st):.0%}), net ${sum(t.pnl for t in st):+.2f}")

    reasons = {}
    for t in trades:
        reasons[t.reason] = reasons.get(t.reason, 0) + 1
    print("  exits:        " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items())))

    if a.trades:
        print("\n" + "-" * 68)
        print(f"{'sleeve':9}{'symbol':10}{'entry':>11}{'exit':>11}{'ret':>8}{'pnl':>8}  reason")
        for t in sorted(trades, key=lambda x: x.entry_t):
            d = dt.datetime.fromtimestamp(t.entry_t, dt.timezone.utc).strftime("%m-%d %H:%M")
            print(f"{t.sleeve:9}{t.symbol.replace('/USD', ''):10}{t.entry:>11.4f}"
                  f"{t.exit:>11.4f}{t.ret:>+8.1%}{t.pnl:>+8.2f}  {t.reason}  ({d})")

    if a.json:
        json.dump({"params": asdict(p), "metrics": m,
                   "trades": [asdict(t) for t in trades]},
                  open(a.json, "w", encoding="utf-8"), indent=2, default=str)
        print(f"\nwritten -> {a.json}")
    print()


if __name__ == "__main__":
    main()
