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
proposals require evidence. (Note: strategy edits are proposal-only pending your
approval — the agent cannot amend TRADING-STRATEGY.md itself.)

### Overall Grade: C
The machine is built, verified against the live API, and behaved correctly — but
a week with no trades and an untested order path earns no more than a pass. The
grade reflects execution readiness, not strategy performance, of which there is
still no evidence.

