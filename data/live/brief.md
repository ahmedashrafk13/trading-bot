# v9 brief - 2026-09-25 07:15 UTC (signal from the 2026-09-25 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-0.60 (-0.3% of budget); from peak $-0.60

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.21 | 1.234 | +0.3% | +0.00 | +0.00 | -0.0012% |
| ETHUSDT | 0.48 | 2.685 | -0.1% | +0.00 | +0.00 | +0.0013% |
| SOLUSDT | -0.68 | 1.786 | +1.4% | +0.00 | +0.00 | -0.0002% |
| BNBUSDT | -1.2 | 2.104 | +0.3% | +0.00 | +0.00 | +0.0024% |
| XRPUSDT | 0.57 | 2.461 | +1.6% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 1.05 | 2.68 | +1.1% | +0.00 | +0.00 | -0.0050% |
| ADAUSDT | 2.15 | 2.503 | +3.1% | -67.24 | -67.62 | +0.0051% |
| AVAXUSDT | -0.04 | 2.128 | -0.3% | +0.00 | +0.00 | -0.0069% |
| LINKUSDT | 0.81 | 1.709 | +8.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.22 | 2.381 | +6.3% | +0.00 | +0.00 | +0.0010% |
| TRXUSDT | -0.52 | 1.148 | -1.3% | +0.00 | +0.00 | -0.0417% |
| DOTUSDT | -1.7 | 1.659 | +1.8% | +49.27 | +48.96 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
