"""Screens (b) OI quadrant + OI-flush reversal and (c) L/S crowding, 12 metrics majors.
Dev data only (end 2025-06-30). Writes backtest/lab/results/_screen_bc.json.
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
START = "2021-12-01"
SYMS = data.MAJORS[:12]
HOUR = 3600


def load():
    p = data.load_panel("1h", symbols=SYMS, start=START, end=END)
    m = data.load_metrics(SYMS, "1h", start=START, end=END)
    return p, m


# --------------------------------------------------------------------------- #
# (b1) OI FLUSH event study on 1h bars
# --------------------------------------------------------------------------- #
def flush_study(p, m, lag=1, sig_k=3.0):
    c = p.c
    lc = np.log(c)
    T, N = c.shape
    r1 = np.full_like(lc, np.nan)
    r1[1:] = lc[1:] - lc[:-1]
    loi = np.log(m["oi_value"])
    d1 = np.full_like(loi, np.nan)
    d1[1:] = loi[1:] - loi[:-1]
    # trailing 30d sigma, EXCLUDING the current bar (shifted)
    sd_oi = pd.DataFrame(d1).rolling(720, min_periods=360).std().shift(1).to_numpy()
    sd_r = pd.DataFrame(r1).rolling(720, min_periods=360).std().shift(1).to_numpy()
    flush = d1 <= -sig_k * sd_oi
    nodrop = d1 > -1.0 * sd_oi
    absz = np.abs(r1) / sd_r
    bucket = np.digitize(np.nan_to_num(absz, nan=-1.0), [0.5, 1, 1.5, 2, 3, 4, 6]).astype(float)
    bucket[~np.isfinite(absz)] = np.nan
    tclose = p.t + p.dt
    out = {}
    # decision at close of bar i+lag; forward return from that close
    for hname, h in {"6h": 6, "24h": 24, "72h": 72}.items():
        fwd = np.full_like(lc, np.nan)
        fwd[:-h] = lc[h:] - lc[:-h]
        fwd_d = np.full_like(lc, np.nan)       # aligned to event bar i
        if lag:
            fwd_d[:-lag] = fwd[lag:]
        else:
            fwd_d[:] = fwd
        s = -np.sign(r1)                        # reversal direction
        rev = s * fwd_d
        # realistic 6h cadence: first 6h close >= close(i+lag)
        tdec = tclose + lag * HOUR
        tnext = ((tdec + ST.H6 - 1) // ST.H6) * ST.H6
        k6 = ((tnext - tclose) // HOUR).astype(int)   # bars from i to the 6h close
        rows = {}
        for half in ("train", "test", "all"):
            if half == "train":
                hm = (tclose + (lag + h + 6) * HOUR) <= ST.TRAIN_END
            elif half == "test":
                hm = (tclose >= ST.TRAIN_END) & (tclose < ST.TEST_END)
            else:
                hm = tclose < ST.TEST_END
            hm = hm[:, None] & np.ones((1, N), bool)
            ev = flush & hm & np.isfinite(rev) & np.isfinite(bucket)
            ctl = nodrop & hm & np.isfinite(rev)
            # decluster: keep first event per symbol within h bars
            evd = np.zeros_like(ev)
            for j in range(N):
                last = -10**9
                for i in np.flatnonzero(ev[:, j]):
                    if i - last >= h:
                        evd[i, j] = True
                        last = i
            # matched control mean by bucket
            # control matched on |r_1h| bucket AND the sign of r_1h (a down-move
            # control for down-move events: removes bull/bear drift)
            ctl_mean = {}
            sgn = np.sign(r1)
            for b in range(8):
                for sg in (-1.0, 1.0):
                    mk = ctl & (bucket == b) & (sgn == sg)
                    ctl_mean[(b, sg)] = np.nanmean(rev[mk]) if mk.sum() > 30 else np.nan
            ii, jj = np.nonzero(evd)
            ex = np.array([rev[i, j] - ctl_mean.get((int(bucket[i, j]), float(sgn[i, j])), np.nan) for i, j in zip(ii, jj)])
            # time clusters: events whose bar falls in the same UTC day = one cluster
            day = (tclose[ii] // 86400)
            def clus(x):
                x = np.asarray(x, float)
                k = np.isfinite(x)
                if k.sum() < 5:
                    return {"n_clusters": 0}
                df = pd.DataFrame({"d": day[k], "x": x[k]}).groupby("d")["x"].mean()
                v = df.to_numpy()
                # clusters within h hours still overlap: NW with lag ceil(h/24)
                mm, tt_, nn = ST.mean_nw_t(v, int(np.ceil(h / 24)))
                return {"n_clusters": int(nn), "mean_bp": round(mm * 1e4, 1), "t_nw": round(tt_, 2)}
            raw = np.array([rev[i, j] for i, j in zip(ii, jj)])
            # 6h-cadence version: reversal from the next 6h close, same horizon
            r6 = []
            for i, j in zip(ii, jj):
                a = i + k6[i]
                if a + h < T and np.isfinite(lc[a + h, j]) and np.isfinite(lc[a, j]):
                    r6.append(s[i, j] * (lc[a + h, j] - lc[a, j]))
                else:
                    r6.append(np.nan)
            r6 = np.array(r6)
            dn = np.array([r1[i, j] < 0 for i, j in zip(ii, jj)])
            yrs = np.array([pd.Timestamp(int(tclose[i]), unit="s").year for i in ii])

            def tt(x):
                x = x[np.isfinite(x)]
                if x.size < 5:
                    return {"n": int(x.size)}
                return {"n": int(x.size), "mean_bp": round(float(x.mean() * 1e4), 1),
                        "t": round(float(x.mean() / (x.std(ddof=1) / np.sqrt(x.size))), 2),
                        "hit": round(float((x > 0).mean()), 3)}
            rows[half] = {
                "events_raw_reversal": tt(raw),
                "excess_vs_matched_control": tt(ex),
                "excess_day_clustered": clus(ex),
                "cadence6h_day_clustered": clus(r6),
                "price_down_events_excess": tt(ex[dn]) if dn.any() else None,
                "price_up_events_excess": tt(ex[~dn]) if (~dn).any() else None,
                "cadence6h_raw_reversal": tt(r6),
                "excess_by_year": {int(y): tt(ex[yrs == y]) for y in np.unique(yrs)},
                "control_mean_by_bucket_bp": {f"{int(b)}{'+' if sg > 0 else '-'}": (None if not np.isfinite(v) else round(v * 1e4, 1))
                                              for (b, sg), v in ctl_mean.items()},
            }
        out[hname] = rows
    return out


# --------------------------------------------------------------------------- #
# 6h-sampled features (b2 quadrant, c crowding)
# --------------------------------------------------------------------------- #
def sampled(p, m):
    tclose = p.t + p.dt
    samp = np.flatnonzero(tclose % ST.H6 == 0)
    lc = np.log(p.c)

    def back(x, k):
        o = np.full_like(x, np.nan)
        o[k:] = x[k:] - x[:-k]
        return o
    F = {"tclose": tclose[samp], "c": p.c[samp],
         "r24": back(lc, 24)[samp], "r7d": back(lc, 168)[samp],
         "doi24": back(np.log(m["oi_value"]), 24)[samp],
         "lnG": np.log(m["ls_ratio"])[samp], "lnT": np.log(m["top_ls_ratio"])[samp]}
    return F


def ts_pooled(y, Xs, h):
    """Pooled time-series regression over symbols with Driscoll-Kraay SEs
    (cross-sectional + serial correlation), NW lags = h."""
    return ST.ols_dk(y, Xs, h)


def quadrant_and_crowding(F):
    T, N = F["c"].shape
    tc = F["tclose"]
    zG = ST.roll_z(F["lnG"], 120, 60)
    zT = ST.roll_z(F["lnT"], 120, 60)
    D = zT - zG
    ext = np.where((zG >= 2) & (D <= -1), -1.0, np.where((zG <= -2) & (D >= 1), 1.0, 0.0))
    ext[~(np.isfinite(zG) & np.isfinite(D))] = np.nan
    up = (F["doi24"] > 0).astype(float)
    up[~np.isfinite(F["doi24"])] = np.nan
    r24, r7 = F["r24"], F["r7d"]
    qint = r24 * (1 - up)             # r24 when OI fell (covering / liquidation)
    out = {"quadrant": {}, "crowding": {}}
    for hname, h in {"6h": 1, "24h": 4, "72h": 12}.items():
        fwd = ST.fwd_log_ret(F["c"], h)
        for half in ("train", "test"):
            if half == "train":
                hm = (tc + h * ST.H6) <= ST.TRAIN_END
            else:
                hm = (tc >= ST.TRAIN_END) & (tc < ST.TEST_END)
            y = fwd[hm]
            # quadrant: fwd ~ r24 + r24*1[dOI<0] + 1[dOI>0] + r7d
            q = ts_pooled(y, [r24[hm], qint[hm], up[hm], r7[hm]], h)
            qx, _ = ST.fama_macbeth(ST.rank_cs(y), [ST.rank_cs(r24[hm]), ST.rank_cs(F["doi24"][hm]),
                                                    ST.rank_cs(r24[hm] * np.sign(F["doi24"][hm])),
                                                    ST.rank_cs(r7[hm])], h, min_n=8)
            # quadrant means (signed by next direction): mean fwd per quadrant
            qm = {}
            for name, mk in {"A_up_oiup": (r24 > 0) & (F["doi24"] > 0), "B_up_oidn": (r24 > 0) & (F["doi24"] < 0),
                             "C_dn_oiup": (r24 < 0) & (F["doi24"] > 0), "D_dn_oidn": (r24 < 0) & (F["doi24"] < 0)}.items():
                v = y[mk[hm]]
                v = v[np.isfinite(v)]
                qm[name] = {"n": int(v.size), "mean_fwd_bp": round(float(v.mean() * 1e4), 1) if v.size else None}
            out["quadrant"][f"{hname}_{half}"] = {
                "ts_t_r24": ST.fmt(q["t"][1], 2), "ts_t_r24_x_oidown": ST.fmt(q["t"][2], 2),
                "ts_t_oiup_dummy": ST.fmt(q["t"][3], 2), "ts_t_r7d": ST.fmt(q["t"][4], 2), "n": q["n"],
                "xs_fm_t_r24": ST.fmt(qx[0]["t"], 2), "xs_fm_t_doi24": ST.fmt(qx[1]["t"], 2),
                "xs_fm_t_r24_x_sign_doi": ST.fmt(qx[2]["t"], 2),
                "quadrant_mean_fwd": qm}
            # crowding: contrarian -zG, D, extreme dummy; partial on r24, r7d
            rows = {}
            for name, sgn in {"minus_zG": -zG, "D": D, "minus_zT": -zT, "extreme": ext}.items():
                s = sgn[hm]
                uni = ts_pooled(y, [s], h)
                par = ts_pooled(y, [s, r24[hm], r7[hm]], h)
                icx = ST.cs_ic(s, y, h, min_n=8) if name != "extreme" else {"ic": None, "t": None}
                fm, _ = ST.fama_macbeth(ST.rank_cs(y), [ST.rank_cs(s), ST.rank_cs(r24[hm]), ST.rank_cs(r7[hm])], h, min_n=8) \
                    if name != "extreme" else ([{"t": None}], None)
                # non-overlapping pooled partial
                tno = []
                for off in range(h):
                    sl = slice(off, None, h)
                    r_ = ts_pooled(y[sl], [s[sl], r24[hm][sl], r7[hm][sl]], 1)
                    if r_ is not None:
                        tno.append(r_["t"][1])
                nz = int(np.nansum(np.abs(s))) if name == "extreme" else None
                rows[name] = {"ts_t_uni": ST.fmt(uni["t"][1], 2) if uni else None,
                              "ts_t_partial_nw": ST.fmt(par["t"][1], 2) if par else None,
                              "ts_b_partial_bp": ST.fmt(par["b"][1] * 1e4, 2) if par else None,
                              "ts_t_partial_nonoverlap": ST.fmt(float(np.mean(tno)), 2) if tno else None,
                              "n": par["n"] if par else 0, "extreme_count": nz,
                              "xs_ic": ST.fmt(icx["ic"]), "xs_t_ic": ST.fmt(icx["t"], 2),
                              "xs_fm_t_partial": ST.fmt(fm[0]["t"], 2)}
            out["crowding"][f"{hname}_{half}"] = rows
    return out


if __name__ == "__main__":
    p, m = load()
    res = {"flush_lag1": flush_study(p, m, lag=1), "flush_lag0_info": flush_study(p, m, lag=0)}
    F = sampled(p, m)
    del p, m
    res.update(quadrant_and_crowding(F))
    with open(os.path.join(os.path.dirname(HERE), "results", "_screen_bc.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps(res, indent=0, default=float)[:20000])
