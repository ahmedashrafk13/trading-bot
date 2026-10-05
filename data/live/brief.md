# v9 brief - 2026-10-05 06:12 UTC (signal from the 2026-10-05 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.28 (-3.6% of budget); from peak $-7.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.12 | 0.994 | +1.0% | +0.00 | +0.00 | +0.0033% |
| ETHUSDT | -0.42 | 2.499 | +0.4% | +0.00 | +0.00 | +0.0009% |
| SOLUSDT | -0.85 | 1.685 | -0.3% | +0.00 | +0.00 | -0.0046% |
| BNBUSDT | -0.37 | 2.184 | +0.7% | +0.00 | +0.00 | +0.0095% |
| XRPUSDT | -0.77 | 2.305 | +1.0% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.17 | 2.451 | +2.7% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.26 | 2.17 | +10.6% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.48 | 2.124 | -1.3% | +0.00 | +0.00 | -0.0048% |
| LINKUSDT | 0.34 | 1.768 | +0.7% | +0.00 | +0.00 | +0.0042% |
| LTCUSDT | -1.13 | 2.116 | -1.1% | +0.00 | +0.00 | +0.0041% |
| TRXUSDT | -0.44 | 1.163 | -0.2% | +0.00 | +0.00 | -0.0477% |
| DOTUSDT | -1.4 | 1.673 | +2.9% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
