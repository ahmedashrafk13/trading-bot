"""Download Binance SPOT 1d klines for the carry strategy (strategy family D).

Source: data.binance.vision monthly archives (data/spot/monthly/klines/SYM/1d/),
which keep delisted pairs (used when the pair is no longer listed); listed
pairs come whole from the public REST endpoint api.binance.com/api/v3/klines (public
market data, no key).  Output: data/hist/spot/1d/<PERPSYMBOL>.npz with
t (bar open, s UTC), o, h, l, c, v, qv, plus scalars spot_symbol and scale
(spot price x scale = perp price units, e.g. 1000PEPEUSDT perp <- PEPEUSDT
spot x 1000).  Also saves Bybit public spot instruments-info (public
endpoint) to data/hist/spot/bybit_spot_instruments.json.

Run:  python backtest/lab/strategies/_carry_spot_fetch.py [symbols.json]
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(ROOT, "data", "hist", "spot", "1d")
S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
ARCH = "https://data.binance.vision/"
_S = requests.Session()
_S.headers["User-Agent"] = "trading-bot-research/1.0"


def get(url, params=None, tries=6):
    for k in range(tries):
        try:
            r = _S.get(url, params=params, timeout=60)
            if r.status_code in (400, 404):
                return None
            if r.status_code == 200:
                return r
        except requests.RequestException:
            pass
        time.sleep(1.5 * (k + 1))
    return None


def s3_keys(prefix):
    keys, marker = [], ""
    while True:
        r = get(S3, {"prefix": prefix, "marker": marker})
        if r is None:
            return keys
        ks = re.findall(r"<Key>([^<]+)</Key>", r.text)
        keys += ks
        if "<IsTruncated>true</IsTruncated>" not in r.text or not ks:
            return keys
        marker = ks[-1]


def spot_candidates(perp):
    base = perp[:-4]
    out = [(perp, 1.0)]
    for pre, sc in (("1000000", 1e6), ("1000", 1e3), ("1M", 1e6)):
        if base.startswith(pre) and len(base) > len(pre):
            out.append((base[len(pre):] + "USDT", sc))
    if perp == "LUNA2USDT":
        out.insert(0, ("LUNAUSDT", 1.0))
    return out


def parse(rows):
    a = np.array(rows, dtype=float)
    ts = a[:, 0]
    ts = np.where(ts > 1e14, ts / 1e6, ts / 1e3)      # 2025+ archives use microseconds
    return ts.astype(np.int64), a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5], a[:, 7]


def fetch_one(perp):
    path = os.path.join(OUT, perp + ".npz")
    if os.path.exists(path):
        return perp, "cached"
    for spot, scale in spot_candidates(perp):
        rows, start = [], 0            # 1) REST (listed pairs): full history, 1000 bars/call
        while True:
            r = get("https://api.binance.com/api/v3/klines",
                    {"symbol": spot, "interval": "1d", "startTime": start, "limit": 1000})
            lst = r.json() if r is not None else None
            if not isinstance(lst, list) or not lst:
                break
            rows += [[float(x) for x in q[:11]] for q in lst]
            if len(lst) < 1000:
                break
            start = int(lst[-1][0]) + 86400000
        if rows:
            t, o, h, l, c, v, qv = parse(rows)
            u, idx = np.unique(t, return_index=True)
            np.savez(path, t=u, o=o[idx], h=h[idx], l=l[idx], c=c[idx], v=v[idx], qv=qv[idx],
                     spot_symbol=spot, scale=scale)
            return perp, f"{spot} x{scale:g} {len(u)} bars from {time.strftime('%Y-%m-%d', time.gmtime(u[0]))} (rest)"
        keys = [k for k in s3_keys(f"data/spot/monthly/klines/{spot}/1d/") if k.endswith(".zip")]
        if not keys:
            continue
        rows = []
        for k in sorted(keys):
            r = get(ARCH + k)
            if r is None:
                continue
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                txt = z.read(z.namelist()[0]).decode()
            for line in txt.splitlines():
                p = line.split(",")
                if p and p[0][:1].isdigit():
                    rows.append([float(x) for x in p[:11]])
        if not rows:
            continue
        last_ms = max(r[0] if r[0] < 1e14 else r[0] / 1e3 for r in rows)
        # tail from REST (only for pairs still listed)
        start = int(last_ms) + 86400000
        while True:
            r = get("https://api.binance.com/api/v3/klines",
                    {"symbol": spot, "interval": "1d", "startTime": start, "limit": 1000})
            if r is None:
                break
            lst = r.json()
            if not isinstance(lst, list) or not lst:
                break
            rows += [[float(x) for x in q[:11]] for q in lst]
            if len(lst) < 1000:
                break
            start = int(lst[-1][0]) + 86400000
        t, o, h, l, c, v, qv = parse(rows)
        u, idx = np.unique(t, return_index=True)
        np.savez(path, t=u, o=o[idx], h=h[idx], l=l[idx], c=c[idx], v=v[idx], qv=qv[idx],
                 spot_symbol=spot, scale=scale)
        return perp, f"{spot} x{scale:g} {len(u)} bars from {time.strftime('%Y-%m-%d', time.gmtime(u[0]))}"
    np.savez(path, t=np.zeros(0, np.int64), o=np.zeros(0), h=np.zeros(0), l=np.zeros(0),
             c=np.zeros(0), v=np.zeros(0), qv=np.zeros(0), spot_symbol="", scale=1.0)
    return perp, "NO SPOT"


def bybit_spot_instruments():
    p = os.path.join(os.path.dirname(OUT), "bybit_spot_instruments.json")
    out, cursor = {}, ""
    while True:
        r = get("https://api.bybit.com/v5/market/instruments-info",
                {"category": "spot", "limit": 1000, "cursor": cursor})
        if r is None:
            break
        d = r.json().get("result") or {}
        for x in d.get("list") or []:
            lot = x.get("lotSizeFilter") or {}
            out[x["symbol"]] = {"status": x.get("status"),
                                "basePrecision": float(lot.get("basePrecision") or 0),
                                "minOrderQty": float(lot.get("minOrderQty") or 0),
                                "minOrderAmt": float(lot.get("minOrderAmt") or 0),
                                "marginTrading": x.get("marginTrading")}
        cursor = d.get("nextPageCursor") or ""
        if not cursor:
            break
    json.dump({"fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "instruments": out}, open(p, "w"))
    return len(out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    syms = json.load(open(sys.argv[1]))
    with ThreadPoolExecutor(6) as ex:
        for s, msg in ex.map(fetch_one, syms):
            print(s, msg, flush=True)
    print("bybit spot instruments:", bybit_spot_instruments())
