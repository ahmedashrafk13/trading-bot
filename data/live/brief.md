# v9 brief - 2026-09-26 18:39 UTC (signal from the 2026-09-26 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.28 (-0.6% of budget); from peak $-1.28

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.39 | 1.294 | +0.4% | +0.00 | +0.00 | +0.0040% |
| ETHUSDT | 0.47 | 2.696 | +0.2% | +0.00 | +0.00 | -0.0007% |
| SOLUSDT | -2.02 | 1.486 | +0.4% | +86.99 | +84.78 | +0.0100% |
| BNBUSDT | -1.37 | 2.054 | -0.1% | +0.00 | +0.00 | +0.0029% |
| XRPUSDT | -0.45 | 2.332 | -1.8% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.06 | 2.469 | +0.7% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.82 | 2.501 | +0.7% | -67.24 | -69.84 | +0.0100% |
| AVAXUSDT | 0.49 | 2.293 | +4.3% | +0.00 | +0.00 | -0.0043% |
| LINKUSDT | 0.76 | 1.713 | +4.0% | +0.00 | -72.37 | +0.0022% |
| LTCUSDT | 0.11 | 2.353 | +3.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.92 | 1.075 | -0.4% | +0.00 | +0.00 | -0.0285% |
| DOTUSDT | 0.17 | 2.058 | +7.8% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
