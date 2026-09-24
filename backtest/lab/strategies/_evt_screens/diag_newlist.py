"""POST-HOC diagnostics for evt_newlist (not strategy candidates): why does the sign-flip null beat the fade?"""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest")
from lab import sim as S, wf, metrics as M
from lab.strategies import _evt_harness as H, evt_newlist as mod
P = H.load_for(mod)
out = json.load(open(r"C:\Users\The Affinity Zone\Documents\Claude Code\trading-bot\backtest\lab\results\evt_newlist.json"))
fn = lambda p, prm: mod.events(p, prm)
folds = out["wf"]["folds"]
# rebuild stitched OOS entries from the saved chosen params
ents = []
tt = np.asarray(P.t)
for f in folds:
    ib = int(np.searchsorted(tt, int(pd.Timestamp(f["test"][0]).timestamp())))
    ic = int(np.searchsorted(tt, int(pd.Timestamp(f["test"][1]).timestamp())))
    sig = wf._call(fn, S.slice_panel(P, 0, ic), f["chosen"], "events")
    ents.extend(e for e in sig["entries"] if ib <= e["i"] < ic)
a = int(np.searchsorted(tt, int(pd.Timestamp(folds[0]["test"][0]).timestamp())))
b = int(np.searchsorted(tt, int(pd.Timestamp(folds[-1]["test"][1]).timestamp())))
kw = H._sim_kw(mod)
base = H._run(P, ents, a, b, kw)
lng = H._run(P, [dict(e, side=1) for e in ents], a, b, kw)
nostop = H._run(P, [dict(e, stop_pct=None) for e in ents], a, b, kw)
wide = H._run(P, [dict(e, stop_pct=1.0) for e in ents], a, b, kw)
sub = S.slice_panel(P, a, b)
for name, r in (("short (strategy)", base), ("ALL LONG same events", lng), ("short no stop", nostop), ("short stop 100%", wide)):
    m = r.metrics()
    print(f"{name:24s} sharpe={m['sharpe']:.3f} cagr={m['cagr']:.4f} mdd={m['max_drawdown']:.4f} win={m['win_rate']:.3f} "
          f"liq={r.n_liquidations} hedged={H.hedge_overlay(sub, r)['sharpe']}")
# raw event study OOS: 60d return from the entry open, coin vs BTC
bj = P.symbols.index("BTCUSDT")
rows = []
for e in ents:
    i, j = e["i"] + 1, e["j"]
    k = min(i + 60 * 4, len(P.t) - 1)
    cj = P.c[i:k + 1, j]; cj = cj[np.isfinite(cj)]
    if not len(cj): continue
    rj = cj[-1] / P.o[i, j] - 1
    rb = P.c[k, bj] / P.o[i, bj] - 1
    mx = np.nanmax(P.h[i:k + 1, j]) / P.o[i, j] - 1
    rows.append((rj, rb, mx))
d = pd.DataFrame(rows, columns=["coin", "btc", "maxup"])
print("OOS entries", len(d), "median coin 60d", d.coin.median().round(4), "mean", d.coin.mean().round(4),
      "median btc", d.btc.median().round(4), "median rel", (d.coin - d.btc).median().round(4),
      "share coin<btc", ((d.coin < d.btc).mean()).round(3), "share maxup>=25%", (d.maxup >= 0.25).mean().round(3))
