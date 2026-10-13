# v9 brief - 2026-10-13 18:12 UTC (signal from the 2026-10-13 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+2.90 (+1.4% of budget); from peak $-1.10

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.08 | 1.238 | +0.7% | +0.00 | +0.00 | +0.0013% |
| ETHUSDT | -0.54 | 2.551 | -0.4% | +0.00 | +0.00 | +0.0051% |
| SOLUSDT | 1.46 | 2.341 | -0.6% | +0.00 | -161.64 | +0.0088% |
| BNBUSDT | -0.88 | 2.114 | -0.5% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.37 | 2.464 | +0.1% | +0.00 | +0.00 | -0.0032% |
| DOGEUSDT | -0.4 | 2.382 | -1.0% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -1.59 | 1.785 | -3.1% | +112.37 | +0.00 | +0.0007% |
| AVAXUSDT | -1.66 | 1.706 | -2.6% | +89.22 | +89.40 | -0.0236% |
| LINKUSDT | -0.6 | 1.544 | -0.1% | +0.00 | +0.00 | +0.0037% |
| LTCUSDT | -1.22 | 1.92 | -2.0% | +0.00 | +0.00 | +0.0057% |
| TRXUSDT | -0.86 | 1.084 | -0.7% | +0.00 | +0.00 | -0.0155% |
| DOTUSDT | 1.84 | 2.374 | -4.5% | -99.14 | -95.73 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
