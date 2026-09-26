# v9 brief - 2026-09-26 08:09 UTC (signal from the 2026-09-26 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-0.40 (-0.2% of budget); from peak $-0.40

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.42 | 1.297 | -0.3% | +0.00 | +0.00 | +0.0032% |
| ETHUSDT | 0.4 | 2.671 | +0.2% | +0.00 | +0.00 | +0.0037% |
| SOLUSDT | -1.97 | 1.498 | +3.5% | +82.87 | +72.36 | +0.0100% |
| BNBUSDT | -1.28 | 2.078 | -0.3% | +0.00 | +0.00 | -0.0117% |
| XRPUSDT | -0.43 | 2.337 | +1.4% | +0.00 | +0.00 | -0.0036% |
| DOGEUSDT | 0.51 | 2.565 | +2.5% | +0.00 | +0.00 | -0.0095% |
| ADAUSDT | 2.45 | 2.67 | +3.0% | -67.24 | -69.68 | +0.0066% |
| AVAXUSDT | 0.11 | 2.177 | +4.2% | +0.00 | +0.00 | -0.0070% |
| LINKUSDT | 1.83 | 1.909 | +4.3% | -72.19 | +0.00 | +0.0100% |
| LTCUSDT | 0.13 | 2.358 | +1.2% | +0.00 | +0.00 | +0.0018% |
| TRXUSDT | -0.84 | 1.092 | -0.4% | +0.00 | +0.00 | -0.0415% |
| DOTUSDT | -0.89 | 1.812 | +7.0% | +0.00 | +52.08 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
