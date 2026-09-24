"""Screen (d): liquidation-wick resting limit orders placed at each 6h run.

Pessimistic fill model (no 1m data): a resting limit at L fills only if a LATER
1h bar trades THROUGH it by >= 10 bps (low <= L*(1-0.001)); fill price = L
(never the better gap price). Maker 0.02% on entry. In the fill bar only the
stop can trigger (the low may come after the fill; the high may have come
before it). Later bars: open beyond stop -> open; low through stop -> stop (also
when the target is inside the same bar); high through target by >= 10 bps ->
target (maker). Otherwise closed at the close of the next run bar (taker).
Dev data only (end 2025-06-30). Writes results/_screen_d.json.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab import data, sim  # noqa: E402
from lab.strategies import _micro_stats as ST  # noqa: E402

END = "2025-06-30"
SYMS = data.MAJORS            # 16 long-lived majors
MAKER = 0.0002
TAKER = sim.DEFAULT_FEE
THROUGH = 0.001


def wick_trades(p, m_sig=3.0, tp_frac=0.5, sides=(1,), btc_filter=0.10, run_every=6,
                time_exit_runs=1):
    """Return a DataFrame of simulated trades (one row per fill)."""
    c, h, l, o = p.c, p.h, p.l, p.o
    T, N = c.shape
    lc = np.log(c)
    r1 = np.full_like(lc, np.nan)
    r1[1:] = lc[1:] - lc[:-1]
    sig = pd.DataFrame(r1).rolling(168, min_periods=120).std().to_numpy()
    jb = p.symbols.index("BTCUSDT")
    btc24 = np.full(T, np.nan)
    btc24[24:] = c[24:, jb] / c[:-24, jb] - 1.0
    slip = sim.default_slippage_bps(p.symbols) / 1e4
    tclose = p.t + p.dt
    runs = np.flatnonzero(tclose % (run_every * 3600) == 0)
    rows = []
    H = run_every * time_exit_runs
    for i in runs:
        if i + H >= T:
            break
        for j in range(N):
            P, s = c[i, j], sig[i, j]
            if not (np.isfinite(P) and np.isfinite(s) and s > 0) or not p.tradable[i, j]:
                continue
            dist = m_sig * s * np.sqrt(run_every)
            for side in sides:
                if side == 1 and np.isfinite(btc24[i]) and btc24[i] < -btc_filter:
                    continue
                if side == -1 and np.isfinite(btc24[i]) and btc24[i] > btc_filter:
                    continue
                L = P * (1 - side * dist)
                SL = L * (1 - side * dist)
                TP = L + tp_frac * (P - L)
                # fill search over bars i+1 .. i+run_every (order lives until next run)
                fill = None
                for k in range(i + 1, i + run_every + 1):
                    if not np.isfinite(l[k, j]):
                        break
                    if (side == 1 and l[k, j] <= L * (1 - THROUGH)) or (side == -1 and h[k, j] >= L * (1 + THROUGH)):
                        fill = k
                        break
                if fill is None:
                    continue
                k = fill
                exit_px, how = None, None
                # fill bar: stop only
                if (side == 1 and l[k, j] <= SL) or (side == -1 and h[k, j] >= SL):
                    exit_px, how, kx = SL, "stop", k
                else:
                    kx = k
                    for kk in range(k + 1, i + H + 1):
                        if not np.isfinite(o[kk, j]):
                            exit_px, how, kx = c[kk - 1, j] * (1 - side * 0.02), "gap", kk
                            break
                        if (side == 1 and o[kk, j] <= SL) or (side == -1 and o[kk, j] >= SL):
                            exit_px, how, kx = o[kk, j], "stop_gap", kk
                            break
                        if (side == 1 and l[kk, j] <= SL) or (side == -1 and h[kk, j] >= SL):
                            exit_px, how, kx = SL, "stop", kk
                            break
                        if (side == 1 and h[kk, j] >= TP * (1 + THROUGH)) or (side == -1 and l[kk, j] <= TP * (1 - THROUGH)):
                            exit_px, how, kx = TP, "target", kk
                            break
                    if exit_px is None:
                        exit_px, how, kx = c[i + H, j], "time", i + H
                gross = side * (exit_px / L - 1.0)
                cost = MAKER + (MAKER if how == "target" else TAKER + slip[j])
                rows.append({"run": int(i), "fill_bar": int(k), "exit_bar": int(kx), "j": j,
                             "sym": p.symbols[j], "side": side, "entry": L, "exit": exit_px,
                             "how": how, "ret": gross - cost, "gross": gross,
                             "stop_dist": dist, "t_run": int(tclose[i])})
    return pd.DataFrame(rows)


def summarise(df):
    if len(df) == 0:
        return {"n": 0}
    x = df["ret"].to_numpy()
    # cluster by run (cascades fill many symbols at once): equal notional per
    # fill, so the run's P&L is the SUM of its fills; t over all runs incl. zero-fill runs
    g = df.groupby("run")["ret"].sum()
    allruns = np.arange(df["run"].min(), df["run"].max() + 1, 6)
    g = g.reindex(allruns, fill_value=0.0).to_numpy()
    mm, tt, nn = ST.mean_nw_t(g, 1)
    return {"n": int(len(x)), "n_runs": int(nn), "mean_bp": round(float(x.mean() * 1e4), 1),
            "median_bp": round(float(np.median(x) * 1e4), 1),
            "t_iid": round(float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))), 2) if len(x) > 2 else None,
            "t_run_clustered": round(tt, 2) if np.isfinite(tt) else None,
            "win_rate": round(float((x > 0).mean()), 3),
            "p05_bp": round(float(np.percentile(x, 5) * 1e4), 1),
            "worst_bp": round(float(x.min() * 1e4), 1), "best_bp": round(float(x.max() * 1e4), 1),
            "exit_mix": df["how"].value_counts(normalize=True).round(3).to_dict(),
            "mean_ret_in_R": round(float((df["ret"] / (df["stop_dist"] * (1 - df["stop_dist"]))).mean()), 3)}


if __name__ == "__main__":
    p = data.load_panel("1h", universe="majors", start="2020-01-01", end=END)
    out = {"grid": {}}
    for m_sig in (2.5, 3.0, 4.0):
        for tp in (0.5, 1.0):
            for sides in ((1,), (1, -1)):
                df = wick_trades(p, m_sig=m_sig, tp_frac=tp, sides=sides)
                key = f"m{m_sig}_tp{tp}_{'long' if sides == (1,) else 'both'}"
                tr = df["t_run"] < ST.TRAIN_END
                te = (df["t_run"] >= ST.TRAIN_END) & (df["t_run"] < ST.TEST_END)
                yr = pd.to_datetime(df["t_run"], unit="s").dt.year
                out["grid"][key] = {"train": summarise(df[tr]), "test": summarise(df[te]),
                                    "by_year": {int(y): summarise(df[yr == y]) for y in sorted(yr.unique())},
                                    "long_test": summarise(df[te & (df["side"] == 1)]),
                                    "short_test": summarise(df[te & (df["side"] == -1)])}
                s1, s2 = out["grid"][key]["train"], out["grid"][key]["test"]
                print(key, "TRAIN", {k: s1.get(k) for k in ("n", "mean_bp", "t_run_clustered", "win_rate")},
                      "TEST", {k: s2.get(k) for k in ("n", "mean_bp", "t_run_clustered", "win_rate", "worst_bp")}, flush=True)
    with open(os.path.join(os.path.dirname(HERE), "results", "_screen_d.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
