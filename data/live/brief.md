# v9 brief - 2026-10-25 10:13 UTC (signal from the 2026-10-25 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-24.01 (-12.0% of budget); from peak $-28.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.78 | 2.094 | -0.2% | -162.66 | -160.77 | +0.0100% |
| ETHUSDT | 0.85 | 3.105 | -1.0% | +0.00 | +0.00 | +0.0089% |
| SOLUSDT | 1.46 | 2.854 | -0.4% | +0.00 | -90.79 | -0.0027% |
| BNBUSDT | 0.26 | 2.375 | +0.8% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.97 | 3.1 | +1.0% | -92.86 | -94.95 | +0.0090% |
| DOGEUSDT | 1.65 | 2.741 | -1.6% | -84.16 | +0.00 | +0.0057% |
| ADAUSDT | -1.13 | 1.796 | -2.3% | +0.00 | +61.64 | +0.0100% |
| AVAXUSDT | -1.25 | 1.454 | -1.5% | +0.00 | +55.49 | +0.0049% |
| LINKUSDT | -0.19 | 1.666 | -3.0% | +0.00 | +0.00 | -0.0045% |
| LTCUSDT | -1.98 | 1.678 | -1.0% | +88.78 | +0.00 | +0.0100% |
| TRXUSDT | 0.03 | 1.179 | -0.4% | +0.00 | +0.00 | -0.0194% |
| DOTUSDT | -1.92 | 1.502 | -4.1% | +51.53 | +0.00 | +0.0068% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
