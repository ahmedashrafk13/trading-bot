# v9 brief - 2026-10-06 18:12 UTC (signal from the 2026-10-06 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-8.70 (-4.3% of budget); from peak $-9.08

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.87 | 1.043 | +0.3% | +0.00 | +0.00 | +0.0049% |
| ETHUSDT | -0.23 | 2.549 | -0.2% | +0.00 | +0.00 | +0.0054% |
| SOLUSDT | -1.09 | 1.619 | +0.7% | +0.00 | +0.00 | +0.0015% |
| BNBUSDT | -0.45 | 2.195 | -0.6% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.81 | 2.285 | +0.7% | +0.00 | +140.11 | -0.0026% |
| DOGEUSDT | 0.48 | 2.559 | +0.1% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.5 | 2.559 | +3.1% | -124.38 | +0.00 | +0.0100% |
| AVAXUSDT | -0.11 | 2.224 | +5.9% | +0.00 | +0.00 | -0.0049% |
| LINKUSDT | -0.35 | 1.62 | +0.7% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.87 | 1.93 | -2.1% | +136.93 | +131.38 | -0.0037% |
| TRXUSDT | -0.37 | 1.179 | -0.2% | +0.00 | +0.00 | -0.0329% |
| DOTUSDT | -0.41 | 1.872 | +2.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
