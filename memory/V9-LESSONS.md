# V9 lessons — read every run (kept short by the weekly review)

Evidence-based notes for Claude's judgement. Only the weekly review edits this
file, and only from scorecard numbers, never from a single trade.

- Prior from research (2026-09-24): overriding the signal because "price
  already moved" or "no catalyst" lost money in v1-v8; event risk (hacks,
  delistings, macro prints inside the 6h hold, exchange outages) is where
  discretion can help.
- 2026-11-22 (weeks 1-9, 152 scored runs / 1848 decisions): still 0
  discretionary and 0 NEWS: overrides. Value-add -$1.07 (87 "changes", 38
  helped) is entirely the gate's x0.96 margin scaling, unchanged since 10-19.
  No evidence of skill either way: approve unless there is real event risk
  inside the 6h hold.
- 2026-11-15: drawdowns recover on the strategy's own: week 8 +$38.2 (live
  -$40.75 -> -$2.59), scored strategy-alone +$37.9 (+4.75 -> +42.64), with no
  overrides. Weeks 5/7 losses were also the signal's. Do NOT override to "fix"
  a drawdown - not overriding through weeks 5-7 is what captured week 8.
- 2026-11-22: missed/late runs are now the biggest measurable cost: live
  +2.5% vs paper 60d +22.0% (gap ~19.5 pts; was 1.7 at 11-15) with 12 runs
  for ~28 bars this week and none from 11-20 18:13 to the review. On a late
  run trade straight to the current plan, no catch-up trades; log missed bars.
- 2026-11-08: the 5% daily-loss circuit breaker (fired 11-05) is the rail
  working - never route around it; after 00:00 UTC trade straight to plan.
- 2026-10-19..11-15: margin_cap (50%) often blocks a last leg at 5x / 2.4x
  (e.g. TRX 11-15); expected, not a fault. BTC lot step 0.001 rounds BTC below
  target.
- 2026-11-22: maker share 78% over 324 groups (backtest assumed 70%):
  maker-first limits work; keep them.
- 2026-11-22: paper (vol 0.80, 2.4x) 30d +40.9% / 60d +22.0% / 90d +18.7%
  (DD -27.0%), inside the tested range. Overrides cost only -$1.07, so the
  live gap is missed bars, not judgement. Keep 9.5% stops and plan sizing.
- 2026-11-22: the binance_delist feed was down 11-03..11-18 (10/10 ok since) -
  say so when it is down, and check delistings manually for non-majors.
