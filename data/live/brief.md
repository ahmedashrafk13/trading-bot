# v9 brief - 2026-10-11 07:14 UTC (signal from the 2026-10-11 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.88 (-1.4% of budget); from peak $-3.26

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.6 | 1.447 | +0.2% | +0.00 | +0.00 | -0.0012% |
| ETHUSDT | 0.7 | 2.942 | +0.2% | +0.00 | +0.00 | -0.0050% |
| SOLUSDT | 1.68 | 2.397 | -0.7% | -131.05 | -153.54 | +0.0068% |
| BNBUSDT | -0.7 | 2.153 | -0.5% | +0.00 | +0.00 | -0.0035% |
| XRPUSDT | -0.47 | 2.341 | -1.2% | +0.00 | +0.00 | +0.0056% |
| DOGEUSDT | -0.45 | 2.376 | -1.4% | +0.00 | +0.00 | -0.0010% |
| ADAUSDT | -0.24 | 2.095 | -2.7% | +0.00 | +0.00 | +0.0000% |
| AVAXUSDT | -1.76 | 1.702 | -3.4% | +75.27 | +0.00 | -0.0028% |
| LINKUSDT | -0.37 | 1.585 | -0.2% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.67 | 1.871 | -0.4% | +114.03 | +0.00 | +0.0067% |
| TRXUSDT | -0.96 | 1.08 | -0.2% | +0.00 | +0.00 | -0.0244% |
| DOTUSDT | 1.88 | 2.36 | -2.9% | -79.65 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
