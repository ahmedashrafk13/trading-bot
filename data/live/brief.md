# v9 brief - 2026-11-19 18:12 UTC (signal from the 2026-11-19 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.65 (-1.8% of budget); from peak $-7.64

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.8 | 2.957 | -0.5% | +0.00 | +0.00 | +0.0033% |
| ETHUSDT | -0.84 | 2.587 | +0.2% | +0.00 | +159.40 | +0.0040% |
| SOLUSDT | 0.6 | 3.431 | +0.4% | +0.00 | +0.00 | -0.0088% |
| BNBUSDT | -0.44 | 2.509 | +0.3% | +0.00 | +0.00 | +0.0098% |
| XRPUSDT | 0.45 | 2.929 | -0.9% | +0.00 | +0.00 | -0.0025% |
| DOGEUSDT | -0.69 | 2.477 | -0.5% | +0.00 | +0.00 | -0.0155% |
| ADAUSDT | 1.72 | 2.179 | +0.7% | -143.00 | +0.00 | -0.0002% |
| AVAXUSDT | -0.48 | 1.587 | +0.5% | +0.00 | +0.00 | -0.0302% |
| LINKUSDT | 0.12 | 1.776 | -0.6% | +0.00 | +0.00 | -0.0075% |
| LTCUSDT | 0.6 | 2.114 | -2.6% | +0.00 | +0.00 | -0.0104% |
| TRXUSDT | 1.77 | 1.362 | +0.5% | -244.18 | -241.89 | -0.0188% |
| DOTUSDT | 0.46 | 1.687 | -0.1% | +0.00 | +0.00 | -0.0151% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
