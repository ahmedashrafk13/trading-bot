# v9 brief - 2026-11-23 18:14 UTC (signal from the 2026-11-23 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+12.10 (+6.1% of budget); from peak $-4.69

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.09 | 2.61 | +1.4% | +0.00 | +0.00 | +0.0005% |
| ETHUSDT | -1.34 | 2.165 | +1.7% | +0.00 | +122.03 | -0.0077% |
| SOLUSDT | 1.19 | 3.675 | +4.7% | +0.00 | +0.00 | +0.0012% |
| BNBUSDT | 0.09 | 2.587 | +0.9% | +0.00 | +0.00 | +0.0052% |
| XRPUSDT | 1.08 | 3.063 | +3.2% | +0.00 | +0.00 | -0.0053% |
| DOGEUSDT | -0.94 | 2.376 | +3.9% | +0.00 | +125.29 | +0.0100% |
| ADAUSDT | 1.71 | 2.299 | +4.3% | -111.19 | +0.00 | +0.0068% |
| AVAXUSDT | -0.16 | 1.69 | +3.2% | +0.00 | +0.00 | -0.0033% |
| LINKUSDT | 1.44 | 1.96 | +3.1% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.9 | 1.845 | +5.0% | +0.00 | +0.00 | +0.0000% |
| TRXUSDT | 0.7 | 1.246 | +2.1% | +0.00 | +0.00 | +0.0100% |
| DOTUSDT | 1.03 | 1.708 | +4.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
