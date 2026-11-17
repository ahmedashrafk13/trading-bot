# v9 brief - 2026-11-17 17:30 UTC (signal from the 2026-11-17 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.99 (-1.5% of budget); from peak $-6.98

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.79 | 2.869 | +0.9% | +0.00 | +0.00 | +0.0039% |
| ETHUSDT | -0.6 | 2.743 | +0.9% | +0.00 | +0.00 | -0.0060% |
| SOLUSDT | 0.11 | 3.186 | +3.0% | +0.00 | +0.00 | -0.0135% |
| BNBUSDT | -0.92 | 2.44 | +0.8% | +0.00 | +0.00 | -0.0049% |
| XRPUSDT | -0.3 | 2.736 | +1.6% | +0.00 | +0.00 | -0.0081% |
| DOGEUSDT | -1.69 | 2.351 | +1.0% | +147.71 | +147.43 | -0.0022% |
| ADAUSDT | 2.11 | 2.163 | +1.4% | -127.45 | -129.05 | -0.0106% |
| AVAXUSDT | -0.42 | 1.593 | +1.5% | +0.00 | +0.00 | -0.0056% |
| LINKUSDT | -0.17 | 1.717 | +1.2% | +0.00 | +0.00 | -0.0067% |
| LTCUSDT | 0.46 | 2.077 | +1.4% | +0.00 | +0.00 | +0.0029% |
| TRXUSDT | -0.61 | 1.092 | +0.3% | +0.00 | +0.00 | -0.0229% |
| DOTUSDT | 0.99 | 1.799 | +0.9% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
