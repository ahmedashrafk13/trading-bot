# v9 brief - 2026-10-14 15:46 UTC (signal from the 2026-10-14 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-1.37 (-0.7% of budget); from peak $-5.36

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.3 | 1.329 | +0.1% | +0.00 | +0.00 | +0.0014% |
| ETHUSDT | 0.42 | 2.849 | +0.1% | +0.00 | +0.00 | -0.0031% |
| SOLUSDT | 1.42 | 2.333 | +0.9% | +0.00 | +0.00 | -0.0048% |
| BNBUSDT | 1.47 | 2.412 | +0.5% | +0.00 | +0.00 | -0.0010% |
| XRPUSDT | 2.24 | 2.796 | +1.2% | -138.22 | -134.57 | +0.0032% |
| DOGEUSDT | -0.1 | 2.435 | +1.1% | +0.00 | +0.00 | -0.0020% |
| ADAUSDT | -1.55 | 1.789 | +0.8% | +112.37 | +108.17 | -0.0046% |
| AVAXUSDT | -2.28 | 1.554 | -0.4% | +89.22 | +85.55 | +0.0026% |
| LINKUSDT | -0.34 | 1.594 | +0.5% | +0.00 | +0.00 | +0.0056% |
| LTCUSDT | -0.32 | 2.11 | +0.9% | +0.00 | +0.00 | +0.0071% |
| TRXUSDT | -0.85 | 1.084 | +1.5% | +0.00 | +0.00 | +0.0049% |
| DOTUSDT | 0.17 | 1.943 | -2.0% | +0.00 | +0.00 | +0.0008% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
