#!/usr/bin/env python3
"""Download and cache historical crypto bars from Alpaca.

Fetches HOURLY bars only; daily bars are resampled from them by the engine, so
there is exactly one source of truth and no cross-timeframe alignment bug.

Usage:
    python backtest/fetch.py --days 400
    python backtest/fetch.py --days 400 --symbols BTC/USD,ETH/USD
    python backtest/fetch.py --days 400 --refresh      # ignore cache

Writes data/bars/1H/<SYM>.json as {"symbol":..., "bars":[[t,o,h,l,c,v], ...]}
with t as a UTC epoch second. Compact on purpose: 400 days x 33 coins of hourly
bars is ~317k rows and the verbose Alpaca shape would be ~40MB of duplicated
keys.
"""
import argparse, datetime as dt, json, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BARS = os.path.join(ROOT, "data", "bars", "1H")
STABLES = {"USDC", "USDT", "USDG", "DAI", "PYUSD"}


def _bash_env():
    """Locate bash, and hand it a PATH that can actually find curl.

    On Windows, CPython is a native process whose PATH usually lacks Git's unix
    tool directories. bash itself resolves, but the curl inside alpaca.sh does
    not, and the script dies with a bare exit 127 that looks like a missing
    interpreter. Prepending Git's bin dirs fixes it for the child only.
    """
    exe = shutil.which("bash") or r"C:\Program Files\Git\usr\bin\bash.exe"
    env = os.environ.copy()
    if os.name == "nt":
        gitroot = os.path.dirname(os.path.dirname(os.path.dirname(exe)))
        extra = [os.path.join(gitroot, "mingw64", "bin"), os.path.join(gitroot, "usr", "bin")]
        env["PATH"] = os.pathsep.join([d for d in extra if os.path.isdir(d)] + [env.get("PATH", "")])
    return exe, env


BASH, BASH_ENV = _bash_env()


def sh(*args):
    """Call scripts/alpaca.sh and parse its JSON. Retries on transient failure."""
    cmd = [BASH, os.path.join(ROOT, "scripts", "alpaca.sh")] + list(args)
    last = None
    for attempt in range(4):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=True,
                                 env=BASH_ENV).stdout
            return json.loads(out)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            last = e
            detail = getattr(e, "stderr", "") or getattr(e, "stdout", "")
            # 429 / 5xx are worth backing off on; a 401 never gets better.
            if "401" in str(detail) or "403" in str(detail):
                break
            time.sleep(2 ** attempt)
    raise SystemExit(f"alpaca.sh {' '.join(args)} failed: {last}")


def universe():
    assets = sh("assets", "crypto")
    return sorted(
        a["symbol"] for a in assets
        if a.get("tradable")
        and a["symbol"].endswith("/USD")
        and a["symbol"].split("/")[0] not in STABLES
    )


def parse_ts(s):
    # Alpaca returns RFC3339 with a trailing Z, which fromisoformat rejects
    # before 3.11. Normalising is cheaper than depending on the interpreter.
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def fetch_symbol(sym, start):
    """Fetch one symbol, following pagination to exhaustion.

    Fetching ONE symbol per request sidesteps the crypto-bars trap where `limit`
    is a total across all requested symbols: a multi-symbol page fills symbols in
    order, so later ones come back short and a caller that ignores the token
    silently backtests an incomplete universe.
    """
    rows, page, pages = [], "", 0
    while True:
        d = sh("crypto-bars", sym, "1H", start, "10000", page)
        for b in d.get("bars", {}).get(sym, []):
            rows.append([parse_ts(b["t"]), b["o"], b["h"], b["l"], b["c"], b.get("v", 0.0)])
        page = d.get("next_page_token") or ""
        pages += 1
        if not page:
            break
        if pages >= 500:
            raise SystemExit(f"{sym}: pagination exceeded 500 pages — refusing to truncate silently")
    rows.sort(key=lambda r: r[0])
    # Alpaca can repeat the boundary bar across pages; dedupe on timestamp.
    dedup, seen = [], set()
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0])
            dedup.append(r)
    return dedup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=400)
    ap.add_argument("--symbols", default="")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    os.makedirs(BARS, exist_ok=True)
    syms = [s.strip() for s in a.symbols.split(",") if s.strip()] or universe()
    start = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)).strftime("%Y-%m-%d")
    print(f"fetching {len(syms)} symbols, 1H bars from {start}", file=sys.stderr)

    for i, sym in enumerate(syms, 1):
        path = os.path.join(BARS, sym.replace("/", "-") + ".json")
        if os.path.exists(path) and not a.refresh:
            n = len(json.load(open(path, encoding="utf-8"))["bars"])
            print(f"  [{i}/{len(syms)}] {sym:12} cached ({n} bars)", file=sys.stderr)
            continue
        bars = fetch_symbol(sym, start)
        json.dump({"symbol": sym, "start": start, "bars": bars},
                  open(path, "w", encoding="utf-8"), separators=(",", ":"))
        print(f"  [{i}/{len(syms)}] {sym:12} {len(bars)} bars", file=sys.stderr)

    print("done -> " + BARS, file=sys.stderr)


if __name__ == "__main__":
    main()
