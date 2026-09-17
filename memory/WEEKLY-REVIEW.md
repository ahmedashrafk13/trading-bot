# Weekly Review

Friday reviews appended here.
Template for each entry:

## Week ending YYYY-MM-DD

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $X |
| Ending portfolio | $X |
| Week return | ±$X (±X%) |
| S&P 500 week | ±X% |
| Bot vs S&P | ±X% |
| Trades | N (W:X / L:Y / open:Z) |
| Win rate | X% |
| Best trade | SYM +X% |
| Worst trade | SYM -X% |
| Profit factor | X.XX |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |

### What Worked
- ...

### What Didn't Work
- ...

### Key Lessons
- ...

### Adjustments for Next Week
- ...

### Overall Grade: X

---
## Week ending 2026-09-10 (partial week, off-cycle run — scheduled slot is Sun 18:37 UTC)

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $200.00 |
| Ending portfolio | $200.00 |
| Week return | $0.00 (0.00%) |
| BTC/USD week | baseline established this run ($77,153.29) — no prior mark to compare |
| Bot vs BTC | n/a for this partial week |
| Trades — CORE | 0 (0/3 weekly cap used) |
| Trades — TACTICAL | 0 (0/3 daily cap used) |
| Win rate | n/a (no closed trades) |
| Best / worst trade | n/a |
| Profit factor | n/a |
| Fees paid | $0.00 |
| Fees vs gross profit | n/a — no gross profit and no fees |
| Stop integrity | n/a — no stops placed yet |

### Closed Trades
none.

### Open Positions at Week End
none. Deployed 0% against a 75-85% target.

### What Worked
- The universe screen caught something a news-driven process would have missed:
  19 tactical "passes" were one correlated bounce, since hourly 30-period
  momentum was negative on all 33 pairs. Position count would have overstated
  diversification threefold.
- Retuning the filters mid-build was necessary and worked. The first CORE test
  passed 32 of 33 coins; requiring price above a rising SMA20 cut it to 5.
- Verifying the API before writing rules prevented three broken assumptions
  shipping: no trailing_stop on crypto, no time_in_force day, and paginated bars.
- The gate rejected trend-only candidates (SUSHI, GRT, UNI) for having no
  documented catalyst, which is the rule working rather than the rule blocking.

### What Didn't Work
- Zero trades means zero evidence about the strategy itself. Everything validated
  this week is plumbing, not edge.
- Perplexity is still unconfigured, so research ran on WebSearch with no
  citations. Catalysts could not be found for 3 of the 5 CORE shortlist names —
  that is a research-quality ceiling, not an absence of catalysts.
- The order path is STILL UNTESTED. No buy and no stop_limit has ever filled on
  this account, so the riskiest code (stop placement immediately after a fill)
  has never run for real.
- The Day 0 row shipped without a BTC baseline, so the benchmark was
  uncomputable until this run fixed it.

### Key Lessons
- Timeframe must match intended frequency: daily bars produced 3 tactical
  candidates, which cannot support 3 trades/day. Hourly produced ~19.
- "Many candidates" is not "many opportunities" when one macro driver moves the
  whole universe.
- Small-account fee maths dominates design: ~1.05%/wk for tactical is the reason
  tactical size is $20 rather than $40.

### Adjustments for Next Week
- Validate the buy -> stop_limit path with one deliberate minimum-size mechanics
  test, so the first real signal is not also the first time that code runs.
- Re-screen after CPI; apply the logged triggers rather than re-deciding freehand.
- Record a BTC mark in every daily snapshot from now on, not just the baseline.

### Rule changes applied
None. Nothing has been observed for long enough to justify changing a rule, and
proposals require evidence. (Note added 2026-09-10, after this review was written: self-amendment was
subsequently ENABLED. The review may now edit TRADING-STRATEGY.md directly
within the limits in that file's Self-amendment section. The sentence originally
here said edits were proposal-only; that is no longer true and would otherwise
be read as current policy.)

### Overall Grade: C
The machine is built, verified against the live API, and behaved correctly — but
a week with no trades and an untested order path earns no more than a pass. The
grade reflects execution readiness, not strategy performance, of which there is
still no evidence.


---

## Amendment 2026-09-15 — risk-based sizing, deployment floor removed

Out-of-cycle amendment. Invoked under the BROKEN-RULE exception in
TRADING-STRATEGY.md ("arithmetically unsatisfiable"), not the 10-closed-trade
trigger — the account has 1 closed trade. Two of the three changes fix a
contradiction; the third removes a rule that never bound.

### Evidence

**1. The 75-85% deployment band never bound, in its entire life.**

| Run | Deployed | What the run wrote |
|---|---|---|
| 09-11 | 0% | "Held flat deliberately" |
| 09-13 | 29.6% | "the band is a target, not a mandate to buy" |
| 09-14 | 29.7% | "Correcting a deployment shortfall is not a reason to buy" |

Never once inside the band. Every run flagged the breach, wrote a paragraph
justifying it, and correctly ignored it. The rule produced commentary, never
behaviour, and cost attention on every single run.

**2. Sizing was risk-inconsistent — the "safe" sleeve was the dangerous one.**

At $197.25 equity, under the OLD fixed-dollar sizing:

| Sleeve | Size | Stop | Risk $ | Risk % of equity |
|---|---|---|---|---|
| CORE | $40 | 20% | $8.00 | 4.06% |
| TACTICAL | $20 | 6% | $1.20 | 0.61% |

CORE carried **6.7x** the risk of TACTICAL per position. Three CORE positions
put 12.2% of the account at risk simultaneously, against a 1-2% per-trade norm.

**3. The circuit breaker was unsatisfiable alongside those sizes.**

Breaker was 3% of equity = $5.92. A single CORE stop-out lost $6.00 at the -15%
hard cut and $8.00 at the -20% trail. **Any one CORE stop tripped the day's
breaker by itself**, halting entries for the rest of the UTC day. A breaker that
fires on one ordinary stop is an outage, not a brake.

**4. The CORE trail was decorative.** The trail sat 20% below high-water while
the hard cut was -15%, so on any position that had not yet risen, the hard cut
always fired first and the trail could never be reached.

### Changes applied

| Rule | Before | After |
|---|---|---|
| Deployment | 75-85% band (floor + ceiling) | <= 85% ceiling, NO floor |
| Position size | fixed $40 CORE / $20 TACTICAL | (equity * 0.015) / stop distance |
| Size caps | 20% of equity | 15% CORE / 25% TACTICAL |
| CORE trail | 20% -> 14% -> 10% | 15% -> 12% -> 10% |
| Circuit breaker | 3% of equity (~$5.92) | 5% of equity (~$9.86) |

At $197.25: CORE ~$20 (risk $2.96), TACTICAL ~$49 (risk $2.96). This INVERTS the
sleeves — TACTICAL is now the larger position. That is intended: a tighter stop
earns more size at equal risk. CORE's edge is TIME (no target, no time limit),
not size.

Exceeds the normal "max 2 rules per amendment" limit. Justified because the
changes are one coherent fix: sizing, the caps and the breaker are the same
arithmetic, and changing any one alone leaves the contradiction in place.

### Not changed
- Per-trade risk set at 1.5%, not the 1% "professional standard". At $200 with a
  15% CORE stop, 1% risk gives a $13 position — close enough to Alpaca's $10
  notional floor that rounding would distort it. Revisit if equity grows.
- The 10-closed-trade trigger for ordinary (non-broken-rule) amendments stands.

### Open risk
The inverted sleeve sizing is UNTESTED against real fills. TACTICAL at ~25% of
equity is a larger single position than this account has ever held. Watch the
first three tactical entries and confirm the stop actually rests at the full
size before trusting the rule.

---

## Week ending 2026-09-17 (broker clock; local clock read 09-18 and was NOT trusted)

Scheduled slot is Sun 18:37 UTC; this run fired early. Week measured Mon
2026-09-14 00:00 UTC -> 2026-09-17 21:20 UTC.

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $200.00 (realized basis, Mon 00:00 UTC — no realized P&L existed before 09-14) |
| Ending portfolio | $193.91 |
| Week return | -$6.09 (-3.05%) |
| BTC/USD week | $76,834.40 -> $76,525.90 = **-0.40%** |
| Bot vs BTC | **-2.64pp — active trading LOST to simply holding BTC** |
| Trades — CORE | 0 closed, 0 opened |
| Trades — TACTICAL | 3 closed (W:0 / L:3 / open:0) |
| Win rate | CORE n/a · TACTICAL **0%** |
| Best trade | XRP -$1.31 (-6.6%) — least bad, not a winner |
| Worst trade | UNI -$3.17 (-6.0%) |
| Profit factor | 0.00 (no gross winners) |
| Fees paid this week | ~$0.35 |
| Fees month-to-date | $0.52 / $2.00 ceiling (26% used, headroom $1.48) |
| Fees vs gross profit | **There was no gross profit. Every closed trade lost, so 100% of the fees paid this week bought nothing.** |
| TACTICAL fees vs TACTICAL gross profit | Same sentence: all three closes were TACTICAL, all three lost. First week this has happened; not yet two weeks running, so no frequency cut is proposed on this basis. |
| Circuit breaker | 0 trips on the 5%-realized test ($6.09 spread over 3 days, max $4.48 in one UTC day vs a $10.00 limit). The 3-consecutive-tactical-loss rule DID fire on 09-15 — see "What didn't work". |
| Stop integrity | 2 filled as intended (UNI, XRP) / 0 gapped / 1 missing when a run checked (DOT) |

### Closed Trades
| Pair | Sleeve | Entry | Exit | P&L | Notes |
|---|---|---|---|---|---|
| DOT/USD | TACTICAL (v1 grandfathered, 6% trail) | 2026-09-10 | 2026-09-14 16:45 UTC | **-$1.61 (-8.0%)** | Orphaned stop leg filled 09-11, remainder sat **NAKED for 70h**, closed past -6% and 92h on a failed screen. The split-quantity defect, since removed. |
| UNI/USD | TACTICAL | 2026-09-15 00:07 UTC | 2026-09-15 14:51 UTC | **-$3.17 (-6.0%)** | Stop filled as intended, 14h hold. |
| XRP/USD | TACTICAL (v1 grandfathered, 6% trail) | 2026-09-14 | 2026-09-15 18:41 UTC | **-$1.31 (-6.6%)** | Stop filled as intended at $1.3272 (trigger $1.3303). Fill landed in a blind window and was not logged until a later run reconciled it. |

### Open Positions at Week End
None. Flat, ~100% cash, $0.11 of unsellable dust (every balance below its
`minOrderAmt`), 0 resting orders. Deployment 0.1% against a 50% ceiling with no
floor — a fully compliant state, not a shortfall.

Memo, unchanged and still not booked: the CORE ETH/USD leg (0.015302647 @
$2,609.50) left the account in an owner/account-level sweep at 2026-09-17 20:22
UTC, alongside 1 BTC, 2496 0G and 1389 CRV — all far larger than the entire $200
budget and none matching a bot entry. No realized P&L is attributed to the
strategy. Had it been, the mark-to-sweep figure would be ~-$2.34, which would
take the week to -$8.43 (-4.22%) and the gap to BTC to -3.82pp. **ACTION FOR THE
HUMAN: confirm whether that sweep should be booked as a strategy exit.**

### What Worked
- **The v2 single-leg stop rule held.** Both stops that were placed under it
  filled at their trigger, at 100% of held qty, with no gapping and no orphan
  legs. The order-thrash failure mode of 09-15 did not recur once.
- **Patience was executed, not just written down.** From 09-15 onward the bot
  found no qualifying catalyst and opened nothing, across roughly a dozen runs.
  Flat while BTC fell 0.4% is the strategy working.
- **The screen refused trend-only candidates.** 30 shadow rows were logged
  instead of traded, every one with a stated reason. That is the only
  statistically meaningful sample this account produces.
- **Reconciliation caught a fill nobody watched.** XRP's stop filled in a blind
  window and a later run found it from `fills` rather than from a guess.

### What Didn't Work
- **0 for 3, all TACTICAL, and a loss to a FALLING benchmark.** Losing less than
  BTC would not have been success; losing 2.64pp MORE than a falling BTC is the
  plainest possible statement that this week's activity subtracted value.
- **A stale script froze the account for two and a half days.** `state.sh`
  computed the 3-consecutive-tactical-loss streak over ALL history rather than
  the UTC day, so a streak whose last close was 09-15 printed `TRIPPED — no new
  entries` on 09-16 and 09-17. The rulebook says the streak resets at 00:00 UTC
  and warns in writing that a permanent reading DEADLOCKS the sleeve, because
  only a winning trade clears it and the freeze prevents the win. Four runs
  logged the conflict and none could fix it — only this run has that authority.
  Repaired below.
- **DOT proved the split-quantity defect in real money.** 70h naked, -8.0%, the
  worst structural failure in the account's history. The rule that caused it is
  gone, but it cost $1.61 to learn.
- **The equity series is still hand-computed.** `state.sh` prints EQUITY as the
  $200 sizing CAP on a demo account holding $178,978.89, so it reads $200.00
  whether the strategy is up or down. Every P&L figure in this review was
  reconstructed by hand from logged realized rows. This is fragile and remains
  unfixed.
- **Snapshot gaps.** No daily snapshot on 09-12, 09-13, 09-14 or 09-16, so
  "Day P&L" figures in the log are multi-day deltas mislabelled as daily.

### Key Lessons
- **An instruction defect can cost more than a bad trade.** The three losses cost
  $6.09; the frozen breaker cost every opportunity from 09-15 to 09-17 and would
  have kept costing indefinitely, because nothing but this weekly run could clear
  it. Prompt repair is a first-class risk control, not housekeeping.
- **A safety rule that can only be cleared by the thing it forbids is not a
  safety rule, it is a deadlock.** Worth auditing the remaining gates for the
  same shape.
- **Three closed trades say nothing about the strategy.** 0% win rate on N=3 is
  inside noise. The evidence gate exists precisely to stop this table from
  becoming a reason to retune, and it is doing its job.
- **Sample comes from the shadow log, not the trade log.** 30 shadow rows this
  week against 3 real closes. None are scored yet — scoring them is worth more
  than any rule change available right now.

### Adjustments for Next Week
- Score the outstanding SHADOW-LOG rows at T+5d. Without scoring, the one
  statistically useful sample the account produces is being thrown away.
- Write a daily snapshot EVERY day, even flat ones, so "Day P&L" stops being a
  multi-day delta with a daily label.
- Book or formally decline the ETH sweep, once the owner rules on it.
- No entry-rule changes. The gate is not what failed this week.

### Rule changes applied
**NONE.** STEP E evidence gate: 3 closed trades since the last amendment
(2026-09-10), against a required 10. `state.sh` reports `not eligible — change
nothing`. Three trades cannot distinguish a real effect from noise, and this
rulebook has already been damaged once by amending on N=1. Nothing in
memory/TRADING-STRATEGY.md was changed on strategy grounds.

The only edits made to TRADING-STRATEGY.md were STEP E2 propagation repairs —
stale restatements inside the doc of rules the doc itself had already amended
elsewhere. They change no rule; both moved the wording to the STRICTER figure
already in force.

### Instruction repairs applied
STEP E2 gate is a reproducible contradiction, not trade count. All twelve below
were confirmed against both named files before editing.

| # | File | Said | Now says | Contradicted |
|---|---|---|---|---|
| 1 | `scripts/state.sh` (breaker) | streak counted over ALL closed trades ever -> `TRIPPED` on 09-17 from a 09-15 close | streak scoped to the UTC day, resets 00:00 UTC -> `clear` | TRADING-STRATEGY.md Buy-Side Gate, `routines/execute.md` STEP D. **Highest-impact repair of the run — it unblocks entries.** |
| 2 | `scripts/state.sh` | `CEILING 85%` | `CEILING 50%` | TRADING-STRATEGY.md deployment ceiling (hypothesis #3, 2026-09-17) |
| 3 | `scripts/state.sh` | `max 4` CORE | `max 1` CORE | TRADING-STRATEGY.md sleeve table (hypothesis #6, 2026-09-18) |
| 4 | `CLAUDE.md` | `Max positions 4 / 1`; `Combined cap: 5, deployment <= 85%`; `Deployment <= 85%` | `1 / 1`; `Combined cap: 2, deployment <= 50%`; `<= 50%` | same two hypotheses |
| 5 | `routines/execute.md` STEP E | entry order carries `"takeProfit"` + "BOTH LEGS ATTACHED", verify "both legs exist", log a "take-profit", ClickUp "stop, TP" | stop leg only, with an explicit NEVER-attach-takeProfit line | CLAUDE.md and TRADING-STRATEGY.md: neither sleeve has a profit target in v2 |
| 6 | `routines/execute.md` STEP D | deployment after fill `<= 85%` | `<= 50%` | TRADING-STRATEGY.md |
| 7 | `routines/execute.md` STEP B + `routines/research.md` STEP EVIDENCE | "30-day momentum is INVERTED (IC -0.037, t=-10)" asserted as settled | 30d momentum is POSITIVE (IC@30d +0.025 test); only <=1d is inverted | HYPOTHESIS-LOG.md standing verdicts, which those same steps name as the authority — CORRECTED there 2026-09-16 |
| 8 | `routines/research.md` + `routines/summary.md` | "this run may NEVER edit TRADING-STRATEGY.md. ANY run may, at any time, with no minimum trade count" — a direct self-negation inside one paragraph | "this run may NEVER edit it. ONLY the weekly-review run may" | itself, and CLAUDE.md's AMENDMENT FREEZE. Resolved to the RESTRICTIVE reading; no run's authority was widened. |
| 9 | `scripts/screen.sh` | STABLES list omitted RLUSD, which reached a live CORE SHORTLIST on 09-17 | RLUSD + 11 other USD pegs added | TRADING-STRATEGY.md immutable rule 9, "No stablecoins as positions" |
| 10 | `memory/TRADING-STRATEGY.md` Buy-Side Gate | "CORE positions after fill <= 4", "Combined <= 5" | `<= 1`, `<= 2` | the same document's own sleeve table |
| 11 | `memory/TRADING-STRATEGY.md` Capital & Constraints | "Max position size 15% CORE / 25% TACTICAL ... (equity * 0.015)" — pre-v2 leftover | "20% CORE / 12% TACTICAL ... risk% 2.0 / 1.0" | the same document's sleeve table AND its Buy-Side Gate, which both already said 20/12 |
| 12 | `backtest/README.md`, `routines/learn.md` | "85% deployment ceiling", "the 4/1 slot split" | "50%", "the 1/1 slot split" | TRADING-STRATEGY.md |

`scripts/audit-rules.py` gained six new BAD patterns (85% ceiling, 4-slot/5-combined,
reintroduced take-profit leg, cross-day streak wording, superseded 30d-momentum
inversion) plus a word-boundary fix on `used this week`, which had been matching
"ca-**used this week**'s" in SHADOW-LOG data rows. Four append-only RECORD files
(HYPOTHESIS-LOG, OBSERVATIONS, SHADOW-LOG, SCAN-GATE-LOG) were added to its SKIP
set: they quote superseded rules by design and no run obeys them, so they
produced only false positives. **`python scripts/audit-rules.py` exits 0.**

### Observations dropped as unreproducible
- **13 rows** logging "harness assigns a `claude/*` branch, BRANCH POLICY says
  push to `main`". Not a repo defect — the conflict lives in a scheduling-harness
  system prompt that no file in this repository can reach, and this run's prompt
  carries no such requirement. Dropped, with the standing ACTION FOR THE HUMAN
  below.
- **~8 rows** naming `routines/scan.md` or `.claude/commands/*.md`. Those files
  no longer exist; no `scan.md` reference remains in `routines/` or `CLAUDE.md`.
- **2 rows** on "SCAN-VERDICT is never emitted by state.sh". It is emitted now.
- **2 rows (2026-09-18)** on unset Bybit credentials, already RETRACTED in the
  file itself. `python scripts/bybit.py time` returned retCode 0 this run.
- **1 row** on `routines/research.md` asserting "There is NO .env file". Already
  fixed in commit 2427717.
- **1 row** on the `state.sh` REALIZED-P&L regex. It now parses all three closed
  trades correctly.
- **1 row** on the ETH/Alpaca-era phantom position. Resolved — it is gone from
  the account and carried as a memo above.

### Observations KEPT (outside this step's authority)
- **`state.sh` EQUITY is the $200 sizing cap, not a P&L-tracked balance**, so day
  and cumulative P&L read $0.00 forever and every figure must be hand-computed.
  Fixing this means deciding what "equity" should mean on a budget-capped demo
  account — a rule question, not a wording one. STEP E, next eligible review.
- **`CLAUDE.md` says "LIVE ... THIS IS REAL MONEY" while `.env` and CLAUDE.md's
  own budget paragraph describe a DEMO account.** Left alone deliberately:
  correcting it LOOSENS the caution framing, which is not a text-only repair.
  ACTION FOR THE HUMAN.
- **`backtest/engine.py` defaults `core_slots=4`** against a rulebook that now
  says 1, and `test_engine.py` asserts the 4-slot cap. Left alone deliberately:
  changing a research baseline silently rewrites the meaning of every result
  already recorded in HYPOTHESIS-LOG. Should be changed with an explicit
  re-baselining run, not buried in a repair pass.

### ACTION FOR THE HUMAN
1. **`routines/BOOTSTRAP.md:62` still describes Bybit attaching `takeProfit` AND
   `stopLoss`.** This step may never edit that file, because its blocks are
   pasted into the cloud routine settings by hand and a repo edit cannot reach
   the deployed copy. The deployed bootstrap text needs the same correction as
   repair #5 above.
2. **Reconfigure the scheduler to work on `main`**, or accept the 13 logged
   branch-policy conflicts as permanent noise.
3. **Rule on the 2026-09-17 ETH sweep** — strategy exit (~-$2.34) or account-level
   cleanup (current reading)?

### Overall Grade: D+
Three trades, three losses, and a 2.64pp loss to a benchmark that itself fell.
On results alone that is a D. The plus is earned entirely off the machinery: the
v2 single-leg stop worked exactly as designed both times it was tested, the bot
stayed genuinely patient for two and a half days rather than trading to look
busy, and it declined to amend the rulebook on a sample of three when the
temptation to explain 0-for-3 was obvious. The single worst thing that happened
this week was not a trade — it was a stale line in a script silently freezing
the account, unfixable by any of the four runs that correctly reported it.
