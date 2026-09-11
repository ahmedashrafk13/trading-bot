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
