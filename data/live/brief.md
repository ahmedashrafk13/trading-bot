# v9 brief - 2026-10-12 12:12 UTC (signal from the 2026-10-12 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.46 (-1.2% of budget); from peak $-2.85

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.37 | 1.371 | +0.3% | +0.00 | +0.00 | +0.0056% |
| ETHUSDT | -0.39 | 2.601 | +1.6% | +0.00 | +0.00 | +0.0078% |
| SOLUSDT | 1.33 | 2.293 | +1.3% | +0.00 | +0.00 | -0.0018% |
| BNBUSDT | -1.03 | 2.104 | +0.0% | +0.00 | +0.00 | +0.0028% |
| XRPUSDT | -0.59 | 2.321 | +0.3% | +0.00 | +0.00 | +0.0011% |
| DOGEUSDT | -1.25 | 2.243 | +2.1% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.65 | 1.999 | +1.4% | +0.00 | +0.00 | +0.0073% |
| AVAXUSDT | -0.94 | 1.887 | +5.9% | +0.00 | +0.00 | -0.0057% |
| LINKUSDT | -0.04 | 1.645 | +3.3% | +0.00 | +0.00 | +0.0049% |
| LTCUSDT | -2.1 | 1.751 | +1.7% | +145.23 | +0.00 | +0.0082% |
| TRXUSDT | -0.66 | 1.112 | +0.3% | +0.00 | +0.00 | -0.0059% |
| DOTUSDT | 1.84 | 2.348 | +2.6% | -103.43 | -103.69 | +0.0098% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
