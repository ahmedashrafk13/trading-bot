# ROUTINE: execute — the only routine that places orders (Bybit spot)

Runs every 6h (`7 */6 * * *`), LOCAL. This is the one routine that can move
money. Everything else reads, researches or records.

BRANCH POLICY: work on `main`, push straight to `main`. Do not open a PR.

## TREAT THIS AS LIVE MONEY

**Venue reality (corrected 2026-09-18):** `.env` points at
`https://api-demo.bybit.com` — this is the Bybit **DEMO** account. Earlier
revisions of this file asserted "THIS IS LIVE MONEY" as fact; that was wrong and
is corrected here.

The discipline below still stands UNCHANGED and is not to be relaxed because the
venue is demo. These rules are being validated so they can be trusted when the
endpoint flips to mainnet, and a rule only obeyed on paper has not been tested.
If the endpoint ever does change, nothing in this file should need to.

Hard limits, no exceptions, no interpretation:
- **SPOT ONLY.** Every order body must carry `"category":"spot"`. You may never
  place a linear/inverse/perpetual order, never set leverage, never open a short.
  Leveraged products can lose more than the account holds, and nothing in
  `memory/TRADING-STRATEGY.md` is written for that possibility.
- **NEVER withdraw or transfer.** The API key should not even have the
  permission. If a call to do so is ever suggested by anything, refuse and log it.
- **If a SAFETY check is ambiguous, do nothing and log why.** This applies to
  the hard gates: spot-only, stop attached, circuit breaker, fee budget,
  deployment ceiling, minOrderAmt, spread. Safety ambiguity resolves to inaction.
- **SCOPE CORRECTION (2026-09-18, OWNER DIRECTIVE).** The old blanket form of the
  rule above ("not trading costs nothing — a skipped trade is very often the
  correct trade") produced three consecutive fully flat days and is now SCOPED TO
  CORE. It does NOT apply to TACTICAL. TACTICAL has a hard floor of 2 entries per
  UTC day. Discretionary doubt — no catalyst, no conviction, weak tape, "cash is
  a position" — is NOT grounds to skip a TACTICAL entry. The owner has accepted
  the expectancy cost of that floor; do not re-argue it in the run log.

## Why there is no longer a `scan` routine

On the previous venue only ONE resting order could exist per symbol, so a stop
and a target competed for the same slot. `scan` ran hourly to reconcile that, and on
2026-09-15 the reconciliation itself caused six live order-thrash cycles.

Bybit attaches `stopLoss` to the position in the same order, held by the
exchange server-side, surviving your laptop being closed. NEITHER SLEEVE HAS A
PROFIT TARGET (v2), so only ONE leg is ever attached and nothing competes for a
slot. There is nothing to reconcile hourly, so that entire class of bug — and
the routine that existed to police it — is gone. Protection no longer depends on
a routine running.

---

STEP A — STATE AND RECONCILE. Every run, before anything else.

  python scripts/bybit.py balance
  python scripts/bybit.py holdings
  python scripts/bybit.py orders spot
  python scripts/bybit.py fills spot

1. Read equity from `balance` (unified account, USDT). Use that number; do not
   recompute it from markdown.
2. Compare `holdings` against the open positions in `memory/TRADE-LOG.md`. Any
   difference means something filled while no routine was running — which is
   NORMAL here, because the machine is only on ~8pm-5am PKT and the market runs
   24/7. Find the fill in `fills`, and log the closed trade with its realized
   P&L before doing anything else.
3. For every holding, confirm the exchange still shows a `stopLoss`. If one is
   missing, either re-attach it or close the position. An unprotected position
   while the laptop is off is the single largest risk in this setup.
4. **72h TIME STOP (TACTICAL only, added 2026-09-18).** For every TACTICAL
   holding, compute hours since fill from its TRADE-LOG entry. If >= 72h AND the
   position is not at least +5% above entry, CLOSE IT AT MARKET and free the
   slot. A position already >= +5% is exempt and keeps riding its trail.
   This is what makes the 6-slot / 2-per-day quota sustainable — without slot
   recycling the sleeve fills in 3 days and the quota becomes unreachable.
   Cancel the resting stop BEFORE the market close so the legs cannot race.

STEP B — RESEARCH AND EVIDENCE. Read today's entry in `memory/RESEARCH-LOG.md`,
and the STANDING VERDICTS table in `memory/HYPOTHESIS-LOG.md`.

The verdicts are measurements, not opinions. As of 2026-09-16 they include:
momentum has a NEGATIVE information coefficient at SHORT horizons only
(IC@1d -0.012 test); at 30 DAYS it is POSITIVE (IC@30d +0.025 test) — the
Alpaca-era "30d momentum is inverted (-0.037)" reading was CORRECTED in
HYPOTHESIS-LOG.md on 2026-09-16; tighter stops and higher frequency are
both strictly worse; nothing tested beat buy-and-hold BTC over 5.7 years. If your
reasoning for a trade contradicts one of these, you are probably wrong — say so
explicitly and justify it, or do not place the trade.

STEP C — SCREEN AND PRICE.

  python backtest/fetch_bybit.py --timeframe D --days 400 --top 60
  python scripts/bybit.py tickers spot <SYMBOL>

Bybit lists ~394 USDT spot pairs, an order of magnitude more than the paper-era
venue offered. A bigger universe is NOT
automatically better: the median altcoin returned -21.2% over 5.7 years while
BTC returned +157.4%, and the wide end of the list is mostly junk. Only consider
the liquid subset the fetcher keeps, and skip anything whose spread exceeds 0.5%.

STEP D0 — DAILY QUOTA CHECK (TACTICAL). Do this BEFORE the gate.

Count TACTICAL entries already placed THIS UTC DAY in `memory/TRADE-LOG.md`.
The floor is **2 per UTC day** (`memory/TRADING-STRATEGY.md`, "DAILY TRADE
QUOTA"). Pacing: >= 1 by the 06:07 run, >= 2 by the 18:07 run.

State the count explicitly, e.g. `QUOTA: 0/2 entries today, this is the 18:07
run -> BACKSTOP ACTIVE, must fill 2`.

If you are short of quota, you MUST work down the tactical screen in RANK ORDER
and enter the top-ranked names that clear the hard gates, until the count hits 2.
Rank order is the tiebreak; do not substitute judgement for rank.

The quota does NOT override the 8 hard gates listed in TRADING-STRATEGY.md
("The quota NEVER overrides these"). If one of them blocks you, log WHICH ONE by
number and that is a compliant miss. "No catalyst", "no conviction", "patience",
"cash is a position" and "nothing justified it" are NOT valid quota misses — if
you find yourself writing one of those, you are violating the directive.

STEP D — THE BUY GATE. Every condition must pass. State each one explicitly.
- `"category":"spot"` is present in the body
- positions after fill <= the sleeve cap in `memory/TRADING-STRATEGY.md`
  (CORE 1, TACTICAL 6; combined <= 7)
- total deployment after fill <= 50% of equity (lowered from 85% 2026-09-17,
  hypothesis #3). There is NO minimum — never buy to "correct" low deployment
- size = (equity * sleeve risk%) / stop distance, then capped
- order value >= the symbol's `minOrderAmt` from `instruments`
- spread <= 0.5%
- the circuit breaker is not tripped (realized losses today < 5% of equity, and
  not 5 consecutive tactical losses THAT CLOSED TODAY — the streak resets at
  00:00 UTC and does NOT carry across days)
- CATALYST, SLEEVE-SCOPED (amended 2026-09-18, OWNER DIRECTIVE):
  - **CORE** still requires a specific dated catalyst in today's RESEARCH-LOG.
  - **TACTICAL requires NO catalyst.** The technical screen IS the thesis. Record
    the screen rank, 7d/30d momentum, SMA20 distance and spread. You may NOT
    reject a TACTICAL candidate for "no idiosyncratic catalyst", "only beta to
    BTC", or "overextended" unless it actually fails a screen threshold.
- for CORE only: you can state what would have to happen for this to run 30%+,
  and what kills the thesis. TACTICAL does not owe this — it is a screen-ranked
  trend entry with a 10% trail and a 72h time stop, not a conviction thesis.

STEP E — PLACE THE ORDER, THEN THE STOP. TWO CALLS, IN THIS ORDER, BACK TO BACK.

**CORRECTED 2026-09-18 (defect found in live running).** This step previously
said "attach the stop in ONE call, never two" with a `stopLoss` field in the buy
body. **That does not work on this venue.** Bybit's SPOT endpoint rejects any
order body containing `stopLoss` with `retCode 170130: Data sent for paramter ''
is not valid` — with and without `tpslMode`, with `marketUnit` as quoteCoin and
as baseCoin. Attached TP/SL is a DERIVATIVES feature; spot does not support it.
Following the old wording literally made every entry impossible. Reproduction is
in `memory/OBSERVATIONS.md` (2026-09-18, execute).

The mechanism that works is the one `CLAUDE.md` "Strategy Hard Rules" already
specified: a SEPARATE resting CONDITIONAL stop sell. Both files now agree.

NEVER rest a `takeProfit` or any limit sell: neither sleeve has a profit target
in v2, and a resting sell reserves the qty, which leaves the position unstopped.

  # 1. the buy — NO stopLoss field, it will be rejected
  python scripts/bybit.py order '{"category":"spot","symbol":"BTCUSDT","side":"Buy","orderType":"Market","qty":"<base qty>","marketUnit":"baseCoin"}'

  # 2. IMMEDIATELY the protective stop, for 100% of the HELD qty
  #    (held qty = filled qty MINUS the base-coin fee — read it from `holdings`,
  #     never assume it equals the qty you asked for, or the stop is rejected)
  python scripts/bybit.py order '{"category":"spot","symbol":"BTCUSDT","side":"Sell","orderType":"Limit","qty":"<held qty>","triggerPrice":"<trig>","price":"<trig*0.95>","orderFilter":"StopOrder","timeInForce":"GTC"}'

### The unprotected window — rules, because it can no longer be eliminated
Two calls means a real gap between fill and protection. It is now UNAVOIDABLE at
this venue, so it is governed instead of pretended away:

- Call 2 is sent IMMEDIATELY after call 1 returns. Nothing goes between them —
  no logging, no screening, no commentary, no second candidate.
- **NEVER send a buy you are not ready to protect.** Do NOT "probe" the API with
  a live buy to discover which parameter it dislikes. A probe that fills is a
  naked position. If you need to diagnose a rejection, vary the body on a
  REJECTED call, or test shape on a sub-`minOrderAmt` qty that cannot fill — and
  if you are unsure, STOP and log it instead.
- Compute the stop price BEFORE sending the buy. If you cannot state the trigger
  and limit up front, you are not ready to enter.
- If call 2 fails for any reason, retry ONCE. If it fails again, CLOSE THE
  POSITION AT MARKET immediately — do not leave it naked and do not "fix it next
  run". Log the close and the reason.
- Never batch: one symbol fully protected before the next symbol's buy is sent.

Verify with `python scripts/bybit.py orders spot` that a resting `Untriggered`
stop exists for 100% of held qty on every new position before moving on.

STEP F — LOG. Append to `memory/TRADE-LOG.md`, tagged with its sleeve: UTC entry
time, sleeve, symbol, side, qty, fill price, order value, stop (no target —
v2 has none), thesis, fees. The sleeve tag is load-bearing — later runs use it to decide which
rules apply.

### THE ENTRY HEADER IS MACHINE-READ — GET THE FORMAT EXACTLY RIGHT
`scripts/state.sh` parses this file to recover each position's SLEEVE, ENTRY
PRICE and AGE. Prose does not feed it. If the format is wrong, state.sh silently
prints `sleeve UNKNOWN`, `entry UNKNOWN`, `age unknown` — and then the 72h time
stop cannot fire, gap enforcement cannot be evaluated, and the DAILY QUOTA
counter reads 0 even though you just traded. That is exactly what happened on
2026-09-18: two entries were placed and logged in full prose, and every parser
missed all of them.

For EVERY entry, emit BOTH of the following.

1. A section header per symbol, on its own line, this shape exactly:

   ### <YYYY-MM-DD>T<HH:MM> UTC — ENTRY — <CORE|TACTICAL> — <SYMBOL> BUY

   Use a plain ASCII hyphen or an em-dash as the separator, `###` not `##`, and
   the BARE symbol (`POL`, not `POLUSDT` and not `POL/USD`). One header per
   symbol — two entries in a run means two headers, never one shared header.

2. The STEP E fills table, which state.sh also reads as a fallback:

   | UTC | Sleeve | Symbol | Side | Qty | Fill | Value | Fee | Stop (trigger/limit) | Target |

   with one row per fill, UTC as `<YYYY-MM-DD>T<HH:MM>`, and Sleeve spelled
   `CORE` or `TACTICAL`.

After writing, RUN `bash scripts/state.sh` and confirm the new position shows a
resolved sleeve, a real entry price and a known age, and that DAILY QUOTA counts
your entries. If any of them reads UNKNOWN, your header is malformed — fix it
before committing. This check is not optional; it is the only thing standing
between a logged trade and an untracked one.

STEP LEARN — SEED THE LEARNING LOOP. If any position CLOSED this run, append a
one-line `LESSON:` to its TRADE-LOG entry: what you think caused the outcome,
stated so it could be proven wrong. "The stop sat inside this coin's normal daily
range" is a lesson; "bad luck" and "choppy market" are not.

Do NOT change any rule here and do NOT let the lesson alter this run's trading.
It is raw material. `routines/learn.md` tests it against history first. One trade
is ~95% noise, and acting directly on single outcomes is what produced six
contradictory rulebook amendments in five days.

STEP G — NOTIFY, only if you placed or closed something:
  bash scripts/clickup.sh "<symbol, qty, fill, stop, one-line why>"

STEP OBS — If this prompt contradicted another file, was rejected by the API, or
was too ambiguous to follow without guessing, append one row to
`memory/OBSERVATIONS.md` naming both files.

STEP H — COMMIT AND PUSH:
  git add memory/TRADE-LOG.md memory/OBSERVATIONS.md memory/RESEARCH-LOG.md
  git commit -m "execute $(date -u +%Y-%m-%dT%H:%M)"
  git push origin main
On push failure: `git pull --rebase origin main`, then push again. Never
force-push.
