# v9 brief - 2026-09-29 18:12 UTC (signal from the 2026-09-29 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-9.49 (-4.7% of budget); from peak $-9.88

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.8 | 1.432 | -0.9% | +0.00 | +0.00 | +0.0025% |
| ETHUSDT | 0.44 | 2.708 | -0.8% | +0.00 | +0.00 | +0.0027% |
| SOLUSDT | -0.37 | 1.827 | -1.7% | +0.00 | +0.00 | -0.0038% |
| BNBUSDT | -0.29 | 2.214 | -2.3% | +0.00 | +0.00 | -0.0049% |
| XRPUSDT | 1.51 | 2.568 | -1.7% | -72.11 | +0.00 | +0.0050% |
| DOGEUSDT | 0.1 | 2.465 | -1.4% | +0.00 | +0.00 | -0.0040% |
| ADAUSDT | 1.12 | 2.352 | -2.9% | +0.00 | +0.00 | -0.0207% |
| AVAXUSDT | 1.76 | 2.765 | +5.5% | -53.26 | +0.00 | +0.0100% |
| LINKUSDT | 1.74 | 1.977 | -3.9% | -64.45 | +0.00 | -0.0017% |
| LTCUSDT | 0.94 | 2.598 | -3.3% | +0.00 | +0.00 | +0.0062% |
| TRXUSDT | -0.62 | 1.104 | -0.1% | +0.00 | +0.00 | -0.0189% |
| DOTUSDT | -0.63 | 1.869 | -2.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
