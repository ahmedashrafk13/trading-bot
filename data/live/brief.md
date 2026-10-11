# v9 brief - 2026-10-11 19:12 UTC (signal from the 2026-10-11 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.25 (-1.1% of budget); from peak $-2.63

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.48 | 1.409 | +0.9% | +0.00 | +0.00 | +0.0044% |
| ETHUSDT | 0.32 | 2.821 | +1.2% | +0.00 | +0.00 | -0.0006% |
| SOLUSDT | 1.15 | 2.228 | +2.0% | +0.00 | -122.51 | +0.0100% |
| BNBUSDT | -0.82 | 2.134 | +0.5% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.79 | 2.295 | +0.9% | +0.00 | +0.00 | +0.0051% |
| DOGEUSDT | -0.47 | 2.373 | +1.2% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.6 | 2.006 | -0.2% | +0.00 | +0.00 | +0.0074% |
| AVAXUSDT | -1.99 | 1.623 | +3.6% | +93.76 | +75.88 | +0.0100% |
| LINKUSDT | -0.25 | 1.605 | +2.4% | +0.00 | +0.00 | -0.0090% |
| LTCUSDT | -1.52 | 1.889 | +0.8% | +142.04 | +103.09 | +0.0012% |
| TRXUSDT | -0.76 | 1.104 | +0.1% | +0.00 | +0.00 | -0.0062% |
| DOTUSDT | 2.15 | 2.426 | -0.4% | -103.43 | -79.74 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
