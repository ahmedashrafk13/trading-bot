# v9 brief - 2026-09-24 16:08 UTC (signal from the 2026-09-24 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $+0.00 (+0.0% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.32 | 1.256 | -2.5% | +0.00 | +0.00 | +0.0064% |
| ETHUSDT | 1.06 | 2.848 | -2.9% | +0.00 | +0.00 | +0.0070% |
| SOLUSDT | -0.28 | 1.879 | -3.2% | +0.00 | +0.00 | -0.0073% |
| BNBUSDT | -0.92 | 2.162 | -1.6% | +0.00 | +0.00 | -0.0093% |
| XRPUSDT | 0.6 | 2.464 | -6.6% | +0.00 | +0.00 | -0.0126% |
| DOGEUSDT | 0.95 | 2.663 | -6.7% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.32 | 2.256 | -6.1% | +0.00 | +0.00 | -0.0047% |
| AVAXUSDT | 0.61 | 2.318 | -8.9% | +0.00 | +0.00 | -0.0120% |
| LINKUSDT | -0.34 | 1.524 | -4.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.25 | 2.276 | +6.2% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.13 | 1.221 | -1.0% | +0.00 | +0.00 | -0.0200% |
| DOTUSDT | -1.43 | 1.729 | -3.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
