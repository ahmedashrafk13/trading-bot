"""
vol_breakout -- strategy family B: volatility breakout entered by SERVER-SIDE
conditional (stop-market) orders, time exit at the next session open.

Rule (per coin, per session; sessions = UTC days or 6h blocks, i.e. the
routine runs at 00/06/12/18 UTC):
  at the session open O (a run):
    R        = prior session high-low ("hl") or ATR(5 sessions) ("atr5")
    k        = fixed, or adaptive = 20-session mean of 1 - |C-O|/(H-L)
    long  if prior session close > MA(n days)  [and BTC > 200d MA if btc_gate]
    short (sides="ls" only) if prior close < MA(n) AND BTC < 200d MA
    place a conditional BUY stop-market at O + k*R with an attached stopLoss at
    O - s*R (s = k or 0.5); mirror for shorts.
  the order expires / the position is closed at the next session open (run).
Sizing: qty = risk * equity / |trigger - stop|, then a causal vol-target
scale: vol_target / (trailing-180d realised vol of the unit-risk book built
from this rule's own past closed trades, BTC gate ignored for the estimate;
expanding window if the trailing one has < 20 active days), clipped [0.1, 5]; per trade <= 1.5x,
book gross <= 3x (sim max_gross_leverage).

HOW TO SIMULATE (important -- sim.run_events has no conditional/stop ENTRY
order type; every entry fills at the OPEN of the bar after its decision bar):
the module works around it WITHOUT editing the lab. It builds a "split" copy
of the 1h panel: each 1h bar k in which some coin's trigger is hit becomes two
rows, k' = (open .. trigger) and k'' = (trigger .. close) with k''.open = the
trigger price (or the bar open if it gapped through the trigger). The entry is
decided at the close of k' (the moment the trigger trades -- causal) and fills
at the open of k'' = the trigger price; run_events then checks the attached
stop over the WHOLE 1h range of k'' (so trigger + stop inside one 1h bar is
always a loss, as the spec demands). k' rows carry no funding and have the
original t minus 1 second, so daily bucketing is unchanged.
  entries returned by events() therefore index the SPLIT panel. They carry
  't' (split-row open time) and no 'i', so running them against the raw panel
  raises ("t=... is not a bar open time") instead of silently mis-filling.
  Canonical calls:
      res = vol_breakout.simulate(panel, params, **sim_kwargs)
  or  sp = vol_breakout.sim_panel(panel, params)
      entries, kw = vol_breakout.events(panel, params)
      res = sim.run_events(sp, entries, **kw)
"""
from __future__ import annotations

import dataclasses
import itertools
import math
import warnings

import numpy as np
import pandas as pd

try:
    from .. import sim as S
except ImportError:                      # plain-directory import
    try:
        from lab import sim as S
    except ImportError:
        import sim as S

# --------------------------------------------------------------------------- #
# contract
# --------------------------------------------------------------------------- #
# first 12 of data.MAJORS (a list fixed by the data agent, not chosen on
# performance); tradable additionally requires PIT top-20 liquidity membership
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT",
           "ADAUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", "TRXUSDT", "DOTUSDT"]
PANEL = dict(timeframe="1h", symbols=SYMBOLS, universe="pit_top20", start="2020-01-01")
USES_METRICS = False
KIND = "events"

FEE = 0.00055
EXTRA_STOP_SLIP_BPS = 3.0     # added to the lab's tiers on EVERY fill (entries are stop-markets)
UNIT_RISK = 0.01              # risk of the "unit" book used for the vol estimate
MAX_TRADE_LEV = 1.5
GROSS_CAP = 3.0
VOL_WIN_DAYS = 180
VOL_MIN_DAYS = 60
MIN_ACTIVE_DAYS = 20
SCALE_CLIP = (0.1, 5.0)
BTC = "BTCUSDT"

DEFAULTS = dict(session="1d", k=0.6, range="hl", ma=20, btc_gate=False, stop="k",
                sides="long", vol_target=0.20, risk_per_trade=0.01)

GRID = [dict(DEFAULTS, session=se, k=k, range=rg, ma=n, btc_gate=g)
        for se, k, rg, n, g in itertools.product(
            ("1d", "6h"), (0.4, 0.5, 0.6, 0.7, 0.8, "adaptive"), ("hl", "atr5"),
            (10, 20, 50), (False, True))]

# chosen after the walk-forward for STABILITY: best median Sharpe over the ten
# half-years 2020H2..2025H1 (see results/vol_breakout.json). Verdict: FAILS
# out of sample (WF OOS Sharpe -0.86; fixed-param 2022-2025H1 Sharpe -0.01).
FROZEN = dict(DEFAULTS, session="1d", k=0.8, range="hl", ma=10, btc_gate=False)


def _p(params):
    q = dict(DEFAULTS)
    q.update(params or {})
    return q


# --------------------------------------------------------------------------- #
# session arrays and candidate trades (vectorised, causal)
# --------------------------------------------------------------------------- #
def _spb(session):
    return {"1d": 24, "6h": 6}[session]


def _reshape(x, a0, S_, spb, fill=np.nan):
    x = np.asarray(x, float)[a0:]
    pad = S_ * spb - x.shape[0]
    if pad:
        x = np.concatenate([x, np.full((pad, x.shape[1]), fill)])
    return x.reshape(S_, spb, -1)


def _roll_mean(a, w):
    """mean of rows s-w .. s-1 (strict: NaN if any NaN / not enough rows)."""
    return pd.DataFrame(a).rolling(w, min_periods=w).mean().shift(1).to_numpy()


def candidates(panel, params):
    """All trades the rule would take (one per triggered coin-session), with
    the exact fill / stop / size, plus the session-open rows (time exits).
    Returns dict of arrays: k (original trigger bar), j, side, fill, stop,
    size, unit_ret, exit_time; and 'exit_rows'; plus per-session levels for
    live_targets."""
    q = _p(params)
    if int(panel.dt) != 3600:
        raise ValueError("vol_breakout needs a 1h panel (intrabar trigger resolution)")
    spb = _spb(q["session"])
    spd = 24 // spb
    t = np.asarray(panel.t, np.int64)
    T, N = len(t), len(panel.symbols)
    sess = spb * 3600
    al = np.flatnonzero(t % sess == 0)
    if al.size == 0:
        raise ValueError("panel shorter than one session")
    a0 = int(al[0])
    S_ = -(-(T - a0) // spb)
    o3 = _reshape(panel.o, a0, S_, spb)
    h3 = _reshape(panel.h, a0, S_, spb)
    l3 = _reshape(panel.l, a0, S_, spb)
    c3 = _reshape(panel.c, a0, S_, spb)
    tr3 = _reshape(np.asarray(panel.tradable, float), a0, S_, spb, 0.0) > 0.5
    ts = t[a0] + np.arange(S_, dtype=np.int64) * sess          # session start times
    bar_t = ts[:, None] + np.arange(spb)[None, :] * 3600       # [S, spb]

    complete = (np.isfinite(o3) & np.isfinite(h3) & np.isfinite(l3) & np.isfinite(c3)).all(1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        O = o3[:, 0, :]
        H = np.where(complete, np.nanmax(h3, 1), np.nan)
        L = np.where(complete, np.nanmin(l3, 1), np.nan)
        C = np.where(complete, c3[:, -1, :], np.nan)
        Os = np.where(complete, O, np.nan)
    Hp, Lp, Cp = (np.vstack([np.full((1, N), np.nan), x[:-1]]) for x in (H, L, C))
    if q["range"] == "hl":
        R = Hp - Lp
    elif q["range"] == "atr5":
        Cpp = np.vstack([np.full((1, N), np.nan), C[:-1]])
        TR = np.fmax(H, Cpp) - np.fmin(L, Cpp)
        TR = np.where(np.isfinite(H) & np.isfinite(Cpp), TR, np.nan)
        R = _roll_mean(TR, 5)
    else:
        raise ValueError(q["range"])
    R = np.where(R > 0, R, np.nan)
    if q["k"] == "adaptive":
        with np.errstate(divide="ignore", invalid="ignore"):
            noise = np.where(H > L, 1.0 - np.abs(C - Os) / (H - L), np.nan)
        K = _roll_mean(noise, 20)
    else:
        K = np.full((S_, N), float(q["k"]))
    s_mult = K if q["stop"] == "k" else np.full((S_, N), float(q["stop"]))
    MA = _roll_mean(C, int(q["ma"]) * spd)

    # BTC 200d MA gate on daily closes (00:00 UTC), compared with BTC's prior-session close
    jb = panel.symbols.index(BTC) if BTC in panel.symbols else None
    if jb is None:
        up = dn = np.zeros(S_, bool)
    else:
        cb = np.asarray(panel.c, float)[:, jb]
        dmask = (t + 3600) % 86400 == 0
        dct = t[dmask] + 3600
        dc = cb[dmask]
        ma200 = pd.Series(dc).rolling(200, min_periods=200).mean().to_numpy()
        idx = np.searchsorted(dct, ts, side="right") - 1
        m2 = np.where(idx >= 0, ma200[np.maximum(idx, 0)], np.nan)
        px = Cp[:, jb]
        up = np.isfinite(m2) & np.isfinite(px) & (px > m2)
        dn = np.isfinite(m2) & np.isfinite(px) & (px < m2)

    base = np.isfinite(O) & np.isfinite(R) & np.isfinite(K) & np.isfinite(MA) & np.isfinite(Cp) \
        & tr3[:, 0, :]
    # long_vol: the long candidates WITHOUT the BTC gate. The vol estimate is built from
    # this gate-independent stream (a gate that switches trading off for months must not
    # collapse the estimate and blow the size up when trading resumes).
    long_vol = base & (Cp > MA)
    long_ok = long_vol & up[:, None] if q["btc_gate"] else long_vol
    short_ok = base & (Cp < MA) & dn[:, None] if q["sides"] == "ls" else np.zeros_like(base)

    trig_l, stop_l = O + K * R, O - s_mult * R
    trig_s, stop_s = O - K * R, O + s_mult * R

    out = {k: [] for k in ("s", "b", "j", "side", "fill", "stop", "trig", "live")}
    for side, ok, trig, stop, live in ((1, long_vol, trig_l, stop_l, long_ok),
                                       (-1, short_ok, trig_s, stop_s, short_ok)):
        if not ok.any():
            continue
        with np.errstate(invalid="ignore"):
            hit = (h3 >= trig[:, None, :]) if side > 0 else (l3 <= trig[:, None, :])
        hit &= ok[:, None, :]
        anyh = hit.any(1)
        b = hit.argmax(1)
        ss, jj = np.nonzero(anyh)
        bb = b[ss, jj]
        oo = o3[ss, bb, jj]
        tg = trig[ss, jj]
        fill = np.maximum(oo, tg) if side > 0 else np.minimum(oo, tg)
        keep = tr3[ss, bb, jj]
        for key, v in (("s", ss), ("b", bb), ("j", jj), ("fill", fill), ("trig", tg),
                       ("stop", stop[ss, jj]), ("live", live[ss, jj])):
            out[key].append(v[keep])
        out["side"].append(np.full(int(keep.sum()), side))
    if out["s"]:
        c = {k: np.concatenate(v) for k, v in out.items()}
    else:
        c = {k: np.array([], dtype=float if k in ("fill", "stop", "trig") else int)
             for k in out}
    c["live"] = c["live"].astype(bool)
    ss, bb, jj, side = c["s"].astype(int), c["b"].astype(int), c["j"].astype(int), c["side"]
    n = ss.size

    # ---- exact outcome of each candidate (for the vol estimate only) ----------
    slip = S._slippage_fraction(panel.symbols, None) + EXTRA_STOP_SLIP_BPS / 1e4
    ex_px = np.full(n, np.nan)
    ex_t = np.full(n, np.inf)
    after = np.arange(spb)[None, :] >= bb[:, None]                  # bars >= trigger bar
    lo = l3[ss, :, jj]
    hi = h3[ss, :, jj]
    op = o3[ss, :, jj]
    with np.errstate(invalid="ignore"):
        hitstop = np.where(side[:, None] > 0, lo <= c["stop"][:, None], hi >= c["stop"][:, None])
    hitstop &= after
    stopped = hitstop.any(1)
    bs = hitstop.argmax(1)
    gap = np.where(side > 0, op[np.arange(n), bs] <= c["stop"], op[np.arange(n), bs] >= c["stop"]) \
        & (bs > bb)
    ex_px[stopped] = np.where(gap, op[np.arange(n), bs], c["stop"])[stopped]
    ex_t[stopped] = (bar_t[ss, bs] + 1800)[stopped]
    nxt = ss + 1
    have_next = (nxt < S_) & (a0 + nxt * spb < T)
    ns = ~stopped & have_next
    nidx = np.where(ns)[0]
    ex_px[nidx] = o3[nxt[nidx], 0, jj[nidx]]
    ex_t[nidx] = ts[nxt[nidx]]
    sl = slip[jj]
    with np.errstate(invalid="ignore", divide="ignore"):
        ur = np.where(side > 0,
                      ex_px * (1 - sl) / (c["fill"] * (1 + sl)) - 1,
                      c["fill"] * (1 - sl) / (ex_px * (1 + sl)) - 1) - 2 * FEE
    dist = np.abs(c["trig"] - c["stop"])
    unit = UNIT_RISK * c["fill"] / dist

    # ---- causal vol-target scale per session -------------------------------------
    day0 = int(t[0] // 86400)
    nd = int(t[-1] // 86400) - day0 + 2
    known = np.isfinite(ex_t) & np.isfinite(ur)
    pnl = np.zeros(nd)
    ed = (ex_t[known] // 86400).astype(np.int64) - day0
    okd = ed < nd
    np.add.at(pnl, ed[okd], (unit[known] * ur[known])[okd])
    first = int(ed.min()) if ed.size else None
    cs1 = np.r_[0.0, np.cumsum(pnl)]
    cs2 = np.r_[0.0, np.cumsum(pnl * pnl)]
    csa = np.r_[0, np.cumsum(pnl != 0)]
    Ds = (ts // 86400).astype(np.int64) - day0
    scale = np.full(S_, np.nan)
    if first is not None:
        hiD = np.minimum(Ds, nd)
        loD = np.maximum(first, hiD - VOL_WIN_DAYS)
        m = (Ds - first) >= VOL_MIN_DAYS
        # fewer than MIN_ACTIVE_DAYS days with a closed unit trade in the trailing
        # window -> fall back to the expanding window since the first trade
        act = csa[hiD] - csa[np.maximum(loD, 0)]
        loD = np.where(act >= MIN_ACTIVE_DAYS, loD, first)
        cnt = (hiD - loD).astype(float)
        s1 = cs1[hiD] - cs1[np.maximum(loD, 0)]
        s2 = cs2[hiD] - cs2[np.maximum(loD, 0)]
        with np.errstate(invalid="ignore", divide="ignore"):
            var = (s2 - s1 * s1 / cnt) / (cnt - 1)
            est = np.sqrt(np.maximum(var, 0.0)) * math.sqrt(365.0)
        vt = q.get("vol_target")
        if vt is None:
            sc = np.full(S_, float(q["risk_per_trade"]) / UNIT_RISK)
        else:
            with np.errstate(divide="ignore"):
                sc = np.where(est > 0, float(vt) / est, SCALE_CLIP[1])
            sc = np.clip(sc, *SCALE_CLIP)
        scale = np.where(m & (cnt > 1), sc, np.nan)
    size = np.minimum(unit * scale[ss], MAX_TRADE_LEV)
    take = np.isfinite(size) & (size > 0) & c["live"]

    k_row = a0 + ss * spb + bb
    sel = take & (k_row < T)
    exit_rows = a0 + np.arange(1, S_) * spb
    exit_rows = exit_rows[exit_rows < T]
    return {"k": k_row[sel], "j": jj[sel], "side": side[sel].astype(int),
            "fill": c["fill"][sel], "stop": c["stop"][sel], "trig": c["trig"][sel],
            "size": size[sel], "unit_ret": ur[sel], "exit_time": ex_t[sel],
            "session": ss[sel], "exit_rows": exit_rows,
            # per-session levels (for live_targets / diagnostics)
            "_lv": dict(ts=ts, O=O, trig_l=trig_l, stop_l=stop_l, trig_s=trig_s,
                        stop_s=stop_s, long_ok=long_ok, short_ok=short_ok, scale=scale,
                        unit_l=UNIT_RISK * O / np.abs(trig_l - stop_l),
                        a0=a0, spb=spb, S=S_)}


# --------------------------------------------------------------------------- #
# split panel assembly
# --------------------------------------------------------------------------- #
def assemble(panel, cands, exit_rows):
    """Split panel + entries + exits for one or several candidate sets.
    cands: dict of arrays (k, j, side, fill, stop, size) -- may be the
    concatenation of several configs' candidates on disjoint windows."""
    t = np.asarray(panel.t, np.int64)
    T, N = len(t), len(panel.symbols)
    k = np.asarray(cands["k"], int)
    j = np.asarray(cands["j"], int)
    dup = np.zeros(T, bool)
    dup[k] = True
    counts = 1 + dup.astype(int)
    second = np.cumsum(counts) - 1
    first_new = second - dup
    rep = np.repeat(np.arange(T), counts)
    T2 = int(counts.sum())
    is_first = np.zeros(T2, bool)
    is_first[first_new[dup]] = True
    o = np.asarray(panel.o, float)[rep]
    h = np.asarray(panel.h, float)[rep]
    l = np.asarray(panel.l, float)[rep]
    c = np.asarray(panel.c, float)[rep]
    h[is_first] = o[is_first]
    l[is_first] = o[is_first]
    c[is_first] = o[is_first]
    fund = np.asarray(panel.funding, float)[rep]
    fund[is_first] = 0.0
    r1 = first_new[k]
    r2 = r1 + 1
    fill = np.asarray(cands["fill"], float)
    o1 = o[r1, j]
    h[r1, j] = np.maximum(o1, fill)
    l[r1, j] = np.minimum(o1, fill)
    c[r1, j] = fill
    o[r2, j] = fill
    h[r2, j] = np.maximum(h[r2, j], fill)
    l[r2, j] = np.minimum(l[r2, j], fill)
    t2 = t[rep] - is_first.astype(np.int64)
    sp = dataclasses.replace(
        panel, t=t2, o=o, h=h, l=l, c=c,
        v=np.asarray(panel.v, float)[rep], qv=np.asarray(panel.qv, float)[rep],
        funding=fund, tradable=np.asarray(panel.tradable, bool)[rep],
        meta={"orig_row": rep, "split_first": is_first, "vol_breakout_split": True})
    ex = np.zeros((T2, N), bool)
    er = np.asarray(exit_rows, int)
    er = er[(er > 0) & (er < T)]
    ex[first_new[er] - 1, :] = True
    syms = panel.symbols
    entries = [{"t": int(t2[a]), "symbol": syms[jj], "side": int(sd), "size": float(sz),
                "stop": float(st)}
               for a, jj, sd, sz, st in zip(r1, j, cands["side"], cands["size"], cands["stop"])]
    return sp, entries, ex, first_new


def run_kwargs(panel, exits):
    slip_bps = S._slippage_fraction(panel.symbols, None) * 1e4 + EXTRA_STOP_SLIP_BPS
    return dict(exits=exits, max_gross_leverage=GROSS_CAP, max_concurrent=len(panel.symbols),
                slippage_bps=slip_bps, fee=FEE)


_CACHE = {}


def _build(panel, params):
    key = (id(panel), len(panel.t), repr(sorted(_p(params).items())))
    hit = _CACHE.get(key)
    if hit is not None and hit[0] is panel:
        return hit[1]
    c = candidates(panel, params)
    sp, entries, ex, _ = assemble(panel, c, c["exit_rows"])
    out = (sp, entries, run_kwargs(panel, ex), c)
    _CACHE.clear()
    _CACHE[key] = (panel, out)
    return out


def sim_panel(panel, params):
    return _build(panel, params)[0]


def events(panel, params, metrics=None):
    """(entries, run_kwargs) for sim.run_events(sim_panel(panel, params), ...).
    Entries carry the SPLIT panel's 't' (see module docstring)."""
    _, entries, kw, _ = _build(panel, params)
    return entries, dict(kw)


def simulate(panel, params, **sim_kwargs):
    sp, entries, kw, _ = _build(panel, params)
    kw = dict(kw)
    kw.update(sim_kwargs)
    return S.run_events(sp, entries, **kw)


def signal_matrix(panel, params):
    """[T, 4N] causal fingerprint (signed size, stop, fill at the trigger bar;
    time-exit flags) on the ORIGINAL panel rows -- for wf.check_causality."""
    c = candidates(panel, params)
    T, N = len(panel.t), len(panel.symbols)
    out = np.zeros((T, 4 * N))
    out[c["k"], c["j"]] = c["side"] * c["size"]
    out[c["k"], N + c["j"]] = c["stop"]
    out[c["k"], 2 * N + c["j"]] = c["fill"]
    er = c["exit_rows"]
    out[er, 3 * N:] = 1.0
    return out


def live_targets(panel, params, metrics=None):
    """Orders to place at the run that opens the NEXT session after the
    panel's last bar (the last bar must be the last complete 1h bar). The next
    session's open is proxied by the last close. Returns
    {"session_start", "close_all_open_positions": True, "orders": {sym: {...}}}."""
    q = _p(params)
    spb = _spb(q["session"])
    t = np.asarray(panel.t, np.int64)
    nxt = int(t[-1]) + 3600
    sess = spb * 3600
    if nxt % sess != 0:
        return {"session_start": None, "note": "last bar does not end a session; "
                "orders are only (re)placed at session opens", "orders": {}}
    N = len(panel.symbols)
    pad = 1
    ext = dataclasses.replace(
        panel, t=np.r_[t, nxt],
        o=np.vstack([panel.o, np.asarray(panel.c, float)[-1:]]),
        h=np.vstack([panel.h, np.full((pad, N), np.nan)]),
        l=np.vstack([panel.l, np.full((pad, N), np.nan)]),
        c=np.vstack([panel.c, np.full((pad, N), np.nan)]),
        v=np.vstack([panel.v, np.full((pad, N), np.nan)]),
        qv=np.vstack([panel.qv, np.full((pad, N), np.nan)]),
        funding=np.vstack([panel.funding, np.zeros((pad, N))]),
        tradable=np.vstack([panel.tradable, np.asarray(panel.tradable, bool)[-1:]]),
        meta={})
    lv = candidates(ext, q)["_lv"]
    s = lv["S"] - 1
    orders = {}
    for j, sym in enumerate(panel.symbols):
        sc = lv["scale"][s]
        for side, ok, tg, st in ((1, lv["long_ok"], lv["trig_l"], lv["stop_l"]),
                                 (-1, lv["short_ok"], lv["trig_s"], lv["stop_s"])):
            if ok[s, j] and np.isfinite(sc):
                size = min(UNIT_RISK * tg[s, j] / abs(tg[s, j] - st[s, j]) * sc, MAX_TRADE_LEV)
                orders[sym] = {"side": "Buy" if side > 0 else "Sell",
                               "order": "conditional stop-market", "trigger": float(tg[s, j]),
                               "stop_loss": float(st[s, j]), "size_notional_frac": float(size),
                               "session_open_proxy": float(lv["O"][s, j]),
                               "expires_at": str(np.datetime64(nxt + sess, "s"))}
    return {"session_start": str(np.datetime64(nxt, "s")), "close_all_open_positions": True,
            "gross_cap": GROSS_CAP, "orders": orders,
            "note": "recompute trigger/stop from the ACTUAL session open price at the run"}
