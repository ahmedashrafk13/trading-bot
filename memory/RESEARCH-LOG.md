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
## 2026-09-15 — TACTICAL (INTRADAY ADDENDUM, execute run, UTC 00:11 broker clock)

**Overriding the 09-14 20:26 HOLD for UNI only.** That HOLD's stated condition —
"a second name with its OWN catalyst, not just shared macro lift" — is now met:
CLARITY/FOMC have NOT resolved yet (vote still ~18h out), but UNI has a fresh,
coin-specific, dated event distinct from that macro overhang.

**Catalyst (WebSearch, PERPLEXITY_API_KEY not set -> fallback per design):**
Uniswap's protocol fee switch is now active, burning UNI from protocol +
Unichain fees; trailing 7-day pace implies ~$263M annualized burn (Hayden
Adams). Robinhood Chain hit ~$3B single-day DEX volume with Uniswap capturing
~98% of it, triggering a record 184,000 UNI burned (~$1.15M) in one day. This
is an idiosyncratic supply-reduction mechanism/volume record, not the shared
CLARITY-optimism lift the prior research flagged as insufficient.
Checked AAVE too: its catalysts (Kalshi listing 09-04, MCP server launch
09-11, CLARITY vote) are all stale or macro-shared — no override for AAVE.

**Screen:** UNI hourly — 7d momentum +1.9%, vsSMA20 +1.9% (within +/-8%), vol
1.2%/h (within 0.4-6% band), spread 0.22% (<=0.5%). TACTICAL PASS.
**Live quote:** ap 6.5521 / bp 6.54192 -> spread ~0.16% (`alpaca.sh crypto-quote`,
00:11 UTC broker clock).

**Gate:** TACTICAL positions after fill 2/3. Combined after fill 3/6.
Deployment 29.8% -> ~54.8% after fill (<=85%). Fee budget $0.52/$2.95 used,
est. this round trip ~$0.37 (0.75% assumed, wider than BTC's floor) ->
~$0.89/$2.95, headroom clear. Circuit breaker clear (0 realized losses, 0
consecutive tactical losses). Size = (196.98*0.015)/0.06 = $49.24 = exactly the
25% TACTICAL cap. Cost $49.24 <= cash $138.30. UNI/USD tradable, not a
stablecoin, notional > $10 floor. R:R ~2.01:1 after fees at this size (fee is
proportional, ratio invariant to notional per TRADING-STRATEGY.md's 14%/6%
worked example).

**Decision: TACTICAL ENTRY — UNI/USD.** Target +14% (limit rests at exchange),
stop -6% (logged, enforced by 30-min scan). See TRADE-LOG for fill/order IDs.

---
## 2026-09-15 — Crypto Research (UTC 06:09, broker clock)

**Account snapshot:** EQUITY $197.31 | CASH $88.98 | DEPLOYED 54.9% (ceiling
85%, no floor). SIZE NOW: CORE $19.73 (15% stop) | TACTICAL $49.33 (6% stop).
Positions: ETH (CORE) -4.36%, stop@100% $2223.69 OK. UNI (TACTICAL) +2.12%,
target@100% $7.480976 OK (restored this run — see TRADE-LOG). XRP (TACTICAL)
-0.12%, target@100% $1.6095 OK (restored this run). Fee budget $0.52/$2.96
used, headroom $2.44. Circuit breaker clear ($0.00 realized vs $9.87 limit, 0
consecutive tactical losses). Amendment trigger 0/10 — not eligible, nothing
changed.

**Resting-leg conflict resolved this run:** state.sh at run start showed UNI
and XRP both in stop-resting shape (placed by the 03:37 scan), not the
owner-directed target-resting shape TRADING-STRATEGY.md specifies. Cancelled
both stop_limit orders and restored the +14% target limits per policy. Full
detail and order IDs in TRADE-LOG. This is a recurring scan-vs-policy conflict
(3rd occurrence today) — the scan-facing prompt content needs correcting to
match the committed strategy file; flagged there for the account owner.

**Market context (WebSearch, PERPLEXITY_API_KEY still the template placeholder
-> fallback per design, same as prior runs):**
- BTC ~$77,624-77,782, dominance 58.88% (flat vs prior entries) — above
  EMA20/50/200, daily MACD histogram negative (deceleration), ATR14 ~$2,077.
  Wedged between pivot support $76,780 / resistance $78,392.
- ETH ~$2,495-2,505. Bullish above $2,438 (target $2,800-2,920); below $2,438
  risks $2,000. Hegotá upgrade H2 2026; Glamsterdam mainnet slipped to Q4,
  Sepolia fork Sept 28 — no near-term price impact.
- ETF flows (week of Sept 8-11): BTC spot ETFs -$462.7M net (4th straight
  outflow day, Thursday alone -$283M, ARKB -$234M) but September still net
  +$307.3M. ETH spot ETFs +$196.9M net, 4th straight week of inflows, $216M
  single-day on Sept 11. Divergence thesis behind the held ETH position is
  intact and getting stronger, not weaker.
- **CLARITY Act: cloture vote today, Sept 15, 2:15pm ET.** MATERIAL CHANGE —
  Polymarket now prices the bill being signed into law in 2026 at **~18-19.5%**,
  down sharply from a ~90% peak in February. Republicans hold 53 seats, need 9
  Democrats for the 60-vote threshold; even a "yes" today is only a procedural
  motion-to-proceed, not passage. This is the exact catalyst the held XRP
  position was opened on — it has visibly deteriorated, not just "not yet
  resolved" as framed in the 09-14 entries.
- **FOMC decision Sept 16, 2pm ET**, dot-plot meeting. Hold at 3.50-3.75% vs a
  25bp hike both live; hike-implied probability rose above 50% (from ~36%
  pre-Jackson-Hole) after Fed Chair Warsh's hawkish comments. BOJ meets Sept
  17-18, adding a third stacked macro event this week.
- Token unlocks: ARB unlocks 92.65M (~$13.02M, 0.93% of supply) tomorrow Sept
  16 — the largest dollar unlock this month, a supply overhang directly
  relevant to ARB's tactical hourly PASS below.
- Narratives: AI-infra convergence and "real revenue" L1/DeFi rotation cited
  as 2026 leaders; memes broadly cooling (-30%+ from mid-April levels). Nothing
  new since the 09-14 entry changes this framing.

**Narrative read:** Majors still leading (dominance flat at 58.88% despite the
DeFi bounce). DeFi (UNI, CRV, SUSHI, SKY, AAVE) continues to clear both sleeve
screens but on a decelerating, aging bounce sitting atop a documented -37% YTD
TVL decline — treat new entries skeptically unless the catalyst is
idiosyncratic (see UNI, SUSHI below). ARB is a daily rollover (-18.7% 7d) with
an hourly bounce sitting directly in front of tomorrow's largest unlock of the
month — a bounce into supply overhang, not a trend change.

**CORE shortlist (12, daily bars):** XTZ FIL AAVE UNI LTC CRV BAT AVAX GRT
SUSHI ARB DOT
Key metrics (7d%/30d%/vsSMA20/spread%): XTZ +6.1/+36.0/+10.3/0.64, FIL
+5.4/+33.7/+12.9/0.33, AAVE -0.8/+48.8/+0.2/0.19, UNI -1.0/+104.5/+11.3/0.21
(held, very extended), ARB -18.7/+82.5/+1.6/0.37 (rolling over, unlock
tomorrow), DOT -20.1/+31.3/+3.4/0.20 (rolling over).

**TACTICAL shortlist (5, hourly bars):** UNI CRV SKY SUSHI ARB
Key metrics (7d%/30d%/vsSMA20/vol%h/spread%): UNI +2.4/+7.8/+2.3/1.4/0.21
(held), CRV +1.7/+1.9/+0.7/0.6/0.18, SKY +1.1/+2.3/0.0/0.8/0.19, SUSHI
+0.5/-1.3/-0.8/0.6/0.18, ARB +0.2/-0.6/-1.1/1.3/0.28.
XRP fails BOTH screens this run (daily -0.6%/7d momentum negative; hourly
-1.1%/7d, vsSMA20 -1.1%) — consistent with its catalyst deteriorating (see
CLARITY odds above).

**Ideas by sleeve**

**CORE — no new entry.** Every CORE-shortlist name is riding the same
decelerating DeFi/majors bounce with no fresh idiosyncratic catalyst: AAVE's
catalysts are 10+ days stale, XTZ/UNI already very extended (+10-11% over
SMA20), ARB/DOT are daily rollovers. Nothing here clears the "own dated
catalyst, not shared macro" bar. CORE stays at 1/3 (ETH only).
What would change it: a CORE-shortlist name develops an idiosyncratic catalyst
independent of the DeFi bounce, or the FOMC/BOJ macro overhang clears without
damage and a name is still un-extended afterward.

**TACTICAL — TRADE recommendation: SUSHI (execute run to confirm/originate).**
Catalyst: Sushi's Strategic Reserve weekly SUSHI buybacks began Sept 7 (passed
DAO vote), with monthly xSUSHI buybacks starting Oct 1 — an ongoing,
mechanically dated, idiosyncratic buyback program, not the shared DeFi-bounce
narrative (also expanding into RWA via Sushi Launch on Robinhood Chain, live
since Aug 1). Screen: hourly TACTICAL PASS — 7d +0.5%, vsSMA20 -0.8%, vol
0.6%/h, spread 0.18%. At $49.33 size: stop -6% = entry*0.94, target +14% =
entry*1.14, R:R ~2:1 after fees per the standard worked example. Gate check:
TACTICAL 2/3 filled (would go to 3/3, at cap); combined 3/6 -> 4/6; deployment
54.9% -> ~79.7% (<=85% ceiling, OK); fee budget headroom $2.44 covers the
~$0.37 estimated round trip; circuit breaker clear.
CRV and SKY also clear the TACTICAL screen but were rejected: CRV's cited
catalyst (Llamalend V2, the Sept 2 breakout) is 2 weeks old and already
priced in — current move reads as the same sector bounce. SKY's catalyst
(Standard Chartered coverage, Sept 11) is a 2028-horizon institutional
research note, not a near-term dated event suited to a 2-day tactical hold.
ARB was rejected outright: daily rollover plus the largest token unlock of
the month (Sept 16, ~$13M/0.93% supply) landing tomorrow — a bounce directly
in front of a supply overhang, the opposite of a clean setup.
**Recommendation only — this is not binding; execute (00:07/06:07/12:07/18:07)
originates if the screen and catalyst still hold then.**

**Flagged: reassess the XRP thesis.** Not a screen failure this run — an
event-risk deterioration. CLARITY passage odds have collapsed from a ~90%
February peak to ~18-19.5% ahead of today's vote, and even a "yes" is only a
procedural cloture motion. XRP now fails both sleeve screens (see above). Per
TRADING-STRATEGY.md's TACTICAL rule ("thesis broken -> close immediately"),
this is trending toward thesis-broken territory, though the position is only
-0.12% and its stop level (-6% at $1.3271) has not been breached. Not closed
in this research run — no execute mandate here, and no hard trigger (hard cut,
naked stop, +14% target) fired. **Explicit recommendation for the next scan
(30-min cadence) and the 06:07 execute run: re-evaluate XRP against the
thesis-broken rule now that the catalyst odds have cratered, independent of
whether price has moved.**

**Risk factors:** Three stacked macro/political events in 96h — CLARITY
cloture today (odds now low, ~18-19.5%), FOMC Sept 16 (hike odds >50%, up from
~36% pre-Jackson-Hole), BOJ Sept 17-18. ARB's Sept 16 unlock overlaps the FOMC
decision. BTC ETF outflows now a 4th consecutive day even as ETH ETFs extend
inflows — a genuine, not yet fully priced, divergence. DeFi bounce (UNI, CRV,
SUSHI, SKY) continues to sit on a -37% YTD TVL decline; treat strength as
rotation/short-covering until it survives a full week without a fresh macro
catalyst.

**Decision:** CORE **HOLD** (binding for the day). TACTICAL **HOLD as the
formal research decision, with a TRADE recommendation on SUSHI** for the
execute run to act on if conditions still hold — per policy this recommendation
is non-binding and does not authorize an entry from this run.
**Fee budget:** $0.52 / $2.96 used this week, unchanged this run (no new
entries; only order-type corrections on existing UNI/XRP legs, at no
incremental fee cost).

---
## 2026-09-16 — Crypto Research (UTC ~00:08, broker clock) — run inline from execute.md STEP B (no standalone research run had posted for today)

**Account snapshot:** EQUITY $190.45 | CASH $153.73 | DEPLOYED 19.3% (ceiling 85%,
no floor). SIZE NOW: CORE $25.39 (15% trail, risk $3.81=2.0%, max 4) | TACTICAL
$19.04 (10% trail, risk $1.90=1.0%, max 1). Positions: ETH (CORE) qty 0.015302647,
entry $2,609.50, current ~$2,399.9-2,417 (screen vs state.sh timestamps differ
slightly), unrealized ~-8%, stop 100% @ $2,223.69 (order `1ebb2562`) OK. XRP
(v1 TACTICAL) STOPPED OUT 2026-09-15T18:41 UTC at -6.23%, discovered this run via
RECONCILE — see TRADE-LOG for the full exit writeup; XRP is no longer an open
position. Fee budget $0.52/$1.90 used (monthly), headroom $1.38. Circuit breaker:
$0.00 realized losses today vs $9.52 limit — dollar threshold clear; BUT 3
consecutive tactical losses now on the books (DOT 09-14, UNI 09-15, XRP 09-15)
with no intervening tactical win — see TRADE-LOG reconcile entry for the
day-boundary ambiguity in that rule. This run treats TACTICAL as closed for new
entries regardless of screen/catalyst until a tactical win breaks the streak.
Amendment trigger: 3 closed trades since last amendment, 3 < 10, not eligible.

**Market context (WebSearch — PERPLEXITY_API_KEY is still the template
placeholder value `your_perplexity_api_key_here` -> exits 3 -> fallback per
design, same as every prior run):**
- BTC live quote (screen.sh) $75,618.15, -3.4% 7d, -3.1% vs SMA20, spread 0.03%.
  WebSearch results for "today" are noisy/conflicting on exact level ($75.6k-79k
  across sources of different recency) but agree on direction: BTC has been
  range-bound/soft, dominance ~58.4-58.9% (flat).
- **FOMC decision TODAY, 2026-09-16, 2:00pm ET (~18:00 UTC), Powell presser
  2:30pm ET.** Hike-odds estimates from different sources range ~68-85%
  (up sharply from ~36-44% in late August) against a 3.50-3.75% hold; driven by
  persistent inflation (PCE 3.7%). This is a live, unresolved, high-impact macro
  event landing squarely inside today's execute/scan windows. BOJ meets Sept
  17-18 right behind it (from 09-15 research, unchanged).
- **CLARITY Act cloture vote FAILED in the Senate on 2026-09-15** (fell short of
  60 votes; Hawley/Collins/Moran among Republicans not supporting) — confirms
  the thesis-deterioration flagged in yesterday's research and explains the XRP
  stop-out discovered this run. No new open position is exposed to this now.
- ETH: spot ETF inflows +$197M last week (4th straight week of inflows) vs BTC
  ETF outflows -$463M in the same window — the BTC/ETH ETF-flow divergence
  flagged 09-14/09-15 is still intact, now with a bigger number. Glamsterdam
  mainnet still slipped to Q4 2026; Sepolia fork Sept 28 unchanged. No new
  near-term ETH-specific catalyst beyond the ETF divergence, which is a slow
  thesis not a today-trade trigger.
- Token unlocks this week: ARB is NOT in the major-unlock headlines this
  specific WebSearch pass, but the 09-15 research entry already flagged ARB's
  own unlock (92.65M tokens, ~$13.02M, 0.93% of supply) landing **today,
  2026-09-16** — a supply overhang on the one name that also clears the
  TACTICAL screen today (see below).
- Narrative rotation: broad 2026 framing continues to favor AI-infra/DePIN,
  stablecoin payments, RWA, and "real revenue" L1/DeFi over pure memes (memes
  broadly -30%+ from mid-April highs) — unchanged from 09-14/09-15 framing,
  nothing fresh enough today to act on by itself.

**CORE shortlist (4, daily bars, `scripts/screen.sh`):** UNI ARB FIL XTZ
(7d%/30d%/vsSMA20/spread%): UNI +3.0/+93.2/+4.4/0.23, ARB +1.1/+101.4/+11.3/0.37,
FIL -0.9/+20.9/+2.8/0.29, XTZ -5.2/+25.5/+4.0/0.26.
Every other one of the 33-pair universe FAILED the CORE screen this run — a much
narrower board than 09-15's 12-name shortlist, consistent with the broad red week
into FOMC (BTC -3.4% 7d, most alts -3% to -16% 7d).

**TACTICAL shortlist (1, hourly bars):** ARB only (0.8/7.7/+6.2/2.9%vol/0.32%
spread). Moot this run — TACTICAL is circuit-breaker-blocked (see above).

**Ideas by sleeve**

**CORE — no new entry (HOLD).** Checked each shortlist name's catalyst
individually against the "own dated catalyst, not shared macro" bar:
- UNI: catalyst is real (fee-switch burn ramp, ~$263M annualized implied burn,
  record Robinhood Chain volume) but it is 8+ days old (dated ~Sept 8), already
  well-priced (+93.2% 30d, +4.4% vs SMA20, and this account already ate a -6%
  TACTICAL stop on UNI on 09-15 — same coin, DeFi narrative already has 1 failed
  trade), not a fresh trigger for a NEW CORE-sized position today.
- ARB: catalyst is BEARISH, not bullish — the largest token unlock of the month
  (~$13M / 0.93% supply) is scheduled for TODAY. A daily-bar bounce sitting
  directly in front of a same-day supply unlock is the setup this desk rejected
  outright on 09-15 for the identical reason; nothing has changed except the
  unlock is now imminent rather than "tomorrow." Reject.
- FIL: WebSearch explicitly could not attribute FIL's rally to any confirmed
  catalyst ("no independently confirmed fundamental catalyst," "technical
  breakout combined with renewed speculation") — this is a shared-narrative/
  momentum move (AI-storage speculation), not the idiosyncratic, dated catalyst
  the entry checklist requires. Reject.
- XTZ: catalysts cited (Tezos X mainnet, Etherlink 7.0) are real but
  undated/ongoing ("anticipation building," no confirmed date this week) —
  not a today-dated trigger. Reject.
No CORE shortlist name clears the bar. Combined with a same-day FOMC decision
that is a coin-flip-adjacent, high-impact macro event, adding CORE exposure
right now is exactly the "shared macro, not idiosyncratic" trade the strategy's
own catalyst rule exists to filter out. CORE stays at 1/4 (ETH only).
What would change it: a shortlist name develops a fresh, dated, idiosyncratic
catalyst, ideally reviewed again after the FOMC print has cleared and the
market has digested it rather than into the event blind.

**TACTICAL — no new entry (HOLD, circuit-breaker-blocked).** ARB is the only
name clearing the TACTICAL hourly screen, and it carries the same same-day
unlock overhang that kills it for CORE. Moot regardless: 3 consecutive tactical
losses (DOT, UNI, XRP) sit on the books with no intervening win, and this run
treats that streak as blocking new tactical originations today (see TRADE-LOG
reconcile entry and account snapshot above for the exact reasoning and the
day-boundary ambiguity flagged to OBSERVATIONS.md). Even absent the breaker
question, ARB's catalyst is bearish, so nothing here would have been traded
today regardless.

**Risk factors:** FOMC decision + Powell presser today (~18:00-18:30 UTC),
hike-odds materially elevated vs a month ago — expect volatility spanning both
today's 18:07 UTC execute run and every scan between now and then. BOJ Sept
17-18 stacked right behind it. ARB's unlock lands same-day as FOMC — a
double catalyst, both bearish/uncertain, on the one TACTICAL-qualifying name.
CLARITY Act failure is now resolved (bearish, already realized via the XRP
stop) rather than a forward risk. Broad market red across almost the entire
33-pair universe this week (32/33 fail the CORE screen) — a much thinner
opportunity set than 09-15, consistent with pre-FOMC de-risking rather than a
narrative rotation.

**Decision:** CORE **HOLD** (binding for the day) — no shortlist name clears
the idiosyncratic-catalyst bar, and adding exposure into a same-day FOMC
decision is the wrong trade even if one did. TACTICAL **HOLD** — blocked by the
3-consecutive-tactical-loss circuit breaker (see reasoning above), and moot
regardless since ARB (the only TACTICAL pass) carries a same-day bearish unlock
catalyst. What would change TACTICAL: a tactical win to break the loss streak
(none available — 0 tactical positions open) or, failing that, explicit
weekly-review guidance on the day-boundary question; what would change CORE:
FOMC clearing without damage plus a shortlist name still un-extended and
carrying its own dated catalyst.

**Fee budget:** $0.52 / $1.90 used this MONTH so far (headroom $1.38). No
entries this run, so unchanged.

---
## 2026-09-16 — Crypto Research (UTC 06:08, broker clock) — scheduled research run

**Account snapshot (`scripts/state.sh`):** EQUITY $190.52 | CASH $153.73 | DEPLOYED
19.3% (ceiling 85%, no floor). SIZE NOW: CORE $25.40 (15% trail, risk $3.81=2.0%,
max 4) | TACTICAL $19.05 (10% trail, risk $1.91=1.0%, max 1). Positions: ETHUSD
(CORE) qty 0.015302647, entry $2,609.50, current $2,404.30, unrealized -7.86%,
stop 100% of qty @ $2,223.69 (order `1ebb2562`) — OK, no action. XRP (v1
TACTICAL) closed 2026-09-15T18:41 UTC (logged in TRADE-LOG); 0 TACTICAL positions
open. Fee budget $0.52/$1.91 used this month, headroom $1.39. Circuit breaker:
$0.00 realized losses today vs $9.53 limit — dollar threshold clear. Consecutive
tactical losses (DOT 09-14, UNI 09-15, XRP 09-15) = 3, no intervening tactical
win — per the 00:08 UTC execute-run reconcile entry this is treated as an active
caution against new TACTICAL originations today, pending weekly-review
clarification of the day-boundary ambiguity already logged to OBSERVATIONS.md.
Amendment trigger: 3 closed trades since last amendment (state.sh's regex still
reports 0 — known bug, already logged), 3 < 10 — not eligible.

**Reconcile (STEP A.1):** `alpaca.sh positions` / `orders` match TRADE-LOG
exactly — one open position (ETHUSD), one resting stop_limit at 100% of held
qty, no drift since the 00:08 UTC runs.

**Gap/ratchet (STEP A.3/A.4):** ETH -7.86% vs -15% CORE hard cut — not
triggered. HWM $2616.11 vs current $2,404.30 — below HWM, no new high, no
ratchet. Stop distance from current price ~7.5%, above the 5% floor. No orders
placed or cancelled this run.

**Market context (WebSearch — PERPLEXITY_API_KEY is still the template
placeholder `your_perplexity_api_key_here` -> perplexity.sh exits 3 -> fallback
per design, same as every prior run):**
- BTC ~$75,900-77,100 depending on source/timestamp, dominance ~60% (a notable
  jump from the ~58.4-58.9% read at 00:08 UTC — sources disagree on exact level
  but agree dominance is elevated, i.e. alts underperforming BTC into the FOMC
  print). BTC has given back its post-golden-cross rally and sits at a
  make-or-break technical level ($77k support / $80k resistance).
- **FOMC decision today, ~18:00 UTC (2:00pm ET), Powell presser 2:30pm ET.**
  Sources remain inconsistent on direction — some frame it as elevated HIKE
  odds (~60-68%, up sharply from ~36% in late August, driven by persistent
  3.7% PCE inflation), others frame the base case as a HOLD that would clear
  ETH's path toward $2,920. Whichever framing is right, this is the day's
  dominant, unresolved, high-impact macro catalyst landing inside today's
  06:07/12:07/18:07 execute windows, plus BOJ Sept 17-18 right behind it.
- ETH: $2,397-2,404. 4th consecutive week of spot ETF inflows ($197M last
  week, $1.62B over 12 weeks), still diverging from BTC's 4th straight day of
  ETF outflows (-$463M same week) — the divergence flagged 09-14/09-15/00:08
  is intact and, if anything, slightly wider. ETH needs to hold ~$2,438 (0.618
  weekly Fib) for the bullish September case toward $2,920; has failed twice
  to clear $2,550 (50-week MA). No new ETH-specific catalyst beyond the
  ETF-flow divergence (a slow thesis, not a today trigger) and Glamsterdam
  (testnet fork ~Sept 28, mainnet slipped to H2 2026 — unchanged, not
  actionable this week).
- CLARITY Act cloture vote FAILED in the Senate 2026-09-15 (confirmed, same as
  00:08 read) — XRP's stop-out this week is the direct consequence. Resolved,
  not a forward risk.
- Token unlocks this week: HYPE's big unlock (9.92M tokens, ~$797M) already
  happened Sept 6 — priced in, not a fresh catalyst. ARB's own unlock
  (92.65M tokens, ~$13M, 0.93% supply) lands TODAY (09-16) — bearish overhang,
  unchanged from 00:08 read.
- Narratives: AI/DePIN, stablecoin payments, RWA, modular infra continue to
  lead 2026 flows (AI tokens ~35.7% of Q1 investor interest, ahead of memes
  ~27.1%); memes broadly still -30%+ from mid-April highs. Nothing narrative-
  fresh enough today to act on by itself — consistent with 09-14/09-15/00:08.

**CORE shortlist (4, daily bars, `scripts/screen.sh`):** UNI ARB FIL XTZ —
identical names to the 00:08 UTC run, prices little changed (UNI $6.3393, ARB
$0.1538, FIL $0.8126, XTZ $0.2448). 29/33 pairs still fail the CORE screen —
board stays this narrow going into the FOMC print.

**TACTICAL shortlist (9, hourly bars):** ARB XRP DOT WIF BTC HYPE SOL ETH DOGE —
much wider than the single-name (ARB-only) TACTICAL board at 00:08 UTC; hourly
momentum has broadened even as the daily/CORE board stayed narrow. Prices:
ARB $0.1538, XRP $1.2944, DOT $0.9508, WIF $0.1792, BTC $75,943.87,
HYPE $77.208, SOL $97.13, ETH $2,403.95, DOGE $0.0801.

**Ideas by sleeve**

**CORE — no new entry (HOLD, binding for the day).** Re-checked each shortlist
name's catalyst against the "own dated catalyst, not shared macro" bar; nothing
changed from the 00:08 UTC read:
- UNI: catalyst (fee-switch burn ramp) is real but 8+ days old, already priced
  (+93% 30d, +4.4% vs SMA20), and this account already ate a TACTICAL stop-out
  on UNI itself on 09-15 (DeFi narrative: 1 failed trade). Reject — not fresh.
- ARB: same-day token unlock (~$13M, 0.93% supply) is a bearish overhang
  directly on the one CORE-passing name with any near-term news. Reject.
- FIL: WebSearch again finds no confirmed catalyst, only "technical breakout /
  renewed speculation" — momentum without a dated trigger. Reject.
- XTZ: catalysts (X mainnet, Etherlink 7.0) remain undated/ongoing. Reject.
No CORE shortlist name clears the bar, and adding exposure hours before a live
FOMC decision is the wrong trade even if one did. CORE stays 1/4 (ETH only).

**TACTICAL — no new entry (HOLD; recommendation, non-binding).** Despite a much
wider hourly board than 00:08, no name has a fresh, dated, idiosyncratic
catalyst independent of today's FOMC event:
- ARB: same bearish same-day unlock as CORE. Reject.
- XRP: its own catalyst (CLARITY cloture) just failed and directly produced
  this week's tactical stop-out — re-entering the same name on the same dead
  catalyst is not a new trade. Reject.
- DOT: no catalyst found; L1/L2 narrative already carries 1 tactical loss
  (09-14). Reject.
- WIF, DOGE: meme narrative broadly rolling over (-30%+ from April highs), no
  dated catalyst for either name specifically. Reject.
- BTC, ETH: passing on hourly momentum but the only "catalyst" is the shared
  FOMC/ETF-flow macro backdrop — exactly the non-idiosyncratic trade the entry
  checklist filters out, and ETH is already the account's sole CORE exposure,
  so a TACTICAL leg on it would concentrate rather than diversify risk.
  Reject both.
- HYPE: its unlock already happened Sept 6 (priced in); no fresh trigger found.
  Reject.
- SOL: no dated catalyst found this run. Reject.
No TACTICAL name clears the bar. Separately, the unresolved 3-consecutive-
tactical-loss streak (see account snapshot) is being treated as an active
caution today, so TACTICAL stays closed to new originations even if a
catalyst had cleared. What would change it: a genuine tactical win to break
the streak (none open), explicit weekly-review guidance on the day-boundary
question, or a shortlist name developing its own dated catalyst once FOMC has
cleared.

**Risk factors:** FOMC decision + Powell presser today (~18:00-18:30 UTC) is
the dominant near-term risk — sources disagree on hike-vs-hold framing but
agree the outcome is unresolved and high-impact, spanning the 06:07/12:07/18:07
UTC execute windows. BOJ Sept 17-18 stacked right behind it. BTC dominance
pushing toward/above 60% signals alts underperforming into the print — a
headwind for any new alt entry regardless of catalyst. ARB carries a same-day
bearish unlock on the one name appearing in both CORE and TACTICAL shortlists.
Broad market remains soft (29/33 fail CORE screen) — a thin opportunity set
consistent with pre-FOMC de-risking rather than a narrative rotation.

**Decision:** CORE **HOLD** (binding for the day) — no shortlist name clears
the idiosyncratic-catalyst bar, and FOMC event risk argues against new exposure
regardless. TACTICAL **HOLD** (recommendation) — no name clears the catalyst
bar, and the ongoing 3-consecutive-tactical-loss caution stands as an
additional reason to stay closed even in the execute run's discretion. What
would move TACTICAL to a TRADE: a fresh, dated, idiosyncratic catalyst on a
shortlist name once FOMC has cleared and been digested, or a tactical win
elsewhere breaking the loss streak.

**Fee budget:** $0.52 / $1.91 used this MONTH so far (headroom $1.39). No
entries this run, unchanged.

## 2026-09-17 — Crypto Research (UTC 20:32, broker clock) — scheduled research run

**Tooling note:** PERPLEXITY_API_KEY not usable (`perplexity.sh` reports "not
set"); all STEP B research done via native WebSearch fallback, as the routine
allows. Bybit credentials present and working via `.env` (the wrappers load it
themselves — `scripts/bybit.py:40`). The earlier run today was blocked at the
env check; that block is resolved.

**Account snapshot (scripts/state.sh, broker clock 2026-09-17 20:32 UTC):**
- EQUITY $200.00 (budget cap; account holds $178,978.89 — NOT the sizing basis)
- FREE $199.89 | DEPLOYED $0.11 = 0.1% (ceiling 85%, no floor)
- OPEN POSITIONS: 0. No stops owed, no ratchet due, no reconciliation drift
  vs TRADE-LOG. SCAN-VERDICT: NO-ACTION.
- Size available: CORE $26.67 (risk $4.00 / 15% trail) | TACTICAL $20.00
  (risk $2.00 / 10% trail)
- Circuit breaker: realized losses today $0.00 vs $10.00 limit. `state.sh`
  prints TRIPPED on the 3-consecutive-tactical-loss streak whose most recent
  close was 2026-09-15; execute.md reads that streak as resetting at 00:00 UTC.
  The two authorities still disagree (already in OBSERVATIONS). MOOT this run —
  the decision is HOLD on both sleeves regardless of which reading wins.

**Market context:**
- FOMC RESOLVED (the dominant risk flagged in the 09-16 entry is now behind us).
  25bp HIKE to 3.75-4.00%, unanimous 12-0, first hike since July 2023.
  16 of 18 officials project at least one more hike in 2026; 2026 median dot
  4.1% (from 3.8%), 2027 median 4.1% (from 3.6%). Warsh hawkish in substance,
  deliberately light on forward guidance: inflation "too high for too long",
  PCE 3.7% for 2026, return to 2% pushed out to 2029.
- Crypto rallied INTO the hawkish print — a relief move on removal of
  uncertainty, not on easing. BTC $76,663 (+1.5%, reclaimed $76k), ETH $2,455
  (+1.8%), XRP $1.30 (+2%). BTC is ~40% below its October $126k high.
- MACRO IS A HEADWIND, and this is what the relief rally is not pricing:
  DXY topped 100 for the first time since July (99.7 -> 100.3 on the print).
  10-year at 5.027%, highest zone since 2007; 2-year 4.736%, near a 52-week
  high. Higher-for-longer with no guidance is the mix that keeps the dollar bid.
- BTC DOMINANCE broke above 60% this week, ending an eight-month accumulation
  phase, targeting the 66% June-2025 cycle high. Altcoin Season Index 37.
  Capital is rotating TO BTC, away from alts — a structural headwind for every
  alt entry this account can make, independent of any single name's catalyst.
- ETF flows NEGATIVE on the week: 09-15 saw ~$592M combined outflows (BTC
  $450.3M, largest single day since June 25; ETH $141.5M, deepest in 155
  sessions), on the CLARITY Act failing cloture 49-60. Week: BTC spot ETFs
  -$462.7M (reversing a three-week inflow streak), ETH spot +$196.9M. BTC ETFs
  remain net +$307.3M for September.

**Leading vs rolling-over narratives:**
- LEADING: privacy. Sector ~$33.6B market cap; ZEC +2,496% on the year and
  +23% to a record high on the FOMC day. NOT ACTIONABLE — ZEC is not in the
  tradable universe, and chasing a name already up 2,496% is the definition of
  buying what has already moved.
- LEADING (secondary): RWA / tokenized equities. SEC roundtable 09-17 with
  BlackRock and Nasdaq on moving stock trading on-chain. Touches ONDO (CORE
  shortlist) but a roundtable is a discussion, not a decision — no dated,
  idiosyncratic outcome to trade.
- ROLLING OVER: alts broadly, on the dominance breakout. Memes (PEPE/SHIB/DOGE
  pass the technical screen but carry no catalyst and the narrative is not bid).
- ETH-specific: Glamsterdam mainnet slipped to Q4 2026; Sepolia fork 09-28.
  Slippage is not a catalyst. Senate inaction leaves staking/DeFi rules in limbo.

**CORE SHORTLIST (18, daily bars):** FLOCK ONDO LIT PIEVERSE AERO AAVE ASTER
XLM HYPE SPCXX FET JUP BNB LTC AVAX RLUSD DOT INJ
- NOTE: RLUSD is a STABLECOIN (last 1.0008, 7p% 0.0, 30p% 0.0). The strategy
  forbids holding a stablecoin as a position. Excluded here, and logged to
  OBSERVATIONS as a screen defect — it should never reach a shortlist.

**TACTICAL SHORTLIST (29, hourly bars):** ARB CRV NEAR FET DOT BR AAVE JUP PEPE
BCH LTC ENA HYPE SHIB HBAR ONDO XLM ASTER INJ ADA CRCLX MON WLD DATA LINK CAP
APT POL XPL

**Ideas, tagged by sleeve:**
- CORE — NONE ADVANCED. No shortlist name carries a dated, idiosyncratic
  catalyst. ONDO (0.3748, +13.6%/30p) is the closest on the RWA/SEC-roundtable
  story, but the catalyst is undated and shared across the sector. Size would
  have been $26.67, stop 15% below entry (trigger 0.3186, limit 0.3027), no
  target — rejected before sizing.
- TACTICAL — NONE ADVANCED. ARB (0.1774) leads the hourly screen at +8.2%/7p
  and passes both sleeves, but carries a KNOWN BEARISH OVERHANG: a 139.15M-token
  unlock (1.4% of supply) on 2026-09-23, six days out, on top of the 92.63M
  (~$9M) unlock that already landed 09-16. Entering a 10%-trail tactical long
  into a dated supply event is taking the wrong side of the only dated catalyst
  on the board. Rejected.
- R:R after ~0.65% measured round-trip friction: not computed for any name — no
  idea cleared the catalyst gate, so there is no entry to price.

**EVIDENCE CHECK (STEP EVIDENCE):** This run's routine restates "30-day momentum
is INVERTED (IC -0.037, t=-10)". That verdict is SUPERSEDED. The HYPOTHESIS-LOG
standing-verdicts table was CORRECTED 2026-09-16: momentum is inverted at SHORT
horizons only (<=1d, IC@1d -0.012 test), while IC@30d is **+0.025 test** —
positive. The old verdict was measured on Alpaca-era hourly bars and wrongly
generalised to all horizons. Logged to OBSERVATIONS; not acted on either way,
since nothing was entered. What still stands and still binds: tighter stops are
strictly worse, higher frequency is strictly worse, the altcoin universe has a
negative median (-21.2% vs BTC +157.4% over 5.7y), and nothing tested beats
buy-and-hold BTC. No part of today's reasoning rests on a REJECTED finding.

**Risk factors:**
- Dominance >60% with Altcoin Season Index 37: the measured negative median of
  the alt universe is being actively expressed right now. Every name this
  account can buy is an alt.
- The post-FOMC bounce echoes March 2022: BTC was also ~40% below its high when
  tightening began, rallied 18% over 12 days, then slid 50%. A relief rally
  inside a hiking cycle is not a trend.
- DXY >100 and 10y >5% are a sustained liquidity headwind, not a one-day event.
- ARB unlock 09-23 (1.4% of supply) — the one dated catalyst on the board runs
  bearish.
- Open interest ~50% above its 30-day average and more than doubled on the
  month: crowded leverage raises flush risk on any macro surprise.
- Three consecutive tactical losses remain unbroken; the sleeve has not yet
  shown it can win under current conditions.

**Decision:**
- CORE: **HOLD** — binding for the day. No shortlist name clears the
  idiosyncratic-catalyst bar, and a >60% dominance breakout is the worst regime
  in which to add alt exposure.
- TACTICAL: **HOLD** — recommendation only; a later execute run may originate if
  the screen passes AND a fresh catalyst is documented then. What would have to
  change: a dated, idiosyncratic catalyst on a shortlist name that is NOT ARB
  (its unlock runs the wrong way until 09-23 clears), plus dominance stalling
  below ~60%. Absent both, the correct action remains none.
- Cash is a position. 0.1% deployed is a valid, compliant state, and this run
  does NOT buy to correct it.

**Fee budget:** $0.52 / $2.00 used this MONTH (headroom $1.48), month started
2026-09-01. No entries this run — unchanged. The budget is a CEILING, not a
target; BTC buy-and-hold, the benchmark, pays 0%.

---

## 2026-09-18 — Research (06:07 slot, run at 16:16 UTC, broker clock)

**Account snapshot (scripts/state.sh):** EQUITY $200.00 (budget cap; account holds
$179,007.19 — not tradeable) | FREE $199.88 | DEPLOYED $0.12 = 0.1% (ceiling 50%, no floor)
| OPEN POSITIONS 0 | RESTING ORDERS 0 (`bybit.py orders spot` -> `[]`) | stop coverage n/a.
Sizes now: CORE $26.67 (risk $4.00 = 2.0%, 15% trail, max 1) | TACTICAL $20.00 (risk $2.00
= 1.0%, 10% trail, max 1). SCAN-VERDICT: NO-ACTION.
STEP A reconcile: live state matches TRADE-LOG tail exactly — flat, dust only. No stop
filled, no fill landed, no drift between runs. Nothing to stop, cut or ratchet.
Circuit breaker CLEAR ($0.00 realized today vs $10.00). Breaker now prints `clear`; the
stale 3-tactical-loss TRIPPED reading that recurred four times has cleared on its own
with the 09-15 streak two days behind.

**Market context:** BTC $80,973 on this screen vs $76,552 at the 09-17 snapshot — a
**+5.8% two-day bounce**, and BTC now leads its own 7d at +3.5% with vol 0.7%. ETH
$2,594 (+3.4%/7p). BTC dominance ~60.15% weekly close, above 60% for the first time in
2026; Altcoin Season Index still depressed. ETF flows split: BTC ETFs taking inflows
while ETH ETFs post a **third consecutive day of net outflows (~$39M)**. Macro unchanged
from 09-17 — DXY and real yields remain the liquidity headwind; no new Fed event today.

**Narratives — leading vs rolling over:**
- LEADING: **privacy** (ZEC +2,496% y/y, sector +213% off the Oct-2025 high, the only
  segment above that mark). NOT TRADEABLE HERE — ZEC is not in the 60-pair Bybit
  universe `screen.sh` ranks, so the one genuinely leading narrative is unreachable.
- LEADING (secondary): L2/alt beta bounce — ARB +53.6%/7p, NEAR +53.5%, UNI +46.5%,
  BR +238.6%. All four FAIL the CORE screen on overextension, which is the filter
  doing its job.
- ROLLING OVER: memes (PEPE/SHIB pass only on the technical, no bid in the story),
  DeFi and L1 both still below their prior-cycle marks.

**CORE SHORTLIST (38, daily bars):** ENA OP PEPE HYPE INJ SKY AERO ZRO FLOCK APT ZIG
ONDO XPL LIT AAVE SUI FET BCH ASTER DOT SOL AVAX WLD XLM JUP ADA SHIB HBAR LINK LTC BTC
BNB MNT DOGE STETH ETH KII GRAM
**TACTICAL SHORTLIST (39, hourly bars):** SOL XPL XRP TRUMP ETH STETH BTC AERO PEPE INJ
NEAR ARB HYPE AAVE LINK DOGE VIRTUAL XLM AVAX PENGU PUMP ONDO MNT GRASS ADA BCH APT HBAR
POL MON JUP SHIB BNB OP SUI LTC GRAM CRV KII

**Ideas, tagged by sleeve:**
- CORE — **NONE ADVANCED.** No shortlist name carries a dated, idiosyncratic catalyst.
  The best-ranked names by 7p momentum that still pass (ENA +18.3%, OP +17.2%, PEPE
  +15.7%, HYPE +14.9%) are all sector-beta moves off the same BTC bounce, not
  name-specific events. Had one cleared, size would have been $26.67, stop 15% below
  entry, no target. Rejected before sizing.
- TACTICAL — **NONE ADVANCED.** ZRO is the only shortlist name with a dated catalyst
  and it runs **bearish**: a ~$26.4M unlock inside the 09-14..09-20 window. ARB carries
  its 139.15M-token (1.4% of supply) unlock on 09-23, five days out, and additionally
  now FAILS the CORE screen at +53.6%/7p. Entering a 10%-trail long into the only two
  dated events on the board, both of which are supply releases, is taking the wrong side
  of the only information that exists. Rejected.
- R:R after the measured 0.65% round-trip friction: not computed for any name — nothing
  cleared the catalyst gate, so there is no entry to price. The 2:1-after-fees minimum
  was never reached for evaluation.

**EVIDENCE CHECK (STEP EVIDENCE):** Read the STANDING VERDICTS table before forming the
view. Nothing in today's reasoning rests on a REJECTED finding. Relevant and binding:
the altcoin universe has a CONFIRMED negative median (-21.2% vs BTC +157.4% over 5.7y)
and every name this account can buy is an alt; nothing tested beats buy-and-hold BTC;
higher frequency and tighter stops are both strictly worse. Momentum: inverted at <=1d
(IC@1d -0.012 test) but POSITIVE at 30d (IC@30d +0.025 test) — the 09-16 correction,
which this run does not contradict. Note the shape of today's board is exactly the
short-horizon-reversal regime: the biggest 7p movers (BR, ARB, NEAR, UNI) are the names
the CORE screen rejects, and buying them would be trading the horizon where the measured
IC is NEGATIVE. Also noted: hypothesis #6 (1 CORE slot, PROMOTED 2026-09-18) states its
own mechanism honestly — the preference for fewer slots is monotone and extrapolates
toward zero exposure, so it is not evidence of a long edge and does not argue for
filling the one remaining slot.

**Risk factors:**
- Dominance >60% with the alt-season index depressed: the CONFIRMED negative alt median
  is being actively expressed, and every tradeable pair here is an alt.
- The +5.8% two-day BTC bounce is precisely the <=1d/short-horizon window where measured
  momentum is INVERTED. Chasing it is arguing against the repo's own evidence.
- Two dated supply events inside the next five days (ZRO this week, ARB 09-23), both on
  names that pass a screen.
- ETH ETF outflows three days running while BTC takes inflows — rotation is into the
  benchmark, not into what this account can buy.
- The one leading narrative (privacy/ZEC) is outside the tradeable universe, so the
  screen's top names are beta, not leadership.

**Decision:**
- CORE: **HOLD** — binding for the day. No shortlist name clears the idiosyncratic-
  catalyst bar, and >60% dominance is the worst regime in which to add alt exposure.
- TACTICAL: **HOLD** — recommendation only; a later execute run may originate if the
  screen passes AND a fresh catalyst is documented then. What would have to change: a
  dated, idiosyncratic catalyst on a shortlist name that is NOT ARB or ZRO (both carry
  bearish supply events), plus dominance stalling below ~60%. Absent both, none.
- Cash is a position. 0.1% deployed is valid and compliant; this run does NOT buy to
  correct deployment.

**Fee budget:** $0.52 / $2.00 used this MONTH (headroom $1.48), month started 2026-09-01.
No entries this run — unchanged. The budget is a CEILING, not a target; BTC
buy-and-hold, the benchmark, pays 0%.

**Shadow log:** 77 rows appended (38 CORE + 39 TACTICAL passes, all skipped), priced from
this screen run. Nothing scored — the oldest unscored rows are 2026-09-16, two days old,
below the 5-day scoring window.

---

## 2026-09-21 (Sun) — research

**NOTE — LATE RUN.** Scheduled 06:07 UTC, actually executed 15:02 UTC (broker clock).
No research run happened on 09-19 or 09-20; the last entry in this file is 09-18. Those
two days had no plan, so no CORE entry was possible on either.

**BLOCKER FOUND AND CLEARED (infrastructure, not strategy).** Every signed Bybit call
failed `retCode 10002` on the first attempt of this run. Cause: this machine's clock runs
**~2.3s AHEAD** of Bybit's server, and Bybit rejects any signed request timestamped more
than ~1s ahead of its own clock — `recv_window` does not widen that side, so all three
retries failed identically and `state.sh` died at its first call. Fixed in
`scripts/bybit.py` by anchoring `X-BAPI-TIMESTAMP` to the exchange clock (offset measured
once per process against the public `/v5/market/time`, re-measured on a 10002). Private
calls verified working afterwards. This is exactly the failure mode `state.sh` warns about
with "[local clock is NOT trusted]" — the wrapper was trusting it anyway.

**Account snapshot (STEP A, from `scripts/state.sh`):**
- EQUITY $200.00 (budget cap; account holds $179,049.62 — NOT tradeable)
- FREE $178.53 | DEPLOYED $21.47 = **10.7%** of budget (ceiling 50%, no floor)
- OPEN POSITIONS 2, both TACTICAL, both age 66.9h, both **stop coverage 100% [OK]**
- Sizes now: CORE $26.67 (risk $4.00) | TACTICAL $10.00 (risk $1.00)

| Symbol | Qty | Entry | Price | P&L | Age | Stop |
|---|---|---|---|---|---|---|
| OP | 84.895020 | 0.11764 | 0.1275 | **+8.40%** | 66.9h | 100% [OK] |
| POL | 93.006900 | 0.10708 | 0.1132 | **+5.72%** | 66.9h | 100% [OK] |

**RECONCILE:** exchange state matches the TRADE-LOG tail exactly — same two fills, same two
resting stops, nothing filled or closed since 09-18T20:29. No drift. Dust balances (ARB
$0.0017, others sub-cent) are residue, not positions.

**72h TACTICAL time stop — NOT due, both exempt.** Both are at 66.9h of 72h, but the rule
is "72h unless >= +5%" and both clear it (+8.40%, +5.72%). Neither is closed for age.
Flagged for the 18:07 execute run: if either falls back below +5% before ~20:07 the time
stop becomes live.

**RATCHET — both stops moved UP** (amended in place, no cancel/replace, so no unprotected
window). High-water from 68 hourly bars since the 09-18T20:07 fills:

| Symbol | High-water | Stop was | Stop now | Limit now | Gap to price |
|---|---|---|---|---|---|
| OP | 0.13315 | 0.10660 | **0.11983** | 0.11384 | 6.0% |
| POL | 0.11460 | 0.09682 | **0.10314** | 0.09798 | 8.9% |

Trail is **10%, not 8%**: OP is +13.2% and POL +7.0% measured entry-to-high-water, both
below the +20% that triggers the 8% tighten. `state.sh`'s advisory SCAN GATE again printed
both ratchets against an 8% trail — the identical defect the 09-18 run caught and logged.
It is SHADOW MODE and was not obeyed. Limits sit 5% below trigger; neither stop was widened
or moved down; both clear the 5%-minimum-gap rule. Verified `Untriggered` at 100% of held
qty after the amend.

**Market context:**
- BTC ~$85,991 (screen), ~+2.7%/7p. Trading above every major MA and outside the upper
  Bollinger on multiple timeframes; daily RSI14 71.6, hourly 84.8 — **overbought on both**.
- BTC dominance **59.1%**, total cap ~$2.88T. Down from >60% a week ago but still high.
- ETH ~$2,742, +1.7%/7p — lagging BTC badly on the 7-period read.
- ETF flows: BTC spot ETFs took a small net inflow (~$6.2M) in the week to 09-18, with a
  ~$433M single-day inflow on the Friday. ETH ETFs positive but smaller. Flow is going to
  the benchmark, not to what this account can buy.
- Macro: Sept dot plot centres on 4.00-4.50% through 2027; no cuts priced for 2026. DXY
  99.36. The 10y real yield at 2.5% is the flagged break-level for the bitcoin case.
- Perplexity unavailable (`PERPLEXITY_API_KEY` not set, exit 0 with warning) — **fell back
  to native WebSearch** for all of STEP B, as the routine directs.

**Narratives — leading vs rolling over:**
- LEADING: nothing idiosyncratic. The 7p table is a near-uniform beta melt-up — 57 of 60
  pairs positive on 7p, the top decile (BR +126.8%, ZAMA +112.1%, ARB +75.6%, ZETA +73.9%,
  NEAR +66.3%) is dispersion around one market move, not sector leadership.
- The breadth itself is the signal: when everything is up 20-70% in a week, a screen PASS
  carries almost no selection information.
- ROLLING OVER: nothing cleanly. STRK (-9.2%/7p on the hourly read), ZETA (-10.0%),
  VVV (-6.7%) are the only weak names.

**Screen (STEP C, `scripts/screen.sh`, 60 pairs):**
- **CORE SHORTLIST (28):** FET ZRO XPL LTC HBAR ADA POL HYPE DOGE SOL WLD CHIP LIT AAVE
  LINK MNT BNB XLM BTC STETH ETH ICP ASTER XRP DATA KII TRX FLOCK
  Top by daily 7p among passes: FET +24.2%, ZRO +23.2%, XPL +22.3%.
  Note the shape — every one of the 20 biggest 7p movers **FAILS** CORE. The daily screen
  is rejecting the extended names, which is it working as designed.
- **TACTICAL SHORTLIST (43):** ARB XPL BR LTC CHIP SUI MNT PIEVERSE ADA HBAR SEI MON SOL
  POL BTC BNB AAVE TRUMP ZAMA XLM GRAM XRP AERO ETH LINK ONDO STETH CRV KMNO APT ENA ASTER
  ZRO AVAX LIT FLOCK CAP CC ICP DATA JTO UNI INJ
  Top by hourly 7p: ARB +8.3%, XPL +7.3%, BR +7.0%, LTC +6.4%.

**Dated catalysts found (all supply-side, all bearish):**
- **XPL — 09-25, 63.2% of circulating supply unlocked, ~$158M.** This is the single
  largest scheduled event on the board and XPL passes BOTH screens. Disqualified.
- ARB — 09-23 unlock (139.15M tokens), on both shortlists. Disqualified.
- Elsewhere this week: 0G (~$5.72M) and SENT (~$5.31M) 09-22, SOON (~$3.77M) 09-23,
  SOSO (~$7.44M) 09-24, H (~$19.2M) 09-25 — none in the tradeable universe.
- ~$900M of total unlock supply hits the market this week.

**Ideas, tagged by sleeve:**
- **CORE — NONE ADVANCED.** No shortlist name carries a dated, idiosyncratic catalyst. The
  two names that DO have dated events (XPL, ARB) both have bearish ones. Had one cleared,
  size would have been $26.67, stop 15% below entry, no target. Rejected before sizing, so
  no R:R computed.
- **TACTICAL — ranked shortlist handed to execute** (this run does not originate entries).
  Excluded from the ranking: XPL and ARB (dated unlocks), BTC (the benchmark — paying
  0.65% round-trip to track what buy-and-hold gets for 0%), STETH (duplicate ETH
  exposure), POL (already held). Ranked by hourly 7p among what remains:
  **1. BR  2. LTC  3. CHIP  4. SUI  5. MNT  6. PIEVERSE  7. ADA  8. HBAR**
  Size $10.00 each, stop 10% below entry (entry is the first high-water mark), limit at
  trigger*0.95, no target. R:R after the measured 0.65% round-trip friction is **unbounded
  on the upside by construction** — the trail is the only exit, so there is no fixed target
  to price a ratio against; the defined side is the ~10.65% all-in downside.
  CAVEAT the execute run should read: BR is +126.8% on 7 daily periods and +412.7% on 30.
  It tops the tactical list on the hourly screen while failing the daily one outright. It
  is the highest-variance name on the board, not the best one.

**EVIDENCE CHECK (STEP EVIDENCE):** Read the STANDING VERDICTS table before forming this
view. Nothing here rests on a REJECTED finding. Binding and relevant:
- The altcoin universe has a **CONFIRMED negative median** (-21.2% vs BTC +157.4% over
  5.7y) and every pair this account can buy is an alt.
- **Nothing tested beats buy-and-hold BTC** (best variant +27.3% vs BTC +157.4%).
- **Higher frequency is strictly worse** (-49.4% even at zero fees) and **tighter stops are
  strictly worse** (-44.8% -> -5.8% as the trail widens to none). Directly applied above in
  rejecting the SCAN GATE's 8% figure.
- Momentum is inverted at <=1d (IC@1d -0.012) but **positive at 30d** (IC@30d +0.025) —
  the 09-16 correction. Today's board sits squarely in the inverted window: the biggest 7p
  movers are what the CORE screen rejects, and chasing them trades the horizon where the
  measured IC is negative. This run does not argue the measured IC is wrong.
- Hypothesis #6 (1 CORE slot, PROMOTED 09-18) states its own mechanism honestly: the
  preference for fewer slots is monotone and extrapolates toward zero exposure, so it is
  "hold less of a universe with no long edge", NOT evidence of a long edge. It does not
  argue for filling the single CORE slot.

**SHADOW LOG — first scored cohort, and it argues AGAINST the gate.** The 13 rows from
2026-09-16 hit T+5d today and were scored. **Every single one rose.** Median +21.9%,
range +13.3% to +54.4%. Nine of twelve distinct names beat BTC's +13.3% over the same
window. The two rejected for bearish unlocks did best of all (ARB +54.4%, and XTZ +41.2%).
Read honestly: this is ONE five-day window inside a market-wide melt-up where 57 of 60
pairs are green, so it measures the regime far more than it measures the gate — a random
pick would also have been up. It is not evidence of skill in the skips and it is not a
reason to loosen anything today. It IS the first real datapoint that the entry gate's
rejections are expensive in a rising tape, and the weekly review should look at it against
the 09-17 and 09-18 cohorts when those score (09-22 and 09-23). Logged, not acted on.

**Risk factors:**
- BTC overbought on both daily (RSI 71.6) and hourly (84.8) and outside the upper Bollinger
  — the two open TACTICAL positions are long alt beta into that.
- Dominance 59.1% with the alt-season index depressed: the CONFIRMED negative alt median is
  the active regime, and both holdings are alts.
- ~$900M of unlock supply this week, including XPL's 63.2%-of-float event on 09-25 — a
  name that PASSES both screens. A screen pass is not a safety check for supply events.
- Both holdings are 66.9h old against a 72h time stop, exempt only by being >= +5%. A
  modest pullback in either re-arms the time stop mid-window with no run watching.
- Breadth this extreme (57/60 green) means screen passes carry near-zero selection
  information right now.
- No cuts priced for 2026 and DXY ~99.4; the macro tailwind that drove this bounce is
  priced, not pending.

**Decision:**
- **CORE: HOLD — binding for the day.** No name clears the dated-idiosyncratic-catalyst
  bar; the only dated events on shortlisted names are bearish supply releases. 59.1%
  dominance in a confirmed negative-median alt universe is the wrong regime to spend the
  single CORE slot.
- **TACTICAL: recommendation only, NOT a stand-down.** Quota is **0/2 for 2026-09-21 with
  one entry window left (18:07)**. The execute run MUST fill it from the ranked list above
  (or from its own fresh screen) — no catalyst is required, the technical screen is the
  thesis, and 'patience' / 'no conviction' are CORE arguments that do not excuse a
  TACTICAL miss. Only the 8 hard safety gates do. Budget, breaker and slots are all clear:
  4 TACTICAL slots free, $178.53 cash, deployment would go to ~21% against a 50% ceiling.
- Cash is a position; this run does not buy to correct deployment, and did not buy at all.

**Fee budget:** **$0.52 / $8.00** used this MONTH (headroom $7.48), month started
2026-09-01. Two ratchet amends this run cost $0.00 — amends are not fee-bearing. The budget
is a CEILING, not a target; BTC buy-and-hold, the benchmark, pays 0%.

**Circuit breaker:** CLEAR. $0.00 realized today vs the $10.00 limit; 0 consecutive losing
closes; most recent loss closed 2026-09-15.

**Shadow log:** 69 rows appended (27 CORE + 42 TACTICAL passes, all skipped), priced from
this screen run; 13 rows from 09-16 scored. Next cohort to score: 09-17 (30 rows) on 09-22.

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

## 2026-09-21T16:20 UTC — RESEARCH RE-RUN (second research run this UTC day)

A research run already completed today (commit `8b6d6c8`, plus its 15:10 addendum written
after the concurrent `execute` run `53bf98b`). This is a SECOND scheduled invocation on the
same UTC day. Everything below is a delta against that entry, not a replacement for it.

### Account snapshot (scripts/state.sh, exchange clock 16:20 UTC)
EQUITY $200.00 (budget cap; account holds $179,060.62 — not tradeable)
FREE $158.90 | DEPLOYED $41.10 = 20.5% of budget (ceiling 50%, no floor)

| Symbol | Qty | Entry | Price | P&L | Age | Stop | Coverage | Sleeve |
|---|---|---|---|---|---|---|---|---|
| ARB | 42.424653 | 0.2381 | 0.2322 | -2.48% | 1.3h | 0.2143 | 100% [OK] | TACTICAL |
| OP | 84.895020 | 0.11764 | 0.1270 | +7.99% | 68.2h | 0.1198 | 100% [OK] | TACTICAL |
| POL | 93.006900 | 0.10708 | 0.1134 | +5.93% | 68.2h | 0.1031 | 100% [OK] | TACTICAL |
| XPL | 97.502400 | 0.1023 | 0.1003 | -1.97% | 1.3h | 0.0922 | 100% [OK] | TACTICAL |

No position is naked. None is near its sleeve hard cut (TACTICAL -10%; worst is ARB at
-2.48%). CORE slot empty. 2 TACTICAL slots free of 6.

### STEP A — reconcile, stops, cut, ratchet
- RECONCILE: live holdings match the TRADE-LOG tail exactly. No fill and no stop execution
  between the 15:10 addendum and this run. No drift to log.
- RESTING LEG: all 4 carry exactly ONE resting conditional stop at 100% of held qty. No
  target legs, nothing split, nothing unreserved. No action.
- HARD CUT: none triggered.
- RATCHET: **no ratchet placed, and the advisory gate was deliberately NOT obeyed.**
  - `state.sh` SCAN-VERDICT flagged POL and XPL as "ratchet may be due", both computed on
    an **8% trail**. The 8% trail is only earned at **+20%** (TRADING-STRATEGY.md, TACTICAL
    ratchet). POL is +5.93% and XPL is -1.97%, so the correct trail for both is 10%. The
    gate is SHADOW MODE and advisory; obeying it would have moved stops to levels the
    rulebook does not authorise. Same defect the 09-18 and 09-21-morning runs logged, still
    present.
  - Verified against actual high-water marks (`bybit.py kline`, daily + hourly):
    OP HWM 0.13315 -> 10% = 0.11984 (resting 0.1198, already correct);
    POL HWM 0.1146 -> 10% = 0.10314 (resting 0.1031, already correct);
    ARB post-entry HWM ~0.23823 -> 10% = 0.21441 (resting 0.2143, already correct).
  - XPL post-entry HWM 0.10279 -> 10% = 0.09251 vs resting 0.0922: a genuine but trivial
    +0.3% improvement, worth **$0.03** on a $9.77 position. Declined deliberately — a
    cancel-then-replace opens a brief window with no resting stop, and paying real
    operational risk for $0.03 four days before XPL's unlock is a bad trade. A judgement
    call, stated, not an oversight. The next run should place it if the high-water rises
    materially.

### Market context (STEP B — perplexity.sh has no API key, exits 0 with a warning; fell back to native WebSearch as the routine directs)
- BTC ~$85.9k on the Bybit tape, ~$85k externally; **BTC.D ~59.1%**, total cap ~$2.88T.
  Daily RSI14 ~71.6, hourly ~84.8 — overbought. Fear & Greed 70 ("Greed"), not euphoric.
- ETH $2,762 on Bybit, above the ~$2,672 Fib level; a weekly close above opens $2,950-3,000.
  Spot ETH ETFs on a **4th consecutive positive week**, ~$1.2-1.75B/month — but **72% of the
  streak is BlackRock's ETHA alone**. Concentrated single-desk flow, not broad demand.
- **MACRO IS THE NEW FACT AND IT IS HAWKISH:** the Fed **HIKED 25bp on 2026-09-16** to
  3.75-4.00%, unanimous, first hike in three years, with 16 of 18 officials seeing at least
  one more this year. Crypto is rallying INTO a tightening cycle — risk appetite running
  against its own liquidity backdrop.
- **2026-09-25 is a concentrated event day:** ~$16.6B Deribit BTC+ETH options expiry
  ($14.63B BTC), call-biased with max pain $72-75k BELOW spot, AND the XPL unlock. Flash
  PMIs land the same week.
- Narratives leading: AI x DePIN, stablecoins/payment rails, RWA, modular infra, prediction
  markets. L2s (OP, POL, ARB, MNT) are framed as distribution plays now, not scaling bets.
  Memes are NOT a named leading narrative this month — though PEPE/WIF top today's tape.

### Screen (STEP C — scripts/screen.sh, 60-coin universe)
Breadth is extreme: **47 of 60 names pass at least one sleeve.** That is a tape-wide move,
not selection information. CORE shortlist 27; TACTICAL shortlist 41.
Top by 7-period: PEPE +18.8, WIF +16.3, FET +9.7, BR +9.0, LTC +6.3, ARB +5.8, SUI +5.4,
HBAR +5.3, DOGE +5.1. Held names all still pass: ARB PASS/PASS, XPL PASS/PASS, POL PASS/PASS.

### Ideas, tagged by sleeve
**CORE — no idea advanced. HOLD, and it is BINDING for the rest of the day.**
This morning's run already wrote a binding CORE HOLD; nothing since changes it. It also
survives re-examination on the merits: 27 CORE names pass and not one carries a dated
idiosyncratic catalyst. The only two dated events on the entire board are bearish supply
releases (XPL 09-25, ARB 09-23). Size would be $26.67 at a 15% trail. Entering a 71-RSI
tape four days before a $16.6B expiry, on a screen where 47/60 names pass, with the Fed
actively hiking, is buying breadth at the top of its range for no idiosyncratic reason —
and "momentum is strong" is argued against by this repo's own measured IC@1d of -0.012
(STANDING VERDICTS). No CORE entry.

**TACTICAL — quota is MET, 2/2 (ARB and XPL, opened 15:05 by `execute` 53bf98b).**
Per TRADING-STRATEGY.md "DAILY TRADE QUOTA" 2 is a FLOOR, not a target, and it is satisfied.
This run originates nothing (research runs never do). Ranked handoff for the 18:07 execute
window **should it choose** to add beyond the floor — it is under no obligation to, and the
quota may NOT be cited to justify a third entry:
1. SUI 1.0286 (30p +27.6, vol 1.5%, spread 0.01%)  2. LTC 62.99 (7p +6.3, spread 0.02%)
3. HBAR 0.0932  4. DOGE 0.0968  5. RENDER 1.8070  6. BCH 264.70  7. MNT 0.6387  8. ADA 0.2449
Excluded: ARB/XPL/POL/OP already held; STETH duplicates ETH; ZETA (13.3% vol, 0.18% spread),
FLOCK and KII fail the spread/vol side. Size for any entry is $10.00 DERIVED (risk $1.00 /
10% trail) from `state.sh`, never fixed.

### Risk factors
- **XPL unlock 2026-09-25: 1.76B tokens, ~63.2% of circulating supply, ~$158M** — the
  largest scheduled event on the board, four days out, on a name this account HOLDS. A
  supply event that size can gap straight through the 5%-wide stop-limit band. The stop at
  0.0922 is the protection and it rests at 100%; the gap risk is ACCEPTED and stated, not
  hedged. A second XPL unlock (~29.7M, ~$28M) follows 09-28.
- ARB follow-on vesting print 09-23, two days out, inside the 72h time-stop window for a
  position opened 09-21T15:05.
- 09-25 Deribit expiry is call-biased with max pain well below spot. Dealer delta-hedging
  amplifies a move in EITHER direction — a volatility event, not a directional one.
- Fed hiking into a risk rally. On a hawkish print, a 71-RSI tape with 47/60 names extended
  unwinds fast and correlated.
- **Concentration: 4/4 positions are TACTICAL L1/L2 alts.** There is no diversification
  here, only four expressions of "alt beta up". Combined defined risk is ~$4.00 (2.0% of
  budget) against a $10.00 daily breaker, so it is bounded — but it is one bet, not four.

### Evidence check (STEP EVIDENCE)
Nothing here rests on anything marked REJECTED in HYPOTHESIS-LOG.md. No entry is justified
on short-horizon momentum (IC@1d -0.012, inverted), on one-sided volatility (#7 REJECTED),
or on 12-2 momentum (#9 REJECTED). Adding nothing is consistent with the CONFIRMED verdicts
that higher frequency is strictly worse and that the altcoin universe has a negative median.

### Decision
- **CORE: HOLD — binding for the day.** (Unchanged from the morning run.)
- **TACTICAL: nothing originated here. Quota MET 2/2; the handoff above is optional.**

### Fee budget
$0.52 / $8.00 used this MONTH (4.0% of equity). Headroom $7.48. This run spent **$0.00** —
no order was placed, cancelled or amended.

## 2026-09-22 — Research (UTC 16:15, broker clock)

> Run context: scheduled research run. Perplexity unconfigured (exit 0 with
> `PERPLEXITY_API_KEY not set`) — native WebSearch fallback used, as the routine
> permits. Credential check `bybit.py time` returned retCode 0.
> **Routine/rulebook version conflict:** `routines/research.md` is still v1 text
> (SPOT ONLY / long only / no leverage, 4 CORE + 6 TACTICAL, 4% fee budget,
> 2/day quota) while `memory/TRADING-STRATEGY.md` and `CLAUDE.md` are v4
> (perps, shorts, 5x, 1 CORE + 12 TACTICAL + 12 SHORT, 20% fee budget, no
> ceiling). Logged to OBSERVATIONS.md. No trade was originated on the contested
> ground, so the conflict did not change this run's actions.

### Account (from scripts/state.sh, budget basis $200)
- Equity $200.00 (budget) | FREE $171.11 -> ~$189.06 after the two cuts below
- DEPLOYED $28.89 = 14.4% -> $10.82 = 5.4% (ceiling 50%, no floor)
- Positions after STEP A: **1** (OP, TACTICAL, stop @100%)
- Fee budget $0.52 + $0.018 this run / $40.00 month — headroom ~$39.46
- Circuit breaker: realized today -$2.29 vs -$10.00 limit — CLEAR (2 consecutive losses, 1 short of the 3-streak halt)
- Perp book: 0 positions, gross notional $0 / $600

### STEP A invariants — ACTION TAKEN (2 hard cuts)
- RECONCILE: 3 live positions matched the TRADE-LOG tail on qty/entry. **Drift
  found:** ARB and XPL had NO resting stop (`*** NAKED ***`, 100% unreserved)
  despite the 2026-09-21 snapshot recording both at "YES — 100% of held qty".
  The stops are gone and no stop fill is recorded for either; the 09-21 20:11
  execute run's order activity is the likely point of loss. OP's stop is intact
  and `Untriggered` at $0.11983.
- HARD CUT: both naked positions were ALSO past the TACTICAL -10% threshold
  (ARB -10.65%, XPL -10.85%), so STEP 3 fired on both. Sold at market. Nothing
  to cancel first — there was no resting leg.
- RATCHET: none due. OP +8.28%, below the +20% that tightens it to 8%.
- TIME STOP: OP 92.1h old but +8.28% >= +5%, exempt.

### Market Context
- **BTC $86,225 spot (screen) / ~$86,624 quoted, +6.47% on the day** — first
  print above $86k since January; still 31.3% below the $126,080 ATH. 24h volume
  $56.2B, futures OI $61.4B (+7.2% / 30d).
- BTC dominance not printed for today; it has oscillated 53-64% through 2026 and
  crossed 60% earlier this year. The screen shows BTC at the BOTTOM of the
  7-period ranking (-0.0%) while alts print +30-90% — dominance is FALLING hard.
- **ETH broke $2.7K** ($2,735.92 on the screen), approaching $3,000.
- Macro: risk-on. Brent at a half-month low, US 10y **4.93%**. UNGA 81 runs
  09-22..28; NY Fed's Williams (permanent FOMC voter) speaks today. Next real
  catalysts are **PCE 09-30** and the **10-02 jobs report**.
- ETF flows: $433.0M net inflow into US spot BTC ETFs on 09-18; the week overall
  "barely stayed positive". Sept 3 saw $731M, the biggest day since 2026-01-14.
- **Unlocks: $4.7B in September** ($1.2B cliff / $3.5B linear), led by SUI
  ($153M, 1.3% of float), APT, ARB and ENA. XPL's own 63.2%-of-float unlock lands
  09-25, three days out — relevant to the XPL cut just executed.
- **$648M of SHORT positions were liquidated in 24h.** This is the single most
  important number in this entry; see the SHORT sleeve note.

### Narratives
- LEADING: L1 beta, violently — NEAR +90% (7p), AVAX +53.5%, SUI +45.5%,
  SEI +44.8%. DeFi close behind (UNI +44.3% / +103% 30p, ENA +46.8%, AERO +29.1%).
- ALSO LEADING: small-cap infra/AI lottery tickets — AURORA +504%, BR +319%,
  ZAMA +88%, ZETA +65%, FLOCK +37.9% / +172% 30p.
- ROLLING OVER: nothing is rolling over on the daily. On the HOURLY screen the
  majors (BTC, ETH, BNB, SOL, LINK) are flat-to-negative while alts run — this is
  a rotation OUT of majors, not a market top.
- Narrative-exit rule: L2 (ARB, XPL) just took two consecutive losses and is on
  the exit list for re-entry purposes.

### Shortlists (scripts/screen.sh, this run)
- **CORE (26, daily bars):** APT BONK ONDO ZRO AERO ADA KAS ZIG WLD DOGE FIL HYPE
  XRP SHIB XLM SOL MNT LTC LIT LINK ICP AAVE DATA ETH BTC BNB
  Top by 7p%: APT +40.0% (30p +20.1, vsSMA20 +19.7, vol 7.2%, spread 0.05%),
  BONK +37.2%, ONDO +30.3%, AERO +29.1%, ADA +27.5%.
- **TACTICAL long (17, hourly bars):** MON UNI FIL AVAX BONK HBAR LTC XRP ZIG WIF
  APT VIRTUAL MNT AAVE ADA DOGE GRAM
  Ranked head: MON (7p +4.9%, 30p +2.8, vsSMA20 +3.7, vol 1.0%, spr 0.04%),
  UNI (+3.6 / +1.8 / +1.9, spr 0.03%), HBAR (+2.3 / +8.2 / +2.8, spr 0.04%),
  FIL (+2.1 / +1.9 / +1.1, spr 0.05%), BONK (+2.1 / +7.9 / +1.4, spr 0.06%).
- **SHORT (33, hourly, weakest-first):** BR GRASS ZAMA AERO CC ZETA ENA VVV XPL
  PEPE DATA PUMP ARB SUI CRV ONDO NEAR SHIB ASTER KAS PENGU INJ SEI SKR LINK ICP
  HYPE SOL LIT TRUMP XLM JTO SPX

### Ideas, tagged by sleeve
**CORE — no idea advanced.** Size would be $26.67 (risk $4.00 = 2.0%, 15% trail).
The screen offers 26 passes, but CORE requires a DATED IDIOSYNCRATIC catalyst and
none of the 26 has one — today's move is undifferentiated beta off a macro
risk-on impulse, which is exactly the "news concentrates on what has already
moved" trap STEP C warns about. APT is the best-ranked name and carries a
*negative* dated catalyst (the September unlock cohort). Decision below.

**TACTICAL (long) — handed to execute as a ranked list, no catalyst required.**
Size $10.00 each (risk $1.00 = 0.5%, 10% trail). Stop = entry * 0.90 as the
trigger, with the limit at trigger * 0.95. R:R is unbounded by construction (no
target, trail only), so the 2:1-after-fees test is met by any name whose 10%
trail clears the 0.65% round trip — all 17 do. The binding constraint is spread,
and the five below are all <= 0.06%.
  1. MON $0.0265 — stop trig $0.02385, limit $0.02266
  2. UNI $9.1820 — stop trig $8.2638, limit $7.8506
  3. HBAR $0.0969 — stop trig $0.08721, limit $0.08285
  4. FIL $1.0069 — stop trig $0.90621, limit $0.86090
  5. BONK sub-cent; use the live quote — stop trig entry * 0.90
MON / UNI / HBAR / FIL are deliberately NOT the L2 narrative that just produced
two consecutive losses.

**SHORT (perp) — RECOMMEND STAND-DOWN THIS RUN. Non-binding.**
This is the one place where I argue against taking a passing screen, so the
reasoning is stated explicitly rather than as "no conviction":
- $648M of shorts were liquidated in the last 24h. The screen ranks 33 names as
  short candidates because they are weak *on the hourly* — measured inside the
  squeeze that just destroyed the previous cohort of shorts.
- HYPOTHESIS-LOG standing verdict, CONFIRMED: high-vol names are lottery-shaped
  (p99 +206.8%, max +832%) and "shorting them is right most days and
  catastrophic occasionally." The top of the short list is BR (+319% 7p), GRASS,
  ZAMA (+88%), ZETA (+65%) — these ARE that right tail.
- Standing verdict, CONFIRMED: momentum is inverted only at <= 1 day; at 30 days
  it is POSITIVE (IC +0.025). Every top short candidate has a strongly positive
  30-period reading, so the short book would be fighting the horizon where the
  measured IC is on the other side.
- Liquidation clearance is satisfiable at 3x (10% stop vs the 16% allowance), so
  this is a signal objection, not a mechanical one.
If execute disagrees and opens shorts, the mechanics it must use: `bybit.py
leverage SYM 3` first, `category: linear`, an attached `stopLoss` at entry * 1.10,
and `bybit.py funding SYM` checked first — a short PAYS funding when funding is
negative, and funding is likely deeply positive-to-the-longs after a +6.5% day,
which favours the short carry. That carry is real and is the strongest argument
against my own recommendation here.

### Risk Factors
- Two consecutive realized losses today. A third trips the circuit breaker and
  halts entries for the rest of the UTC day.
- The stop-disappearance defect is unexplained. Until the cause is known, every
  run must verify stop presence from `state.sh` and never from the prior log.
- $4.7B of September unlock supply, concentrated in SUI / APT / ARB / ENA — four
  names that appear on today's shortlists.
- BTC +6.47% in a day is a large move, and 1-day mean reversion is the one thing
  this repo has CONFIRMED (IC@1d -0.012). Fresh longs would be opened into that.
- Deployment is 5.4% against a 50% ceiling after the cuts — the participation gap
  that produced the -15.38pp edge is now WIDER, not narrower.

### Evidence check (STEP EVIDENCE)
Nothing in this plan rests on a REJECTED verdict. The TACTICAL hand-off is
screen-mechanical, not a momentum argument. The SHORT stand-down is argued FROM
two CONFIRMED verdicts rather than against them. The CORE HOLD is the documented
default. **New evidence generated this run:** the 09-17 shadow cohort scored
below — 27 of 28 up over 5 days, median ~+19% — is the strongest signal yet that
this account's leak is non-participation, not selection.

### Decision
- **CORE: HOLD.** Binding for the UTC day. No dated idiosyncratic catalyst.
- **TACTICAL: TRADE — recommendation only, non-binding.** Execute originates from
  the screen alone. Ranked list handed over above; 0 entries so far today against
  a 2/day floor and 11 free slots. An idle slot on this screen is a breach.
- **SHORT: stand-down RECOMMENDED, non-binding**, on the evidence above. Execute
  may override; if it does, the funding carry is the honest argument for it.

### Fee budget
$0.538 of $40.00 used this month (1.3%). Headroom ~$39.46. Churn is not the leak.
