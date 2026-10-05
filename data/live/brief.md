# v9 brief - 2026-10-05 15:38 UTC (signal from the 2026-10-05 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.28 (-3.6% of budget); from peak $-7.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.08 | 1.002 | +1.1% | +0.00 | +0.00 | +0.0036% |
| ETHUSDT | -0.81 | 2.397 | +0.7% | +0.00 | +0.00 | +0.0013% |
| SOLUSDT | -0.79 | 1.695 | -0.4% | +0.00 | +0.00 | -0.0057% |
| BNBUSDT | -0.41 | 2.18 | +0.3% | +0.00 | +0.00 | +0.0093% |
| XRPUSDT | -1.37 | 2.227 | +1.3% | +0.00 | +0.00 | +0.0076% |
| DOGEUSDT | -0.79 | 2.33 | +3.0% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.01 | 2.099 | +11.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.0 | 1.974 | +0.2% | +0.00 | +0.00 | +0.0012% |
| LINKUSDT | 0.24 | 1.746 | +0.9% | +0.00 | +0.00 | +0.0005% |
| LTCUSDT | -1.65 | 2.003 | -0.4% | +131.83 | +0.00 | +0.0072% |
| TRXUSDT | -0.39 | 1.172 | +0.1% | +0.00 | +0.00 | -0.0288% |
| DOTUSDT | -0.98 | 1.759 | +2.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
