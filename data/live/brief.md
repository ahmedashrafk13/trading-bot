# v9 brief - 2026-11-14 17:58 UTC (signal from the 2026-11-14 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.36 (-1.7% of budget); from peak $-7.35

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.24 | 3.095 | -2.9% | +0.00 | +0.00 | +0.0099% |
| ETHUSDT | 0.8 | 3.525 | -2.5% | +0.00 | +0.00 | -0.0004% |
| SOLUSDT | 1.54 | 3.764 | -5.8% | -153.15 | +0.00 | -0.0026% |
| BNBUSDT | -0.65 | 2.507 | -3.5% | +0.00 | +0.00 | +0.0068% |
| XRPUSDT | 0.91 | 3.042 | -2.8% | +0.00 | +0.00 | +0.0043% |
| DOGEUSDT | -0.5 | 2.539 | -3.5% | +0.00 | +0.00 | +0.0005% |
| ADAUSDT | 1.45 | 2.019 | -4.8% | +0.00 | -117.25 | -0.0040% |
| AVAXUSDT | 1.91 | 2.205 | -4.3% | -122.18 | -98.42 | -0.0192% |
| LINKUSDT | -0.52 | 1.649 | -3.9% | +0.00 | +0.00 | -0.0058% |
| LTCUSDT | 0.83 | 2.148 | -1.6% | +0.00 | +0.00 | -0.0124% |
| TRXUSDT | -0.97 | 1.079 | +0.1% | +0.00 | +0.00 | -0.0790% |
| DOTUSDT | 0.25 | 1.688 | -5.0% | +0.00 | +0.00 | -0.0035% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
