# v9 brief - 2026-10-04 18:12 UTC (signal from the 2026-10-04 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.28 (-3.6% of budget); from peak $-7.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.47 | 1.128 | +0.4% | +0.00 | +0.00 | +0.0057% |
| ETHUSDT | 0.1 | 2.642 | +0.5% | +0.00 | +0.00 | +0.0040% |
| SOLUSDT | -1.15 | 1.626 | +1.3% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.27 | 2.201 | -0.0% | +0.00 | +0.00 | +0.0042% |
| XRPUSDT | -0.48 | 2.345 | +0.5% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.97 | 2.301 | +2.4% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.59 | 1.955 | +0.8% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.12 | 2.311 | -0.7% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.37 | 1.773 | +1.8% | +0.00 | +0.00 | +0.0087% |
| LTCUSDT | -1.19 | 2.11 | +3.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.26 | 1.189 | -0.3% | +0.00 | +0.00 | -0.0474% |
| DOTUSDT | -1.06 | 1.751 | -0.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
