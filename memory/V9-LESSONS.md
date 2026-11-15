# V9 lessons — read every run (kept short by the weekly review)

Evidence-based notes for Claude's judgement. Only the weekly review edits this
file, and only from scorecard numbers, never from a single trade.

- Prior from research (2026-09-24): overriding the signal because "price
  already moved" or "no catalyst" lost money in v1-v8; event risk (hacks,
  delistings, macro prints inside the 6h hold, exchange outages) is where
  discretion can help.
- 2026-11-15 (weeks 1-8, 140 scored runs / 1704 decisions): still 0
  discretionary and 0 NEWS: overrides. Value-add -$1.07 (87 "changes", 38
  helped) is entirely the gate's x0.96 margin scaling, unchanged since 10-19.
  No evidence of skill either way: approve unless there is real event risk
  inside the 6h hold.
- 2026-11-15: drawdowns recover on the strategy's own: week 8 +$38.2 (live
  -$40.75 -> -$2.59), scored strategy-alone +$37.9 (+4.75 -> +42.64), with no
  overrides. Weeks 5/7 losses were also the signal's. Do NOT override to "fix"
  a drawdown - not overriding through weeks 5-7 is what captured week 8.
- 2026-11-15: missed/late runs remain the largest ops problem: ~16 runs this
  week for ~28 bars (11-08/09/10 00/06, 11-11 00/06/18, 11-13..14 several
  missed). On a late run trade straight to the current plan, no catch-up
  trades; log missed bars.
- 2026-11-08: the 5% daily-loss circuit breaker (fired 11-05) is the rail
  working - never route around it; after 00:00 UTC trade straight to plan.
- 2026-10-19..11-15: margin_cap (50%) often blocks a last leg at 5x / 2.4x
  (e.g. TRX 11-15); expected, not a fault. BTC lot step 0.001 rounds BTC below
  target.
- 2026-11-15: maker share 79% over 309 groups (backtest assumed 70%):
  maker-first limits work; keep them.
- 2026-11-15: paper (vol 0.80, 2.4x) 30d -2.7% / 60d +0.4% / 90d +1.3%
  (DD -27.0%); was 90d -22.7% a week ago - well back inside the tested range.
  Live -1.3% since start tracks paper 60d, so execution is not the problem.
  Keep 9.5% stops and plan sizing; risk level is owner-only.
- 2026-11-15: the binance_delist feed has been down most runs since 11-03 -
  say so when it is, and check delistings manually for non-majors.
