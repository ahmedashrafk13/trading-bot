"""Strategy family D: funding carry (long SPOT + short PERP, same coin, same
notional) with a regime gate.  Research #5 / phase-1 `carry_regime_gate`.

PANEL LOADING - READ THIS: the trade needs spot prices, which the lab's
perp-only store does not have.  Load the panel with THIS module's
`load_panel(end=...)` (PANEL holds its kwargs), not with data.load_panel.
The returned lab `data.Panel` has 2*Np columns: [0, Np) = Binance USDT-M perps
(the pit_top30 union, 1d bars), [Np, 2Np) = the matching Binance SPOT pairs
("<PERP>@SPOT", priced in perp units, funding 0).  Simulate it with
`sim_kwargs(panel)` (per-column slippage: spot = perp tier + 4.5 bps, which
models Bybit's 0.10% spot taker fee against the lab's single 0.055% fee).
Spot klines: data/hist/spot/1d/ (strategies/_carry_spot_fetch.py).

Timing: 1d bars, decisions at the close of day i (00:00 UTC = a 6h decision
point, the 00:07 run), market fills at the next open.  Funding in bar i is the
sum settled in (t_i, t_i + 1d], i.e. known at the decision.

Rules (per coin j, day i):
  eligible  = perp in the PIT top-30 at i, perp AND spot each have >= 30 valid
              daily bars (PIT hedgeability: Binance spot first-kline date is the
              proxy for Bybit spot listing), no relist in 30d, not stressed,
              |spot/perp - 1| < 1.5% on each of the last 3 closes
  stressed  = any funding print with |rate| >= 0.5% or any settlement interval
              <= 2h in the trailing 30 days (funding cap / 1h settlement)
  enter     : f7 * 365 > h  AND  14 * f7 > 1.5 * round_trip_j  AND gate ON
              (f7/f3 = trailing 7d/3d mean DAILY funding; round_trip_j = 4 legs
              of fee + slippage), best f7 first, up to K pairs
  exit      : f3 < 0 OR f7 * 365 < h/3 OR stressed OR |basis| > 10%
              (gate_exit=True: also when the gate turns OFF)
  gate      : share of PIT top-30 perps with f7 > 0 exceeds gate (None = off)
  size      : every pair 1/K of equity per leg -> spot notional <= 1x equity;
              a pair is re-sized to 1/K when its price has drifted > 25% since
              it was last sized (else a 5x rally = 5x hidden leverage)
              (spot bought with cash; perp short margined by the spot in a
              Bybit UTA).  vol_target (None = natural 1x): scale all legs by
              L in [1, lev_cap] from a trailing 90d vol of the 1x book, changed
              only when it moves > 25%; L > 1 needs BORROWED spot -> simulate
              with `borrow_panel(panel, W)` (8% APR on spot notional above 1x).
  account_usd (None = off): skip coins whose Bybit perp qtyStep x price exceeds
              step_frac (10%) of one leg (account_usd / K); without it a $200
              book cannot match BTC/ETH/SOL/LTC legs and runs unhedged.
"""
from __future__ import annotations

import os
import sys

import numpy as np

try:                                   # imported as lab.strategies.carry_gated
    from .. import data as D
    from .. import sim as S
except ImportError:                    # imported as a top-level module
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from lab import data as D
    from lab import sim as S

HERE = os.path.dirname(os.path.abspath(__file__))
SPOT_DIR = os.path.join(D.HIST, "spot", "1d")
SPOT_EXTRA_BPS = 4.5            # Bybit spot taker 0.10% - lab fee 0.055%
FEE = S.DEFAULT_FEE
BORROW_APR = 0.08

PANEL = dict(timeframe="1d", universe="pit_top30", start="2020-01-01",
             loader="lab.strategies.carry_gated.load_panel")
USES_METRICS = False
KIND = "weights"

_H = [0.08, 0.12, 0.15, 0.20]
GRID = [dict(h=h, K=K, gate=g, gate_exit=ge, vol_target=None)
        for h in _H for K in (5, 8)
        for (g, ge) in ((None, False), (0.6, False), (0.6, True))]
FROZEN = dict(h=0.08, K=8, gate=None, gate_exit=False, vol_target=None)   # most-chosen in WF (see results)
# $200 live variant (not searched): FROZEN + account_usd=200 (drops coins whose perp qtyStep > 10% of a leg)
DEFAULTS = dict(h=0.12, K=8, gate=0.6, gate_exit=False, vol_target=None, cost_mult=1.5,
                lev_cap=2.5, stress_abs=0.005, stress_int_h=2, min_age=30,
                basis_in=0.015, basis_out=0.10, band=0.25)


# --------------------------------------------------------------------------- #
# panel
# --------------------------------------------------------------------------- #
def load_panel(timeframe="1d", universe="pit_top30", start="2020-01-01", end=None,
               symbols=None, hedge_marks="close", **_):
    """hedge_marks: how h/l are presented to the lab's liquidation check.
    The check values every long at its OWN bar low and every short at its OWN
    bar high independently.  For a same-coin spot/perp hedge that is a price path
    that never exists: with raw daily h/l it 'liquidated' a 1x hedged book on
    2021-05-19 although the two legs never diverged by more than ~1% at the
    closes.  "close" (default): h = l = c for both legs, i.e. the check sees the
    marked (close) basis and the open basis only; intrabar basis spikes are NOT
    modelled (reported separately).  "body": h/l = max/min(open, close) (still
    charges the whole open->close move against the hedge: conservative, and it
    false-liquidates the 2.5x variant on 40% days).  "raw": untouched h/l.
    h/l feed nothing else in run_weights."""
    if timeframe != "1d":
        raise ValueError("carry_gated is built on 1d bars (spot store is 1d)")
    pp = D.load_panel("1d", symbols=symbols, universe=universe, start=start, end=end)
    t, T, Np = pp.t, len(pp.t), len(pp.symbols)
    so, sh, sl, sc, sv, sq = (np.full((T, Np), np.nan) for _ in range(6))
    spot_sym, spot_first = [], []
    for j, s in enumerate(pp.symbols):
        p = os.path.join(SPOT_DIR, s + ".npz")
        if not os.path.exists(p):
            spot_sym.append(""); spot_first.append(None)
            continue
        with np.load(p) as z:
            ts = z["t"].astype(np.int64); sc_ = float(z["scale"]); nm = str(z["spot_symbol"])
            arrs = [z[k].astype(float) for k in ("o", "h", "l", "c", "v", "qv")]
        spot_sym.append(nm)
        spot_first.append(int(ts[0]) if ts.size else None)
        if not ts.size:
            continue
        idx = (ts - int(t[0])) // 86400
        k = (idx >= 0) & (idx < T) & ((ts - int(t[0])) % 86400 == 0)
        for dst, a, mult in zip((so, sh, sl, sc, sv, sq), arrs, (sc_, sc_, sc_, sc_, 1 / sc_, 1.0)):
            dst[idx[k], j] = a[k] * mult
    svalid = (np.isfinite(so) & np.isfinite(sh) & np.isfinite(sl) & np.isfinite(sc)
              & (np.nan_to_num(sv) > 0))
    # spot relist: first valid bar after >= 3 missing days
    srel = np.zeros((T, Np), bool)
    for j in range(Np):
        v = np.flatnonzero(svalid[:, j])
        if v.size > 1:
            g = np.flatnonzero(np.diff(v) > 3)
            srel[v[g + 1], j] = True
    # funding stress inputs from the raw settlement stamps
    fmax = np.zeros((T, Np)); fmin_int = np.full((T, Np), 99.0)
    lo = int(t[0])
    for j, s in enumerate(pp.symbols):
        p = os.path.join(D.HIST, "funding", s + ".npz")
        if not os.path.exists(p):
            continue
        with np.load(p) as z:
            ts, rt = z["ts"].astype(np.int64), z["rate"].astype(float)
        if ts.size < 2:
            continue
        itv = np.r_[99.0, np.diff(ts) / 3600.0]
        k = (ts > lo) & (ts <= int(t[-1]) + 86400)
        i = (ts[k] - lo - 1) // 86400
        np.maximum.at(fmax[:, j], i, np.abs(rt[k]))
        np.minimum.at(fmin_int[:, j], i, itv[k])
    ph, pl = pp.h, pp.l
    if hedge_marks in (True, "body"):
        ph = np.where(np.isfinite(pp.h), np.fmax(pp.o, pp.c), np.nan)
        pl = np.where(np.isfinite(pp.l), np.fmin(pp.o, pp.c), np.nan)
        sh = np.where(np.isfinite(sh), np.fmax(so, sc), np.nan)
        sl = np.where(np.isfinite(sl), np.fmin(so, sc), np.nan)
    elif hedge_marks == "close":
        ph = np.where(np.isfinite(pp.h), pp.c, np.nan)
        pl = np.where(np.isfinite(pp.l), pp.c, np.nan)
        sh = np.where(np.isfinite(sh), sc, np.nan)
        sl = np.where(np.isfinite(sl), sc, np.nan)
    elif hedge_marks not in (False, "raw"):
        raise ValueError("hedge_marks must be close|body|raw")
    pvalid = pp.meta["valid"]
    member = pp.meta["member"] if pp.meta.get("member") is not None else np.ones((T, Np), bool)
    slip = S.default_slippage_bps(pp.symbols)
    cat = lambda a, b: np.concatenate([a, b], axis=1)
    meta = dict(pp.meta)
    meta.update({
        "valid": cat(pvalid, svalid),
        "member": cat(member, np.zeros((T, Np), bool)),
        "relisted": cat(pp.meta["relisted"], srel),
        "perp_member": member.copy(),
        "fund_maxabs": fmax, "fund_min_int_h": fmin_int,
        "n_pairs": Np, "spot_symbols": list(spot_sym), "spot_first_t": list(spot_first),
        "slippage_bps": [float(x) for x in np.r_[slip, slip + SPOT_EXTRA_BPS]],
        "source": "binance-usdm perps + binance spot (carry_gated)",
        "hedge_marks": str(hedge_marks),
    })
    meta.pop("n_hours", None)
    syms = list(pp.symbols) + [s + "@SPOT" for s in pp.symbols]
    return D.Panel(t=t, dt=pp.dt, symbols=syms,
                   o=cat(pp.o, so), h=cat(ph, sh), l=cat(pl, sl), c=cat(pp.c, sc),
                   v=cat(pp.v, sv), qv=cat(pp.qv, sq),
                   funding=cat(pp.funding, np.zeros((T, Np))),
                   tradable=cat(pvalid, svalid), meta=meta)


def sim_kwargs(panel, **kw):
    out = dict(slippage_bps=np.asarray(panel.meta["slippage_bps"], float),
               max_gross_leverage=5.0)
    out.update(kw)
    return out


def borrow_panel(panel, W, apr=BORROW_APR):
    """Copy of panel whose spot columns carry a borrow charge as 'funding':
    rate = apr/365 * max(0, 1 - 1/S) on the spot notional, S = spot weight sum
    held during the bar (target decided at the previous close)."""
    Np = panel.meta["n_pairs"]
    Sw = np.nansum(np.clip(np.asarray(W, float)[:, Np:], 0, None), axis=1)
    held = np.r_[0.0, Sw[:-1]]
    frac = np.where(held > 1.0, 1.0 - 1.0 / np.maximum(held, 1e-12), 0.0)
    f = panel.funding.copy()
    f[:, Np:] = (apr * panel.dt / (365 * 86400) * frac)[:, None]
    import dataclasses
    return dataclasses.replace(panel, funding=f)


# --------------------------------------------------------------------------- #
# signal
# --------------------------------------------------------------------------- #
def _roll_mean(x, n):
    c = np.cumsum(np.vstack([np.zeros((1, x.shape[1])), x]), axis=0)
    out = np.full(x.shape, np.nan)
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def _roll_any(b, n):
    c = np.cumsum(np.vstack([np.zeros((1, b.shape[1])), b.astype(np.int64)]), axis=0)
    out = np.zeros(b.shape, bool)
    idx = np.arange(b.shape[0])
    lo = np.maximum(idx + 1 - n, 0)
    out[:] = (c[idx + 1] - c[lo]) > 0
    return out


def _age(valid, relist):
    """Consecutive-ish count of valid bars since the last relist (causal)."""
    T, N = valid.shape
    out = np.zeros((T, N))
    run = np.zeros(N)
    for i in range(T):
        run = np.where(relist[i], 0.0, run)
        run = run + valid[i]
        out[i] = run
    return out


def _state(panel, params):
    p = dict(DEFAULTS); p.update(params or {})
    m = panel.meta
    Np = m["n_pairs"]
    T = len(panel.t)
    pv = m["valid"][:, :Np]; sv = m["valid"][:, Np:]
    fd = np.where(pv, panel.funding[:, :Np], 0.0)
    f7 = _roll_mean(fd, 7); f3 = _roll_mean(fd, 3)
    # funding needs 7 valid perp days inside the window
    nv7 = _roll_mean(pv.astype(float), 7) * 7
    f7 = np.where(nv7 >= 7 - 1e-9, f7, np.nan)
    f3 = np.where(_roll_mean(pv.astype(float), 3) * 3 >= 3 - 1e-9, f3, np.nan)
    stress = _roll_any((m["fund_maxabs"] >= p["stress_abs"])
                       | (m["fund_min_int_h"] <= p["stress_int_h"]), 30)
    rel = m["relisted"]
    page = _age(pv, rel[:, :Np]); sage = _age(sv, rel[:, Np:])
    relent = _roll_any(rel[:, :Np] | rel[:, Np:], 30)
    pc = panel.c[:, :Np]; sc = panel.c[:, Np:]
    with np.errstate(invalid="ignore", divide="ignore"):
        basis = sc / pc - 1.0
    ab = np.abs(np.where(np.isfinite(basis), basis, np.inf))
    b3 = np.maximum(np.maximum(ab, np.vstack([np.full((1, Np), np.inf), ab[:-1]])),
                    np.vstack([np.full((2, Np), np.inf), ab[:-2]]))
    slip = np.asarray(m["slippage_bps"], float) / 1e4
    rt = 2 * (2 * FEE + slip[:Np] + slip[Np:])
    mem = m["perp_member"]
    pos7 = (f7 > 0) & mem & np.isfinite(f7)
    cnt = (mem & np.isfinite(f7)).sum(1)
    gate_share = np.where(cnt > 0, pos7.sum(1) / np.maximum(cnt, 1), 0.0)
    return dict(p=p, Np=Np, T=T, pv=pv, sv=sv, fd=fd, f7=f7, f3=f3, stress=stress,
                page=page, sage=sage, relent=relent, basis=basis, b3=b3, rt=rt,
                mem=mem, gate_share=gate_share, pc=pc, sc=sc)


def _run(panel, params):
    st = _state(panel, params)
    p, Np, T = st["p"], st["Np"], st["T"]
    h, K = float(p["h"]), int(p["K"])
    f7, f3 = st["f7"], st["f3"]
    gate = p["gate"]
    gate_on = np.ones(T, bool) if gate is None else st["gate_share"] > float(gate)
    elig = (st["mem"] & (st["page"] >= p["min_age"]) & (st["sage"] >= p["min_age"])
            & ~st["relent"] & ~st["stress"] & (st["b3"] < p["basis_in"])
            & st["pv"] & st["sv"] & np.isfinite(f7)
            & (f7 * 365 > h) & (14 * f7 > p["cost_mult"] * st["rt"][None, :]))
    acct = p.get("account_usd")
    if acct:
        # $-account implementability: skip coins whose perp qtyStep is worth more
        # than `step_frac` of one leg (Bybit instruments of TODAY, applied to history)
        ins = D.load_bybit_instruments()
        step = np.array([float((ins.get(sym) or {}).get("qtyStep") or np.inf)
                         for sym in panel.symbols[:Np]])
        leg = float(acct) * max(float(p.get("lev_hint", 1.0)), 1.0) / K
        elig &= (step[None, :] * st["pc"]) <= float(p.get("step_frac", 0.1)) * leg
    held = np.zeros(Np, bool)
    H = np.zeros((T, Np), bool)
    for i in range(T):
        if held.any():
            with np.errstate(invalid="ignore"):
                ex = ((f3[i] < 0) | (f7[i] * 365 < h / 3) | st["stress"][i]
                      | (np.abs(np.nan_to_num(st["basis"][i], nan=0.0)) > p["basis_out"]))
            # a perp/spot that has stopped trading for good cannot be held
            ex |= ~np.isfinite(f7[i]) & ~st["pv"][i]
            if p["gate_exit"] and not gate_on[i]:
                ex[:] = True
            held &= ~ex
        free = K - int(held.sum())
        if free > 0 and gate_on[i]:
            c = np.flatnonzero(elig[i] & ~held)
            if c.size:
                c = c[np.argsort(-f7[i, c], kind="stable")][:free]
                held[c] = True
        H[i] = held
    return st, H


def _book_returns(st, H, K):
    """1x book daily return from prices + funding (for the vol estimate)."""
    pc, sc, fd = st["pc"], st["sc"], st["fd"]
    with np.errstate(invalid="ignore", divide="ignore"):
        rp = np.vstack([np.zeros((1, pc.shape[1])), pc[1:] / pc[:-1] - 1])
        rs = np.vstack([np.zeros((1, sc.shape[1])), sc[1:] / sc[:-1] - 1])
    pair = np.nan_to_num(rs - rp + fd, nan=0.0, posinf=0.0, neginf=0.0)
    Hp = np.vstack([np.zeros((1, H.shape[1]), bool), H[:-1]])
    return (pair * Hp).sum(1) / K


def weights(panel, params, metrics=None):
    st, H = _run(panel, params)
    return _weights_from_H(st, H)


def _weights_from_H(st, H):
    p, Np, T = st["p"], st["Np"], st["T"]
    K = int(p["K"])
    L = np.ones(T)
    vt = p.get("vol_target")
    if vt:
        r = _book_returns(st, H, K)
        cur = 1.0
        for i in range(T):
            a = max(0, i - 89)
            seg = r[a:i + 1]
            if seg.size >= 30:
                vol = max(float(np.std(seg, ddof=1)) * np.sqrt(365), 0.005)
                tgt = float(np.clip(vt / vol, 1.0, p["lev_cap"]))
                if abs(tgt - cur) / cur > 0.25:
                    cur = tgt
            L[i] = cur
    W = np.zeros((T, 2 * Np))
    # both legs are dropped together if either is not tradable at the decision bar
    ok = st["pv"] & st["sv"]
    Hk = H & ok
    # Drift control.  The sim holds qty between weight changes, so a pair whose
    # coin rallies 5x would silently run at 5x notional/equity (2021).  When the
    # perp close has moved more than `band` (relative) since the pair was last
    # sized, the target is re-issued with a 1e-9 relative jitter so the sim
    # re-sizes BOTH legs back to L/K at the next open (works under the default
    # rebalance="on_change").
    band = float(p.get("band", 0.25))
    pc = st["pc"]
    w = np.zeros((T, Np))
    ref = np.full(Np, np.nan)
    par = np.zeros(Np)
    lastL = np.full(Np, np.nan)
    for i in range(T):
        on = Hk[i]
        newp = on & ~np.isfinite(ref)
        ref[newp] = pc[i, newp]; lastL[newp] = L[i]
        with np.errstate(invalid="ignore", divide="ignore"):
            drift = np.abs(pc[i] / ref - 1.0)
        re = on & ~newp & ((drift > band) | (L[i] != lastL))
        par[re] = 1.0 - par[re]
        ref[re] = pc[i, re]; lastL[re] = L[i]
        w[i] = np.where(on, (L[i] / K) * (1.0 + 1e-9 * par), 0.0)
        ref[~on] = np.nan; par[~on] = 0.0
    W[:, :Np] = -w
    W[:, Np:] = w
    return W


def live_targets(panel, params, metrics=None):
    st, H = _run(panel, params)
    W = weights(panel, params)
    Np = st["Np"]
    i = st["T"] - 1
    pairs = []
    for j in np.flatnonzero(W[i, Np:] > 0):
        pairs.append({"perp": panel.symbols[j], "spot_binance": panel.meta["spot_symbols"][j],
                      "notional_frac_per_leg": float(W[i, Np + j]),
                      "f7_annualised": float(st["f7"][i, j] * 365),
                      "basis": float(st["basis"][i, j])})
    return {"as_of_bar_open": int(panel.t[i]), "gate_share_pos_f7": float(st["gate_share"][i]),
            "pairs": pairs,
            "orders": "market BUY spot + market SELL perp (same notional) for new pairs, "
                      "reverse for dropped pairs, at the 00:07 run; perp stopLoss far "
                      "(e.g. 3x the liquidation clearance rule allows) - it is a hedge leg"}
