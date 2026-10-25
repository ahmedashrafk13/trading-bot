# V9 weekly reviews

One entry per week, written by `routines/v9-weekly.md`. PROPOSALS here need lab
evidence and the owner's OK. Scheduled runs never enact them.

## 2026-09-27 — week 1 (v9 live since 2026-09-24 15:54 UTC, ~2.7 days)

**P&L**
- Since v9 start (= this week): **+$0.38 (+0.2% of budget)** at review time. That
  includes open SOL uPnL of +$1.69. At the last run (07:25) it was -$1.56.
- Drawdown: $0.00 from peak (review time is the new peak, +$0.38). Worst point
  logged was -$2.05 (-1.0%) at the 09-26 12:12 run.
- Closed trades: DOT +$2.68, LINK -$0.75, ADA -$3.07 (gross). 1 win out of 3.
  SOL long still open ($87, SL 111.52). Fees $0.14 in total.

**Edge re-check (`revalidate`, frozen strategy, vol 0.55, 2.4x cap, 70% maker)**
- 30d +0.4% (DD -9.6%) | 60d -13.1% (DD -19.2%) | 90d **-18.9%** (DD -26.5%).
- Last check (09-24): 30d +1.8% | 60d -8.6% | 90d -20.1%.
- Still inside the tested range (EDGE ALERT would be 90d below about -25%), near its
  bottom. 60d got worse by 4.5 pts.

**Live vs paper**
- Paper over the v9 window (18:00 close 09-24 to 06:00 close 09-27, 11 bars, fees
  and funding included): -0.81% = **-$1.61**. Live at the 06:00-bar run: **-$1.56**.
  The gap of +$0.05 is noise. Execution and overrides cost nothing so far.
  (Scratch computation using `v9.build_panel` + `lab.sim.run_weights`. No tool
  prints this yet, see P2.)

**Claude's decisions (`scorecard`)**
- 96 decisions scored over 8 runs, plus 1 run not scored yet: **108/108 approve,
  0 overrides, value-add $0.00**. No action types to break down.
- 8 runs is below the 60-run minimum, so there is no verdict on skill.
- One factual slip: the runs on 09-25 cited "August PCE Sep 26", but Sep 26 was a
  Saturday. The 09-26 run caught and corrected it. It changed no decision.

**Maker fills**
- **75%** over 8 order groups. The backtest assumed 70%, and the alert line is 40%.
  Entries were 5/5 maker. Exits were 1/3 maker: the DOT and LINK closes filled as
  taker. With only 8 groups this sample is small.

**Alerts**
- No EDGE ALERT. No maker alert. No live-vs-paper alert (needs 4+ weeks).
- **OPS ALERT: schedule adherence.** The bot should have acted on 11 bars (18:00
  09-24 through 06:00 09-27). It acted on 8 of them. **All three 00:00-UTC bars
  were missed**:
  - 09-25: no run at all.
  - 09-26: the 00:11 run wrote decisions but never executed or committed.
  - 09-27: no run at all.

  Also, 5 of the 8 scheduled runs started more than 30 min late (+32m, +68m, +78m,
  +99m, +122m), and there was one off-schedule re-run (09-25 23:18).
  - Cost so far: two of the missed bars would not have changed the book. The 09-26
    one would have closed DOT, which stayed open ~8h longer. It happened to gain
    ~$0.37: paper would have closed at ~1.2128, live closed at 1.2215.
  - Why it matters: the lab's timing-luck test found that the 6h candle alignment
    alone moves lockbox results between -21% and +66%/yr. Runs 1-2h late trade an
    alignment that was never tested.
  - Owner action: check why the 00:07 UTC (05:07 PKT) run fails, and why runs start
    late. The repo does not show the cause. Check the scheduler and whether the PC
    sleeps or the app is closed overnight. This is not a strategy change.

**Proposals (owner decides; none enacted)**
- Strategy (signal, threshold, vol target, universe): **no change proposed.** 2.7
  live days give no evidence. Keep the pre-committed rule: if the 90d paper return
  drops below -25%, write an EDGE ALERT and recommend lowering the risk level or
  pausing.
- P1 (tooling, `scripts/v9.py`, owner edit): make `scorecard`/`status` report
  **missed and late bars**. Count the bars since start with no logged run, plus
  each run's delay after the bar close. Today the scorecard only scores the runs
  that happened, so the cost of missed runs is invisible. Test: on the current
  log it should report 3 missed bars (00:00 on 09-25, 09-26, 09-27).
- P2 (tooling, `scripts/v9.py`, owner edit): add `revalidate --since-start`. It
  would print the paper return over the live window next to live P&L, so the
  weekly live-vs-paper gap is reproducible without a scratch script. Test: it
  should reproduce -$1.61 for the 11 bars ending at the 09-27 06:00 close.

## 2026-10-04 — week 2 (v9 live since 2026-09-24 15:54 UTC, ~9.7 days)

**P&L**
- Since v9 start: **-$7.26 (-3.6% of budget)** at review time (08:4x UTC). That
  includes the open XRP short's uPnL of -$1.46.
- This week: **-$7.64**. The 09-27 review stood at +$0.38.
- Drawdown: **-$7.65 from the peak** (-3.8%). The worst logged run was -$9.18
  (-4.6%) at 10-02 07:42.
- Fees: $0.66 in total since start. Risk level was raised to vol 0.80 on 10-02.
  The first run at the new level was 10-02 18:13.

**Edge re-check (`revalidate`, frozen strategy, vol 0.80, 2.4x cap, 70% maker)**
- 30d -4.0% (DD -14.3%) | 60d -9.3% (DD -18.6%) | 90d **-15.5%** (DD -22.5%).
- Last week (vol 0.55): 30d +0.4% | 60d -13.1% | 90d -18.9%. The 90d figure
  improved even at the higher vol. The 30d figure turned negative.
- **No EDGE ALERT.** The line is 90d below about -25%, so it is 9.5 pts inside the range.

**Live vs paper** (scratch: `v9.build_panel` + `lab.sim.run_weights`, vol 0.55
until the 10-02 12:00 close and 0.80 after; it reproduces last week's -$1.61 at
the 09-27 06:00 close)
- Paper from the 09-24 18:00 close to the 10-04 06:00 close: **-2.07% = -$4.13**
  (DD -4.6%). This week alone: -$2.52.
- Live: **-$7.26**. The gap is about **-$3.1**. Claude made 0 overrides, so
  overrides did not cause it. Likely sources:
  - Missed and late runs (below). Paper changed position on bars that live
    skipped. Examples: LINK close and XRP open at 10-03 00:00/06:00, which live
    did at 12:45.
  - BTC qty floor: the 10-02 target of 0.0018 BTC was floored to 0.001.
  - Market-fallback fills.
- The pre-committed live-vs-paper alert needs 4+ weeks, so this is not an alert
  yet. Watch item.

**Claude's decisions (`scorecard`)**
- 360 decisions over 30 runs: **360/360 approve, value-add $0.00**. No action types
  to break down. news-driven line: 0 overrides, $0.00.
- 30 runs is below the 60-run minimum, so there is still no verdict on skill.

**Maker fills**
- **81% over 37 order groups** (assumed 70%; alert below 40%). Market fallback
  mostly happens on exits (10-01 00:00 run 0/2 maker, 10-03 18:13 run 1/2).

**Alerts**
- No EDGE ALERT, no maker alert, no live-vs-paper alert (needs 4+ weeks).
- **OPS ALERT (worse than week 1): schedule adherence.**
  - 39 bars since start (09-24 18:00 → 10-04 06:00). **10 had no run**:
    - 00:00 on 09-25, 09-26, 09-27, 09-28, 10-03, 10-04
    - 18:00 on 09-27
    - 06:00 on 09-28, 10-03, 10-04
  - Of the 29 bars that did get a run, **10 started more than 30 min late**:
    +75, +106, +129, +39, +85, +320, +227, +102, +227 and +45 min.
  - The 00:00-UTC slot (05:07 PKT) fails most often: 6 of 10 since start.
- **OPS ALERT: position off strategy right now.**
  - The frozen strategy's target has been **flat since the 10-04 00:00 close**,
    and it is still flat at 06:00.
  - Live still holds an **XRP short of 89.4 (~$134, SL 1.6318)** because neither
    run happened.
  - This review places no orders. The 12:07 UTC run should close it. If that run
    is missed too, the owner may want to close it by hand.
- **CONFIG NOTE: uncommitted live config.**
  - Several files have uncommitted working-tree edits: `scripts/v9.py`,
    `scripts/checks.py`, `CLAUDE.md` and both routines.
  - The live code runs vol 0.80, **gross cap 2.4x, leverage 5x, stop 9.5%**.
    `checks.py` MARGIN_CAP was changed 0.50 → **0.60**.
  - CLAUDE.md says gross ≤ 2.0x, 4x leverage, 12% stop, margin ≤ 50%.
  - The STOP_PCT comment cites "25% liquidation distance at 4x", but LEVERAGE = 5.
  - 9.5% at 5x passes the gate (half of 20% = 10%), but the lab's stop study
    tested 8% and 12%, not 9.5%.
  - This review did not touch these files. The owner should decide the intended
    setup and commit it.

**Proposals (owner decides; none enacted)**
- Strategy (signal, threshold, vol target, universe): **no change proposed.**
  - 9.7 live days is noise.
  - The paper 90d is inside the tested range.
  - The pre-committed EDGE ALERT rule stands.
- P3 (config, owner): make the documented and the running config the same.
  - Either restore the lab-tested 4x / 12% / 2.0x setup (2.0x at 4x = 50%
    margin, so MARGIN_CAP can go back to 0.50), or document 5x / 9.5% / 2.4x /
    0.60.
  - If keeping 9.5%, confirm it in the lab: rerun
    `backtest/lab/strategies/_stop_study.py` with a 9.5% stop at 5x / 2.4x on
    dev (walk-forward), then make one lockbox look.
  - Then commit `scripts/v9.py` and `scripts/checks.py`, and run
    `python scripts/test_checks.py`.
- P1 (still open): `scorecard`/`status` should report missed and late bars.
  - Test: on the current log it should report 10 missed bars of 39.
- P2 (still open): `revalidate --since-start`, so the live-vs-paper figure is
  reproducible. Test: it should print -$4.13 to the 10-04 06:00 close, with
  vol switching to 0.80 at 10-02 18:00.
- Ops (owner): fix the scheduler, the most urgent item this week. Find out why
  the 00:07 UTC run fails and why runs start late: PC sleep, the app being
  closed, or task queueing. Missed bars are now the largest measurable cost
  (~-$3 vs paper).

## 2026-10-11 — week 3 (v9 live since 2026-09-24 15:54 UTC, ~16.7 days)

**Measure**
- P&L since v9 start: **-$3.14 (-1.6% of budget)**; this week **+$4.12** (from -$7.26 at the 10-04 review). From peak: -$3.53.
- Open: AVAX long $72, LTC long $108, SOL short $120, all with stops.
- Scorecard: 54 runs / 648 decisions. Strategy alone +$8.80 gross, with Claude +$8.66, **value-add -$0.14**.
  - All 30 "changed" decisions are `approve*0.96` = execute's margin scaling of the book (2.0x gross at 4x = 50% margin, scaled to 96%), not Claude's judgement. 16/30 helped. Real discretionary overrides: 0. NEWS: overrides: 0.
- Maker-fill share **78% over 88 groups** (assumed 70%).
- Paper (frozen, vol 0.80, 2.0x): 30d **+0.5%** (DD -12.5%), 60d **+3.2%** (DD -14.2%), 90d **-5.9%** (DD -18.6%). All improved vs 10-04 (-4.0 / -9.3 / -15.5).
- Live vs paper: scorecard strategy-alone is +$8.80 gross over scored runs vs live -$3.14 net; the gap is fees + bars with no/late run (24 runs this week vs 28 bars; several 2-5h late), not overrides.

**Judge**
- 90d paper -5.9% > -25% → inside tested range. **No EDGE ALERT.**
- Maker share 78% ≥ 40% → fee assumption holds.
- Claude value-add: -$0.14 over 54 runs, below the 60-run minimum and caused by margin scaling only → no lesson yet.
- NEWS-driven line: 0 overrides, $0.
- Config: the 10-04 CONFIG NOTE is resolved — code now matches CLAUDE.md (vol 0.80, gross 2.0x, 4x, 12% stop, MARGIN_CAP 0.50) and is committed. P3 closed.
- Ops: missed/late runs continue (e.g. 10-10 00:00 missed, 06:00/12:00 runs ~2.5h late). Still the largest measurable cost.

**Proposals (owner decides; none enacted)**
- Strategy: **no change proposed** (16.7 live days; paper inside range and recovering).
- P1 (open): scorecard/status should report missed and late bars.
- P2 (open): `revalidate --since-start` for a reproducible live-vs-paper figure.
- P4 (new, tooling): scorecard should not count the gate's uniform `*0.96` scaling as a Claude override (it inflates "changed decisions" with non-judgement noise). Test: on the current log, changed decisions → 0, value-add → $0.00.
- Ops (owner): fix the scheduler (late/missed 00:07 and 06:07 UTC runs).

## 2026-10-19 — week 4 (v9 live since 2026-09-24 15:54 UTC, ~24.8 days; review ran Mon, a day late)

**Measure**
- P&L since v9 start: **-$0.09 (-0.0% of budget)**; this week **+$3.05** (from -$3.14 at 10-11). From peak: -$4.08.
- Open: shorts TRX $180, BNB $87, BTC $82, XRP $53, SOL $52, all with SL (uPnL ~+$0.04).
- Scorecard: 77 runs / 948 decisions. Strategy alone +$22.47 gross, with Claude +$21.40, **value-add -$1.07** (87 changed, 38 helped) - all `approve*0.96` margin scaling, 0 discretionary, 0 NEWS:.
- Maker-fill share **79% over 149 groups** (assumed 70%).
- Paper (frozen, vol 0.80, 2.4x): 30d **+3.9%** (DD -8.4%), 60d **-3.8%** (DD -14.3%), 90d **-10.4%** (DD -20.8%).
- Live vs paper: scored strategy-alone +$22.47 gross vs live -$0.09 net. Gap ~$22 = fees/funding + missed/late bars, not overrides (none).

**Judge**
- 90d paper -10.4% > -25% → inside tested range. **No EDGE ALERT.**
- Maker share 79% ≥ 40% → fee assumption holds.
- Claude value-add negative over 77 runs, but entirely margin-scaling noise (see P4) → no "override less" lesson; there are no overrides.
- NEWS-driven line: 0 overrides, $0.
- **OPS ALERT:** last run 2026-10-17 00:20 UTC; no runs for ~2.4 days (~9 bars). Positions held stale with stops. Scheduler/PC problem is worse than before.
- Config 10-16 (5x / 9.5% / 2.4x) is committed and matches CLAUDE.md; margin_cap blocked top-ups 4 times this week (expected at 2.4x/5x vs 50% cap).

**Proposals (owner decides; none enacted)**
- Strategy: **no change proposed.**
- Ops (owner, URGENT): restore the 6h runs - check whether the PC/app was off or asleep since 10-17.
- P1 (open): scorecard/status report missed and late bars.
- P2 (open): `revalidate --since-start` for a reproducible live-vs-paper figure.
- P4 (open): scorecard must not count the gate's uniform x0.96 scaling as a Claude override.
- P5 (new, lab): explain the ~$22 live-vs-scored gap - split into fees, funding, and missed bars. Test: reconstruct from `fills` + funding history for 09-24..10-19.

## 2026-10-25 — week 5 (v9 live since 2026-09-24 15:54 UTC, ~30.7 days)

**Measure**
- P&L since v9 start: **-$23.99 (-12.0% of budget)**; this week **-$23.90** (from -$0.09 at 10-19). From peak: -$27.98.
- Open: shorts XRP $95, SOL $91, BTC $161; longs ADA $62, AVAX $56; all with SL (uPnL ~+$0.69).
- Scorecard: 95 runs / 1164 decisions. Strategy alone **+$3.31** gross (was +$22.47), with Claude +$2.25, **value-add -$1.07** (87 changed, 38 helped) - unchanged; all `approve*0.96` margin scaling, 0 discretionary, 0 NEWS:.
- Maker-fill share **79% over 196 groups** (assumed 70%).
- Paper (frozen, vol 0.80, 2.4x): 30d **-14.5%** (DD -20.5%), 60d **-12.8%** (DD -20.5%), 90d **-20.5%** (DD -26.0%).
- Live vs paper: live -12.0% over ~31d vs paper 30d -14.5% → live is not lagging paper this month; the week's loss is the strategy's (scored strategy-alone -$19 gross), not execution or overrides.

**Judge**
- 90d paper -20.5% > -25% → still inside tested range, **no EDGE ALERT**, but within ~4.5 pts of the line (was -10.4% a week ago). WATCH: if next week's 90d falls below -25%, the routine requires an EDGE ALERT and a recommendation to lower risk or pause.
- Maker share 79% ≥ 40% → fee assumption holds.
- Claude value-add negative over 95 runs, but entirely margin-scaling noise (P4) → no "override less" lesson; there are no overrides.
- NEWS-driven line: 0 overrides, $0.
- Ops: 18 scored runs this week vs ~28 bars; several 3-4.7h late, 06:00/12:00 bars missed repeatedly; last run 10-24 10:37 UTC (~4 bars missed before this review). Better than week 4's 2.4-day outage, still the main ops cost.

**Proposals (owner decides; none enacted)**
- Strategy: **no change proposed** - a 1-month -12% is within the stated -40..-50% DD expectation; no lab evidence for a change.
- Owner FYI (not a proposal to act now): paper 90d is approaching the pre-committed alert line at the "very high" risk level (vol 0.80). Size menu (`backtest/lab/results/_size_menu_*.json`) shows vol 0.55 as the tested lower-risk option if the owner prefers to de-risk pre-emptively.
- Ops (owner): restore reliable 6h runs (06:07 / 12:07 UTC most often missed).
- P1, P2, P4, P5 (open, unchanged).
