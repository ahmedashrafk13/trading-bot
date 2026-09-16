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
