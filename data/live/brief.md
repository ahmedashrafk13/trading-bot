# v9 brief - 2026-10-04 12:12 UTC (signal from the 2026-10-04 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.28 (-3.6% of budget); from peak $-7.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.17 | 1.196 | +0.7% | +0.00 | +0.00 | +0.0070% |
| ETHUSDT | 0.38 | 2.719 | +0.6% | +0.00 | +0.00 | +0.0070% |
| SOLUSDT | -0.7 | 1.731 | +1.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.56 | 2.15 | +2.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.7 | 2.317 | +0.9% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.33 | 2.425 | +0.8% | +0.00 | +0.00 | +0.0022% |
| ADAUSDT | -0.47 | 1.986 | -0.0% | +0.00 | +0.00 | +0.0066% |
| AVAXUSDT | 0.36 | 2.389 | -1.3% | +0.00 | +0.00 | -0.0102% |
| LINKUSDT | 0.35 | 1.768 | +1.2% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | -1.0 | 2.155 | +2.2% | +0.00 | +0.00 | +0.0037% |
| TRXUSDT | -0.31 | 1.179 | -0.1% | +0.00 | +0.00 | -0.0134% |
| DOTUSDT | -0.99 | 1.768 | -0.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
