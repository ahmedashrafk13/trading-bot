# v9 brief - 2026-11-27 12:12 UTC (signal from the 2026-11-27 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+9.46 (+4.7% of budget); from peak $-17.41

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.5 | 2.393 | +1.6% | +0.00 | +0.00 | +0.0017% |
| ETHUSDT | -1.27 | 2.064 | +1.4% | +0.00 | +0.00 | +0.0031% |
| SOLUSDT | -0.04 | 3.413 | +3.2% | +0.00 | +0.00 | -0.0001% |
| BNBUSDT | -0.99 | 2.414 | +2.2% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.35 | 2.891 | +2.5% | +0.00 | +0.00 | -0.0027% |
| DOGEUSDT | 0.43 | 2.584 | +3.5% | +0.00 | +0.00 | -0.0077% |
| ADAUSDT | 1.71 | 2.455 | +3.2% | -114.33 | -114.97 | +0.0073% |
| AVAXUSDT | -1.1 | 1.513 | +2.2% | +0.00 | +0.00 | -0.0093% |
| LINKUSDT | 1.58 | 2.007 | +3.3% | -108.81 | -107.82 | -0.0124% |
| LTCUSDT | 1.27 | 2.251 | +2.4% | +0.00 | -125.13 | +0.0100% |
| TRXUSDT | -0.6 | 1.095 | +0.4% | +0.00 | +0.00 | +0.0087% |
| DOTUSDT | 1.36 | 1.81 | +1.4% | +0.00 | +0.00 | -0.0030% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
