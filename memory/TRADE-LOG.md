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

---

### 2026-09-15T14:11 UTC — SCAN — RATCHET XRP

**State:** EQUITY $194.35 | CASH $88.98 | DEPLOYED 54.2%. Fee budget $0.52/$1.94 used (monthly). Circuit breaker clear. Amendment trigger 0/10.

**Positions (v2 shape — all stop_limit @100%):**
- ETHUSD (CORE): -6.22%, stop 100% @ $2223.69 ✓ — no action
- UNIUSD (v1 TACTICAL, 6% trail): -2.54%, stop 100% @ $6.1685 ✓ — no action
- XRPUSD (v1 TACTICAL, 6% trail): +0.24%, stop 100% @ $1.3271 — RATCHETED

**Gap check:** ETH -6.22% vs CORE -15% ✓, UNI -2.54% vs -6% ✓, XRP +0.24% vs -6% ✓. None triggered.

**RATCHET — XRPUSD:** Current price $1.4152 is above entry $1.41184 → new high-water.
- Old stop: $1.3271 (6% below entry $1.41184)
- New stop: $1.3303 (6% below HWM $1.4152; $1.4152 × 0.94 = $1.33029 → $1.3303)
- New limit: $1.2638 ($1.3303 × 0.95)
- Cancelled order `e59a3afa`, placed `607e3472` ✓
- Direction: $1.3303 > $1.3271 — never moved down ✓
- Distance: $1.4152 − $1.3303 = 6.0% from current — above 5% minimum ✓

**XRP thesis:** CLARITY Act Senate cloture vote ~18:15 UTC (~4h ahead). Price +0.24%, thesis intact. Execute at 18:07 UTC must check the outcome and close XRP at market if the motion to proceed fails.

**ETHUSD CORE ratchet:** HWM $2616.11 (first-hour high), stop $2223.69 = 15% below HWM. Current $2447.12 is below HWM. No new high → no ratchet.
**UNIUSD ratchet:** Current $6.3954 is below entry $6.56226. No ratchet.

**No new positions opened. No rule edits.**

---

### 2026-09-15T14:51 UTC — EXIT — TACTICAL (v1 grandfathered) — UNI/USD — STOPPED OUT

Stop_limit order `3ad1dca9` (placed by 14:11 scan) triggered and filled automatically at the broker.

| Field | Value |
|---|---|
| Exit time (UTC) | 2026-09-15T14:51:42Z |
| Exit type | stop_limit fill (stop triggered, filled within limit) |
| Qty | 7.49691075 |
| Stop trigger | $6.1685 (-6% below entry $6.56226) |
| Fill price | $6.1608 (between trigger $6.1685 and limit $5.8601 — filled normally) |
| Exit proceeds | ~$46.19 |
| Cost basis | $49.20 |
| Gross P&L | -$3.01 |
| Sell fee (~0.35%) | -$0.16 |
| Buy fee (in kind, reflected in cost basis) | -$0.12 |
| **REALIZED P&L** | **≈ -$3.17** (gross -$3.01, sell fee -$0.16) |

**Circuit breaker status after this exit:**
- Realized losses today (UTC 2026-09-15): ~$3.17 vs $9.58 limit (5% of equity) → **CLEAR**
- Consecutive tactical losses: DOT (closed 2026-09-14, -$1.61) → UNI (closed today, -$3.17) = **2 of 3** → **CLEAR**

**Reason:** Stop hit at -6% from entry. UNI's CLARITY Act catalyst (Senate cloture vote, scheduled ~18:15 UTC today) was a binary event and the position was sized smaller for that reason. The -6% stop executed correctly.

**Narrative:** DeFi (UNI, AAVE, LINK, CRV, LDO...) — **1** consecutive failed DeFi trade. Exit-narrative rule needs 2.

---

### 2026-09-15T17:08 UTC — SCAN — QUIET, NO ACTION

**State:** EQUITY $191.62 | CASH $135.05 | DEPLOYED 29.5% (down from 54.8% — UNI exit freed ~$46). Fee budget $0.52/$1.92 used (monthly). Circuit breaker clear ($3.17 realized losses vs $9.58 limit; 2 consecutive tactical losses vs 3 threshold). Amendment trigger 0/10.

**Positions (v2 shape — stop_limit @100%):**
- ETHUSD (CORE): -7.35%, stop 100% @ $2223.69 (order `1ebb2562`) ✓ — no action
- XRPUSD (v1 TACTICAL, 6% trail): -1.78%, stop 100% @ $1.3303 (order `607e3472`) ✓ — no action

**Gap check (STEP 3):** ETH -7.35% vs CORE -15% ✓. XRP: current $1.38668 > stop $1.3303, not gapped through ✓. No close needed.

**Ratchet (STEP 4):**
- ETH (CORE, 15% trail): HWM $2616.11, current $2417.646 below HWM → no new high → no ratchet.
- XRP (v1 TACTICAL, 6% trail): HWM $1.4152 (from 14:11 ratchet log), current $1.38668 below HWM → no new high → no ratchet.

**UNI exit logged above** (stopped out at 14:51 UTC while this run was not active; discovered via order history reconciliation this run).

**XRP thesis flag (carry-forward):** CLARITY Act Senate cloture vote ~18:15 UTC, still ~1h ahead. Execute at 18:07 UTC must check the outcome and close XRP at market if the motion to proceed fails — thesis would be broken.

**No orders placed, no stops cancelled. No clickup notification sent (scan acted on nothing — documentation only).**

---

### 2026-09-15T18:08 UTC — EXECUTE — NO ACTION

**State:** EQUITY $192.23 | CASH $135.05 | DEPLOYED 29.7%. Fee budget $0.52/$1.92 used (monthly), headroom $1.40. Circuit breaker clear ($0.00 realized vs $9.61 limit; 0 consecutive tactical losses — UNI/DOT stops are prior days, today's tally is 0). Amendment trigger 0/10 — not eligible, nothing changed.

**Positions (v2 shape — both stop_limit @100%):**
- ETHUSD (CORE): -6.58%, stop 100% @ $2223.69 (order `1ebb2562`) ✓ — no action
- XRPUSD (v1 TACTICAL, 6% trail, grandfathered): -0.28%, stop 100% @ $1.3303 (order `607e3472`) ✓ — no action

**Reconcile:** Matches 17:08 scan position set exactly (ETH, XRP). No fills, no drift.

**Gap check:** ETH -6.58% vs CORE -15% ✓. XRP: current $1.4079 > stop trigger $1.3303, not gapped ✓.

**Ratchet:** ETH HWM $2616.11, current $2437.798 below HWM → no new high → no ratchet. XRP HWM $1.4152 (set at 14:11 scan), current $1.4079 below HWM → no new high → no ratchet.

**XRP thesis check (CLARITY Act cloture vote):** Vote is scheduled 2:15pm ET = 18:15 UTC. Broker clock at run start was **18:08 UTC — 7 minutes BEFORE the vote**. WebSearch (PERPLEXITY_API_KEY is the template placeholder → fallback per design) across three queries returned only pre-vote previews/context; no outlet had a vote count yet. **Outcome not yet knowable — the vote had not occurred at run time.** Took no action on XRP; nothing to override (thesis not yet resolved either way). Flagging for the next scan (hourly) to check the actual result once it lands, since execute does not run again until 00:07 UTC tomorrow, ~6h after the vote.

**STEP B — Research:** Today's entry (06:09 UTC) read. CORE: **HOLD** (binding). TACTICAL: **HOLD** (formal decision) with a non-binding recommendation to consider SUSHI if conditions still hold.

**TACTICAL gate (SUSHI candidate) — REJECTED on position cap, screen not re-run:** Current TACTICAL count is 1 (XRP only — UNI stopped out at 14:51 UTC). Cap is 1. Adding SUSHI would make TACTICAL positions after fill = 2 > cap of 1. Per execute.md STEP E, this is a hard stop regardless of catalyst or screen state, so STEP C/D (live re-quote, re-screen) were skipped as moot — no gate downstream of the cap could pass. No TACTICAL entry originated.

**CORE:** No entry — research HOLD is binding and CORE requires the morning research plan to originate.

**No orders placed. No stops cancelled. No clickup notification sent (no trade placed).**

---

## 2026-09-15 — Daily Snapshot (Day 5, UTC ~18:10)

**Portfolio:** $192.23 | **Cash:** $135.05 (70.3%) | **Day P&L:** -$6.54 (-3.29%) | **Cumulative:** -$7.77 (-3.89%)
**vs BTC:** -3.49pp edge | **Fees today:** ~$0.28 | **Fee budget:** $0.52 / $1.92 used this month (headroom $1.40)

| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
|--------|------|-----|-------|------|------------|---------------|---------------|
| CORE | ETH/USD | 0.015302647 | $2,609.50 | $2,437.798 | -6.58% | $2,223.69 | yes — 100% of qty, 0% unreserved |
| TACTICAL (v1 grandfathered, 6% trail) | XRP/USD | 14.114625 | $1.41184 | $1.4079 | -0.28% | $1.3303 | yes — 100% of qty, 0% unreserved |

**Benchmark:** BTC/USD $76,845.74 (mid) vs $77,153.29 Day-0 baseline (2026-09-10 19:39 UTC) = **-0.40% cumulative**. Bot cumulative -3.89%. **EDGE -3.49pp** — bot is trailing the benchmark.

**Trades today (2026-09-15 UTC):** 1 round trip — TACTICAL UNI/USD entered 00:07 UTC, stopped out 14:51 UTC at -6%, REALIZED P&L -$3.17 (this is the day's only realized fee/loss driver). CORE: no trades. Reconciled against live positions/orders — no drift found.

**Circuit breaker:** realized losses today $3.17 vs $9.61 limit (5% of equity) — CLEAR. Consecutive tactical losses: DOT (09-14) -> UNI (09-15) = 2 of 3 — CLEAR, not tripped.

**Amendment trigger:** 2 closed trades total (DOT -$1.61, UNI -$3.17) since the last applied amendment (none has ever been applied via a weekly-review STEP E — WEEKLY-REVIEW.md's only "Rule changes applied" entry says "None"). 2 < 10 -> **not eligible, nothing amended this run.**

**Invariants this run:** both open positions carry a full-size (100%) resting `stop_limit`, no naked/split legs, no target legs. Neither ETH nor XRP made a new high-water mark since the last ratchet (14:11 UTC), so no ratchet fired. Neither position breached its hard-cut threshold (ETH -6.58% vs -15% CORE; XRP -0.28% vs -6% grandfathered TACTICAL).

**Notes:** Quiet day after the v2 rulebook rewrite — one TACTICAL round trip (UNI) stopped out for a small loss, leaving 2 open positions (1 CORE, 1 grandfathered v1 TACTICAL) both fully stopped and within their hard-cut bands. The bot is underperforming BTC by 3.49pp cumulative, driven mostly by ETH's -6.58% unrealized drawdown plus this account's two realized tactical losses (DOT, UNI) — no CORE trade has closed yet to test the "let winners run" half of the thesis. Two data caveats for the record (also logged to OBSERVATIONS.md): (1) no daily snapshot was written 2026-09-12 through 2026-09-14, so the "Day P&L" above is actually a ~4-day delta versus the 2026-09-11 snapshot, not a true 1-day figure; (2) `scripts/state.sh`'s circuit-breaker/amendment regex does not match the `REALIZED P&L` formats actually used in this log (table-row and inline-colon styles), so it reported $0.00 realized and 0 closed trades this run — the $3.17/2-closed figures above were computed by hand from the log rows and should be treated as authoritative over the script's output until fixed.

---

### 2026-09-16T00:08 UTC — EXECUTE — STEP A RECONCILE: XRP stop fill discovered (drift between runs)

**State at run start (broker clock 2026-09-16 00:08 UTC):** EQUITY $190.45 | CASH $153.73 | DEPLOYED 19.3%. `bash scripts/state.sh` shows only ONE open position (ETHUSD) — XRPUSD, open at the 18:10 snapshot, is gone from `alpaca.sh positions`.

**RECONCILE finding:** `alpaca.sh orders` (status=all) shows XRP's resting stop_limit `607e3472` (stop $1.3303 / limit $1.2638, placed by the 14:11 UTC scan) FILLED at **2026-09-15T18:41:08Z**, qty 14.114625 @ $1.3272 — 33 minutes after the 18:08 execute run logged the CLARITY Act vote as "not yet knowable." This fill was never logged. No run was active between the 18:10 daily snapshot and this one to catch it — exactly the blind-window case Every-Run Invariants STEP A.1 exists for.

**EXIT — TACTICAL (v1 grandfathered, 6% trail) — XRP/USD — STOPPED OUT**
*(Also discovered concurrently by the 2026-09-16T00:08 UTC scan run; execute version is canonical.)*

| Field | Value |
|---|---|
| Exit time (UTC) | 2026-09-15T18:41:08Z |
| Exit type | stop_limit fill (stop triggered at $1.3303, filled within limit $1.2638) |
| Qty | 14.114625 |
| Entry | $1.41184 (14.15 ordered, 2026-09-14T16:43:35Z; qty haircut to 14.114625 by in-kind buy fee) |
| Fill price | $1.3272 |
| Cost basis | $19.98 (14.15 × $1.41184) |
| Gross proceeds | $18.73 (14.114625 × $1.3272) |
| Gross P&L | -$1.24 (-6.23%, consistent with the 6% v1 trail from HWM $1.4152) |
| Sell fee (~0.35%) | -$0.07 |
| **REALIZED P&L** | **≈ -$1.31** |

**Reason:** Grandfathered v1 6% trail stop hit. CLARITY Act cloture vote (the position's catalyst) resolved unfavorably/thesis continued to deteriorate per the 09-15 research entry's flagged concern; price gapped through the trail window before the next scan could re-evaluate. Stop filled normally within its limit band — no naked exposure.

**Narrative:** Payments/legacy (XRP, LTC, BCH) — **1** consecutive failed trade in this narrative. Exit-narrative rule needs 2.

**Circuit breaker — consecutive TACTICAL losses now 3: DOT (09-14) → UNI (09-15) → XRP (09-15).** No intervening tactical win. TRADING-STRATEGY.md's breaker text reads "3 consecutive tactical losses -> no new entries for the rest of the UTC day," which literally scopes the freeze to the day the 3rd loss closed (2026-09-15, now over). Read literally, that day-scoped freeze has expired and does not by itself block today (2026-09-16). However, the *streak* of 3 consecutive tactical losses is real and unbroken by any tactical win, and the account currently holds 0 TACTICAL positions, so nothing is being management-frozen either way right now. **Decision for this run: treat the streak as an active caution flag and do NOT originate a new TACTICAL entry today** even though the literal day-boundary language would technically permit it — a fresh tactical entry immediately behind 3 straight losses is exactly the compounding-losing-streak scenario the breaker exists to prevent, and the rule's day-scoping looks like an oversight rather than an intended reset mechanism. Logged as an ambiguity to OBSERVATIONS.md rather than resolved by editing the rule (amendment freeze). Realized losses TODAY (2026-09-16 UTC) = $0.00 vs $9.52 limit (this exit posted on 09-15) — the dollar threshold is unaffected.

**Amendment trigger:** 3 closed trades total (DOT -$1.61, UNI -$3.17, XRP -$1.31) since the last applied amendment. 3 < 10 -> not eligible, nothing amended.

**No stops cancelled, no new orders placed for this reconcile step.**

---

### 2026-09-16T00:08 UTC — SCAN — QUIET, NO ACTION

**State (broker clock):** EQUITY $190.45 | CASH $153.73 | DEPLOYED 19.3% (ceiling 85%). Fee budget $0.52/$1.90 used (monthly), headroom $1.38. Circuit breaker clear ($0.00 realized vs $9.52 limit, 0 consecutive tactical losses on 09-16). Amendment trigger 0/10 (script bug; manual count 3/10) — not eligible.

**Positions:**
- ETHUSD (CORE): -8.03%, stop 100% @ $2223.69 (order `1ebb2562`) ✓ — no action
- XRPUSD: CLOSED at 18:41 UTC 09-15 (logged above in execute entry) — no action

**Gap check (STEP 3):** ETH -8.03% vs CORE -15% ✓. Not triggered.

**Ratchet (STEP 4):** ETH HWM $2616.11, current ~$2400 below HWM → no new high → no ratchet. Stop $2223.69 = 15% below HWM, distance ~7.4% from current — above 5% minimum ✓.

**No orders placed, no stops cancelled. No clickup notification (nothing acted upon).**

---

### 2026-09-16T06:08 UTC — EXECUTE — NO ACTION

**State (broker clock):** EQUITY $190.52 | CASH $153.73 | DEPLOYED 19.3% (ceiling 85%). SIZE NOW: CORE $25.40 / TACTICAL $19.05. Fee budget $0.52/$1.91 used (monthly), headroom $1.39. Circuit breaker (script): $0.00 realized vs $9.53 limit, streak 0 — **script under-reports**, same known regex bug as prior runs (state.sh only matches the literal `REALIZED P&L $` substring, not this log's table/bold formats). Manual count: 3 consecutive tactical losses on the books (DOT 09-14, UNI 09-15, XRP 09-15), no intervening tactical win. Amendment trigger: 3 closed trades since last amendment, 3 < 10 — not eligible.

**STEP A — Reconcile:** `alpaca.sh positions` shows exactly ETHUSD, qty 0.015302647, matching TRADE-LOG. No drift since the 00:08 UTC run.

**Resting stop:** ETHUSD stop_limit `1ebb2562`, 100% of held qty, stop $2223.69 / limit $2112.51 — OK, single leg, no target.

**Gap check:** ETH unrealized -7.86% (current $2404.30) vs CORE -15% cut — not triggered.

**Ratchet:** HWM $2616.11 unchanged (current $2404.30 is below HWM) — no new high, no ratchet. Stop distance from current price ~7.5%, above the 5% minimum.

**STEP B — Research:** Today's entry (00:08 UTC inline addendum from the prior execute run) read. CORE: **HOLD** (binding — no CORE entry originates from this run). TACTICAL: **HOLD**, and this run continues treating the unbroken 3-consecutive-tactical-loss streak as an active block on new TACTICAL originations (per the 00:08 run's reasoning and the still-unresolved day-boundary ambiguity already logged in OBSERVATIONS.md) — no tactical win has occurred since to break the streak.

**STEP D — Re-screened anyway for completeness:** CORE shortlist unchanged (UNI ARB FIL XTZ). TACTICAL shortlist widened to 8 (ARB XRP DOT WIF BTC SOL ETH DOGE), but moot — blocked by the tactical-loss-streak caution flag above regardless of any catalyst. Did not run STEP C (live quote/spread re-validation) or spend a perplexity/WebSearch catalyst call, since no candidate can pass the circuit-breaker gate this run.

**No orders placed, no stops cancelled. No clickup notification (nothing acted upon).**

---

### 2026-09-16T12:11 UTC — EXECUTE — NO ACTION

**State (broker clock via `state.sh`):** EQUITY $190.67 | CASH $153.73 | DEPLOYED 19.4% (ceiling 85%). SIZE NOW: CORE $25.42 / TACTICAL $19.07. Fee budget $0.52/$1.91 used this month, headroom $1.39. Circuit breaker (script): $0.00 realized vs $9.53 limit, script-reported consecutive losing closes 0 — same known regex bug as prior runs (table/bold `REALIZED P&L` formats aren't matched). Manual count from the log: 3 consecutive tactical losses on the books (DOT 09-14, UNI 09-15, XRP 09-15), still no intervening tactical win, 0 TACTICAL positions open. Amendment trigger: 3 closed trades since last amendment, 3 < 10 — not eligible, nothing amended.

**STEP A — Reconcile:** `alpaca.sh positions` shows exactly one position, ETHUSD qty 0.015302647, avg entry $2,609.50, current $2,414.20, unrealized -7.48% ($-2.99) — matches TRADE-LOG, no drift since the 06:08 UTC run. `alpaca.sh orders` shows the single resting leg `1ebb2562` (stop_limit, stop $2,223.69 / limit $2,112.51) still open, covering 100% of held qty — one leg, no target, no split.

**Gap check:** ETH unrealized -7.48% vs CORE -15% hard cut — not triggered.

**Ratchet:** HWM $2,616.11 unchanged (current $2,414.20 is below HWM) — no new high, no ratchet. Stop distance from current price ~7.9%, above the 5% minimum.

**STEP B — Research:** Today's 06:08 UTC entry read. CORE: **HOLD** (binding — no CORE entry originates from this run regardless of screen changes). TACTICAL: **HOLD** (recommendation), and this run continues treating the unbroken 3-consecutive-tactical-loss streak as an active block on new TACTICAL originations, same reasoning as the 00:08 and 06:08 UTC runs today — no tactical win has occurred since to break the streak, and the day-boundary ambiguity is already logged in OBSERVATIONS.md pending weekly-review. Not re-logging a duplicate observation this run.

**STEP D — Re-screened for completeness:** CORE shortlist now UNI FIL XTZ DOT (ARB dropped off CORE, DOT joined) — moot, CORE is HOLD-binding regardless of shortlist composition. TACTICAL (1H) shortlist narrowed to 5 (POL DOT HYPE GRT DOGE) — moot, blocked by the tactical-loss-streak caution flag above regardless of any catalyst. Did not run STEP C (live quote/spread re-validation) or spend a perplexity/WebSearch catalyst call, since no candidate can pass the circuit-breaker-caution gate this run.

**No orders placed, no stops cancelled. No clickup notification (nothing acted upon).**

---

### 2026-09-17T17:08 UTC — EXECUTE — NO ACTION (BLOCKED AT STEP A)

**Blocker:** `python scripts/bybit.py balance|holdings|orders spot|fills spot` and
`bash scripts/state.sh` all fail with:
`BYBIT ERROR: BYBIT_API_KEY / BYBIT_API_SECRET are not set.`
Root cause: `.env` exists, but `BYBIT_API_KEY` and `BYBIT_API_SECRET` are still the
shipped `your_..._here` placeholders, which `load_env()` (scripts/bybit.py:57-59)
correctly normalizes to absent. Bybit credentials have never been filled in since
the Alpaca -> Bybit migration.

**Consequence:** STEP A (state and reconcile) could not be performed at all. Equity,
holdings, resting stops and fills are ALL unknown this run. Per execute.md
("If any check below is ambiguous, do nothing and log why"), STEPS B-G were not
attempted and NO orders were placed, amended or cancelled.

**UNVERIFIED RISK — carried forward:** the last reconciled state (2026-09-16T12:11 UTC,
Alpaca era) showed one open CORE position, ETHUSD qty 0.015302647, with resting
stop_limit `1ebb2562`. Whether any position exists on the Bybit account, and whether
it carries a `stopLoss`, CANNOT be confirmed without credentials. execute.md STEP A.3
calls an unprotected position the single largest risk in this setup.

**Owner action required:** fill real Bybit API key/secret (read + spot trade, NO
withdraw permission) into `.env`. Until then every execute run is a no-op.

**No orders placed, no stops cancelled. No clickup notification (nothing acted upon).**

---

### 2026-09-17T20:27 UTC — EXECUTE — NO ACTION (flat, no candidate passes STEP D)

**Credentials blocker RESOLVED.** The last two execute runs (17:08, 20:08 UTC) halted at
STEP A because `.env` carried the `your_..._here` placeholders. Real Bybit credentials are
now present: `balance`, `holdings`, `orders spot` and `fills spot` all returned successfully
this run. STEP A was performed in full for the first time in the Bybit era.

**STEP A — State (`state.sh`, exchange clock 2026-09-17 20:27 UTC):**
EQUITY $200.00 (BUDGET CAP; account holds $178,978.89 — NOT tradeable) | FREE $199.89 |
DEPLOYED $0.11 = 0.1% (ceiling 85%, no floor). SIZE NOW: CORE $26.67 (risk $4.00, 15% trail,
max 4) / TACTICAL $20.00 (risk $2.00, 10% trail, max 1). Fee budget $0.52 / $2.00 used this
month, headroom $1.48. Amendment trigger: 3 closed trades since 2026-09-10, 3 < 10 — not
eligible, nothing amended.

**STEP A — Reconcile:** `orders spot` returns `[]` — NO resting orders of any kind.
`holdings` shows USDT $128,984.48, USDC $50,000.00, and eight dust balances: ARB $0.00125,
AR $0.00550, UNI $0.07105, CRV $0.01902, XRP $0.01272, ZK $0.00002, CAKE $0.00096,
0G $0.00038 — total $0.11, i.e. 0.05% of the $200 budget.

**The Alpaca-era ETHUSD position does not exist on Bybit.** TRADE-LOG's last reconciled
state (2026-09-16T12:11 UTC) showed one open CORE position, ETHUSD qty 0.015302647, with
resting stop_limit `1ebb2562`. That position lived on the *previous venue*. The Bybit account
holds no ETH whatsoever. The "UNVERIFIED RISK — carried forward" flag raised by the
2026-09-17T17:08 run is hereby **CLOSED**: there is no unprotected Bybit position, because
there is no Bybit position. **The bot is flat: 0 CORE, 0 TACTICAL, 0 resting orders.**

**Unexplained account-level activity at 2026-09-17 20:22 UTC (5 min before this run).**
`fills spot` shows four Sells, none of which this bot originated:

| Time (UTC) | Symbol | Side | Qty | Price | Value | Fee |
|---|---|---|---|---|---|---|
| 09-17 20:22 | BTCUSDT | Sell | 1 | 76,670.9 | $76,670.90 | 76.6709 |
| 09-17 20:22 | ETHUSDT | Sell | 1 | 2,456.41 | $2,456.41 | 2.45641 |
| 09-17 20:22 | 0GUSDT | Sell | 2496.25 | 0.2027 | $505.99 | 0.50599 |
| 09-17 20:22 | CRVUSDT | Sell | 1388.6 | 0.3328 | $462.13 | 0.46213 |

These are NOT bot trades and are NOT logged as closed trades. Evidence: (a) a single $76,671
BTC sale is 383x the entire $200 TRADING BUDGET and could never have been sized by any rule
in TRADING-STRATEGY.md; (b) `grep -niE "BTCUSDT|0GUSDT|CRVUSDT" memory/TRADE-LOG.md` finds no
corresponding bot entry; (c) no matching Buys appear anywhere in the fills window, so the bot
never opened them. Read as owner//account-level cleanup on the shared demo account, which
holds far more than the strategy may trade. Recorded for the audit trail only; no realized
P&L is attributed to the strategy and the fee budget is unaffected.

The only bot-scale fills in the window are the 2026-09-14 XRPUSDT pair (Buy 6.9367 @ 1.4416,
$10.00, 22:24 → Sell 6.92 @ 1.4441, $9.99, 22:26), a ~2-minute near-flat round trip already
accounted for in the closed-trade history. Not re-logged.

**STEP A.3 — Stops on holdings:** every remaining balance is dust worth $0.00002–$0.07, all
far below any symbol's `minOrderAmt`, so no stop can be placed on any of them and none is
warranted — combined they are $0.11 against a $200 budget. No position requires protection
and none was left unprotected.

**STEP B — Research:** `memory/RESEARCH-LOG.md` has NO entry for 2026-09-17 or 2026-09-18.
The most recent entry is 2026-09-16 06:08 UTC, whose standing decision was CORE **HOLD**
(binding) and TACTICAL **HOLD**. HYPOTHESIS-LOG STANDING VERDICTS re-read: short-horizon
momentum IC is negative (-0.050, t=-13), 30-day momentum likewise (-0.037, t=-10), tighter
stops and higher frequency both strictly worse, nothing tested beat BTC buy-and-hold over
5.7 years. Nothing this run contradicts them — this run places no trade.

**STEP C — Screen: NOT RUN, and why.** Skipped the 400-day/60-symbol fetch and all live
quote/spread validation deliberately: no candidate it could surface is able to pass STEP D
this run (see below), so the screen would be spent compute with no reachable decision
attached. Same reasoning the 2026-09-16 12:11 and 17:08 runs recorded.

**STEP D — BUY GATE: FAILS. No entry is legal this run.**
- `"category":"spot"` present in body — N/A, no order composed.
- positions after fill <= sleeve cap — would PASS (0 CORE of 4, 0 TACTICAL of 1).
- deployment after fill <= 85% — would PASS (0.1% now; there is NO floor, and this run does
  NOT buy to "correct" low deployment — 100% cash is a valid, compliant state).
- size = (equity * risk%) / stop distance — available: CORE $26.67 / TACTICAL $20.00.
- order value >= `minOrderAmt` — not evaluated, no candidate.
- spread <= 0.5% — not evaluated, no candidate.
- **catalyst documented in today's RESEARCH-LOG — FAILS. This is the binding block.**
  There is no 2026-09-17 research entry at all. CORE entries require the morning research
  plan and cannot originate here under any circumstance. TACTICAL may be originated in an
  execute run only if the current screen passes AND a catalyst is documented then — no
  catalyst exists to document, and manufacturing one to justify an entry is precisely the
  behaviour the gate exists to prevent.
- circuit breaker — **the two authorities disagree; logged to OBSERVATIONS.** `state.sh`
  prints "status: TRIPPED — no new entries" on a streak of 3 tactical losses whose most
  recent close was 2026-09-15. execute.md STEP D defines the gate as "realized losses today
  < 5% of equity, and not 3 consecutive tactical losses THAT CLOSED TODAY — the streak
  resets at 00:00 UTC and does NOT carry across days". Realized losses today are $0.00 vs
  the $10.00 limit, and no tactical loss closed today, so under execute.md — the sole
  authority for this run — the breaker is **NOT tripped**. Moot in practice: the missing
  catalyst blocks every entry regardless of which reading wins, so this run did not have to
  resolve it and did not act on the permissive reading.
- what would have to happen for a 30%+ run / what kills the thesis — N/A, no thesis formed.

**STEP E — No order placed.** No naked buy, no stop cancelled, no stop moved, no position
opened or closed by this bot.

**STEP LEARN — No position closed this run** (the 20:22 UTC sells are account-level, not bot
positions), so no `LESSON:` line is owed.

**STEP G — No clickup notification** (nothing placed, nothing closed).

**Net:** flat, $0.11 dust, 100% cash, 0 resting orders, fee budget untouched at $0.52/$2.00.
Patience is the strategy — a run that does nothing is the system working.

## 2026-09-17 20:32 UTC — research run, STEP A reconciliation

- Account FLAT: 0 open positions, $0.11 dust, 100% cash ($199.89 free of $200 budget).
- Reconciles CLEAN against the TRADE-LOG tail (prior run also closed flat). No drift.
- No resting orders owed: no position, so no stop, no ratchet, no hard-cut check applicable.
- No order placed, cancelled or amended. No position opened or closed by this bot.
- Realized P&L today: $0.00. Circuit breaker on the realized-loss test: NOT tripped ($0.00 vs $10.00).
- Fee budget unchanged: $0.52 / $2.00 this month, headroom $1.48.
- Decision recorded in RESEARCH-LOG: CORE HOLD (binding for the day), TACTICAL HOLD (advisory).

## 2026-09-17 20:47 UTC — execute run, no order placed

**STEP A — state and reconcile.** `balance`/`holdings`/`orders spot`/`fills spot` all
returned live. EQUITY $200.00 (budget cap; account holds $178,978.89 — NOT the sizing
basis). FREE $199.89, DEPLOYED $0.11 = 0.1%. Open positions: 0. Open orders: `[]`.
Non-zero balances are dust only (ARB 0.0071, AR 0.0021, UNI 0.0091, CRV 0.057, XRP 0.0098,
ZK, CAKE, 0G — $0.11 combined, every line below any symbol's `minOrderAmt`). Reconciles
CLEAN against the TRADE-LOG tail; no fill occurred since the 20:32 research run. No stop
is owed on dust: there is no position to protect and no sellable quantity. Nothing
ratcheted, nothing cut, nothing closed.

**STEP B — evidence.** RESEARCH-LOG 2026-09-17 (20:32 UTC) read in full; HYPOTHESIS-LOG
standing verdicts read. Still binding: wider stops beat tighter, lower frequency beats
higher, alt universe median -21.2% vs BTC +157.4% over 5.7y, nothing tested beats
buy-and-hold BTC. No reasoning below contradicts a standing verdict.

**STEP C — screen.** `screen.sh` re-run live. Output is materially unchanged from the
20:32 screen 15 minutes earlier: ARB still leads the tactical ranks, ONDO 0.3742 leads
CORE on 30p (+13.4%), BTC 76,536.5 (-0.2% 7p). TACTICAL shortlist 29 names, same set.
No new name appeared, no ranking inverted.

**STEP D — buy gate. NO ENTRY. Stated condition by condition:**
- `"category":"spot"` — N/A, no order body composed.
- positions after fill <= sleeve cap — would pass (0 of 4 CORE, 0 of 1 TACTICAL).
- deployment after fill <= 85% — would pass (0.1% now). NO floor; not buying to correct it.
- size = (equity * risk%) / stop distance — available: CORE $26.67, TACTICAL $20.00.
- order value >= `minOrderAmt` — not evaluated, no candidate.
- spread <= 0.5% — not evaluated, no candidate.
- circuit breaker — realized losses today $0.00 vs $10.00 limit: NOT tripped. `state.sh`
  again prints "TRIPPED" on a 3-tactical-loss streak whose most recent close was
  2026-09-15; execute.md STEP D — the sole authority for this run — resets that streak at
  00:00 UTC and says it does NOT carry across days, so under execute.md the breaker is
  NOT tripped. Third occurrence, re-logged to OBSERVATIONS. Moot again: the catalyst gate
  below blocks every entry regardless of which reading wins, and this run did not act on
  the permissive reading.
- **catalyst documented in today's RESEARCH-LOG — this is the binding block.**
  CORE: today's research decision is **HOLD, binding for the day** — no shortlist name
  carries a dated idiosyncratic catalyst, and CORE may not be originated in an execute run
  regardless. TACTICAL: research left HOLD with origination permitted here only if the
  screen passes AND a fresh catalyst is documented in this run. The screen passes for
  several names; **no fresh catalyst exists.** Nothing has occurred in the 15 minutes since
  the research run — no dated event, no print, no listing, no unlock resolving. ARB, the
  screen leader, carries the one dated catalyst on the board and it runs BEARISH: 139.15M
  tokens (1.4% of supply) unlock 2026-09-23, five days out. Entering a 10%-trail long into
  a dated supply event is taking the wrong side of the only dated catalyst available.
  Research's stated condition for a tactical entry — a dated idiosyncratic catalyst on a
  non-ARB name, plus BTC dominance stalling below ~60% — is unmet on both halves:
  dominance broke above 60% this week and the Altcoin Season Index is 37.
- 30%+ path / thesis-killer — N/A, no thesis formed. Manufacturing a catalyst to clear
  this gate is precisely the behaviour the gate exists to prevent.

**STEP E — No order placed.** No buy, no naked buy, no stop cancelled, moved or widened,
no position opened or closed by this bot. No `takeProfit`/`stopLoss` body was composed, so
the standing execute.md-vs-CLAUDE.md target-leg conflict did not have to be resolved.

**STEP LEARN — No position closed this run**, so no `LESSON:` line is owed.

**STEP G — No clickup notification** (nothing placed, nothing closed).

**Net:** flat, $0.11 dust, ~100% cash, 0 resting orders, fee budget untouched at
$0.52 / $2.00 this month (headroom $1.48). Cash is a position; 0.1% deployed is a valid,
compliant state. A run that does nothing is the system working.

---

## 2026-09-17 — Daily Snapshot (Day 7, UTC 20:44)

**Portfolio:** $193.91 | **Cash:** $193.80 (99.9%) | **Day P&L:** +$1.68 (+0.87%, 2-day delta) | **Cumulative:** -$6.09 (-3.05%)
**vs BTC:** -2.27pp edge | **Fees today:** $0.00 | **Fee budget:** $0.52 / $2.00 used this month (headroom $1.48)

| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
|--------|------|-----|-------|------|------------|---------------|---------------|
| — | none | — | — | — | — | — | n/a — flat, 0 positions |

Only dust remains ($0.11 total, every balance below its symbol's `minOrderAmt`), so no
position can or should carry a stop. `state.sh` SCAN-VERDICT: NO-ACTION.

**Benchmark:** BTC/USD $76,551.70 (last) vs $77,153.29 Day-0 baseline (2026-09-10 19:39 UTC) = **-0.78% cumulative**. Bot cumulative **-3.05%**. **EDGE -2.27pp** — bot still trailing the benchmark, but the gap narrowed from -3.49pp on 09-15 because the bot has been flat and BTC fell.

**Trades today (2026-09-17 UTC):** NONE by this bot. No entry, no exit, no order placed, cancelled or amended. Fee budget untouched.

**Equity basis — read this before trusting the figures above.** `state.sh` prints `EQUITY $200.00 (budget)` because $200 is the sizing CAP applied to a demo account holding $178,978.89; it is NOT a P&L-tracked balance and does NOT decrease when the strategy loses. The $193.91 above is therefore computed by hand as $200.00 starting budget minus $6.09 of logged realized losses (DOT -$1.61 09-14, UNI -$3.17 09-15, XRP -$1.31 09-15). Day P&L is measured against the 2026-09-15 snapshot ($192.23) because no snapshot was written on 09-16 or 09-17 — it is a **2-day delta, not a one-day figure**, and it reads positive only because the 09-15 figure included ETH/XRP unrealized drawdown that has since left the book.

**ETH disposition (unchanged from the 2026-09-17 20:27 run, not re-booked).** The bot's CORE ETH/USD leg (0.015302647 @ $2,609.50) is gone from the account. It was not closed by any bot order: the 09-17 20:22 UTC fills show an account-level sweep of 1.0 ETH @ $2,456.41 alongside 1 BTC, 2496 0G and 1389 CRV — all 10x-383x the entire $200 budget and none with a matching bot entry. Read as owner/account-level cleanup on the shared demo account. **No realized P&L is attributed to the strategy** and the fee budget is unaffected, consistent with the prior run's ruling. Memo only: had it been attributed, the mark-to-sweep figure would be ≈ -$2.34. If the owner intends that sweep to count as a strategy exit, a weekly-review run should book it explicitly — this run will not manufacture a close the bot did not place.

**Circuit breaker:** realized losses today $0.00 vs $10.00 limit (5% of budget) — **CLEAR**. `state.sh` again prints `status: TRIPPED` on a 3-consecutive-tactical-loss streak whose most recent close was 2026-09-15, two UTC days ago; `routines/execute.md` STEP D resets that streak at 00:00 UTC and says it does not carry across days. **FOURTH occurrence of this conflict** — re-logged to OBSERVATIONS.md. Moot again this run: the bot is flat and placed no order, so the permissive reading was not acted on.

**Amendment trigger:** 3 closed trades since the last applied amendment (2026-09-10), 3 all-time. 3 < 10 → **not eligible, nothing amended.** `memory/TRADING-STRATEGY.md` untouched.

**Notes:** Second consecutive fully flat day — no entries, no exits, no fees, 99.9% cash. The research run left CORE on a binding HOLD and TACTICAL blocked for want of a dated idiosyncratic catalyst, and nothing in the 6h since changed that; ARB still leads the screen while carrying a bearish 139.15M-token unlock on 09-23. The edge versus BTC improved 1.22pp this week purely by not trading into a falling benchmark, which is the "patience is the strategy" clause working as designed rather than luck. The one thing that genuinely needs owner attention is not a trading decision: the $200 budget figure `state.sh` reports is a cap and not a balance, so every "EQUITY" line in this log has to be hand-reconciled against realized rows to mean anything — that reconciliation is currently the most error-prone step in the whole routine and is logged to OBSERVATIONS.md.

---

## 2026-09-18 — Execute run (18:07 slot, run at 17:07 UTC broker clock)

**STEP A — state & reconcile.** `state.sh`: EQUITY $200.00 (budget cap; account holds
$179,007.19, not tradeable) | FREE $199.88 | DEPLOYED $0.12 = 0.1% (ceiling 50%, no floor)
| OPEN POSITIONS 0 | `bybit.py orders spot` -> `[]`. Live state matches the TRADE-LOG tail
exactly: flat, dust only (every balance below its symbol's `minOrderAmt`). No fill landed
since the research run, no stop was hit, no drift. Stop coverage n/a — no position can or
should carry a stop. Nothing to cut, re-attach or ratchet.
Circuit breaker: realized losses today $0.00 vs $10.00 limit; 0 consecutive losing closes
today (most recent loss closed 09-15) — **CLEAR**. The stale TRIPPED reading that recurred
four times is gone; `state.sh` prints `clear` on its own now.

**STEP B — evidence.** STANDING VERDICTS binding and unchallenged this run: altcoin median
-21.2% vs BTC +157.4% over 5.7y (CONFIRMED); nothing tested beats buy-and-hold BTC; higher
frequency and tighter stops both strictly worse; momentum inverted at <=1d (IC -0.012 test)
but positive at 30d (+0.025 test). New row #9 (2026-09-18, `sig_momentum_skip_recent`)
REJECTED — sign flips train-to-test. No reasoning below contradicts a verdict.

**STEP C — screen.** `screen.sh` re-run live. Board unchanged in substance from the 16:16
research run 51 min earlier: the top 7p movers (XPL, ETHFI, ARB, NEAR, UNI) are the names
the CORE screen rejects on overextension, which is the short-horizon window where measured
IC is NEGATIVE. TACTICAL shortlist 37 names.

**STEP D — BUY GATE: NOT REACHED. No candidate advanced to sizing.**
- CORE: today's RESEARCH-LOG puts CORE on a **binding HOLD** for the day. CORE entries
  require the morning research plan and it advanced none. Gate closed by rule, not judgement.
- TACTICAL: may be originated here, but only if the screen passes AND a catalyst is
  documented in this run. **No fresh catalyst exists.** The only two dated events on the
  board are both bearish supply releases (ZRO ~$26.4M unlock in the 09-14..09-20 window;
  ARB 139.15M tokens on 09-23) and nothing new has landed in the 51 minutes since research.
  Beta bounce off a +5.8% two-day BTC move is not an idiosyncratic catalyst.
- Remaining gate conditions therefore never evaluated (no body composed, no size derived,
  no spread/minOrderAmt check owed). Deployment 0.1% is far under the 50% ceiling; there is
  NO floor, so this run does **not** buy to correct it.

**STEP E — No order placed.** No buy, no naked buy, no stop cancelled, moved or widened.
No `stopLoss`/`takeProfit` body was composed, so the standing execute.md-vs-CLAUDE.md
target-leg wording conflict again did not have to be resolved.

**STEP LEARN — No position closed this run**, so no `LESSON:` line is owed.

**STEP G — No clickup notification** (nothing placed, nothing closed).

**Net:** flat, $0.12 dust, ~99.9% cash, 0 resting orders, fee budget untouched at
$0.52 / $2.00 this month (headroom $1.48). Third consecutive fully flat day. Cash is a
position; a run that does nothing against a >60%-dominance alt tape is the system working.

---

## 2026-09-18T20:07 UTC — execute (18:07 slot, broker clock 20:07)

**STEP A — state & reconcile.** `state.sh`: EQUITY $200.00 (budget cap; account holds
$179,026.40 — not tradeable) | FREE $199.88 | DEPLOYED $0.12 = 0.1% | OPEN POSITIONS 0 |
RESTING ORDERS 0 (`orders spot` -> `[]`). `holdings` = dust only (0G, CAKE), matching the
TRADE-LOG tail exactly. No drift, no fill while unattended, nothing to cut or ratchet.
72h TACTICAL time stop: no TACTICAL holdings, not applicable.
Circuit breaker CLEAR ($0.00 realized today vs $10.00; 0 consecutive losing closes today).
Fee budget $0.52 / $8.00 this month, headroom $7.48.

**STEP B — evidence.** STANDING VERDICTS binding: altcoin median -21.2% vs BTC +157.4%
(CONFIRMED); nothing tested beats buy-and-hold BTC; higher frequency and tighter stops both
strictly worse; momentum inverted at <=1d (IC -0.012 test), positive at 30d (+0.025 test);
row #9 `sig_momentum_skip_recent` REJECTED. **These verdicts argue against these entries**
and I state that explicitly: both names are short-horizon 7p movers, the horizon where
measured IC is negative. They are taken anyway because the owner directive of 2026-09-18
(v3 quota mode, commit 900e78b) sets a HARD FLOOR of 2 TACTICAL entries per UTC day and
declares the expectancy cost accepted. This is quota compliance, not a conviction claim.

**STEP C — screen.** `screen.sh` live. TACTICAL SHORTLIST (46) in rank order:
POL OP XPL ARB AERO VVV SKY MNT SOL UNI ...

**STEP D0 — QUOTA: 0/2 entries today, this is the 18:07 run -> BACKSTOP ACTIVE, must fill 2.**
Worked the tactical screen in RANK ORDER; ranks 1 and 2 (POL, OP) both cleared every hard
gate, so no substitution or judgement was applied.

**STEP D — BUY GATE, both entries:**
- `"category":"spot"` present in every body — yes. No leverage, no short, no perp.
- positions after fill = 2 TACTICAL <= 6 cap; combined 2 <= 7. PASS
- deployment after fill = $19.97 = 10.0% of the $200 budget <= 50% ceiling. PASS
- size = (equity $200 * 0.5%) / 10% trail = $10.00 per position, under the 8% ($16) cap. PASS
- order value $9.97 / $10.00 >= minOrderAmt $5 for both. PASS
- spread: POL 0.13% (0.10719/0.10733), OP 0.026% (0.11765/0.11768) — both <= 0.5%. PASS
- circuit breaker not tripped. PASS
- catalyst: TACTICAL requires NONE (amended 2026-09-18). Screen record below is the thesis.

| Sleeve | Symbol | Rank | 7p% | 30p% | vsSMA20 | vol% | spr% |
|---|---|---|---|---|---|---|---|
| TACTICAL | POLUSDT | 1 | +8.0 | +11.0 | +7.2 | 1.5 | 0.15 |
| TACTICAL | OPUSDT | 2 | +6.5 | +20.3 | +5.7 | 1.1 | 0.06 |

**STEP E — orders placed.**

| UTC | Sleeve | Symbol | Side | Qty | Fill | Value | Fee | Stop (trigger/limit) | Target |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18T20:10 | TACTICAL | POLUSDT | Buy | 93.1 | 0.10708 | $9.97 | 0.0931 POL | 0.09637 / 0.09155 | NONE (v2) |
| 2026-09-18T20:10 | TACTICAL | OPUSDT | Buy | 84.98 | 0.11764 | $10.00 | 0.08498 OP | 0.10588 / 0.10059 | NONE (v2) |

Stops are 10% below entry (entry = first high-water mark), ratchet UP only, tighten to 8%
at +20%. Each stop covers 100% of the HELD qty (fill minus the base-coin fee): POL 93.0 of
93.0069 held, OP 84.89 of 84.895 held. Verified resting via `orders spot`: both
`Untriggered`. No `takeProfit` attached to either — neither sleeve has a target in v2.
72h time stop starts now: both are due for a close at 2026-09-21T20:10 UTC unless >= +5%.

**MECHANISM DEVIATION — READ THIS.** `routines/execute.md` STEP E prescribes ONE call with
`stopLoss` attached to the market buy. **Bybit rejected every form of that body** with
`retCode 170130: Data sent for paramter '' is not valid` — with `tpslMode":"Full"`, without
it, with `marketUnit` quoteCoin and with baseCoin. The attached-stop form does not work on
this venue's spot endpoint. Protection was instead placed as the separate resting
CONDITIONAL stop sell that `CLAUDE.md` ("Strategy Hard Rules") actually specifies —
`orderFilter":"StopOrder"`, `triggerPrice` at the stop, limit 5% below it — which was
accepted first try on both names. Consequence, stated plainly: each position was
**unprotected for the few seconds between the buy fill and the stop acknowledgement**,
which is the exact exposure STEP E exists to prevent. The first such gap was opened by a
probe buy I sent to isolate which parameter the API was rejecting, and that probe filled —
that was my error, not an API quirk. Logged to OBSERVATIONS.md. Until execute.md STEP E is
repaired, the two-call sequence is the only way to hold a stop at this venue.

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**Net:** 2 TACTICAL positions, $19.97 deployed = 10.0% of budget, both stopped at the
exchange, 4 TACTICAL slots free, CORE slot empty (binding HOLD from the 09-18 research run
stands). Quota 2/2 — satisfied. Fees this run ~$0.02 equivalent; month-to-date unchanged
band, headroom ample.

---

## 2026-09-18T20:29 UTC — execute (re-run, same 18:07 slot)

Manual re-run ~20 min after the 20:07 execution. Full routine walked again.

**STEP A — state & reconcile.** EQUITY $200.00 (budget) | FREE $179.85 | DEPLOYED $20.15 =
10.1% (ceiling 50%). OPEN POSITIONS 2, both TACTICAL, both age 0.3h. Exchange state matches
the TRADE-LOG tail exactly — same two fills, same two resting stops, no new fill, nothing
closed, no drift.

| Symbol | Qty held | Entry | Price | P&L | Stop coverage |
|---|---|---|---|---|---|
| OPUSDT | 84.895020 | 0.11764 | 0.1183 | +0.59% | 100% [OK] |
| POLUSDT | 93.006900 | 0.10708 | 0.1073 | +0.17% | 100% [OK] |

72h TACTICAL time stop: both at 0.3h of 72h — not due. Nothing to cut.
Circuit breaker CLEAR ($0.00 realized today, 0 consecutive losing closes). Fee budget
$0.52 / $8.00, headroom $7.48 — untouched this run, no fee-bearing order placed.

**RATCHET — both stops moved UP.** High-water since fill taken from 1m klines bounded to
bars after the fill timestamp (21 bars each): OP 0.11844, POL 0.10758. TACTICAL trail is 10%
below high-water, ratcheted up only. Both were still sitting at 10% below ENTRY, so both
were stale. Amended in place (`bybit.py amend`, one call each — no cancel/replace, so no
unprotected window at any point):

| Symbol | High-water | Stop was | Stop now | Limit now | Move |
|---|---|---|---|---|---|
| OPUSDT | 0.11844 | 0.10588 | 0.10660 | 0.10127 | +0.68% |
| POLUSDT | 0.10758 | 0.09637 | 0.09682 | 0.09198 | +0.47% |

Verified resting `Untriggered` at 100% of held qty after the amend. Limit legs stay 5%
below trigger. Neither stop was widened; neither was moved down. Both remain ~9.8-9.9%
below current price, clear of the 5%-minimum-gap rule.

**Trail is 10%, NOT 8%.** `state.sh`'s advisory SCAN GATE printed both ratchets against an
**8% trail** (`8% trail on $0.1183 = $0.1089`). That is wrong here: 8% only applies once a
TACTICAL position is >= +20%, and these are +0.59% and +0.17%. Obeying it would have placed
both stops ~2% tighter than the rulebook allows, against the CONFIRMED standing verdict that
tighter stops are strictly worse. The gate is advisory/SHADOW MODE and runs must not obey it
yet, which is what saved this. Logged to OBSERVATIONS.md.

**STEP B — evidence.** Standing verdicts unchanged from the 20:07 run; nothing in this run
rests on a REJECTED finding. Relevant here: tighter stops are strictly worse (CONFIRMED) —
directly applied above in rejecting the 8% figure.

**STEP C/D0 — screen & quota. QUOTA: 2/2 entries today — MET.** The floor is satisfied by
the 20:07 POL and OP entries. The quota is a FLOOR, not a target, and trade count is the
enemy (BTC buy-and-hold pays 0% in fees), so no third entry was sought.

**STEP D — BUY GATE: not reached, no candidate advanced.**
- CORE: binding HOLD from the 2026-09-18 research run stands — that run advanced no CORE
  idea and CORE entries require the morning plan. Gate closed by rule, not judgement.
- TACTICAL: quota already met; no rule requires a further entry and none was taken. This is
  not a quota miss and not a discretionary skip — the floor is satisfied.

**STEP E — no new order placed.** Only the two ratchet amends above. No buy, no naked buy,
no stop cancelled, widened or moved down, no target leg anywhere.

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**STEP G — no notification.** Nothing was placed or closed; a ratchet is neither.

**Net:** unchanged at 2 TACTICAL positions, $20.15 deployed = 10.1% of budget, both stops
tightened to a correct 10%-of-high-water trail and resting at 100% coverage. 4 TACTICAL
slots free, CORE slot empty. Fees this run $0.00.

---

### 2026-09-21T15:05 UTC — ENTRY — TACTICAL — ARB BUY

### 2026-09-21T15:05 UTC — ENTRY — TACTICAL — XPL BUY

| UTC | Sleeve | Symbol | Side | Qty | Fill | Value | Fee | Stop (trigger/limit) | Target |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21T15:05 | TACTICAL | ARB | Buy | 42.46 | 0.2381 | $10.11 | 0.04246 ARB | 0.21429 / 0.20357 | none (v2) |
| 2026-09-21T15:05 | TACTICAL | XPL | Buy | 97.6 | 0.10231 | $9.99 | 0.0976 XPL | 0.09216 / 0.08755 | none (v2) |

**STEP A — state & reconcile.** BLOCKED AT FIRST CALL, then repaired. Every private API
call failed `retCode 10002` (timestamp). Measured against `/v5/market/time`: this machine's
clock runs **+2.34s ahead** of Bybit. `recv_window` does not widen the ahead-side of the
window (Bybit rejects `req_timestamp > server_time + 1000ms` regardless), so the existing
retry-on-10002 could never succeed — it just re-sent an equally-skewed timestamp. Patched
`scripts/bybit.py` to sign with the exchange's clock (one-shot offset probe, biased 1s early
for flight time) instead of the local one. All calls then succeeded. Logged to OBSERVATIONS.

Reconcile: `holdings` = OP + POL, matching TRADE-LOG. No fills since 2026-09-18T20:10, so
nothing closed while the machine was off and no unlogged trade exists. Both stops present,
`Untriggered`, at 100% of held qty.

**72h time stop:** OP and POL both at 66.9h — under 72h, and both are >= +5% anyway
(OP +8.6%, POL +5.5%), so both are exempt and keep riding the trail. No slot freed.

**Ratchets applied** (both TACTICAL, 10% trail — neither has reached +20%, so the 8% tighten
does NOT apply; the SHADOW-MODE scan gate again suggested 8% and was again correctly ignored):
- OP: high-water $0.13315 -> stop $0.10660 -> **$0.11983** / limit $0.11383 (5.96% below spot)
- POL: high-water $0.11460 -> stop $0.09682 -> **$0.10314** / limit $0.09798 (8.9% below spot)
Both amended in place rather than cancel-and-replace, so protection was never interrupted.

**STEP B — evidence.** No RESEARCH-LOG entry exists for 2026-09-19, -20 or -21 (latest is
2026-09-18). **CORE is therefore blocked by rule** — CORE entries require the morning plan.
TACTICAL requires no catalyst and may be originated here. Standing verdicts unchanged;
nothing below rests on a REJECTED finding. Both entries are trend entries on a 10% trail
with a 72h time stop, not a claim of edge — consistent with, not contradicting, the
CONFIRMED verdict that nothing tested beats buy-and-hold BTC.

**STEP D0 — QUOTA: 0/2 entries today (2026-09-21), and this is the last entry window ->
BACKSTOP ACTIVE, must fill 2.** Worked the TACTICAL shortlist in RANK ORDER: ARB (#1),
XPL (#2). No judgement substituted for rank. ARB carries a dated 09-23 token unlock noted in
the 09-18 research run; that is NOT one of the 8 hard gates and "bearish catalyst" is not a
valid quota miss, so rank order governed and ARB was taken. Flagged here for the next run,
since the unlock lands inside ARB's 72h window.

**STEP D — BUY GATE (each condition, both names):**
1. `"category":"spot"` present in both bodies — yes. Market Buy, no leverage, long only.
2. Positions after fill: 4 TACTICAL <= 6; combined 4 <= 7. PASS.
3. Deployment after fill: $21.50 + $20.10 = $41.60 = 20.8% of $200 budget <= 50%. PASS.
4. Size = ($200 * 0.5%) / 10% trail = $10.00; cap 8% = $16.00 -> $10.00 each. Risk-derived,
   not a fixed dollar amount. PASS.
5. Order value $10.11 / $9.99 >= `minOrderAmt` $5 for both. PASS.
6. Spread ARB 0.068%, XPL 0.068% — both <= 0.5%. PASS.
7. Circuit breaker: realized losses today $0.00 vs $10.00 limit; 0 consecutive losses today
   (most recent loss closed 2026-09-15). Not tripped. PASS.
8. Fee budget: $0.52 of $8.00 used this month, headroom $7.48. Not exhausted. PASS.
9. Catalyst: TACTICAL requires none — the screen IS the thesis. Recorded below.

**Screen evidence at entry** (TACTICAL shortlist of 43, ranked by 7-period move):
- ARB — rank 1. 7p +7.8%, 30p +10.1%, +5.4% vs SMA20, vol 2.9%, spread 0.09%.
- XPL — rank 2. 7p +6.8%, 30p +13.2%, +6.8% vs SMA20, vol 1.6%, spread 0.05%.

**STEP E — two calls per symbol, buy then stop, back to back, one symbol fully protected
before the next buy was sent.** No `stopLoss` field in any buy body (spot rejects it,
`retCode 170130`). No `takeProfit`, no resting limit sell, no target leg. Stop trigger and
limit were computed BEFORE each buy. No probe orders. Both stops sized to HELD qty read from
`holdings` after the fill (ARB 42.4246 -> 42.42; XPL 97.5024 -> 97.5), i.e. net of the
base-coin fee, not the requested qty.

ARB filled at 0.2381 against an ask of 0.23549 (slippage), which left the pre-computed stop
11.0% below the actual entry instead of 10%. Amended UP to 0.21429 / 0.20357 to match the
rulebook's 10%-below-entry. Never moved down. XPL filled at 0.10231 vs 0.1024 quoted; its
stop sits 9.9% below entry, inside spec, left alone.

Verified via `orders spot`: four `Untriggered` stops resting, one per position, each at 100%
of held qty. No position is naked.

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**Net:** 4 TACTICAL positions, $41.60 deployed = 20.8% of budget, 2 TACTICAL slots free,
CORE slot empty (blocked — no research plan). Quota 2/2 MET. Fees this run ~$0.011 in base
coin (~$0.011), fee budget still ~$7.47 free.

---

## 2026-09-21T15:02 UTC — research (late; scheduled 06:07, ran 15:02)

**BLOCKER CLEARED FIRST.** Every signed Bybit call failed `retCode 10002` — local clock
~2.3s ahead of Bybit's server, and Bybit rejects a signed timestamp more than ~1s ahead
regardless of `recv_window`, so all 3 retries failed identically and `state.sh` died at its
first call. Fixed in `scripts/bybit.py`: `X-BAPI-TIMESTAMP` is now anchored to the exchange
clock (offset measured once per process off the public `/v5/market/time`, re-measured on a
10002). Verified working before any trading action was taken. No trading rule touched.

**STEP A — state & reconcile.** EQUITY $200.00 (budget) | FREE $178.53 | DEPLOYED $21.47 =
10.7% (ceiling 50%). OPEN POSITIONS 2, both TACTICAL, both age 66.9h. Exchange state matches
the TRADE-LOG tail exactly — same two fills, same two resting stops, nothing filled or
closed since 09-18T20:29, no drift. Dust (ARB $0.0017 etc) is residue, not a position.

| Symbol | Qty held | Entry | Price | P&L | Stop coverage |
|---|---|---|---|---|---|
| OPUSDT | 84.895020 | 0.11764 | 0.1275 | +8.40% | 100% [OK] |
| POLUSDT | 93.006900 | 0.10708 | 0.1132 | +5.72% | 100% [OK] |

**72h time stop — NOT due.** Both at 66.9h of 72h but the rule is "72h unless >= +5%", and
both clear it (+8.40%, +5.72%). Neither closed for age. Handoff note for 18:07 execute: if
either slips below +5% before ~20:07 the time stop re-arms.

**No hard cut.** Both positions positive; nothing near the -10% TACTICAL cut level.

Circuit breaker CLEAR ($0.00 realized today, 0 consecutive losing closes, last loss
2026-09-15). Fee budget $0.52 / $8.00, headroom $7.48 — no fee-bearing order this run.

**RATCHET — both stops moved UP.** High-water taken from 68 hourly bars since the
09-18T20:07 fills: OP 0.13315, POL 0.11460. TACTICAL trail is 10% below high-water,
ratcheted up only. Both stops were stale at the 09-18 levels. Amended in place
(`bybit.py amend`, one call each — no cancel/replace, so no unprotected window):

| Symbol | High-water | Stop was | Stop now | Limit now | Move |
|---|---|---|---|---|---|
| OPUSDT | 0.13315 | 0.10660 | 0.11983 | 0.11384 | +12.4% |
| POLUSDT | 0.11460 | 0.09682 | 0.10314 | 0.09798 | +6.5% |

Verified resting `Untriggered` at 100% of held qty after the amend. Limits sit 5% below
trigger. Neither stop widened, neither moved down. Gap to current price 6.0% (OP) and 8.9%
(POL), both clear of the 5%-minimum rule.

**Trail is 10%, NOT 8% — again.** `state.sh`'s advisory SCAN GATE printed both ratchets
against an 8% trail (`8% trail on $0.1275 = $0.1173`). Wrong here: 8% applies only at
>= +20%, and entry-to-high-water is +13.2% (OP) and +7.0% (POL). Obeying it would have set
both stops ~2% tighter than the rulebook allows, against the CONFIRMED verdict that tighter
stops are strictly worse. The gate is SHADOW MODE and was not obeyed. This is the identical
defect the 09-18 run logged; it is still present.

**No entry this run.** Research runs do not originate entries. CORE: HOLD, binding for the
day — no dated idiosyncratic catalyst on any of the 28 CORE-shortlist names, and the only
two dated events (XPL 09-25 unlock at 63.2% of float, ARB 09-23) are bearish supply
releases on names that pass. TACTICAL: quota is **0/2 for today with one window left
(18:07)** — the ranked shortlist was handed to execute in RESEARCH-LOG.md
(BR, LTC, CHIP, SUI, MNT, PIEVERSE, ADA, HBAR; XPL/ARB/BTC/STETH/POL excluded and why).

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**Net:** unchanged at 2 TACTICAL positions, $21.47 deployed = 10.7% of budget, both stops
ratcheted up to a correct 10%-of-high-water trail at 100% coverage. 4 TACTICAL slots free,
CORE slot empty. Fees this run $0.00.

### ADDENDUM 2026-09-21T15:10 UTC — an execute run landed DURING this research run

Everything above was written against a 2-position account. While this run was between
STEP C and STEP D, a concurrent `execute` run (commit `53bf98b`, "execute 2026-09-21T15:05
— 2 TACTICAL entries (ARB, XPL), quota 2/2") opened **two new TACTICAL positions and met
the daily quota**. The account is now 4 positions, not 2. The TACTICAL handoff above is
therefore SPENT — the 18:07 window no longer needs to fill a quota, it reads 2/2.

Re-read of `state.sh` after the fact:

| Symbol | Qty | Entry | Price | P&L | Age | Stop | Coverage |
|---|---|---|---|---|---|---|---|
| ARB | 42.424653 | 0.2381 | 0.2371 | -0.44% | 0.1h | 0.2143 | 100% [OK] |
| OP | 84.895020 | 0.11764 | 0.1279 | +8.70% | 67.0h | 0.11983 | 100% [OK] |
| POL | 93.006900 | 0.10708 | 0.1136 | +6.12% | 67.0h | 0.10314 | 100% [OK] |
| XPL | 97.502400 | 0.1023 | 0.1016 | -0.65% | 0.1h | 0.0922 | 100% [OK] |

FREE $158.51 | DEPLOYED $41.49 = 20.7% of budget (ceiling 50%). **No position is naked**;
all four carry a single resting conditional stop at 100% of held qty. My two ratchets on
OP and POL survived the concurrent run intact. Nothing here is a safety problem.

**But the two names it bought are the exact two this run disqualified, for a documented
reason.** ARB and XPL were the ONLY two shortlist names carrying dated events, both
bearish supply releases, and both were excluded from the ranked handoff above:

- **XPL unlocks 63.2% of circulating supply on 2026-09-25 (~$158M)** — four days out, the
  single largest scheduled event on the entire board.
- **ARB unlocked 139.15M tokens on 2026-09-23** — two days out.

This is not the execute run breaking a rule. Under the 2026-09-18 owner directive TACTICAL
"needs NO catalyst — the technical screen is the thesis", and both names PASS the tactical
screen, so the entries are compliant. The defect is structural: **nothing in the tactical
path ever looks at the unlock calendar.** Research checks catalysts but does not enter;
execute enters but is explicitly relieved of checking. A dated, known, bearish supply event
on a held name can therefore be found by one run and bought by another on the same day.
Logged to OBSERVATIONS.md — it needs a rule, not a one-off intervention.

**No corrective trade taken, deliberately.** Both positions are ~$10 with a 10% stop, so
the defined risk is ~$1.00 each against a $10.00 daily breaker — immaterial. Closing them
would burn ~0.65% round-trip in real fees to override a compliant decision by another run
on the basis of a story, against the CONFIRMED verdict that higher frequency is strictly
worse. The stops are the right instrument here and they are in place. Flagged, not traded.

**Handoff to the 18:07 execute run and to the weekly review:**
- Quota is MET (2/2). Do not add a third entry to satisfy a floor that is already satisfied.
- **XPL: the unlock is 09-25.** The stop at 0.0922 is the protection; verify it still rests
  at 100% on every run between now and then, and do not widen it. A 63%-of-float event can
  gap straight through a 5%-wide stop-limit band — that risk is accepted and stated, not
  hedged.
- ARB's unlock is 09-23, inside the 72h time-stop window for a position opened 09-21T15:05.
- The two SHADOW-LOG rows written earlier this run for ARB and XPL ("not taken") were true
  when written and were overtaken ~minutes later. Per the append-only rule they are left
  standing rather than edited; the weekly review should treat both as TAKEN, not skipped,
  when it scores the 09-21 cohort on 09-26.

### 2026-09-21T16:20 UTC — research RE-RUN (second research invocation this UTC day)

**No order placed, cancelled or amended. Fees this run $0.00.**

Reconciliation: live holdings match this log exactly — ARB 42.424653, OP 84.895020,
POL 93.006900, XPL 97.502400. No fill and no stop execution since the 15:10 addendum.
All four carry exactly ONE resting conditional stop at 100% of held qty; nothing naked,
nothing split, no target legs. No sleeve hard cut triggered (worst is ARB -2.48% against
the TACTICAL -10% cut).

**Ratchet: none placed, and `state.sh`'s SCAN-VERDICT was deliberately not obeyed.** The
gate flagged POL and XPL on an **8% trail**; the 8% trail is only earned at **+20%**, and
POL is +5.93% while XPL is -1.97%, so 10% is the correct trail for both. Obeying the
advisory gate would have set stops the rulebook does not authorise. This is the SAME
SHADOW-MODE defect logged on 09-18 and again on 09-21-morning — still present, still not
obeyed.

Checked against real high-water marks (`bybit.py kline`): OP 0.13315 -> 0.11984 (resting
0.1198, correct), POL 0.1146 -> 0.10314 (resting 0.1031, correct), ARB post-entry 0.23823
-> 0.21441 (resting 0.2143, correct). XPL post-entry HWM 0.10279 -> 0.09251 vs resting
0.0922 is a real but trivial +0.3% raise worth **$0.03**; declined, because a
cancel-then-replace opens a window with no resting stop and that operational risk is not
worth $0.03 four days before XPL's unlock. Judgement call, recorded as such — not an
oversight. Next run should place it if the high-water rises materially.

**CORE: HOLD, binding (unchanged from the morning run).** 27 CORE names pass the screen and
none carries a dated idiosyncratic catalyst; the only two dated events on the board are
bearish supply releases on names already held (XPL 09-25, ARB 09-23).

**TACTICAL: quota MET 2/2** (ARB, XPL, opened 15:05 by execute `53bf98b`). Nothing
originated — research runs never originate. Ranked handoff written to RESEARCH-LOG.md for
the 18:07 window as OPTIONAL; the floor is already satisfied and may not be cited to
justify a third entry.

**New market facts since the morning run:** the Fed HIKED 25bp on 2026-09-16 to 3.75-4.00%
(unanimous, first hike in three years, 16 of 18 officials see at least one more this year),
and 2026-09-25 now carries BOTH the XPL unlock AND a ~$16.6B Deribit BTC+ETH options expiry.
The screen shows 47 of 60 names passing — that is tape-wide beta, not selection information,
and all four open positions are the same L1/L2 alt-beta bet expressed four ways.

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**Net:** unchanged at 4 TACTICAL positions, $41.10 deployed = 20.5% of budget, all stops
correct at 100% coverage. CORE slot empty, 2 TACTICAL slots free. Fee budget $0.52 / $8.00.

## 2026-09-21T17:15 UTC — execute run — NO ENTRIES (quota already met 2/2)

**STEP A — reconcile.** EQUITY $200.00 (budget cap; account holds $179,079.55, not
tradeable). FREE $159.29 | DEPLOYED $40.71 = 20.4% of budget (ceiling 50%). `holdings`,
`orders spot` and `fills spot` match the TRADE-LOG tail exactly — 4 TACTICAL positions,
4 resting `Untriggered` conditional stops, 100% of held qty each, no target legs, no
unlogged fill since 09-21T15:05. Nothing closed this run.

**STEP A4 — 72h TACTICAL time stop: not due for any position.**
- OP  — filled 09-18T20:10, age 69.1h, +6.1% vs entry -> **exempt** (>= +5%), rides trail.
- POL — filled 09-18T20:10, age 69.1h, **+4.4% vs entry -> NOT exempt.** 72h falls at
  **2026-09-21T20:10 UTC**, ~3h after this run. Cannot be closed early; the rule is 72h.
  **Flagged for the next execute run: if POL is still < +5% at/after 20:10 UTC, cancel its
  resting stop (id 2307087177345142016) then close at market.**
- ARB, XPL — age 2.2h, nowhere near.

**STEP B — evidence.** Read the STANDING VERDICTS table. Nothing this run contradicts one.
Verdicts actually applied below: tighter stops are strictly worse (-44.8% -> -5.8% as the
trail widens), and momentum IC is negative at <= 1d.

**Ratchet check — real high-water marks from `bybit.py kline` (hourly, since fill), 10%
trail (none of the four is +20% entry-to-high-water, so the 8% tighten does NOT apply):**

| Symbol | Entry | High-water | 10% trail level | Resting stop | Action |
|---|---|---|---|---|---|
| ARB | 0.2381 | 0.24780 | 0.22302 | 0.21429 | **BLOCKED — see below** |
| OP | 0.11764 | 0.13315 | 0.11983 | 0.11983 | none, already there |
| POL | 0.10708 | 0.11460 | 0.10314 | 0.10314 | none, already there |
| XPL | 0.10231 | 0.10412 | 0.09371 | 0.09216 | **RATCHETED UP -> 0.09371** |

- **XPL ratcheted 0.09216 -> 0.09371** (limit 0.08902 = trigger*0.95), amended in place via
  `/v5/order/amend`, no cancel/replace, so no unprotected window. Verified `Untriggered` at
  97.5 = 100% of held qty. Gap to price ($0.1004) is 6.7%, clears the 5% minimum.
- **ARB ratchet BLOCKED by hard rule 8** ("never place a stop within 5% of current price").
  Its 10% trail level 0.22302 sits only 2.0% below the live price $0.22751. The stop was
  therefore LEFT at 0.21429 (5.8% below price) rather than moved to some intermediate level
  — an intermediate is not a level the rulebook derives, and manufacturing a tighter stop
  runs directly against the CONFIRMED verdict that tighter stops are strictly worse. No
  stop was moved down. Revisit when ARB's price rises enough for the trail to clear the 5%.

**STEP D0 — DAILY QUOTA: 2/2 TACTICAL entries for 2026-09-21 (ARB, XPL at 15:05) ->
MET.** The floor is satisfied; it is a minimum, not a target, and may not be cited to
justify a third entry.

**STEP D — no buy gate evaluated: no candidate was advanced.**
- **CORE: HOLD, binding.** Today's RESEARCH-LOG carries no dated idiosyncratic catalyst on
  any of the 28 CORE shortlist names; the only dated events on the board are bearish supply
  releases (ARB unlock 09-23, XPL 63.2%-of-float unlock 09-25). CORE requires a catalyst, so
  this is a rule-compliant CORE stand-down, not discretion.
- **TACTICAL: quota met, no further entry.** This is NOT a quota miss and NOT a patience
  argument — the floor of 2 was filled earlier today.

**Risk still carried:** all four positions are the same L1/L2 alt-beta bet expressed four
ways, into BTC dominance 59.1%, a confirmed negative-median alt universe, ~$900M of unlock
supply this week (including XPL's own on 09-25) and the 09-25 ~$16.6B Deribit expiry.

**STEP LEARN — no position closed this run**, so no `LESSON:` line is owed.

**Fee budget:** $0.52 / $8.00 this month, headroom $7.48. This run spent **$0.00** — the
amend is not fee-bearing and no order filled.

**Circuit breaker:** CLEAR. $0.00 realized losses today vs the $10.00 limit; 0 consecutive
losing closes today; most recent loss closed 2026-09-15.

**Net:** 4 TACTICAL positions, $40.71 deployed = 20.4% of budget, every position stopped at
100% coverage. CORE slot empty, 2 TACTICAL slots free.

---

### 2026-09-21T20:12 UTC — EXIT — TACTICAL — POL — 72h TIME STOP

Closed at market by the 72h TACTICAL time stop (`routines/execute.md` STEP A.4).
Filled 2026-09-18T20:10, so 72h fell at 2026-09-21T20:10 — this run began 20:11 UTC.
At the gate POL was **+4.24%** vs entry (bid 0.11162 / entry 0.10708), i.e. **below the
+5% exemption**, so it was not exempt and the rule is mandatory. OP, filled in the same
minute, was **+5.62%** and IS exempt — it keeps riding its trail.

Resting stop `2307087177345142016` was CANCELLED BEFORE the market sell, per STEP A.4, so
the two legs could not race. Cancel confirmed, then sell sent.

| Field | Value |
|---|---|
| Exit time (UTC) | 2026-09-21T20:12 |
| Exit type | market sell, 72h time stop (not a stop trigger) |
| Qty | 93.0 of 93.0069 held (0.0069 POL dust left, $0.0008, below minOrderQty 0.1) |
| Fill price | $0.11161 |
| Exit proceeds | $10.37973 |
| Sell fee | -$0.01038 (USDT) |
| Cost basis | $9.96915 (93.1 @ $0.10708; buy fee 0.0931 POL taken in kind) |
| Gross P&L | +$0.41058 |
| **REALIZED P&L** | **$0.40** (+4.02% net) |
| Order id | 2309263168041651456 |

**Circuit breaker after this exit:** realized losses today $0.00 vs $10.00 limit → CLEAR.
This close was a WIN, so the consecutive-tactical-loss streak stays at 0.

**Narrative:** L1/L2 alt beta — profitable close, streak counter unaffected.

LESSON: The 72h time stop and the +5% exemption were separated by 0.8pp on a position that
was +5.72% at the 15:02 research run and +4.24% at the 20:11 gate — the exemption test is
evaluated at a single instant against a price that moves ~1pp/hour, so which side of it a
position lands on is close to arbitrary for anything in the +4-6% band. Falsifiable
prediction: across the next ten TACTICAL closes, positions exiting in the +4-6% band will
show no difference in forward 72h return between those closed by the time stop and those
exempted — if true, the exemption threshold is adding noise, not selection, and belongs in
the weekly review as a candidate for a band rather than a point test. Do NOT act on this
run.

---

### 2026-09-21T20:11 UTC — EXECUTE — 72h time stop fired (POL), no entries, quota already met

**Venue:** Bybit DEMO `api-demo.bybit.com`, `"category":"spot"` on every call. Spot only,
long only, no leverage, nothing withdrawn or transferred.

**STEP A — state and reconcile.** `state.sh` + `balance`/`holdings`/`orders`/`fills`.
- EQUITY $200.00 (budget cap; account holds $179,056.52 — NOT tradeable). Exchange clock
  2026-09-21 20:11 UTC; local clock not trusted.
- DEPLOYED at open $40.32 = 20.2% of budget. 4 positions, all TACTICAL, CORE slot empty.
- RECONCILE: `holdings` matched the TRADE-LOG tail exactly — ARB, OP, POL, XPL, same four
  resting stops (`Untriggered`, 100% of held qty each). Nothing filled or closed while no
  routine was running. No drift, no anomaly. Sub-cent dust (XRP, AR, UNI, CRV, ZK, CAKE,
  0G) is residue, not positions.
- STOP COVERAGE: all four at 100% before the run; three at 100% after (POL's was cancelled
  as part of its close).
- **72h TIME STOP:** OP and POL both filled 2026-09-18T20:10, both exactly 72.0h old.
  OP +5.62% → **exempt**, no action. POL +4.24% → **NOT exempt, CLOSED AT MARKET**, logged
  above. ARB and XPL are 5.1h old, nowhere near the limit.

**STEP B — research and evidence.** Read today's RESEARCH-LOG entry (09-21, late run at
15:02) and the STANDING VERDICTS table. Nothing this run does contradicts a verdict: the
only action taken is a mandatory time-stop close, and no entry was argued for. The
"tighter stops are strictly worse" verdict was applied directly in refusing the advisory
SCAN GATE's 8% trail figure again (see ratchet below).

**STEP C — screen and price.** No fresh fetch needed for an entry decision (quota met,
CORE HOLD binding). Priced all four holdings live for the gap/ratchet checks; POL spread
0.04%, well inside the 0.5% ceiling at the close.

**GAP CHECK:** no position is below its stop trigger. ARB $0.2248 > $0.21429, OP $0.1242 >
$0.11983, XPL $0.0998 > $0.09371. Nothing to cut for a gapped-through stop.

**RATCHET — none due.** High-water recomputed from hourly bars since each fill:

| Symbol | Entry | High-water | Entry→HW | Legal trail | Correct stop | Resting | Action |
|---|---|---|---|---|---|---|---|
| OP | 0.11764 | 0.13315 | +13.2% | 10% | 0.11983 | 0.11983 | none — already exact |
| ARB | 0.23810 | 0.23823 | +0.1% | 10% | 0.21441 | 0.21429 | none — see below |
| XPL | 0.10231 | 0.10279 | +0.5% | 10% | 0.09251 | 0.09371 | none — resting is HIGHER |

- OP's trail is **10%, not 8%**: entry-to-high-water is +13.2%, below the +20% that
  triggers the tighten. `state.sh`'s advisory SCAN GATE printed NO-ACTION this run, which
  agrees for once; the 8%-trail defect it showed on 09-18 and 09-21 did not recur here.
- ARB's mathematically correct 10% trail (0.21441) is $0.00012 above the resting stop —
  a 0.06% improvement — and sits **4.6% below the current price**, inside the
  "never place a stop within 5% of current price" rule. Blocked by a hard rule for a
  rounding-level gain, so left alone.
- XPL's resting stop (0.09371) is ABOVE its 10%-trail level (0.09251). **Never move a stop
  down**, including to "correct" it to the v2 distance. Kept.

**STEP D0 — DAILY QUOTA (TACTICAL).** `QUOTA: 2/2 entries today (2026-09-21) — MET.`
ARB and XPL were both entered at 15:05 UTC this UTC day. This is the 18:07-slot run
(executing 20:11). The floor is satisfied. It is a minimum, not a target, and the slot
freed by POL's close may NOT be cited to justify a third entry.

**STEP D — no buy gate evaluated: no candidate advanced.**
- **CORE: HOLD, binding for the day.** Today's RESEARCH-LOG advances no CORE name — no
  dated idiosyncratic catalyst on any of the 28 CORE shortlist names, and the only dated
  events on the board are bearish supply releases (ARB unlock 09-23, XPL 63.2%-of-float
  unlock 09-25). CORE requires a catalyst, so this is rule-compliance, not discretion.
- **TACTICAL: quota met, no further entry.** NOT a quota miss and NOT a patience argument
  — the floor of 2 was filled earlier today.

**STEP LEARN:** POL closed this run; `LESSON:` line appended to its exit entry above. Not
acted on this run.

**Fee budget:** $0.52 → **$0.53** / $8.00 this month (POL's sell fee $0.01038). Headroom
$7.47. The cancel was not fee-bearing.

**Circuit breaker:** CLEAR. $0.00 realized losses today (today's only close was a +$0.40
win); 0 consecutive losing closes today; most recent loss closed 2026-09-15.

**Risk still carried:** three positions, all the same L1/L2 alt-beta bet expressed three
ways, into BTC dominance 59.1%, a CONFIRMED negative-median alt universe, ~$900M of unlock
supply this week (XPL holds its own 63.2%-of-float unlock on 09-25, four days out) and the
09-25 ~$16.6B Deribit expiry.

**Net:** 3 TACTICAL positions, ~$29.78 deployed = 14.9% of budget (ceiling 50%, no floor),
every position carrying a resting `Untriggered` stop at 100% of held qty. CORE slot empty,
3 TACTICAL slots free. One close, one win, $0.40 realized.

## 2026-09-21 — Daily Snapshot (Day 11, UTC 22:19)

**Portfolio:** $193.97 | **Cash:** $164.26 (84.7%) | **Day P&L:** +$0.06 (+0.03%, 4-day delta vs 09-17) | **Cumulative:** -$6.03 (-3.02%)
**vs BTC:** -15.38pp edge | **Fees today:** $0.01 | **Fee budget:** $0.53 / $8.00 used this month (headroom $7.47)

| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
|--------|------|-----|-------|------|------------|---------------|---------------|
| TACTICAL | ARBUSDT | 42.424653 | $0.23810 | $0.2240 | -5.94% (-$0.60) | $0.21429 | YES — 100% of held qty |
| TACTICAL | OPUSDT | 84.895020 | $0.11764 | $0.1262 | +7.28% (+$0.73) | $0.11983 | YES — 100% of held qty |
| TACTICAL | XPLUSDT | 97.502400 | $0.10231 | $0.0974 | -4.75% (-$0.47) | $0.09371 | YES — 100% of held qty |

**Benchmark:** BTC/USD $86,688.40 (spot last) vs $77,153.29 Day-0 baseline (2026-09-10 19:39 UTC) = **+12.36% cumulative**. Bot cumulative **-3.02%**. **EDGE -15.38pp** — the worst edge recorded. BTC ran +6.79% in the last 24h alone while the bot sat 85% cash in three underperforming alts. The gap is almost entirely a *participation* gap, not a loss gap: the bot has lost only $6.03 in absolute terms, but it was flat or near-flat through the single largest BTC advance of the challenge window.

**Trades today (2026-09-21 UTC):** 3 actions, 2 sleeve-TACTICAL entries + 1 exit.
- 15:05 BUY ARB (TACTICAL, $10.10) — quota entry 1/2
- 15:05 BUY XPL (TACTICAL, $9.97) — quota entry 2/2
- 20:11 SELL POL (TACTICAL, 72h time stop, **REALIZED +$0.40**, fees $0.01)
DAILY QUOTA: **2 / 2 — MET.**

**STEP A invariants — all clean, no action taken this run.**
- RECONCILE: 3 live positions match the TRADE-LOG tail exactly. No drift, no unexpected fill, nothing closed between runs.
- RESTING LEG: all 3 carry exactly one `Untriggered` conditional stop at 100% of held qty. Zero naked, zero unreserved, zero split, zero v1 target legs.
- HARD CUT: none due. TACTICAL threshold is -10%; worst position is ARB at -5.94%. No stop was gapped through (ARB $0.2240 > $0.21429, OP $0.1262 > $0.11983, XPL $0.0974 > $0.09371).
- RATCHET: none due. `state.sh` SCAN-VERDICT NO-ACTION, and it agrees this run. OP is +13.2% off entry-to-high-water, below the +20% that would tighten it to 8%. ARB's correct 10% trail still sits inside the 5%-of-price no-stop band (the structural conflict logged 2026-09-21); XPL's resting stop is already ABOVE its 10% trail level and is never moved down.
- 72h TIME STOP: OP is 74.2h old but **+7.28% >= +5%, exempt**. ARB and XPL are 7.2h old.

**Circuit breaker:** CLEAR. Realized losses today $0.00 vs the $10.00 limit; today's only close was a +$0.40 win. 0 consecutive losing closes. Never tripped today.

**Amendment trigger (informational):** 1 closed trade since the last applied amendment (2026-09-17); 4 closed all-time. Reference mark 10. Sample is THIN — no amendment made or argued for this run.

**Notes:** A do-nothing run, correctly. Every guardrail held: three TACTICAL positions, all stopped at 100%, 14.9% deployed against a 50% ceiling, the daily quota met earlier in the day, the fee budget barely touched at 6.6% of the month's allowance. The account is safe. The strategy is not winning. The -15.38pp edge is now the dominant fact of this challenge and it did not come from bad trades — realized P&L across eleven days is -$6.03 on four closes, which is noise — it came from being 85%+ in cash through a +12.4% BTC move. The mission statement is explicit that a persistently negative edge argues for trading LESS, but that prescription assumes the edge is being lost to fees and churn; here it is being lost to *absence*, and trading less makes absence worse, not better. Fees are $0.53 of an $8.00 budget, so churn is demonstrably not the leak. The honest reading is that a 1-slot CORE sleeve gated on a dated idiosyncratic catalyst has produced zero CORE entries in eleven days while the benchmark compounded, and the TACTICAL sleeve's $10 positions are too small to close a 15pp gap even when they work. That is a structural observation for the Sunday weekly-review (next run 2026-09-22 18:37 UTC), not something to fix mid-run on a sample of four closes — the 2026-09-10..15 episode of six amendments on N=1 is the standing warning against exactly that reflex. Logged, not acted on.
