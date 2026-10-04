# V9 lessons — read every run (kept short by the weekly review)

Evidence-based notes for Claude's judgement. Only the weekly review edits this
file, and only from scorecard numbers, never from a single trade.

- 2026-09-24 (start): no live record yet. Prior from research: overriding the
  signal because "price already moved" or "no catalyst" lost money in v1-v8;
  event risk (hacks, delistings, macro prints inside the 6h hold, exchange
  outages) is where discretion can help.
- 2026-09-27 (week 1, 8 scored runs / 96 decisions): Claude approved 108 of 108
  decisions, value-add $0.00. Too few runs to judge skill (60+ needed). No
  evidence yet for overriding more; keep approving unless there is real event risk.
- 2026-09-27: live tracks paper. At the 06:00-bar run live P&L was -$1.56 vs
  -$1.61 for the frozen strategy paper-traded over the same 11 bars (gap +$0.05).
  Maker share 75% over 8 order groups (entries 5/5 maker, exits 1/3). Execution
  is not leaking money so far.
- 2026-10-04 (week 2, 30 scored runs / 360 decisions): still 360/360 approve,
  value-add $0.00, 0 NEWS: overrides. Still below the 60-run minimum. Nothing
  supports overriding more; keep approving unless there is real event risk.
  Scheduled AMBER prints (NFP inside the hold on 10-02) were approved; no scored
  evidence yet either way.
- 2026-10-04: the live-vs-paper gap is now -$3.1 over the v9 window (live -$7.26
  vs paper -$4.13, 0 overrides). Cause: missed and late runs (10 of 39 bars
  missed, 10 more >30 min late), not Claude's decisions. A late run should still
  trade straight to the current plan (no catch-up trades) and log which bars
  were missed. Today the strategy has been flat since the 10-04 00:00 close,
  but the XRP short stayed open because no run happened.
- 2026-10-04: maker share 81% over 37 order groups (assumed 70%). Market
  fallback still happens mostly on exits. Fees $0.66 total. Execution cost is small.
- 2026-10-04: paper re-check of the frozen strategy, now at vol 0.80:
  30d -4.0% (DD -14.3%), 60d -9.3% (DD -18.6%), 90d -15.5% (DD -22.5%).
  The 09-27 figures at vol 0.55 were 90d -18.9% / 60d -13.1% / 30d +0.4%.
  Still inside the tested range (alert below -25% on 90d). The 30d figure turned
  negative. Watch it, don't panic.
