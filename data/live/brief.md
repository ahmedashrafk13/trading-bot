# v9 brief - 2026-10-23 15:21 UTC (signal from the 2026-10-23 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-26.00 (-13.0% of budget); from peak $-29.99

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.41 | 2.193 | -0.0% | -149.38 | -81.46 | +0.0042% |
| ETHUSDT | 1.92 | 3.411 | +0.1% | -98.77 | -72.02 | +0.0056% |
| SOLUSDT | 1.75 | 2.874 | +0.1% | -84.62 | -73.05 | +0.0092% |
| BNBUSDT | 0.77 | 2.457 | +2.0% | +0.00 | -112.16 | +0.0100% |
| XRPUSDT | 2.85 | 3.219 | -0.4% | -80.63 | -70.46 | +0.0100% |
| DOGEUSDT | 1.34 | 2.694 | +1.2% | +0.00 | +0.00 | +0.0014% |
| ADAUSDT | -1.37 | 1.779 | +0.1% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.4 | 1.466 | -0.4% | +0.00 | +0.00 | -0.0009% |
| LINKUSDT | -0.05 | 1.68 | +0.4% | +0.00 | +0.00 | +0.0006% |
| LTCUSDT | -1.91 | 1.71 | -0.7% | +66.61 | +0.00 | +0.0002% |
| TRXUSDT | -1.03 | 1.061 | -0.1% | +0.00 | +0.00 | -0.0208% |
| DOTUSDT | 0.43 | 2.007 | +4.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
