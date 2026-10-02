# v9 brief - 2026-10-02 18:12 UTC (signal from the 2026-10-02 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-8.59 (-4.3% of budget); from peak $-8.98

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.61 | 1.073 | -0.1% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | 0.59 | 2.755 | -0.6% | +0.00 | +0.00 | +0.0045% |
| SOLUSDT | -0.6 | 1.76 | +1.1% | +0.00 | +0.00 | -0.0103% |
| BNBUSDT | 0.19 | 2.284 | +0.1% | +0.00 | +0.00 | -0.0081% |
| XRPUSDT | 0.87 | 2.506 | -0.2% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.99 | 2.68 | -0.5% | +0.00 | +0.00 | -0.0001% |
| ADAUSDT | 1.28 | 2.445 | -0.0% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.95 | 2.566 | +0.9% | +0.00 | +0.00 | +0.0070% |
| LINKUSDT | 1.73 | 2.091 | -1.4% | -101.16 | -67.79 | +0.0100% |
| LTCUSDT | -0.57 | 2.25 | +2.9% | +0.00 | +0.00 | +0.0096% |
| TRXUSDT | -0.59 | 1.123 | +0.4% | +0.00 | +0.00 | -0.0212% |
| DOTUSDT | -0.77 | 1.845 | +2.3% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
