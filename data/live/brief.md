# v9 brief - 2026-10-20 15:51 UTC (signal from the 2026-10-20 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-4.37 (-2.2% of budget); from peak $-8.36

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.55 | 1.811 | -1.0% | -214.54 | +0.00 | +0.0043% |
| ETHUSDT | 1.37 | 3.174 | -1.5% | +0.00 | +0.00 | +0.0024% |
| SOLUSDT | 1.32 | 2.505 | -0.6% | +0.00 | +0.00 | -0.0016% |
| BNBUSDT | 2.1 | 2.666 | +0.4% | -193.55 | -227.02 | +0.0004% |
| XRPUSDT | 0.89 | 2.685 | -0.5% | +0.00 | +0.00 | +0.0057% |
| DOGEUSDT | 0.36 | 2.554 | -0.1% | +0.00 | +0.00 | -0.0008% |
| ADAUSDT | -1.19 | 1.863 | -0.9% | +0.00 | +0.00 | +0.0058% |
| AVAXUSDT | -1.96 | 1.429 | -2.2% | +71.91 | +85.99 | +0.0097% |
| LINKUSDT | -0.8 | 1.548 | -0.7% | +0.00 | +0.00 | +0.0079% |
| LTCUSDT | -1.09 | 1.922 | -1.9% | +0.00 | +0.00 | +0.0048% |
| TRXUSDT | 0.83 | 1.315 | +0.3% | +0.00 | +0.00 | -0.0083% |
| DOTUSDT | 0.96 | 2.112 | +3.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
