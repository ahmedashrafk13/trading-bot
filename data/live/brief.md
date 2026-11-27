# v9 brief - 2026-11-27 09:22 UTC (signal from the 2026-11-27 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+10.44 (+5.2% of budget); from peak $-16.43

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.39 | 2.434 | +1.6% | +0.00 | +0.00 | -0.0013% |
| ETHUSDT | -1.19 | 2.111 | +2.8% | +0.00 | +0.00 | +0.0068% |
| SOLUSDT | 0.6 | 3.587 | +3.1% | +0.00 | +0.00 | +0.0082% |
| BNBUSDT | -0.74 | 2.45 | +1.6% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.78 | 2.982 | +1.2% | +0.00 | +0.00 | -0.0113% |
| DOGEUSDT | 0.35 | 2.57 | +2.5% | +0.00 | +0.00 | -0.0105% |
| ADAUSDT | 1.97 | 2.511 | +2.4% | -114.33 | +0.00 | +0.0019% |
| AVAXUSDT | -1.13 | 1.508 | +1.4% | +0.00 | +0.00 | -0.0056% |
| LINKUSDT | 1.69 | 2.018 | +5.0% | -108.81 | +0.00 | -0.0101% |
| LTCUSDT | 1.57 | 2.307 | +2.9% | -124.71 | +0.00 | +0.0100% |
| TRXUSDT | -0.78 | 1.077 | +0.6% | +0.00 | +0.00 | -0.0089% |
| DOTUSDT | 1.36 | 1.807 | +3.9% | +0.00 | -119.66 | -0.0102% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
