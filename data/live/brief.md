# v9 brief - 2026-10-09 18:12 UTC (signal from the 2026-10-09 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.79 (-1.4% of budget); from peak $-3.18

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.64 | 1.462 | +2.4% | +0.00 | +0.00 | +0.0039% |
| ETHUSDT | 0.73 | 2.934 | +2.9% | +0.00 | +0.00 | +0.0008% |
| SOLUSDT | 1.66 | 2.357 | +3.4% | -163.23 | -153.83 | +0.0061% |
| BNBUSDT | -0.37 | 2.212 | +2.6% | +0.00 | +0.00 | -0.0017% |
| XRPUSDT | 0.63 | 2.506 | +4.8% | +0.00 | +0.00 | -0.0176% |
| DOGEUSDT | -0.62 | 2.351 | +4.2% | +0.00 | +0.00 | +0.0010% |
| ADAUSDT | -0.63 | 1.981 | +5.9% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.41 | 1.829 | +4.0% | +0.00 | +0.00 | +0.0020% |
| LINKUSDT | -0.67 | 1.537 | +5.4% | +0.00 | +0.00 | +0.0025% |
| LTCUSDT | -1.18 | 2.007 | +3.6% | +0.00 | +0.00 | +0.0013% |
| TRXUSDT | -0.69 | 1.13 | -0.1% | +0.00 | +0.00 | -0.0307% |
| DOTUSDT | -0.61 | 1.772 | +18.5% | +0.00 | +101.37 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
