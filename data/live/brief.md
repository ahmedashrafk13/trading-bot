# v9 brief - 2026-10-21 15:10 UTC (signal from the 2026-10-21 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-2.78 (-1.4% of budget); from peak $-6.77

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.14 | 1.302 | +2.5% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -0.79 | 2.576 | +3.6% | +0.00 | +0.00 | +0.0092% |
| SOLUSDT | 1.18 | 2.487 | +2.7% | +0.00 | +0.00 | -0.0046% |
| BNBUSDT | 0.73 | 2.412 | +2.5% | +0.00 | +0.00 | -0.0066% |
| XRPUSDT | -0.05 | 2.494 | +4.5% | +0.00 | +0.00 | +0.0090% |
| DOGEUSDT | 0.48 | 2.578 | +3.8% | +0.00 | +0.00 | +0.0036% |
| ADAUSDT | -1.11 | 1.865 | +4.4% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.71 | 1.449 | +3.1% | +101.10 | +102.76 | +0.0100% |
| LINKUSDT | -0.64 | 1.579 | +3.7% | +0.00 | +0.00 | -0.0027% |
| LTCUSDT | -2.01 | 1.727 | +5.3% | +132.46 | +130.16 | +0.0076% |
| TRXUSDT | -0.71 | 1.107 | -0.5% | +0.00 | +0.00 | -0.0098% |
| DOTUSDT | 1.03 | 2.153 | +1.5% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
