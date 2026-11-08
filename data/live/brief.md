# v9 brief - 2026-11-08 18:15 UTC (signal from the 2026-11-08 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-41.94 (-21.0% of budget); from peak $-45.93

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.71 | 3.075 | -0.1% | -243.26 | -227.57 | +0.0084% |
| ETHUSDT | 1.3 | 3.608 | -0.2% | +0.00 | +0.00 | +0.0030% |
| SOLUSDT | 1.88 | 3.697 | -0.7% | -158.89 | -151.95 | +0.0100% |
| BNBUSDT | 0.83 | 2.724 | +0.1% | +0.00 | +0.00 | -0.0046% |
| XRPUSDT | 0.38 | 2.829 | -0.6% | +0.00 | +0.00 | +0.0041% |
| DOGEUSDT | 1.13 | 2.764 | -1.1% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.51 | 1.921 | -1.5% | +0.00 | +0.00 | -0.0037% |
| AVAXUSDT | 0.16 | 1.648 | -0.8% | +0.00 | +0.00 | +0.0044% |
| LINKUSDT | 1.09 | 1.851 | -2.2% | +0.00 | +0.00 | +0.0000% |
| LTCUSDT | 0.55 | 2.101 | -1.6% | +0.00 | +0.00 | -0.0049% |
| TRXUSDT | 0.32 | 1.247 | +0.1% | +0.00 | +0.00 | -0.0123% |
| DOTUSDT | -0.65 | 1.561 | -1.7% | +0.00 | +0.00 | -0.0119% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
