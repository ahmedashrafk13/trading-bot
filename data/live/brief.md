# v9 brief - 2026-11-08 17:14 UTC (signal from the 2026-11-08 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-40.76 (-20.4% of budget); from peak $-44.75

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.75 | 3.082 | -0.0% | -243.26 | -227.07 | +0.0064% |
| ETHUSDT | 1.15 | 3.515 | -0.2% | +0.00 | +0.00 | +0.0012% |
| SOLUSDT | 1.79 | 3.625 | -0.3% | -158.89 | -142.41 | +0.0100% |
| BNBUSDT | 0.79 | 2.711 | +0.6% | +0.00 | +0.00 | -0.0064% |
| XRPUSDT | 0.35 | 2.818 | -0.6% | +0.00 | +0.00 | -0.0014% |
| DOGEUSDT | 1.17 | 2.767 | -0.9% | +0.00 | +0.00 | +0.0073% |
| ADAUSDT | 0.53 | 1.923 | -1.5% | +0.00 | +0.00 | -0.0046% |
| AVAXUSDT | 0.07 | 1.637 | -1.0% | +0.00 | +0.00 | -0.0094% |
| LINKUSDT | 1.0 | 1.832 | -0.4% | +0.00 | +0.00 | -0.0044% |
| LTCUSDT | 0.27 | 2.041 | -0.4% | +0.00 | +0.00 | -0.0021% |
| TRXUSDT | 0.32 | 1.247 | +0.3% | +0.00 | +0.00 | -0.0124% |
| DOTUSDT | -0.73 | 1.541 | -0.0% | +0.00 | +0.00 | -0.0075% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
