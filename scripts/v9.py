#!/usr/bin/env python3
"""v9 live engine - the tested crowd strategy, with Claude as the decision-maker.

    python scripts/v9.py plan                 # signal -> data/live/plan.json + data/live/brief.md
    python scripts/v9.py execute [--dry]      # plan + data/live/decisions.json -> orders
    python scripts/v9.py flatten-legacy       # close every pre-v9 position (one-off switch-over)
    python scripts/v9.py status               # book, P&L since v9 start, maker-fill rate

WHAT IT TRADES (validated 2026-09-24, backtest/lab, lockbox 2025-07..2026-09)
  micro_crowd: time-series CONTRARIAN to the 30d z-score of Binance's GLOBAL
  long/short ACCOUNT ratio on 12 major USDT perps. |z| >= 1.5 -> take the other
  side of the crowd for the next 6h bar, inverse-vol sized, book vol-targeted.
  Owner picked VOL_TARGET 0.55 ("very high"). Lockbox at that level with the
  live 2.5x gross cap: +54.5% CAGR, max DD -40.8%, 0 liquidations (70% maker
  fills assumed - this script measures the real rate).

WHY BINANCE'S RATIO, WHEN WE TRADE ON BYBIT
  The same frozen strategy on Bybit's own account ratio lost -5.6% over the
  lockbox; on Binance's it made +14.6% (taker fees). The signal is the crowd on
  the biggest venue. Only the 5-MINUTE Binance feed matches the tested history;
  the 1h feed does not (0.07), so the cache is built from 5m. The live endpoint
  stamps each 5-min value 300 s LATER than the archive the strategy was tested
  on (archive[ts] == api[ts+300] to 7e-4); the cache stores archive stamps (see
  API_STAMP_SHIFT). Parity (2026-09-24, 400 decisions 2026-06..09): live
  weights == research weights to 1e-13, 0 sign disagreements.

EXECUTION SAFETY (2026-09-24 audit)
  Every round re-reads positions and trades only the gap to the goal, so a lost
  order record, a partial fill, or a rerun after a crash never trades twice.
  Orders are tagged orderLinkId "v9-..."; resting ones are cancelled on any
  exit and at the start of the next execute. After the run every position is
  checked for a stopLoss. decisions.json must carry the plan's run_id.

CLAUDE'S ROLE
  `plan` writes the strategy's targets and a brief. Claude reads it, researches,
  and writes data/live/decisions.json (schema in routines/v9.md). Claude may
  approve, skip, resize (0-1.5x), flip, or open its own trades in symbols the
  strategy is not holding. Every opening order still passes scripts/checks.py
  (stopLoss attached, <=5x, stop inside half the liquidation distance, margin
  <= 50% and notional <= 300% of budget, daily loss breaker, HALT_TRADING).
  Strategy target and Claude target are both logged, so Claude's value is
  measured in dollars, not asserted.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import math
import os
import sys
import time
import urllib.request
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "backtest"))

import bybit as B        # noqa: E402  (loads .env, signs requests)
import checks            # noqa: E402

LIVE = os.path.join(ROOT, "data", "live")
CACHE = os.path.join(LIVE, "ls5m")
PLAN = os.path.join(LIVE, "plan.json")
DECISIONS = os.path.join(LIVE, "decisions.json")
BRIEF = os.path.join(LIVE, "brief.md")
STATE = os.path.join(LIVE, "v9_state.json")
LOG = os.path.join(ROOT, "memory", "V9-LOG.csv")

SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT",
        "ADAUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", "TRXUSDT", "DOTUSDT"]
VOL_TARGET = 0.55        # owner choice 2026-09-24
GROSS_CAP = 2.4          # x budget; 2.4x at 5x leverage = 48% margin, under the 50% gate
LEVERAGE = 5
STOP_PCT = 0.08          # attached stop; must stay inside half the 20% liquidation distance at 5x
CLAUDE_MAX_MULT = 1.5    # Claude may resize a strategy trade up to this multiple
MIN_TRADE_USD = 5.0      # Bybit minNotionalValue floor for USDT perps
POST_ONLY_ROUNDS = 3     # re-quote a resting maker order this many times ...
ROUND_WAIT_S = 50        # ... waiting this long each time, then take the remainder
BAR = 6 * 3600
# History the live panel is built from. The strategy's state (30d z, 120-bar vol
# scale with min-periods + ffill, 0.02 hysteresis band) reaches back further than
# one window: with 400 bars / 60 days the LAST row matched research only by a
# one-bar margin and 15 of 120 recent decisions differed (band state). 800 bars /
# 120 days reproduces research exactly (max |dw| 5e-14 over 120 decisions).
N_BARS = 800             # Binance klines limit (max 1500)
RETAIN_D = 120           # days of 5-min ratio kept in the cache
# Timestamp convention. The research store (Binance archive) stamps a 5-min row at
# the period START; the live fapi endpoint stamps the SAME value at the period END
# (verified 2026-09-24: archive[ts] == api[ts + 300] to 7e-4 on all 12 coins, vs
# 0.03-0.14 at equal stamps). The cache stores ARCHIVE stamps, so API rows are
# shifted back 300 s. Without this the live signal used the previous 5-min
# observation: 284 of 400 decisions differed, 28 threshold sign flips.
API_STAMP_SHIFT = 300
CACHE_CONV = "archive_period_start"
FAPI = "https://fapi.binance.com"
ARCHIVE = "https://data.binance.vision/data/futures/um/daily/metrics"

BUDGET = checks.BUDGET


def now_s():
    return int(time.time())


def utc(ts):
    return dt.datetime.fromtimestamp(int(ts), dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def http_json(url, tries=6):
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:     # noqa: BLE001 - network, retry (~1 min in total)
            if k == tries - 1:
                B.die(f"Binance data fetch failed after {tries} tries ({e}): {url.split('?')[0]} - "
                      "no plan this run; retry `v9.py plan` shortly")
            time.sleep(2 ** k)


def jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def jdump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, default=float)
    os.replace(tmp, path)


# --------------------------------------------------------------------- data
def _seed_from_archive_store(sym):
    """First use: the research store (Binance 5-min metrics) is the history."""
    p = os.path.join(ROOT, "data", "hist", "metrics", sym + ".npz")
    if not os.path.exists(p):
        return np.zeros(0, np.int64), np.zeros(0)
    with np.load(p) as z:
        ts, ls = z["ts"].astype(np.int64), z["ls_ratio"].astype(float)
    keep = (ts >= now_s() - RETAIN_D * 86400) & (ls > 0)   # 0 = archive placeholder, not data
    return ts[keep], ls[keep]


def _archive_day(sym, day):
    """One day of 5-min metrics from the public archive (published ~1 day late)."""
    url = f"{ARCHIVE}/{sym}/{sym}-metrics-{day}.zip"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            raw = r.read()
    except Exception:              # noqa: BLE001 - 404 before publication is normal
        return []
    out = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for line in zf.read(zf.namelist()[0]).decode().splitlines():
            parts = line.split(",")
            if len(parts) < 7 or not parts[1].startswith(sym):
                continue                                   # header row
            try:
                t = int(dt.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                        .replace(tzinfo=dt.timezone.utc).timestamp())
                v = float(parts[6])                        # count_long_short_ratio
            except ValueError:
                continue
            if v > 0:
                out.append((t, v))
    return out


def update_ls_cache(sym):
    """5-min global long/short ACCOUNT ratio, cached locally. Returns (ts, ls)."""
    path = os.path.join(CACHE, sym + ".npz")
    rows = {}
    if os.path.exists(path):
        with np.load(path) as z:
            # a cache written before the stamp fix mixes archive and API stamps -> rebuild
            if "conv" in z.files and str(z["conv"]) == CACHE_CONV:
                rows = dict(zip(z["ts"].astype(np.int64).tolist(), z["ls"].astype(float).tolist()))
    if not rows or min(rows) > now_s() - (RETAIN_D - 2) * 86400:
        ts, ls = _seed_from_archive_store(sym)         # research store fills the history
        for t, v in zip(ts.tolist(), ls.tolist()):
            rows.setdefault(t, v)
    # a gap longer than the live endpoint's ~41h window -> backfill from the archive
    last = max(rows) if rows else now_s() - RETAIN_D * 86400
    if now_s() - last > 40 * 3600:
        d = dt.datetime.fromtimestamp(last, dt.timezone.utc).date()
        end = dt.datetime.now(dt.timezone.utc).date()
        while d <= end:
            rows.update(dict(_archive_day(sym, d.isoformat())))
            d += dt.timedelta(days=1)
    api = http_json(f"{FAPI}/futures/data/globalLongShortAccountRatio"
                    f"?symbol={sym}&period=5m&limit=500")
    for x in api:
        v = float(x["longShortRatio"])
        if v > 0:
            rows[int(x["timestamp"]) // 1000 - API_STAMP_SHIFT] = v
    keep = sorted(t for t in rows if t >= now_s() - RETAIN_D * 86400)
    ts = np.array(keep, np.int64)
    ls = np.array([rows[t] for t in keep], float)
    os.makedirs(CACHE, exist_ok=True)
    tmp = path + ".part.npz"
    np.savez_compressed(tmp, ts=ts, ls=ls, conv=CACHE_CONV)
    os.replace(tmp, path)
    return ts, ls


def binance_6h(sym, n=N_BARS):
    """Completed 6h Binance perp bars (the price source the strategy was tested on)."""
    rows = http_json(f"{FAPI}/fapi/v1/klines?symbol={sym}&interval=6h&limit={n + 1}")
    rows = [r for r in rows if int(r[0]) // 1000 + BAR <= now_s()]      # drop the forming bar
    return (np.array([int(r[0]) // 1000 for r in rows], np.int64),
            np.array([[float(r[i]) for i in (1, 2, 3, 4, 5, 7)] for r in rows]))


def build_panel():
    from lab import data as D
    bars = {s: binance_6h(s) for s in SYMS}
    t = bars["BTCUSDT"][0]
    T, N = len(t), len(SYMS)
    f = {k: np.full((T, N), np.nan) for k in ("o", "h", "l", "c", "v", "qv")}
    for j, s in enumerate(SYMS):
        ts, x = bars[s]
        idx = np.searchsorted(t, ts)
        ok = (idx < T) & (t[np.clip(idx, 0, T - 1)] == ts)
        for k, col in zip(("o", "h", "l", "c", "v", "qv"), range(6)):
            f[k][idx[ok], j] = x[ok, col]
    ls = np.full((T, N), np.nan)
    close = t + BAR
    last_obs = {}
    for j, s in enumerate(SYMS):
        cts, cls = update_ls_cache(s)
        # tested rule (lab.data.load_metrics): value at bar i = last row whose ARCHIVE stamp + 300 s
        # is <= the bar close; NaN if that row is older than max(dt, 2h) = 6h. Cache stamps are
        # archive stamps (see API_STAMP_SHIFT).
        avail = cts + 300
        k = np.searchsorted(avail, close, side="right") - 1
        good = k >= 0
        v = np.where(good, cls[np.clip(k, 0, None)], np.nan)
        stale = close - np.where(good, avail[np.clip(k, 0, None)], 0) > BAR
        v[stale] = np.nan
        ls[:, j] = v
        last_obs[s] = int(cts[-1]) + 300 if len(cts) else 0
    p = D.Panel(t=t, dt=BAR, symbols=list(SYMS), o=f["o"], h=f["h"], l=f["l"], c=f["c"],
                v=f["v"], qv=f["qv"], funding=np.zeros((T, N)), tradable=np.isfinite(f["c"]),
                meta={"source": "binance fapi live", "last_ratio_obs": last_obs})
    return p, {"ls_ratio": ls, "top_ls_ratio": np.full((T, N), np.nan)}


def strategy_targets():
    from lab.strategies import micro_crowd as MC
    from lab.strategies import _micro_stats as ST
    p, m = build_panel()
    latest_close = now_s() - now_s() % BAR
    if int(p.t[-1]) + BAR != latest_close:
        B.die(f"Binance klines end at the {utc(p.t[-1] + BAR)} close, but the {utc(latest_close)} bar has "
              "closed - feed lagging or clock skew; re-run `v9.py plan` in a minute")
    warn = []
    for j, s in enumerate(SYMS):
        if not np.isfinite(p.c[-1, j]):
            warn.append(f"{s}: no Binance kline for the last bar - strategy holds it flat")
        if not np.isfinite(m["ls_ratio"][-1, j]):
            warn.append(f"{s}: no fresh long/short ratio - strategy holds it flat")
        elif p.meta["last_ratio_obs"].get(s, 0) < latest_close:
            warn.append(f"{s}: ratio for the bar close not published yet - using an older 5-min value")
        n_ok = int(np.isfinite(m["ls_ratio"][-360:, j]).sum())
        if n_ok < 350:
            warn.append(f"{s}: only {n_ok}/360 bars of ratio history - signal differs from the tested one")
    params = dict(MC.FROZEN, vol_target=VOL_TARGET)
    w = MC.weights(p, params, m)[-1].copy()
    gross = float(np.abs(w).sum())
    if gross > GROSS_CAP:
        w *= GROSS_CAP / gross
    with np.errstate(invalid="ignore", divide="ignore"):
        z = ST.roll_z(np.log(m["ls_ratio"]), 120, 60)[-1]
    info = {}
    for j, s in enumerate(SYMS):
        c = p.c[:, j]
        info[s] = {"z_crowd": None if not np.isfinite(z[j]) else round(float(z[j]), 2),
                   "ls_ratio": None if not np.isfinite(m["ls_ratio"][-1, j]) else round(float(m["ls_ratio"][-1, j]), 3),
                   "ret_24h": round(float(c[-1] / c[-5] - 1), 4) if np.isfinite(c[-5]) else None,
                   "weight": round(float(w[j]), 4), "target_usd": round(float(w[j]) * BUDGET, 2)}
    return int(p.t[-1] + BAR), info, warn


# ------------------------------------------------------------------ exchange
def ticker(sym):
    r = B.request("GET", "/v5/market/tickers", {"category": "linear", "symbol": sym})
    lst = r.get("result", {}).get("list", [])
    if not lst:
        raise ValueError(f"{sym} is not a Bybit USDT perp")
    return lst[0]


_INSTR = {}


def instrument(sym):
    if sym not in _INSTR:
        try:
            r = B.request("GET", "/v5/market/instruments-info", {"category": "linear", "symbol": sym})
        except SystemExit:                 # retCode 10001 'symbol invalid'
            raise ValueError(f"{sym} is not a Bybit USDT perp") from None
        lst = r.get("result", {}).get("list", [])
        if not lst or lst[0].get("status", "Trading") != "Trading":
            raise ValueError(f"{sym} is not a tradable Bybit USDT perp")
        x = lst[0]
        _INSTR[sym] = {"step": float(x["lotSizeFilter"]["qtyStep"]),
                       "min_qty": float(x["lotSizeFilter"]["minOrderQty"]),
                       "min_usd": float(x["lotSizeFilter"].get("minNotionalValue") or MIN_TRADE_USD),
                       "tick": float(x["priceFilter"]["tickSize"])}
    return _INSTR[sym]


def fmt(x, step):
    dec = max(0, -int(math.floor(math.log10(step) + 1e-9))) if step < 1 else 0
    return f"{x:.{dec}f}"


def floor_to(x, step):
    return math.floor(x / step + 1e-9) * step


def positions():
    rows, cursor = [], None
    while True:
        prm = {"category": "linear", "settleCoin": "USDT", "limit": 200}
        if cursor:
            prm["cursor"] = cursor
        res = B.request("GET", "/v5/position/list", prm, private=True).get("result", {})
        rows += res.get("list", [])
        cursor = res.get("nextPageCursor") or None
        if not cursor:
            break
    live = [p for p in rows if float(p.get("size") or 0) != 0]
    if any(int(p.get("positionIdx") or 0) != 0 for p in live):
        B.die("a position has positionIdx != 0 (hedge mode) - v9 assumes one-way mode (positionIdx 0)")
    return {p["symbol"]: p for p in live}


def signed_qty(p):
    q = float(p.get("size") or 0)
    return q if p.get("side") == "Buy" else -q


def _leverage_now(sym):
    r = B.request("GET", "/v5/position/list", {"category": "linear", "symbol": sym}, private=True)
    lst = r.get("result", {}).get("list", [])
    return {float(x.get("leverage") or 0) for x in lst}


def set_leverage(sym):
    """Set LEVERAGE on sym. B.request raises SystemExit(1) on ANY retCode, so the old
    `"110043" in str(e)` test never matched ("1") and an already-5x symbol crashed the
    run. Read first; after a failed POST accept only if the venue now reports 5x."""
    if _leverage_now(sym) == {float(LEVERAGE)}:
        return
    try:
        B.request("POST", "/v5/position/set-leverage",
                  {"category": "linear", "symbol": sym,
                   "buyLeverage": str(LEVERAGE), "sellLeverage": str(LEVERAGE)}, private=True)
    except SystemExit:
        if _leverage_now(sym) != {float(LEVERAGE)}:
            raise


def stop_price(sym, side, ref):
    """Long stop floored, short stop ceiled to the tick: always >= STOP_PCT away (by < 1 tick)."""
    tick = instrument(sym)["tick"]
    raw = ref * (1 - STOP_PCT) if side == "Buy" else ref * (1 + STOP_PCT)
    return fmt(floor_to(raw, tick) if side == "Buy" else math.ceil(raw / tick - 1e-9) * tick, tick)


_LINK = [0]


def link_id():
    """orderLinkId tag, so a crashed run's resting orders can be found and cancelled."""
    _LINK[0] += 1
    return f"v9-{int(time.time() * 1000)}-{_LINK[0]}"


def place(body):
    """Same path as `bybit.py order`: the deterministic gate first, then the venue.
    `_allow_add` lets a strategy REBALANCE grow an existing same-side position.
    `_pending` is the notional of this run's OTHER opening orders still resting; it is
    added to this order's notional so a batch placed in one round cannot jointly breach
    the gate's gross/margin caps (the gate only sees filled positions). Every other
    check (stop, leverage, clearance, breaker, caps) still applies."""
    if not checks.is_exit(body):
        mark = float(ticker(body["symbol"])["markPrice"])
        body["_notional"] = float(body.get("qty") or 0) * mark + float(body.get("_pending") or 0)
        checks.check_order(body, checks.live_fetch())      # raises GateReject
    for k in ("_notional", "_allow_add", "_pending"):
        body.pop(k, None)
    return B.request("POST", "/v5/order/create", body, private=True)["result"]["orderId"]


TERMINAL = ("Filled", "Cancelled", "Rejected", "Deactivated", "PartiallyFilledCanceled")


def order_state(sym, oid):
    for k in range(3):
        for path in ("/v5/order/realtime", "/v5/order/history"):
            lst = B.request("GET", path, {"category": "linear", "symbol": sym, "orderId": oid},
                            private=True).get("result", {}).get("list", [])
            if lst:
                return lst[0]
        time.sleep(1 + k)
    return {}


def cancel(sym, oid):
    try:
        B.request("POST", "/v5/order/cancel", {"category": "linear", "symbol": sym, "orderId": oid},
                  private=True)
    except SystemExit:
        pass                           # already filled / gone


def stale_v9_orders():
    """Open orders a previous (crashed) v9 run left resting - found by the orderLinkId tag."""
    r = B.request("GET", "/v5/order/realtime", {"category": "linear", "settleCoin": "USDT", "limit": 50},
                  private=True).get("result", {}).get("list", [])
    return [o for o in r if str(o.get("orderLinkId") or "").startswith("v9-")]


def _left(j, cur, step):
    """Qty still to trade for job j given the CURRENT signed position (exchange truth).
    Reconciling against the position, not against order-status bookkeeping, means a
    lost/late order record, a partial fill or a rerun can never trade the same qty twice,
    and a reduceOnly order can never ask for more than is held."""
    goal = j["goal"]
    if j["reduce"]:
        if j["side"] == "Sell":
            left = cur - max(goal, 0.0) if cur > 0 else 0.0
        else:
            left = min(goal, 0.0) - cur if cur < 0 else 0.0
    elif j["side"] == "Buy":
        left = goal - max(cur, 0.0)
    else:
        left = -goal - max(-cur, 0.0)
    return floor_to(max(0.0, left), step)


def work_orders(jobs, fills, dry=False):
    """jobs: [{sym, side, goal, reduce, add}] -> maker-first execution; fills are appended
    to `fills` as they happen (so a crash still leaves them for the log). Each round
    re-reads positions and re-quotes the unfilled qty at the touch as PostOnly; after
    POST_ONLY_ROUNDS the remainder goes as a market order. Any order still resting when
    this returns or raises (crash, Ctrl-C, venue error) is cancelled."""
    for j in jobs:
        j["maker_qty"] = 0.0
    if dry:
        return
    resting = {}
    try:
        for rnd in range(POST_ONLY_ROUNDS + 1):
            held = positions()
            live, pending = [], 0.0
            for j in jobs:
                if j.get("blocked") or j.get("error"):
                    continue
                ins = instrument(j["sym"])
                cur = signed_qty(held[j["sym"]]) if j["sym"] in held else 0.0
                if not j["reduce"] and cur and (cur > 0) != (j["side"] == "Buy"):
                    j["blocked"] = "opposite position still open after the close leg - not opening"
                    print(f"  {j['sym']}: {j['blocked']}", file=sys.stderr)
                    continue
                j["left"] = left = _left(j, cur, ins["step"])
                if left < ins["min_qty"] - 1e-12:
                    continue
                tk = ticker(j["sym"])
                px = float(tk["bid1Price"] if j["side"] == "Buy" else tk["ask1Price"])
                mark = float(tk["markPrice"])
                if not j["reduce"] and left * mark < max(ins["min_usd"], MIN_TRADE_USD):
                    j["note"] = (f"remainder {left:g} is below the ${max(ins['min_usd'], MIN_TRADE_USD):g} "
                                 "minimum order value - left unfilled")
                    continue                  # the venue would reject it (110094)
                body = {"category": "linear", "symbol": j["sym"], "side": j["side"],
                        "qty": fmt(left, ins["step"]), "positionIdx": 0, "orderLinkId": link_id()}
                if j["reduce"]:
                    body["reduceOnly"] = True
                else:
                    body.update({"stopLoss": stop_price(j["sym"], j["side"], mark),
                                 "slTriggerBy": "MarkPrice", "tpslMode": "Full", "_pending": pending})
                    if j["add"] or cur:        # growing a same-side position (incl. an earlier round's fill)
                        body["_allow_add"] = True
                if rnd < POST_ONLY_ROUNDS:
                    body.update({"orderType": "Limit", "price": fmt(px, ins["tick"]), "timeInForce": "PostOnly"})
                else:
                    body.update({"orderType": "Market", "timeInForce": "IOC"})
                try:
                    j["oid"] = place(body)
                except checks.GateReject as e:
                    j["blocked"] = str(e)
                    print(f"  {j['sym']}: {e}", file=sys.stderr)
                    continue
                except (SystemExit, ValueError) as e:   # venue rejected (B.request printed the retCode)
                    j["error"] = f"order rejected by the venue ({e})"
                    print(f"  {j['sym']}: {j['error']}", file=sys.stderr)
                    continue
                resting[j["oid"]] = j["sym"]
                live.append(j)
                if not j["reduce"]:
                    pending += left * mark
            if not live:
                break
            time.sleep(ROUND_WAIT_S if rnd < POST_ONLY_ROUNDS else 3)
            for j in live:
                st = order_state(j["sym"], j["oid"])
                if st.get("orderStatus") not in TERMINAL:
                    cancel(j["sym"], j["oid"])
                    st = order_state(j["sym"], j["oid"])
                if st.get("orderStatus") in TERMINAL:
                    resting.pop(j["oid"], None)
                done = float(st.get("cumExecQty") or 0)
                if done > 0:
                    fills.append({"sym": j["sym"], "side": j["side"], "qty": done,
                                  "price": float(st.get("avgPrice") or 0), "reduce": j["reduce"],
                                  "maker": rnd < POST_ONLY_ROUNDS, "fee": float(st.get("cumExecFee") or 0)})
                    if rnd < POST_ONLY_ROUNDS:
                        j["maker_qty"] += done
    finally:
        for oid, sym in list(resting.items()):
            cancel(sym, oid)


def ensure_stops(added):
    """After the run: re-anchor the stop of every position that was ADDED to at STOP_PCT
    from the mark, and give any position with NO stop one. Never raises - a failed
    trading-stop call (34040 'not modified', network) must not abort the run's log."""
    problems = []
    try:
        held = positions()
    except SystemExit:
        return ["could not read positions to verify stops - CHECK MANUALLY (v9.py status)"]
    for s, p in held.items():
        has = float(p.get("stopLoss") or 0) > 0
        if has and s not in added:
            continue
        try:
            stop = stop_price(s, p["side"], float(p["markPrice"]))
            if has and stop == fmt(float(p["stopLoss"]), instrument(s)["tick"]):
                continue
            B.request("POST", "/v5/position/trading-stop",
                      {"category": "linear", "symbol": s, "positionIdx": 0, "stopLoss": stop,
                       "slTriggerBy": "MarkPrice", "tpslMode": "Full"}, private=True)
        except (SystemExit, ValueError) as e:
            if not has:
                problems.append(f"{s} has NO stopLoss and setting one failed ({e})")
    try:
        flagged = {x.split()[0] for x in problems}
        problems += [f"{s} has NO stopLoss" for s, p in positions().items()
                     if not float(p.get("stopLoss") or 0) > 0 and s not in flagged]
    except SystemExit:
        problems.append("could not re-read positions to verify stops - CHECK MANUALLY")
    return problems


def total_equity():
    r = B.request("GET", "/v5/account/wallet-balance", {"accountType": "UNIFIED"}, private=True)
    return float(r["result"]["list"][0]["totalEquity"])


# ----------------------------------------------------------------- commands
def cmd_plan(_args):
    decided_at, info, warn = strategy_targets()
    held = positions()
    rows = []
    for s in SYMS:
        tk = ticker(s)
        cur_usd = signed_qty(held[s]) * float(tk["markPrice"]) if s in held else 0.0
        rows.append({"symbol": s, **info[s], "current_usd": round(cur_usd, 2),
                     "mark": float(tk["markPrice"]), "funding_8h": float(tk.get("fundingRate") or 0)})
    others = {s: {"side": p["side"], "size": p["size"], "uPnL": p.get("unrealisedPnl"),
                  "stopLoss": p.get("stopLoss")} for s, p in held.items() if s not in SYMS}
    guard = drawdown_guard()
    plan = {"run_id": utc(now_s()), "decided_at_bar_close": utc(decided_at), "budget": BUDGET,
            "vol_target": VOL_TARGET, "gross_cap": GROSS_CAP, "rows": rows, "non_strategy_positions": others,
            "data_warnings": warn, "risk": guard}
    jdump(plan, PLAN)
    L = [f"# v9 brief - {plan['run_id']} UTC (signal from the {plan['decided_at_bar_close']} bar close)",
         "", f"Budget ${BUDGET:.0f} | vol target {VOL_TARGET} | gross cap {GROSS_CAP}x | leverage {LEVERAGE}x | stop {STOP_PCT:.0%}",
         *(["", "RISK: " + " | ".join(guard)] if guard else []),
         "", "Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.",
         "", "| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        r24 = "" if r["ret_24h"] is None else f"{r['ret_24h'] * 100:+.1f}%"
        L.append(f"| {r['symbol']} | {r['z_crowd']} | {r['ls_ratio']} | {r24} | {r['target_usd']:+.2f} | "
                 f"{r['current_usd']:+.2f} | {r['funding_8h'] * 100:+.4f}% |")
    if warn:
        L += ["", "DATA WARNINGS:"] + [f"- {w}" for w in warn]
    if others:
        L += ["", "Positions OUTSIDE the strategy (legacy or Claude's own):"]
        L += [f"- {s}: {v['side']} {v['size']} uPnL {v['uPnL']} SL {v['stopLoss']}" for s, v in others.items()]
    L += ["", "Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`."]
    with open(BRIEF, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


ACTIONS = {"approve": 1.0, "skip": 0.0, "flip": -1.0, "resize": None}
SIDES = {"buy": "Buy", "sell": "Sell"}


def _finite(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def load_decisions(plan):
    """decisions.json -> normalized dict, or die. Strict on purpose: a stale file from an
    earlier run, a typo'd action or side, or a missing file must stop the run loudly
    instead of silently approving everything / opening a trade on the wrong side / closing
    every non-strategy position."""
    if not os.path.exists(DECISIONS):
        B.die("no data/live/decisions.json - write it (routines/v9.md). "
              f'{{"run_id": "{plan["run_id"]}", "decisions": []}} approves the strategy as-is.')
    try:
        with open(DECISIONS, encoding="utf-8") as f:
            dec = json.load(f)
    except ValueError as e:
        B.die(f"data/live/decisions.json is not valid JSON: {e}")
    if not isinstance(dec, dict):
        B.die("data/live/decisions.json must be a JSON object")
    if dec.get("run_id") != plan["run_id"]:
        B.die(f"decisions.json run_id {dec.get('run_id')!r} != plan run_id {plan['run_id']!r} - "
              "these decisions were written for another plan; re-decide on the current brief")
    errs, out = [], {"decisions": {}, "claude_trades": [], "keep": set()}
    for key in ("decisions", "claude_trades", "keep"):
        v = dec.get(key) or []
        if not isinstance(v, list) or not all(isinstance(x, dict) for x in v):
            errs.append(f"{key} must be a list of objects")
            v = []
        dec[key] = v
    for d in dec["decisions"]:
        s = str(d.get("symbol", "")).upper()
        act = str(d.get("action", "approve")).lower()
        if s not in SYMS:
            errs.append(f"decision for {s or '?'}: not a strategy symbol ({', '.join(SYMS)}) - use claude_trades")
            continue
        if s in out["decisions"]:
            errs.append(f"{s}: more than one decision")
        if act not in ACTIONS:
            errs.append(f"{s}: unknown action {d.get('action')!r} (approve|skip|resize|flip)")
            continue
        mult = ACTIONS[act]
        if act == "resize":
            mult = _finite(d.get("size_mult"))
            if mult is None or not 0.0 <= mult <= CLAUDE_MAX_MULT:
                errs.append(f"{s}: size_mult {d.get('size_mult')!r} must be a number in 0..{CLAUDE_MAX_MULT}")
                continue
        out["decisions"][s] = {"action": act, "mult": mult, "reason": d.get("reason", "")}
    for t in dec["claude_trades"]:
        s = str(t.get("symbol", "")).upper()
        side = SIDES.get(str(t.get("side", "")).lower())
        usd = _finite(t.get("notional_usd"))
        if not s.endswith("USDT"):
            errs.append(f"claude trade {s or '?'}: symbol must be a USDT perp")
        elif side is None:
            errs.append(f"claude trade {s}: side {t.get('side')!r} must be Buy or Sell")
        elif usd is None or usd <= 0:
            errs.append(f"claude trade {s}: notional_usd {t.get('notional_usd')!r} must be a positive number")
        else:
            out["claude_trades"].append({"symbol": s, "usd": usd if side == "Buy" else -usd,
                                         "reason": t.get("reason", "")})
    out["keep"] = {str(k.get("symbol", "")).upper() for k in dec["keep"]}
    if errs:
        B.die("decisions.json rejected - fix and re-run execute:\n  - " + "\n  - ".join(errs))
    return out


def cmd_execute(args):
    dry = "--dry" in args
    plan = jload(PLAN)
    if not plan:
        B.die("no data/live/plan.json - run `v9.py plan` first")
    t_plan = int(dt.datetime.strptime(plan["run_id"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp())
    age_h = (now_s() - t_plan) / 3600
    if age_h > 1.5:
        B.die(f"plan is {age_h:.1f}h old - re-run `v9.py plan`; the edge is in the first hours")
    t_bar = int(dt.datetime.strptime(plan["decided_at_bar_close"], "%Y-%m-%d %H:%M")
                .replace(tzinfo=dt.timezone.utc).timestamp())
    if t_bar < now_s() - now_s() % BAR:
        B.die(f"a newer 6h bar has closed since the plan's signal ({plan['decided_at_bar_close']}) - "
              "re-run `v9.py plan` and re-decide")
    dec = load_decisions(plan)
    for s in dec["keep"] & set(SYMS):
        print(f"  keep {s} ignored: strategy symbols follow the strategy target (use resize/skip)", file=sys.stderr)

    targets, rows = {}, {}
    for r in plan["rows"]:
        s, strat = r["symbol"], float(r["target_usd"])
        d = dec["decisions"].get(s, {"action": "approve", "mult": 1.0, "reason": ""})
        targets[s] = strat * d["mult"]
        rows[s] = {"strat": strat, "final": targets[s], "act": d["action"], "why": d["reason"]}
    held = positions()
    errs = []
    for t in dec["claude_trades"]:                     # Claude's own ideas
        s = t["symbol"]
        if s in targets and targets[s] != 0:
            print(f"  claude trade {s} ignored: the strategy holds it - use resize/flip instead", file=sys.stderr)
            continue
        try:
            instrument(s)
        except ValueError as e:
            errs.append(str(e))
            continue
        targets[s] = t["usd"]
        rows[s] = {"strat": rows.get(s, {}).get("strat", 0.0), "final": t["usd"], "act": "claude_trade",
                   "why": t["reason"]}
    if errs:
        B.die("claude_trades rejected: " + "; ".join(errs))
    kept = set()
    for s, p in held.items():                        # Claude closes its own / legacy positions explicitly
        if s not in targets:
            keep = s in dec["keep"]
            targets[s] = signed_qty(p) * float(p["markPrice"]) if keep else 0.0
            rows[s] = {"strat": 0.0, "final": targets[s], "act": "keep" if keep else "close_unlisted", "why": ""}
            if keep:
                kept.add(s)
    # Hard book cap BEFORE any order: resize (<=1.5x) + claude_trades can ask for more than the
    # gate allows (margin 50% of budget = 2.5x notional at 5x). Without this, orders placed in
    # the same round each passed the gate alone and could jointly breach it; with it, the
    # book is scaled down in proportion instead of the last symbols being blocked at random.
    cap_usd = min(checks.NOTIONAL_CAP, checks.MARGIN_CAP * LEVERAGE) * BUDGET * 0.96
    fixed = sum(abs(targets[s]) * LEVERAGE / max(1.0, float(held[s].get("leverage") or LEVERAGE)) for s in kept)
    flex = sum(abs(v) for s, v in targets.items() if s not in kept)
    if flex > 0 and fixed + flex > cap_usd:
        k = max(0.0, cap_usd - fixed) / flex
        print(f"  book ${fixed + flex:.0f} exceeds the ${cap_usd:.0f} cap - scaling new targets x{k:.3f}", file=sys.stderr)
        for s in targets:
            if s not in kept:
                targets[s] *= k
                rows[s]["final"] = targets[s]
                rows[s]["act"] += f"*{k:.2f}"

    jobs_close, jobs_open = [], []
    for s, usd in targets.items():
        ins = instrument(s)
        mark = float(ticker(s)["markPrice"])
        floor_usd = max(ins["min_usd"], MIN_TRADE_USD)
        want = floor_to(abs(usd) / mark, ins["step"]) * (1 if usd >= 0 else -1)
        if abs(want) * mark < floor_usd or abs(want) < ins["min_qty"]:
            want = 0.0
        have = signed_qty(held[s]) if s in held else 0.0
        if want == have or (want != 0 and abs(want - have) * mark < floor_usd):
            continue                                  # inside the rebalance band (a close to flat always goes)
        if have and (want == 0 or (want > 0) != (have > 0)):
            jobs_close.append({"sym": s, "side": "Sell" if have > 0 else "Buy", "goal": 0.0,
                               "qty": abs(have), "reduce": True, "add": False})
            have = 0.0
        if want and abs(want) < abs(have):
            jobs_close.append({"sym": s, "side": "Sell" if have > 0 else "Buy", "goal": want,
                               "qty": floor_to(abs(have) - abs(want), ins["step"]), "reduce": True, "add": False})
        elif want:
            jobs_open.append({"sym": s, "side": "Buy" if want > 0 else "Sell", "goal": want,
                              "qty": floor_to(abs(want) - abs(have), ins["step"]), "reduce": False, "add": bool(have)})
    stale = stale_v9_orders()
    if dry:
        print(json.dumps({"dry": True, "targets_usd": {s: round(v, 2) for s, v in targets.items()},
                          "stale_v9_orders_to_cancel": [(o["symbol"], o["orderId"]) for o in stale],
                          "close": [{k: j[k] for k in ("sym", "side", "qty", "goal")} for j in jobs_close],
                          "open": [{k: j[k] for k in ("sym", "side", "qty", "goal", "add")} for j in jobs_open]},
                         indent=1, default=float))
        return
    for o in stale:                                   # a crashed earlier run must not fill on top of this one
        cancel(o["symbol"], o["orderId"])
    for j in jobs_open:
        try:
            set_leverage(j["sym"])
        except SystemExit:
            j["blocked"] = f"could not set {LEVERAGE}x leverage"
    fills, problems = [], []
    try:
        work_orders(jobs_close, fills)
        work_orders(jobs_open, fills)
    finally:
        problems = ensure_stops({f["sym"] for f in fills if not f["reduce"]})
        _write_log(plan, rows, fills)
        for p in problems:
            print(f"  STOP PROBLEM: {p}", file=sys.stderr)
    st = jload(STATE, {}) or {}
    if "start_equity" not in st:
        st.update({"start_equity": total_equity(), "start_utc": utc(now_s())})
        jdump(st, STATE)
    print(json.dumps({"dry": dry, "orders_close": len(jobs_close), "orders_open": len(jobs_open),
                      "fills": fills, "stop_problems": problems,
                      "blocked": [{k: j.get(k) for k in ("sym", "side", "blocked", "error", "note")}
                                  for j in jobs_close + jobs_open if j.get("blocked") or j.get("error") or j.get("note")]},
                     indent=1, default=float))


def _write_log(plan, rows, fills):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a", encoding="utf-8") as f:
        if new:
            f.write("run_utc,symbol,strategy_usd,final_usd,action,reason,filled_qty,avg_price,maker,fee\n")
        for s, r in rows.items():
            fl = [x for x in fills if x["sym"] == s]
            q = sum(x["qty"] for x in fl)
            px = (sum(x["qty"] * x["price"] for x in fl) / q) if q else 0
            mk = (sum(x["qty"] for x in fl if x["maker"]) / q) if q else ""
            why = str(r["why"]).replace(",", ";").replace("\n", " ")[:200]
            f.write(f"{plan['run_id']},{s},{r['strat']:.2f},{r['final']:.2f},{r['act']},{why},{q:g},{px:g},{mk},"
                    f"{sum(x['fee'] for x in fl):.5f}\n")


def cmd_flatten_legacy(args):
    dry = "--dry" in args
    held = positions()
    jobs = [{"sym": s, "side": "Sell" if signed_qty(p) > 0 else "Buy", "qty": abs(signed_qty(p)),
             "goal": 0.0, "reduce": True, "add": False} for s, p in held.items()]
    print(f"closing {len(jobs)} perp positions: {', '.join(held)}")
    fills = []
    work_orders(jobs, fills, dry)
    if dry:
        fills = [{k: j[k] for k in ("sym", "side", "qty")} for j in jobs]
    spot = B.request("GET", "/v5/order/realtime", {"category": "spot", "orderFilter": "StopOrder"},
                     private=True).get("result", {}).get("list", [])
    for o in spot:
        print(f"cancel spot stop {o['symbol']} {o['orderId']}")
        if not dry:
            B.request("POST", "/v5/order/cancel", {"category": "spot", "symbol": o["symbol"],
                                                   "orderId": o["orderId"], "orderFilter": "StopOrder"}, private=True)
            coin = o["symbol"].replace("USDT", "")
            bal = B.request("GET", "/v5/account/wallet-balance", {"accountType": "UNIFIED", "coin": coin},
                            private=True)["result"]["list"][0]["coin"]
            qty = float(bal[0]["walletBalance"]) if bal else 0.0
            r = B.request("GET", "/v5/market/instruments-info", {"category": "spot", "symbol": o["symbol"]})
            step = float(r["result"]["list"][0]["lotSizeFilter"]["basePrecision"])
            q = floor_to(qty, step)
            if q > 0:
                B.request("POST", "/v5/order/create", {"category": "spot", "symbol": o["symbol"], "side": "Sell",
                                                        "orderType": "Market", "qty": fmt(q, step)}, private=True)
                print(f"sold spot {coin} {fmt(q, step)}")
    print(json.dumps({"dry": dry, "fills": fills}, indent=1, default=float))


def cmd_status(_args):
    held = positions()
    st = jload(STATE, {}) or {}
    eq = total_equity()
    print(f"v9 since {st.get('start_utc', 'not started')} | P&L ${eq - st['start_equity']:+.2f} on the ${BUDGET:.0f} budget"
          if "start_equity" in st else "v9 has not executed yet")
    for s, p in held.items():
        print(f"  {s:10s} {p['side']:4s} size {p['size']:>10s} value ${float(p.get('positionValue') or 0):8.2f} "
              f"uPnL {float(p.get('unrealisedPnl') or 0):+7.2f} SL {p.get('stopLoss')}")
    if os.path.exists(LOG):
        rows = [l.rstrip("\n").split(",") for l in open(LOG, encoding="utf-8")][1:]
        mk = [float(r[8]) for r in rows if len(r) > 9 and r[8] not in ("", None)]
        if mk:
            print(f"maker-fill share (by qty, per order group): {100 * sum(mk) / len(mk):.0f}% over {len(mk)} fills "
                  f"(backtest assumed 70%)")


# ------------------------------------------------------------ learning loop
REVIEW_DD = 0.35         # of budget: brief shouts REVIEW
HALT_DD = 0.50           # of budget: plan writes HALT_TRADING (new entries stop, exits work)
HALT_FILE = os.path.join(ROOT, "HALT_TRADING")


def drawdown_guard():
    """P&L since the v9 start and from its peak, on the $200 budget. Creates the
    kill-switch file at -50% of budget so a losing streak cannot run unattended."""
    st = jload(STATE, {}) or {}
    if "start_equity" not in st:
        return []
    eq = total_equity()
    pnl = eq - st["start_equity"]
    peak = max(float(st.get("peak_pnl", 0.0)), pnl)
    if peak != st.get("peak_pnl"):
        st["peak_pnl"] = peak
        jdump(st, STATE)
    out = [f"P&L since v9 start ${pnl:+.2f} ({pnl / BUDGET:+.1%} of budget); from peak ${pnl - peak:+.2f}"]
    if pnl <= -HALT_DD * BUDGET and not os.path.exists(HALT_FILE):
        with open(HALT_FILE, "w", encoding="utf-8") as f:
            f.write(f"v9 auto-halt {utc(now_s())}: P&L ${pnl:.2f} <= -{HALT_DD:.0%} of the ${BUDGET:.0f} budget. "
                    "New entries stop; exits still work. Owner decides whether to resume (delete this file).\n")
        out.append(f"AUTO-HALT: loss reached {HALT_DD:.0%} of budget - HALT_TRADING created; only exits run until the owner resumes")
    elif pnl <= -REVIEW_DD * BUDGET:
        out.append(f"REVIEW LEVEL: loss beyond {REVIEW_DD:.0%} of budget - be conservative and flag it in the journal")
    return out


def _log_rows():
    if not os.path.exists(LOG):
        return []
    rows = []
    for line in open(LOG, encoding="utf-8").read().splitlines()[1:]:
        p = line.split(",")
        if len(p) < 10:
            continue
        try:
            ts = int(dt.datetime.strptime(p[0], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp())
            rows.append({"ts": ts, "sym": p[1], "strat": float(p[2]), "final": float(p[3]), "act": p[4],
                         "why": p[5], "maker": float(p[8]) if p[8] else None})
        except ValueError:
            continue
    return rows


def _fwd_returns(sym, t0):
    """6h Binance bar returns keyed by bar OPEN (= the decision close)."""
    rows = http_json(f"{FAPI}/fapi/v1/klines?symbol={sym}&interval=6h&startTime={t0 * 1000}&limit=1500")
    return {int(r[0]) // 1000: float(r[4]) / float(r[1]) - 1 for r in rows if int(r[0]) // 1000 + BAR <= now_s()}


def cmd_scorecard(args):
    """Claude's decisions vs the strategy's, marked to the 6h bar they applied to.
    Gross of fees (overrides that trade less also save fees - not counted)."""
    brief = "--brief" in args
    rows = _log_rows()
    for line in drawdown_guard():
        print(line)
    if not rows:
        print("scorecard: no v9 decisions logged yet")
        return
    fwd = {}
    for s in {r["sym"] for r in rows}:
        try:
            fwd[s] = _fwd_returns(s, min(r["ts"] for r in rows if r["sym"] == s) - BAR)
        except Exception as e:             # noqa: BLE001 - unknown symbol / network
            print(f"  (no prices for {s}: {e})")
    scored, by_act = [], {}
    for r in rows:
        bar = r["ts"] - r["ts"] % BAR                     # the close the run acted on
        ret = fwd.get(r["sym"], {}).get(bar)
        if ret is None:
            continue
        s_pnl, f_pnl = r["strat"] * ret, r["final"] * ret
        d = {**r, "ret": ret, "strat_pnl": s_pnl, "final_pnl": f_pnl, "edge": f_pnl - s_pnl}
        scored.append(d)
        a = by_act.setdefault(r["act"], {"n": 0, "edge": 0.0, "wins": 0})
        if abs(r["final"] - r["strat"]) > 1e-9:
            a["n"] += 1
            a["edge"] += d["edge"]
            a["wins"] += d["edge"] > 0
    strat = sum(d["strat_pnl"] for d in scored)
    final = sum(d["final_pnl"] for d in scored)
    runs = len({d["ts"] for d in scored})
    print(f"scored {len(scored)} decisions over {runs} runs (gross of fees):")
    print(f"  strategy alone ${strat:+.2f} | with Claude's decisions ${final:+.2f} | Claude's value-add ${final - strat:+.2f}")
    for act, a in sorted(by_act.items()):
        if a["n"]:
            print(f"  {act:13s} {a['n']:3d} changed decisions, value-add ${a['edge']:+.2f}, helped {a['wins']}/{a['n']}")
    mk = [r["maker"] for r in rows if r["maker"] is not None]
    if mk:
        print(f"  maker-fill share {100 * sum(mk) / len(mk):.0f}% over {len(mk)} filled order groups (backtest assumed 70%)")
    changed = [d for d in scored if abs(d["final"] - d["strat"]) > 1e-9]
    k = 3 if brief else 8
    if changed:
        print("  best overrides:")
        for d in sorted(changed, key=lambda x: -x["edge"])[:k]:
            print(f"    {utc(d['ts'])} {d['sym']} {d['act']} ${d['edge']:+.2f}  ({d['why'][:90]})")
        print("  worst overrides:")
        for d in sorted(changed, key=lambda x: x["edge"])[:k]:
            print(f"    {utc(d['ts'])} {d['sym']} {d['act']} ${d['edge']:+.2f}  ({d['why'][:90]})")
    if runs < 60:
        print(f"  NOTE: {runs} runs is too few to judge skill (60+ runs ~ 2 weeks is the minimum; months to be sure).")


def cmd_revalidate(_args):
    """Paper-trade the FROZEN strategy on the most recent live data (Binance 6h bars,
    cached 5-min ratio) with the lab simulator: is the edge still there?"""
    from lab import sim as S
    from lab.strategies import micro_crowd as MC
    p, m = build_panel()
    w = MC.weights(p, dict(MC.FROZEN, vol_target=VOL_TARGET), m)
    print(f"paper-trading the frozen strategy (vol {VOL_TARGET}, gross cap {GROSS_CAP}x, 70%-maker fee) on live data:")
    for days in (30, 60, 90):
        a = int(np.searchsorted(p.t, now_s() - days * 86400))
        if a < 240:
            print(f"  last {days}d: not enough ratio history yet")
            continue
        r = S.run_weights(S.slice_panel(p, a, len(p.t)), w[a:], fee=0.000305, max_gross_leverage=GROSS_CAP)
        x = r.metrics()
        print(f"  last {days:2d}d: return {x['total_return']:+.1%}  maxDD {x['max_drawdown']:.1%}  "
              f"trades/wk {x['trades_per_week']:.1f}")
    print("  lab reference (lockbox 2025-07..2026-09, this risk level): +54.5%/yr at the tested timing, "
          "~+22%/yr averaged over candle timings; a 90d paper return below about -25% is outside that range.")


COMMANDS = {"plan": cmd_plan, "execute": cmd_execute, "flatten-legacy": cmd_flatten_legacy, "status": cmd_status,
            "scorecard": cmd_scorecard, "revalidate": cmd_revalidate}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        B.die("usage: v9.py plan | execute [--dry] | flatten-legacy [--dry] | status | scorecard [--brief] | revalidate")
    COMMANDS[sys.argv[1]](sys.argv[2:])
