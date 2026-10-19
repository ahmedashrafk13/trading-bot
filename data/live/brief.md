# v9 brief - 2026-10-19 15:42 UTC (signal from the 2026-10-19 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.19 (-0.6% of budget); from peak $-5.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.59 | 1.461 | +0.3% | +0.00 | +0.00 | +0.0056% |
| ETHUSDT | -0.41 | 2.618 | +0.1% | +0.00 | +0.00 | +0.0029% |
| SOLUSDT | 0.85 | 2.279 | +0.7% | +0.00 | +0.00 | -0.0023% |
| BNBUSDT | 1.78 | 2.569 | +0.3% | -224.15 | -116.13 | +0.0100% |
| XRPUSDT | 1.37 | 2.786 | +0.4% | +0.00 | -72.03 | -0.0020% |
| DOGEUSDT | -0.34 | 2.447 | -0.4% | +0.00 | +0.00 | -0.0003% |
| ADAUSDT | -1.25 | 1.863 | -0.9% | +0.00 | +0.00 | -0.0100% |
| AVAXUSDT | -1.7 | 1.542 | -1.3% | +81.09 | +39.36 | +0.0031% |
| LINKUSDT | -1.02 | 1.508 | -0.0% | +0.00 | +0.00 | +0.0022% |
| LTCUSDT | -1.41 | 1.875 | +0.6% | +0.00 | +0.00 | +0.0057% |
| TRXUSDT | 0.59 | 1.275 | -0.5% | +0.00 | -251.20 | +0.0062% |
| DOTUSDT | -0.92 | 1.681 | -0.6% | +0.00 | +0.00 | +0.0069% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
