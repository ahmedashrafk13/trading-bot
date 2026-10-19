# v9 brief - 2026-10-19 10:50 UTC (signal from the 2026-10-19 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-0.21 (-0.1% of budget); from peak $-4.20

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.74 | 1.504 | +1.3% | +0.00 | -82.40 | +0.0100% |
| ETHUSDT | 0.35 | 2.836 | +0.8% | +0.00 | +0.00 | +0.0069% |
| SOLUSDT | 1.16 | 2.398 | +2.1% | +0.00 | -52.46 | +0.0021% |
| BNBUSDT | 2.35 | 2.668 | +1.1% | -116.69 | -86.94 | +0.0100% |
| XRPUSDT | 1.55 | 2.824 | +1.5% | -72.20 | -52.85 | +0.0013% |
| DOGEUSDT | 0.03 | 2.497 | +0.8% | +0.00 | +0.00 | -0.0004% |
| ADAUSDT | -1.28 | 1.86 | +0.8% | +0.00 | +0.00 | -0.0118% |
| AVAXUSDT | -1.64 | 1.568 | +0.4% | +40.08 | +0.00 | -0.0058% |
| LINKUSDT | -0.98 | 1.514 | +1.7% | +0.00 | +0.00 | -0.0088% |
| LTCUSDT | -1.41 | 1.88 | +2.0% | +0.00 | +0.00 | -0.0058% |
| TRXUSDT | 1.78 | 1.453 | -0.7% | -251.02 | -179.60 | -0.0153% |
| DOTUSDT | -1.11 | 1.643 | +2.2% | +0.00 | +0.00 | +0.0032% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
