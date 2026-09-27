# v9 brief - 2026-09-27 17:20 UTC (signal from the 2026-09-27 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.21 (-0.6% of budget); from peak $-1.59

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.12 | 1.233 | +0.9% | +0.00 | +0.00 | +0.0011% |
| ETHUSDT | 0.15 | 2.615 | +0.8% | +0.00 | +0.00 | +0.0037% |
| SOLUSDT | -2.05 | 1.486 | +2.2% | +91.18 | +85.43 | +0.0062% |
| BNBUSDT | -1.41 | 2.035 | +0.6% | +0.00 | +0.00 | -0.0079% |
| XRPUSDT | 0.83 | 2.488 | -0.6% | +0.00 | +0.00 | -0.0044% |
| DOGEUSDT | 0.0 | 2.453 | +0.2% | +0.00 | +0.00 | -0.0032% |
| ADAUSDT | 1.12 | 2.312 | -0.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.34 | 2.252 | +0.4% | +0.00 | +0.00 | +0.0099% |
| LINKUSDT | 1.68 | 1.899 | +0.1% | -73.08 | +0.00 | +0.0100% |
| LTCUSDT | 0.31 | 2.408 | -2.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.86 | 1.079 | -0.8% | +0.00 | +0.00 | -0.0467% |
| DOTUSDT | 0.85 | 2.236 | +1.2% | +0.00 | +0.00 | -0.0011% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
