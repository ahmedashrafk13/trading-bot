# v9 brief - 2026-10-12 00:12 UTC (signal from the 2026-10-12 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-0.12 (-0.1% of budget); from peak $-0.50

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.49 | 1.413 | +0.9% | +0.00 | +0.00 | +0.0078% |
| ETHUSDT | 0.47 | 2.873 | +1.2% | +0.00 | +0.00 | +0.0046% |
| SOLUSDT | 1.57 | 2.377 | +1.1% | -168.31 | +0.00 | +0.0100% |
| BNBUSDT | -0.14 | 2.223 | +0.5% | +0.00 | +0.00 | -0.0124% |
| XRPUSDT | 0.01 | 2.409 | +0.6% | +0.00 | +0.00 | -0.0002% |
| DOGEUSDT | -0.33 | 2.396 | +1.2% | +0.00 | +0.00 | -0.0007% |
| ADAUSDT | -0.54 | 2.022 | +1.2% | +0.00 | +0.00 | +0.0056% |
| AVAXUSDT | -1.94 | 1.626 | +5.9% | +93.76 | +94.42 | +0.0100% |
| LINKUSDT | -0.05 | 1.644 | +2.6% | +0.00 | +0.00 | +0.0091% |
| LTCUSDT | -1.38 | 1.914 | +1.0% | +0.00 | +142.21 | +0.0055% |
| TRXUSDT | -0.76 | 1.103 | -0.2% | +0.00 | +0.00 | -0.0262% |
| DOTUSDT | 2.08 | 2.411 | -0.3% | -103.43 | -102.81 | +0.0034% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
