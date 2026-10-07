# v9 brief - 2026-10-07 11:27 UTC (signal from the 2026-10-07 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-4.80 (-2.4% of budget); from peak $-5.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.62 | 1.401 | -1.4% | +0.00 | +0.00 | +0.0012% |
| ETHUSDT | 2.12 | 3.273 | -2.9% | -116.66 | +0.00 | -0.0202% |
| SOLUSDT | 0.09 | 1.884 | -0.8% | +0.00 | +0.00 | -0.0070% |
| BNBUSDT | 1.57 | 2.539 | -1.4% | -145.97 | +0.00 | -0.0080% |
| XRPUSDT | 2.18 | 2.715 | -1.8% | -73.14 | +0.00 | +0.0046% |
| DOGEUSDT | 0.94 | 2.64 | -4.4% | +0.00 | +0.00 | +0.0092% |
| ADAUSDT | 1.65 | 2.628 | -4.2% | -64.23 | -115.57 | -0.0138% |
| AVAXUSDT | 1.02 | 2.611 | -0.1% | +0.00 | +0.00 | -0.0179% |
| LINKUSDT | -0.39 | 1.607 | -1.0% | +0.00 | +0.00 | -0.0056% |
| LTCUSDT | -0.39 | 2.237 | -2.7% | +0.00 | +127.68 | -0.0054% |
| TRXUSDT | -0.74 | 1.124 | -0.8% | +0.00 | +0.00 | -0.0247% |
| DOTUSDT | -0.65 | 1.813 | -8.6% | +0.00 | +0.00 | +0.0027% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
