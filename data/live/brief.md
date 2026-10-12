# v9 brief - 2026-10-12 06:13 UTC (signal from the 2026-10-12 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.74 (-1.4% of budget); from peak $-3.12

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.28 | 1.346 | +1.2% | +0.00 | +0.00 | +0.0041% |
| ETHUSDT | 0.02 | 2.729 | +2.4% | +0.00 | +0.00 | +0.0031% |
| SOLUSDT | 1.28 | 2.276 | +3.2% | +0.00 | -168.66 | +0.0100% |
| BNBUSDT | -0.17 | 2.216 | +0.9% | +0.00 | +0.00 | +0.0086% |
| XRPUSDT | -0.61 | 2.319 | +1.5% | +0.00 | +0.00 | +0.0062% |
| DOGEUSDT | -0.47 | 2.372 | +2.7% | +0.00 | +0.00 | +0.0038% |
| ADAUSDT | -0.74 | 1.976 | +2.7% | +0.00 | +0.00 | +0.0048% |
| AVAXUSDT | -1.38 | 1.764 | +7.6% | +0.00 | +94.83 | -0.0017% |
| LINKUSDT | -0.09 | 1.636 | +4.0% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.48 | 1.888 | +2.7% | +0.00 | +0.00 | -0.0017% |
| TRXUSDT | -0.72 | 1.106 | +0.6% | +0.00 | +0.00 | -0.0035% |
| DOTUSDT | 1.7 | 2.307 | +3.1% | -103.43 | -103.90 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
