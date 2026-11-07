# v9 brief - 2026-11-07 18:10 UTC (signal from the 2026-11-07 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-42.63 (-21.3% of budget); from peak $-46.62

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.87 | 3.072 | +0.1% | -235.52 | -151.67 | +0.0100% |
| ETHUSDT | 1.17 | 3.505 | +0.4% | +0.00 | -134.20 | +0.0100% |
| SOLUSDT | 1.93 | 3.636 | -0.3% | -151.89 | -125.77 | +0.0100% |
| BNBUSDT | 1.11 | 2.779 | +0.1% | +0.00 | +0.00 | -0.0111% |
| XRPUSDT | 0.48 | 2.848 | -2.0% | +0.00 | +0.00 | +0.0012% |
| DOGEUSDT | 1.15 | 2.754 | -1.3% | +0.00 | +0.00 | -0.0033% |
| ADAUSDT | 0.94 | 1.969 | -3.0% | +0.00 | +0.00 | -0.0025% |
| AVAXUSDT | 0.56 | 1.72 | -1.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.73 | 1.784 | +0.3% | +0.00 | +0.00 | -0.0027% |
| LTCUSDT | 0.55 | 2.1 | -1.3% | +0.00 | +0.00 | +0.0065% |
| TRXUSDT | -0.24 | 1.169 | +0.2% | +0.00 | +0.00 | -0.0081% |
| DOTUSDT | -0.69 | 1.554 | -2.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
