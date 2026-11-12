# v9 brief - 2026-11-12 18:14 UTC (signal from the 2026-11-12 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-27.72 (-13.9% of budget); from peak $-31.71

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.49 | 3.163 | -3.5% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | 0.96 | 3.564 | -3.5% | +0.00 | +0.00 | +0.0084% |
| SOLUSDT | 1.39 | 3.61 | -4.3% | +0.00 | +0.00 | +0.0028% |
| BNBUSDT | -0.31 | 2.559 | -4.6% | +0.00 | +0.00 | -0.0044% |
| XRPUSDT | 1.1 | 3.07 | -3.6% | +0.00 | +0.00 | -0.0015% |
| DOGEUSDT | -1.21 | 2.434 | -4.4% | +0.00 | +0.00 | -0.0072% |
| ADAUSDT | 1.71 | 2.005 | -4.3% | -130.20 | -129.71 | -0.0051% |
| AVAXUSDT | 3.07 | 2.393 | -3.7% | -115.12 | -109.68 | -0.0081% |
| LINKUSDT | 0.49 | 1.796 | -4.9% | +0.00 | +0.00 | +0.0009% |
| LTCUSDT | 0.05 | 1.995 | -3.4% | +0.00 | +0.00 | -0.0128% |
| TRXUSDT | -0.57 | 1.135 | -0.1% | +0.00 | +0.00 | +0.0023% |
| DOTUSDT | 0.06 | 1.665 | -4.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
