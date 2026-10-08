# v9 brief - 2026-10-08 06:13 UTC (signal from the 2026-10-08 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-6.22 (-3.1% of budget); from peak $-6.60

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.65 | 1.748 | -2.0% | -174.19 | -165.74 | -0.0020% |
| ETHUSDT | 1.94 | 3.292 | -2.3% | -138.78 | -128.51 | -0.0010% |
| SOLUSDT | 0.98 | 2.119 | -3.3% | +0.00 | +0.00 | -0.0052% |
| BNBUSDT | 0.46 | 2.346 | -0.3% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.04 | 2.551 | -5.0% | +0.00 | -82.80 | -0.0017% |
| DOGEUSDT | -0.04 | 2.458 | -3.8% | +0.00 | +0.00 | -0.0033% |
| ADAUSDT | 1.13 | 2.487 | -1.9% | +0.00 | +0.00 | +0.0090% |
| AVAXUSDT | 0.8 | 2.529 | -3.8% | +0.00 | +0.00 | -0.0096% |
| LINKUSDT | -0.25 | 1.627 | -4.3% | +0.00 | +0.00 | +0.0027% |
| LTCUSDT | -2.14 | 1.838 | -5.1% | +87.03 | +0.00 | +0.0098% |
| TRXUSDT | -0.3 | 1.193 | +0.5% | +0.00 | +0.00 | +0.0008% |
| DOTUSDT | -1.2 | 1.686 | -2.6% | +0.00 | +0.00 | +0.0056% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
