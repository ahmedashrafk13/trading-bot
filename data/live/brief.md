# v9 brief - 2026-09-29 06:13 UTC (signal from the 2026-09-29 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-7.80 (-3.9% of budget); from peak $-8.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.76 | 1.417 | +0.3% | +0.00 | +0.00 | +0.0000% |
| ETHUSDT | 0.61 | 2.757 | +0.9% | +0.00 | +0.00 | +0.0017% |
| SOLUSDT | -0.32 | 1.841 | -0.7% | +0.00 | +0.00 | +0.0031% |
| BNBUSDT | -0.04 | 2.265 | -0.8% | +0.00 | +0.00 | -0.0022% |
| XRPUSDT | 0.9 | 2.493 | +0.7% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.47 | 2.541 | +0.6% | +0.00 | +0.00 | +0.0041% |
| ADAUSDT | 0.76 | 2.239 | -0.6% | +0.00 | +0.00 | +0.0073% |
| AVAXUSDT | 0.7 | 2.381 | -0.1% | +0.00 | +0.00 | +0.0002% |
| LINKUSDT | 1.74 | 1.964 | +7.2% | -67.89 | -65.76 | +0.0039% |
| LTCUSDT | 0.29 | 2.427 | -4.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.6 | 1.11 | +0.3% | +0.00 | +0.00 | -0.0274% |
| DOTUSDT | -0.89 | 1.815 | -5.8% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
