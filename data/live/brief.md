# v9 brief - 2026-09-26 12:12 UTC (signal from the 2026-09-26 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.92 (-1.0% of budget); from peak $-1.92

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.43 | 1.304 | -0.5% | +0.00 | +0.00 | -0.0029% |
| ETHUSDT | 0.56 | 2.72 | -1.0% | +0.00 | +0.00 | +0.0032% |
| SOLUSDT | -1.84 | 1.521 | +0.4% | +86.99 | +72.67 | +0.0100% |
| BNBUSDT | -1.3 | 2.07 | -0.5% | +0.00 | +0.00 | +0.0017% |
| XRPUSDT | -0.27 | 2.355 | -3.0% | +0.00 | +0.00 | +0.0060% |
| DOGEUSDT | 0.3 | 2.52 | -0.4% | +0.00 | +0.00 | +0.0005% |
| ADAUSDT | 1.92 | 2.52 | +0.7% | -67.24 | -70.39 | +0.0100% |
| AVAXUSDT | 0.07 | 2.166 | +3.4% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.74 | 1.897 | +1.3% | -72.19 | -72.48 | +0.0100% |
| LTCUSDT | 0.17 | 2.367 | +3.9% | +0.00 | +0.00 | +0.0088% |
| TRXUSDT | -0.86 | 1.088 | -0.1% | +0.00 | +0.00 | -0.0273% |
| DOTUSDT | -0.58 | 1.88 | +3.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
