# v9 brief - 2026-09-27 07:25 UTC (signal from the 2026-09-27 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.46 (-0.7% of budget); from peak $-1.46

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.3 | 1.276 | +0.7% | +0.00 | +0.00 | +0.0023% |
| ETHUSDT | 0.39 | 2.679 | +0.7% | +0.00 | +0.00 | +0.0099% |
| SOLUSDT | -1.72 | 1.549 | +0.5% | +91.18 | +85.09 | +0.0100% |
| BNBUSDT | -1.35 | 2.049 | +0.0% | +0.00 | +0.00 | -0.0058% |
| XRPUSDT | -0.38 | 2.339 | -2.0% | +0.00 | +0.00 | +0.0035% |
| DOGEUSDT | 0.19 | 2.492 | -1.2% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.16 | 2.32 | -0.7% | +0.00 | -70.34 | +0.0100% |
| AVAXUSDT | 0.34 | 2.25 | +2.2% | +0.00 | +0.00 | +0.0052% |
| LINKUSDT | 1.42 | 1.842 | +1.1% | +0.00 | +0.00 | +0.0071% |
| LTCUSDT | 0.21 | 2.381 | -0.1% | +0.00 | +0.00 | +0.0056% |
| TRXUSDT | -1.02 | 1.056 | -1.2% | +0.00 | +0.00 | -0.0532% |
| DOTUSDT | -0.35 | 1.933 | +0.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
