# v9 brief - 2026-11-23 05:22 UTC (signal from the 2026-11-23 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+7.51 (+3.8% of budget); from peak $-6.59

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.0 | 2.101 | +1.7% | +0.00 | +0.00 | +0.0041% |
| ETHUSDT | -2.18 | 1.86 | +2.3% | +126.22 | +121.10 | -0.0038% |
| SOLUSDT | 0.53 | 3.468 | +0.6% | +0.00 | +0.00 | -0.0051% |
| BNBUSDT | -1.21 | 2.38 | +2.0% | +0.00 | +0.00 | +0.0040% |
| XRPUSDT | -0.61 | 2.701 | -0.3% | +0.00 | +0.00 | -0.0010% |
| DOGEUSDT | -1.65 | 2.279 | +0.1% | +127.06 | +127.30 | +0.0100% |
| ADAUSDT | 1.76 | 2.296 | +0.2% | -111.67 | -111.00 | -0.0144% |
| AVAXUSDT | -0.29 | 1.654 | +1.6% | +0.00 | +0.00 | -0.0032% |
| LINKUSDT | 0.0 | 1.776 | +2.4% | +0.00 | +0.00 | -0.0002% |
| LTCUSDT | -0.45 | 1.919 | +1.0% | +0.00 | +0.00 | +0.0010% |
| TRXUSDT | 0.48 | 1.217 | +0.1% | +0.00 | +0.00 | -0.0026% |
| DOTUSDT | 0.86 | 1.686 | +1.1% | +0.00 | +0.00 | +0.0042% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
