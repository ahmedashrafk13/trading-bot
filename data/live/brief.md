# v9 brief - 2026-10-23 18:12 UTC (signal from the 2026-10-23 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-26.15 (-13.1% of budget); from peak $-30.14

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.07 | 2.079 | +0.5% | -297.67 | -81.51 | +0.0100% |
| ETHUSDT | 1.27 | 3.205 | +1.2% | +0.00 | -96.22 | +0.0068% |
| SOLUSDT | 1.55 | 2.785 | +0.9% | -167.54 | -83.43 | +0.0084% |
| BNBUSDT | 0.27 | 2.358 | +2.3% | +0.00 | +0.00 | +0.0077% |
| XRPUSDT | 0.58 | 2.664 | +0.1% | +0.00 | -80.74 | +0.0100% |
| DOGEUSDT | 1.13 | 2.664 | +2.1% | +0.00 | +0.00 | +0.0079% |
| ADAUSDT | -1.36 | 1.778 | +2.0% | +0.00 | +0.00 | +0.0010% |
| AVAXUSDT | -1.47 | 1.435 | +0.4% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.15 | 1.665 | +1.3% | +0.00 | +0.00 | +0.0041% |
| LTCUSDT | -1.03 | 1.88 | +0.7% | +0.00 | +64.72 | -0.0123% |
| TRXUSDT | -0.96 | 1.068 | +0.4% | +0.00 | +0.00 | -0.0360% |
| DOTUSDT | 1.19 | 2.207 | +1.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
