# v9 brief - 2026-10-29 18:12 UTC (signal from the 2026-10-29 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-30.03 (-15.0% of budget); from peak $-34.02

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.46 | 1.735 | +0.0% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | 0.16 | 2.981 | -0.1% | +0.00 | -163.61 | +0.0091% |
| SOLUSDT | 1.17 | 2.936 | -0.6% | +0.00 | -151.41 | +0.0100% |
| BNBUSDT | 0.97 | 2.579 | -0.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.3 | 3.04 | -1.8% | +0.00 | +0.00 | +0.0058% |
| DOGEUSDT | 0.63 | 2.636 | +0.5% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.69 | 1.843 | +0.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.7 | 1.553 | +0.2% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.16 | 1.639 | +1.7% | +0.00 | +0.00 | +0.0072% |
| LTCUSDT | 2.3 | 2.506 | -1.4% | -161.45 | -144.47 | +0.0100% |
| TRXUSDT | 0.43 | 1.25 | +0.3% | +0.00 | +0.00 | +0.0024% |
| DOTUSDT | -1.53 | 1.48 | +0.0% | +95.18 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
