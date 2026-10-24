# v9 brief - 2026-10-24 10:37 UTC (signal from the 2026-10-24 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.21 (-11.1% of budget); from peak $-26.20

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.12 | 2.149 | -1.3% | -170.60 | -80.66 | +0.0054% |
| ETHUSDT | 0.9 | 3.098 | -1.1% | +0.00 | +0.00 | +0.0084% |
| SOLUSDT | 1.76 | 2.94 | -2.0% | -95.75 | -81.38 | -0.0047% |
| BNBUSDT | 0.48 | 2.4 | -0.5% | +0.00 | +0.00 | -0.0172% |
| XRPUSDT | 2.41 | 3.149 | -2.9% | -93.93 | +0.00 | -0.0005% |
| DOGEUSDT | 1.31 | 2.687 | -1.8% | +0.00 | +0.00 | -0.0082% |
| ADAUSDT | -1.56 | 1.723 | -2.5% | +63.05 | +0.00 | -0.0196% |
| AVAXUSDT | -1.57 | 1.389 | -3.2% | +56.67 | +0.00 | -0.0091% |
| LINKUSDT | -0.06 | 1.683 | -3.2% | +0.00 | +0.00 | +0.0083% |
| LTCUSDT | -1.28 | 1.827 | -4.6% | +0.00 | +0.00 | +0.0045% |
| TRXUSDT | -0.42 | 1.127 | +0.0% | +0.00 | +0.00 | -0.0280% |
| DOTUSDT | -0.8 | 1.737 | -8.1% | +0.00 | +0.00 | +0.0009% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
