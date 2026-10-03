# v9 brief - 2026-10-03 18:13 UTC (signal from the 2026-10-03 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-6.45 (-3.2% of budget); from peak $-6.83

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.04 | 1.235 | +0.3% | +0.00 | +0.00 | -0.0010% |
| ETHUSDT | 0.98 | 2.888 | +0.2% | +0.00 | +0.00 | +0.0018% |
| SOLUSDT | -0.09 | 1.877 | +0.2% | +0.00 | +0.00 | +0.0015% |
| BNBUSDT | -1.09 | 2.055 | +1.9% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.52 | 2.619 | -0.3% | -133.41 | -113.20 | -0.0023% |
| DOGEUSDT | 0.32 | 2.552 | -1.3% | +0.00 | +0.00 | +0.0051% |
| ADAUSDT | 0.19 | 2.151 | -1.8% | +0.00 | +0.00 | +0.0028% |
| AVAXUSDT | 0.66 | 2.479 | +0.7% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.33 | 1.754 | -1.6% | +0.00 | +0.00 | +0.0029% |
| LTCUSDT | -0.53 | 2.262 | -1.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.37 | 1.163 | -0.1% | +0.00 | +0.00 | -0.0450% |
| DOTUSDT | -1.32 | 1.709 | -0.7% | +0.00 | +73.48 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
