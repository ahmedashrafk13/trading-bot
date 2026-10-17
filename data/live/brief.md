# v9 brief - 2026-10-17 00:20 UTC (signal from the 2026-10-17 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.06 (-0.5% of budget); from peak $-5.05

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.56 | 1.726 | -0.8% | -92.71 | -81.55 | +0.0080% |
| ETHUSDT | 0.69 | 2.917 | -0.8% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.75 | 2.544 | -0.9% | -54.08 | -41.71 | +0.0017% |
| BNBUSDT | 1.75 | 2.5 | -1.1% | -87.95 | -79.14 | -0.0153% |
| XRPUSDT | 2.58 | 2.97 | -1.8% | -53.06 | +0.00 | +0.0092% |
| DOGEUSDT | 0.51 | 2.555 | -0.2% | +0.00 | +0.00 | +0.0075% |
| ADAUSDT | -1.09 | 1.897 | -1.8% | +0.00 | +0.00 | +0.0074% |
| AVAXUSDT | -1.39 | 1.706 | -0.8% | +0.00 | +27.78 | -0.0144% |
| LINKUSDT | -0.56 | 1.574 | -0.9% | +0.00 | +0.00 | -0.0153% |
| LTCUSDT | 0.05 | 2.187 | -2.2% | +0.00 | +0.00 | +0.0063% |
| TRXUSDT | 2.83 | 1.483 | +0.9% | -192.20 | -182.12 | +0.0076% |
| DOTUSDT | 0.22 | 1.943 | +3.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
