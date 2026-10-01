# v9 brief - 2026-10-01 12:12 UTC (signal from the 2026-10-01 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.34 (-3.7% of budget); from peak $-7.72

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.69 | 1.42 | -0.0% | +0.00 | +0.00 | +0.0052% |
| ETHUSDT | 0.15 | 2.64 | +0.3% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.39 | 2.013 | -1.3% | +0.00 | +0.00 | -0.0114% |
| BNBUSDT | -0.21 | 2.215 | +0.1% | +0.00 | +0.00 | +0.0070% |
| XRPUSDT | 2.1 | 2.678 | -1.5% | -73.79 | -73.88 | -0.0047% |
| DOGEUSDT | 1.87 | 2.857 | -0.9% | -65.91 | +0.00 | +0.0002% |
| ADAUSDT | 0.9 | 2.31 | +0.2% | +0.00 | +0.00 | -0.0148% |
| AVAXUSDT | 1.04 | 2.566 | -1.0% | +0.00 | +0.00 | -0.0027% |
| LINKUSDT | 1.41 | 1.964 | -0.3% | +0.00 | -64.81 | +0.0026% |
| LTCUSDT | -0.9 | 2.174 | -0.6% | +0.00 | +0.00 | +0.0054% |
| TRXUSDT | -0.22 | 1.177 | -2.5% | +0.00 | +0.00 | -0.1159% |
| DOTUSDT | 0.66 | 2.198 | -1.7% | +0.00 | +0.00 | +0.0023% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
