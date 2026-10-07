# v9 brief - 2026-10-07 18:12 UTC (signal from the 2026-10-07 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-6.54 (-3.3% of budget); from peak $-6.92

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.43 | 1.654 | -3.0% | +0.00 | +0.00 | +0.0016% |
| ETHUSDT | 2.33 | 3.394 | -5.5% | -243.98 | -204.64 | +0.0039% |
| SOLUSDT | 0.59 | 2.012 | -3.8% | +0.00 | +0.00 | +0.0011% |
| BNBUSDT | 0.19 | 2.3 | -1.6% | +0.00 | +0.00 | +0.0093% |
| XRPUSDT | -0.31 | 2.351 | -5.8% | +0.00 | +0.00 | +0.0013% |
| DOGEUSDT | 0.06 | 2.477 | -6.7% | +0.00 | +0.00 | -0.0039% |
| ADAUSDT | 1.16 | 2.482 | -6.5% | +0.00 | +0.00 | -0.0030% |
| AVAXUSDT | 0.8 | 2.534 | -2.3% | +0.00 | +0.00 | +0.0076% |
| LINKUSDT | 0.09 | 1.7 | -4.3% | +0.00 | +0.00 | +0.0042% |
| LTCUSDT | -1.24 | 2.033 | -4.7% | +0.00 | +131.96 | -0.0019% |
| TRXUSDT | -0.74 | 1.123 | -0.2% | +0.00 | +0.00 | -0.0023% |
| DOTUSDT | -1.37 | 1.661 | -9.9% | +0.00 | +0.00 | -0.0130% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
