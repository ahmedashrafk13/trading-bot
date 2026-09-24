"""Train-only screen 2 for (a): funding floor, membership depth, per-event detail."""
import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest\lab\strategies\_evt_screens")
exec(open(r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest\lab\strategies\_evt_screens\screen1.py").read().split("# ---------------- (a)")[0])
U = data.pit_rank_table()
t_day = (p.t - U["day0"]) // 86400
rank_bar = np.full((T, N), -1, np.int16)
for j, s in enumerate(p.symbols):
    k = U["symbols"].index(s)
    di = np.clip(t_day, 0, U["rank"].shape[0] - 1)
    rank_bar[:, j] = U["rank"][di, k]
first = np.array([np.flatnonzero(np.isfinite(c[:, j]))[0] if np.isfinite(c[:, j]).any() else -1 for j in range(N)])
F3 = pd.DataFrame(f).rolling(8, min_periods=1).sum().to_numpy()   # trailing 2d funding
for K in (30, 60):
    for floor in (None, -0.002):
        for d0, Hd in ((7, 30), (14, 30), (14, 60)):
            ev = []
            for j in range(N):
                if first[j] <= 0 or p.symbols[j] == "BTCUSDT":
                    continue
                lo, hi = first[j] + d0 * BPD, first[j] + (d0 + 14) * BPD
                cand = [i for i in range(lo, min(hi, T - 1)) if 0 <= rank_bar[i, j] < K and valid[i, j]
                        and (floor is None or F3[i, j] >= floor)]
                if cand:
                    x = trade(cand[0], j, -1, Hd * BPD, 0.4, hedge=True)
                    if x: x["sym"] = p.symbols[j]; ev.append(x)
            summarize(f"a K={K} floor={floor} d0={d0} H={Hd} stop=.4", ev)
            if K == 60 and floor is None and d0 == 14 and Hd == 30:
                d = pd.DataFrame(ev); d["t"] = pd.to_datetime(p.t[d.i], unit="s")
                print(d.sort_values("net")[["sym", "t", "r", "fund", "net", "stopped", "days"]].to_string())
