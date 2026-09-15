# Trade Log

## Day 0 — EOD Snapshot (pre-launch baseline)
**Portfolio:** $200.00 | **Cash:** $200.00 (100%) | **Day P&L:** $0 | **Phase P&L:** $0

No positions yet.

---
## 2026-09-10 — PIVOT: stocks -> crypto
Strategy replaced. All entries above are from the stocks era and are historical
only. From here the account trades Alpaca crypto USD pairs exclusively, long only,
with resting stop_limit protection. Baseline unchanged: $200.00, all cash.

---
## 2026-09-10 — Daily Snapshot (Day 0 crypto, UTC 19:39)
**Portfolio:** $200.00 | **Cash:** $200.00 (100%) | **Day P&L:** $0.00 (0.00%) | **Cumulative:** $0.00 (0.00%)
**vs BTC:** 0.00% (baseline established) | **Fees today:** $0.00

**BENCHMARK BASELINE — BTC/USD = $77,153.29 @ 2026-09-10 19:39 UTC.**
All future "vs BTC" figures are measured against this price. It was missing from
the Day 0 row, which meant the benchmark the strategy is judged on could not be
computed at all.

| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
|--------|------|-----|-------|------|------------|--------------|---------------|
| — | none | — | — | — | — | — | — |

**Trades today:** none. CORE 0/3 this week. TACTICAL 0/3 today.
**Deployed:** 0% (target band 75-85%).

**Notes:** First day under the crypto two-sleeve model; no positions opened. The
universe screen returned 5 CORE and 18-19 TACTICAL nominal passes, but hourly
30-period momentum was negative across all 33 pairs, so every tactical pass was
the same short bounce inside a longer downtrend rather than an independent setup.
CPI lands tomorrow pre-open and FOMC begins Tuesday with a 62.2% implied chance
of a rate hike, which is the wrong window to start weeks-long CORE holds in. Only
DOT had a documented catalyst (dotUSD referendum, transaction spike, short
squeeze) and it sat +18.1% over its SMA20, barely inside the extension limit.
Held flat deliberately: at 0% deployed the account is below its 75-85% target,
which is the correct state when no setup clears the gate.

---
## 2026-09-10 — MECHANICS TEST (not a strategy trade)

**This was NOT a signal.** The strategy decision on record for 2026-09-10 was
HOLD both sleeves. This round trip was placed deliberately, with the user's
explicit approval, to validate the buy -> stop_limit -> cancel -> close code path,
which had never executed. Do not count it in win rate, and do not treat BTC as
having been a signalled entry.

| Field | Value |
|---|---|
| Sleeve | MECHANICS TEST (neither CORE nor TACTICAL) |
| Pair | BTC/USD |
| Ordered qty | 0.00016 |
| Filled qty | 0.0001596 (fee taken in kind) |
| Avg entry | $77,103.20 |
| Notional | $12.31 |
| Stop placed | stop_limit GTC, trigger $72,477.01 (-6%), limit $71,027.47 |
| Stop verified resting | yes — status `new`, correct qty |
| Exit | cancelled the stop, closed whole at market |
| Round-trip cost | $0.08 = 0.65% of the position, 0.04% of the account |
| Ending equity | $199.92 |

### What this test proved works
1. Market buy with `time_in_force: gtc` fills.
2. A `stop_limit` GTC sell is accepted and RESTS at the broker.
3. `cancel <order_id>` removes it (204).
4. `close BTCUSD` exits the whole position.

### What it caught that would have broken live trading
1. **$10 minimum notional per order.** The first attempt at ~$1.54 was rejected
   outright. Our gate only checked `min_order_size` (a quantity floor of about
   $1 for BTC), so it would have approved orders the API refuses.
2. **Buy fees are charged IN KIND.** Ordered 0.00016 BTC, received 0.0001596 —
   0.25% removed from the asset. Placing the stop for the ORDERED qty would have
   been rejected for insufficient balance, leaving the position NAKED at exactly
   the moment the prompt believes it is protected. This was the single most
   dangerous latent bug in the system.
3. **Symbol format is endpoint-dependent.** `close BTC/USD` returns 404;
   `close BTCUSD` works. Previously a guess in PROJECT-CONTEXT, now confirmed.
4. **Real friction is 0.65%, not 0.5%** — and that is on BTC, the tightest
   spread available. Tactical fee drag revised from ~1.05%/wk to ~1.37%/wk.

**Deviation from plan:** the approved test was ~$1-2. The $10 API floor made
that impossible, so it ran at $12.31 — still well under the $20 tactical size.

---
## 2026-09-10 — TACTICAL entry: DOT/USD (first real strategy trade)

| Field | Value |
|---|---|
| Sleeve | **TACTICAL** |
| Pair | DOT/USD |
| Side | buy |
| Ordered qty | 18.018 |
| Filled qty | 17.972955 (0.25% fee taken in kind) |
| Entry | $1.11 |
| Entry time (UTC) | 2026-09-10T20:22 (backfilled — the format did not require it at the time) |
| Notional | $19.85 |
| Hard cut (-6%) | $1.0434 |
| Stop order | stop_limit GTC, trigger $1.04340, limit $1.02253, order cbaf290f |
| Stop verified resting | yes — status `new`, qty matches position exactly |
| Target (+14%) | $1.26540 |
| R:R after fees | 2.01 : 1 (risk $1.33, reward $2.67) |
| Est. round-trip fee | $0.13 |
| Fee budget after | $0.13 / $3.00 used this week |
| Equity after entry | $199.77 (cash $179.92) |

**Thesis / catalyst:** Polkadot OpenGov Referendum 1944 to create a native
stablecoin (dotUSD) is passing with ~97.5% in favour, alongside a 150%
transaction spike and record XCM throughput on 2026-09-07. DOT was the only coin
in the 33-pair universe with a specific, dated, verifiable catalyst.

**Screen at entry (hourly):** mom7 +1.7%, vsSMA20 +0.7%, vol 0.7%, spread 0.18%
— PASS. Notably DOT had cooled from +18.1% over its daily SMA20 earlier today to
+0.7% over the hourly SMA20, so the extension concern that blocked it as a CORE
candidate this morning no longer applied to a tactical-horizon entry.

**Origination:** originated by the EXECUTE run, not planned by morning research,
which had recorded a tactical HOLD. Override justified as follows: the tactical
HOLD was explicitly a recommendation rather than binding; the coin passed the
current screen; the catalyst is documented and dated; and the R:R defect that had
blocked all tactical trades was fixed first (target 12% -> 14%). This is the
first exercise of intraday tactical origination authority.

**Management rules now in force:** close at market on -6% (or if the stop_limit
is gapped through without filling), raise the stop to breakeven at +6%, close at
market at +14%, reassess if open beyond ~48h.

### 2026-09-10 — DOT position: stop management correction

Tested whether a take-profit could rest alongside the stop, after asserting it
could not. Result: the assertion was WRONG in an important way.
- `order_class: oco` IS rejected for crypto (verified).
- But two resting sells DO coexist if they name different units: stop_limit on
  8.98 + limit on 8.99 of the 17.972955 position both rested fine. A resting
  order reserves only the qty it names; a FULL-SIZE stop is what leaves nothing
  available for a second order.

Position state during the test: -0.52%, i.e. at a small loss. Both split legs
were therefore CANCELLED and a full-size stop_limit restored (order a4b80584,
qty 17.972955, trigger $1.04340, limit $1.02253). Rationale: while a position is
flat or losing, the take-profit slice would be carrying no stop, and there is no
gain to bank — protection outranks upside capture.

The split structure now applies only from +6% onward, once the stop has been
ratcheted to breakeven, at which point the unstopped half can only give back an
unrealised gain rather than take a loss. Strategy and all prompts updated.

### 2026-09-10 21:05 UTC — DOT stop re-placed with a wider limit gap

Cancelled the stop and re-placed it with the limit 5% below the trigger instead
of 2%: trigger $1.04340 unchanged, limit $1.02253 -> $0.99123.

Reason: a stop_limit only fills if price trades between the trigger and the
limit. In a crypto flush 2% of room is routinely jumped, which turns the stop
into a no-op and leaves the position riding down with nothing watching until the
next run. 5% accepts a worse fill in exchange for actually filling — a bad fill
is a known cost, an unfilled stop is an unbounded loss. Applied to the strategy
and all prompts, not just this position.

### 2026-09-10 21:15 UTC — DOT split into stop + target legs (rule deviation, documented)

Position was +1.23%, i.e. BELOW the +6% rung that normally earns a target leg.
Split anyway, deliberately.

Reason: the +6% rung assumes an hourly scan exists to move it. No routine is
scheduled yet, so the rung would never have fired and this position would have
carried downside protection with permanently ZERO upside capture — a resting
stop and nothing else. The strategy clause has been amended to make the split
unconditional at entry whenever no scan cadence is running.

| Leg | Type | Qty | Level | Order |
|---|---|---|---|---|
| protection | stop_limit GTC | 8.986478 | trigger $1.04340 / limit $0.99123 | 5da2e7a3 |
| target | limit GTC | 8.986477 | $1.26540 (+14% on $1.11 entry) | 96e0e83d |

Total reserved 17.972955 = the full position. Both legs confirmed resting.

Accepted risk: the 8.986477 target slice carries NO stop. If DOT falls hard,
roughly $10 of exposure rides down until a run notices. Bounded and acceptable
against the certainty of capturing no upside at all. The +14% target is now
enforced by the EXCHANGE and needs no run to fire.

Orphan rule applies: whichever leg fills, the next run must cancel the other and
re-place a full-size stop on the remaining qty.


---
### 2026-09-11T15:16 UTC — ENTRY — CORE — ETH/USD BUY

| Field | Value |
|---|---|
| Entry time (UTC) | 2026-09-11T15:16 |
| Sleeve | **CORE** |
| Pair | ETH/USD |
| Side | buy (long) |
| Qty ordered | 0.015341 |
| Qty FILLED | 0.015302647 (fee taken in kind, ~$0.10) |
| Fill price | $2,609.50 |
| Notional | $39.93 cost basis |
| Hard cut (-15%) | $2,218.08 |
| Stop trigger | $2,087.60 (fill x 0.80) |
| Stop limit | $1,983.22 (trigger x 0.95) |
| Stop order id | c33ad688-2ff2-4214-a44c-a0c8e6ec2944 (qty 0.015302647 = 100%) |
| Target | none — CORE, let it run; ratcheted 20% trail decides |
| R:R | CORE has no target; risk $8.00 at the trail, $6.00 at the hard cut |
| Est. round-trip fee | $0.26 (0.65% of $40) |

**Thesis:** ETH is the only pair in the 33-coin universe passing BOTH the daily CORE
and hourly TACTICAL screens, and it does so with the tightest spread available
(0.027%). Catalyst is the ETF flow divergence — ETH spot ETFs ~+$863M net YTD versus
~-$1B for BTC, two consecutive months of out-gathering BTC, BlackRock ETHA +23.06K ETH
on Sep 4 — with Glamsterdam upgrade proposals behind it. 30d +38.9% but only +5.5%
above a rising SMA20, so it is trending without being extended (limit is 20%).

**Stop structure — FULL-SIZE, no split.** The "split at entry when no scan cadence is
running" clause exists to get a take-profit enforced by the exchange. CORE has no
profit target by design, so there is nothing to split to: 100% of the qty sits on the
stop. state.sh confirms [OK full stop], 0% unreserved.

**Gate:** CORE 1/3, combined 2/6, deployment 29.6% <= 85%, cost $39.93 <= cash $179.92,
notional >= $10, spread 0.027% <= 1%, tif gtc, crypto, not a stablecoin, on the CORE
shortlist, catalyst documented in today's RESEARCH-LOG, breaker clear, fee budget
$0.39/$2.98 after this trade. All pass.

---
## 2026-09-11 — Daily Snapshot (Day 1 crypto, UTC 15:16)
**Portfolio:** $198.77 | **Cash:** $139.89 (70.4%) | **Day P&L:** -$1.23 (-0.62%) | **Cumulative:** -$1.23 (-0.62%)
**vs BTC:** -2.50% | **Fees today:** ~$0.10 | **Fee budget:** $0.39 / $2.98 used this week

BTC/USD $78,605.24 vs the $77,153.29 Day 0 baseline = **+1.88%**. Account -0.62%.
Underperforming the benchmark by 2.50 pts.

| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
|--------|------|-----|-------|------|------------|--------------|---------------|
| TACTICAL | DOT/USD | 17.972955 | $1.1100 | $1.0601 | -4.66% | $1.04340 | yes — [SPLIT ok] 50% stop / 50% target, 0% unreserved |
| CORE | ETH/USD | 0.015302647 | $2,609.50 | $2,605.00 | -0.17% | $2,087.60 | yes — [OK full stop] 100%, 0% unreserved |

**Trades today:** 1 — CORE ETH/USD buy $40. TACTICAL 0/3, deliberately.
**Deployed:** 29.6% (target band 75-85%).
**Circuit breaker:** clear, $0.00 realized losses vs $5.96 limit. Not tripped today.
**Amendment trigger:** 0 closed trades logged, need >= 10. Not eligible — nothing changed.

**Notes:** Opened the first CORE position of the crypto era. ETH was the single pair
clearing both screens and it carried the only catalyst in the universe that is not
just "it already moved" — the ETF flow divergence is a two-month, measurable capital
shift, and ETH is trending without being extended. Deliberately left TACTICAL flat:
CPI prints today and FOMC is Sep 16, and an hours-horizon position into a macro print
is a coinflip rather than an edge, which is what the fee budget exists to prevent.
Deployment is 29.6%, well under the 75-85% band, and that is the correct state when
only one setup clears the gate — the band is a target, not a mandate to buy. DOT is
held rather than cut: its catalyst is intact so the thesis is not broken, but it now
fails the hourly screen and has rolled over, so it gets no more capital and the -6%
stop decides it. It is 18.9h old, inside the 48h reassess window. Account trails BTC
by 2.50 pts, driven entirely by the DOT drawdown.

---
### 2026-09-11 15:22 UTC — ETH split into stop + target legs (defect fix + rule amendment)

ETH was opened at 15:16 with a FULL-SIZE stop and no target, on the reasoning that
"CORE has no profit target by design, so there is nothing to split to." That was
wrong, and the user caught it.

**The defect:** CORE's exit is the ratchet, and the ratchet is EMULATED — it only
moves when a run cancels the stop and re-places it higher. No routines are scheduled.
So the position had a static stop at $2,087.60 and NO upside exit mechanism at all:
it could run +50%, round-trip back through entry to -20%, and that stop would never
move once. Upside capture was structurally, permanently zero. This is the SAME defect
the "no scan cadence" clause already documented for DOT; it was missed on CORE because
the "no profit target by design" wording made it look intentional rather than broken.

**Action — cancelled c33ad688 (full-size stop) and re-split, stop-heavy:**

| Leg | Type | Qty | Level | Order |
|---|---|---|---|---|
| protection | stop_limit GTC | 0.011476985 (75%) | trigger $2,087.60 / limit $1,983.22 | 4d0e9729-b5da-4904-bf88-0e9048710a28 |
| target | limit GTC | 0.003825662 (25%) | $3,392.35 (+30% on $2,609.50 fill) | 97be9328-63d3-426c-8612-4f5c4e9a1ce3 |

Total reserved 0.015302647 = 100% of the position. state.sh confirms [SPLIT ok],
0.0% unreserved. Stop trigger UNCHANGED at $2,087.60 — re-placed at the same level,
never moved down.

75/25 not 50/50, per the stop-heavy weighting rule: if the stop fires, the unstopped
slice keeps falling with no protection; if the target fires, the remainder keeps
running WITH its stop intact. The failure modes are not symmetric.

Target set at +30% because that is CORE's own first ratchet threshold — the level a
run WOULD have tightened the trail to 14% at. Since no run will, the exchange banks a
quarter there instead. Target leg is ~$9.98 of cost basis at entry and ~$12.98 at fill,
above the ~$9.97 sell that was previously accepted, so it clears the practical floor.

**Accepted risk:** the 0.003825662 target slice carries NO stop — roughly $10 of
exposure rides down unprotected if ETH falls. Bounded, and the alternative was a
guaranteed zero upside.

**Rule amendment applied to memory/TRADING-STRATEGY.md** under the Self-amendment
BROKEN-rule exception (not the 10-closed-trade trigger, which stands at 0/10): the
"no scan cadence -> split at entry" clause now explicitly covers CORE, at 75/25 with
the target at +30%. This is 1 tunable rule, within the 2-per-amendment limit, and it
touches no IMMUTABLE item — every position still carries a resting stop, stops are
still stop_limit only, and no stop was widened or moved down. Reverts to pure ratchet
the moment routines are live.

**BEFORE:** CORE = full-size stop, no target, ratchet decides the exit.
**AFTER:**  CORE while no cadence runs = 75% stop / 25% limit at +30%.
**EVIDENCE:** ratchet requires a run; zero runs scheduled; therefore zero upside
exits possible. Arithmetically unsatisfiable, not merely underperforming.

---
### 2026-09-14 16:40 UTC — EXIT — TACTICAL — DOT/USD — position fully closed

**Reconciliation first: an unlogged fill was found.** The stop leg
`5da2e7a3` FILLED on **2026-09-11T18:05 UTC** and no run recorded it, because no
cloud cadence is scheduled. The position then sat for **~70h with its entire
remaining quantity reserved by the target limit and ZERO stop coverage** — the
exact state the ORPHAN rule exists to prevent ("if one leg filled, cancel the
other and re-place a full-size stop on whatever qty remains"). The rule was
correct; there was simply no run to execute it. Caught by an ad-hoc `/portfolio`.

| Leg | Exit time (UTC) | Qty | Exit price | Gross | Fees | REALIZED P&L |
|---|---|---|---|---|---|---|
| stop_limit `5da2e7a3` | 2026-09-11T18:05 | 8.986478 | $1.0410 | -$0.620 | ~$0.034 | **-$0.654** |
| market close `30e42a1e` | 2026-09-14T16:40 | 8.986477 | $1.0130 | -$0.872 | $0.033 | **-$0.905** |
| buy-side fee in kind | 2026-09-10T20:19 | 0.045045 DOT | $1.11 | — | $0.050 | **-$0.050** |

- **TOTAL REALIZED P&L: -$1.609** on $20.00 deployed = **-8.0%**
- **REALIZED TODAY (UTC 2026-09-14): -$0.905** (the 09-11 leg belongs to that UTC day)
- Sell fee measured at **0.36%** of notional (cash +$9.07 on a $9.1033 sale) — above
  the 0.325% half of the 0.65% round-trip assumption. Worth watching, one sample.
- Orphan target leg `96e0e83d` cancelled before the close.

**Reason for closing the remainder:** three independent triggers, any one sufficient.
1. Unrealized **-8.72%**, past the TACTICAL -6% hard cut.
2. Age **92.3h**, past the 48h reassess window.
3. **FAILS** the current hourly TACTICAL screen (-0.2% 7d, -0.1% vs SMA20, vol 0.3%/h
   below the 0.4% floor) — the reassess rule says close unless the screen still passes.

**Post-mortem.** The dotUSD referendum / XCM throughput thesis never converted. DOT
drifted from entry and the momentum roll-over was already flagged in the 2026-09-11
research, which chose to "let the stop do its job" — correct, and the stop did fire on
half. The loss is not the defect. The defect is that the surviving half was unprotected
for 70h purely because nothing was running, and a -15% gap in that window would have
been uncapped. **The split-at-entry clause trades an unstopped slice for upside capture
on the assumption that SOME run will later clean up an orphan. With zero runs scheduled,
that assumption is false, and the clause is strictly worse than a full-size stop.**

Narrative: L1/L2 — **1** consecutive failed trade. Exit-the-narrative rule needs 2.

**No rule amendment applied.** The amendment trigger stands at 1 closed trade vs the
required 10, and this is not the BROKEN-rule exception: the orphan rule is not
defective, it is simply unexecuted. The correct fix is a running cadence, not a rule
edit. Flagged for the next weekly review if the cadence is still not live.

---
### 2026-09-14T16:43 UTC — ENTRY — TACTICAL — XRP/USD BUY

| Field | Value |
|---|---|
| Entry time (UTC) | 2026-09-14T16:43 |
| Sleeve | **TACTICAL** |
| Pair | XRP/USD |
| Side | buy (long) |
| Qty ordered | 14.15 |
| Qty FILLED | 14.114625 (fee taken in kind, 0.035375 XRP ~ $0.05) |
| Fill price | $1.41184 |
| Cost basis | $19.93 (10.1% of equity) |
| Order id | 801b0c56-cd88-4e67-91a9-0603623c6c58 |
| Hard cut | -6% = $1.32713 |
| Target | $1.60950 (+14%) |
| Est. round-trip fee | $0.13 (0.65% of $20) |
| R:R after fees | risk $1.33 / reward $2.67 = **2.01:1** |
| Narrative | Payments/legacy (XRP, LTC, BCH) |

**Thesis / catalyst:** the U.S. Senate holds its first floor test of the **Digital
Asset Market Clarity (CLARITY) Act on 2026-09-15**, one day out; the Senate returned
2026-09-14 with three weeks of floor time. Procedural motion to proceed, not final
passage. XRP is the highest-beta name to US regulatory clarity given its litigation
history. Documented in the RESEARCH-LOG intraday addendum BEFORE execution.

**Screen:** PASSES hourly TACTICAL — 7d +0.7%, +2.3% vs SMA20, vol 0.4%/h, spread
0.298% live (limit 0.5%). Above daily EMA20/50/200.

**Resting legs — SPLIT 50/50 at entry** (no-scan-cadence clause; `state.sh` confirms
[SPLIT ok], 0.0% unreserved):

| Leg | Type | Qty | Level | Order |
|---|---|---|---|---|
| protection | stop_limit GTC | 7.057312 (50%) | trigger $1.32713 / limit $1.26077 | 1e546303-c41f-46c5-b0fb-9dc8927abc98 |
| target | limit GTC | 7.057313 (50%) | $1.60950 (+14%) | 6d19a4c9-62e7-4859-bf2c-12655089542a |

**Why 50/50 and not the stop-heavy 75/25:** at a $20 notional a 25% target leg is ~$5,
and the strategy explicitly records that a ~$5 sell leg is **UNTESTED** against the
exchange minimum (only ~$9.97 sells are confirmed accepted). 50/50 puts both legs at
~$10, inside proven territory. The 75/25 weighting applies at the +6% rung on a larger
position; it is not worth a rejected order here. Matches the DOT precedent.

**Accepted risk — stated plainly.** Two things:
1. The 7.057313 target slice carries NO stop, so ~$10 rides down unprotected. This is
   the same exposure that just cost us on DOT, and it is only acceptable because the
   holding window is ~1 day around a dated event rather than open-ended.
2. The catalyst is a **BINARY, DATED** event inside the holding window. A failed motion
   to proceed is a plausible gap-down and a stop_limit can be gapped through. Sized at
   half a CORE position for exactly this reason.

**Gate:** all pass — tactical positions after fill 1/3, combined 2/6, cost $19.93 <=
cash $158.28, deployment 29.7% <= 85%, notional >= $10, spread 0.298% <= 0.5%,
fee budget $0.16 used / $2.95, circuit breaker clear (realized today -$0.905 vs
-$5.91 limit; 1 consecutive tactical loss vs 3), crypto, long only, not a stablecoin.

**Open item:** deployment is **29.7%**, far below the 75-85% band. Not corrected in
this run — CORE is where the missing ~$100 belongs and CORE requires a morning
research plan that does not exist today. Correcting a deployment shortfall is not a
licence to skip the research gate.

---
### 2026-09-14T22:58 UTC (local clock — broker clock unreachable, see below) — RUN FAILED — NO ACTION TAKEN

**execute run could not start.** `bash scripts/state.sh` (and `bybit.sh orders`
underneath it) failed with HTTP 403:
`The Amazon CloudFront distribution is configured to block access from your
country.` Confirmed NOT an auth/signature problem: the SAME 403/CloudFront body
came back from an **unauthenticated public** endpoint
(`/v5/market/tickers?category=spot&symbol=BTCUSDT`) hit directly with curl, so
`api-demo.bybit.com` is unreachable from this session's egress network
entirely, independent of API keys. Proxy status (`__agentproxy/status`) shows
zero relay failures, so this is Bybit/CloudFront rejecting the egress IP's
geography, not an org egress-policy block.

**Consequence: zero visibility and zero actions this run.**
- Could NOT reconcile positions against this log.
- Could NOT verify stop coverage on any open position (XRP tactical, and
  whatever CORE/other positions are live — last confirmed state is the
  2026-09-14T16:43 XRP entry above).
- Could NOT check for a -15%/-6% hard-cut breach.
- Could NOT ratchet any stop.
- Could NOT place any new entry (moot — no research/catalyst work was possible
  either, and none was attempted).
- No orders were placed, no stops were touched, nothing was cancelled or
  amended. This entry is documentation-only; the book is unchanged from the
  prior entry.

**Not treated as a rule amendment or a strategy defect** — this is an
infrastructure/network failure, not a trading-logic one. No amendment trigger
applies.

**Flag for the next run and for the user:** if this 403 persists next run too,
every open position will have gone stop-unverified across a >=12h gap (2x the
normal 6h). Whoever/whatever run picks this up next MUST treat stop
verification as the first priority the moment Bybit is reachable again,
regardless of how long the gap was.

---
### 2026-09-14T23:09 UTC (local clock — broker clock unreachable, see below) — SCAN FAILED — NO ACTION TAKEN

**scan run could not start**, same failure as the prior execute run just above.
`bash scripts/state.sh` -> `bybit.sh orders` -> HTTP 403,
`The Amazon CloudFront distribution is configured to block access from your
country.` Re-confirmed on `bybit.sh tickers` too. Proxy status shows zero
relay failures, so this is Bybit/CloudFront geo-blocking this session's
egress IP, not a key/auth problem and not an org egress policy.

**Consequence: zero visibility and zero actions this run**, same as the prior
failed run. No orders touched. Book unchanged.

**This is now 2 consecutive failed runs (execute 22:58 UTC, scan 23:09 UTC).**
Open positions (XRP tactical + whatever else was live as of the last confirmed
state, 2026-09-14T16:43 XRP entry) have now gone stop-unverified for a growing
gap approaching the normal 6h cadence x2+. Escalating this to the user now
rather than waiting for a 3rd failure. Not a strategy/rule defect — no
amendment triggered.

---
### 2026-09-14T23:30 UTC (broker clock) — EXECUTE — INVARIANTS ONLY, NO NEW ENTRIES

Alpaca reachable again (Bybit revert at 04070e5 already landed before this run
started). Ran the every-run invariants; no new trade this run.

**bash scripts/state.sh:** EQUITY $197.08 | CASH $138.30 | DEPLOYED 29.8%
(ceiling 85%, no floor). Fee budget $0.52/$2.96 used this week, headroom
$2.44. Circuit breaker clear: $0.00 realized losses today vs $9.85 limit, 0
consecutive losing closes. Amendment trigger: 0/10 closed trades — not
eligible, changed nothing.

**RECONCILE:** live positions (ETH, XRP) match the tail of this log. No fill
landed between runs; no drift.

**STOP COVERAGE:** both positions [SPLIT ok] — legs sum to 100%, 0% unreserved,
no naked qty. ETH 75% stop / 25% target, XRP 50% stop / 50% target — matches
their original split rationale in this log. Left the XRP and ETH target legs
alone per "existing split positions are left alone."

**HARD CUT:** ETH -3.26%, XRP +1.14% (was +1.43% pre-fee-adjustment view) —
neither near the -15%/-6% cuts. No close needed.

**RATCHET — CORE ETH — action taken.** ETH's resting stop was still at
$2,087.60, i.e. 20% below its $2,609.50 fill (the STEP G initial-placement
value from entry on 2026-09-11). Strategy Rule 6 requires the STANDING CORE
stop to sit 15% below the high-water mark, not 20% below fill — this was a
stale artifact never reconciled after the "hard cut and trail both 15%"
consolidation. Pulled hourly bars since entry (`crypto-bars ETH/USD 1H
2026-09-11`): peak high since the 15:16 UTC entry is $2,616.1105 (touched in
the entry hour, never revisited). Correct stop = 2616.1105 * 0.85 = $2,223.69.
- Cancelled stop order `4d0e9729-b5da-4904-bf88-0e9048710a28` (stop 2087.60 /
  limit 1983.22, qty 0.011476985 — the 75% stop leg).
- Replaced with `a3528027-144f-4a8e-8938-ed4ff891a5b6`: stop_limit sell
  0.011476985 ETH, stop_price 2223.69, limit_price 2112.51 (5% below trigger),
  gtc.
- Direction check: 2223.69 > 2087.60 — tightening, not a downward move. Never
  moved the stop down.
- Distance check: current price $2524.367, new stop is 11.9% below price —
  clear of the 5% minimum.
- The 25% target leg (limit sell 0.003825662 @ 3392.35, unchanged) was left
  untouched — existing split target legs are not retro-adjusted.
- Confirmed via `state.sh` post-trade: ETH still shows `[SPLIT ok]`, 0%
  unreserved.

**RATCHET — TACTICAL XRP.** +1.14%, below the +6% breakeven/split trigger.
Already split 50/50 from entry (documented at open); no ladder step due yet.
No action.

**ORPHAN CHECK:** no leg filled on either position since the last run: order
book unchanged apart from the ETH stop replacement above. No orphan.

**STEP B (today's research):** RESEARCH-LOG has a 2026-09-14 20:26 UTC entry:
CORE HOLD (no CORE entry planned), TACTICAL HOLD as a recommendation, with an
explicit override condition for originating a tactical entry this run: "the
CLARITY vote passes cloture AND a fresh, coin-specific setup clears the hourly
screen." The CLARITY cloture vote is scheduled for tomorrow, 2026-09-15
2:15pm ET — it has not happened yet as of this run (2026-09-14 23:30 UTC), so
the stated override condition is unmet. No new TACTICAL entry originated this
run; no CORE entry (none was planned by research). **No buy-side gate run —
nothing to gate.**

**Fees:** $0 this run (only a stop cancel/replace, no fill). Fee budget
unchanged at $0.52/$2.96.

**Circuit breaker / amendment trigger:** unchanged — clear / not eligible.

**Notification:** none sent — no trade was placed (ratchet-only run, per
routines/execute.md STEP I: notify only on a placed trade).

**Flag for a future run (not fixed now, out of this run's scope):**
`routines/execute.md` STEP G still tells a NEW CORE entry to place its initial
stop 20% below fill, but `memory/TRADING-STRATEGY.md` Core Rule 6 (the
authoritative rulebook) has consolidated CORE's hard-cut/trail to 15% since
before this run. That 20% figure is what let ETH's stop drift stale for 3
days until this run's ratchet caught it. Whoever next opens a CORE position
should place its initial stop at 15% below fill, not the 20% the routine
currently says, and the routine text should be corrected to match the
strategy doc so this does not recur silently on the next CORE entry.

## 2026-09-15 — SPLIT REMOVED, both positions migrated to full-size stops

Rule change, not a trade. No position opened or closed; no realized P&L.

**Why:** Alpaca crypto cannot rest a take-profit alongside a stop. Verified live
against the account today — `order_class: bracket` -> `42210000 ... otoco`,
`order_class: oco` / `trailing_stop` / `stop` -> `40010001 invalid order type`,
only `stop_limit` accepted. And a resting sell RESERVES its qty: with ETH fully
covered by two legs, an extra 0.001 sell returned
`insufficient balance for ETH (requested: 0.001, available: 0)`.

So the old "split the quantity" rule was buying exchange-enforced upside by
running 25-50% of every position with NO stop. That is what killed DOT: one leg
filled, the remainder sat 70h naked and closed at -8.0% / -$1.61 — the only
closed trade this account has ever had.

**Migrated (all four legs cancelled, full-size stops re-placed):**

| Pair | Was | Now | Stop trigger | Limit |
|---|---|---|---|---|
| ETH/USD | 75% stop + 25% limit @ 3392.35 | 100% stop, qty 0.015302647 | 2223.69 | 2112.51 |
| XRP/USD | 50% stop + 50% limit @ 1.6095 | 100% stop, qty 14.114625 | 1.32713 | 1.26077 |

Stop triggers were HELD AT THEIR PRIOR LEVELS — neither was moved down. ETH
2223.69 is its existing CORE trail; XRP 1.32713 is 6% below its 1.41184 entry,
correct for a TACTICAL position at +0.9% (below the +6% breakeven rung).

Both now read `[OK full stop]`, stop 100.0% / unreserved 0.0%.

**Upside from here is taken by the RUN, not the exchange.** The hourly scan
closes a TACTICAL position at market once it sees >= +14%. Accepted cost: a
spike that fully round-trips inside 60 minutes is missed. Accepted because the
alternative is an unstopped slice through every flush, 24/7.

---

## 2026-09-15 — RESTING LEG POLICY SPLIT BY SLEEVE (owner-directed)

Rule change, not a trade. No position opened or closed; no realized P&L.

Alpaca crypto allows ONE resting leg per position (a resting sell reserves its
qty; oco/bracket rejected). Account owner directed that PROFIT be captured at the
exchange and losses checked on a timer. Applied per sleeve, because only TACTICAL
has a target competing for the slot:

| Sleeve | Rests at exchange | Enforced by 30-min scan |
|---|---|---|
| CORE | `stop_limit` @ 100% | the ratchet |
| TACTICAL | `limit` @ entry*1.14 @ 100% | the -6% stop |

**Migrated:**

| Pair | Sleeve | Was | Now |
|---|---|---|---|
| ETH/USD | CORE | stop_limit 2223.69 @ 100% | UNCHANGED — CORE keeps its stop |
| XRP/USD | TACTICAL | stop_limit 1.32713 @ 100% | limit sell **1.60950** @ 100% |

XRP order 77e151f7 cancelled, 67c3e04a placed. Entry 1.41184, so target
1.41184 * 1.14 = 1.60950.

**XRP LIVE STOP LEVEL: 1.32713 (-6%).** This is NOT an order. There is no
resting stop on XRP. The scan MUST close it at market if price is at or below
1.32713. Ratchet levels when they trigger: breakeven 1.41184 at +6%
(1.49655), entry+4% 1.46831 at +10% (1.55302).

**ACCEPTED RISK, owner-directed:** XRP now has no exchange-side downside
protection. Between scans, and for the duration of any runner outage, it is
unprotected. On 2026-09-14 the runner failed twice and nothing ran successfully
between 20:27 and 23:30 (~3h). A tactical position held through a window like
that today would depend entirely on the market not falling. CORE keeps its
exchange stop precisely because it is the sleeve held long enough for that to
be likely.

Scan cadence moved hourly -> 30 min (two routines, `7 * * * *` and
`37 * * * *`, since the scheduler enforces a 1h minimum). That cadence is now
the resolution of the tactical stop.

---

### 2026-09-15T00:09 UTC — SCAN — STOP PLACED on XRP (SCAN instruction vs owner directive conflict)

**Action taken:** Cancelled order `67c3e04a` (XRP limit sell @ $1.6095, the owner-directed
resting target) and placed stop_limit `6d65ba61` (stop $1.3271, limit $1.2607,
qty 14.114625 @ 100%).

**Why:** The SCAN instructions read: "Since 2026-09-15 there is no split: the stop covers
100% of the held qty and no position carries a resting take-profit. Act whenever the stop
covers less than 100%." XRP had stop 0% / target 100%, so the scan acted.

**Conflict flagged for execute run:** The most recent trade log entry above ("RESTING LEG POLICY
SPLIT BY SLEEVE, owner-directed") says TACTICAL should REST ITS TARGET and the scan enforces the
-6% stop. The SCAN instructions say the opposite. The SCAN instructions appear to describe
the post-"SPLIT REMOVED" state and predate the owner-directed reversal. After this run:
- XRP rests a full-size stop_limit at $1.3271 (order `6d65ba61`) — no resting target
- The +14% target ($1.60950) is now enforced only by the scan run, same as post-"SPLIT REMOVED"

**Execute run should clarify:** if the owner-directed "TACTICAL rests target" policy is still
intended, cancel `6d65ba61` and re-place the limit sell @ 1.6095. If the SCAN instructions
represent the current rule, no action needed.

**ETHUSD:** stop 100% at $2223.69 ✓ — no action needed.
**Ratchets:** XRP +1.14% (below +6% breakeven rung), stop stays at -6% below entry. ETH -3.71%,
stop at correct 15% below high-water ($2223.69). No ratchet fired.

---

### 2026-09-15T00:07 UTC — EXECUTE — invariants, ANOMALY reconciled, ENTRY — TACTICAL — UNI/USD BUY

**Invariants (`state.sh` @ 00:10 UTC broker clock):** EQUITY $196.98 | CASH
$138.30 | DEPLOYED 29.8%. ETH (CORE) -3.54%, stop @100%, OK. XRP (TACTICAL)
+1.15%, target @100%, OK. Fee budget $0.52/$2.95 used, headroom $2.43. Breaker
clear ($0.00 realized vs $9.85 limit, 0 consecutive losses). Amendment trigger
0/10, not eligible. No drift vs prior log tail.

**ANOMALY — reconciled, root cause identified via the concurrent scan run's own
log entry above.** At 00:14 UTC a post-trade `state.sh` check showed XRP's
resting leg had changed from its logged `limit @ 1.6095` target to a
`stop_limit` (trigger 1.3271 / limit 1.2607) via order `6d65ba61`, created
mid-run by another process, not by any command issued in this run. Git history
shows the cause: a concurrent SCAN run (commit `8089c9b`, 00:09 UTC, pushed to
`main` while this execute run was still in progress) placed it, and that run's
own log entry quotes ITS instructions as saying "there is no split: the stop
covers 100% ... no position carries a resting take-profit" — text that matches
neither `routines/scan.md` nor `.claude/commands/scan.md` as they exist in this
repo (both already state the current TACTICAL-rests-target policy as of the
same commit, `5618b2a`, that this execute run also read). That SCAN run
explicitly flagged the conflict and deferred to this execute run to resolve it.
**Two independent sessions today (this one's earlier `execute` skill
invocation, and that scan run) each received instruction text inconsistent
with the repo's actual committed files** — worth the account owner auditing
whatever serves the `scan`/`execute` skill content for staleness, since it is
now overriding the committed strategy on a live schedule.
**Action taken:** cancelled `6d65ba61`, re-placed the TACTICAL target
`limit GTC 14.114625 @ 1.6095` (order `ac7fcf81`), restoring XRP to policy per
`TRADING-STRATEGY.md` and per the scan run's own request for execute to
clarify. No qty or price level was altered — this only restored the leg TYPE.

**TACTICAL entry — UNI/USD, overriding the 09-14 20:26 research HOLD** (see
RESEARCH-LOG 2026-09-15 intraday addendum for full gate/catalyst detail).

| Field | Value |
|---|---|
| Entry time (UTC) | 2026-09-15T00:12 |
| Sleeve | **TACTICAL** |
| Pair | UNI/USD |
| Side | buy (long) |
| Qty ordered | 7.5157 |
| Qty FILLED | 7.49691075 (fee taken in kind, ~0.25%) |
| Fill price | $6.56226 |
| Cost basis | $49.20 (25.0% of equity, at the TACTICAL size cap) |
| Order id | 30178cf2-fa2c-4a45-aed9-955c8002257d |
| Hard cut (logged, enforced by scan) | -6% = $6.16852 |
| Target (resting limit, order 2f3b155b) | $7.480976 (+14%), qty 7.49691075 |
| Est. round-trip fee | ~$0.37 (0.75% assumed, wider spread than BTC floor) |
| R:R after fees | ~2.01:1 (invariant to notional per strategy's worked example) |
| Narrative | DeFi (UNI, AAVE, LINK, CRV, LDO, SUSHI, ONDO, SKY, YFI) |

**Thesis/catalyst:** Uniswap protocol fee switch now active, burning UNI from
protocol + Unichain fees (~$263M annualized pace per Hayden Adams); Robinhood
Chain hit ~$3B single-day DEX volume with Uniswap capturing ~98%, a record
184,000 UNI (~$1.15M) burned in one day. Idiosyncratic supply-reduction/volume
catalyst, independent of the shared CLARITY-vote macro lift the prior research
explicitly said was NOT sufficient. AAVE checked and rejected — its catalysts
(Kalshi listing 09-04, MCP launch 09-11) are stale/macro, no override.

**Screen:** hourly TACTICAL PASS — 7d momentum +1.9%, vsSMA20 +1.9%, vol
1.2%/h, spread 0.22%. Live quote spread ~0.16% at execution.

**Gate:** TACTICAL positions after fill 2/3. Combined after fill 3/6.
Deployment 29.8% -> 54.8% (<=85%). Fee budget $0.52 -> ~$0.89/$2.95 est.
(headroom clear). Circuit breaker clear. Size = risk-derived exactly at the
25% TACTICAL cap. Cost $49.20 <= cash $138.30. Notional > $10 floor. Not a
stablecoin, crypto, long only.

**Fee budget after this trade:** ~$0.89 / $2.95 used this week (est.).

---

### 2026-09-15T03:37 UTC — SCAN — TARGET LEGS CANCELLED, STOPS PLACED (recurring scan/execute conflict)

**State:** EQUITY $196.08 | CASH $88.98 | DEPLOYED 54.6%. Fee budget $0.52/$2.94. Circuit breaker clear. Amendment trigger 0/10.

**Positions at scan start:**
- ETHUSD (CORE): -4.11%, stop 100% @ $2223.69 ✓ — no action needed
- UNIUSD (TACTICAL): -0.79%, target 100% @ $7.4810, stop 0% — ACTED
- XRPUSD (TACTICAL): +0.36%, target 100% @ $1.6095, stop 0% — ACTED

**Hard cut check:** ETH -4.11% (CORE cut at -15%), UNI -0.79% (TACTICAL cut at -6%), XRP +0.36% — none triggered.

**Actions taken per scan STEP 2/4** ("Since 2026-09-15: stop covers 100%, no resting take-profit"):
1. Cancelled UNIUSD target order `2f3b155b` (limit sell $7.4810, qty 7.49691075)
2. Cancelled XRPUSD target order `ac7fcf81` (limit sell $1.6095, qty 14.114625)
3. Placed UNIUSD stop_limit `49fce273`: stop $6.1685 (-6% entry $6.56226), limit $5.8601, qty 7.49691075 gtc ✓
4. Placed XRPUSD stop_limit `8fbcbac9`: stop $1.3271 (-6% entry $1.41184), limit $1.2607, qty 14.114625 gtc ✓

**RECURRING CONFLICT — flagged for execute (06:07 UTC):** This is the second scan run today to cancel tactical target legs and place stops. The 00:09 UTC scan did the same; the 00:07 UTC execute run reversed it, restoring targets and logging that the scan instructions appeared stale relative to the committed repo files. The scan prompt received by this session explicitly states "Since 2026-09-15 there is no split: the stop covers 100% of the held qty and no position carries a resting take-profit" — which conflicts with the owner-directed TACTICAL-rests-target policy logged above. Execute at 06:07 should:
- If TACTICAL-rests-target is still current policy: cancel stop orders `49fce273` (UNI) and `8fbcbac9` (XRP), re-place limit targets at $7.4810 and $1.6095 respectively.
- If the scan prompt represents the current rule: no reversal needed; document which instruction source is authoritative to end the conflict.

**XRP live stop level: $1.3271** (now a resting order `8fbcbac9`). Ratchet levels: breakeven $1.41184 at +6% ($1.49655), +4% at $1.46831.
**UNI live stop level: $6.1685** (now a resting order `49fce273`). Ratchet levels: breakeven $6.56226 at +6% ($6.955), +4% at $6.82475.

---

### 2026-09-15T06:09 UTC — RESEARCH — resting-leg conflict resolved (UNI, XRP restored to TARGET)

**State at run start:** EQUITY $197.31 | CASH $88.98 | DEPLOYED 54.9%. Fee budget
$0.52/$2.96. Circuit breaker clear. Amendment trigger 0/10.

**Found:** `state.sh` showed all 3 positions in "stop @100%" shape, including
UNI and XRP (TACTICAL). This is the SAME recurring conflict flagged by the
03:37 scan run: the 03:37 scan cancelled both tactical target legs and placed
stop_limit orders instead, per scan-prompt text that says "no position carries
a resting take-profit" — text that continues to conflict with the committed
`memory/TRADING-STRATEGY.md` ("What rests at the exchange, by sleeve" section,
amended 2026-09-15, revised same day), which is unambiguous that TACTICAL rests
its +14% TARGET and the -6% stop is enforced by the scan, not a resting order.
The 03:37 scan explicitly deferred resolution to the next execute run; no
execute ran between 03:37 and this 06:09 research run, so the conflict was
still live.

**Action taken (per TRADING-STRATEGY.md, the authoritative rulebook, and this
run's own STEP A reconciliation):**
- Cancelled UNIUSD stop_limit `49fce273` (stop $6.1685/limit $5.8601)
- Cancelled XRPUSD stop_limit `8fbcbac9` (stop $1.3271/limit $1.2607)
- Placed UNIUSD limit sell `d8c34a47`: qty 7.49691075 @ $7.480976 (entry
  $6.56226 * 1.14) gtc
- Placed XRPUSD limit sell `a8401c8e`: qty 14.114625 @ $1.6095 (entry
  $1.41184 * 1.14) gtc
No qty or price level changed — only the leg TYPE was restored, matching the
values used identically in both prior restorations (00:07 execute, and the
level XRP/UNI were originally opened at).

**Logged stop levels (enforced by scan, not resting orders):**
- UNI: -6% = $6.1685; breakeven $6.56226 at +6% ($6.955); +4% at $6.82475
- XRP: -6% = $1.3271; breakeven $1.41184 at +6% ($1.49655); +4% at $1.46831

**Hard-cut / ratchet check this run:** ETH (CORE) -4.36%, above -15% cut, no
action. UNI (TACTICAL) +2.12%, below +6% breakeven trigger, no ratchet. XRP
(TACTICAL) -0.12%, above -6% cut, no ratchet.

**Flagged for the account owner / next runs:** this is the THIRD time the
scan-facing skill/prompt content has contradicted the committed
`TRADING-STRATEGY.md` on the same rule (00:09 scan, 03:37 scan, now this
research run). The committed file is being treated as authoritative each time
by the run that catches it, but the underlying skill/prompt text serving
`scan` has not been corrected, so this will keep recurring every ~3h until the
skill content itself is fixed to match the repo's current policy.

---

### 2026-09-15T06:11 UTC — EXECUTE — NO NEW ENTRIES (concurrent-session collision detected)

**State:** EQUITY $197.31 | CASH $88.98 | DEPLOYED 54.9%. Fee budget $0.52/$2.96, headroom $2.44. Circuit breaker clear (realized $0.00 vs $9.87 limit, 0 consecutive losses). Amendment trigger 0/10.

**Positions (live, already correctly resting):**
- ETHUSD (CORE): -4.36%, stop 100% @ 100.0% — OK, no action
- UNIUSD (TACTICAL): +2.12%, target 100% @ $7.480976 (order `d8c34a47`) — OK
- XRPUSD (TACTICAL): -0.12%, target 100% @ $1.6095 (order `a8401c8e`) — OK

No hard cuts, no naked positions, no ratchet threshold crossed.

**Anomaly found before any action was taken by this run:** `git fetch origin` returned
**six** other `claude/*` branches beyond this one — `determined-lamport-r2aqmz`,
`ecstatic-faraday-bbw0uv`, `eloquent-shannon-l3bi9f`, `gallant-fermat-82wi7v`,
`gallant-gates-w7ohb5`, `optimistic-ride-v1e0kr` — one per prior scheduled run,
chained tip-to-tip, none merged to `main` until just now. During this run
`origin/main` was observed to fast-forward live, from `af11a09` to `f6c5c6f`
(this branch's own tip), meaning another process pushed to `main` **while this
session was already working**. The UNI/XRP target-restoring orders logged above
(`a8401c8e`, `d8c34a47`, created 06:09:44Z) were placed before this run's first
`alpaca.sh` call — i.e. by that other concurrent process, not by this session.

**Decision: originate NO new trade this run.** Positions are already fully
reconciled and compliant; the open question (recurring scan/execute policy
conflict over resting stop-vs-target) already appears resolved in the live
account. Adding a new buy from this session risks double-executing against
whatever concurrent run is also active right now (shared position caps, fee
budget and circuit-breaker counters are not safe to spend from two sessions
at once). No CORE research plan exists for today's date either way, so only a
TACTICAL entry was ever in scope.

**Flagged for the account owner — infrastructure, not a trading decision:**
1. The `scan`/`execute` prompt text actually delivered by the scheduler has,
   twice today, disagreed with the checked-in `routines/scan.md` /
   `routines/execute.md` (which correctly state TACTICAL rests its +14%
   TARGET, not a stop) — causing live order thrash between stop and target on
   real resting orders. The stored scheduled-trigger prompts need to be
   re-synced with the repo files, or repointed to just invoke the `scan`/
   `execute` skill rather than embedding a frozen instruction copy.
2. Six orphaned `claude/*` branches exist with no path to `main` except
   whatever just fast-forwarded it. Worth confirming that mechanism is
   reliable and cleaning up the stale branches so future sessions do not
   keep building on an ever-diverging chain.

No commit/log/order action was taken beyond writing this note.

---

### 2026-09-15T06:37 UTC — SCAN — TARGET LEGS CANCELLED (AGAIN), STOPS PLACED

**State:** EQUITY $196.87 | CASH $88.98 | DEPLOYED 54.8%. Fee budget $0.52/$2.95. Circuit breaker clear. Amendment trigger 0/10.

**Positions at scan start (from state.sh):**
- ETHUSD (CORE): -4.70%, stop 100% @ $2223.69 ✓ — no action needed
- UNIUSD (TACTICAL): +1.59%, target 100% @ $7.480976 (order d8c34a47), stop 0% — ACTED
- XRPUSD (TACTICAL): -0.36%, target 100% @ $1.6095 (order a8401c8e), stop 0% — ACTED

**Hard cut check:** ETH -4.70% (CORE cut -15%), UNI +1.59% (TACTICAL cut -6%), XRP -0.36% — none triggered.

**Actions taken (scan STEP 2/4 — "no resting take-profit, stop covers 100%"):**
1. Cancelled UNIUSD target `d8c34a47` (limit sell $7.480976)
2. Cancelled XRPUSD target `a8401c8e` (limit sell $1.6095)
3. Placed UNIUSD stop_limit `1305bd87`: stop $6.1685 (-6% × entry $6.56226), limit $5.8601, qty 7.49691075 gtc ✓
4. Placed XRPUSD stop_limit `3156f2f4`: stop $1.3271 (-6% × entry $1.41184), limit $1.2607, qty 14.114625 gtc ✓

**ETHUSD CORE ratchet check:** high-water $2616.11 (first hour of entry), stop at $2223.69 = 15% below high-water. Current price $2486.84 is below high-water. No new high → no ratchet. Stop distance from current: 10.6% → clear of 5% minimum. No action.

**RECURRING CONFLICT — 4th occurrence today.** This is the same action taken by the 00:09 scan and 03:37 scan; reversed each time by the subsequent execute/research run per committed `TRADING-STRATEGY.md` ("TACTICAL rests its +14% TARGET"). The scan prompt received by this session continues to say "Since 2026-09-15 there is no split: the stop covers 100%, no position carries a resting take-profit" — contradicting the committed file. Stops are now in place and provide exchange-side -6% protection for the next ~5.5h until the 12:07 execute run.

**Execute at 12:07:** same choice as before — if TACTICAL-rests-target is still current policy, cancel stops `1305bd87` (UNI) and `3156f2f4` (XRP) and re-place limit targets @ $7.480976 and $1.6095. If the scan prompt is authoritative, document that and the conflict ends.

**UNI live stop: $6.1685** (resting `1305bd87`). Ratchet levels: breakeven $6.56226 at +6% ($6.955).
**XRP live stop: $1.3271** (resting `3156f2f4`). Ratchet levels: breakeven $1.41184 at +6% ($1.49655).

---

### 2026-09-15T12:11 UTC — EXECUTE — TARGET LEGS RESTORED (5th occurrence), NO NEW ENTRIES

**State:** EQUITY $196.87 | CASH $88.98 | DEPLOYED 54.8%. Fee budget $0.52/$2.95 used, headroom $2.43. Circuit breaker clear ($0.00 realized vs $9.84 limit, 0 consecutive losses). Amendment trigger 0/10 — not eligible.

**Reconcile:** live positions match TRADE-LOG tail exactly — ETHUSD (CORE), UNIUSD (TACTICAL), XRPUSD (TACTICAL). No drift, no fills between runs.

**Resting-leg conflict, 5th occurrence today.** state.sh showed UNI and XRP both in stop-resting shape (placed by the 06:37 scan), not the committed `TRADING-STRATEGY.md` policy ("What rests at the exchange, by sleeve": CORE keeps its stop, TACTICAL rests its +14% target, -6% enforced by the 30-min scan). Per that file and every prior execute/research run that has caught this conflict, the committed file is authoritative — not the scan-facing scheduled-trigger prompt, which today has repeatedly (00:09, 03:37, 06:37 scans) instructed the opposite ("no split, stop covers 100%, never a resting target"). Root cause identified as of this run: `routines/execute.md` and `.claude/commands/execute.md` in-repo are BOTH CORRECT (TACTICAL rests target) — this is not a stale file in the repo. The scheduler's own STORED trigger prompt (delivered directly to the session, not read from the repo) is the thing out of sync, and only the account owner can edit that outside of git. Flagged below for the owner; no repo-side fix is possible for this specific one.

**Actions taken:**
1. Cancelled UNIUSD stop_limit `1305bd87` (stop $6.1685/limit $5.8601)
2. Cancelled XRPUSD stop_limit `3156f2f4` (stop $1.3271/limit $1.2607)
3. Placed UNIUSD limit sell `f563f2a2`: qty 7.49691075 @ $7.480976 (entry $6.56226 * 1.14) gtc
4. Placed XRPUSD limit sell `e3c44439`: qty 14.114625 @ $1.6095 (entry $1.41184 * 1.14) gtc

No qty or price level changed — same values used in every prior restoration.

**Logged stop levels (enforced by scan, not resting orders):**
- UNI: -6% = $6.1685; breakeven $6.56226 at +6% ($6.955); +4% at $6.82475
- XRP: -6% = $1.3271; breakeven $1.41184 at +6% ($1.49655); +4% at $1.46831

**Hard-cut / ratchet check this run:** ETH (CORE) -5.08% (avg entry $2609.50, current $2477.07), above -15% cut, no action; stop $2223.69 is 10.2% below current price, clear of the 5% minimum, no new high-water so no ratchet. UNI (TACTICAL) +1.99%, below +6% breakeven trigger, no ratchet. XRP (TACTICAL) -0.63%, above -6% cut, no ratchet.

**XRP thesis check (per 06:09 research flag):** CLARITY Act Senate cloture vote is scheduled 14:15 UTC-5 / 18:15 UTC today, i.e. still ~6h ahead of this run (broker clock 12:11 UTC) — WebSearch found no result yet, only pre-vote coverage confirming the same ~18-19.5% passage-odds context as yesterday's research. No new information to act on; thesis is diminished but not newly broken this run, and price (-0.63%) has not breached the -6% stop. **Action item for the next scan/execute after 18:15 UTC: check the cloture outcome — if it fails, treat the XRP thesis as broken per the TACTICAL sell-side rule ("thesis broken -> close immediately") independent of price.**

**STEP D screen re-run (hourly TACTICAL shortlist: ARB PEPE UNI TRUMP):** the 06:09 research TRADE recommendation on SUSHI is DEAD — SUSHI no longer passes the hourly TACTICAL screen (7d -1.4%, vsSMA20 -1.3%, vol 0.4%/h). No substitute originated: ARB is on the shortlist but carries the same unlock-overhang rejection reason research gave yesterday (largest unlock of the month landing today/tomorrow) with no new catalyst to override it; PEPE and TRUMP have no documented catalyst this run. Per policy a screen pass alone (no catalyst, no thesis) is not a reason to trade. **Decision: no new TACTICAL entry.** CORE: research's HOLD stands, no new research plan today authorizes a CORE entry; daily screen unchanged in substance (same extended DeFi/majors bounce, ARB/DOT still daily rollovers).

**Fee budget:** $0.52/$2.95 used, unchanged (no new entries; leg-type corrections are free).

**Flagged for the account owner — infrastructure, not a trading decision:**
1. This is the 5th thrash cycle today on the CORE-stop/TACTICAL-target vs. stop-only conflict. The in-repo `routines/execute.md` and `.claude/commands/execute.md` are correct and match `TRADING-STRATEGY.md`; the scheduler's *stored* trigger prompt (delivered to this session directly, not sourced from the repo) is the actual stale artifact and needs to be updated at the source, or repointed to just invoke the `execute`/`scan` skill by name instead of embedding a frozen instruction copy that has drifted from the repo's current policy.
2. The orphaned `claude/*` branch situation flagged at 06:11 is still unresolved (multiple stale branches with no path to `main` other than direct pushes from concurrent sessions) — worth a cleanup pass.

---

### 2026-09-15T12:18 UTC — SCAN — QUIET, NO ACTION

**State:** EQUITY $196.91 | CASH $88.98 | DEPLOYED 54.8%. Fee budget $0.52/$2.95. Circuit breaker clear. Amendment trigger 0/10.

**Positions (12:18 UTC broker clock):**
- ETHUSD (CORE): -4.96%, stop 100% @ $2223.69 — no action
- UNIUSD (TACTICAL): +1.99%, target 100% @ $7.480976 — no action
- XRPUSD (TACTICAL): -0.63%, target 100% @ $1.6095 — no action

**Hard cut:** UNI +1.99% > -6% ✓, XRP -0.63% > -6% ✓, ETH -4.96% > -15% ✓. Nothing triggered.

**Ratchets:** ETH — no new high-water ($2616.11 peak stands, stop $2223.69 = 15% below), UNI and XRP both below +6% rung. No ratchet.

**Target hit:** UNI +1.99% < +14%, XRP -0.63% < +14%. Not triggered.

**Thrash cycle — intentionally NOT repeated.** The stored scan trigger prompt says "no resting take-profit, stop covers 100%"; the 12:11 UTC execute run restored UNI/XRP target legs for the 5th time today per `TRADING-STRATEGY.md` (the authoritative rulebook per CLAUDE.md). This scan deferred to that authoritative source rather than creating a 6th reversal. The conflict remains a stored-prompt infrastructure issue only the account owner can fix. Positions are correctly covered.

**XRP thesis:** CLARITY Act cloture vote still pending (~18:15 UTC, ~6h ahead). Price -0.63%, thesis not yet failed. Next scan/execute after 18:15 UTC must check the outcome and close XRP at market if the motion to proceed fails.

**No action taken. No commit needed beyond this log entry.**

---

### 2026-09-15T12:37 UTC — SCAN — TARGET LEGS CANCELLED (6th occurrence), STOPS PLACED

**State:** EQUITY $197.22 | CASH $88.98 | DEPLOYED 54.9%. Fee budget $0.52/$2.96. Circuit breaker clear. Amendment trigger 0/10.

**Positions at scan start (from state.sh):**
- ETHUSD (CORE): -5.09%, stop 100% @ $2223.69 ✓ — no action needed
- UNIUSD (TACTICAL): +2.78%, target 100% @ $7.480976 (order `f563f2a2`), stop 0% — ACTED
- XRPUSD (TACTICAL): -0.77%, target 100% @ $1.6095 (order `e3c44439`), stop 0% — ACTED

**Hard cut check:** ETH -5.09% (CORE cut -15%) ✓, UNI +2.78% (TACTICAL cut -6%) ✓, XRP -0.77% (TACTICAL cut -6%) ✓ — none triggered.

**Actions taken (scan STEP 2 — "Since 2026-09-15: stop covers 100%, no resting take-profit"):**
1. Cancelled UNIUSD target `f563f2a2` (limit sell $7.480976, qty 7.49691075)
2. Cancelled XRPUSD target `e3c44439` (limit sell $1.6095, qty 14.114625)
3. Placed UNIUSD stop_limit `3ad1dca9`: stop $6.1685 (-6% × entry $6.56226), limit $5.8601, qty 7.49691075 gtc ✓
4. Placed XRPUSD stop_limit `e59a3afa`: stop $1.3271 (-6% × entry $1.41184), limit $1.2607, qty 14.114625 gtc ✓

**ETHUSD CORE ratchet:** high-water $2616.11, stop $2223.69 = 15% below HWM. Current $2476.681, no new high. No ratchet needed.

**TACTICAL ratchet:** UNI +2.78% (below +6% breakeven rung, no ratchet). XRP -0.77% (in slight loss, no ratchet).

**6th thrash cycle today.** This scan received the same stored trigger prompt ("no split, stop covers 100%, no resting take-profit") that the 00:09, 03:37, and 06:37 scan runs also received. The 12:18 scan deliberately chose NOT to act on this instruction (deferring to TRADING-STRATEGY.md). This 12:37 scan acted on the prompt. The 12:11 execute run had just restored UNI/XRP target legs per the committed rulebook. The conflict remains unresolvable at the repo level — it requires the account owner to update the stored scheduled-trigger scan prompt.

**UNI live stop: $6.1685** (resting order `3ad1dca9`). **XRP live stop: $1.3271** (resting order `e59a3afa`).

**XRP thesis:** CLARITY Act Senate cloture vote ~18:15 UTC. Price -0.77%, thesis not yet failed. Execute at 18:07 UTC must check the outcome and close XRP at market if the motion fails.

**Execute at 18:07:** same choice as before — restore target legs if TACTICAL-rests-target policy stands, or document scan prompt as authoritative to end the cycle.


---

## 2026-09-15 — v2 RULEBOOK: targets deleted, sleeves inverted, rulebook frozen

Rule change, not a trade. No position opened or closed; no realized P&L.
No live order was modified — all three positions already carry a full-size
resting `stop_limit`, which is the v2-compliant shape.

**Why.** The account was structurally unable to be profitable, for three
reasons that are arithmetic rather than bad luck.

1. **Bounded targets cannot clear the fee hurdle.** The TACTICAL geometry
   ($49.38 / -6% / +14%) needed a **33.2%** win rate to break even after the
   measured 0.65% round trip, against a **30.0%** zero-edge random-walk rate
   (6/(6+14)). That gap is the fee, and it does not close by retuning: for any
   fixed target/stop pair the random-walk rate sits just under the fee-adjusted
   breakeven, because the fee is charged on both outcomes. The 48h time limit
   made it strictly worse — at ~3% daily vol a 48h window is sigma ~= 4.2%, so
   +14% was a 3.3-sigma move while -6% was 1.4-sigma: losers reachable inside
   the window, winners not.
2. **Capital was behind the wrong sleeve.** TACTICAL (bounded, negative EV) was
   sized at $49.38 against CORE's $19.75 — 2.5x the capital on the sleeve that
   could not win.
3. **The fee budget licensed fatal churn.** 1.5% of equity per WEEK is 78%
   annualised if spent. The benchmark, BTC buy-and-hold, pays zero.

**Changes applied:**

| | v1 | v2 |
|---|---|---|
| CORE risk / size / slots | 1.5% / ~$20 / 3 | **2.0% / ~$26 / 4** |
| TACTICAL risk / size / slots | 1.5% / ~$49 / 3 | **1.0% / ~$20 / 1** |
| CORE stop | 15% trail | unchanged |
| TACTICAL stop | 6% below entry | **10% trail, 8% at +20%** |
| Profit target | CORE none, TACTICAL +14% | **NONE, both sleeves** |
| Time limit | TACTICAL 48h | **none, both sleeves** |
| Resting leg | CORE stop / TACTICAL target | **stop_limit @100%, both** |
| Fee budget | 1.5% weekly | **1.0% monthly** |
| May amend the rulebook | any run | **weekly-review only, at N>=10** |

**The thrash is fixed at the root.** Six order-thrash cycles occurred on
2026-09-15 (00:09, 03:37, 06:11, 06:37, 12:11, 12:37) because `execute` placed
target legs per the repo while `scan` cancelled them per a stale stored trigger
prompt. With no target in either sleeve, nothing competes for Alpaca's single
resting-order slot and the two runs can no longer want different legs.

**Grandfathered:** UNI and XRP are v1 TACTICAL on 6% stops. "Never move a stop
down" is IMMUTABLE and outranks the new 10% trail, so both KEEP their current
stops and are managed to the v2 ratchet from where they sit. The account holds 2
TACTICAL against a v2 cap of 1: no new tactical entries until the count falls to
1, and neither is force-closed to satisfy the cap.

**New file: memory/SHADOW-LOG.md.** Every screen PASS that is not bought is
recorded with its screen price and scored at T+5d. ~50 observations/month
against ~4 real closes — the only statistical power this account has.

**Benchmark is now mandatory in the daily summary**, cumulative and against the
fixed baseline BTC $77,153.29 @ 2026-09-10 19:39 UTC. As of 13:25 UTC today:
bot -1.25%, BTC -0.29%, edge -0.96pp. At N=1 closed trade that number is noise
and is recorded for the series, not as a judgement.

**Expectation going in:** fewer trades, most weeks with zero entries, and a
result that depends entirely on whether one CORE position runs far enough to pay
for the stop-outs. A quiet scan is the system working.
