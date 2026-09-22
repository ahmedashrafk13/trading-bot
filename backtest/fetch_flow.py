#!/usr/bin/env python3
"""Fetch NON-PRICE data: open interest and the long/short account ratio.

WHY (2026-09-23)
----------------
Every signal tested so far is derived from OHLCV, which is the cheapest and most
picked-over data in existence. Momentum on it scores exactly at the random null.
The one time a genuinely new column was read (volume, 2026-09-22) it immediately
produced the best signal in the file. So the pattern is: new DIMENSIONS pay, new
formulas on price do not.

These two are the next real dimensions available without a paid feed:

  OPEN INTEREST - how many contracts are actually open. Price up with OI up is
  new money entering; price up with OI DOWN is shorts covering, which exhausts.
  A price series cannot distinguish those two, and they resolve differently.

  LONG/SHORT ACCOUNT RATIO - what share of accounts are positioned long. This is
  crowding. It is the closest free proxy for "everyone is on one side", which is
  the setup that liquidation cascades resolve violently.

HISTORY DEPTH: cursor paging stops after ~1200 rows (50 days), which is NOT the
API's limit -- it is the cursor's. Passing explicit startTime/endTime windows
walks all the way back to ~400 days, which fully covers the committed hourly
cache. This fetcher therefore steps backwards in fixed windows instead of
following nextPageCursor.

Usage:
    python backtest/fetch_flow.py            # every symbol in the 1H cache
    python backtest/fetch_flow.py BTCUSDT    # one symbol
"""
import json
import os
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BARS = ROOT / "data" / "bars" / "1H"
OUT = ROOT / "data" / "flow"
BASE = "https://api.bybit.com"


def get(path, params):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    for attempt in range(4):
        try:
            with urllib.request.urlopen(f"{BASE}{path}?{qs}", timeout=20) as r:
                d = json.loads(r.read())
            if d.get("retCode") == 0:
                return d["result"]
            # 10001 on a symbol with no perp listing is expected, not an error
            return None
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return None


def window(path, params, span_hours, days_back=400):
    """Walk explicit startTime/endTime windows backwards.

    Bybit caps a single response, so the window is sized to stay under that cap
    rather than relying on nextPageCursor, which quietly stops at ~50 days.
    """
    now = int(time.time())
    rows, seen = [], set()
    end = now
    floor = now - days_back * 86400
    while end > floor:
        start = max(floor, end - span_hours * 3600)
        p = dict(params)
        p["startTime"] = start * 1000
        p["endTime"] = end * 1000
        res = get(path, p)
        if res:
            for x in (res.get("list") or []):
                ts = int(x["timestamp"]) // 1000
                if ts not in seen:
                    seen.add(ts)
                    rows.append(x)
        end = start
        time.sleep(0.10)
    return rows


def symbols():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    out = []
    for f in sorted(BARS.glob("*.json")):
        coin = f.stem.replace("-USD", "")
        out.append(f"{coin}USDT")
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    syms = symbols()
    print(f"fetching open interest + long/short ratio for {len(syms)} symbols")
    ok = skipped = 0
    for i, sym in enumerate(syms, 1):
        dest = OUT / f"{sym}.json"
        # 190h per window keeps each response under the 200-row cap.
        oi = window("/v5/market/open-interest",
                    {"category": "linear", "symbol": sym,
                     "intervalTime": "1h", "limit": 200}, span_hours=190)
        ratio = window("/v5/market/account-ratio",
                       {"category": "linear", "symbol": sym,
                        "period": "1h", "limit": 500}, span_hours=480)
        if not oi and not ratio:
            skipped += 1
            print(f"  [{i}/{len(syms)}] {sym:14} no perp data, skipped")
            continue
        rec = {
            "symbol": sym,
            "open_interest": [
                {"t": int(x["timestamp"]) // 1000, "oi": float(x["openInterest"])}
                for x in oi if x.get("openInterest")
            ],
            "long_ratio": [
                {"t": int(x["timestamp"]) // 1000, "buy": float(x["buyRatio"])}
                for x in ratio if x.get("buyRatio")
            ],
        }
        rec["open_interest"].sort(key=lambda r: r["t"])
        rec["long_ratio"].sort(key=lambda r: r["t"])
        dest.write_text(json.dumps(rec), encoding="utf-8")
        ok += 1
        print(f"  [{i}/{len(syms)}] {sym:14} OI {len(rec['open_interest']):5}  "
              f"ratio {len(rec['long_ratio']):5}")
    print(f"\nwrote {ok} file(s) to {OUT}, skipped {skipped}")


if __name__ == "__main__":
    main()
