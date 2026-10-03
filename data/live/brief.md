# v9 brief - 2026-10-03 12:45 UTC (signal from the 2026-10-03 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-6.52 (-3.3% of budget); from peak $-6.90

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.01 | 1.221 | -2.0% | +0.00 | +0.00 | -0.0052% |
| ETHUSDT | 1.02 | 2.894 | -2.3% | +0.00 | +0.00 | -0.0009% |
| SOLUSDT | -0.1 | 1.876 | -2.1% | +0.00 | +0.00 | -0.0007% |
| BNBUSDT | 0.33 | 2.311 | -1.0% | +0.00 | +0.00 | -0.0096% |
| XRPUSDT | 1.89 | 2.672 | -3.0% | -112.58 | +0.00 | -0.0130% |
| DOGEUSDT | 0.9 | 2.672 | -3.9% | +0.00 | +0.00 | -0.0097% |
| ADAUSDT | 0.4 | 2.203 | -4.0% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.64 | 2.47 | +0.1% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.4 | 1.768 | -3.3% | +0.00 | -98.21 | -0.0010% |
| LTCUSDT | -0.11 | 2.358 | -0.3% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.55 | 1.133 | +0.6% | +0.00 | +0.00 | -0.0024% |
| DOTUSDT | -1.61 | 1.654 | -1.8% | +72.73 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
