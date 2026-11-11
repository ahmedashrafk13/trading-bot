# v9 brief - 2026-11-11 18:12 UTC (signal from the 2026-11-11 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-32.55 (-16.3% of budget); from peak $-36.54

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.92 | 2.663 | +1.7% | +0.00 | +0.00 | +0.0059% |
| ETHUSDT | 0.31 | 3.181 | +3.1% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 0.88 | 3.321 | +3.6% | +0.00 | +0.00 | +0.0038% |
| BNBUSDT | -0.12 | 2.568 | +2.0% | +0.00 | +0.00 | +0.0082% |
| XRPUSDT | 0.85 | 2.992 | +1.5% | +0.00 | +0.00 | -0.0019% |
| DOGEUSDT | -0.85 | 2.476 | +3.1% | +0.00 | +0.00 | -0.0044% |
| ADAUSDT | 0.4 | 1.89 | +4.0% | +0.00 | +0.00 | +0.0000% |
| AVAXUSDT | 2.93 | 2.237 | +4.8% | -110.96 | -113.86 | -0.0145% |
| LINKUSDT | 0.53 | 1.794 | +2.7% | +0.00 | +0.00 | +0.0023% |
| LTCUSDT | -0.33 | 1.921 | +2.5% | +0.00 | +0.00 | +0.0054% |
| TRXUSDT | -0.69 | 1.119 | -0.5% | +0.00 | +0.00 | -0.0062% |
| DOTUSDT | -0.75 | 1.501 | +2.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
