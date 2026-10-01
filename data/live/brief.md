# v9 brief - 2026-10-01 18:12 UTC (signal from the 2026-10-01 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.97 (-4.0% of budget); from peak $-8.35

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.66 | 1.075 | +1.0% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | 0.0 | 2.598 | +0.7% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.03 | 1.919 | -0.7% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.33 | 2.193 | +0.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.53 | 2.463 | +0.1% | +0.00 | -74.34 | +0.0100% |
| DOGEUSDT | 1.35 | 2.745 | +0.6% | +0.00 | -65.88 | +0.0100% |
| ADAUSDT | 0.68 | 2.249 | +1.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.17 | 2.621 | -0.5% | +0.00 | +0.00 | +0.0051% |
| LINKUSDT | 1.65 | 2.035 | -0.3% | -69.52 | +0.00 | +0.0100% |
| LTCUSDT | -1.33 | 2.086 | +1.7% | +0.00 | +0.00 | -0.0036% |
| TRXUSDT | -0.55 | 1.122 | -0.8% | +0.00 | +0.00 | -0.0491% |
| DOTUSDT | 0.16 | 2.071 | -5.0% | +0.00 | +0.00 | +0.0047% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
