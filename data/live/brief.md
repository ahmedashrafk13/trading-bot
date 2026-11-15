# v9 brief - 2026-11-15 12:12 UTC (signal from the 2026-11-15 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.45 (-1.2% of budget); from peak $-6.44

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.81 | 2.802 | -2.9% | +0.00 | +0.00 | -0.0019% |
| ETHUSDT | -1.19 | 2.511 | -4.5% | +0.00 | +0.00 | -0.0072% |
| SOLUSDT | 0.94 | 3.49 | -4.8% | +0.00 | +0.00 | -0.0262% |
| BNBUSDT | -1.57 | 2.361 | -3.5% | +175.16 | +172.96 | +0.0100% |
| XRPUSDT | -0.56 | 2.686 | -3.2% | +0.00 | +0.00 | -0.0263% |
| DOGEUSDT | -1.66 | 2.38 | -6.3% | +145.92 | +148.76 | -0.0109% |
| ADAUSDT | 1.61 | 2.05 | -5.3% | -127.40 | -132.19 | -0.0272% |
| AVAXUSDT | 0.33 | 1.774 | -10.2% | +0.00 | +0.00 | -0.0220% |
| LINKUSDT | -0.67 | 1.631 | -4.0% | +0.00 | +0.00 | -0.0036% |
| LTCUSDT | 0.02 | 1.987 | -6.3% | +0.00 | +0.00 | +0.0087% |
| TRXUSDT | -1.27 | 1.031 | -1.3% | +0.00 | +0.00 | -0.0341% |
| DOTUSDT | -0.22 | 1.591 | -7.0% | +0.00 | +0.00 | -0.0063% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
