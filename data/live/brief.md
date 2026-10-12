# v9 brief - 2026-10-12 18:12 UTC (signal from the 2026-10-12 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.96 (-1.5% of budget); from peak $-3.34

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.72 | 1.473 | -1.6% | +0.00 | +0.00 | -0.0038% |
| ETHUSDT | 0.1 | 2.752 | -1.0% | +0.00 | +0.00 | -0.0010% |
| SOLUSDT | 1.42 | 2.322 | -3.9% | +0.00 | +0.00 | -0.0033% |
| BNBUSDT | -1.28 | 2.07 | -1.3% | +0.00 | +0.00 | +0.0019% |
| XRPUSDT | 0.56 | 2.49 | -3.8% | +0.00 | +0.00 | +0.0006% |
| DOGEUSDT | -0.4 | 2.38 | -2.5% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.76 | 1.974 | -4.5% | +0.00 | +0.00 | +0.0085% |
| AVAXUSDT | -0.76 | 1.943 | -3.6% | +0.00 | +0.00 | -0.0314% |
| LINKUSDT | -0.04 | 1.645 | -3.8% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | -0.54 | 2.087 | -3.1% | +0.00 | +137.30 | +0.0046% |
| TRXUSDT | -0.59 | 1.12 | -0.2% | +0.00 | +0.00 | -0.0257% |
| DOTUSDT | 1.86 | 2.357 | -3.2% | -103.43 | -99.09 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
