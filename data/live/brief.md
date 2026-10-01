# v9 brief - 2026-10-01 06:12 UTC (signal from the 2026-10-01 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-8.43 (-4.2% of budget); from peak $-8.82

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.55 | 1.377 | +1.1% | +0.00 | +0.00 | +0.0043% |
| ETHUSDT | -0.04 | 2.587 | +1.6% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.01 | 1.915 | +0.3% | +0.00 | +0.00 | +0.0033% |
| BNBUSDT | -0.2 | 2.22 | +1.0% | +0.00 | +0.00 | -0.0087% |
| XRPUSDT | 2.22 | 2.687 | +0.4% | -73.79 | -74.59 | +0.0026% |
| DOGEUSDT | 1.45 | 2.754 | +2.0% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.4 | 2.165 | +3.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.01 | 2.549 | -1.3% | +0.00 | +0.00 | +0.0048% |
| LINKUSDT | 1.56 | 1.994 | +0.4% | -66.02 | +0.00 | +0.0013% |
| LTCUSDT | -0.5 | 2.26 | +0.2% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.0 | 1.214 | -0.0% | +0.00 | +0.00 | -0.0022% |
| DOTUSDT | 0.47 | 2.146 | +2.8% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
