# v9 brief - 2026-10-13 05:14 UTC (signal from the 2026-10-13 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.74 (-1.4% of budget); from peak $-3.12

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.82 | 1.501 | -2.3% | +0.00 | +0.00 | +0.0057% |
| ETHUSDT | 0.92 | 3.031 | -3.5% | +0.00 | +0.00 | +0.0020% |
| SOLUSDT | 1.52 | 2.359 | -5.0% | -164.39 | +0.00 | -0.0050% |
| BNBUSDT | -0.99 | 2.105 | -2.8% | +0.00 | +0.00 | -0.0027% |
| XRPUSDT | -0.35 | 2.356 | -4.8% | +0.00 | +0.00 | -0.0115% |
| DOGEUSDT | -0.03 | 2.443 | -5.2% | +0.00 | +0.00 | +0.0021% |
| ADAUSDT | -0.76 | 1.977 | -7.6% | +0.00 | +0.00 | -0.0191% |
| AVAXUSDT | -1.14 | 1.838 | -7.6% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.19 | 1.618 | -5.4% | +0.00 | +0.00 | +0.0017% |
| LTCUSDT | -0.68 | 2.052 | -5.6% | +0.00 | +0.00 | +0.0010% |
| TRXUSDT | -0.83 | 1.089 | -0.4% | +0.00 | +0.00 | -0.0283% |
| DOTUSDT | 2.07 | 2.422 | -6.8% | -103.43 | -98.69 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
