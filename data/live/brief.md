# v9 brief - 2026-11-13 22:49 UTC (signal from the 2026-11-13 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.45 (-11.2% of budget); from peak $-26.44

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.34 | 3.114 | -4.1% | +0.00 | -136.74 | +0.0055% |
| ETHUSDT | 1.17 | 3.735 | -3.9% | +0.00 | +0.00 | +0.0043% |
| SOLUSDT | 0.99 | 3.444 | -2.1% | +0.00 | +0.00 | +0.0000% |
| BNBUSDT | -1.08 | 2.45 | -3.5% | +0.00 | +0.00 | +0.0073% |
| XRPUSDT | 0.85 | 3.019 | -0.9% | +0.00 | +0.00 | -0.0013% |
| DOGEUSDT | -0.96 | 2.472 | -1.1% | +0.00 | +0.00 | -0.0015% |
| ADAUSDT | 2.6 | 2.111 | -0.2% | -125.04 | -126.54 | +0.0100% |
| AVAXUSDT | 2.34 | 2.28 | +0.3% | -110.15 | -108.24 | +0.0014% |
| LINKUSDT | -0.66 | 1.626 | -0.7% | +0.00 | +0.00 | +0.0010% |
| LTCUSDT | 0.16 | 2.015 | -0.2% | +0.00 | +0.00 | +0.0036% |
| TRXUSDT | -1.26 | 1.051 | -1.0% | +0.00 | +0.00 | -0.0263% |
| DOTUSDT | 0.22 | 1.687 | -0.2% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
