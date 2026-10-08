# v9 brief - 2026-10-08 12:12 UTC (signal from the 2026-10-08 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-4.01 (-2.0% of budget); from peak $-4.39

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.91 | 1.86 | -1.5% | -152.32 | -164.69 | +0.0027% |
| ETHUSDT | 2.1 | 3.373 | -1.6% | -121.18 | -126.68 | -0.0019% |
| SOLUSDT | 1.21 | 2.188 | -3.5% | +0.00 | +0.00 | -0.0056% |
| BNBUSDT | 0.59 | 2.369 | -0.7% | +0.00 | +0.00 | -0.0015% |
| XRPUSDT | 0.94 | 2.539 | -3.4% | +0.00 | +0.00 | +0.0012% |
| DOGEUSDT | -0.08 | 2.448 | -2.0% | +0.00 | +0.00 | -0.0039% |
| ADAUSDT | 0.96 | 2.436 | -1.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.19 | 2.313 | -2.3% | +0.00 | +0.00 | -0.0066% |
| LINKUSDT | -0.26 | 1.622 | -2.8% | +0.00 | +0.00 | +0.0086% |
| LTCUSDT | -1.96 | 1.865 | -4.3% | +76.06 | +76.76 | +0.0100% |
| TRXUSDT | 0.14 | 1.266 | +0.4% | +0.00 | +0.00 | -0.0026% |
| DOTUSDT | -1.59 | 1.61 | -0.6% | +50.43 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
