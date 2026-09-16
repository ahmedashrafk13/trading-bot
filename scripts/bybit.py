#!/usr/bin/env python3
"""Bybit v5 API wrapper. All trading calls go through here.

    python scripts/bybit.py <subcommand> [args...]

This is the ONLY way the bot speaks to the exchange.

WHY BYBIT
  * Bybit accepts a take-profit AND a stop-loss attached to the same position,
    so a position can carry both legs at once. The previous venue allowed only
    ONE resting order per symbol, which is what the hourly `scan` routine
    existed to police. That whole class of order-thrash bug is gone by
    construction.
  * Fees are ~0.055% taker against the paper-era ~0.35%, roughly a 6x reduction
    in the drag that made the old tactical geometry negative-expectancy.
  * Far more symbols, and spot as well as perpetuals.

SAFETY
  Reads credentials from .env (gitignored) or the environment. Never hard-code a
  key here. `category` defaults to `spot`: perpetuals allow losing more than the
  account holds, and nothing in this repo's risk machinery assumes that is
  possible, so linear/perp access is opt-in per call rather than default.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECV_WINDOW = "10000"
PLACEHOLDER_PREFIX = "your_"


def load_env():
    """Load .env without overriding anything already in the environment.

    env.template ships `your_..._here` placeholders which are NON-EMPTY, so a
    naive truthiness check would pass them to the API and produce a signature
    error instead of a clear message. They are normalized to absent.
    """
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v
    for k in ("BYBIT_API_KEY", "BYBIT_API_SECRET"):
        if os.environ.get(k, "").startswith(PLACEHOLDER_PREFIX):
            os.environ.pop(k, None)


load_env()
BASE = os.environ.get("BYBIT_ENDPOINT", "https://api.bybit.com")
KEY = os.environ.get("BYBIT_API_KEY", "")
SECRET = os.environ.get("BYBIT_API_SECRET", "")


def _need_keys():
    if not KEY or not SECRET:
        die("BYBIT_API_KEY / BYBIT_API_SECRET are not set. Copy env.template to "
            ".env and fill them in, or export them. Never commit them.")


def die(msg, code=1):
    print(f"BYBIT ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _sign(ts, payload):
    return hmac.new(SECRET.encode(),
                    f"{ts}{KEY}{RECV_WINDOW}{payload}".encode(),
                    hashlib.sha256).hexdigest()


def request(method, path, params=None, private=False, retries=3):
    params = params or {}
    for attempt in range(retries):
        ts = str(int(time.time() * 1000))
        if method == "GET":
            qs = urllib.parse.urlencode(params)
            url = f"{BASE}{path}" + (f"?{qs}" if qs else "")
            body, payload = None, qs
        else:
            # Bybit signs the EXACT body bytes sent, so the string built here is
            # the string that must be transmitted — re-serializing later would
            # invalidate the signature.
            payload = json.dumps(params, separators=(",", ":"))
            url, body = f"{BASE}{path}", payload.encode()

        headers = {"Content-Type": "application/json"}
        if private:
            _need_keys()
            headers.update({
                "X-BAPI-API-KEY": KEY,
                "X-BAPI-TIMESTAMP": ts,
                "X-BAPI-RECV-WINDOW": RECV_WINDOW,
                "X-BAPI-SIGN": _sign(ts, payload),
            })
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read().decode())
        except Exception as e:
            if attempt == retries - 1:
                die(f"{method} {path} failed: {e}")
            time.sleep(2 ** attempt)
            continue

        # Bybit returns HTTP 200 with retCode != 0 for logical failures, so the
        # HTTP status alone never tells you whether an order was placed.
        if out.get("retCode") not in (0, None):
            msg = f"{method} {path} -> retCode {out.get('retCode')}: {out.get('retMsg')}"
            # 10002 = timestamp out of sync; retrying with a fresh one may work.
            if out.get("retCode") == 10002 and attempt < retries - 1:
                time.sleep(1)
                continue
            die(msg)
        return out
    return {}


def out(obj):
    print(json.dumps(obj, indent=2))


# ------------------------------------------------------------------ commands
def cmd_balance(args):
    """Unified account balance. The number routines should treat as equity."""
    r = request("GET", "/v5/account/wallet-balance",
                {"accountType": "UNIFIED"}, private=True)
    out(r.get("result", {}))


def cmd_positions(args):
    cat = args[0] if args else "spot"
    r = request("GET", "/v5/position/list",
                {"category": cat, "settleCoin": "USDT"}, private=True)
    out(r.get("result", {}).get("list", []))


def cmd_holdings(args):
    """Spot holdings with a non-zero balance — the spot analogue of positions."""
    r = request("GET", "/v5/account/wallet-balance",
                {"accountType": "UNIFIED"}, private=True)
    rows = []
    for acct in r.get("result", {}).get("list", []):
        for c in acct.get("coin", []):
            try:
                if float(c.get("walletBalance") or 0) > 0:
                    rows.append(c)
            except ValueError:
                continue
    out(rows)


def cmd_tickers(args):
    cat = args[0] if args else "spot"
    sym = args[1] if len(args) > 1 else None
    p = {"category": cat}
    if sym:
        p["symbol"] = sym
    r = request("GET", "/v5/market/tickers", p)
    out(r.get("result", {}).get("list", []))


def cmd_instruments(args):
    cat = args[0] if args else "spot"
    rows, cursor = [], ""
    while True:
        p = {"category": cat, "limit": 1000}
        if cursor:
            p["cursor"] = cursor
        r = request("GET", "/v5/market/instruments-info", p)
        res = r.get("result", {})
        rows += res.get("list", [])
        cursor = res.get("nextPageCursor") or ""
        if not cursor:
            break
    out(rows)


def cmd_kline(args):
    """kline SYMBOL [interval] [limit] [category] [end_ms]

    interval: 1 3 5 15 30 60 120 240 360 720 D W M (minutes, or a letter).
    Bybit returns NEWEST FIRST and caps `limit` at 1000, so callers paginate
    backwards with `end`. Output here is re-sorted OLDEST FIRST to match the
    rest of this repo.
    """
    if not args:
        die("usage: kline SYMBOL [interval] [limit] [category] [end_ms]")
    sym = args[0]
    interval = args[1] if len(args) > 1 else "D"
    limit = args[2] if len(args) > 2 else "1000"
    cat = args[3] if len(args) > 3 else "spot"
    p = {"category": cat, "symbol": sym, "interval": interval, "limit": limit}
    if len(args) > 4 and args[4]:
        p["end"] = args[4]
    r = request("GET", "/v5/market/kline", p)
    rows = r.get("result", {}).get("list", [])
    rows.sort(key=lambda x: int(x[0]))
    out(rows)


def cmd_order(args):
    """order '<json>' — places an order. Body is passed through to Bybit v5.

    THE POINT OF BYBIT: takeProfit and stopLoss can both be attached here, so a
    position carries both legs at once. On the previous venue only one order could
    exist per symbol, and reconciling that is what the hourly scan routine was
    for. Example:

      {"category":"spot","symbol":"BTCUSDT","side":"Buy","orderType":"Market",
       "qty":"0.001","takeProfit":"75000","stopLoss":"60000"}
    """
    if not args:
        die("usage: order '<json body>'")
    try:
        body = json.loads(args[0])
    except json.JSONDecodeError as e:
        die(f"order body is not valid JSON: {e}")
    body.setdefault("category", "spot")
    if body.get("category") != "spot":
        print("WARNING: non-spot category — leveraged products can lose more "
              "than the account holds, which no risk rule in this repo assumes.",
              file=sys.stderr)
    out(request("POST", "/v5/order/create", body, private=True).get("result", {}))


def cmd_amend(args):
    if not args:
        die("usage: amend '<json body>'")
    out(request("POST", "/v5/order/amend", json.loads(args[0]), private=True).get("result", {}))


def cmd_cancel(args):
    if not args:
        die("usage: cancel '<json body>'")
    out(request("POST", "/v5/order/cancel", json.loads(args[0]), private=True).get("result", {}))


def cmd_orders(args):
    cat = args[0] if args else "spot"
    r = request("GET", "/v5/order/realtime", {"category": cat}, private=True)
    out(r.get("result", {}).get("list", []))


def cmd_history(args):
    cat = args[0] if args else "spot"
    r = request("GET", "/v5/order/history", {"category": cat, "limit": 50}, private=True)
    out(r.get("result", {}).get("list", []))


def cmd_fills(args):
    cat = args[0] if args else "spot"
    r = request("GET", "/v5/execution/list", {"category": cat, "limit": 100}, private=True)
    out(r.get("result", {}).get("list", []))


def cmd_time(args):
    out(request("GET", "/v5/market/time"))


def cmd_funding(args):
    """funding SYMBOL [limit] [end_ms] — public, read-only.

    GET /v5/market/funding/history, category=linear (perps). Bybit spot has no
    funding rate; this is a crowding/leverage signal from the perp market,
    reported OLDEST-to-check via re-sort like kline. Returns newest-first,
    capped at 200/page.
    """
    if not args:
        die("usage: funding SYMBOL [limit] [end_ms]")
    sym = args[0]
    limit = args[1] if len(args) > 1 else "200"
    p = {"category": "linear", "symbol": sym, "limit": limit}
    if len(args) > 2 and args[2]:
        p["endTime"] = args[2]
    r = request("GET", "/v5/market/funding/history", p)
    rows = r.get("result", {}).get("list", [])
    rows.sort(key=lambda x: int(x["fundingRateTimestamp"]))
    out(rows)


COMMANDS = {
    "balance": cmd_balance, "positions": cmd_positions, "holdings": cmd_holdings,
    "tickers": cmd_tickers, "instruments": cmd_instruments, "kline": cmd_kline,
    "order": cmd_order, "amend": cmd_amend, "cancel": cmd_cancel,
    "orders": cmd_orders, "history": cmd_history, "fills": cmd_fills,
    "time": cmd_time, "funding": cmd_funding,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("usage: python scripts/bybit.py <" + "|".join(COMMANDS) + "> [args]",
              file=sys.stderr)
        raise SystemExit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
