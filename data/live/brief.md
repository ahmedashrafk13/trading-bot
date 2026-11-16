# v9 brief - 2026-11-16 18:13 UTC (signal from the 2026-11-16 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.85 (-0.9% of budget); from peak $-5.84

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.61 | 2.713 | +0.5% | +0.00 | +0.00 | +0.0072% |
| ETHUSDT | -0.92 | 2.607 | +0.4% | +0.00 | +0.00 | +0.0017% |
| SOLUSDT | 1.1 | 3.604 | -0.3% | +0.00 | +0.00 | -0.0065% |
| BNBUSDT | -1.03 | 2.429 | -0.2% | +0.00 | +170.81 | +0.0100% |
| XRPUSDT | -0.28 | 2.744 | +0.7% | +0.00 | +0.00 | -0.0110% |
| DOGEUSDT | -1.87 | 2.334 | +0.9% | +147.85 | +148.94 | -0.0030% |
| ADAUSDT | 2.43 | 2.176 | -0.3% | -127.45 | -129.56 | -0.0191% |
| AVAXUSDT | -0.35 | 1.609 | -0.6% | +0.00 | +0.00 | -0.0177% |
| LINKUSDT | 0.3 | 1.778 | -0.8% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | 0.37 | 2.056 | -0.5% | +0.00 | +0.00 | +0.0028% |
| TRXUSDT | -1.49 | 0.996 | +0.6% | +0.00 | +0.00 | -0.0052% |
| DOTUSDT | 0.7 | 1.747 | -0.9% | +0.00 | +0.00 | -0.0071% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
