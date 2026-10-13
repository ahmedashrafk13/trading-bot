# v9 brief - 2026-10-13 12:12 UTC (signal from the 2026-10-13 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+3.99 (+2.0% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.24 | 1.199 | -0.0% | +0.00 | +0.00 | +0.0094% |
| ETHUSDT | -0.37 | 2.607 | -1.8% | +0.00 | +0.00 | -0.0049% |
| SOLUSDT | 1.58 | 2.384 | -4.3% | -160.18 | -148.64 | -0.0021% |
| BNBUSDT | -1.1 | 2.089 | -1.4% | +0.00 | +0.00 | +0.0010% |
| XRPUSDT | 0.46 | 2.478 | -2.9% | +0.00 | -131.33 | -0.0013% |
| DOGEUSDT | -0.52 | 2.361 | -4.1% | +0.00 | +0.00 | -0.0045% |
| ADAUSDT | -1.46 | 1.816 | -7.0% | +0.00 | +0.00 | -0.0079% |
| AVAXUSDT | -1.69 | 1.7 | -6.9% | +89.22 | +0.00 | -0.0114% |
| LINKUSDT | -0.62 | 1.54 | -3.6% | +0.00 | +0.00 | +0.0002% |
| LTCUSDT | -1.28 | 1.91 | -6.0% | +0.00 | +0.00 | +0.0054% |
| TRXUSDT | -0.79 | 1.093 | -0.9% | +0.00 | +0.00 | -0.0404% |
| DOTUSDT | 1.85 | 2.372 | -7.0% | -99.14 | -96.18 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
