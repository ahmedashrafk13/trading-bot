# v9 brief - 2026-11-18 16:21 UTC (signal from the 2026-11-18 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.27 (-1.1% of budget); from peak $-6.26

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.26 | 2.22 | -1.2% | +0.00 | +0.00 | -0.0041% |
| ETHUSDT | -0.84 | 2.609 | -1.2% | +0.00 | +0.00 | -0.0084% |
| SOLUSDT | 0.29 | 3.284 | +1.3% | +0.00 | +0.00 | -0.0059% |
| BNBUSDT | -0.56 | 2.49 | -0.8% | +0.00 | +0.00 | -0.0021% |
| XRPUSDT | 0.58 | 2.948 | +1.7% | +0.00 | +0.00 | -0.0049% |
| DOGEUSDT | -1.21 | 2.408 | -0.0% | +0.00 | +145.87 | -0.0205% |
| ADAUSDT | 2.47 | 2.252 | -1.1% | -138.97 | -126.76 | -0.0172% |
| AVAXUSDT | -0.23 | 1.637 | -1.7% | +0.00 | +0.00 | -0.0176% |
| LINKUSDT | 0.47 | 1.815 | -1.1% | +0.00 | +0.00 | -0.0063% |
| LTCUSDT | 0.62 | 2.114 | -2.0% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 0.32 | 1.186 | +1.4% | +0.00 | +0.00 | -0.0282% |
| DOTUSDT | 1.08 | 1.825 | -1.5% | +0.00 | +0.00 | -0.0071% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
