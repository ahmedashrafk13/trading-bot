# v9 brief - 2026-10-07 12:12 UTC (signal from the 2026-10-07 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-5.90 (-2.9% of budget); from peak $-6.28

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.9 | 1.484 | -2.9% | +0.00 | +0.00 | +0.0003% |
| ETHUSDT | 2.26 | 3.344 | -5.0% | -218.47 | -103.13 | -0.0168% |
| SOLUSDT | 0.14 | 1.896 | -2.5% | +0.00 | +0.00 | -0.0067% |
| BNBUSDT | 0.09 | 2.284 | -2.1% | +0.00 | -138.12 | -0.0082% |
| XRPUSDT | -0.61 | 2.31 | -4.4% | +0.00 | +0.00 | +0.0068% |
| DOGEUSDT | 0.14 | 2.492 | -7.2% | +0.00 | +0.00 | +0.0091% |
| ADAUSDT | 1.37 | 2.542 | -9.2% | +0.00 | -61.66 | -0.0106% |
| AVAXUSDT | 0.94 | 2.584 | -3.9% | +0.00 | +0.00 | -0.0143% |
| LINKUSDT | -0.32 | 1.619 | -4.9% | +0.00 | +0.00 | -0.0018% |
| LTCUSDT | -2.51 | 1.78 | -4.9% | +137.66 | +0.00 | +0.0007% |
| TRXUSDT | -0.84 | 1.108 | -0.4% | +0.00 | +0.00 | -0.0122% |
| DOTUSDT | -1.25 | 1.688 | -10.2% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
