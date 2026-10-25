# v9 brief - 2026-10-25 12:12 UTC (signal from the 2026-10-25 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-24.38 (-12.2% of budget); from peak $-28.37

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.75 | 2.098 | -0.0% | -195.78 | -160.96 | +0.0068% |
| ETHUSDT | 1.09 | 3.189 | -1.1% | +0.00 | +0.00 | +0.0028% |
| SOLUSDT | 1.56 | 2.922 | -0.2% | -114.68 | +0.00 | -0.0055% |
| BNBUSDT | 0.1 | 2.345 | +1.7% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.29 | 2.912 | +1.4% | +0.00 | -95.13 | +0.0100% |
| DOGEUSDT | -0.07 | 2.517 | -1.1% | +0.00 | -84.13 | +0.0053% |
| ADAUSDT | -1.11 | 1.797 | -1.7% | +0.00 | +0.00 | +0.0032% |
| AVAXUSDT | -1.16 | 1.478 | -0.9% | +0.00 | +0.00 | +0.0016% |
| LINKUSDT | -0.47 | 1.621 | -1.7% | +0.00 | +0.00 | -0.0031% |
| LTCUSDT | -1.89 | 1.689 | +0.0% | +106.83 | +84.54 | +0.0100% |
| TRXUSDT | -0.08 | 1.166 | -0.4% | +0.00 | +0.00 | -0.0140% |
| DOTUSDT | -2.01 | 1.48 | -3.5% | +62.70 | +0.00 | -0.0018% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
