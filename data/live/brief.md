# v9 brief - 2026-11-25 15:10 UTC (signal from the 2026-11-25 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+26.70 (+13.3% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.24 | 2.716 | -3.0% | +0.00 | +0.00 | +0.0010% |
| ETHUSDT | -1.14 | 2.196 | -3.8% | +0.00 | +0.00 | +0.0018% |
| SOLUSDT | 0.9 | 3.647 | -4.7% | +0.00 | +0.00 | -0.0142% |
| BNBUSDT | -0.55 | 2.486 | -2.3% | +0.00 | +0.00 | +0.0021% |
| XRPUSDT | 0.46 | 2.922 | -2.7% | +0.00 | +0.00 | -0.0026% |
| DOGEUSDT | -0.51 | 2.436 | -4.1% | +0.00 | +0.00 | -0.0082% |
| ADAUSDT | 2.21 | 2.516 | -5.0% | -117.81 | -113.60 | +0.0072% |
| AVAXUSDT | -0.88 | 1.558 | -5.1% | +0.00 | +0.00 | -0.0167% |
| LINKUSDT | 0.82 | 1.898 | -4.5% | +0.00 | +0.00 | +0.0055% |
| LTCUSDT | 0.14 | 2.029 | -2.7% | +0.00 | +0.00 | -0.0072% |
| TRXUSDT | 1.51 | 1.364 | -0.1% | -215.40 | +0.00 | -0.0284% |
| DOTUSDT | 1.67 | 1.823 | -5.2% | -120.13 | -115.87 | -0.0263% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
