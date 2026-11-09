# v9 brief - 2026-11-09 15:18 UTC (signal from the 2026-11-09 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-36.14 (-18.1% of budget); from peak $-40.13

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.44 | 2.92 | -2.1% | +0.00 | -225.04 | +0.0083% |
| ETHUSDT | 1.76 | 3.929 | -5.7% | -163.58 | +0.00 | +0.0027% |
| SOLUSDT | 1.22 | 3.396 | -4.0% | +0.00 | -148.75 | +0.0077% |
| BNBUSDT | 0.35 | 2.624 | -2.2% | +0.00 | +0.00 | +0.0010% |
| XRPUSDT | 0.22 | 2.796 | -7.3% | +0.00 | +0.00 | +0.0011% |
| DOGEUSDT | 0.03 | 2.588 | -3.4% | +0.00 | +0.00 | +0.0036% |
| ADAUSDT | 0.12 | 1.882 | -2.6% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.53 | 1.544 | -1.9% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.38 | 1.746 | -2.5% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.74 | 1.847 | -2.5% | +0.00 | +0.00 | +0.0092% |
| TRXUSDT | -0.19 | 1.18 | -0.9% | +0.00 | +0.00 | -0.0240% |
| DOTUSDT | -0.7 | 1.539 | -4.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
