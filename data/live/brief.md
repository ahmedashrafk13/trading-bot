# v9 brief - 2026-10-10 14:36 UTC (signal from the 2026-10-10 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-4.05 (-2.0% of budget); from peak $-4.44

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.82 | 1.524 | -0.4% | +0.00 | +0.00 | -0.0013% |
| ETHUSDT | 0.96 | 3.022 | -0.4% | +0.00 | +0.00 | +0.0026% |
| SOLUSDT | 1.83 | 2.432 | -1.2% | -163.23 | -154.59 | -0.0005% |
| BNBUSDT | -0.59 | 2.172 | +0.8% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.01 | 2.412 | +0.2% | +0.00 | +0.00 | +0.0028% |
| DOGEUSDT | -0.12 | 2.43 | +1.0% | +0.00 | +0.00 | +0.0023% |
| ADAUSDT | -0.44 | 2.037 | +6.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.06 | 1.902 | +1.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.3 | 1.599 | +0.2% | +0.00 | +0.00 | +0.0037% |
| LTCUSDT | -1.3 | 1.967 | -0.6% | +0.00 | +0.00 | +0.0063% |
| TRXUSDT | -0.76 | 1.115 | -0.6% | +0.00 | +0.00 | -0.0279% |
| DOTUSDT | 1.43 | 2.249 | +6.1% | +0.00 | -99.18 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
