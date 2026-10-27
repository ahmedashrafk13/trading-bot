# v9 brief - 2026-10-27 12:12 UTC (signal from the 2026-10-27 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.77 (-11.4% of budget); from peak $-26.76

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.89 | 2.343 | -0.6% | -169.09 | -159.75 | +0.0100% |
| ETHUSDT | 1.52 | 3.417 | -0.8% | -110.40 | -92.53 | +0.0034% |
| SOLUSDT | 1.59 | 3.039 | -1.6% | -99.22 | -89.98 | +0.0005% |
| BNBUSDT | 1.29 | 2.626 | -0.4% | +0.00 | +0.00 | +0.0098% |
| XRPUSDT | 1.7 | 3.11 | +0.7% | -101.29 | -101.43 | +0.0056% |
| DOGEUSDT | 1.32 | 2.705 | -0.1% | +0.00 | +0.00 | +0.0036% |
| ADAUSDT | -0.65 | 1.873 | -0.8% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.78 | 1.567 | -2.5% | +0.00 | +0.00 | +0.0051% |
| LINKUSDT | -0.69 | 1.576 | -1.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.19 | 2.091 | -0.9% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.57 | 1.121 | -0.8% | +0.00 | +0.00 | -0.0338% |
| DOTUSDT | -1.42 | 1.546 | -4.0% | +0.00 | +0.00 | -0.0101% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
