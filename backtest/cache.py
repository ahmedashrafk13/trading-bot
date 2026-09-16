#!/usr/bin/env python3
"""Committed bar cache, so a cloud run can backtest immediately.

The per-symbol cache under data/bars/ is gitignored: it is ~40MB of hourly bars
and regenerating it costs ~15 minutes of API calls. A cloud routine cannot spend
its run doing that before it tests anything, so the DAILY bars — which is what
strategy research actually needs, and which covers 5.7 years rather than 400
days — are committed compressed instead.

    python backtest/cache.py pack      # rebuild data/cache/bars-1D.json.gz
    python backtest/cache.py unpack    # expand it into data/bars/1D/

`unpack` is idempotent and safe to run at the start of any routine.
"""
from __future__ import annotations

import glob
import gzip
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Default to the Bybit daily cache. The Alpaca-era 1D cache is kept so old
# results stay reproducible, but it is no longer what routines load.
TF = os.environ.get("CACHE_TF", "D")
CACHE = os.path.join(ROOT, "data", "cache", f"bars-{TF}.json.gz")
DEST = os.path.join(ROOT, "data", "bars", TF)


def pack():
    src = sorted(glob.glob(os.path.join(DEST, "*.json")))
    if not src:
        raise SystemExit(f"nothing to pack in {DEST} — run fetch.py --timeframe 1D first")
    out = {}
    for f in src:
        d = json.load(open(f, encoding="utf-8"))
        # Volume is dropped because no engine here reads it, and prices are
        # rounded to 8 significant decimals: full float repr roughly doubles the
        # file for no analytical difference.
        out[d["symbol"]] = [[r[0]] + [round(x, 8) for x in r[1:5]] for r in d["bars"]]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with gzip.open(CACHE, "wb", compresslevel=9) as fh:
        fh.write(json.dumps(out, separators=(",", ":")).encode())
    n = sum(len(v) for v in out.values())
    print(f"packed {len(out)} symbols, {n:,} bars -> {CACHE} "
          f"({os.path.getsize(CACHE) / 1e6:.2f} MB)")


def unpack(force=False):
    if not os.path.exists(CACHE):
        raise SystemExit(f"no committed cache at {CACHE}")
    os.makedirs(DEST, exist_ok=True)
    existing = glob.glob(os.path.join(DEST, "*.json"))
    if existing and not force:
        print(f"{len(existing)} symbol files already present in {DEST} — nothing to do")
        return
    with gzip.open(CACHE, "rb") as fh:
        data = json.loads(fh.read().decode())
    for sym, bars in data.items():
        # Volume is re-added as 0.0 so the row shape matches what fetch.py
        # writes and Universe unpacks (t, o, h, l, c, v).
        rows = [r + [0.0] for r in bars]
        json.dump({"symbol": sym, "start": "cache", "bars": rows},
                  open(os.path.join(DEST, sym.replace("/", "-") + ".json"), "w",
                       encoding="utf-8"), separators=(",", ":"))
    print(f"unpacked {len(data)} symbols into {DEST}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "unpack"
    if cmd == "pack":
        pack()
    elif cmd == "unpack":
        unpack("--force" in sys.argv)
    else:
        raise SystemExit("usage: python backtest/cache.py [pack|unpack] [--force]")
