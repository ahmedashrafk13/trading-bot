# v9 brief - 2026-10-29 13:09 UTC (signal from the 2026-10-29 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-29.15 (-14.6% of budget); from peak $-33.14

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.43 | 2.191 | -1.4% | +0.00 | +0.00 | +0.0053% |
| ETHUSDT | 1.53 | 3.46 | -1.5% | -172.03 | +0.00 | +0.0064% |
| SOLUSDT | 1.78 | 3.284 | -2.3% | -157.54 | -160.90 | +0.0068% |
| BNBUSDT | 1.47 | 2.683 | -2.8% | +0.00 | +0.00 | +0.0088% |
| XRPUSDT | 1.42 | 3.068 | -2.5% | +0.00 | +0.00 | +0.0006% |
| DOGEUSDT | 1.02 | 2.69 | -1.9% | +0.00 | +0.00 | +0.0058% |
| ADAUSDT | -0.74 | 1.836 | -2.6% | +0.00 | +0.00 | +0.0032% |
| AVAXUSDT | -0.71 | 1.556 | -2.4% | +0.00 | +0.00 | +0.0077% |
| LINKUSDT | -0.14 | 1.643 | -1.2% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 1.65 | 2.36 | +0.4% | -150.43 | +156.82 | +0.0040% |
| TRXUSDT | 0.3 | 1.232 | -0.1% | +0.00 | +0.00 | +0.0031% |
| DOTUSDT | -1.47 | 1.498 | -3.5% | +0.00 | +0.00 | +0.0016% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
