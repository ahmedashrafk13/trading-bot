# v9 brief - 2026-09-29 12:12 UTC (signal from the 2026-09-29 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-9.40 (-4.7% of budget); from peak $-9.78

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.11 | 1.24 | +1.5% | +0.00 | +0.00 | +0.0027% |
| ETHUSDT | -1.1 | 2.292 | +2.4% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | -0.7 | 1.752 | +1.2% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.1 | 2.253 | +0.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.49 | 2.441 | +1.6% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.37 | 2.377 | +2.7% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.75 | 2.239 | +3.3% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.98 | 2.476 | +12.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.25 | 1.859 | +9.0% | +0.00 | -67.37 | +0.0100% |
| LTCUSDT | 0.09 | 2.38 | -3.2% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.46 | 1.133 | +0.4% | +0.00 | +0.00 | -0.0077% |
| DOTUSDT | -1.27 | 1.732 | +2.2% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
