# V9 lessons — read every run (kept short by the weekly review)

Evidence-based notes for Claude's judgement. Only the weekly review edits this
file, and only from scorecard numbers, never from a single trade.

- 2026-09-24 (start): no live record yet. Prior from research: overriding the
  signal because "price already moved" or "no catalyst" lost money in v1-v8;
  event risk (hacks, delistings, macro prints inside the 6h hold, exchange
  outages) is where discretion can help.
- 2026-09-27..10-11 (weeks 1-3, up to 54 runs): every decision approved,
  0 discretionary / 0 NEWS: overrides; value-add only from the gate's x0.96
  margin scaling. Execution matched paper early (gap +$0.05 on 09-27).
- 2026-10-04: the live-vs-paper gap is now -$3.1 over the v9 window (live -$7.26
  vs paper -$4.13, 0 overrides). Cause: missed and late runs (10 of 39 bars
  missed, 10 more >30 min late), not Claude's decisions. A late run should still
  trade straight to the current plan (no catch-up trades) and log which bars
  were missed. Today the strategy has been flat since the 10-04 00:00 close,
  but the XRP short stayed open because no run happened.
- 2026-10-11: maker share 78% over 88 groups; paper 90d -5.9% / 60d +3.2% /
  30d +0.5% (vol 0.80), all better than 10-04. Live -$3.14 since start. Missed
  and late runs remain the main cost: on a late run trade straight to the
  current plan, no catch-up trades.
- 2026-10-19 (week 4, 77 scored runs / 948 decisions): past the 60-run mark.
  Value-add -$1.07 (38/87 helped), but all 87 "changes" are the gate's x0.96
  margin scaling - 0 discretionary overrides, 0 NEWS:. No evidence of skill
  either way; the default stays: approve unless there is real event risk.
- 2026-10-19: no run since 10-17 00:20 UTC (~9 bars missed, positions held
  stale ~2.4 days with stops on). Missed runs remain the largest cost. On the
  next run trade straight to the current plan; no catch-up trades. With 5x /
  2.4x since 10-16, margin_cap blocks top-ups often - that is expected, not a fault.
- 2026-10-19: paper (vol 0.80, 2.4x): 30d +3.9% / 60d -3.8% / 90d -10.4%
  (DD -20.8%). Inside the tested range. Maker share 79% over 149 groups.
- 2026-10-25 (week 5, 95 scored runs / 1164 decisions): still 0 discretionary
  and 0 NEWS: overrides; value-add -$1.07 unchanged (all x0.96 gate scaling).
  This week's -$23.9 loss is the strategy's own (scored strategy-alone fell
  from +$22.47 to +$3.31 gross), not Claude's choices. Do NOT start overriding
  to "fix" a losing week - there is no evidence discretion helps.
- 2026-10-25: paper 90d -20.5% (DD -26.0%), 30d -14.5% - near the -25% alert
  line. Live -12.0% since start, slightly better than paper 30d. Stops at 9.5%
  stay as-is; keep sizing to plan. Runs were still late/missed (last run
  10-24 10:37 UTC); trade straight to the current plan, no catch-up trades.
- 2026-11-01 (week 6, 112 scored runs / 1368 decisions): still 0 discretionary
  and 0 NEWS: overrides; value-add -$1.07 unchanged (all x0.96 gate scaling).
  Week -$1.55 (live -12.8% since start). Default stays: approve unless real
  event risk; do not override to chase the drawdown.
- 2026-11-01: paper 90d -23.1% (DD -29.6%), 30d -15.4% - 1.9 pts from the
  -25% alert line. Maker share 80% over 251 groups. Only 17 runs this week
  (~28 bars); last run 10-30 16:25 UTC. On a late run trade straight to the
  current plan, no catch-up trades.
