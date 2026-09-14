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
