# v9 brief - 2026-11-06 15:20 UTC (signal from the 2026-11-06 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-42.64 (-21.3% of budget); from peak $-46.63

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.23 | 3.149 | -5.3% | -129.40 | +0.00 | +0.0057% |
| ETHUSDT | 2.14 | 3.987 | -7.3% | -89.12 | +0.00 | +0.0003% |
| SOLUSDT | 2.06 | 3.615 | -6.3% | -79.72 | +0.00 | -0.0001% |
| BNBUSDT | 1.55 | 2.86 | -2.9% | -103.02 | +0.00 | +0.0100% |
| XRPUSDT | 1.24 | 3.049 | -9.2% | +0.00 | +0.00 | +0.0020% |
| DOGEUSDT | 0.42 | 2.624 | -5.5% | +0.00 | +0.00 | -0.0021% |
| ADAUSDT | 0.08 | 1.906 | -5.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.31 | 1.719 | -4.1% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.08 | 1.829 | -5.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 1.69 | 2.346 | -5.0% | -78.74 | +0.00 | +0.0100% |
| TRXUSDT | -0.45 | 1.143 | -0.2% | +0.00 | +0.00 | -0.0022% |
| DOTUSDT | -0.61 | 1.577 | -2.2% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
