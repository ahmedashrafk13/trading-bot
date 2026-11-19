# v9 brief - 2026-11-19 07:58 UTC (signal from the 2026-11-19 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-5.82 (-2.9% of budget); from peak $-9.81

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.86 | 2.982 | -2.0% | +0.00 | +0.00 | +0.0055% |
| ETHUSDT | -1.39 | 2.357 | -0.6% | +0.00 | +0.00 | +0.0039% |
| SOLUSDT | 0.64 | 3.438 | -0.6% | +0.00 | +0.00 | -0.0003% |
| BNBUSDT | -0.35 | 2.526 | -0.9% | +0.00 | +0.00 | +0.0051% |
| XRPUSDT | 0.76 | 3.003 | -1.1% | +0.00 | +0.00 | +0.0020% |
| DOGEUSDT | -1.22 | 2.402 | -0.7% | +0.00 | +0.00 | +0.0041% |
| ADAUSDT | 1.64 | 2.157 | -1.0% | -138.97 | -142.85 | +0.0088% |
| AVAXUSDT | -0.43 | 1.593 | -1.8% | +0.00 | +0.00 | +0.0010% |
| LINKUSDT | -0.05 | 1.751 | -1.3% | +0.00 | +0.00 | +0.0056% |
| LTCUSDT | -0.07 | 1.982 | -0.3% | +0.00 | +0.00 | +0.0089% |
| TRXUSDT | 1.58 | 1.333 | +1.5% | -244.18 | +0.00 | -0.0007% |
| DOTUSDT | 0.74 | 1.752 | -1.7% | +0.00 | +0.00 | +0.0082% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
