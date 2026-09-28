# v9 brief - 2026-09-28 15:47 UTC (signal from the 2026-09-28 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-4.94 (-2.5% of budget); from peak $-5.33

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.59 | 1.36 | -2.1% | +0.00 | +0.00 | +0.0050% |
| ETHUSDT | 0.63 | 2.759 | -1.5% | +0.00 | +0.00 | +0.0068% |
| SOLUSDT | -0.42 | 1.82 | -4.2% | +0.00 | +82.88 | +0.0074% |
| BNBUSDT | -0.84 | 2.123 | -2.1% | +0.00 | +0.00 | -0.0110% |
| XRPUSDT | 0.59 | 2.459 | -2.9% | +0.00 | +0.00 | +0.0025% |
| DOGEUSDT | 0.52 | 2.554 | -4.8% | +0.00 | +0.00 | -0.0036% |
| ADAUSDT | 0.69 | 2.21 | -4.2% | +0.00 | +0.00 | +0.0000% |
| AVAXUSDT | 0.38 | 2.272 | -4.5% | +0.00 | +0.00 | +0.0054% |
| LINKUSDT | 1.84 | 1.96 | -1.4% | -73.43 | -73.15 | +0.0100% |
| LTCUSDT | 1.13 | 2.632 | -0.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.74 | 1.092 | -0.0% | +0.00 | +0.00 | -0.0333% |
| DOTUSDT | -0.28 | 1.954 | -4.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
