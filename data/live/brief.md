# v9 brief - 2026-10-14 00:25 UTC (signal from the 2026-10-14 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+3.17 (+1.6% of budget); from peak $-0.82

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.14 | 1.29 | +1.6% | +0.00 | +0.00 | +0.0000% |
| ETHUSDT | -0.18 | 2.659 | +2.1% | +0.00 | +0.00 | +0.0063% |
| SOLUSDT | 1.5 | 2.356 | +1.0% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | 0.47 | 2.28 | +1.2% | +0.00 | +0.00 | -0.0085% |
| XRPUSDT | 1.71 | 2.682 | +1.8% | -138.22 | +0.00 | -0.0148% |
| DOGEUSDT | -0.4 | 2.383 | +2.6% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -1.55 | 1.793 | +1.2% | +112.37 | +112.53 | +0.0012% |
| AVAXUSDT | -1.73 | 1.69 | +0.8% | +89.22 | +89.31 | +0.0023% |
| LINKUSDT | -0.42 | 1.576 | +2.0% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.1 | 1.944 | +0.2% | +0.00 | +0.00 | +0.0060% |
| TRXUSDT | -0.72 | 1.099 | -0.5% | +0.00 | +0.00 | -0.0291% |
| DOTUSDT | 1.4 | 2.255 | -0.8% | +0.00 | -95.88 | -0.0184% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
