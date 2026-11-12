# v9 brief - 2026-11-12 12:12 UTC (signal from the 2026-11-12 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-30.34 (-15.2% of budget); from peak $-34.33

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.28 | 2.975 | -1.4% | +0.00 | +0.00 | +0.0055% |
| ETHUSDT | 0.53 | 3.312 | -1.7% | +0.00 | +0.00 | +0.0033% |
| SOLUSDT | 1.22 | 3.513 | -1.8% | +0.00 | +0.00 | +0.0014% |
| BNBUSDT | 0.3 | 2.651 | -2.6% | +0.00 | +0.00 | -0.0051% |
| XRPUSDT | 1.07 | 3.058 | -1.9% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.43 | 2.539 | -2.5% | +0.00 | +0.00 | -0.0004% |
| ADAUSDT | 2.86 | 2.099 | -3.0% | -130.20 | -124.33 | -0.0032% |
| AVAXUSDT | 2.64 | 2.235 | -1.2% | -115.12 | -111.98 | +0.0025% |
| LINKUSDT | 0.78 | 1.842 | -3.8% | +0.00 | +0.00 | +0.0064% |
| LTCUSDT | -0.19 | 1.947 | -3.7% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.66 | 1.124 | -0.3% | +0.00 | +0.00 | -0.0057% |
| DOTUSDT | -0.01 | 1.655 | -2.1% | +0.00 | +0.00 | -0.0128% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
