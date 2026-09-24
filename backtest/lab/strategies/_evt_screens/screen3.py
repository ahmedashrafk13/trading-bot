"""Screen 3 (b)/(c) with crowd metrics, on the FIRST metrics-era train window only:
2021-12-01 .. 2023-11-30 (the walk-forward for these ideas starts its first test fold 2023-12)."""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest")
from lab import data
ST, END = "2021-12-01", "2023-11-30"
p = data.load_panel("6h", universe="pit_top50", start=ST, end=END)
T, N = p.c.shape
syms = json.load(open(r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\data\hist\metric_symbols_ext.json"))
m = data.load_metrics(p.symbols, "6h", start=ST, end=END)
print("panel", p.c.shape, "coins with any OI:", int(np.isfinite(m["oi_value"]).any(0).sum()))
valid = p.meta["valid"]; elig = p.tradable
o, h, l, c, f = p.o, p.h, p.l, p.c, p.funding
bj = p.symbols.index("BTCUSDT")
COST = 2 * (0.00055 + 0.0008); BPD = 4
exec(open(r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest\lab\strategies\_evt_screens\common_fns.py").read())
F3 = pd.DataFrame(f).rolling(12, min_periods=12).sum().to_numpy()
cc = pd.DataFrame(c).ffill(limit=2).to_numpy()
R7 = cc / np.roll(cc, 28, 0) - 1; R7[:28] = np.nan
lo7 = pd.DataFrame(l).rolling(28, min_periods=20).min().to_numpy()
rk = pd.DataFrame(np.where(elig, R7, np.nan)).rank(axis=1, pct=True).to_numpy()
oi = m["oi_value"]; ls = m["ls_ratio"]; tls = m["top_ls_ratio"]
oich = oi / np.roll(oi, 12, 0) - 1; oich[:12] = np.nan
def z30(x):
    lx = np.log(x)
    d = pd.DataFrame(lx)
    return ((d - d.rolling(120, min_periods=60).mean()) / d.rolling(120, min_periods=60).std()).to_numpy()
lsz = z30(ls); tlsz = z30(tls)
def dedupe(cands, gap):
    last = {}; out = []
    for i, j in cands:
        if i - last.get(j, -10**9) >= gap:
            out.append((i, j)); last[j] = i
    return out
def run(name, mask, side, H, stopf):
    ii, jj = np.nonzero(mask[:-1]); order = np.argsort(ii, kind="stable")
    cands = dedupe(list(zip(ii[order], jj[order])), H * BPD)
    ev = []
    for i, j in cands:
        x = trade(i, j, side, H * BPD, stopf(i, j), hedge=True)
        if x: ev.append(x)
    summarize(name, ev)
nn = lambda a, v: np.nan_to_num(a, nan=v)
has = np.isfinite(oi)
print("== (b) pump + crowd fade, metrics era (only coins with metrics)")
top = (rk >= 0.9) & has
run("b0 price-only top-decile (metrics coins) H=3", top, -1, 3, lambda i, j: 0.25)
for H in (3, 7):
    run(f"b F3z-free F3>=0.0015 H={H}", top & (nn(F3, -9) >= 0.0015), -1, H, lambda i, j: 0.25)
    run(f"b OI3d>=+10% H={H}", top & (nn(oich, -9) >= 0.10), -1, H, lambda i, j: 0.25)
    run(f"b lsz>=1 H={H}", top & (nn(lsz, -9) >= 1.0), -1, H, lambda i, j: 0.25)
    run(f"b OI>=10% & F3>=.0015 H={H}", top & (nn(oich, -9) >= 0.10) & (nn(F3, -9) >= 0.0015), -1, H, lambda i, j: 0.25)
    run(f"b OI>=10% & lsz>=1 H={H}", top & (nn(oich, -9) >= 0.10) & (nn(lsz, -9) >= 1.0), -1, H, lambda i, j: 0.25)
    run(f"b OI>=10% & F3>=.0015 & lsz>=0.5 H={H}", top & (nn(oich, -9) >= 0.10) & (nn(F3, -9) >= 0.0015) & (nn(lsz, -9) >= 0.5), -1, H, lambda i, j: 0.25)
print("== (c) squeeze harvest, metrics era")
stp = lambda i, j: 1 - lo7[i, j] / c[i, j] + 0.01
base = elig & (c >= lo7 * 1.05)
for fth in (-0.001, -0.003):
    for H in (3, 7):
        run(f"c F3<={fth} H={H} (all top50)", base & (nn(F3, 9) <= fth), +1, H, stp)
        run(f"c F3<={fth} & OI3d>=+5% H={H}", base & (nn(F3, 9) <= fth) & (nn(oich, -9) >= 0.05), +1, H, stp)
        run(f"c F3<={fth} & lsz<=-1 H={H}", base & (nn(F3, 9) <= fth) & (nn(lsz, 9) <= -1.0), +1, H, stp)
        run(f"c F3<={fth} & tlsz<=-1 H={H}", base & (nn(F3, 9) <= fth) & (nn(tlsz, 9) <= -1.0), +1, H, stp)
