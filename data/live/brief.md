# v9 brief - 2026-10-21 06:12 UTC (signal from the 2026-10-21 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.41 (-3.7% of budget); from peak $-11.40

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.47 | 1.464 | +1.2% | +0.00 | +0.00 | +0.0066% |
| ETHUSDT | -0.14 | 2.74 | +1.8% | +0.00 | +0.00 | +0.0042% |
| SOLUSDT | 1.37 | 2.564 | +1.1% | +0.00 | +0.00 | -0.0049% |
| BNBUSDT | 0.75 | 2.414 | +1.8% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.2 | 2.542 | +2.4% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.64 | 2.596 | +2.7% | +0.00 | +0.00 | +0.0030% |
| ADAUSDT | -1.13 | 1.865 | +2.5% | +0.00 | +0.00 | -0.0009% |
| AVAXUSDT | -1.89 | 1.409 | +0.9% | +101.10 | +100.02 | +0.0072% |
| LINKUSDT | -0.65 | 1.577 | +2.5% | +0.00 | +0.00 | +0.0008% |
| LTCUSDT | -2.22 | 1.698 | +2.8% | +132.46 | +0.00 | +0.0044% |
| TRXUSDT | -0.36 | 1.151 | -0.2% | +0.00 | +0.00 | -0.0032% |
| DOTUSDT | 1.2 | 2.192 | +1.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
