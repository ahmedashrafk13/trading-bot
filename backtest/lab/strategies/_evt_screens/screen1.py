"""Train-only screen (2020-01-01 .. 2021-12-31, the first walk-forward train window).
Per-event forward returns from the NEXT open, short side sign applied, with an
approximate cost of 2 x (5.5 + 8) bp and funding (short receives +funding)."""
import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest")
from lab import data
END = "2021-12-31"
p = data.load_panel("6h", universe="pit_top60", end=END)
T, N = p.c.shape
mem = p.meta["member"]; valid = p.meta["valid"]
o, h, l, c, f = p.o, p.h, p.l, p.c, p.funding
bj = p.symbols.index("BTCUSDT")
COST = 2 * (0.00055 + 0.0008)
BPD = 4

def trade(i, j, side, H, stop=None, hedge=False):
    """enter at o[i+1]; exit at o[i+1+H] or stop (intrabar, pessimistic at stop or open gap)."""
    a = i + 1
    if a >= T or not np.isfinite(o[a, j]):
        return None
    e = o[a, j]
    b = min(a + H, T - 1)
    ex = None; k_exit = b
    for k in range(a, b):
        if not np.isfinite(h[k, j]):
            ex = c[k - 1, j] if k > a and np.isfinite(c[k - 1, j]) else e; k_exit = k; break
        if stop is not None:
            sp = e * (1 + stop) if side < 0 else e * (1 - stop)
            if side < 0 and h[k, j] >= sp:
                ex = max(sp, o[k, j]); k_exit = k + 1; break
            if side > 0 and l[k, j] <= sp:
                ex = min(sp, o[k, j]); k_exit = k + 1; break
    if ex is None:
        ex = o[b, j] if np.isfinite(o[b, j]) else c[b - 1, j]
    r = side * (ex / e - 1)
    fund = -side * np.nansum(f[a:k_exit, j])  # short receives positive funding
    rb = 0.0
    if hedge:
        eb = o[a, bj]; xb = o[min(k_exit, T - 1), bj]
        rb = -side * (xb / eb - 1)            # opposite BTC leg, beta 1
    return dict(i=i, j=j, r=r, fund=fund, rb=rb, net=r + fund - COST, neth=r + rb + fund - 2 * COST,
                stopped=k_exit < b, days=(k_exit - a) / BPD)

def summarize(name, ev):
    if not ev:
        print(name, "no events"); return
    d = pd.DataFrame(ev)
    d["t"] = pd.to_datetime(p.t[d.i], unit="s")
    yr = d.groupby(d.t.dt.year).net.agg(["size", "mean"]).round(4).to_dict("index")
    print(f"{name:42s} n={len(d):4d} gross={d.r.mean():+.4f} fund={d.fund.mean():+.4f} net={d.net.mean():+.4f} "
          f"med={d.net.median():+.4f} hit={(d.net>0).mean():.2f} worst={d.net.min():+.3f} hedged={d.neth.mean():+.4f} "
          f"stop%={d.stopped.mean():.2f} t={d.net.mean()/d.net.std()*np.sqrt(len(d)):.2f} yr={yr}")

# ---------------- (a) new-listing fade ----------------
first = np.array([np.flatnonzero(np.isfinite(c[:, j]))[0] if np.isfinite(c[:, j]).any() else -1 for j in range(N)])
print("== (a) new-listing fade (entry = first 6h bar with age>=d0 and PIT top-60 member, age<=d0+14d)")
for d0 in (2, 7, 14):
    for Hd in (30, 60, 90):
        for stop in (None, 0.4, 1.0):
            ev = []
            for j in range(N):
                if first[j] <= 0 or p.symbols[j] == "BTCUSDT":
                    continue
                lo, hi = first[j] + d0 * BPD, first[j] + (d0 + 14) * BPD
                cand = [i for i in range(lo, min(hi, T - 1)) if mem[i, j] and valid[i, j]]
                if cand:
                    x = trade(cand[0], j, -1, Hd * BPD, stop, hedge=True)
                    if x: ev.append(x)
            summarize(f"a d0={d0} H={Hd} stop={stop}", ev)

# ---------------- funding features ----------------
F3 = pd.DataFrame(f).rolling(12, min_periods=12).sum().to_numpy()          # 3d funding sum
F3z = (F3 - pd.DataFrame(F3).rolling(240, min_periods=120).mean().to_numpy()) / pd.DataFrame(F3).rolling(240, min_periods=120).std().to_numpy()
cc = pd.DataFrame(c).ffill(limit=2).to_numpy()
R7 = cc / np.roll(cc, 28, 0) - 1; R7[:28] = np.nan
lo7 = pd.DataFrame(l).rolling(28, min_periods=20).min().to_numpy()
mem50 = mem  # top-60 here; module uses pit_top50
elig = mem50 & valid
R7e = np.where(elig, R7, np.nan)
rk = pd.DataFrame(R7e).rank(axis=1, pct=True).to_numpy()

def dedupe(cands, gap):
    last = {}
    out = []
    for i, j in cands:
        if i - last.get(j, -10**9) >= gap:
            out.append((i, j)); last[j] = i
    return out

print("== (b) pump + crowd fade (short)")
for fz in (0, 1.0, 2.0):
    for fabs in (0.0, 0.0015, 0.003):
        for H in (3, 7):
            for stop in (0.25,):
                m = (rk >= 0.9) & (np.nan_to_num(F3z, nan=-9) >= fz) & (np.nan_to_num(F3, nan=-9) >= fabs)
                ii, jj = np.nonzero(m[:-1])
                order = np.argsort(ii, kind="stable")
                cands = dedupe(list(zip(ii[order], jj[order])), H * BPD)
                ev = [x for x in (trade(i, j, -1, H * BPD, stop, hedge=True) for i, j in cands) if x]
                summarize(f"b fz>={fz} F3>={fabs} H={H}d stop={stop}", ev)
print("   (b0) price-only control: top-decile 7d return, no crowd filter")
m = (rk >= 0.9); ii, jj = np.nonzero(m[:-1]); order = np.argsort(ii, kind="stable")
cands = dedupe(list(zip(ii[order], jj[order])), 7 * BPD)
summarize("b0 price only H=7 stop=.25", [x for x in (trade(i, j, -1, 28, 0.25, True) for i, j in cands) if x])

print("== (c) squeeze harvest (long)")
for fth in (-0.001, -0.003, -0.006):
    for hold in (0.03, 0.08):
        for H in (3, 7):
            m = elig & (np.nan_to_num(F3, nan=9) <= fth) & (c >= lo7 * (1 + hold))
            ii, jj = np.nonzero(m[:-1]); order = np.argsort(ii, kind="stable")
            cands = dedupe(list(zip(ii[order], jj[order])), H * BPD)
            ev = []
            for i, j in cands:
                st = 1 - lo7[i, j] / c[i, j] + 0.01
                x = trade(i, j, +1, H * BPD, st, hedge=True)
                if x: ev.append(x)
            summarize(f"c F3<={fth} >{hold:.2f} over 7d low H={H}d", ev)

print("== (d) first entry into PIT top-20 (long/short both shown as LONG)")
U = data.pit_rank_table()
# first time the coin is ranked < 20 on the daily table, only coins whose first bar is after 2020-01-01 + 30d
t_day = (p.t - U["day0"]) // 86400
rank = U["rank"]; usy = U["symbols"]
for H in (7, 14, 30):
    ev = []
    for j, s in enumerate(p.symbols):
        if s not in usy: continue
        k = usy.index(s)
        r = rank[:, k]
        top = np.flatnonzero((r >= 0) & (r < 20))
        if not len(top): continue
        d_first = top[0]
        # bar = first 6h bar of that day (membership known at 00:00 of that day)
        ib = np.searchsorted(t_day, d_first)
        if ib <= 120 or ib >= T - 1: continue   # need history: skip coins already top-20 at data start
        x = trade(ib, j, +1, H * BPD, 0.3, hedge=True)
        if x: ev.append(x)
    summarize(f"d first-top20 LONG H={H}d stop=.3", ev)
for H in (7, 14, 30):
    ev = []
    for j, s in enumerate(p.symbols):
        if s not in usy: continue
        k = usy.index(s); r = rank[:, k]
        inn = (r >= 0) & (r < 50)
        # exits from top-50 after >= 60 days inside
        runs = np.flatnonzero(inn[:-1] & ~inn[1:]) + 1
        for d_out in runs:
            if inn[max(0, d_out - 60):d_out].mean() < 0.95: continue
            ib = np.searchsorted(t_day, d_out)
            if ib <= 0 or ib >= T - 1: continue
            x = trade(ib, j, -1, H * BPD, 0.3, hedge=True)
            if x: ev.append(x)
    summarize(f"d leaves-top50 SHORT H={H}d stop=.3", ev)
