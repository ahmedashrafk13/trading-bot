# v9 brief - 2026-11-25 07:23 UTC (signal from the 2026-11-25 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+18.57 (+9.3% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.21 | 2.698 | -2.4% | +0.00 | +0.00 | +0.0007% |
| ETHUSDT | -1.02 | 2.266 | -2.9% | +0.00 | +0.00 | +0.0034% |
| SOLUSDT | 1.44 | 3.81 | -4.3% | +0.00 | -102.91 | -0.0076% |
| BNBUSDT | -0.66 | 2.47 | -2.2% | +0.00 | +0.00 | +0.0011% |
| XRPUSDT | 0.34 | 2.896 | -4.2% | +0.00 | +0.00 | -0.0011% |
| DOGEUSDT | -0.56 | 2.43 | -3.8% | +0.00 | +0.00 | +0.0050% |
| ADAUSDT | 2.55 | 2.583 | -4.4% | -117.81 | -96.80 | +0.0028% |
| AVAXUSDT | -0.92 | 1.551 | -4.7% | +0.00 | +0.00 | -0.0049% |
| LINKUSDT | 1.15 | 1.938 | -4.1% | +0.00 | +0.00 | +0.0037% |
| LTCUSDT | -0.05 | 1.998 | -3.5% | +0.00 | +0.00 | +0.0040% |
| TRXUSDT | 1.35 | 1.341 | -0.1% | +0.00 | -179.16 | +0.0009% |
| DOTUSDT | 1.79 | 1.835 | -6.2% | -120.13 | -97.17 | -0.0040% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
