# v9 brief - 2026-11-13 15:13 UTC (signal from the 2026-11-13 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-29.63 (-14.8% of budget); from peak $-33.62

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.7 | 3.405 | -5.0% | -204.67 | +0.00 | +0.0027% |
| ETHUSDT | 1.16 | 3.719 | -3.1% | +0.00 | +0.00 | +0.0021% |
| SOLUSDT | 0.9 | 3.394 | -2.2% | +0.00 | +0.00 | -0.0050% |
| BNBUSDT | -1.15 | 2.44 | -3.7% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.67 | 2.971 | -1.4% | +0.00 | +0.00 | +0.0065% |
| DOGEUSDT | -0.76 | 2.499 | -1.9% | +0.00 | +0.00 | +0.0044% |
| ADAUSDT | 2.36 | 2.081 | +0.1% | -125.04 | -129.78 | +0.0100% |
| AVAXUSDT | 2.21 | 2.219 | -0.9% | -110.15 | -111.50 | +0.0026% |
| LINKUSDT | -0.7 | 1.62 | +0.1% | +0.00 | +0.00 | +0.0046% |
| LTCUSDT | 0.44 | 2.073 | +0.1% | +0.00 | +0.00 | +0.0016% |
| TRXUSDT | -1.2 | 1.059 | -1.1% | +0.00 | +0.00 | +0.0005% |
| DOTUSDT | -0.03 | 1.637 | -0.3% | +0.00 | +0.00 | +0.0080% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
