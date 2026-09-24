"""Add bug-hunt notes / robustness / screen evidence to the family-E module JSONs and
re-apply the (documented) family verdict rule. Run after the modules' run()."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from lab.strategies import _micro_harness as HX  # noqa: E402

RES = HX.RESULTS
rob = json.load(open(os.path.join(RES, "_micro_robustness.json")))

NOTES = {
    "micro_flowts": {
        "screen_evidence": "BTC W=24h residual flow z, controls r24+r7d: NW t train/test 2.25/2.49 (6h), 2.92/3.83 (24h), 2.96/1.69 (72h). ETH failed (results/micro_flowts_eth.json).",
        "bug_hunt": [
            "tbqv is summed (not last-valued) when data.py resamples 1h->6h (checked _resample).",
            "Sign-flip null p=0.01 is flattered: the FROZEN config is LONG-ONLY and the OOS folds 2023-2025 were a bull market, so flipping signs of long runs mostly makes them short. The random-timing (shift) null, which keeps the long exposure and moves it in time, gives p=0.079 (93rd pct) - not significant at 5%.",
            "OOS P&L is concentrated: folds 2023H2 +40% and 2024H1 +39%; 2022 -6.8%, 2024H2 -23%.",
            "First evaluation used per-asset vol scaling and ran at 10.5% realised vol (Sharpe 0.76, CAGR 7.7%); switched to book-level scaling so the stream is at ~20% vol (now 19%).",
        ],
        "extra_caveats": [
            "At $200, BTC minOrderQty 0.001 (~$60-100) makes small rebalances impossible: ~74% of order changes are below the minimum; round_to_qty OOS Sharpe 0.77 vs 0.81.",
        ],
    },
    "micro_flowxs": {
        "screen_evidence": "Pre-registered XS residual-z FAILED (results/micro_flowz_xs.json). The control 'raw rank(imb) next to rank(r_W), rank(r7d)' passed: FM t train/test 6.47/2.08 (W24,24h), 5.94/3.34 (W24,72h), 6.18/2.12 (W4,24h), 5.43/3.15 (W4,72h).",
        "bug_hunt": [
            "FROZEN is resid='none': plain cross-sectional rank of the 24h taker-buy share - a coin-level characteristic, weekly (H=28) overlapping hold.",
            "FUNDING is ~1/4 of the return: funding RECEIVED 8.9%/yr of equity OOS (funding_per_year -0.089). Dev-period frozen Sharpe 1.59 with funding vs 1.25 with funding=False. The long leg (high taker-buy share) tends to sit in negative-funding (short-crowded) coins - overlap with carry / short-squeeze exposure; check correlation with the carry modules.",
            "Leg split (dev, frozen): long leg alone Sharpe 0.99 (net long the market), short leg alone 0.03; daily corr with BTC of the combined book 0.09, mean net weight +0.025.",
            "Concentration: top-5 symbols (TRB, APT, BTC, SOL, SUI) = 55% of dev P&L over 206 names; TRB was the 2023 squeeze coin.",
            "Dev-period worst trade -451% of notional (DOGE short, Jan 2021 squeeze: -$30, ~15% of equity at the time); OOS worst trade -99% of notional; 2 delisting closes in OOS; no liquidations. Single-name short squeezes are the tail risk (no per-name stop in this weights book).",
            "Robust to an extra 6h decision lag (dev Sharpe 1.52 vs 1.59), 2x fees (1.46) and 3x slippage (1.31).",
            "Random-timing 'runs' null ignored for the verdict: its shuffled continuous weights trade 491x/yr vs 292x for the strategy (biased low).",
        ],
        "extra_caveats": [
            "49 symbols traded in the backtest are not in the current Bybit instrument list (delisted or renamed: MATIC->POL, RNDR->RENDER, FTM->S, 1000SHIB->SHIB1000, ...): live wiring needs a symbol map; historical names that no longer exist cannot be checked.",
            "~57% of order changes are below Bybit minimums at $200 (small stagger rebalances); round_to_qty OOS Sharpe 1.11 vs 1.17.",
        ],
    },
    "micro_crowd": {
        "screen_evidence": "Pooled Driscoll-Kraay partial t (controls r24, r7d) train/test: -zG 1.95/2.83 (6h), 2.49/2.00 (24h); D 2.19/3.28 (6h), 1.80/2.79 (24h). The phase-1 'extreme' rule failed (results/micro_crowd_extreme.json).",
        "bug_hunt": [
            "-zG correlates +0.36 with r24 and +0.26 with r7d (Binance retail L/S FALLS into rallies on the majors: contrarian retail), so part of the signal is short-term momentum. Regressing the frozen dev returns on 24h/7d/30d TSMOM baskets built the same way leaves an intercept of ~40%/yr (in-sample alpha Sharpe ~2.1): it is not just momentum.",
            "But the pre-registered PARTIAL form (zG residualised on r24, r7d per coin) is weak as a strategy (dev Sharpe 0.35); the tradable edge uses raw zG.",
            "FROZEN holds 6h (H=1). With the decision delayed one more 6h bar the dev Sharpe drops 1.58 -> 0.62: most of the edge is in the first 6h after the reading. The metric is taken as knowable at stamp + 5 min (data.load_metrics), which is exact or 5 min conservative per the data agent's verification.",
            "Decay: OOS 2023 +68% (Sharpe 2.35), 2024 +11% (0.58), 2025H1 -4.5% (-0.37); the last two walk-forward folds are negative.",
            "Fee drag 15%/yr (turnover 188x/yr); 2x fees -> dev Sharpe 1.06, 3x slippage -> 1.09.",
            "Long side carries it (dev long-leg Sharpe 1.68 vs short-leg 0.41); mean net exposure ~0.",
        ],
        "extra_caveats": [
            "Only 2.6 OOS years (metrics start 2021-12, 365d training).",
        ],
    },
    "micro_topxs": {
        "screen_evidence": "XS FM partial t train/test 0.48/3.61 (6h), 0.19/3.11 (24h), 0.87/2.68 (72h); pooled TS version wrong sign.",
        "bug_hunt": [
            "FROZEN is the raw rank (resid='none'), 72h overlapping hold.",
            "OOS 2025H1 -10%; fees matter: 2x fees -> dev Sharpe 0.21 (from 0.51).",
            "Random-timing 'runs' null ignored for the verdict (null turnover 1995x/yr vs 368x for the strategy).",
        ],
        "extra_caveats": [],
    },
    "micro_oiquad": {
        "screen_evidence": "TS interaction r24 x 1[dOI24<0] Driscoll-Kraay t train/test -1.36/-2.18 at 72h only (6h -1.24/-1.70, 24h -1.18/-0.84). XS FM form -2.59/-2.16 at 24h.",
        "bug_hunt": [
            "Fragile: FROZEN needs dOI24 <= -1 sigma; with thr=0 the dev Sharpe is -0.59. The XS variants have train Sharpe -3.8 / -2.4.",
            "Cost-fragile: 2x fees -> dev Sharpe 0.16, extra 6h lag -> 0.16 (from 0.52).",
            "Random-timing 'runs' null ignored for the verdict (null turnover 793x/yr vs 417x).",
        ],
        "extra_caveats": ["Parameter- and cost-fragile: do not deploy on this evidence."],
    },
}

for name, add in NOTES.items():
    p = os.path.join(RES, name + ".json")
    o = json.load(open(p))
    o["screen_evidence"] = add["screen_evidence"]
    o["bug_hunt"] = add["bug_hunt"]
    o["robustness_dev_frozen"] = rob.get(name)
    base_cav = [c for c in o.get("caveats", []) if c not in add["extra_caveats"]]
    v, cav = HX.default_verdict(o)
    o["verdict"] = v
    o["caveats"] = list(dict.fromkeys(base_cav + add["extra_caveats"] + cav))
    o["verdict_rule"] = HX.default_verdict.__doc__
    with open(p, "w") as f:
        json.dump(o, f, indent=1, default=HX._json_default)
    om = o["wf"]["oos_metrics"]
    print(name, v, om.get("sharpe"), om.get("cagr"), om.get("max_drawdown"), o["verdict_inputs"])
