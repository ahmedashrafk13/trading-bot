# V9 lessons — read every run (kept short by the weekly review)

Evidence-based notes for Claude's judgement. Only the weekly review edits this
file, and only from scorecard numbers, never from a single trade.

- Prior from research (2026-09-24): overriding the signal because "price
  already moved" or "no catalyst" lost money in v1-v8; event risk (hacks,
  delistings, macro prints inside the 6h hold, exchange outages) is where
  discretion can help.
- 2026-11-08 (weeks 1-7, 124 scored runs / 1512 decisions): still 0
  discretionary and 0 NEWS: overrides. Value-add -$1.07 (87 "changes", 38
  helped) is entirely the gate's x0.96 margin scaling, unchanged since 10-19.
  No evidence of skill either way: approve unless there is real event risk
  inside the 6h hold.
- 2026-11-08: the losing weeks are the strategy's own, not Claude's. Week 5
  -$23.9, week 7 -$15.2; 11-05 the signal's ETH + LTC longs (fading crowd
  shorts) lost ~-$23 into a -6% day, stops (9.5%) not hit (LTC -7.5%, ETH -7%).
  Do NOT start overriding to "fix" a drawdown - there is no evidence it helps.
- 2026-11-08: missed/late runs remain the largest ops problem: only 12 runs
  this week for ~28 bars (11-05 06/12, 11-06 00/06, 11-07 00/06/12, 11-08
  00/06/12 missed). Positions then sit 15-24h with only the stop. On a late
  run trade straight to the current plan, no catch-up trades; log missed bars.
- 2026-11-08: the 5% daily-loss circuit breaker fired on 11-05 (realized
  -$14.15) and blocked the 18:12 shorts until 00:00 UTC. That is the rail
  working - never route around it; after 00:00 trade straight to plan.
- 2026-10-19..11-08: margin_cap (50%) often blocks top-ups or a last leg at
  5x / 2.4x; expected, not a fault. BTC lot step 0.001 rounds BTC below target.
- 2026-11-08: maker share 79% over 280 groups (backtest assumed 70%):
  maker-first limits work; keep them.
- 2026-11-08: paper (vol 0.80, 2.4x) 30d -22.9% / 60d -20.3% / 90d -22.7%
  (DD -27.0%); 90d has sat 2-5 pts above the -25% alert line for 3 weeks
  (-20.5, -23.1, -22.7). Live -20.4% since start tracks paper 60d, so
  execution is not the problem. Keep 9.5% stops and plan sizing; risk level
  is owner-only.
- 2026-11-08: AMBER flags in weeks 6-7 were stale hack / KOSPI headlines with
  no event inside the hold; approving was correct. The binance_delist feed
  was down 11-03..11-05 - say so when it is, and check delistings manually.
