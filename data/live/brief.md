# v9 brief - 2026-10-23 00:18 UTC (signal from the 2026-10-23 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.02 (-11.0% of budget); from peak $-26.01

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.28 | 2.102 | -3.2% | -132.17 | +0.00 | +0.0079% |
| ETHUSDT | 2.43 | 3.547 | -3.4% | -87.65 | +0.00 | +0.0058% |
| SOLUSDT | 1.92 | 2.92 | -3.1% | -75.14 | +0.00 | +0.0100% |
| BNBUSDT | 2.32 | 2.776 | -2.0% | -114.48 | +0.00 | -0.0019% |
| XRPUSDT | 1.81 | 2.902 | -4.1% | -70.56 | +0.00 | -0.0024% |
| DOGEUSDT | 1.47 | 2.709 | -3.8% | +0.00 | +0.00 | +0.0009% |
| ADAUSDT | -1.2 | 1.824 | -5.8% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.4 | 1.48 | -5.5% | +0.00 | +37.43 | -0.0022% |
| LINKUSDT | 0.18 | 1.717 | -4.4% | +0.00 | +0.00 | -0.0123% |
| LTCUSDT | -0.08 | 2.102 | -4.4% | +0.00 | +0.00 | +0.0010% |
| TRXUSDT | -1.12 | 1.055 | -0.6% | +0.00 | +0.00 | -0.0015% |
| DOTUSDT | -0.5 | 1.79 | -2.8% | +0.00 | +0.00 | +0.0064% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
