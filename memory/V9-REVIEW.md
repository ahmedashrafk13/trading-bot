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
