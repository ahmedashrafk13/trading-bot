# v9 brief - 2026-11-12 08:30 UTC (signal from the 2026-11-12 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-32.42 (-16.2% of budget); from peak $-36.41

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.99 | 2.738 | -0.5% | +0.00 | +0.00 | +0.0028% |
| ETHUSDT | 0.4 | 3.232 | -1.1% | +0.00 | +0.00 | +0.0087% |
| SOLUSDT | 1.08 | 3.433 | -0.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | 0.29 | 2.647 | -1.2% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.2 | 3.088 | -2.0% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.52 | 2.525 | -2.1% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 2.55 | 2.063 | -1.7% | -124.79 | +0.00 | +0.0100% |
| AVAXUSDT | 2.54 | 2.184 | +0.8% | -115.12 | -113.72 | +0.0100% |
| LINKUSDT | 0.98 | 1.874 | -3.6% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.12 | 1.96 | -3.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.66 | 1.123 | -0.1% | +0.00 | +0.00 | -0.0031% |
| DOTUSDT | -0.38 | 1.577 | -0.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
