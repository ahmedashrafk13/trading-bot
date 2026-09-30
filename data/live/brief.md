# v9 brief - 2026-09-30 18:12 UTC (signal from the 2026-09-30 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.51 (-3.8% of budget); from peak $-7.89

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.15 | 1.261 | +1.1% | +0.00 | +0.00 | +0.0011% |
| ETHUSDT | 0.46 | 2.722 | +0.3% | +0.00 | +0.00 | +0.0027% |
| SOLUSDT | -0.27 | 1.848 | +1.2% | +0.00 | +0.00 | -0.0016% |
| BNBUSDT | -0.61 | 2.148 | +2.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.25 | 2.544 | +1.2% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 1.14 | 2.676 | +1.3% | +0.00 | +0.00 | -0.0064% |
| ADAUSDT | 0.81 | 2.273 | +1.9% | +0.00 | +0.00 | -0.0095% |
| AVAXUSDT | 1.46 | 2.702 | -0.8% | +0.00 | -51.84 | -0.0250% |
| LINKUSDT | 1.71 | 2.017 | -1.2% | -64.45 | -63.30 | +0.0100% |
| LTCUSDT | -0.31 | 2.298 | -0.7% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.36 | 1.146 | +0.9% | +0.00 | +0.00 | -0.0354% |
| DOTUSDT | 0.17 | 2.065 | +6.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
