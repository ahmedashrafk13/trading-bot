# v9 brief - 2026-10-27 06:05 UTC (signal from the 2026-10-27 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.62 (-11.3% of budget); from peak $-26.61

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.99 | 2.376 | -0.4% | -169.09 | -79.89 | +0.0037% |
| ETHUSDT | 1.5 | 3.4 | -0.5% | -110.40 | +0.00 | +0.0022% |
| SOLUSDT | 1.79 | 3.151 | -1.3% | -99.22 | -60.00 | -0.0030% |
| BNBUSDT | 1.43 | 2.652 | -0.5% | +0.00 | +0.00 | +0.0000% |
| XRPUSDT | 1.75 | 3.115 | +0.7% | -101.29 | -63.44 | +0.0100% |
| DOGEUSDT | 1.36 | 2.706 | +0.4% | +0.00 | +0.00 | -0.0097% |
| ADAUSDT | -0.57 | 1.893 | +0.0% | +0.00 | +0.00 | -0.0045% |
| AVAXUSDT | -0.7 | 1.599 | -1.4% | +0.00 | +0.00 | -0.0038% |
| LINKUSDT | -0.77 | 1.567 | -0.6% | +0.00 | +0.00 | -0.0054% |
| LTCUSDT | 0.01 | 2.057 | -0.3% | +0.00 | +0.00 | +0.0029% |
| TRXUSDT | 0.67 | 1.273 | -0.4% | +0.00 | -213.68 | -0.0412% |
| DOTUSDT | -1.45 | 1.546 | -2.4% | +0.00 | +33.09 | -0.0122% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
