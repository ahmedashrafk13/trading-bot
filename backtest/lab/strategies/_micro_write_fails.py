"""Write short 'fails' records for the family-E signals rejected at the screen."""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "results")


def load(n):
    with open(os.path.join(RES, n)) as f:
        return json.load(f)


def write(name, rec):
    rec.setdefault("verdict", "fails")
    rec.setdefault("oos_sharpe", None)
    with open(os.path.join(RES, name + ".json"), "w") as f:
        json.dump(rec, f, indent=1)


a = load("_screen_a.json")
bc = load("_screen_bc.json")
d = load("_screen_d.json")

# (a) pre-registered XS residual-z flow
xs = a["xs_pit_top20"]
write("micro_flowz_xs", {
    "name": "micro_flowz_xs",
    "description": "PIT top-20 cross-sectional rank of the TIME-SERIES-residualised taker-flow z (pre-registered signal a, XS form).",
    "mechanism": "Residual (not explained by the same-window return) taker buying predicts relative returns.",
    "universe": "pit_top20", "timeframe": "6h decisions (features from 1h klines)",
    "n_trials": 12, "stage": "screen only (Step 1)",
    "gate": "same sign train vs test AND |t| >= 2 in the test half (FM with rank(r_W), rank(r7d) controls, NW)",
    "ic_table": {k: {kk: v[kk] for kk in ("ic_z", "t_ic_z", "fm_rank_z_ctl", "t_fm_z_ctl_nw",
                                          "t_fm_z_ctl_nonoverlap_mean", "periods")} for k, v in xs.items()},
    "result": "fails: test-half controlled FM t between -1.91 and +0.14 in every W/horizon cell; sign flips vs train in 5 of 6 cells.",
    "note": "The CONTROL regression (raw rank imbalance next to rank(r_W), rank(r7d)) did pass and was built as micro_flowxs (flagged post-hoc).",
    "verdict": "fails", "caveats": ["Delisted coins' forward returns are dropped when the price series ends (mild survivorship in the IC)."],
})

# (a) ETH time-series (BTC passed)
ts = a["ts_btc_eth"]
write("micro_flowts_eth", {
    "name": "micro_flowts_eth",
    "description": "ETH time-series residualised taker-flow z (signal a), W in {4h,24h}, horizons 6h/24h/72h.",
    "mechanism": "as micro_flowts", "universe": ["ETHUSDT"], "timeframe": "6h decisions",
    "n_trials": 6, "stage": "screen only (Step 1)",
    "ic_table": {k: v["ETHUSDT"] for k, v in ts.items()},
    "result": "fails: controlled NW t in the test half <= 1.46 in every cell (same sign as train in only 2 of 6).",
    "verdict": "fails", "caveats": [],
})

# (b) OI flush
fl = bc["flush_lag1"]
write("micro_oiflush", {
    "name": "micro_oiflush",
    "description": "OI FLUSH reversal on the 12 metrics majors: 1h dOI <= -3 sigma (trailing 30d), 1-bar decision lag, fade the event bar's return.",
    "mechanism": "Forced liquidations (proxied by sharp OI drops) overshoot and revert.",
    "universe": "12 Binance-metrics majors", "timeframe": "1h events (6h-cadence variant also measured)",
    "n_trials": 9, "stage": "screen only (Step 1)",
    "control": "matched bars with the same |r_1h|/sigma bucket AND the same sign of r_1h, with no OI drop (dOI > -1 sigma)",
    "ic_table": {h: {half: {k: v[k] for k in ("events_raw_reversal", "excess_vs_matched_control", "excess_day_clustered",
                                                "cadence6h_raw_reversal", "cadence6h_day_clustered")}
                     for half, v in r.items() if half in ("train", "test")} for h, r in fl.items()},
    "by_year_excess_all": {h: r["all"]["excess_by_year"] for h, r in fl.items()},
    "result": ("fails: excess over the direction-matched control in the TEST half is +7.9 bp (6h, day-clustered t 1.06), "
               "-61.8 bp (24h) and -141 bp (72h); signs flip between halves and 2022 is negative at every horizon "
               "(spec needed the same sign in >= 4 of 5 years). With an |r|-only control (not direction-matched) the test "
               "half looked strongly positive (t ~7) - that was bull-market drift on 95%-long events plus cross-coin "
               "clustering, not a reversal edge."),
    "verdict": "fails", "caveats": ["Events cluster across coins in cascades: iid t-stats overstate by ~2-3x; day-clustered t reported."],
})

# (d) liquidation-wick limits
g = d["grid"]
write("micro_wick", {
    "name": "micro_wick",
    "description": ("Liquidation-wick resting limits: at each 6h run, limit buy at P*(1-m*sigma_1h*sqrt(6)) (optional mirror sell), "
                    "fill only if a later 1h bar trades through by >= 10 bp, TP at a partial retrace, SL one more m*sigma, "
                    "time exit at the next run; maker 0.02% entry, taker on stop; longs skipped when BTC 24h < -10%."),
    "mechanism": "Providing liquidity into forced liquidation cascades earns a premium.",
    "universe": "16 long-lived majors (lab MAJORS)", "timeframe": "1h bars, orders refreshed at 6h runs",
    "n_trials": len(g), "stage": "screen only (Step 1) - own pessimistic simulator (sim.run_events has no limit entries)",
    "grid_table": {k: {"train": v["train"], "test": v["test"]} for k, v in g.items()},
    "by_year": {k: {y: {kk: s.get(kk) for kk in ("n", "mean_bp", "win_rate")} for y, s in v["by_year"].items()} for k, v in g.items()},
    "result": ("fails: >= 100 OOS fills in every config (378-2505), but the test-half mean net return per fill is negative in 11 of 12 configs "
               "(-51.4 to -1.6 bp) and +5.7 bp (run-clustered t 0.10) in the best; train-half means were small and insignificant too "
               "(best +46.6 bp, t 1.25). Worst fills -10% to -14% of notional."),
    "verdict": "fails",
    "caveats": ["No 1m data: fills require a 10 bp trade-through and the stop is assumed hit first inside the fill bar (pessimistic).",
                "Funding ignored (holds < 6h)."],
})

# (c) crowding extremes rule (the phase-1 rule) - record
cr = bc["crowding"]
write("micro_crowd_extreme", {
    "name": "micro_crowd_extreme",
    "description": "Phase-1 rule: short when zG >= 2 and D <= -1, long when zG <= -2 and D >= 1 (12 metrics majors).",
    "mechanism": "Retail crowded one way while top accounts lean the other.",
    "universe": "12 Binance-metrics majors", "timeframe": "6h decisions", "n_trials": 3, "stage": "screen only (Step 1)",
    "ic_table": {k: v["extreme"] for k, v in cr.items()},
    "result": "fails: pooled Driscoll-Kraay partial t in the test half 1.66 (6h), 1.25 (24h), 0.72 (72h). The continuous -zG / D signals passed and are in micro_crowd.",
    "verdict": "fails", "caveats": [],
})
print("written")
