# v9 brief - 2026-11-15 00:12 UTC (signal from the 2026-11-15 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.31 (-1.7% of budget); from peak $-7.31

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.19 | 3.08 | -6.1% | +0.00 | +0.00 | +0.0088% |
| ETHUSDT | -0.3 | 2.926 | -8.3% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.9 | 3.462 | -10.2% | +0.00 | +0.00 | +0.0099% |
| BNBUSDT | -2.25 | 2.274 | -7.7% | +125.86 | +0.00 | +0.0100% |
| XRPUSDT | -0.64 | 2.668 | -9.6% | +0.00 | +0.00 | -0.0075% |
| DOGEUSDT | -2.0 | 2.345 | -11.1% | +103.48 | +0.00 | +0.0100% |
| ADAUSDT | 1.79 | 2.06 | -12.4% | -90.90 | +0.00 | -0.0253% |
| AVAXUSDT | 0.93 | 1.929 | -13.8% | +0.00 | +0.00 | -0.0092% |
| LINKUSDT | -0.58 | 1.642 | -9.9% | +0.00 | +0.00 | -0.0277% |
| LTCUSDT | -0.13 | 1.957 | -9.9% | +0.00 | +0.00 | -0.0033% |
| TRXUSDT | -1.5 | 1.01 | -1.7% | +159.76 | +0.00 | -0.0250% |
| DOTUSDT | 0.06 | 1.648 | -13.7% | +0.00 | +0.00 | -0.0051% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
