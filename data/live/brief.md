# v9 brief - 2026-10-07 00:29 UTC (signal from the 2026-10-07 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.30 (-3.6% of budget); from peak $-7.68

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.54 | 1.114 | -0.2% | +0.00 | +0.00 | -0.0003% |
| ETHUSDT | 0.25 | 2.682 | -0.4% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | -1.02 | 1.63 | -0.1% | +0.00 | +0.00 | -0.0024% |
| BNBUSDT | -0.42 | 2.199 | -0.9% | +0.00 | +0.00 | -0.0306% |
| XRPUSDT | -0.61 | 2.31 | -0.7% | +0.00 | +0.00 | -0.0120% |
| DOGEUSDT | 0.57 | 2.573 | -1.8% | +0.00 | +0.00 | -0.0012% |
| ADAUSDT | 1.52 | 2.575 | -1.1% | -124.38 | -121.35 | +0.0100% |
| AVAXUSDT | 0.31 | 2.361 | +4.3% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.38 | 1.612 | +0.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -2.06 | 1.883 | -1.6% | +136.93 | +130.95 | -0.0011% |
| TRXUSDT | -0.45 | 1.167 | -0.2% | +0.00 | +0.00 | -0.0480% |
| DOTUSDT | -0.19 | 1.918 | -2.5% | +0.00 | +0.00 | +0.0007% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
