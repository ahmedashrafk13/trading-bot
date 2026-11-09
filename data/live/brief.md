# v9 brief - 2026-11-09 18:12 UTC (signal from the 2026-11-09 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-36.19 (-18.1% of budget); from peak $-40.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.24 | 2.776 | -1.3% | +0.00 | +0.00 | +0.0071% |
| ETHUSDT | 1.59 | 3.845 | -4.7% | -163.58 | -148.85 | +0.0100% |
| SOLUSDT | 1.13 | 3.357 | -2.8% | +0.00 | +0.00 | +0.0042% |
| BNBUSDT | 0.42 | 2.644 | -1.3% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.74 | 2.937 | -5.3% | +0.00 | +0.00 | -0.0044% |
| DOGEUSDT | -0.13 | 2.564 | -1.5% | +0.00 | +0.00 | +0.0036% |
| ADAUSDT | 0.09 | 1.877 | -0.4% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.07 | 1.472 | +5.9% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.3 | 1.892 | -0.1% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.53 | 1.705 | +0.2% | +148.53 | +0.00 | -0.0009% |
| TRXUSDT | -0.5 | 1.139 | -1.0% | +0.00 | +0.00 | -0.0037% |
| DOTUSDT | -0.67 | 1.543 | -1.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
