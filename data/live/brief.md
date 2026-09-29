# v9 brief - 2026-09-29 00:22 UTC (signal from the 2026-09-29 00:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-10.33 (-5.2% of budget); from peak $-10.71

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.58 | 1.361 | -1.1% | +0.00 | +0.00 | +0.0054% |
| ETHUSDT | 0.06 | 2.595 | +0.0% | +0.00 | +0.00 | +0.0091% |
| SOLUSDT | -0.27 | 1.855 | -2.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.49 | 2.183 | -1.9% | +0.00 | +0.00 | +0.0043% |
| XRPUSDT | 0.9 | 2.493 | -1.3% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.36 | 2.519 | -3.1% | +0.00 | +0.00 | +0.0023% |
| ADAUSDT | 0.74 | 2.23 | -3.1% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.33 | 2.263 | -2.6% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.55 | 1.912 | +10.2% | -67.89 | -68.23 | +0.0100% |
| LTCUSDT | 1.08 | 2.63 | -2.9% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.51 | 1.129 | +0.7% | +0.00 | +0.00 | -0.0238% |
| DOTUSDT | -0.76 | 1.845 | -6.8% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
