# v9 brief - 2026-10-15 18:12 UTC (signal from the 2026-10-15 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-0.19 (-0.1% of budget); from peak $-4.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.96 | 1.539 | +1.0% | +0.00 | -82.21 | +0.0096% |
| ETHUSDT | 0.07 | 2.749 | +0.6% | +0.00 | +0.00 | +0.0090% |
| SOLUSDT | 1.5 | 2.424 | +1.4% | -82.44 | -73.85 | +0.0100% |
| BNBUSDT | 1.95 | 2.529 | +0.8% | -136.74 | -124.62 | +0.0087% |
| XRPUSDT | 1.58 | 2.722 | +0.9% | -74.82 | +0.00 | +0.0100% |
| DOGEUSDT | 0.09 | 2.473 | -1.0% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -1.54 | 1.778 | +1.1% | +59.82 | +0.00 | +0.0100% |
| AVAXUSDT | -2.06 | 1.547 | +0.8% | +46.19 | +44.81 | +0.0100% |
| LINKUSDT | -0.61 | 1.554 | +0.5% | +0.00 | +0.00 | +0.0077% |
| LTCUSDT | -1.15 | 1.933 | +1.3% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 1.38 | 1.302 | -0.8% | +0.00 | +0.00 | +0.0034% |
| DOTUSDT | -0.81 | 1.723 | -0.6% | +0.00 | +0.00 | +0.0010% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
