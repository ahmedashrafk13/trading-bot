# v9 brief - 2026-10-16 18:14 UTC (signal from the 2026-10-16 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+0.06 (+0.0% of budget); from peak $-3.93

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.55 | 1.718 | -1.5% | -87.45 | +0.00 | +0.0016% |
| ETHUSDT | 0.17 | 2.757 | -1.4% | +0.00 | +0.00 | -0.0046% |
| SOLUSDT | 1.55 | 2.447 | -2.1% | -50.84 | +0.00 | -0.0079% |
| BNBUSDT | 1.57 | 2.473 | -1.7% | -81.88 | +0.00 | +0.0067% |
| XRPUSDT | 2.24 | 2.879 | -3.1% | -49.46 | +0.00 | -0.0059% |
| DOGEUSDT | 0.5 | 2.551 | -1.6% | +0.00 | +0.00 | -0.0058% |
| ADAUSDT | -1.18 | 1.871 | -3.5% | +0.00 | +0.00 | +0.0013% |
| AVAXUSDT | -1.51 | 1.674 | +0.3% | +28.61 | +50.20 | -0.0201% |
| LINKUSDT | -0.55 | 1.574 | -1.8% | +0.00 | +0.00 | -0.0009% |
| LTCUSDT | -1.0 | 1.963 | -1.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 2.15 | 1.395 | +0.9% | -181.75 | -212.28 | -0.0095% |
| DOTUSDT | -0.28 | 1.831 | +3.4% | +0.00 | +0.00 | -0.0169% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
