# v9 brief - 2026-10-28 18:13 UTC (signal from the 2026-10-28 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-30.02 (-15.0% of budget); from peak $-34.01

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.19 | 2.035 | +0.4% | +0.00 | +0.00 | +0.0085% |
| ETHUSDT | 1.11 | 3.281 | -0.1% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.53 | 3.075 | +0.9% | -169.76 | +0.00 | +0.0091% |
| BNBUSDT | 0.36 | 2.442 | -0.1% | +0.00 | +0.00 | -0.0024% |
| XRPUSDT | 0.7 | 2.83 | -0.2% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.38 | 2.589 | +1.3% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.4 | 1.915 | -1.2% | +0.00 | +0.00 | +0.0059% |
| AVAXUSDT | -0.67 | 1.582 | +0.1% | +0.00 | +0.00 | +0.0064% |
| LINKUSDT | 0.28 | 1.71 | +0.7% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -2.21 | 1.64 | +3.3% | +161.36 | +0.00 | +0.0011% |
| TRXUSDT | 0.94 | 1.312 | +0.5% | +0.00 | +0.00 | -0.0140% |
| DOTUSDT | -1.26 | 1.556 | -0.1% | +0.00 | +0.00 | -0.0109% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
