# v9 brief - 2026-11-25 18:12 UTC (signal from the 2026-11-25 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+15.05 (+7.5% of budget); from peak $-11.83

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.6 | 2.917 | -0.8% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -0.97 | 2.273 | -0.4% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.61 | 3.878 | -0.2% | -124.49 | +0.00 | +0.0100% |
| BNBUSDT | -0.44 | 2.501 | -0.3% | +0.00 | +0.00 | +0.0036% |
| XRPUSDT | 0.46 | 2.918 | +0.1% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.4 | 2.454 | -0.9% | +0.00 | +0.00 | +0.0090% |
| ADAUSDT | 1.08 | 2.26 | -1.4% | +0.00 | -118.37 | +0.0100% |
| AVAXUSDT | -0.59 | 1.614 | -1.2% | +0.00 | +0.00 | +0.0070% |
| LINKUSDT | 1.01 | 1.922 | -0.3% | +0.00 | +0.00 | +0.0031% |
| LTCUSDT | 0.54 | 2.102 | +2.1% | +0.00 | +0.00 | -0.0090% |
| TRXUSDT | 1.06 | 1.299 | -1.2% | +0.00 | -216.36 | -0.0434% |
| DOTUSDT | 1.38 | 1.787 | -0.4% | +0.00 | -121.71 | +0.0012% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
