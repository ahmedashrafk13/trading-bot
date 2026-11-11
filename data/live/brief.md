# v9 brief - 2026-11-11 13:05 UTC (signal from the 2026-11-11 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-31.30 (-15.6% of budget); from peak $-35.29

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.0 | 2.711 | -0.6% | +0.00 | -221.28 | +0.0080% |
| ETHUSDT | 0.39 | 3.221 | -1.8% | +0.00 | +0.00 | +0.0082% |
| SOLUSDT | 0.89 | 3.321 | -0.9% | +0.00 | -142.44 | +0.0086% |
| BNBUSDT | 0.18 | 2.618 | -1.0% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.96 | 3.016 | -1.9% | +0.00 | +0.00 | +0.0077% |
| DOGEUSDT | -0.27 | 2.558 | -1.7% | +0.00 | +0.00 | +0.0008% |
| ADAUSDT | 0.23 | 1.879 | -0.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 2.87 | 2.204 | +3.2% | -110.96 | -112.83 | -0.0019% |
| LINKUSDT | 0.8 | 1.836 | -0.6% | +0.00 | +0.00 | +0.0091% |
| LTCUSDT | 0.0 | 1.988 | -0.5% | +0.00 | +0.00 | +0.0082% |
| TRXUSDT | -0.35 | 1.162 | -0.7% | +0.00 | +0.00 | -0.0139% |
| DOTUSDT | -0.61 | 1.536 | -0.5% | +0.00 | +0.00 | +0.0042% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
