# v9 brief - 2026-11-14 18:13 UTC (signal from the 2026-11-14 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.20 (-1.6% of budget); from peak $-7.20

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.08 | 2.978 | -4.4% | +0.00 | +0.00 | +0.0097% |
| ETHUSDT | 0.45 | 3.325 | -4.9% | +0.00 | +0.00 | +0.0012% |
| SOLUSDT | 1.36 | 3.682 | -8.9% | +0.00 | -152.65 | -0.0032% |
| BNBUSDT | -0.77 | 2.489 | -6.9% | +0.00 | +0.00 | +0.0069% |
| XRPUSDT | 0.27 | 2.882 | -6.0% | +0.00 | +0.00 | +0.0053% |
| DOGEUSDT | -0.59 | 2.527 | -7.6% | +0.00 | +0.00 | +0.0013% |
| ADAUSDT | 1.49 | 2.027 | -9.0% | +0.00 | +0.00 | -0.0036% |
| AVAXUSDT | 1.43 | 2.068 | -10.3% | +0.00 | -121.94 | -0.0196% |
| LINKUSDT | -0.45 | 1.66 | -7.7% | +0.00 | +0.00 | -0.0080% |
| LTCUSDT | 1.02 | 2.19 | -7.3% | +0.00 | +0.00 | -0.0092% |
| TRXUSDT | -1.34 | 1.032 | -1.8% | +0.00 | +0.00 | -0.0809% |
| DOTUSDT | 0.28 | 1.694 | -8.8% | +0.00 | +0.00 | -0.0017% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
