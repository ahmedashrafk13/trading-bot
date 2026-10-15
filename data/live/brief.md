# v9 brief - 2026-10-15 00:26 UTC (signal from the 2026-10-15 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-0.07 (-0.0% of budget); from peak $-4.06

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.67 | 1.772 | -1.8% | -95.95 | +0.00 | +0.0065% |
| ETHUSDT | 1.81 | 3.374 | -3.0% | -74.74 | -72.76 | +0.0097% |
| SOLUSDT | 1.95 | 2.561 | -2.4% | -56.17 | -62.63 | -0.0012% |
| BNBUSDT | 2.53 | 2.583 | -1.5% | -92.21 | -109.58 | +0.0096% |
| XRPUSDT | 2.99 | 2.981 | -2.5% | -49.31 | -62.51 | +0.0026% |
| DOGEUSDT | 0.4 | 2.524 | -3.0% | +0.00 | +0.00 | -0.0021% |
| ADAUSDT | -1.34 | 1.832 | -2.4% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -2.28 | 1.534 | -2.1% | +31.60 | +39.95 | +0.0100% |
| LINKUSDT | -0.6 | 1.552 | -3.5% | +0.00 | +0.00 | -0.0071% |
| LTCUSDT | 0.45 | 2.276 | -3.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 0.19 | 1.187 | +1.6% | +0.00 | +0.00 | -0.0009% |
| DOTUSDT | 0.03 | 1.907 | -1.2% | +0.00 | +0.00 | +0.0004% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
