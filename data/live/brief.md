# v9 brief - 2026-10-25 18:37 UTC (signal from the 2026-10-25 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-23.54 (-11.8% of budget); from peak $-27.53

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.81 | 2.144 | +0.7% | -190.41 | -161.29 | +0.0064% |
| ETHUSDT | 1.34 | 3.283 | +1.5% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.72 | 3.034 | +1.5% | -113.65 | -112.13 | +0.0092% |
| BNBUSDT | 0.23 | 2.373 | +2.5% | +0.00 | +0.00 | +0.0052% |
| XRPUSDT | 1.61 | 3.013 | +2.3% | -113.80 | +0.00 | +0.0021% |
| DOGEUSDT | 0.37 | 2.57 | +1.2% | +0.00 | +0.00 | -0.0056% |
| ADAUSDT | -0.89 | 1.842 | +1.0% | +0.00 | +0.00 | -0.0091% |
| AVAXUSDT | -0.94 | 1.544 | +1.1% | +0.00 | +0.00 | +0.0029% |
| LINKUSDT | -0.32 | 1.643 | +1.0% | +0.00 | +0.00 | +0.0017% |
| LTCUSDT | -1.08 | 1.843 | +1.7% | +0.00 | +102.73 | -0.0108% |
| TRXUSDT | -0.01 | 1.175 | +0.2% | +0.00 | +0.00 | -0.0043% |
| DOTUSDT | -2.03 | 1.468 | +1.4% | +62.14 | +63.57 | -0.0084% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
