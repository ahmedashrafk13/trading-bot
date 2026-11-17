# v9 brief - 2026-11-17 18:12 UTC (signal from the 2026-11-17 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.78 (-1.4% of budget); from peak $-6.77

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.39 | 2.592 | -1.7% | +0.00 | +0.00 | +0.0030% |
| ETHUSDT | -0.78 | 2.652 | -1.8% | +0.00 | +0.00 | -0.0059% |
| SOLUSDT | 0.56 | 3.38 | +1.6% | +0.00 | +0.00 | -0.0165% |
| BNBUSDT | -0.77 | 2.463 | -0.5% | +0.00 | +0.00 | -0.0020% |
| XRPUSDT | 0.0 | 2.805 | +0.1% | +0.00 | +0.00 | -0.0079% |
| DOGEUSDT | -1.69 | 2.346 | -1.1% | +147.71 | +147.03 | -0.0019% |
| ADAUSDT | 2.42 | 2.212 | -0.5% | -127.45 | -128.45 | -0.0087% |
| AVAXUSDT | -0.47 | 1.581 | -0.8% | +0.00 | +0.00 | -0.0105% |
| LINKUSDT | 0.1 | 1.757 | -0.5% | +0.00 | +0.00 | -0.0074% |
| LTCUSDT | 0.56 | 2.096 | -0.8% | +0.00 | +0.00 | +0.0047% |
| TRXUSDT | -0.75 | 1.075 | -0.1% | +0.00 | +0.00 | -0.0284% |
| DOTUSDT | 0.9 | 1.782 | +0.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
