# v9 brief - 2026-09-24 18:13 UTC (signal from the 2026-09-24 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $+0.00 (+0.0% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.18 | 1.223 | -0.2% | +0.00 | +0.00 | +0.0032% |
| ETHUSDT | 0.81 | 2.778 | +0.1% | +0.00 | +0.00 | +0.0009% |
| SOLUSDT | -0.52 | 1.826 | +1.9% | +0.00 | +0.00 | -0.0163% |
| BNBUSDT | -0.96 | 2.153 | +1.6% | +0.00 | +0.00 | -0.0223% |
| XRPUSDT | 0.51 | 2.452 | +1.7% | +0.00 | +0.00 | +0.0055% |
| DOGEUSDT | 0.95 | 2.66 | +3.8% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.64 | 2.34 | +3.0% | -67.24 | +0.00 | +0.0015% |
| AVAXUSDT | 0.57 | 2.308 | -0.1% | +0.00 | +0.00 | -0.0036% |
| LINKUSDT | -0.34 | 1.523 | +4.9% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.91 | 2.122 | +17.9% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.21 | 1.206 | +0.3% | +0.00 | +0.00 | +0.0020% |
| DOTUSDT | -1.93 | 1.628 | +5.8% | +49.27 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
