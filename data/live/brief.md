# v9 brief - 2026-10-02 00:21 UTC (signal from the 2026-10-02 00:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.74 (-3.9% of budget); from peak $-8.12

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.81 | 1.039 | +1.5% | +0.00 | +0.00 | +0.0015% |
| ETHUSDT | -0.07 | 2.579 | +0.8% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.11 | 1.939 | +0.2% | +0.00 | +0.00 | -0.0006% |
| BNBUSDT | -0.16 | 2.222 | +0.3% | +0.00 | +0.00 | -0.0083% |
| XRPUSDT | 0.91 | 2.513 | +0.3% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 1.73 | 2.84 | -0.2% | -68.89 | +0.00 | +0.0083% |
| ADAUSDT | 1.24 | 2.418 | -0.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.02 | 2.571 | +0.5% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.48 | 1.998 | +0.1% | +0.00 | -68.62 | +0.0100% |
| LTCUSDT | -0.88 | 2.183 | +1.3% | +0.00 | +0.00 | -0.0107% |
| TRXUSDT | -0.6 | 1.116 | -0.8% | +0.00 | +0.00 | -0.0853% |
| DOTUSDT | -0.4 | 1.937 | -3.9% | +0.00 | +0.00 | -0.0038% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
