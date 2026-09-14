# Research Log

Daily pre-market research entries will be appended here.
Format each entry:

## YYYY-MM-DD — Pre-market Research

### Account
- Equity: $X
- Cash: $X
- Buying power: $X
- Daytrade count: N

### Market Context
- WTI / Brent:
- S&P 500 futures:
- VIX:
- Today's catalysts:
- Earnings before open:
- Economic calendar:
- Sector momentum:

### Trade Ideas
1. TICKER — catalyst, entry $X, stop $X, target $X, R:R X:1
2. ...

### Risk Factors
- ...

### Decision
TRADE or HOLD (default HOLD if no edge)

## 2026-09-10 — Pre-market Research (OFF-CYCLE local run, ~14:40 ET, market open)

> Run context: executed manually via /pre-market at 14:40 ET, ~80 min before the
> close — not the scheduled 06:00 CT slot. Perplexity unconfigured, so research
> used the native WebSearch fallback (no Perplexity citations). Date taken from
> the Alpaca market clock, NOT the local machine clock, which is 12h fast.

### Account
- Equity: $200.00
- Cash: $200.00 (settled, cash account — multiplier 1)
- Buying power: $200.00
- Daytrade count: not reported (cash account; PDT N/A)
- Positions: none. Open orders: none.

### Market Context
- WTI / Brent: Brent settled $101.21 (+3.4%) on 9/9, highest since July; renewed
  Iran-U.S. attacks near the Strait of Hormuz driving energy supply fear.
- S&P 500: closed 7,636.36 (-37.16, -0.5%) on 9/9. S&P and Nasdaq declining again
  today on the oil move.
- VIX: ~16.3-17.6, up ~7% intraday. Near 10-yr average — no panic, but hedging
  demand is picking up into a seasonally volatile stretch.
- Today's catalysts: PPI released 08:30 ET today. Treasury yields at 52-week highs.
- Economic calendar: **CPI tomorrow (Fri 9/11) 08:30 ET** — the dominant near-term risk.
- Sector momentum: Energy leading (oil shock). Tech slumping. Rate-sensitives
  pressured by the yield move.

### Candidates screened (live Alpaca quotes, $40 whole-share ceiling)
| Ticker | Ask | Spread | Verdict |
|--------|-----|--------|---------|
| HAL  | 36.13 | 0.03% | PASSES — 1 sh = 18.1% of equity |
| KMI  | 31.19 | 0.03% | PASSES — 1 sh = 15.6% of equity |
| RIG  |  5.76 | 0.17% | PASSES — 6 sh = $34.56 (17.3%) |
| CTRA | 34.54 | 11.32% | SKIP — spread far too wide (see feed caveat) |
| OKE  | 99.35 | 3.93% | SKIP — over $40 cap AND wide spread |
| DVN  | 49.81 | 0.02% | SKIP — over the 20% cap ($40) |
| APA  | 44.89 | 0.02% | SKIP — over the 20% cap ($40) |
| SLB  | 56.12 | 0.02% | SKIP — over the 20% cap ($40) |

### Trade Ideas (WATCHLIST ONLY — not actionable today)
1. HAL — oilfield services levered to a sustained crude bid. Entry <= $36.50,
   stop $33.96 (-7%), target $41.58 (+14%), R:R 2:1. Needs oil strength to hold
   through CPI.
2. KMI — midstream, lower beta, steadier than E&P on an oil spike. Entry <= $31.40,
   stop $29.20 (-7%), target $35.80 (+14%), R:R 2:1.
3. RIG — speculative offshore driller, highest beta to crude of the three. Only
   with a smaller size; skip if CPI turns risk-off.

### Risk Factors
- CPI tomorrow 08:30 ET is binary and unhedgeable at this size. A hot print with
  yields already at 52-wk highs is the obvious downside path.
- Oil is 3 days into a geopolitical spike. Buying day 3 of a headline move is
  chasing; Hormuz headlines mean-revert violently on any de-escalation.
- 80 minutes to the close is not enough time for a thesis to work, and a same-day
  buy leaves the stop exposed to an overnight gap that trailing stops do not cover.
- T+1 settlement: all $200 is settled now, but any exit locks proceeds until the
  next business day.

### Decision
**HOLD.** No orders. Three independent reasons: this is an off-cycle run with 80
minutes left in the session, CPI lands tomorrow pre-open, and the leading sector is
mid-spike rather than early. Re-evaluate at the 06:00 CT pre-market run tomorrow
AFTER the CPI print is known. Patience > activity.

---
## 2026-09-10 — PIVOT: stocks -> crypto
The entry above (HAL/KMI/RIG energy screen) is from the stocks era — historical
only, do not act on it. The account now trades crypto USD pairs exclusively.
Next research run screens crypto pairs against the new gate.

---
## 2026-09-10 — Crypto Research (local run, 19:39 UTC)

> Perplexity unconfigured -> native WebSearch fallback, no Perplexity citations.
> Date from the Alpaca clock (19:39 UTC); the machine clock is 12h fast.
> First run under the two-sleeve model.

### Account
- Equity: $200.00 | Cash: $200.00 | Deployed: 0%
- Positions: none. Open orders: none. Stop coverage: N/A.
- Capacity: CORE 3 slots ($120), TACTICAL 3 slots ($80). Trades used: 0/3 wk, 0/3 day.

### Market Context
- BTC $77,155 (screen) / ~$78,039 earlier, -1% on 24h. ETH $2,464, -0.7%.
- Global market cap -0.9% to $2.76T. Both majors opened at week lows.
- **FOMC starts Tuesday with a 62.2% implied chance of a RATE HIKE.** Higher
  rates are directly negative for crypto.
- **CPI tomorrow (2026-09-11) 08:30 ET**, after today's PPI. Last inflation
  reads before the Fed decides.
- Macro backdrop from the equity session: Brent >$100 on Iran/Hormuz, Treasury
  yields at 52-week highs. Risk-off, not risk-on.

### Universe screen (all 33 pairs — scripts/screen.sh)
CORE shortlist, daily bars (5): DOT XTZ SUSHI GRT UNI
TACTICAL shortlist, hourly bars (19): SKY UNI POL ETH RENDER LDO TRUMP SOL AAVE
CRV SHIB DOT GRT YFI ADA ARB FIL DOGE LINK

Read the tactical list carefully: the hourly 30-period momentum is NEGATIVE for
every single one of the 33 coins (-0.4% to -11.9%). All 19 "passes" are a ~7-hour
bounce inside a 30-hour downtrend, driven by one macro move. They are not 19
independent setups — they are one correlated setup wearing 19 tickers. Taking 3
tactical positions here would be three bets on the same bounce.

### Candidate notes
- DOT — the only strong catalyst in the universe: OpenGov Referendum 1944 for a
  native stablecoin (dotUSD) at ~97.5% in favour, a 150% transaction spike and
  record XCM throughput on 9/7, plus a short-liquidation squeeze. But +24% on
  the week and +18.1% over SMA20 — it barely clears the <=20% extension filter,
  and a squeeze-driven leg is exactly the kind that retraces.
- XTZ — Tezos X mainnet targeted for summer 2026, named an altseason contender
  on 8/23. Real but vague; no dated near-term catalyst.
- SUSHI / GRT / UNI — pass on trend mechanics with no specific catalyst found.
  Gate requires a documented catalyst, so none are entry-eligible today.

### Risk Factors
- A 62% probability of a rate hike is the single most important fact here, and
  it lands 2 trading days out. CORE holds are weeks-long by design; opening one
  into that is choosing the worst entry window available.
- CPI tomorrow pre-open. A tactical 6% stop is well inside a normal CPI-day
  range for alts, so a stop-out is likelier than a 12% target being reached.
- Everything is correlated to the same macro driver, so position count would
  overstate diversification.
- Fees: 3 tactical round trips cost ~1.05%/wk of the account. Paying that to
  express one macro guess is poor value.

### Decision
**HOLD both sleeves. No orders.**
- CORE: HOLD. Only DOT has a real catalyst and it is extended after a squeeze,
  two days before a probable hike. Waiting costs nothing; the dotUSD narrative
  is not a one-day event.
- TACTICAL: HOLD. 19 nominal passes are one correlated bounce, and CPI tomorrow
  makes a 6% stop a coin flip.

### Triggers for the next run (2026-09-11, post-CPI)
1. CPI printing at or below expectations AND hike odds falling below ~50%
   -> re-screen; DOT becomes CORE-eligible if it has cooled to <=12% over SMA20.
2. CPI hot / hike odds rising -> stay flat. Do not "buy the dip" into a hiking
   Fed; that is not a catalyst, it is hope.
3. Tactical entries only once hourly 30-period momentum turns positive for the
   candidate, so the bounce is confirmed rather than assumed.

### 2026-09-10 20:20 UTC — Intraday addendum (execute run, tactical origination attempted)

First run with tactical origination authority. Outcome: **NO TRADE**, blocked by
the gate — and the blocking rule exposed a defect in the strategy itself.

State: flat, equity $199.92, fee budget $0.00/$3.00 used, breaker clear,
0 of 3 tactical slots filled. Nothing structural prevented a trade.

Tactical shortlist (12): UNI SKY POL DOT ETH TRUMP RENDER AAVE SHIB SOL DOGE YFI
Best candidate: DOT — on the shortlist, spread 0.21%, and the only coin in the
universe with a specific documented catalyst (OpenGov Referendum 1944 for a
native dotUSD stablecoin at ~97.5% in favour, 150% transaction spike, record XCM
throughput).

It failed on R:R after fees:
- notional $20.00, round-trip fee at measured 0.65% = $0.13
- risk if the 6% stop fills: $1.20 + $0.13 = $1.33
- reward if the 12% target fills: $2.40 - $0.13 = $2.27
- R:R = **1.71 : 1**, against a required 2:1 -> FAIL

**DEFECT: the tactical sleeve's own parameters cannot satisfy the gate's own R:R
rule.** A 6% stop with a 12% target is 2:1 gross, but fees are charged on both
legs, so after friction it is 1.71:1. This is not specific to DOT — EVERY
tactical trade fails this check by construction, at any notional, because the
ratio is set by the parameters and not by the candidate. The tactical sleeve as
specified could never have placed a single trade.

To satisfy 2:1 after fees, one of:
- target 14.0% instead of 12% (keeps the 6% stop, needs a bigger move), or
- stop 5.0% instead of 6% (keeps the 12% target, tighter and more whipsaw-prone)

Not self-amending this: the weekly review is the amendment path and it requires
3+ closed trades as evidence, of which there are zero. Flagged for human decision.

Note also that the fee budget worked as intended in the opposite direction: it
was NOT the binding constraint. $0.13 of a $3.00 weekly budget is trivially
affordable — the trade was refused on edge quality, not on cost, which is the
correct order of priority.


---
## 2026-09-11 — Crypto Research (UTC 15:13)

**Account:** Equity $198.95 | Cash $179.92 | Deployed 9.6% (target 75-85%)
Positions: DOT (TACTICAL) -4.59%, age 18.9h, [SPLIT ok] 0% unreserved.
Fee budget $0.13 / $2.98 used. Breaker clear. Amendment trigger 0/10 — not eligible.

**Market context (WebSearch; PERPLEXITY_API_KEY not set — fallback used, noted per prompt):**
- BTC $78,605 (Alpaca) — down ~1.6% 24h; global mcap $2.7T, -1.9% 24h
- BTC dominance 56.8%, ETH 11% — capital rotating INTO the majors, not out the risk curve
- August PPI +0.4% m/m, +5.4% y/y — hotter than expected, cooled rate-cut hopes
- BTC spot ETFs -$282.56M, worst outflow since July
- **CPI prints TODAY (Sep 11); FOMC decision Sep 16** — the two binding near-term events
- ETH spot ETFs diverging the other way: ~+$863M net YTD vs ~-$1B for BTC; ETH has
  out-gathered BTC two consecutive months; Sep 4 BlackRock ETHA +23.06K ETH

**Narratives:** Majors leading (ETH specifically, on flows). L1/L2 rolling over — DOT,
ADA, XTZ, AVAX all failing one or both screens. Memes mixed and macro-fragile.

**CORE shortlist (15):** DOT SUSHI XTZ ARB GRT FIL ETH LTC AVAX BAT UNI LINK SOL CRV LDO
**TACTICAL shortlist (23):** ETH UNI AAVE PEPE FIL LINK HYPE SOL ARB WIF XRP TRUMP ONDO DOGE SUSHI YFI RENDER LDO POL BTC ADA CRV GRT

ETH is the only pair passing BOTH screens with a top-tier spread:
  CORE 1D: 7d +6.1%, 30d +38.9%, +5.5% vs rising SMA20 (limit 20% — not extended), spr 0.03%
  TACTICAL 1H: 7d +5.3%, +5.0% vs SMA20, vol 1.4% (in 0.4-6% band), spr 0.03%

### Ideas by sleeve

**CORE — ETH/USD — TRADE**
- Catalyst: ETF flow divergence is specific, measurable and sustained — ETH spot ETFs
  ~+$863M net YTD against ~-$1B for BTC, two straight months of out-gathering BTC,
  BlackRock ETHA +23.06K ETH on Sep 4. Glamsterdam upgrade proposals ahead.
- Entry ~$2,609 | Size $40 (20% of equity) | Stop trigger $2,087.60 / limit $1,983.22
- Target: none — CORE lets it run; the ratcheted 20% trail decides the exit
- Risk in dollars: $8.00 at the 20% trail; hard cut -15% = $6.00. Sane at this size.
- Est. round-trip fee $0.26 (0.65% of $40); spread 0.027% is the cheapest in the universe

**TACTICAL — HOLD, no new entries**
- CPI lands today and FOMC is Sep 16. A tactical position has an hours-to-2-day
  horizon, which puts the whole thesis on a macro print rather than on the setup.
  That is a coinflip, not an edge, and it is exactly the churn the fee budget exists
  to stop. The screen passing is not by itself a reason.
- What would change it: CPI printing and the tape holding, with a coin on the hourly
  shortlist carrying its own catalyst rather than borrowing the market's.
- DOT held, not added to: catalyst (dotUSD referendum, XCM throughput highs) is still
  intact so the thesis is not broken, but momentum has rolled over and it now FAILS
  the hourly screen (-5.9% 7d, -4.5% vs SMA20). Age 18.9h is inside the 48h reassess
  window and the -6% stop is resting. Let the stop do its job; no averaging down.

**Risk factors:** CPI today + FOMC Sep 16 either could break the tape. Hot PPI already
landed. BTC ETF outflows show majors bid is not uniform. ETH entered into a risk-off
session — sized and stopped accordingly, and the CORE horizon is weeks-to-months, so a
single print is noise against a 20% trail.

**Decision:** CORE **TRADE** (ETH $40). TACTICAL **HOLD**.
**Fee budget after this trade:** $0.39 / $2.98 used this week.

---
## 2026-09-14 — Crypto Research (INTRADAY ADDENDUM, execute run, UTC 16:45)

No pre-market research ran today (no cloud cadence). This addendum exists to
document a TACTICAL origination before execution, per the execute STEP B(d) rule.
**No CORE entry is considered** — CORE requires the morning research plan, and
there is none.

### Ideas by sleeve

**TACTICAL — XRP/USD — TRADE**
- Catalyst: the U.S. Senate holds its first floor test of the **Digital Asset
  Market Clarity (CLARITY) Act on 2026-09-15**, one day out. The Senate returned
  2026-09-14 with three weeks of floor time. This is a procedural cloture-style
  vote on whether to proceed to debate, not final passage. Secondary September
  catalysts already landed: the XRPL 3.3.0 upgrade and the fixCleanup3_3_0
  amendment, plus a custodial-fund unlock.
- Why this is XRP's own catalyst and not a borrowed macro print: the 2026-09-11
  research refused tactical entries because CPI/FOMC put the thesis on a market-wide
  coinflip. The CLARITY Act is crypto-legislation-specific and XRP is the highest-beta
  name to US regulatory clarity, given its litigation history. It is dated, public and
  lands inside the tactical hours-to-2-day horizon rather than after it.
- Technicals: PASSES the hourly TACTICAL screen (7d +0.7%, +2.3% vs SMA20, vol 0.4%/h,
  spread 0.298% live). Trading above EMA20/50/200 on the daily.
- Entry ~$1.4134 | Size $20 (10% of equity) | Stop trigger $1.3286 / limit $1.2622
- Target $1.6113 (+14% on fill)
- Est. round-trip fee $0.13 (0.65% of $20)
- R:R after fees: risk $20*0.06 + 0.13 = $1.33; reward $20*0.14 - 0.13 = $2.67 -> **2.01:1 PASS**

**CORE — no entry.** No morning research plan exists today, so no CORE origination
is permitted regardless of the screen. ETH/USD is held, split legs intact.

**Risk factors:** the vote is a BINARY, DATED event inside the holding window. A
failed motion to proceed is a plausible downside gap and a stop_limit can be gapped
through. Sized at $20 (10%, half of a CORE position) and stopped at 6% specifically
because the event risk is known in advance, not discovered later. This is the
acknowledged cost of trading a scheduled catalyst rather than a drift setup.

**Decision:** TACTICAL **TRADE** (XRP $20). CORE **HOLD**.

---
## 2026-09-14 — Crypto Research (UTC 19:56, broker clock)

**Account:** Equity $197.67 | Cash $138.30 | Deployed 30.0% (target 75-85%)
Positions: ETH (CORE) -2.79%, [SPLIT ok] 0% unreserved (75% stop / 25% target,
no-scan-cadence clause still in force — no `scan <timestamp>` commit found in
`git log`). XRP (TACTICAL) +3.13%, [SPLIT ok] 0% unreserved (50/50, below the
+6% ratchet trigger). Both stops verified resting, no orphans, no hard-cut breach.
Fee budget $0.52 / $2.97 used this week, headroom $2.45. Breaker clear (realized
$0.00 vs $5.93 limit, 0 consecutive losses). Amendment trigger 0/10 — not eligible.

**Note on tooling:** `PERPLEXITY_API_KEY` is a template placeholder
(`your_perplexity_...`), so `scripts/perplexity.sh` correctly exited 3 on every
query — fell back to native WebSearch per the prompt, as it did on 09-11.
Also fixed two script bugs blocking this run: `scripts/screen.sh` had lost its
executable bit (blocked its own `"$0" --sleeve core` self-invocation) and
contained a same-quote nested f-string (`f'...{os.environ.get('TF', '1D')}...'`)
that is a syntax error before Python 3.12 — this container runs 3.11. Both fixed
so the screen would run at all; logged here rather than silently patched.

**Market context (WebSearch fallback):**
- BTC $79,012 (Alpaca) / ~$77.8-79.0k cross-source — up ~1.9-2% since midnight UTC.
  Trading above EMA20/50/200, structurally bullish, but daily MACD histogram
  negative (deceleration) and ATR14 ~$2,077 (elevated 2-way volatility).
- **BTC dominance 58.88%**, up from 56.8% on 09-11 — capital continuing to
  concentrate into majors, not rotating out the risk curve.
- BTC spot ETFs: -$462.7M net for the week (4th straight outflow day, worst
  single day -$282.7M), but September still net +$307.3M — a weekly wobble
  inside a positive month, not a trend reversal yet.
- ETH spot ETFs: +$196.9M net for the week, single-day high +$216.4M on 09-11
  (BlackRock ETHA +$148.8M) — ETH continues out-gathering BTC on flows, same
  divergence that justified the 09-11 CORE entry.
- ETH price ~$2,540, Glamsterdam upgrade mainnet slipped to Q4 2026 (Sepolia
  testnet fork now Sep 28) — no new near-term ETH-specific catalyst since entry;
  thesis (ETF flow divergence) intact, unchanged.
- **FOMC Sep 16 (2 days out): odds of a 25bp HIKE now 80-87%**, up sharply from
  the 09-11 framing ("hike odds falling below ~50%" was the de-risking trigger).
  Hot August CPI/PPI and strong payrolls are driving this. This is a bigger
  near-term risk than 09-11 anticipated, not a smaller one — a hike is a genuine
  headwind for risk assets, not a coin-flip resolved in crypto's favor.
- CLARITY Act: Senate cloture vote (motion to proceed to H.R. 3633) is
  **tomorrow, Sep 15, 2:15pm ET** — still procedural, needs 60 votes, not final
  passage. This is the exact catalyst behind the held XRP tactical position;
  no new information changes that thesis, still pending.
- Token unlocks this week (~$746M, led by LayerZero, Bedrock) don't touch any
  held or shortlisted pair.

**Narratives:**
- Leading: Majors (BTC dominance rising). DeFi showing a short-term bounce —
  UNI/AAVE/LINK/CRV all clear BOTH sleeve screens with real 7d momentum — but
  against a YTD DeFi TVL decline of ~37% and Aave TVL down ~43% since an April
  hack; AAVE's cited catalysts (Kalshi AAVE futures listing Sep 4, Ethena USDH
  stablecoin integration Sep 9) are 5-10 days old and already reflected in its
  +52% 30d move, not a fresh catalyst — this reads as chasing an extended bounce,
  not entering early. Payments/legacy alive via the XRP position already held.
- Rolling over: L1/L2 broadly — ARB shows +93% 30d but -17.2% 7d (already
  reversing hard despite still clearing the daily filter), DOT -4.5% 7d (just
  closed a losing tactical trade in this narrative, 1/2 toward the exit-narrative
  rule), AVAX/SOL/ADA all 7d-negative. Memes and Infra/AI narratives fail both
  screens almost across the board (RENDER, GRT, FIL, HYPE, BAT, DOGE, SHIB, PEPE,
  BONK, WIF, TRUMP) despite AI-agent narrative getting heavy financial-media
  coverage this month — the coverage is not showing up in this universe's price
  action yet, which is exactly the "news is late" trap the screen exists to catch.

**CORE shortlist (18, daily bars):** XTZ BAT XRP ETH BTC SOL AAVE LTC SHIB UNI
ADA CRV DOT GRT AVAX SUSHI LINK ARB
Key metrics (7d% / 30d% / vsSMA20 / spread%): XTZ +17.2/+39.3/+15.5/0.58 (extended),
XRP +4.5/+45.9/+4.9/0.37, ETH +2.0/+35.0/+2.6/0.03 (held), BTC -0.1/+25.4/+0.6/0.03,
AAVE -0.8/+52.2/+2.6/0.18, ARB -17.2/+93.0/+7.8/0.35 (rolling over).

**TACTICAL shortlist (15, hourly bars):** UNI XRP ARB AAVE LINK CRV ONDO PEPE
WIF ADA SUSHI SKY SHIB TRUMP RENDER
Key metrics (7d% / vsSMA20 / vol%/h / spread%): UNI +6.6/+5.0/1.0/0.17,
XRP +4.8/+4.6/1.0/0.40 (held), ARB +4.4/+2.6/0.8/0.35, AAVE +4.4/+3.5/0.6/0.23,
LINK +3.6/+2.6/0.4/0.16.

**Ideas by sleeve**

**CORE — HOLD, no new entry.** ETH is the only position with a specific, live
catalyst (ETF flow divergence, unchanged). Nothing else on the CORE shortlist
has a catalyst that is both specific and NOT already priced in days ago (AAVE)
or already reversing (ARB, XTZ extended). Committing new $40 two days ahead of
an 80-87%-priced hawkish FOMC surprise, into a name with no catalyst of its own,
is exactly the market-wide-coinflip pattern the 09-11 research refused for
TACTICAL — it applies here too, just on CORE's wider stop.
What would change it: a coin on this shortlist develops its own dated catalyst
(upgrade, listing, flow data) independent of the Fed outcome, or FOMC resolves
and the tape holds/rallies through it, removing the two-day overhang.

**TACTICAL — HOLD (recommendation only).** XRP is already held at 1/3 tactical
slots into the same CLARITY Act catalyst; adding a second position ahead of the
same binary vote concentrates the sleeve on one event rather than diversifying
it. No other shortlisted tactical coin (UNI, ARB, AAVE, LINK, CRV, etc.) has a
dated catalyst of its own today — their moves are DeFi-bounce momentum, not
event-driven, and the imminent FOMC hike risk argues against adding pure-momentum
risk in the next 48h regardless.
What would change it: the CLARITY cloture vote passes tomorrow and a second
crypto-legislation-sensitive name (also payments/legacy or a name with its own
regulatory angle) sets up on the hourly screen, or FOMC prices down further and
a fresh hourly setup with its own catalyst appears post-decision.

**Risk factors:** FOMC Sep 16 hike odds 80-87% (up from ~09-11 framing) is the
dominant 48h risk for both open positions and any new entry. CLARITY cloture
vote Sep 15 is binary and can gap XRP either direction; existing stop can be
gapped through per the documented stop_limit risk. BTC ETF outflows persisting
a 4th day. DeFi bounce (UNI/AAVE/LINK/CRV) sits on top of a -37% YTD TVL
decline — treat as short-covering/rotation, not a confirmed reversal, until it
survives a full week.

**Decision:** CORE **HOLD**. TACTICAL **HOLD** (recommendation; execute run may
still originate if a fresh catalyst appears and the screen still passes).
**Fee budget:** $0.52 / $2.97 used this week, unchanged this run (no trade placed).

---
## 2026-09-14 — Crypto Research (UTC 20:26, broker clock)

**Account:** Equity $199.13 | Cash $138.30 | Deployed 30.5% (target 75-85%)
Positions: ETH (CORE) -0.05%, [SPLIT ok] 0% unreserved (75% stop / 25% target).
XRP (TACTICAL) +4.97%, [SPLIT ok] 0% unreserved (50/50) — below the +6% ratchet
trigger, no action this run. Both stops verified resting via `alpaca.sh orders`,
qtys match TRADE-LOG, no orphans, no hard-cut breach. Fee budget $0.52 / $2.99
used this week, headroom $2.47. Breaker clear (realized $0.00 vs $5.97 limit,
0 consecutive losses). Amendment trigger 0/10 — not eligible.

**Note on tooling:** `PERPLEXITY_API_KEY` is still the template placeholder
(`your_perplexity_api_key_here`) — `scripts/perplexity.sh` exited 3 on the
first query as designed; fell back to native WebSearch for all queries per the
prompt, as in the two prior research runs.

**What changed since the 19:56 UTC entry today (30 min ago):** Senate
Republicans released revised CLARITY Act text and are calling it their "final
offer" to Democrats ahead of tomorrow's cloture vote, which raised market-implied
odds of the bill advancing. That optimism is now visibly in the screen: the CORE
shortlist widened 18->21 names and the TACTICAL shortlist widened 15->23 names
versus the prior run, with broad green across majors and alts rather than a
single-name move. Nothing has resolved yet — this is pre-vote optimism, not a
result.

**Market context (WebSearch fallback):**
- BTC $79,438 (Alpaca feed) / ~$77.8k cross-source, dominance **58.88%**
  (unchanged from 19:56 entry) — still above EMA20/50/200, daily MACD histogram
  still negative (deceleration), ATR14 ~$2,077.
- ETH $2,604 (Alpaca) / ~$2,499-2,540 cross-source, base case still sideways
  $2,400-$2,600 pending macro. Ethereum spot ETFs: 4th straight week of net
  inflows ($196.9M this week, $216.4M single-day high 09-11, BlackRock ETHA
  leading) — ETF-flow-divergence thesis for the held ETH position is intact,
  unchanged.
- Bitcoin spot ETFs: -$462.7M net for the week, 4th straight outflow day, but
  September still net +$307.3M — unchanged framing from 19:56 entry.
- **FOMC decision is tomorrow-into-Friday, Sep 15-16, announcement Sep 16.**
  Hike-odds estimates are noisy across venues (Polymarket ~80%, Kalshi ~57%,
  CME FedWatch >60%) but every source has a 25bp hike as the leading or
  co-leading outcome — same elevated-risk framing as the 19:56 entry, not
  resolved, still the dominant 48h overhang for both open positions and any
  new entry.
- **CLARITY Act cloture vote is tomorrow, Sep 15, 2:15pm ET** — still a
  procedural motion-to-proceed needing 60 votes, still not final passage.
  This is the exact catalyst behind the held XRP tactical position; today's
  "final offer" text is incrementally bullish for the vote passing but the
  vote itself has NOT happened. XRP $1.4818, up from $1.41 at entry Friday,
  position now +4.97% (below the +6% ratchet trigger).
- Token unlocks this week: ~$746.5M led by LayerZero (Sep 20, ~$26M),
  Bedrock, plus Arbitrum/Starknet/Sei/YZY — none touch a held or shortlisted
  pair directly, though ARB is on both shortlists this run (see below).

**Narratives:**
- Leading: Majors, still — dominance flat at 58.88% despite a broad alt rally,
  meaning the rally is CLARITY-driven risk-on across the board rather than
  capital rotating out of BTC into alts specifically.
- DeFi (UNI, AAVE, LINK, CRV, SUSHI, ONDO, LDO) clears both sleeve screens
  again but 7d momentum is DECELERATING versus the 19:56 entry: AAVE 7d +0.8%
  (was part of a +52% 30d move already flagged as extended), UNI 7d **-1.1%**
  on a +109.6% 30d base. Reading unchanged from 19:56: this is an aging bounce
  on top of a -37% YTD TVL decline, not a fresh setup — still not an entry,
  CORE or TACTICAL.
- L1/L2 narrative is split by timeframe: ARB is -16.3% 7d (still rolling over
  on the daily, matches 19:56 framing) but flipped to +5.5% 7d TACTICAL PASS
  on the hourly — a bounce inside a rollover, not a trend change. DOT closed
  a losing tactical trade in this narrative Sunday (1/2 toward the
  exit-narrative rule); today DOT is -2.7% 7d, still not attractive.
- Memes/Infra broadened slightly (PEPE, SHIB, RENDER, GRT, WIF now clear the
  TACTICAL screen where they failed at 19:56) but with negative-to-flat 7d on
  the daily for most — reads as the same broad CLARITY-optimism lift, not
  narrative-specific strength, and none carry a coin-specific catalyst today.

**CORE shortlist (21, daily bars):** XTZ BAT XRP ETH AAVE SOL BTC SHIB UNI LTC
ADA DOT CRV LDO AVAX GRT DOGE ONDO SUSHI LINK ARB
Key metrics (7d% / 30d% / vsSMA20 / spread%): XTZ +18.2/+40.5/+16.4/0.63
(extended), XRP +6.1/+48.0/+6.3/0.39 (held), ETH +4.6/+38.4/+5.1/0.03 (held),
AAVE +0.8/+54.7/+4.3/0.21 (extended, decelerating), BTC +0.4/+26.0/+1.2/0.03,
UNI -1.1/+109.6/+14.9/0.20 (very extended), ARB -16.3/+95.1/+8.9/0.31
(rolling over).

**TACTICAL shortlist (23, hourly bars):** UNI XRP AAVE ARB LINK PEPE ETH LDO
ONDO ADA SKY SOL WIF SHIB DOGE CRV SUSHI DOT RENDER YFI TRUMP GRT POL
Key metrics (7d% / vsSMA20 / vol%/h / spread%): UNI +6.6/+6.1/0.9/0.16, XRP
+6.3/+5.6/1.0/0.44 (held), AAVE +6.0/+4.9/0.7/0.19, ARB +5.5/+3.4/0.9/0.34,
LINK +5.3/+4.2/0.6/0.22.

**Ideas by sleeve**

**CORE — HOLD, no new entry.** ETH remains the only position with a specific,
live, asset-level catalyst (ETF flow divergence, unchanged and still positive).
Everything else clearing the CORE shortlist today is riding the same
CLARITY-optimism macro lift, not an idiosyncratic catalyst: XTZ/UNI are already
extended, AAVE's cited catalysts (Kalshi listing, Ethena integration) are now
10+ days old, ARB is a daily rollover despite the hourly bounce. Opening a new
$40 CORE position one day ahead of a still-binary CLARITY vote and two days
ahead of an 80%-priced hawkish FOMC surprise, on a coin whose "catalyst" is the
same macro event already driving the whole screen, adds concentration to the
same risk twice rather than diversifying it.
What would change it: a CORE-shortlist coin develops its OWN dated catalyst
independent of CLARITY/FOMC, or both events resolve and the tape holds/extends
through them.

**TACTICAL — HOLD (recommendation only).** XRP is already 1/3 tactical slots
into tomorrow's exact CLARITY vote; every other TACTICAL-shortlist name showing
strength today (UNI, AAVE, ARB, LINK) is showing that strength for the SAME
reason (CLARITY optimism), not an independent one — adding any of them adds a
second bet on the identical binary event rather than spreading risk. No
coin-specific catalyst has appeared since 19:56. Compounding this, both binary
events (CLARITY tomorrow, FOMC the day after) are still pending, which argues
for not adding fresh event risk in the next 24-48h regardless of screen state.
What would change it: the CLARITY vote passes cloture tomorrow AND a second
name with its OWN catalyst (not just the same macro tailwind) clears the hourly
screen post-vote, or FOMC resolves without the priced hike and a fresh
independent hourly setup appears.

**Risk factors:** Two stacked binary/macro events in the next 48h — CLARITY
cloture Sep 15 2:15pm ET (60-vote threshold, procedural only even if it
passes) and FOMC Sep 16 (25bp hike priced 60-83% depending on venue, up from
the 09-11 framing that assumed a cut/hold). Either can gap XRP or the broader
market in either direction; the resting stop_limit on XRP can be gapped
through per the documented risk. BTC spot ETFs are on a 4th straight outflow
day even as the market rallies on CLARITY optimism — a divergence worth
watching, not yet actionable. DeFi's bounce continues to sit on top of a -37%
YTD TVL decline; today's deceleration (AAVE/UNI 7d momentum both near flat or
negative versus 30d gains of 50-110%) is consistent with the bounce aging, not
reversing into a new leg up.

**Decision:** CORE **HOLD**. TACTICAL **HOLD** (recommendation; execute run
may still originate if the CLARITY vote passes and a fresh, coin-specific
setup — not just shared macro lift — clears the hourly screen).
**Fee budget:** $0.52 / $2.99 used this week, unchanged this run (no trade
placed).

---
## 2026-09-14 — Crypto Research (UTC ~22:54, LOCAL clock — broker unreachable, see below)

**RUN ABORTED — Bybit demo API totally unreachable, no trading decisions made.**

- `bash scripts/state.sh` failed immediately: `curl: (22) ... 403`.
- Root-caused by hand: `curl -i https://api-demo.bybit.com/v5/market/time`
  (public, unauthenticated, no keys needed) returns HTTP 403 from CloudFront:
  `"The Amazon CloudFront distribution is configured to block access from
  your country."` Reproduced 3x on retry, zero successes. This is a network/
  geo-block at Bybit's CDN edge in this session's execution environment, NOT
  a credentials problem — confirmed `BYBIT_API_KEY`/`BYBIT_API_SECRET` are
  real (non-placeholder) values; a public unauthenticated endpoint fails
  identically before auth is ever checked.
- No prior occurrence found in git history — first time this environment has
  hit this block.
- Consequence: `scripts/state.sh`, `scripts/bybit.sh` (positions/orders/
  balance/instruments), and `scripts/screen.sh` are ALL unusable this run.
  STEP A (reconcile, stop-coverage check, hard-cut, ratchet) and STEP C
  (screen the universe) could NOT be performed. Per project rules, account
  state, positions, and P&L must come from `state.sh`/`pnl.sh` only — none of
  that is fabricated or re-derived here.
- Last KNOWN (unverified this run) state, from the 2026-09-14T20:26 UTC entry:
  equity $199.13, ETH (CORE) ~-0.05% [SPLIT ok], XRP (TACTICAL) ~+4.97%
  [SPLIT ok], fee budget $0.52/$2.99 used. **This cycle could NOT confirm
  either position still has live stop coverage, was not gapped through, or
  has not breached a hard-cut level.** Treat both positions as unmonitored
  for this window until the next successful run.
- `PERPLEXITY_API_KEY` env var holds the template placeholder
  (`your_perplexity_api_key_here`) — `scripts/perplexity.sh` correctly
  normalized it to empty and exited 3 as designed. Did not fall back to
  WebSearch given the run was aborted before STEP B/D (no screen data to
  pair catalysts with, and no verified account state to size against).
- `CLICKUP_*` env vars are also template placeholders — `scripts/clickup.sh`
  would no-op locally (documented behavior), so the urgent notification for
  this outage was sent out-of-band instead (session-level alert), not via
  ClickUp.
- **No orders were placed, no memory files beyond this entry were touched,
  no CORE/TACTICAL decision is recorded** (there is nothing to decide from —
  this is neither a HOLD nor a TRADE, it is a failed run).

**Action needed before the next run relies on this bot:** verify Bybit demo
API reachability from wherever the next scheduled run executes (region/IP
may differ per session). If the block persists, scan/execute runs will also
fail, and open positions will accumulate unmonitored 6h+ windows — escalate
if this repeats.
