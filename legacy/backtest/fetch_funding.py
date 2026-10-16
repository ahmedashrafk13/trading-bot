#!/usr/bin/env python3
"""Download and cache Bybit perp funding-rate history.

    python backtest/fetch_funding.py --days 1500 --symbols BTCUSDT,ETHUSD...

Funding is a crowding measure, not a price derivative: positive funding means
longs are paying shorts, i.e. leveraged longs are crowded. It comes from the
LINEAR (perp) market, not spot, so coverage is limited to symbols that have a
USDT perp — most majors do, many small caps do not. Symbols with no perp are
silently skipped.

Writes data/funding/<SYMBOL>.json as {"symbol", "rates": [[t_sec, rate], ...]}
with t as UTC epoch SECOND (8h cadence), so it lines up with the existing bar
cache format.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data", "funding")
BYBIT = os.path.join(ROOT, "scripts", "bybit.py")
BARS_D = os.path.join(ROOT, "data", "bars", "D")


def by(*args):
    r = subprocess.run([sys.executable, BYBIT] + list(args),
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def fetch_symbol(sym, since_ms):
    """Page BACKWARDS via endTime, same pattern as fetch_bybit.fetch_symbol."""
    rows, seen, end, pages = [], set(), "", 0
    while True:
        args = ["funding", sym, "200"] + ([end] if end else [])
        page = by(*args)
        if page is None:
            return None  # symbol has no perp / API error — skip, don't cache empty
        if not page:
            break
        fresh = False
        for r in page:
            t = int(r["fundingRateTimestamp"])
            if t in seen:
                continue
            seen.add(t)
            fresh = True
            rows.append([t // 1000, float(r["fundingRate"])])
        oldest = min(int(r["fundingRateTimestamp"]) for r in page)
        pages += 1
        if oldest <= since_ms or not fresh or pages >= 60:
            break
        end = str(oldest - 1)
    rows = [r for r in rows if r[0] * 1000 >= since_ms]
    rows.sort(key=lambda r: r[0])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1500)
    ap.add_argument("--symbols", default="", help="comma list; default = cached D bars universe")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    os.makedirs(DEST, exist_ok=True)
    syms = ([s.strip() for s in a.symbols.split(",") if s.strip()]
            or [f[:-5] for f in sorted(os.listdir(BARS_D)) if f.endswith(".json")])
    since_ms = int((dt.datetime.now(dt.timezone.utc)
                    - dt.timedelta(days=a.days)).timestamp() * 1000)
    print(f"fetching funding for {len(syms)} symbols, {a.days}d", file=sys.stderr)

    fetched, skipped = 0, 0
    for i, sym in enumerate(syms, 1):
        path = os.path.join(DEST, sym + ".json")
        if os.path.exists(path) and not a.refresh:
            n = len(json.load(open(path, encoding="utf-8"))["rates"])
            print(f"  [{i}/{len(syms)}] {sym:14} cached ({n})", file=sys.stderr)
            fetched += 1
            continue
        rows = fetch_symbol(sym, since_ms)
        if not rows:
            print(f"  [{i}/{len(syms)}] {sym:14} no perp / no data — skipped", file=sys.stderr)
            skipped += 1
            continue
        json.dump({"symbol": sym, "rates": rows},
                  open(path, "w", encoding="utf-8"), separators=(",", ":"))
        print(f"  [{i}/{len(syms)}] {sym:14} {len(rows)} funding prints", file=sys.stderr)
        fetched += 1

    print(f"done: {fetched} fetched/cached, {skipped} skipped -> {DEST}", file=sys.stderr)


if __name__ == "__main__":
    main()
