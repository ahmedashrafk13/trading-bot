# v9 brief - 2026-11-24 18:15 UTC (signal from the 2026-11-24 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+13.79 (+6.9% of budget); from peak $-4.06

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.05 | 2.555 | -2.5% | +0.00 | +0.00 | +0.0054% |
| ETHUSDT | -1.29 | 2.153 | -3.3% | +0.00 | +0.00 | +0.0091% |
| SOLUSDT | 1.65 | 3.864 | -5.6% | -106.08 | -104.53 | -0.0002% |
| BNBUSDT | -0.9 | 2.433 | -2.1% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.7 | 2.979 | -3.5% | +0.00 | +0.00 | +0.0041% |
| DOGEUSDT | -0.76 | 2.399 | -3.4% | +0.00 | +0.00 | +0.0041% |
| ADAUSDT | 2.72 | 2.578 | -3.5% | -96.84 | -98.63 | +0.0100% |
| AVAXUSDT | -0.54 | 1.624 | -4.3% | +0.00 | +0.00 | -0.0006% |
| LINKUSDT | 1.08 | 1.925 | -2.1% | +0.00 | +0.00 | -0.0036% |
| LTCUSDT | -0.16 | 1.977 | -2.7% | +0.00 | +0.00 | -0.0003% |
| TRXUSDT | 1.6 | 1.371 | -1.1% | -178.33 | -178.95 | -0.0020% |
| DOTUSDT | 2.27 | 1.887 | -4.3% | -98.75 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
