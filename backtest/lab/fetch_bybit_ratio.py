#!/usr/bin/env python3
"""Bybit v5 PUBLIC long/short account-ratio history (no keys, no orders).

    python backtest/lab/fetch_bybit_ratio.py [SYMBOLS_JSON]

Live, the bot reads Bybit's /v5/market/account-ratio, but the crowd strategies
were researched on Binance's global account ratio.  This pulls Bybit's own 1h
history so the signal can be re-validated on the population it will trade on.
Writes data/hist/bybit_ratio/<SYM>.npz with ts (epoch s, bar open), buy, sell,
ls (= buy / sell).  Resumable: a symbol whose file exists is skipped.
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HIST = os.path.join(ROOT, "data", "hist")
OUT = os.path.join(HIST, "bybit_ratio")
URL = "https://api.bybit.com/v5/market/account-ratio"
START_MS = 1609459200000          # 2021-01-01, earliest Bybit serves at 1h
STEP_MS = 500 * 3600 * 1000       # 500 rows per request


def get(params, tries=6):
    for k in range(tries):
        try:
            r = requests.get(URL, params=params, timeout=30)
            j = r.json()
            if j.get("retCode") == 0:
                return j["result"]["list"]
            if j.get("retCode") in (10006, 10018):      # rate limited
                time.sleep(5 + 5 * k)
                continue
            return []                                    # unknown symbol etc.
        except Exception:                                # noqa: BLE001 - retry network
            time.sleep(min(2 ** k, 30))
    raise RuntimeError(f"account-ratio failed: {params}")


def fetch(sym):
    dst = os.path.join(OUT, sym + ".npz")
    if os.path.exists(dst):
        return sym, "skip"
    now = int(time.time() * 1000)
    rows = {}
    s = START_MS
    while s < now:
        e = min(s + STEP_MS, now)
        for x in get({"category": "linear", "symbol": sym, "period": "1h",
                      "limit": 500, "startTime": s, "endTime": e}):
            rows[int(x["timestamp"]) // 1000] = (float(x["buyRatio"]), float(x["sellRatio"]))
        s = e
        time.sleep(0.05)
    if not rows:
        return sym, "empty"
    ts = np.array(sorted(rows), np.int64)
    buy = np.array([rows[t][0] for t in ts])
    sell = np.array([rows[t][1] for t in ts])
    with np.errstate(divide="ignore", invalid="ignore"):
        ls = np.where(sell > 0, buy / sell, np.nan)
    tmp = dst + ".part.npz"
    np.savez_compressed(tmp, ts=ts, buy=buy, sell=sell, ls=ls)
    os.replace(tmp, dst)
    return sym, f"{len(ts)} rows {time.strftime('%Y-%m-%d', time.gmtime(ts[0]))}.."


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIST, "metric_symbols_ext.json")
    syms = json.load(open(path))
    os.makedirs(OUT, exist_ok=True)
    with ThreadPoolExecutor(4) as ex:
        for sym, status in ex.map(fetch, syms):
            print(time.strftime("%H:%M:%S"), sym, status, flush=True)


if __name__ == "__main__":
    main()
