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

