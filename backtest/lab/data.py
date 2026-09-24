"""Research-dataset loader (read-only; build the data with fetch_hist.py).

Interface (shared with the harness - keep EXACTLY):

    Panel(t, dt, symbols, o, h, l, c, v, qv, funding, tradable, meta)
    load_panel(timeframe="1h"|"4h"|"6h"|"1d", symbols=None, universe=None,
               start=None, end=None) -> Panel
    load_bybit_instruments() -> {symbol: {"minOrderQty", "qtyStep",
               "minNotionalValue", "tickSize", "maxLeverage", "has_spot", ...}}
    load_metrics(symbols, timeframe, start=None, end=None)
               -> {"oi_value"|"ls_ratio"|"top_ls_ratio"|"taker_ratio": [T,N]}

Conventions
  * t = bar OPEN time, epoch seconds UTC, regular spacing dt.  The grid depends
    ONLY on (timeframe, start, end) - never on the symbol list - so panels and
    metrics built with the same arguments align row for row.
    Default start 2020-01-01 00:00 UTC; default end = end of the last bar in
    the 1h store.  Rows are t with start <= t < end (start floored to dt).
  * o/h/l/c/v/qv: NaN where the symbol has no bar (not listed yet, delisted,
    exchange gap).  Zero-volume bars keep their (flat) prices but are not
    "valid".
  * DEAD periods: a run of >= DEAD_RUN_H consecutive zero-volume 1h bars is
    a delisted / suspended contract (the Binance archive keeps printing flat,
    zero-volume klines for SETTLING symbols until today, and during relist
    gaps).  Those bars are set to NaN like any other "no data" bar, so
    delisted coins really END at delisting.  Short zero-volume runs (1-2 h
    exchange-wide halts, e.g. 2024-10-28 20:00) are kept, flat and not valid.
  * meta["relisted"] [T,N] bool: True on the first bar with data after a gap
    (NaN or dead) of >= DEAD_RUN_H hours.  The symbol may be a DIFFERENT
    token (LITUSDT 2025-12, PUMPUSDT 2025-07) or redenominated (BNXUSDT
    2023-02, price /55): never compute a return or indicator across it.
  * valid bar := finite o,h,l,c and v > 0.  meta["valid"] holds it separately
    from tradable so a harness can still mark-to-market / exit a position after
    the coin drops out of the universe.
  * funding[i] = SUM of funding rates whose settlement time is in
    (t[i], t[i]+dt]  (settled during the bar, at or before its close).
    Positive = longs pay shorts.  0.0 where none.
  * tradable = valid & member-of-universe-at-t[i].  PIT membership for day D
    uses trailing-30d quote volume of complete daily bars D-30..D-1 (strictly
    before t[i]), requires the coin to have traded on D-1, and excludes
    non-crypto perps (TradFi equities/commodities/FX/pre-IPO, index perps,
    stablecoins, gold tokens).  Membership is re-ranked DAILY.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import time
import warnings
from dataclasses import dataclass, field

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HIST = os.path.join(ROOT, "data", "hist")
CACHE = os.path.join(HIST, "cache")

DT = {"1h": 3600, "4h": 14400, "6h": 21600, "1d": 86400}
DEFAULT_START = 1577836800  # 2020-01-01 00:00 UTC

MAJORS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT",
          "ADAUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", "TRXUSDT", "DOTUSDT",
          "BCHUSDT", "ETCUSDT", "XLMUSDT", "ATOMUSDT"]

# Binance 5-min metrics stamps changed convention over time (re-verified
# against 5m klines, taker buy/sell ratio): in 2021-06 and 2024-03 the row
# stamped ts describes the 5m period ENDING at ts (corr 1.000 vs ~0.03 for
# the period starting at ts); in 2026-09 it describes the period STARTING at
# ts (corr 0.9998).  Treating every row as knowable only at ts + 300 s is
# exact for the latter and 5 min conservative for the former - never early.
METRIC_AVAIL_LAG = 300
METRIC_FIELDS = ("oi_value", "ls_ratio", "top_ls_ratio", "taker_ratio")

_PRICE = ("o", "h", "l", "c", "v", "qv", "tbqv")
DEAD_RUN_H = 24   # >= this many consecutive zero-volume hours = dead contract
_CACHE_FIELDS = ("relist", "n_hours")   # a cache file without these is stale


@dataclass
class Panel:
    t: np.ndarray
    dt: int
    symbols: list
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    v: np.ndarray
    qv: np.ndarray
    funding: np.ndarray
    tradable: np.ndarray
    meta: dict = field(default_factory=dict)

    def col(self, sym):
        return self.symbols.index(sym)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _to_epoch(x):
    if x is None:
        return None
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return int(x)
    if isinstance(x, _dt.datetime):
        if x.tzinfo is None:
            x = x.replace(tzinfo=_dt.timezone.utc)
        return int(x.timestamp())
    if isinstance(x, _dt.date):
        return int(_dt.datetime(x.year, x.month, x.day, tzinfo=_dt.timezone.utc).timestamp())
    if hasattr(x, "timestamp"):          # pandas Timestamp
        ts = x if getattr(x, "tzinfo", None) else x.tz_localize("UTC")
        return int(ts.timestamp())
    if isinstance(x, str):
        s = x.strip().replace("Z", "+00:00")
        d = _dt.datetime.fromisoformat(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=_dt.timezone.utc)
        return int(d.timestamp())
    raise TypeError(f"cannot interpret time {x!r}")


def _jload(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _need(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} missing - run: python backtest/lab/fetch_hist.py all")
    return path


def _k1h_symbols():
    d = os.path.join(HIST, "k1h")
    if not os.path.isdir(d):
        raise FileNotFoundError(f"{d} missing - run fetch_hist.py all")
    return sorted(f[:-4] for f in os.listdir(d) if f.endswith(".npz"))


def _store_end():
    """End (exclusive) of the last 1h bar in the whole store. Cached."""
    p = os.path.join(CACHE, "store_meta.json")
    if os.path.exists(p):
        m = _jload(p)
        return int(m["end"])
    end = 0
    for s in _k1h_symbols():
        with np.load(os.path.join(HIST, "k1h", s + ".npz")) as z:
            end = max(end, int(z["t0"]) + len(z["c"]) * 3600)
    os.makedirs(CACHE, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"end": end}, f)
    return end


def _grid(timeframe, start, end):
    if timeframe not in DT:
        raise ValueError(f"timeframe must be one of {list(DT)}")
    dt = DT[timeframe]
    s = _to_epoch(start)
    s = DEFAULT_START if s is None else s
    s -= s % dt
    e = _to_epoch(end)
    store_end = _store_end()
    e = store_end if e is None else min(e, store_end)
    if e <= s:
        raise ValueError("empty time range")
    n = (e - s + dt - 1) // dt
    t = s + dt * np.arange(n, dtype=np.int64)
    # only complete bars: the last bar must close by the end of the 1h store
    t = t[t + dt <= store_end]
    return t, dt


def _runs(mask):
    """-> (starts, ends) of True runs in a 1-D bool array (ends exclusive)."""
    m = np.concatenate([[False], mask, [False]])
    dm = np.diff(m.astype(np.int8))
    return np.flatnonzero(dm == 1), np.flatnonzero(dm == -1)


def _clean_1h(d):
    """NaN-out dead (long zero-volume) runs and flag relistings, on the 1h
    grid of one symbol.  Mutates and returns d (adds d["relist"])."""
    for f in _PRICE:
        d[f] = np.array(d[f], dtype=np.float64)       # own copy
    v = d["v"]
    zero = np.isfinite(d["c"]) & (np.nan_to_num(v) <= 0)
    a, b = _runs(zero)
    for x, y in zip(a, b):
        if y - x >= DEAD_RUN_H:
            for f in _PRICE:
                d[f][x:y] = np.nan
    fin = np.isfinite(d["c"])
    relist = np.zeros(len(fin), bool)
    a, b = _runs(~fin)
    for x, y in zip(a, b):
        if x > 0 and y < len(fin) and y - x >= DEAD_RUN_H:
            relist[y] = True
    d["relist"] = relist
    return d


def _resample(d, k):
    """Resample a dense per-symbol 1h dict to k-hour UTC-aligned bars."""
    t0 = int(d["t0"])
    step = 3600 * k
    a0 = t0 - (t0 % step)
    pad = (t0 - a0) // 3600
    L = len(d["c"])
    G = -(-(pad + L) // k)
    tail = G * k - (pad + L)

    def P(x):
        return np.concatenate([np.full(pad, np.nan), np.asarray(x, np.float64),
                               np.full(tail, np.nan)]).reshape(G, k)
    o, h, l, c = P(d["o"]), P(d["h"]), P(d["l"]), P(d["c"])
    fin = np.isfinite(o) & np.isfinite(h) & np.isfinite(l) & np.isfinite(c)
    anyf = fin.any(axis=1)
    r = np.arange(G)
    first = np.argmax(fin, axis=1)
    last = k - 1 - np.argmax(fin[:, ::-1], axis=1)
    out = {"t0": np.int64(a0), "dt": np.int64(step)}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        out["o"] = np.where(anyf, o[r, first], np.nan)
        out["c"] = np.where(anyf, c[r, last], np.nan)
        out["h"] = np.where(anyf, np.nanmax(np.where(fin, h, np.nan), axis=1), np.nan)
        out["l"] = np.where(anyf, np.nanmin(np.where(fin, l, np.nan), axis=1), np.nan)
        for f in ("v", "qv", "tbqv"):
            x = P(d[f])
            out[f] = np.where(anyf, np.nansum(np.where(fin, x, np.nan), axis=1), np.nan)
    out["n_hours"] = fin.sum(axis=1).astype(np.int8)
    rl = np.concatenate([np.zeros(pad, bool), np.asarray(d["relist"], bool),
                         np.zeros(tail, bool)]).reshape(G, k)
    out["relist"] = rl.any(axis=1)
    return out


def _sym_bars(sym, timeframe):
    """Per-symbol bars on their own dense grid (1h raw or cached resample)."""
    src = _need(os.path.join(HIST, "k1h", sym + ".npz"))
    if timeframe == "1h":
        with np.load(src) as z:
            return _clean_1h({k: z[k] for k in ("t0", "dt") + _PRICE})
    cp = os.path.join(CACHE, timeframe, sym + ".npz")
    if os.path.exists(cp) and os.path.getmtime(cp) >= os.path.getmtime(src):
        with np.load(cp) as z:
            if all(f in z.files for f in _CACHE_FIELDS):
                return {k: z[k] for k in z.files}
    with np.load(src) as z:
        d = _clean_1h({k: z[k] for k in ("t0", "dt") + _PRICE})
    out = _resample(d, DT[timeframe] // 3600)
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    tmp = cp + ".part.npz"
    np.savez(tmp, **out)                  # uncompressed: faster reloads
    os.replace(tmp, cp)
    return out


_UNI = None


def _universe():
    global _UNI
    if _UNI is None:
        with np.load(_need(os.path.join(HIST, "universe_pit.npz"))) as z:
            _UNI = {"day0": int(z["day0"]), "symbols": [str(s) for s in z["symbols"]],
                    "rank": z["rank"], "qv30": z["qv30"]}
    return _UNI


def _pit_members(t, topn):
    """-> (symbols ever member in grid, bool [T, len(symbols)] membership)."""
    U = _universe()
    di = (t - U["day0"]) // 86400
    D = U["rank"].shape[0]
    days, inv = np.unique(di, return_inverse=True)
    rk = np.full((len(days), len(U["symbols"])), -1, np.int16)
    okd = (days >= 0) & (days < D)       # outside the table -> not a member
    rk[okd] = U["rank"][days[okd]]
    mem_day = (rk >= 0) & (rk < topn)
    ever = mem_day.any(axis=0)
    syms = [s for s, e in zip(U["symbols"], ever) if e]
    return syms, mem_day[:, ever][inv]


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------
def load_panel(timeframe="1h", symbols=None, universe=None, start=None, end=None,
               with_taker=False) -> Panel:
    """Build a [T,N] panel.  See module docstring for semantics.

    universe: None (exactly `symbols`), "majors", "pit_top20", "pit_top50",
    any "pit_topK" with K <= 60 (the download union covers ever-top-60), "all".
    If both `symbols` and `universe` are given, columns = the given symbols and
    tradable additionally requires universe membership.
    with_taker=True adds meta["tbqv"] (taker-BUY quote volume, [T,N]).
    """
    tt = time.time()
    t, dt = _grid(timeframe, start, end)
    T = len(t)
    have = set(_k1h_symbols())
    member = None
    missing = []
    if universe is None:
        if symbols is None:
            raise ValueError("give symbols=[...] or a universe")
        cols = list(dict.fromkeys(symbols))
    elif universe == "majors":
        cols = [s for s in MAJORS if s in have] if symbols is None else list(symbols)
        member = np.isin(np.array(cols), MAJORS)[None, :].repeat(T, 0)
    elif universe == "all":
        cols = sorted(have) if symbols is None else list(symbols)
        member = np.ones((T, len(cols)), bool)
        if symbols is None:
            # the 1h store is the download union = coins that were EVER in the
            # PIT top-60, i.e. selected with knowledge of the future.
            warnings.warn("universe='all' is the ever-top-60 download union: "
                          "column selection uses FUTURE volume (survivor/hindsight "
                          "bias).  Use a pit_topK universe for any backtest.",
                          stacklevel=2)
    else:
        m = re.fullmatch(r"pit_top(\d+)", str(universe))
        if not m:
            raise ValueError(f"unknown universe {universe!r}")
        topn = int(m.group(1))
        if topn > 60:
            raise ValueError("pit universes are only complete up to top-60 "
                             "(download union); raise UNION_TOPN and re-fetch")
        usyms, umem = _pit_members(t, topn)
        if symbols is None:
            cols = usyms
            member = umem
        else:
            cols = list(symbols)
            member = np.zeros((T, len(cols)), bool)
            for j, s in enumerate(cols):
                if s in usyms:
                    member[:, j] = umem[:, usyms.index(s)]
    N = len(cols)
    arr = {f: np.full((T, N), np.nan) for f in _PRICE}
    nh = np.zeros((T, N), np.int8) if timeframe != "1h" else None
    relisted = np.zeros((T, N), bool)
    for j, s in enumerate(cols):
        if s not in have:
            missing.append(s)
            continue
        d = _sym_bars(s, timeframe)
        t0 = int(d["t0"])
        L = len(d["c"])
        # overlap of symbol grid [t0, t0+L*dt) with panel grid
        i0 = (t0 - int(t[0])) // dt if T else 0
        a = max(0, i0)
        b = min(T, i0 + L)
        if b <= a:
            continue
        sa, sb = a - i0, b - i0
        for f in _PRICE:
            arr[f][a:b, j] = d[f][sa:sb]
        if nh is not None:
            nh[a:b, j] = d["n_hours"][sa:sb]
        relisted[a:b, j] = d["relist"][sa:sb]
    valid = (np.isfinite(arr["o"]) & np.isfinite(arr["h"]) & np.isfinite(arr["l"])
             & np.isfinite(arr["c"]) & (np.nan_to_num(arr["v"]) > 0))
    funding = np.zeros((T, N))
    if T:
        lo, hi = int(t[0]), int(t[-1]) + dt
        for j, s in enumerate(cols):
            p = os.path.join(HIST, "funding", s + ".npz")
            if not os.path.exists(p):
                continue
            with np.load(p) as z:
                ts, rt = z["ts"], z["rate"]
            k = (ts > lo) & (ts <= hi)
            if k.any():
                i = (ts[k] - lo - 1) // dt       # bar with t < ts <= t+dt
                np.add.at(funding[:, j], i, rt[k])
    tradable = valid if member is None else (valid & member)
    meta = {
        "timeframe": timeframe, "universe": universe, "source": "binance-usdm",
        "valid": valid, "member": member, "missing_symbols": missing,
        "relisted": relisted,
        "selection_lookahead": bool(universe == "all" and symbols is None),
        "hist_dir": HIST, "build_seconds": round(time.time() - tt, 2),
        "notes": "t=bar open (s UTC); funding summed over (t,t+dt]; "
                 "tradable=valid&PIT member (membership from data before t)",
    }
    if nh is not None:
        meta["n_hours"] = nh            # 1h bars present in each 4h/1d bar
    if with_taker:
        meta["tbqv"] = arr["tbqv"]
    return Panel(t=t, dt=int(dt), symbols=cols, o=arr["o"], h=arr["h"], l=arr["l"],
                 c=arr["c"], v=arr["v"], qv=arr["qv"], funding=funding,
                 tradable=tradable, meta=meta)


def load_bybit_instruments():
    d = _jload(_need(os.path.join(HIST, "bybit_instruments.json")))
    return d["instruments"]


def load_metrics(symbols, timeframe, start=None, end=None, max_stale=None):
    """[T,N] arrays aligned to load_panel(timeframe, start=, end=).t.

    Value at bar i = last observation KNOWABLE at or before the bar close
    t[i]+dt, where a row stamped ts is knowable at ts + 300 s (stamps are
    period starts).  NaN if none, or if that observation is older than
    max_stale seconds (default: max(dt, 2h)) - no stale forward-fill across
    archive gaps.
    """
    t, dt = _grid(timeframe, start, end)
    stale = max(dt, 7200) if max_stale is None else max_stale
    close = t + dt
    out = {f: np.full((len(t), len(symbols)), np.nan) for f in METRIC_FIELDS}
    for j, s in enumerate(symbols):
        p = os.path.join(HIST, "metrics", s + ".npz")
        if not os.path.exists(p):
            continue
        with np.load(p) as z:
            avail = z["ts"] + METRIC_AVAIL_LAG
            vals = {f: np.array(z[f], dtype=np.float64) for f in METRIC_FIELDS}
        for f in METRIC_FIELDS:            # 0 = archive placeholder, not data
            vals[f][~(vals[f] > 0)] = np.nan
        idx = np.searchsorted(avail, close, side="right") - 1
        ok = idx >= 0
        age = np.where(ok, close - avail[np.maximum(idx, 0)], np.inf)
        ok &= age <= stale
        for f in METRIC_FIELDS:
            col = np.full(len(t), np.nan)
            col[ok] = vals[f][idx[ok]]
            out[f][:, j] = col
    return out


def pit_rank_table():
    """Raw PIT table: {"day0", "symbols", "rank" [D,N] (-1 = ineligible),
    "qv30" [D,N]} - row d ranks trailing 30d quote volume of days d-30..d-1."""
    return dict(_universe())
