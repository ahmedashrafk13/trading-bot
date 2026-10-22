# v9 brief - 2026-10-22 00:21 UTC (signal from the 2026-10-22 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-8.69 (-4.3% of budget); from peak $-12.68

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.42 | 1.022 | +1.3% | +0.00 | +0.00 | +0.0041% |
| ETHUSDT | -1.74 | 2.353 | +1.0% | +204.88 | +198.11 | +0.0030% |
| SOLUSDT | 0.9 | 2.38 | +0.4% | +0.00 | +0.00 | +0.0025% |
| BNBUSDT | 0.7 | 2.411 | +0.6% | +0.00 | +0.00 | -0.0099% |
| XRPUSDT | -0.61 | 2.389 | +2.2% | +0.00 | +0.00 | +0.0048% |
| DOGEUSDT | 0.63 | 2.598 | +0.1% | +0.00 | +0.00 | +0.0012% |
| ADAUSDT | -1.04 | 1.874 | +0.5% | +0.00 | +0.00 | -0.0130% |
| AVAXUSDT | -1.52 | 1.484 | -1.0% | +101.10 | +100.80 | +0.0038% |
| LINKUSDT | -0.43 | 1.614 | +1.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.88 | 1.735 | -0.1% | +132.46 | +129.34 | +0.0004% |
| TRXUSDT | -0.75 | 1.1 | -0.2% | +0.00 | +0.00 | -0.0232% |
| DOTUSDT | 0.65 | 2.059 | -0.7% | +0.00 | +0.00 | -0.0212% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
