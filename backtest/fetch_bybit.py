#!/usr/bin/env python3
"""Download and cache historical Bybit spot bars.

    python backtest/fetch_bybit.py --timeframe D --days 1500
    python backtest/fetch_bybit.py --timeframe 60 --days 400 --top 80
    python backtest/fetch_bybit.py --timeframe D --days 1500 --refresh

Bybit lists ~394 tradable USDT spot pairs against Alpaca's 33. That is not
automatically an improvement: the median altcoin in the old 33-coin universe
returned -21.2% over 5.7 years while BTC returned +157.4%, and a wider list is
mostly wider at the junk end. So this fetcher ranks by 24h turnover and takes
the top N by default. Liquidity is also what makes a spread assumption
survivable - a signal that only fires on a coin with a 3% spread is not
tradable at any size.

Writes data/bars/<tf>/<SYMBOL>.json as {"symbol", "bars": [[t,o,h,l,c,v], ...]}
with t as a UTC epoch SECOND, matching the Alpaca-era cache format so the
backtest engines need no changes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BARS_ROOT = os.path.join(ROOT, "data", "bars")
BYBIT = os.path.join(ROOT, "scripts", "bybit.py")

STABLES = {"USDC", "USDT", "USDE", "FDUSD", "DAI", "TUSD", "BUSD", "USDD",
           "PYUSD", "EURT", "USDR"}

# Bybit interval -> seconds per bar. Letters are calendar periods.
STEP = {"1": 60, "3": 180, "5": 300, "15": 900, "30": 1800, "60": 3600,
        "120": 7200, "240": 14400, "360": 21600, "720": 43200,
        "D": 86400, "W": 604800}


def by(*args):
    r = subprocess.run([sys.executable, BYBIT] + list(args),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"bybit.py {' '.join(args)} failed:\n{r.stderr.strip()}")
    return json.loads(r.stdout)


def universe(top):
    """Tradable non-stablecoin USDT spot pairs, ranked by 24h turnover."""
    inst = by("instruments", "spot")
    ok = {x["symbol"] for x in inst
          if x.get("quoteCoin") == "USDT" and x.get("status") == "Trading"
          and x.get("baseCoin") not in STABLES}
    tick = by("tickers", "spot")
    rows = []
    for t in tick:
        if t.get("symbol") in ok:
            try:
                rows.append((float(t.get("turnover24h") or 0), t["symbol"]))
            except ValueError:
                continue
    rows.sort(reverse=True)
    picked = [s for _v, s in rows[:top]] if top else [s for _v, s in rows]
    if rows:
        cutoff = rows[min(top, len(rows)) - 1][0] if top else rows[-1][0]
        print(f"universe: {len(picked)} of {len(rows)} USDT spot pairs, "
              f"24h turnover cutoff ${cutoff:,.0f}", file=sys.stderr)
    return picked


def fetch_symbol(sym, tf, since_ms):
    """Page BACKWARDS to since_ms.

    Bybit returns newest-first and caps a page at 1000 bars, so history is
    walked by moving `end` earlier each call. A forward walk is not possible.
    """
    step_ms = STEP[tf] * 1000
    end, rows, seen, pages = "", [], set(), 0
    while True:
        args = ["kline", sym, tf, "1000", "spot"] + ([end] if end else [])
        page = by(*args)
        if not page:
            break
        fresh = False
        for r in page:
            t = int(r[0])
            if t in seen:
                continue
            seen.add(t)
            fresh = True
            rows.append([t // 1000, float(r[1]), float(r[2]), float(r[3]),
                         float(r[4]), float(r[5])])
        oldest = min(int(r[0]) for r in page)
        pages += 1
        # Stop when the page is entirely older than we need, brought nothing
        # new (Bybit clamps `end` at the listing date), or the coin is new.
        if oldest <= since_ms or not fresh or pages >= 400:
            break
        end = str(oldest - step_ms)
    rows = [r for r in rows if r[0] * 1000 >= since_ms]
    rows.sort(key=lambda r: r[0])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeframe", default="D", help="D, 60, 240, 15 ...")
    ap.add_argument("--days", type=int, default=1500)
    ap.add_argument("--top", type=int, default=60,
                    help="keep the N most liquid pairs; 0 = all")
    ap.add_argument("--symbols", default="")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    if a.timeframe not in STEP:
        raise SystemExit(f"unknown timeframe {a.timeframe}; use one of {', '.join(STEP)}")

    dest = os.path.join(BARS_ROOT, a.timeframe)
    os.makedirs(dest, exist_ok=True)
    syms = ([s.strip() for s in a.symbols.split(",") if s.strip()]
            or universe(a.top))
    since_ms = int((dt.datetime.now(dt.timezone.utc)
                    - dt.timedelta(days=a.days)).timestamp() * 1000)
    print(f"fetching {len(syms)} symbols, {a.timeframe} bars, {a.days}d",
          file=sys.stderr)

    for i, sym in enumerate(syms, 1):
        path = os.path.join(dest, sym + ".json")
        if os.path.exists(path) and not a.refresh:
            n = len(json.load(open(path, encoding="utf-8"))["bars"])
            print(f"  [{i}/{len(syms)}] {sym:14} cached ({n})", file=sys.stderr)
            continue
        bars = fetch_symbol(sym, a.timeframe, since_ms)
        if len(bars) < 30:
            print(f"  [{i}/{len(syms)}] {sym:14} only {len(bars)} bars — skipped",
                  file=sys.stderr)
            continue
        json.dump({"symbol": sym, "bars": bars},
                  open(path, "w", encoding="utf-8"), separators=(",", ":"))
        print(f"  [{i}/{len(syms)}] {sym:14} {len(bars)} bars", file=sys.stderr)

    print(f"done -> {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
