# v9 brief - 2026-10-05 05:19 UTC (signal from the 2026-10-05 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.28 (-3.6% of budget); from peak $-7.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.01 | 1.015 | +2.1% | +0.00 | +0.00 | +0.0055% |
| ETHUSDT | -0.51 | 2.477 | +1.5% | +0.00 | +0.00 | +0.0000% |
| SOLUSDT | -1.15 | 1.622 | +1.7% | +0.00 | +0.00 | -0.0042% |
| BNBUSDT | -0.47 | 2.166 | +1.1% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -1.19 | 2.253 | +2.3% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.62 | 2.365 | +3.4% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.12 | 2.132 | +6.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.11 | 2.309 | -0.2% | +0.00 | +0.00 | -0.0078% |
| LINKUSDT | 0.51 | 1.805 | +1.1% | +0.00 | +0.00 | +0.0015% |
| LTCUSDT | -0.88 | 2.173 | +0.6% | +0.00 | +0.00 | +0.0034% |
| TRXUSDT | -0.27 | 1.188 | +0.1% | +0.00 | +0.00 | -0.0467% |
| DOTUSDT | -1.3 | 1.697 | +1.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
