# v9 brief - 2026-11-05 18:12 UTC (signal from the 2026-11-05 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-42.21 (-21.1% of budget); from peak $-46.20

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.82 | 2.761 | -5.6% | -116.16 | +0.00 | +0.0066% |
| ETHUSDT | 1.41 | 3.531 | -7.0% | +0.00 | +158.00 | -0.0107% |
| SOLUSDT | 2.11 | 3.63 | -6.9% | -71.93 | +0.00 | -0.0075% |
| BNBUSDT | 1.7 | 2.872 | -3.5% | -92.97 | +0.00 | +0.0100% |
| XRPUSDT | 1.0 | 2.954 | -5.8% | +0.00 | +0.00 | -0.0065% |
| DOGEUSDT | 2.22 | 2.922 | -6.9% | -71.07 | +0.00 | -0.0339% |
| ADAUSDT | 1.08 | 2.096 | -8.0% | +0.00 | +0.00 | -0.0243% |
| AVAXUSDT | 0.76 | 1.856 | -7.1% | +0.00 | +0.00 | -0.0024% |
| LINKUSDT | 3.06 | 2.134 | -7.6% | -56.50 | +0.00 | -0.0232% |
| LTCUSDT | 2.38 | 2.476 | -8.1% | -71.37 | +0.00 | -0.0156% |
| TRXUSDT | -0.98 | 1.076 | -1.0% | +0.00 | +0.00 | -0.0220% |
| DOTUSDT | -0.72 | 1.554 | -6.1% | +0.00 | +0.00 | -0.0138% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
