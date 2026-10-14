# v9 brief - 2026-10-14 18:12 UTC (signal from the 2026-10-14 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-0.07 (-0.0% of budget); from peak $-4.06

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.48 | 1.695 | -1.8% | +0.00 | +0.00 | +0.0036% |
| ETHUSDT | 1.66 | 3.303 | -2.8% | -98.36 | +0.00 | +0.0026% |
| SOLUSDT | 1.83 | 2.498 | -2.6% | -73.97 | +0.00 | +0.0020% |
| BNBUSDT | 2.25 | 2.529 | -1.6% | -121.12 | +0.00 | -0.0002% |
| XRPUSDT | 2.83 | 2.926 | -2.5% | -64.92 | -133.86 | -0.0012% |
| DOGEUSDT | 0.27 | 2.5 | -2.3% | +0.00 | +0.00 | +0.0084% |
| ADAUSDT | -1.49 | 1.8 | -2.6% | +0.00 | +108.31 | -0.0089% |
| AVAXUSDT | -2.3 | 1.541 | -2.9% | +41.63 | +85.99 | +0.0100% |
| LINKUSDT | -0.37 | 1.591 | -3.3% | +0.00 | +0.00 | +0.0065% |
| LTCUSDT | 0.33 | 2.253 | -2.8% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.51 | 1.118 | +2.0% | +0.00 | +0.00 | -0.0024% |
| DOTUSDT | -0.18 | 1.862 | -2.0% | +0.00 | +0.00 | -0.0173% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
