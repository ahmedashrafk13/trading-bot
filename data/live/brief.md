# v9 brief - 2026-10-20 18:13 UTC (signal from the 2026-10-20 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-5.39 (-2.7% of budget); from peak $-9.38

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.8 | 1.557 | +1.1% | +0.00 | -165.30 | +0.0099% |
| ETHUSDT | -0.03 | 2.758 | +2.2% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.4 | 2.554 | +2.6% | +0.00 | +0.00 | -0.0014% |
| BNBUSDT | 1.78 | 2.609 | +1.6% | -255.98 | -192.00 | +0.0087% |
| XRPUSDT | 1.03 | 2.72 | +2.2% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 1.0 | 2.64 | +2.9% | +0.00 | +0.00 | -0.0015% |
| ADAUSDT | -1.21 | 1.855 | +2.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.88 | 1.437 | +1.5% | +101.10 | +72.55 | +0.0100% |
| LINKUSDT | -0.7 | 1.566 | +2.8% | +0.00 | +0.00 | +0.0009% |
| LTCUSDT | -0.25 | 2.098 | +1.1% | +0.00 | +0.00 | +0.0000% |
| TRXUSDT | 0.44 | 1.26 | +0.0% | +0.00 | +0.00 | -0.0017% |
| DOTUSDT | 1.54 | 2.272 | +2.7% | -97.48 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
