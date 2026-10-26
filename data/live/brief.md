# v9 brief - 2026-10-26 18:12 UTC (signal from the 2026-10-26 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-23.89 (-11.9% of budget); from peak $-27.88

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.73 | 2.188 | -0.6% | -105.54 | -240.92 | +0.0100% |
| ETHUSDT | 1.23 | 3.281 | -1.4% | +0.00 | -139.59 | +0.0076% |
| SOLUSDT | 1.58 | 2.994 | -0.6% | -62.04 | +0.00 | +0.0100% |
| BNBUSDT | 0.95 | 2.539 | +0.3% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 2.03 | 3.179 | -0.6% | -63.38 | +0.00 | +0.0079% |
| DOGEUSDT | 1.08 | 2.664 | +0.3% | +0.00 | +0.00 | -0.0019% |
| ADAUSDT | -0.97 | 1.813 | +0.1% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.71 | 1.606 | +0.4% | +0.00 | +0.00 | +0.0021% |
| LINKUSDT | -0.5 | 1.61 | -0.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.08 | 2.078 | -0.3% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 2.13 | 1.47 | +0.3% | -214.94 | +0.00 | -0.0289% |
| DOTUSDT | -1.63 | 1.52 | -2.8% | +34.10 | +77.03 | +0.0094% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
