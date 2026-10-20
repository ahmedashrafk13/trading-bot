# v9 brief - 2026-10-20 06:18 UTC (signal from the 2026-10-20 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.32 (-1.7% of budget); from peak $-7.31

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.18 | 1.671 | -1.3% | +0.00 | +0.00 | +0.0060% |
| ETHUSDT | 0.65 | 2.945 | -1.4% | +0.00 | +0.00 | +0.0032% |
| SOLUSDT | 1.05 | 2.384 | -1.1% | +0.00 | +0.00 | -0.0023% |
| BNBUSDT | 2.08 | 2.65 | +0.2% | -232.76 | -218.54 | -0.0080% |
| XRPUSDT | 0.49 | 2.593 | -0.9% | +0.00 | +0.00 | +0.0069% |
| DOGEUSDT | 0.25 | 2.536 | -0.6% | +0.00 | +0.00 | -0.0016% |
| ADAUSDT | -1.18 | 1.868 | -1.9% | +0.00 | +0.00 | -0.0053% |
| AVAXUSDT | -1.9 | 1.459 | -2.2% | +86.47 | +80.15 | -0.0127% |
| LINKUSDT | -0.86 | 1.536 | -1.6% | +0.00 | +0.00 | +0.0008% |
| LTCUSDT | -1.17 | 1.908 | -0.9% | +0.00 | +112.69 | -0.0007% |
| TRXUSDT | 0.58 | 1.278 | +0.1% | +0.00 | +0.00 | -0.0011% |
| DOTUSDT | 0.54 | 2.006 | +1.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
