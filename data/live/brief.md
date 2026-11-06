# v9 brief - 2026-11-06 18:12 UTC (signal from the 2026-11-06 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-42.00 (-21.0% of budget); from peak $-45.99

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.12 | 3.117 | -0.2% | -208.28 | -75.76 | +0.0081% |
| ETHUSDT | 2.08 | 3.973 | -1.2% | -143.44 | -89.03 | +0.0031% |
| SOLUSDT | 1.94 | 3.568 | +1.0% | -128.27 | -72.03 | +0.0002% |
| BNBUSDT | 1.39 | 2.826 | +0.5% | +0.00 | -97.24 | +0.0100% |
| XRPUSDT | 1.03 | 2.992 | -4.0% | +0.00 | +0.00 | -0.0055% |
| DOGEUSDT | -0.2 | 2.526 | +1.8% | +0.00 | +0.00 | -0.0069% |
| ADAUSDT | -0.07 | 1.882 | +3.6% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.19 | 1.686 | +2.2% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.04 | 1.824 | +1.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.29 | 2.042 | +2.7% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.27 | 1.167 | +0.7% | +0.00 | +0.00 | -0.0086% |
| DOTUSDT | -0.34 | 1.652 | +2.4% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
