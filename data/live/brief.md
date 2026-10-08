# v9 brief - 2026-10-08 18:50 UTC (signal from the 2026-10-08 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-4.79 (-2.4% of budget); from peak $-5.17

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.86 | 1.855 | -2.9% | -124.33 | -81.48 | +0.0061% |
| ETHUSDT | 2.1 | 3.392 | -5.2% | -94.38 | -97.83 | -0.0011% |
| SOLUSDT | 1.58 | 2.305 | -8.6% | -73.27 | +0.00 | -0.0080% |
| BNBUSDT | 0.82 | 2.411 | -6.2% | +0.00 | +0.00 | -0.0304% |
| XRPUSDT | 1.51 | 2.63 | -6.5% | -62.24 | +0.00 | -0.0037% |
| DOGEUSDT | -0.45 | 2.385 | -7.8% | +0.00 | +0.00 | -0.0185% |
| ADAUSDT | 0.25 | 2.222 | -11.6% | +0.00 | +0.00 | -0.0206% |
| AVAXUSDT | -0.49 | 2.102 | -12.6% | +0.00 | +0.00 | -0.0013% |
| LINKUSDT | -0.36 | 1.601 | -8.8% | +0.00 | +0.00 | -0.0131% |
| LTCUSDT | -1.0 | 2.063 | -7.0% | +0.00 | +68.28 | +0.0073% |
| TRXUSDT | -0.17 | 1.216 | -0.7% | +0.00 | +0.00 | -0.0127% |
| DOTUSDT | -1.52 | 1.618 | -7.3% | +45.78 | +45.39 | -0.0081% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
