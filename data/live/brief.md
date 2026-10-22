# v9 brief - 2026-10-22 06:13 UTC (signal from the 2026-10-22 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-17.33 (-8.7% of budget); from peak $-21.32

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.34 | 1.435 | +0.2% | +0.00 | +0.00 | +0.0055% |
| ETHUSDT | 0.17 | 2.827 | -0.0% | +0.00 | +195.13 | +0.0021% |
| SOLUSDT | 1.35 | 2.584 | -0.6% | +0.00 | +0.00 | -0.0071% |
| BNBUSDT | 1.39 | 2.549 | -0.5% | +0.00 | +0.00 | -0.0151% |
| XRPUSDT | -0.07 | 2.495 | +0.8% | +0.00 | +0.00 | +0.0048% |
| DOGEUSDT | 0.25 | 2.552 | -1.8% | +0.00 | +0.00 | -0.0025% |
| ADAUSDT | -1.01 | 1.878 | -1.5% | +0.00 | +0.00 | -0.0190% |
| AVAXUSDT | -1.65 | 1.437 | -2.6% | +101.10 | +97.65 | -0.0035% |
| LINKUSDT | -0.27 | 1.64 | -0.6% | +0.00 | +0.00 | -0.0002% |
| LTCUSDT | -1.63 | 1.777 | -1.2% | +132.46 | +126.86 | -0.0028% |
| TRXUSDT | -0.9 | 1.082 | -0.2% | +0.00 | +0.00 | -0.0269% |
| DOTUSDT | -0.31 | 1.831 | -2.3% | +0.00 | +0.00 | -0.0027% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
