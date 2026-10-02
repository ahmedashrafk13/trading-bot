# v9 brief - 2026-10-02 15:47 UTC (signal from the 2026-10-02 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-9.11 (-4.6% of budget); from peak $-9.49

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.47 | 0.897 | +3.0% | +0.00 | +85.29 | +0.0100% |
| ETHUSDT | -1.32 | 2.249 | +1.5% | +0.00 | +0.00 | +0.0039% |
| SOLUSDT | -1.26 | 1.617 | +3.3% | +0.00 | +0.00 | +0.0098% |
| BNBUSDT | 0.13 | 2.273 | +1.0% | +0.00 | +0.00 | -0.0081% |
| XRPUSDT | -1.33 | 2.228 | +2.6% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.17 | 2.505 | +1.6% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.72 | 2.276 | +2.6% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.25 | 2.674 | +0.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 1.7 | 2.073 | +0.1% | -69.55 | -68.21 | +0.0100% |
| LTCUSDT | -1.08 | 2.138 | +3.8% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.63 | 1.115 | +0.7% | +0.00 | +0.00 | -0.0411% |
| DOTUSDT | -0.8 | 1.84 | +1.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
