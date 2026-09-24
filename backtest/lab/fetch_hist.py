#!/usr/bin/env python3
"""Research-dataset downloader (PUBLIC market data only, no keys, no orders).

    python backtest/lab/fetch_hist.py all          # everything, resumable
    python backtest/lab/fetch_hist.py <stage>      # one stage

Stages, in dependency order:
    symbols   list every Binance USDT-M perp that EVER existed (S3 listing of
              data.binance.vision keeps delisted symbols) + fapi exchangeInfo
    k1d       1d klines for every symbol (monthly zips + daily zips for the
              current / not-yet-published month)
    gap1d     re-fetch DAILY zips for days missing inside a symbol's 1d history
              (some monthly zips are truncated, e.g. 2022-02 / 2022-04)
    universe  point-in-time trailing-30d quote-volume ranks (daily) and the
              download union (ever PIT top-60 since 2020 + majors)
    k1h       1h klines for the union
    gap1h     same gap re-fetch for the 1h klines of the union
    funding   funding-rate history for the union (monthly zips + public fapi
              for the current month, which the archive does not have yet)
    fundfill  public-fapi backfill of funding for live days the archive lacks
              (the archive keeps only a symbol's latest listing)
    metrics   5-min OI / long-short / taker metrics for the metrics majors
    bybit     Bybit v5 public instrument specs (linear + spot)
    build     parse raw zips -> compact per-symbol .npz under data/hist/
    all       every stage above in order

Raw zips are kept under data/hist/raw/ (same relative paths as the archive),
so a re-run only downloads what is missing (idempotent). Everything lives
under data/hist/, which is git-ignored.
"""
from __future__ import annotations

import datetime as _dt
import io
import json
import os
import re
import sys
import threading
import time
import urllib.parse
import zipfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HIST = os.path.join(ROOT, "data", "hist")
RAW = os.path.join(HIST, "raw")

S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
ARCH = "https://data.binance.vision/"
UM = "data/futures/um/"
FAPI = "https://fapi.binance.com"
BYBIT = "https://api.bybit.com"

START_MONTH = "2020-01"          # first month of 1h / funding history
UNION_TOPN = 60                  # union = ever in PIT top-60 (+ majors)
WORKERS = 16

# Long-lived large caps present on BOTH Binance USDT-M and Bybit linear.
MAJORS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT",
          "ADAUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", "TRXUSDT", "DOTUSDT",
          "BCHUSDT", "ETCUSDT", "XLMUSDT", "ATOMUSDT"]
METRIC_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
                  "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT",
                  "TRXUSDT", "DOTUSDT"]
# Not crypto beta: stablecoins and gold tokens (underlyingType COIN on Binance
# but they would pollute a volume-ranked crypto universe).  TradFi / index /
# commodity perps are excluded via exchangeInfo underlyingType != COIN.
EXCLUDE_EXTRA = {"USDCUSDT", "BUSDUSDT", "TUSDUSDT", "USDPUSDT", "FDUSDUSDT",
                 "USDEUSDT", "USD1USDT", "EURUSDT", "PAXGUSDT", "XAUTUSDT",
                 "BTCDOMUSDT", "DEFIUSDT", "BLUEBIRDUSDT", "FOOTBALLUSDT",
                 "ALLUSDT"}

KL_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
           "quote_volume", "count", "taker_buy_volume",
           "taker_buy_quote_volume", "ignore"]

_tl = threading.local()


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def sess() -> requests.Session:
    s = getattr(_tl, "s", None)
    if s is None:
        s = requests.Session()
        s.headers["User-Agent"] = "trading-bot-research/1.0"
        _tl.s = s
    return s


def http_get(url, params=None, tries=6, timeout=60):
    """GET with retries. Returns bytes, or None on 404."""
    last = None
    for k in range(tries):
        try:
            r = sess().get(url, params=params, timeout=timeout)
            if r.status_code == 404:
                return None
            if r.status_code in (418, 429):
                time.sleep(30 + 10 * k)
                continue
            r.raise_for_status()
            return r.content
        except Exception as e:  # noqa: BLE001 - network: retry everything
            last = e
            time.sleep(min(2 ** k, 30))
    raise RuntimeError(f"GET failed after {tries} tries: {url} ({last})")


def s3_list(prefix, delimiter=None):
    """List an S3 prefix of data.binance.vision -> (common_prefixes, keys)."""
    prefixes, keys, marker = [], [], ""
    while True:
        p = {"prefix": prefix, "marker": marker}
        if delimiter:
            p["delimiter"] = delimiter
        body = http_get(S3, params=p).decode("utf-8")
        prefixes += re.findall(r"<CommonPrefixes><Prefix>([^<]*)</Prefix>", body)
        keys += re.findall(r"<Key>([^<]*)</Key>", body)
        if "<IsTruncated>true</IsTruncated>" not in body:
            break
        m = re.search(r"<NextMarker>([^<]*)</NextMarker>", body)
        marker = m.group(1) if m else keys[-1]
    return [p for p in prefixes if p != prefix], keys


def raw_path(key):
    return os.path.join(RAW, *key[len(UM):].split("/"))


def download(key):
    """Download archive key to data/hist/raw (skip if present). -> 'ok'|'skip'|'404'."""
    dst = raw_path(key)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return "skip"
    data = http_get(ARCH + urllib.parse.quote(key))
    if data is None:
        return "404"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)
    return "ok"


def pmap(fn, items, label, workers=WORKERS):
    items = list(items)
    out, done, t0 = [], 0, time.time()
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(fn, items):
            out.append(r)
            done += 1
            if done % 500 == 0 or done == len(items):
                log(f"{label}: {done}/{len(items)} ({time.time() - t0:.0f}s)")
    return out


def jdump(obj, path):
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def jload(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def utc_now():
    return _dt.datetime.now(_dt.timezone.utc)


def month_str(d):
    return f"{d.year:04d}-{d.month:02d}"


def prev_month(ms):
    y, m = map(int, ms.split("-"))
    return f"{y - 1:04d}-12" if m == 1 else f"{y:04d}-{m - 1:02d}"


# --------------------------------------------------------------------------
# stage: symbols
# --------------------------------------------------------------------------
def stage_symbols():
    os.makedirs(HIST, exist_ok=True)
    seen = set()
    for kind in ("monthly", "daily"):
        pre = UM + f"{kind}/klines/"
        prefixes, _ = s3_list(pre, "/")
        for p in prefixes:
            seen.add(p[len(pre):].strip("/"))
    syms = sorted(s for s in seen if s.endswith("USDT") and "_" not in s
                  and not s.endswith("SETTLED"))
    ex = http_get(FAPI + "/fapi/v1/exchangeInfo")
    exi = json.loads(ex)
    info = {}
    for s in exi["symbols"]:
        info[s["symbol"]] = {k: s.get(k) for k in (
            "status", "contractType", "underlyingType", "underlyingSubType",
            "onboardDate", "deliveryDate", "baseAsset", "quoteAsset")}
    jdump(info, os.path.join(HIST, "binance_exchangeinfo.json"))
    excluded = sorted(s for s in syms if s in EXCLUDE_EXTRA or (
        s in info and info[s]["underlyingType"] not in (None, "COIN")))
    jdump({"symbols": syms, "excluded_from_pit": excluded,
           "listed_at_utc": utc_now().isoformat()},
          os.path.join(HIST, "symbols_all.json"))
    log(f"symbols: {len(syms)} USDT perps ever listed; "
        f"{len(excluded)} excluded from PIT ranking (non-crypto/stable/index)")


def load_symbols():
    return jload(os.path.join(HIST, "symbols_all.json"))


# --------------------------------------------------------------------------
# kline key discovery
# --------------------------------------------------------------------------
def kline_keys(sym, interval, start_month=None):
    """All monthly zips for sym/interval (>= start_month), plus daily zips for
    months after the last monthly file, limited to the current and previous
    month (older months are always published monthly)."""
    cur = month_str(utc_now())
    prv = prev_month(cur)
    _, keys = s3_list(UM + f"monthly/klines/{sym}/{interval}/")
    mk = [k for k in keys if k.endswith(".zip")]
    months = set()
    out = []
    for k in mk:
        m = k[-11:-4]
        if start_month and m < start_month:
            continue
        months.add(m)
        out.append(k)
    for m in (prv, cur):
        if m in months:
            continue
        _, dk = s3_list(UM + f"daily/klines/{sym}/{interval}/{sym}-{interval}-{m}")
        out += [k for k in dk if k.endswith(".zip")]
    return out


def fetch_klines(symbols, interval, start_month=None, label=""):
    lists = pmap(lambda s: kline_keys(s, interval, start_month), symbols,
                 f"list {interval}{label}")
    keys = [k for ks in lists for k in ks]
    res = pmap(download, keys, f"download {interval}{label}")
    log(f"{interval}: {len(keys)} files, new={res.count('ok')} "
        f"skip={res.count('skip')} 404={res.count('404')}")
    manifest = {s: ks for s, ks in zip(symbols, lists)}
    jdump(manifest, os.path.join(HIST, f"manifest_k{interval}.json"))


def stage_k1d():
    fetch_klines(load_symbols()["symbols"], "1d")


def fill_kline_gaps(symbols, interval):
    """Some MONTHLY archive zips are truncated (verified: ~48 symbols' 2022-02
    files end on Feb 25 and their 2022-04 files start on Apr 3, for both 1h
    and 1d), which left multi-day NaN holes while the coin was trading - they
    knocked the coins out of the PIT universe and forced exits in the sim.
    For every UTC day inside a symbol's history that has a missing bar, try
    the DAILY archive zip and add it to the manifest.  404s (real exchange
    absences: relist gaps, redenominations) are remembered and not retried."""
    mp = os.path.join(HIST, f"manifest_k{interval}.json")
    man = jload(mp)
    np404 = os.path.join(HIST, f"gap404_k{interval}.json")
    known404 = set(jload(np404)) if os.path.exists(np404) else set()
    dt = 3600 if interval == "1h" else 86400

    def want(sym):
        d = parse_klines(sym, interval)
        if d is None:
            return []
        miss = np.flatnonzero(~np.isfinite(d["c"]))
        days = sorted({time.strftime("%Y-%m-%d", time.gmtime(int(d["t0"]) + int(i) * dt))
                       for i in miss})
        have = set(man.get(sym, []))
        keys = [UM + f"daily/klines/{sym}/{interval}/{sym}-{interval}-{dd}.zip" for dd in days]
        return [k for k in keys if k not in have and k not in known404]
    lists = pmap(want, symbols, f"gap-scan {interval}", workers=8)
    keys = [k for ks in lists for k in ks]
    res = pmap(download, keys, f"gap-fill {interval}", workers=8) if keys else []
    added = 0
    for k, r in zip(keys, res):
        if r == "404":
            known404.add(k)
            continue
        sym = k[len(UM):].split("/")[2]       # daily/klines/<sym>/...
        man.setdefault(sym, []).append(k)
        added += 1
    jdump(man, mp)
    jdump(sorted(known404), np404)
    log(f"gap-fill {interval}: {len(keys)} candidate daily zips, added={added}, "
        f"404={res.count('404') if res else 0}")


def stage_gap1d():
    fill_kline_gaps(load_symbols()["symbols"], "1d")


def stage_gap1h():
    fill_kline_gaps(load_union(), "1h")


# --------------------------------------------------------------------------
# kline parsing
# --------------------------------------------------------------------------
def read_zip_csv(path, names):
    with zipfile.ZipFile(path) as z:
        raw = z.read(z.namelist()[0])
    if not raw.strip():
        return pd.DataFrame(columns=names)
    first = raw[:1]
    header = 0 if not (first.isdigit() or first == b"-") else None
    df = pd.read_csv(io.BytesIO(raw), header=header)
    if header is None:
        df.columns = names[: df.shape[1]]
    return df


def to_seconds(ts):
    """Binance timestamps: ms historically, us in some newer files."""
    ts = np.asarray(ts, dtype=np.int64)
    out = np.where(ts > 10 ** 14, ts // 1_000_000, ts // 1000)
    return out.astype(np.int64)


def parse_klines(sym, interval):
    man = jload(os.path.join(HIST, f"manifest_k{interval}.json"))
    keys = man.get(sym, [])
    frames = []
    for k in keys:
        p = raw_path(k)
        if not os.path.exists(p):
            continue
        df = read_zip_csv(p, KL_COLS)
        if len(df):
            frames.append(df[KL_COLS[:11]])
    if not frames:
        return None
    df = pd.concat(frames, ignore_index=True)
    t = to_seconds(df["open_time"].to_numpy())
    dt = 3600 if interval == "1h" else 86400
    ndup = int(len(t) - len(np.unique(t)))
    misal = int(np.sum(t % dt != 0))
    df = df.assign(t=t).drop_duplicates("t", keep="last").sort_values("t")
    df = df[df["t"] % dt == 0]
    t = df["t"].to_numpy(np.int64)
    t0, t1 = int(t[0]), int(t[-1])
    L = (t1 - t0) // dt + 1
    idx = (t - t0) // dt
    out = {"t0": np.int64(t0), "dt": np.int64(dt)}
    for name, col in (("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"),
                      ("v", "volume"), ("qv", "quote_volume"),
                      ("tbqv", "taker_buy_quote_volume"), ("n", "count")):
        a = np.full(L, np.nan)
        a[idx] = pd.to_numeric(df[col], errors="coerce").to_numpy(np.float64)
        out[name] = a
    out["n_dup_raw"] = np.int64(ndup)
    out["n_misaligned_raw"] = np.int64(misal)
    return out


def save_npz(path, d):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part.npz"
    np.savez_compressed(tmp, **d)
    os.replace(tmp, path)


def fname(sym):
    return sym + ".npz"


# --------------------------------------------------------------------------
# stage: universe (PIT ranks from daily bars)
# --------------------------------------------------------------------------
def build_k1d_store():
    syms = load_symbols()["symbols"]

    def one(s):
        d = parse_klines(s, "1d")
        if d is not None:
            save_npz(os.path.join(HIST, "k1d", fname(s)), d)
        return s if d is not None else None
    got = [s for s in pmap(one, syms, "parse 1d", workers=8) if s]
    log(f"k1d store: {len(got)} symbols with daily bars")
    return got


def stage_universe():
    info = load_symbols()
    syms = build_k1d_store()
    excl = set(info["excluded_from_pit"])
    per = {}
    for s in syms:
        z = np.load(os.path.join(HIST, "k1d", fname(s)))
        per[s] = (int(z["t0"]), z["qv"], z["v"])
    day0 = min(v[0] for v in per.values())
    day1 = max(v[0] + (len(v[1]) - 1) * 86400 for v in per.values())
    D = (day1 - day0) // 86400 + 1
    qv = np.zeros((D, len(syms)))
    traded = np.zeros((D, len(syms)), bool)
    for j, s in enumerate(syms):
        t0, q, v = per[s]
        i0 = (t0 - day0) // 86400
        q = np.where(np.isfinite(q), q, 0.0)
        qv[i0:i0 + len(q), j] = q
        traded[i0:i0 + len(q), j] = np.isfinite(v) & (v > 0)
    # S[d] = sum of qv over days d-30 .. d-1 (ends the day BEFORE d)
    cs = np.vstack([np.zeros((1, len(syms))), np.cumsum(qv, axis=0)])
    d_idx = np.arange(D)
    lo = np.maximum(d_idx - 30, 0)
    S = cs[d_idx] - cs[lo]                      # rows: days d-30..d-1
    prev_traded = np.zeros_like(traded)
    prev_traded[1:] = traded[:-1]               # must have traded on day d-1
    elig = prev_traded & (S > 0)
    elig[:, [j for j, s in enumerate(syms) if s in excl]] = False
    key = np.where(elig, S, -1.0)
    order = np.argsort(-key, axis=1, kind="stable")
    rank = np.full((D, len(syms)), -1, np.int16)
    rows = np.repeat(d_idx[:, None], len(syms), 1)
    rank[rows, order] = np.arange(len(syms), dtype=np.int16)[None, :]
    rank[~elig] = -1
    save_npz(os.path.join(HIST, "universe_pit.npz"), {
        "day0": np.int64(day0), "symbols": np.array(syms),
        "qv30": S.astype(np.float64), "rank": rank})
    # download union: ever in PIT top-N on or after START_MONTH, plus majors
    start = int(pd.Timestamp(START_MONTH + "-01", tz="UTC").timestamp())
    di = max(0, (start - day0) // 86400)
    ever = (rank[di:] >= 0) & (rank[di:] < UNION_TOPN)
    union = sorted(set(np.array(syms)[ever.any(axis=0)]) | set(MAJORS))
    jdump({"union": union, "topn": UNION_TOPN, "since": START_MONTH},
          os.path.join(HIST, "union.json"))
    log(f"universe: {D} days x {len(syms)} symbols; union={len(union)}")


def load_union():
    return jload(os.path.join(HIST, "union.json"))["union"]


# --------------------------------------------------------------------------
# stage: k1h, funding, metrics
# --------------------------------------------------------------------------
def stage_k1h():
    fetch_klines(load_union(), "1h", START_MONTH)


FUND_COLS = ["calc_time", "funding_interval_hours", "last_funding_rate"]


def funding_keys(sym):
    _, keys = s3_list(UM + f"monthly/fundingRate/{sym}/")
    return [k for k in keys if k.endswith(".zip") and k[-11:-4] >= START_MONTH]


def fapi_funding(sym, since_ms):
    """Current-month funding from public fapi (archive lags a month)."""
    rows, st = [], since_ms
    for _ in range(20):
        body = http_get(FAPI + "/fapi/v1/fundingRate",
                        params={"symbol": sym, "startTime": st, "limit": 1000})
        if body is None:
            break
        arr = json.loads(body)
        if not isinstance(arr, list) or not arr:
            break
        rows += [[int(a["fundingTime"]), float(a["fundingRate"])] for a in arr]
        if len(arr) < 1000:
            break
        st = int(arr[-1]["fundingTime"]) + 1
        time.sleep(0.2)
    return rows


def stage_funding():
    union = load_union()
    lists = pmap(funding_keys, union, "list funding")
    keys = [k for ks in lists for k in ks]
    res = pmap(download, keys, "download funding")
    log(f"funding: {len(keys)} files, new={res.count('ok')} 404={res.count('404')}")
    jdump({s: ks for s, ks in zip(union, lists)},
          os.path.join(HIST, "manifest_funding.json"))
    # current / unpublished months from fapi, for symbols still trading
    info = jload(os.path.join(HIST, "binance_exchangeinfo.json"))
    tail = {}

    def one(sym):
        ks = [k for k in lists[union.index(sym)]]
        last = max((k[-11:-4] for k in ks), default=None)
        if info.get(sym, {}).get("status") != "TRADING":
            return sym, None
        if last is None:
            since = pd.Timestamp(START_MONTH + "-01", tz="UTC")
        else:
            y, m = map(int, last.split("-"))
            since = pd.Timestamp(year=y + (m == 12), month=m % 12 + 1, day=1, tz="UTC")
        return sym, fapi_funding(sym, int(since.timestamp() * 1000))
    for sym, rows in pmap(one, union, "fapi funding tail", workers=4):
        if rows:
            tail[sym] = rows
    jdump(tail, os.path.join(HIST, "funding_fapi_tail.json"))
    log(f"funding tail from fapi: {len(tail)} symbols")


MET_COLS = ["create_time", "symbol", "sum_open_interest", "sum_open_interest_value",
            "count_toptrader_long_short_ratio", "sum_toptrader_long_short_ratio",
            "count_long_short_ratio", "sum_taker_long_short_vol_ratio"]


def stage_metrics():
    lists = pmap(lambda s: [k for k in s3_list(UM + f"daily/metrics/{s}/")[1]
                            if k.endswith(".zip")], METRIC_SYMBOLS, "list metrics",
                 workers=12)
    keys = [k for ks in lists for k in ks]
    res = pmap(download, keys, "download metrics")
    log(f"metrics: {len(keys)} files, new={res.count('ok')} 404={res.count('404')}")
    jdump({s: ks for s, ks in zip(METRIC_SYMBOLS, lists)},
          os.path.join(HIST, "manifest_metrics.json"))


# --------------------------------------------------------------------------
# stage: bybit instruments
# --------------------------------------------------------------------------
def bybit_all(category):
    out, cursor = [], ""
    for _ in range(50):
        p = {"category": category, "limit": 1000}
        if cursor:
            p["cursor"] = cursor
        j = json.loads(http_get(BYBIT + "/v5/market/instruments-info", params=p))
        if j.get("retCode") != 0:
            raise RuntimeError(f"bybit {category}: {j.get('retMsg')}")
        out += j["result"]["list"]
        cursor = j["result"].get("nextPageCursor") or ""
        if not cursor:
            break
    return out


def stage_bybit():
    lin = bybit_all("linear")
    spot = bybit_all("spot")
    spot_ok = {s["symbol"] for s in spot if s.get("status") == "Trading"}
    out = {}
    for s in lin:
        if s.get("contractType") != "LinearPerpetual" or s.get("settleCoin") != "USDT":
            continue
        lf, pf, lev = s.get("lotSizeFilter", {}), s.get("priceFilter", {}), s.get("leverageFilter", {})
        out[s["symbol"]] = {
            "minOrderQty": float(lf.get("minOrderQty", "nan")),
            "qtyStep": float(lf.get("qtyStep", "nan")),
            "minNotionalValue": float(lf.get("minNotionalValue", "nan") or "nan"),
            "tickSize": float(pf.get("tickSize", "nan")),
            "maxLeverage": float(lev.get("maxLeverage", "nan")),
            "has_spot": s["symbol"] in spot_ok,
            "status": s.get("status"),
            "launchTime": int(s.get("launchTime") or 0) // 1000,
            "fundingInterval_min": int(s.get("fundingInterval") or 0),
        }
    jdump({"fetched_at_utc": utc_now().isoformat(), "instruments": out},
          os.path.join(HIST, "bybit_instruments.json"))
    log(f"bybit: {len(out)} USDT linear perps, {sum(v['has_spot'] for v in out.values())} with spot")


# --------------------------------------------------------------------------
# stage: build (1h store, funding store, metrics store)
# --------------------------------------------------------------------------
def build_k1h():
    union = load_union()

    def one(s):
        d = parse_klines(s, "1h")
        if d is not None:
            save_npz(os.path.join(HIST, "k1h", fname(s)), d)
        return s if d is not None else None
    got = [s for s in pmap(one, union, "parse 1h", workers=8) if s]
    log(f"k1h store: {len(got)}/{len(union)} symbols")


def _funding_archive_rows(keys):
    ts, rt, iv = [], [], []
    for k in keys:
        p = raw_path(k)
        if not os.path.exists(p):
            continue
        df = read_zip_csv(p, FUND_COLS)
        if not len(df):
            continue
        if "last_funding_rate" not in df.columns:
            if df.shape[1] != 2:
                raise ValueError(f"unexpected funding layout {p}: {list(df.columns)}")
            df.columns = ["calc_time", "last_funding_rate"]
        ts.append(to_seconds(df["calc_time"].to_numpy()))
        rt.append(pd.to_numeric(df["last_funding_rate"], errors="coerce").to_numpy(np.float64))
        if "funding_interval_hours" in df:
            iv.append(pd.to_numeric(df["funding_interval_hours"], errors="coerce").to_numpy(np.float64))
        else:
            iv.append(np.full(len(df), np.nan))
    return ts, rt, iv


def stage_fundfill():
    """The monthly fundingRate archive only holds a symbol's LATEST listing
    (verified: ICPUSDT 2021-05..2022-08, TLMUSDT 2021-07..2023-02, BNXUSDT
    2022-04..2023-01 and QTUMUSDT 2020-02 are absent although the coins traded
    and public fapi still serves those rates, matching the archive exactly
    where both exist).  For every union symbol, find live daily bars (k1d,
    volume > 0) on which no funding settled, and backfill those windows from
    public /fapi/v1/fundingRate.  Result: data/hist/funding_fapi_backfill.json
    (merged by build_funding)."""
    man = jload(os.path.join(HIST, "manifest_funding.json"))
    outp = os.path.join(HIST, "funding_fapi_backfill.json")
    out = jload(outp) if os.path.exists(outp) else {}
    tailp = os.path.join(HIST, "funding_fapi_tail.json")
    tail = jload(tailp) if os.path.exists(tailp) else {}
    start = int(pd.Timestamp(START_MONTH + "-01", tz="UTC").timestamp())

    def windows(sym):
        kp = os.path.join(HIST, "k1d", fname(sym))
        if not os.path.exists(kp):
            return sym, []
        with np.load(kp) as z:
            t0, v = int(z["t0"]), z["v"]
        days = t0 + 86400 * np.arange(len(v))
        live = np.isfinite(v) & (v > 0) & (days >= start)
        lv = np.flatnonzero(live)
        if len(lv):                      # partial listing / delisting days may
            live[lv[0]] = live[lv[-1]] = False   # legitimately have no settlement
        ts, _, _ = _funding_archive_rows(man.get(sym, []))
        ts = np.concatenate(ts) if ts else np.zeros(0, np.int64)
        extra = [np.asarray([r[0] for r in tail.get(sym, []) + out.get(sym, [])], np.int64) // 1000]
        ts = np.concatenate([ts] + extra)
        di = np.unique((ts - t0) // 86400)
        has = np.zeros(len(v), bool)
        di = di[(di >= 0) & (di < len(v))]
        has[di] = True
        miss = np.flatnonzero(live & ~has)
        if not len(miss):
            return sym, []
        # contiguous runs of missing live days -> [start, end) windows
        br = np.flatnonzero(np.diff(miss) > 1)
        a = np.r_[miss[0], miss[br + 1]]
        b = np.r_[miss[br], miss[-1]] + 1
        return sym, [(int(days[x]), int(days[y - 1]) + 86400) for x, y in zip(a, b)]
    wins = [w for w in pmap(windows, list(man), "funding coverage", workers=8) if w[1]]
    n = 0
    for sym, ws in wins:
        rows = []
        for a, b in ws:
            st = a * 1000
            for _ in range(50):
                body = http_get(FAPI + "/fapi/v1/fundingRate",
                                params={"symbol": sym, "startTime": st,
                                        "endTime": b * 1000, "limit": 1000})
                arr = json.loads(body) if body else []
                if not isinstance(arr, list) or not arr:
                    break
                rows += [[int(x["fundingTime"]), float(x["fundingRate"])] for x in arr]
                if len(arr) < 1000:
                    break
                st = int(arr[-1]["fundingTime"]) + 1
                time.sleep(0.2)
        log(f"fundfill {sym}: {len(ws)} window(s) "
            f"{[time.strftime('%Y-%m-%d', time.gmtime(a)) for a, _ in ws][:4]} -> {len(rows)} rates")
        if rows:
            out[sym] = sorted({r[0]: r for r in out.get(sym, []) + rows}.values())
            n += 1
    jdump(out, outp)
    log(f"fundfill: {len(wins)} symbols had live days without funding; backfilled {n}")


def build_funding():
    man = jload(os.path.join(HIST, "manifest_funding.json"))
    tailp = os.path.join(HIST, "funding_fapi_tail.json")
    tail = jload(tailp) if os.path.exists(tailp) else {}
    bfp = os.path.join(HIST, "funding_fapi_backfill.json")
    backfill = jload(bfp) if os.path.exists(bfp) else {}
    n = 0
    for sym, keys in man.items():
        ts, rt, iv = _funding_archive_rows(keys)
        for src in (tail, backfill):
            if sym in src and len(src[sym]):
                a = np.asarray(src[sym], dtype=np.float64)
                ts.append(to_seconds(a[:, 0].astype(np.int64)))
                rt.append(a[:, 1])
                iv.append(np.full(len(a), np.nan))
        if not ts:
            continue
        ts = np.concatenate(ts)
        ts_raw = ts.copy()
        ts = ((ts + 30) // 60) * 60          # settlement stamps carry ms jitter
        rt, iv = np.concatenate(rt), np.concatenate(iv)
        order = np.argsort(ts, kind="stable")
        ts, rt, iv, ts_raw = ts[order], rt[order], iv[order], ts_raw[order]
        keep = np.ones(len(ts), bool)
        keep[:-1] = ts[1:] != ts[:-1]        # dedupe (archive + fapi overlap)
        ts, rt, iv, ts_raw = ts[keep], rt[keep], iv[keep], ts_raw[keep]
        ok = np.isfinite(rt)
        save_npz(os.path.join(HIST, "funding", fname(sym)),
                 {"ts": ts[ok], "rate": rt[ok], "interval_h": iv[ok],
                  "max_jitter_s": np.int64(np.max(np.abs(ts_raw - ts)) if len(ts) else 0)})
        n += 1
    log(f"funding store: {n} symbols")


def build_metrics():
    man = jload(os.path.join(HIST, "manifest_metrics.json"))
    for sym, keys in man.items():
        frames = []
        for k in keys:
            p = raw_path(k)
            if os.path.exists(p):
                df = read_zip_csv(p, MET_COLS)
                if len(df):
                    frames.append(df)
        if not frames:
            continue
        df = pd.concat(frames, ignore_index=True)
        ct = df["create_time"]
        # pandas 3 string columns carry an extension dtype np.issubdtype rejects
        if pd.api.types.is_numeric_dtype(ct):
            ts = to_seconds(ct.to_numpy())
        else:
            # pandas 3 parses to datetime64[us]; never assume ns resolution
            ts = ((pd.to_datetime(ct, utc=True) - pd.Timestamp("1970-01-01", tz="UTC"))
                  // pd.Timedelta(seconds=1)).to_numpy(np.int64)
        df = df.assign(ts=ts).drop_duplicates("ts", keep="last").sort_values("ts")
        g = lambda c: pd.to_numeric(df[c], errors="coerce").to_numpy(np.float64)
        save_npz(os.path.join(HIST, "metrics", fname(sym)), {
            "ts": df["ts"].to_numpy(np.int64),
            "oi_value": g("sum_open_interest_value"),
            "ls_ratio": g("count_long_short_ratio"),
            "top_ls_ratio": g("sum_toptrader_long_short_ratio"),
            "top_ls_acct_ratio": g("count_toptrader_long_short_ratio"),
            "taker_ratio": g("sum_taker_long_short_vol_ratio")})
    log(f"metrics store: {len(man)} symbols")


def stage_build():
    build_k1h()
    build_funding()
    build_metrics()
    cache = os.path.join(HIST, "cache")
    if os.path.isdir(cache):             # stale resample/panel caches
        for root, _, files in os.walk(cache):
            for f in files:
                os.remove(os.path.join(root, f))
    log("build done (panel caches cleared)")


STAGES = {"symbols": stage_symbols, "k1d": stage_k1d, "gap1d": stage_gap1d,
          "universe": stage_universe, "k1h": stage_k1h, "gap1h": stage_gap1h,
          "funding": stage_funding, "fundfill": stage_fundfill,
          "metrics": stage_metrics, "bybit": stage_bybit, "build": stage_build}


def main(argv):
    names = argv[1:] or ["all"]
    if names == ["all"]:
        names = list(STAGES)
    for n in names:
        if n not in STAGES:
            sys.exit(f"unknown stage {n}; choose from {list(STAGES)} or all")
        t = time.time()
        log(f"== stage {n}")
        STAGES[n]()
        log(f"== stage {n} done in {time.time() - t:.0f}s")


if __name__ == "__main__":
    main(sys.argv)
