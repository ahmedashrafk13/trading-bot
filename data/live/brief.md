# v9 brief - 2026-11-20 18:13 UTC (signal from the 2026-11-20 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+13.99 (+7.0% of budget); from peak $-0.11

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.43 | 3.446 | -5.7% | +0.00 | +0.00 | +0.0023% |
| ETHUSDT | -0.34 | 2.845 | -7.9% | +0.00 | +0.00 | -0.0141% |
| SOLUSDT | 1.75 | 3.861 | -6.2% | -154.91 | +0.00 | -0.0247% |
| BNBUSDT | -0.21 | 2.554 | -7.2% | +0.00 | +0.00 | -0.0094% |
| XRPUSDT | 0.99 | 3.075 | -6.4% | +0.00 | +0.00 | -0.0090% |
| DOGEUSDT | -0.9 | 2.441 | -8.0% | +0.00 | +0.00 | -0.0112% |
| ADAUSDT | 2.24 | 2.318 | -8.2% | -138.08 | -143.08 | -0.0301% |
| AVAXUSDT | -0.43 | 1.608 | -7.4% | +0.00 | +0.00 | -0.0078% |
| LINKUSDT | -0.31 | 1.732 | -7.0% | +0.00 | +0.00 | -0.0051% |
| LTCUSDT | -0.74 | 1.865 | -5.4% | +0.00 | +0.00 | -0.0033% |
| TRXUSDT | 0.43 | 1.208 | -2.7% | +0.00 | +0.00 | -0.0988% |
| DOTUSDT | 1.32 | 1.793 | -7.0% | +0.00 | +0.00 | +0.0080% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
