# v9 brief - 2026-10-01 00:22 UTC (signal from the 2026-10-01 00:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.32 (-3.7% of budget); from peak $-7.70

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.46 | 1.347 | -0.1% | +0.00 | +0.00 | +0.0011% |
| ETHUSDT | 0.43 | 2.715 | +0.3% | +0.00 | +0.00 | +0.0056% |
| SOLUSDT | 0.17 | 1.955 | -0.9% | +0.00 | +0.00 | -0.0070% |
| BNBUSDT | -0.56 | 2.155 | +1.4% | +0.00 | +0.00 | -0.0065% |
| XRPUSDT | 1.57 | 2.589 | -0.1% | -73.79 | +0.00 | -0.0036% |
| DOGEUSDT | 1.07 | 2.666 | +0.7% | +0.00 | +0.00 | -0.0016% |
| ADAUSDT | 0.36 | 2.153 | +0.9% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.15 | 2.591 | -4.4% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.45 | 1.959 | -1.6% | +0.00 | -63.15 | +0.0040% |
| LTCUSDT | -0.43 | 2.272 | +0.6% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.24 | 1.169 | +0.9% | +0.00 | +0.00 | -0.0016% |
| DOTUSDT | 0.29 | 2.098 | +2.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
