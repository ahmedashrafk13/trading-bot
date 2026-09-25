# v9 brief - 2026-09-25 13:46 UTC (signal from the 2026-09-25 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.41 (-0.7% of budget); from peak $-1.41

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.06 | 1.197 | +1.3% | +0.00 | +0.00 | +0.0022% |
| ETHUSDT | -0.09 | 2.525 | +2.6% | +0.00 | +0.00 | +0.0032% |
| SOLUSDT | -1.42 | 1.63 | +6.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -1.07 | 2.124 | +1.2% | +0.00 | +0.00 | -0.0227% |
| XRPUSDT | -0.2 | 2.366 | +8.5% | +0.00 | +0.00 | +0.0033% |
| DOGEUSDT | 1.08 | 2.69 | +5.8% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 2.1 | 2.505 | +8.2% | -67.24 | -69.62 | +0.0100% |
| AVAXUSDT | -0.4 | 2.028 | +4.6% | +0.00 | +0.00 | +0.0056% |
| LINKUSDT | 1.35 | 1.807 | +15.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.74 | 2.514 | +6.2% | +0.00 | +0.00 | +0.0078% |
| TRXUSDT | -0.63 | 1.13 | -0.7% | +0.00 | +0.00 | -0.0182% |
| DOTUSDT | -1.54 | 1.687 | +7.3% | +49.27 | +50.12 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
