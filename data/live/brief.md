# v9 brief - 2026-10-16 12:12 UTC (signal from the 2026-10-16 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+0.25 (+0.1% of budget); from peak $-3.74

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.99 | 1.532 | +2.1% | +0.00 | +0.00 | +0.0034% |
| ETHUSDT | -0.75 | 2.49 | +4.8% | +0.00 | +0.00 | +0.0077% |
| SOLUSDT | 1.46 | 2.409 | +4.3% | +0.00 | +0.00 | -0.0027% |
| BNBUSDT | 1.49 | 2.46 | +1.6% | +0.00 | -94.88 | +0.0100% |
| XRPUSDT | 1.39 | 2.696 | +3.1% | +0.00 | +0.00 | +0.0063% |
| DOGEUSDT | 0.34 | 2.522 | +2.6% | +0.00 | +0.00 | -0.0006% |
| ADAUSDT | -1.34 | 1.83 | +4.7% | +0.00 | +42.14 | +0.0100% |
| AVAXUSDT | -1.67 | 1.632 | +7.8% | +54.46 | +33.85 | +0.0084% |
| LINKUSDT | -0.44 | 1.589 | +5.5% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | -1.43 | 1.877 | +5.0% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 2.02 | 1.376 | +1.4% | -345.54 | -213.17 | +0.0100% |
| DOTUSDT | -0.5 | 1.785 | +7.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
