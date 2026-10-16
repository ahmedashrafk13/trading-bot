# Trading Bot — v9 (2026-09-24)

Claude-driven crypto trader on a Bybit **DEMO** account (`api-demo.bybit.com`),
**$200 trading budget**, USDT **perpetual futures**, long and short, leverage 5x.
Treat it with live-money discipline.

v9 SUPERSEDES every earlier version (v1–v8: CORE / TACTICAL / SHORT sleeves,
carry, BTC+ETH trend, conviction sizing). Their rulebook is archived at
`memory/archive/CLAUDE-v8.md` for history only — do not apply its rules.
Why they were retired: an audit on 2026-09-24 found the v8 numbers were inflated
(a sqrt(24) Sharpe units bug, perp funding on longs never charged); honestly
measured, v8 earned ~+7.7%/yr over the last 15 months.

## How a run works

`routines/v9.md` is the only run procedure (every 6h, 00:07/06:07/12:07/18:07 UTC):
1. `python scripts/v9.py plan` — the tested strategy's targets + a brief.
2. `python scripts/news_check.py` (event-risk flags), then Claude researches and
   decides: approve / skip / resize (0–1.5x) / flip, plus
   its own trades → `data/live/decisions.json`.
3. `python scripts/v9.py execute` — maker-first limit orders, market fallback,
   attached stopLoss, every opening order through `scripts/checks.py`.
4. `python scripts/v9.py status` + a short entry in `memory/V9-JOURNAL.md`.

## The strategy (what the numbers are)

`micro_crowd`: fade the retail crowd on 12 major perps. Signal = 30d z-score of
Binance's GLOBAL long/short ACCOUNT ratio (5-minute feed); |z| ≥ 1.5 → take the
other side for 6h; inverse-vol sizing; book vol target 0.80 (owner 2026-10-02, was 0.55);
gross ≤ 2.4x budget, 5x leverage, 9.5% attached stop since 2026-10-16 (4x / 12% / 2.0x 2026-09-30..10-16; 2.4x / 5x / 8% before;
see backtest/lab/strategies/_stop_study.py - the 8% stop cut winners, no DD benefit).

Measured in `backtest/lab/` (independent, adversarially verified harness,
survivorship-aware data, Bybit fees + slippage + funding + liquidation):
- walk-forward out-of-sample 2022-12..2025-06: Sharpe 1.25 at 20% vol
- LOCKBOX 2025-07..2026-09 (never used for tuning; BTC −16%): at vol 0.55 with
  a 2.5x gross cap (live uses 2.4x) and 70% maker fills **+54.5%/yr, max DD −40.8%,
  0 liquidations**; with all-taker fills roughly half that.
- TIMING LUCK (measured 2026-09-24): the same strategy on the six possible 6h
  candle alignments made -21%..+66%/yr over the lockbox (avg ~+22%/yr); every
  alignment was positive on 2022-25. The live timing (00/06/12/18 UTC closes) is
  the tested one, but plan on ~+20-25%/yr with -40..-50% drawdowns, not +54.5%.
- The edge is decaying (huge in 2023, weaker since). Expect bad months: at this
  risk level a −25% month is possible. No configuration wins every trade.
- The signal MUST come from Binance's ratio: on Bybit's own ratio the same
  strategy lost −5.6% over the lockbox.
- Full research record: `backtest/lab/results/` (REPORT.md, PORTFOLIO.json,
  per-strategy JSON) and `memory/HYPOTHESIS-LOG.md`. Strategies that FAILED
  honest testing (do not re-propose without new evidence): trend ensembles,
  volatility breakout, pairs, cross-sectional momentum/reversal, carry (idle),
  OI flush, wick-catching, crowd composites on 53 coins, LightGBM ranker,
  new-listing / pump / squeeze event trades, the equal-weight ranker.

## Safety rails — enforced in code (`scripts/checks.py`), not by this file

- $200 budget cap; every % is of the budget, never the $179k demo balance.
- Every opening perp order carries an attached stopLoss (v9: 9.5% at 5x since 2026-10-16), stop
  inside half the liquidation distance (12.5% at 4x, 10% at 5x); leverage ≤ 5x.
- Margin ≤ 50% and gross notional ≤ 300% of budget; daily realized loss ≥ 5% of
  budget stops new entries until 00:00 UTC.
- `touch HALT_TRADING` = kill switch for new entries; exits always work.
- `python scripts/test_checks.py` after any edit to checks.py.
- Never withdraw. Never bypass the gate (no BYBIT_SKIP_GATE, no raw API entries).

## Owner directives in force

- Perps, shorts and leverage are enabled (2026-09-22); risk level "very high"
  = vol target 0.80 (2026-10-02; 0.55 from 2026-09-24). Size menu: backtest/lab/results/_size_menu_{dev,lockbox}.json - lockbox vol 0.8 @ 2.0x +54%/yr DD -33%, dev +165%/yr DD -50% (2.5x cap: lockbox +65% / -39%; live 2.4x since 2026-10-16). Only the owner changes the budget or risk level.
- Claude stays in the decision loop with full discretion inside the rails; its
  decisions are logged against the strategy's (`memory/V9-LOG.csv`).

## Tools

- `scripts/v9.py` plan | execute [--dry] | flatten-legacy [--dry] | status |
  scorecard [--brief] (Claude vs strategy, in $) | revalidate (paper-trade the
  frozen strategy on recent live data)
- `routines/v9-weekly.md` — weekly review (Sun 13:37 PKT): scorecard, edge
  re-check, lessons for Claude. Strategy changes need lab evidence + owner OK.
- Loss guard: `plan` flags REVIEW at -35% of budget and creates HALT_TRADING at
  -50% (only the owner resumes).
- `scripts/bybit.py` (positions linear, tickers, kline, fills, funding, …)
- `python scripts/news_check.py` - event-risk flags (RED/AMBER/INFO) from free feeds
  every run; flags justify only skip / resize <= 1, reasons tagged `NEWS:` are
  scored separately. Tests: `python scripts/test_news_check.py`.
- `bash scripts/perplexity.sh "<q>"` or WebSearch for news.
- Research lab: `backtest/lab/README.md`; data in `data/hist/` (gitignored).

Communicate ultra-concise: short bullets, no fluff.
