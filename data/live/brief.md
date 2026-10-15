# v9 brief - 2026-10-15 12:18 UTC (signal from the 2026-10-15 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+3.86 (+1.9% of budget); from peak $-0.13

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.65 | 1.779 | -3.0% | -140.66 | -80.99 | +0.0046% |
| ETHUSDT | 1.2 | 3.151 | -5.6% | +0.00 | +0.00 | +0.0058% |
| SOLUSDT | 2.03 | 2.63 | -4.6% | -81.75 | -61.34 | +0.0072% |
| BNBUSDT | 2.42 | 2.595 | -3.0% | -131.78 | -100.93 | +0.0044% |
| XRPUSDT | 1.36 | 2.675 | -4.9% | +0.00 | -58.31 | +0.0048% |
| DOGEUSDT | -0.49 | 2.376 | -4.9% | +0.00 | +0.00 | +0.0052% |
| ADAUSDT | -1.33 | 1.828 | -5.8% | +0.00 | +0.00 | +0.0009% |
| AVAXUSDT | -2.12 | 1.546 | -6.3% | +45.80 | +36.56 | -0.0102% |
| LINKUSDT | -0.46 | 1.578 | -6.7% | +0.00 | +0.00 | +0.0038% |
| LTCUSDT | 0.21 | 2.223 | -4.8% | +0.00 | +0.00 | -0.0028% |
| TRXUSDT | 1.33 | 1.299 | -0.8% | +0.00 | +0.00 | -0.0073% |
| DOTUSDT | -0.23 | 1.848 | -5.2% | +0.00 | +0.00 | +0.0054% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
