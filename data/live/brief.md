# v9 brief - 2026-10-02 07:42 UTC (signal from the 2026-10-02 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-8.87 (-4.4% of budget); from peak $-9.26

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.51 | 0.896 | +2.0% | +154.72 | +0.00 | +0.0100% |
| ETHUSDT | -1.13 | 2.301 | +0.1% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | -1.41 | 1.59 | +2.1% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.07 | 2.237 | +0.7% | +0.00 | +0.00 | +0.0000% |
| XRPUSDT | -0.09 | 2.382 | +0.6% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.75 | 2.623 | -0.0% | +0.00 | -69.90 | +0.0100% |
| ADAUSDT | 0.75 | 2.28 | -0.1% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.26 | 2.67 | -0.6% | +0.00 | +0.00 | +0.0084% |
| LINKUSDT | 1.88 | 2.113 | -0.3% | -69.55 | +0.00 | +0.0100% |
| LTCUSDT | -1.11 | 2.134 | +4.0% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.53 | 1.13 | -1.0% | +0.00 | +0.00 | -0.0448% |
| DOTUSDT | -0.9 | 1.823 | -2.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
