# v9 brief - 2026-11-15 08:51 UTC (signal from the 2026-11-15 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.56 (-1.3% of budget); from peak $-6.55

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.8 | 2.788 | -4.0% | +0.00 | +0.00 | +0.0054% |
| ETHUSDT | -1.26 | 2.481 | -5.5% | +0.00 | +0.00 | -0.0044% |
| SOLUSDT | 0.83 | 3.433 | -6.8% | +0.00 | +0.00 | -0.0140% |
| BNBUSDT | -2.04 | 2.296 | -4.5% | +175.16 | +123.73 | +0.0000% |
| XRPUSDT | -0.9 | 2.61 | -3.8% | +0.00 | +0.00 | -0.0227% |
| DOGEUSDT | -1.87 | 2.357 | -8.1% | +145.92 | +103.87 | -0.0227% |
| ADAUSDT | 1.84 | 2.069 | -9.2% | -127.40 | -91.80 | -0.0114% |
| AVAXUSDT | 0.33 | 1.774 | -10.9% | +0.00 | +0.00 | -0.0134% |
| LINKUSDT | -0.7 | 1.625 | -5.9% | +0.00 | +0.00 | -0.0098% |
| LTCUSDT | 0.01 | 1.983 | -8.9% | +0.00 | +0.00 | -0.0227% |
| TRXUSDT | -1.26 | 1.035 | -1.8% | +0.00 | +0.00 | -0.0725% |
| DOTUSDT | -0.09 | 1.618 | -10.1% | +0.00 | +0.00 | -0.0096% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
