# v9 brief - 2026-11-02 18:13 UTC (signal from the 2026-11-02 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-21.00 (-10.5% of budget); from peak $-24.99

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.19 | 2.321 | -1.1% | +0.00 | +0.00 | +0.0071% |
| ETHUSDT | -1.35 | 2.541 | -0.2% | +0.00 | +158.42 | +0.0034% |
| SOLUSDT | 1.52 | 3.352 | -2.5% | -153.52 | +0.00 | +0.0094% |
| BNBUSDT | 1.14 | 2.702 | -1.6% | +0.00 | +0.00 | +0.0078% |
| XRPUSDT | -0.34 | 2.57 | -0.7% | +0.00 | +0.00 | -0.0031% |
| DOGEUSDT | 1.6 | 2.782 | -1.8% | -145.37 | +0.00 | -0.0061% |
| ADAUSDT | -0.1 | 1.914 | -2.2% | +0.00 | +0.00 | -0.0157% |
| AVAXUSDT | 0.51 | 1.839 | -3.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 2.57 | 1.948 | -3.5% | -113.50 | -112.65 | +0.0099% |
| LTCUSDT | 0.72 | 2.124 | -2.5% | +0.00 | +0.00 | +0.0080% |
| TRXUSDT | -0.69 | 1.119 | +1.6% | +0.00 | +0.00 | -0.0385% |
| DOTUSDT | -1.31 | 1.431 | -1.5% | +0.00 | +0.00 | +0.0028% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
