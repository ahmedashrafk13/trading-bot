# v9 brief - 2026-10-30 16:25 UTC (signal from the 2026-10-30 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-34.30 (-17.2% of budget); from peak $-38.29

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.78 | 2.463 | -3.5% | -202.76 | +0.00 | +0.0100% |
| ETHUSDT | -0.32 | 2.839 | -3.8% | +0.00 | +0.00 | -0.0157% |
| SOLUSDT | 0.99 | 2.881 | -3.8% | +0.00 | +0.00 | -0.0034% |
| BNBUSDT | 1.14 | 2.644 | -5.5% | +0.00 | +0.00 | -0.0284% |
| XRPUSDT | -0.19 | 2.607 | -3.5% | +0.00 | +0.00 | -0.0218% |
| DOGEUSDT | -1.18 | 2.383 | -3.7% | +0.00 | +0.00 | -0.0144% |
| ADAUSDT | -1.48 | 1.682 | -4.1% | +0.00 | +0.00 | -0.0078% |
| AVAXUSDT | -0.57 | 1.583 | -4.0% | +0.00 | +0.00 | -0.0013% |
| LINKUSDT | 0.33 | 1.695 | -4.7% | +0.00 | +0.00 | -0.0161% |
| LTCUSDT | -0.0 | 2.016 | -5.0% | +0.00 | -150.74 | -0.0025% |
| TRXUSDT | 2.22 | 1.537 | +2.5% | -208.67 | +0.00 | -0.0060% |
| DOTUSDT | -1.79 | 1.404 | -4.1% | +68.57 | +0.00 | -0.0290% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
