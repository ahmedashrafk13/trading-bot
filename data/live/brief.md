# v9 brief - 2026-11-01 10:48 UTC (signal from the 2026-11-01 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-25.55 (-12.8% of budget); from peak $-29.54

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.62 | 2.54 | +0.8% | -258.82 | -155.98 | +0.0069% |
| ETHUSDT | -0.85 | 2.706 | +1.2% | +0.00 | +0.00 | -0.0036% |
| SOLUSDT | 1.32 | 3.149 | -0.2% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | 1.36 | 2.727 | +0.3% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.48 | 2.536 | +0.6% | +0.00 | +0.00 | -0.0054% |
| DOGEUSDT | -0.31 | 2.49 | +0.6% | +0.00 | +115.12 | +0.0076% |
| ADAUSDT | -0.54 | 1.842 | +0.5% | +0.00 | +0.00 | +0.0091% |
| AVAXUSDT | -0.35 | 1.619 | +5.1% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 2.86 | 1.97 | +2.5% | -113.50 | +0.00 | +0.0072% |
| LTCUSDT | 0.55 | 2.105 | +1.8% | +0.00 | +0.00 | +0.0088% |
| TRXUSDT | -0.75 | 1.114 | -4.5% | +0.00 | +0.00 | -0.0002% |
| DOTUSDT | -1.57 | 1.401 | -0.7% | +85.89 | +68.90 | -0.0066% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
