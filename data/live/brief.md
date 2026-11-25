# v9 brief - 2026-11-25 04:56 UTC (signal from the 2026-11-25 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+18.56 (+9.3% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.03 | 2.571 | -2.4% | +0.00 | +0.00 | -0.0006% |
| ETHUSDT | -1.28 | 2.15 | -1.8% | +0.00 | +0.00 | +0.0070% |
| SOLUSDT | 1.6 | 3.857 | -3.2% | -106.08 | -103.20 | -0.0016% |
| BNBUSDT | -0.82 | 2.446 | -1.4% | +0.00 | +0.00 | +0.0015% |
| XRPUSDT | 0.39 | 2.909 | -1.7% | +0.00 | +0.00 | -0.0045% |
| DOGEUSDT | -0.8 | 2.392 | -1.9% | +0.00 | +0.00 | +0.0042% |
| ADAUSDT | 2.67 | 2.589 | -2.8% | -96.84 | -96.53 | +0.0011% |
| AVAXUSDT | -0.7 | 1.593 | -3.1% | +0.00 | +0.00 | -0.0033% |
| LINKUSDT | 1.16 | 1.938 | -1.8% | +0.00 | +0.00 | +0.0055% |
| LTCUSDT | -0.24 | 1.965 | -1.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 1.52 | 1.363 | -0.6% | -178.33 | -179.13 | -0.0002% |
| DOTUSDT | 2.15 | 1.878 | -3.5% | -98.75 | -97.23 | -0.0086% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
