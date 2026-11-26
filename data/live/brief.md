# v9 brief - 2026-11-26 18:12 UTC (signal from the 2026-11-26 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+12.37 (+6.2% of budget); from peak $-14.50

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.51 | 2.366 | +1.6% | +0.00 | +0.00 | +0.0088% |
| ETHUSDT | -1.34 | 2.06 | +0.9% | +0.00 | +0.00 | +0.0074% |
| SOLUSDT | -0.32 | 3.321 | +2.4% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.79 | 2.445 | +0.7% | +0.00 | +0.00 | +0.0060% |
| XRPUSDT | 0.08 | 2.831 | +2.9% | +0.00 | +0.00 | +0.0082% |
| DOGEUSDT | -0.19 | 2.482 | +3.6% | +0.00 | +0.00 | +0.0081% |
| ADAUSDT | 1.35 | 2.337 | +4.0% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.21 | 1.494 | +1.7% | +0.00 | +0.00 | -0.0091% |
| LINKUSDT | 0.97 | 1.926 | +3.9% | +0.00 | +0.00 | -0.0065% |
| LTCUSDT | 0.54 | 2.103 | +3.7% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -1.23 | 1.032 | -0.5% | +0.00 | +0.00 | -0.0686% |
| DOTUSDT | 1.59 | 1.833 | +2.2% | -117.93 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
