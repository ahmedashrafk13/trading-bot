"""Screen (a): residualised taker-flow imbalance. Dev data only (end 2025-06-30).

Run: python backtest/lab/strategies/_micro_screen_a.py  -> writes
     backtest/lab/results/_screen_a.json (IC tables).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data  # noqa: E402
from lab.strategies import _micro_stats as ST  # noqa: E402

END = "2025-06-30"
HORIZ = {"6h": 1, "24h": 4, "72h": 12}


def feats_1h(p1):
    """Sampled-at-6h-closes features from a 1h panel with tbqv."""
    tb = pd.DataFrame(p1.meta["tbqv"])
    qv = pd.DataFrame(p1.qv)
    c = p1.c
    lc = np.log(c)
    out = {}
    tclose = p1.t + p1.dt
    samp = np.flatnonzero(tclose % ST.H6 == 0)
    for W in (4, 24):
        tbs = tb.rolling(W, min_periods=W).sum().to_numpy()
        qvs = qv.rolling(W, min_periods=W).sum().to_numpy()
        imb = 2.0 * tbs / np.where(qvs > 0, qvs, np.nan) - 1.0
        rW = np.full_like(lc, np.nan)
        rW[W:] = lc[W:] - lc[:-W]
        out[f"imb{W}"] = imb[samp]
        out[f"r{W}"] = rW[samp]
    r7 = np.full_like(lc, np.nan)
    r7[168:] = lc[168:] - lc[:-168]
    out["r7d"] = r7[samp]
    out["c"] = c[samp]
    out["tclose"] = tclose[samp]
    return out


def ts_block(F, sym_idx, names):
    """Time-series tests per symbol and pooled."""
    res = {}
    tc = F["tclose"]
    for W in (4, 24):
        z = ST.roll_resid_z(F[f"imb{W}"], F[f"r{W}"], 360, 180)
        F[f"z{W}"] = z
    for W in (4, 24):
        for hname, h in HORIZ.items():
            fwd = np.column_stack([ST.fwd_log_ret(F["c"][:, j], h) for j in range(F["c"].shape[1])])
            for half in ("train", "test"):
                if half == "train":
                    m = (tc + h * ST.H6) <= ST.TRAIN_END
                else:
                    m = (tc >= ST.TRAIN_END) & (tc < ST.TEST_END)
                rows = {}
                for j, s in zip(sym_idx, names):
                    y = fwd[m, j]
                    z = F[f"z{W}"][m, j]
                    imb = F[f"imb{W}"][m, j]
                    rW = F[f"r{W}"][m, j]
                    r7 = F["r7d"][m, j]
                    one = np.ones_like(y)
                    uni = ST.ols_nw(y, np.column_stack([one, z]), h)
                    ctl = ST.ols_nw(y, np.column_stack([one, z, rW, r7]), h)
                    raw = ST.ols_nw(y, np.column_stack([one, imb, rW, r7]), h)
                    rev = ST.ols_nw(y, np.column_stack([one, rW]), h)
                    # non-overlapping, average t over the h offsets
                    tno = []
                    for off in range(h):
                        sl = slice(off, None, h)
                        r_ = ST.ols_nw(y[sl], np.column_stack([one[sl], z[sl], rW[sl], r7[sl]]), 0)
                        if r_ is not None:
                            tno.append(r_["t"][1])
                    ok = np.isfinite(y) & np.isfinite(z)
                    ic = pd.Series(z[ok]).rank().corr(pd.Series(y[ok]).rank()) if ok.sum() > 10 else np.nan
                    rows[s] = {
                        "n": uni["n"] if uni else 0,
                        "ic_spearman": ST.fmt(ic),
                        "b_z_uni": ST.fmt(uni["b"][1] * 1e4, 2) if uni else None,
                        "t_z_uni": ST.fmt(uni["t"][1], 2) if uni else None,
                        "b_z_ctl_bp": ST.fmt(ctl["b"][1] * 1e4, 2) if ctl else None,
                        "t_z_ctl_nw": ST.fmt(ctl["t"][1], 2) if ctl else None,
                        "t_z_ctl_nonoverlap_mean": ST.fmt(np.mean(tno), 2) if tno else None,
                        "t_rawimb_ctl": ST.fmt(raw["t"][1], 2) if raw else None,
                        "t_rW_alone": ST.fmt(rev["t"][1], 2) if rev else None,
                    }
                res[f"W{W}_{hname}_{half}"] = rows
    return res


def run_ts():
    p1 = data.load_panel("1h", symbols=["BTCUSDT", "ETHUSDT"], start="2020-01-01", end=END,
                         with_taker=True)
    F = feats_1h(p1)
    del p1
    return ts_block(F, [0, 1], ["BTCUSDT", "ETHUSDT"])


def run_xs():
    p6 = data.load_panel("6h", universe="pit_top20", start="2020-01-01", end=END)
    syms = p6.symbols
    trad = p6.tradable
    tc6 = p6.t + p6.dt
    c6 = p6.c
    T6, N = c6.shape
    keys = ("imb4", "r4", "imb24", "r24", "r7d", "c")
    A = {k: np.full((T6, N), np.nan) for k in keys}
    for a in range(0, N, 20):
        chunk = syms[a:a + 20]
        p1 = data.load_panel("1h", symbols=chunk, start="2020-01-01", end=END, with_taker=True)
        F = feats_1h(p1)
        # align sampled closes to 6h closes
        idx = np.searchsorted(tc6, F["tclose"])
        okk = (idx < T6) & (tc6[np.minimum(idx, T6 - 1)] == F["tclose"])
        for k in keys:
            A[k][idx[okk], a:a + len(chunk)] = F[k][okk]
        del p1, F
    # relisted: invalidate 7d around relists
    rel = p6.meta["relisted"]
    relwin = pd.DataFrame(rel.astype(float)).rolling(28, min_periods=1).max().to_numpy() > 0
    for k in ("imb4", "r4", "imb24", "r24", "r7d"):
        A[k][relwin] = np.nan
    A["z4"] = ST.roll_resid_z(A["imb4"], A["r4"], 360, 180)
    A["z24"] = ST.roll_resid_z(A["imb24"], A["r24"], 360, 180)
    for k in ("z4", "z24", "imb4", "imb24", "r4", "r24", "r7d"):
        A[k][~trad] = np.nan
    res = {}
    for W in (4, 24):
        for hname, h in HORIZ.items():
            fwd = ST.fwd_log_ret(A["c"], h)
            fwd = np.clip(fwd, -0.7, 0.7)
            # forward window must not start after a relist
            relf = pd.DataFrame(rel[::-1].astype(float)).rolling(h, min_periods=1).max().to_numpy()[::-1] > 0
            fwd[np.roll(relf, -1, axis=0)] = np.nan
            for half in ("train", "test"):
                if half == "train":
                    m = (tc6 + h * ST.H6) <= ST.TRAIN_END
                else:
                    m = (tc6 >= ST.TRAIN_END) & (tc6 < ST.TEST_END)
                z, imb, rW, r7, y = (A[f"z{W}"][m], A[f"imb{W}"][m], A[f"r{W}"][m], A["r7d"][m], fwd[m])
                ic = ST.cs_ic(z, y, h)
                ic_raw = ST.cs_ic(imb, y, h)
                ic_rev = ST.cs_ic(-rW, y, h)
                fm, _ = ST.fama_macbeth(ST.rank_cs(y), [ST.rank_cs(z), ST.rank_cs(rW), ST.rank_cs(r7)], h)
                fmr, _ = ST.fama_macbeth(ST.rank_cs(y), [ST.rank_cs(imb), ST.rank_cs(rW), ST.rank_cs(r7)], h)
                # non-overlapping: FM on every h-th row, mean t over offsets
                tno = []
                for off in range(h):
                    sl = slice(off, None, h)
                    f2, _ = ST.fama_macbeth(ST.rank_cs(y[sl]), [ST.rank_cs(z[sl]), ST.rank_cs(rW[sl]), ST.rank_cs(r7[sl])], 0)
                    tno.append(f2[0]["t"])
                res[f"W{W}_{hname}_{half}"] = {
                    "ic_z": ST.fmt(ic["ic"]), "t_ic_z": ST.fmt(ic["t"], 2), "periods": ic["n_periods"],
                    "ic_raw_imb": ST.fmt(ic_raw["ic"]), "t_ic_raw_imb": ST.fmt(ic_raw["t"], 2),
                    "ic_minus_rW": ST.fmt(ic_rev["ic"]), "t_ic_minus_rW": ST.fmt(ic_rev["t"], 2),
                    "fm_rank_z_ctl": ST.fmt(fm[0]["coef"]), "t_fm_z_ctl_nw": ST.fmt(fm[0]["t"], 2),
                    "t_fm_z_ctl_nonoverlap_mean": ST.fmt(float(np.nanmean(tno)), 2),
                    "t_fm_rW": ST.fmt(fm[1]["t"], 2), "t_fm_r7d": ST.fmt(fm[2]["t"], 2),
                    "t_fm_rawimb_ctl": ST.fmt(fmr[0]["t"], 2),
                }
    return res


if __name__ == "__main__":
    out = {"ts_btc_eth": run_ts()}
    print(json.dumps(out["ts_btc_eth"], indent=0)[:6000])
    out["xs_pit_top20"] = run_xs()
    print(json.dumps(out["xs_pit_top20"], indent=0))
    with open(os.path.join(os.path.dirname(HERE), "results", "_screen_a.json"), "w") as f:
        json.dump(out, f, indent=1)
