# v9 brief - 2026-11-03 19:57 UTC (signal from the 2026-11-03 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-23.55 (-11.8% of budget); from peak $-27.54

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.25 | 2.421 | +0.7% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -2.33 | 2.258 | +1.6% | +178.21 | +0.00 | +0.0084% |
| SOLUSDT | 0.98 | 3.068 | +1.3% | +0.00 | -149.04 | +0.0057% |
| BNBUSDT | 1.4 | 2.784 | -0.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -1.48 | 2.296 | +3.4% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.62 | 2.635 | +1.6% | +0.00 | -147.00 | +0.0100% |
| ADAUSDT | 0.06 | 1.94 | +0.9% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.43 | 1.788 | +1.7% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 2.74 | 2.01 | +0.1% | -113.50 | -111.51 | +0.0100% |
| LTCUSDT | -0.08 | 1.974 | +0.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.37 | 1.159 | +1.8% | +0.00 | +0.00 | +0.0100% |
| DOTUSDT | -0.72 | 1.566 | -0.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
