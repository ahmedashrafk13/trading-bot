# v9 brief - 2026-10-26 15:29 UTC (signal from the 2026-10-26 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-24.38 (-12.2% of budget); from peak $-28.37

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.83 | 2.22 | -0.2% | -243.17 | -161.16 | +0.0091% |
| ETHUSDT | 1.54 | 3.382 | -0.2% | -158.76 | +0.00 | +0.0043% |
| SOLUSDT | 1.46 | 2.917 | +0.4% | +0.00 | -112.47 | +0.0080% |
| BNBUSDT | 1.25 | 2.602 | -0.0% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.45 | 2.989 | -0.4% | +0.00 | -113.68 | +0.0084% |
| DOGEUSDT | 0.88 | 2.636 | +0.7% | +0.00 | +0.00 | -0.0010% |
| ADAUSDT | -1.01 | 1.809 | +0.1% | +0.00 | +0.00 | +0.0079% |
| AVAXUSDT | -0.89 | 1.546 | +1.5% | +0.00 | +0.00 | +0.0097% |
| LINKUSDT | -0.77 | 1.571 | +0.6% | +0.00 | +0.00 | +0.0099% |
| LTCUSDT | 0.06 | 2.076 | +0.6% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 1.38 | 1.355 | +0.5% | +0.00 | +0.00 | -0.0118% |
| DOTUSDT | -1.84 | 1.486 | -0.1% | +78.07 | +62.92 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
