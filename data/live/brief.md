# v9 brief - 2026-11-23 14:09 UTC (signal from the 2026-11-23 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+16.80 (+8.4% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.05 | 2.077 | +0.6% | +0.00 | +0.00 | +0.0027% |
| ETHUSDT | -1.95 | 1.906 | +1.0% | +126.22 | +125.18 | +0.0001% |
| SOLUSDT | 0.15 | 3.367 | +2.7% | +0.00 | +0.00 | -0.0063% |
| BNBUSDT | -0.8 | 2.443 | +0.7% | +0.00 | +0.00 | +0.0038% |
| XRPUSDT | -0.66 | 2.686 | +1.4% | +0.00 | +0.00 | +0.0009% |
| DOGEUSDT | -2.03 | 2.207 | +0.6% | +127.06 | +133.23 | +0.0077% |
| ADAUSDT | 1.48 | 2.25 | +0.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.33 | 1.652 | +0.8% | +0.00 | +0.00 | -0.0168% |
| LINKUSDT | 0.83 | 1.879 | +1.7% | +0.00 | +0.00 | +0.0095% |
| LTCUSDT | -0.43 | 1.927 | +2.7% | +0.00 | +0.00 | +0.0061% |
| TRXUSDT | 0.41 | 1.21 | +0.6% | +0.00 | +0.00 | +0.0074% |
| DOTUSDT | 0.75 | 1.672 | +2.7% | +0.00 | +0.00 | +0.0012% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
