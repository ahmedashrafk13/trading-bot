# v9 brief - 2026-10-13 06:13 UTC (signal from the 2026-10-13 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-3.21 (-1.6% of budget); from peak $-3.59

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.42 | 1.378 | -0.4% | +0.00 | +0.00 | +0.0056% |
| ETHUSDT | 0.21 | 2.791 | -1.3% | +0.00 | +0.00 | +0.0024% |
| SOLUSDT | 1.78 | 2.453 | -3.9% | -158.99 | -162.63 | -0.0032% |
| BNBUSDT | 0.52 | 2.297 | -1.1% | +0.00 | +0.00 | -0.0052% |
| XRPUSDT | 1.7 | 2.676 | -2.7% | -138.34 | +0.00 | -0.0094% |
| DOGEUSDT | -0.13 | 2.426 | -3.0% | +0.00 | +0.00 | +0.0036% |
| ADAUSDT | -1.11 | 1.894 | -5.5% | +0.00 | +0.00 | -0.0193% |
| AVAXUSDT | -1.48 | 1.751 | -4.2% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.33 | 1.591 | -1.8% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | -0.55 | 2.08 | -5.0% | +0.00 | +0.00 | -0.0004% |
| TRXUSDT | -0.64 | 1.111 | -0.6% | +0.00 | +0.00 | -0.0241% |
| DOTUSDT | 1.75 | 2.336 | -5.0% | -102.66 | -98.91 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
