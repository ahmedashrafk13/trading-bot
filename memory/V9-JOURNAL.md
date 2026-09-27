# V9 journal - one short entry per run

## 2026-09-24 18:13 UTC (18:00 bar) - first v9 run
- Strategy: SHORT ADA $67.24 (z +1.64), LONG DOT $49.27 (z -1.93); other 10 flat. Book held nothing before.
- Decided: approve both. News scan: ADA up on Mastercard/x402 news, DOT on the 21Shares spot ETF and a short squeeze. No hack, delisting, unlock or macro print inside the 6h hold. Chasing momentum against the signal is the override that has cost money before.
- Fills: ADA Sell 274 @ 0.2457, DOT Buy 42.5 @ 1.1584, both maker (100%), fees $0.02. SL ADA 0.2653 / DOT 1.0642. 0 blocked, 0 stop problems.
- P&L since v9 start: status shows $-7.62, but the positions account for only about $-0.08 (uPnL plus fees). The rest is stablecoin peg drift: P&L = USD totalEquity of the whole demo wallet ($129k USDT + $50k USDC). A 0.05% peg wobble moves it about $90, near the -$100 auto-halt. Owner should switch the P&L to a USDT/position basis.
- 2026-09-24 18:42 UTC owner-side fix: P&L now measured on the USDT coin's equity (not the wallet's USD total incl. USDC), re-baselined; P&L since start -$0.22. Auto-halt can no longer trip on stablecoin peg noise.

## 2026-09-25 07:15 UTC (06:00 bar) - ran ~1h late; no 00:00-bar run on record
- Strategy: SHORT ADA $67.24 (z +2.15), LONG DOT $49.27 (z -1.70); other 10 flat. Book already held both from the 18:00 bar.
- Decided: approve both. WebSearch (perplexity key not set): ADA still riding Mastercard/x402 news, DOT on the ETF and Polkadot 2.0; no hack, delisting, unlock or outage. Next macro print is Durable Goods at 12:30 UTC, after this hold.
- Fills: none needed (gap to target below min order); 0 blocked, 0 stop problems. SL ADA 0.2653 / DOT 1.0642 in place. Maker share to date 100% (2 fills).
- P&L since v9 start: $-0.66 (-0.3% of budget); uPnL ADA -0.47, DOT -0.17.

## 2026-09-25 13:46 UTC (12:00 bar) - ran ~1h40m late
- Strategy: SHORT ADA $67.24 (z +2.10), LONG DOT $49.27 (z -1.54); other 10 flat (SOL z -1.42, LINK +1.35 just under the line). Book already held both.
- Decided: approve both. WebSearch: ADA still on Mastercard/x402/IndiaChain news, DOT on the TDOT ETF and Polkadot 2.0; no hack, delisting, unlock or outage. 12:30 UTC macro prints (GDP, durables, claims) and the quarterly options expiry are already past; August PCE is tomorrow, outside this hold.
- Fills: none needed (gap to target below min order); 0 blocked, 0 stop problems. SL ADA 0.2653 / DOT 1.0642 in place. Maker share to date 100% (2 fills).
- P&L since v9 start: $-1.45 (-0.7% of budget); uPnL ADA -2.06, DOT +0.67.

## 2026-09-25 18:12 UTC (18:00 bar) - on time
- Strategy: NEW LONG SOL $82.87 (z -2.01); keep SHORT ADA $67.24 (z +1.99) and LONG DOT $49.27 (z -1.55); other 9 flat.
- Decided: approve all three. WebSearch: SOL near $120 (8-month high) on ETF inflows and a record in daily users; Alpenglow upgrade is Sep 28, after this hold. Bitget hot-wallet hack (Sep 24 18:31 UTC) is exchange-specific and does not touch our coins. No delisting, unlock or macro print on a Friday evening.
- Fills: SOL Buy 0.6 @ 122.00, maker (qty rounded down to $73 vs $83 target), fee $0.01; SL 112.34. ADA/DOT unchanged. 0 blocked, 0 stop problems. Maker share 100% (3 fills).
- P&L since v9 start: $-1.69 (-0.8% of budget); uPnL SOL +0.02, ADA -2.74, DOT +1.07.

## 2026-09-25 23:18 UTC (18:00 bar again) - off-schedule re-run, ~42 min before the 00:00 bar
- Strategy: same as 18:12 - LONG SOL $82.87 (z -2.01), SHORT ADA $67.24 (z +1.99), LONG DOT $49.27 (z -1.55); other 9 flat. Book already held all three.
- Decided: approve all three. WebSearch: nothing new since 18:12 (SOL ~$117-118 on ETF inflows, ADA ~$0.25 after its weekly rally, DOT ~$1.18 on ETF inflows and Polkadot 2.0). Bitget hack does not touch our coins. August PCE (Sep 26 12:30 UTC) is outside this hold.
- Fills: none needed (gap to target below min order); 0 blocked, 0 stop problems. SL SOL 112.34 / ADA 0.2653 / DOT 1.0642 in place. Maker share 100% (3 fills).
- P&L since v9 start: $-0.95 (-0.5% of budget); uPnL SOL +0.03, ADA -3.53, DOT +2.58. Scorecard: 3 runs, Claude value-add $0.00.

## 2026-09-26 08:09 UTC (06:00 bar) - ran ~2h late; the 00:00-bar run (00:11) wrote decisions but never executed or committed
- Strategy: keep LONG SOL $82.87 (z -1.97) and SHORT ADA $67.24 (z +2.45); NEW SHORT LINK $72.19 (z +1.83); close DOT (z -0.89); other 8 flat.
- Decided: approve all. WebSearch: SOL ~$120 on ETF inflows, ADA up on Mastercard/Fireblocks news, LINK +4-5% on Infosys/Arc news and range-bound 13.7-14.2. No hack, delisting, unlock or outage. Saturday, so no macro print (the "PCE Sep 26" in earlier entries was wrong: Sep 26 is a Saturday).
- Fills: LINK Sell 5.1 @ 14.032 maker (SL 15.153); DOT Sell 42.5 @ 1.2215 taker, closed (bought 1.1584, about +$2.68 gross). 0 blocked, 0 stop problems. Maker share 80% (5 fills).
- P&L since v9 start: $-0.59 (-0.3% of budget); uPnL LINK +0.03, ADA -2.30, SOL -0.90. Scorecard: 5 runs, Claude value-add $0.00.

## 2026-09-26 12:12 UTC (12:00 bar) - on time
- Strategy: keep LONG SOL $86.99 (z -1.84), SHORT ADA $67.24 (z +1.92), SHORT LINK $72.19 (z +1.74); other 9 flat.
- Decided: approve all. WebSearch: SOL ~$120 at $120-122 resistance (Schwab opened SOL/AVAX/LINK trading), ADA below $0.23 resistance, LINK dipped after the Infosys deal. The Bitget hack is exchange-specific. No delisting, unlock, outage or macro print (Saturday).
- Fills: SOL Buy 0.1 @ 121.16 maker (top-up to 0.7, SL now 111.52). ADA/LINK unchanged. 0 blocked, 0 stop problems. Maker share 83% (6 fills).
- P&L since v9 start: $-2.05 (-1.0% of budget); uPnL SOL -0.46, LINK -1.01, ADA -3.18. Scorecard: 6 runs, Claude value-add $0.00.

## 2026-09-26 18:39 UTC (18:00 bar) - ran ~32 min late
- Strategy: keep LONG SOL $86.99 (z -2.02) and SHORT ADA $67.24 (z +1.82); close LINK (z 0.76, crowd back to normal); other 9 flat.
- Decided: approve all. WebSearch: SOL ~$121 at $120-122 resistance (slot time cut to 250ms), ADA ~$0.255 after ~20% weekly rally (Cardano AI-payments news). No hack, delisting, unlock, outage or macro print (Saturday).
- Fills: LINK Buy 5.1 @ 14.18 taker, reduce-only, closed (sold 14.032, about -$0.75 gross). SOL/ADA gap below min order. 0 blocked, 0 stop problems. SL SOL 111.52 / ADA 0.2653 in place. Maker share 71% (7 fills).
- P&L since v9 start: $-1.22 (-0.6% of budget); uPnL SOL -0.50, ADA -2.52. Scorecard: 7 runs, Claude value-add $0.00.

## 2026-09-27 07:25 UTC (06:00 bar) - ran ~78 min late; the 00:00-bar run never happened (no commit, no journal)
- Strategy: keep LONG SOL $91.18 (z -1.72); close SHORT ADA (z 1.16, back inside band); other 10 flat.
- Decided: approve all. WebSearch: SOL ~$120.7, flat 24h, range 119.9-122.0 (ZetaChain vote, Alpenglow testnet). Bitget hack (Sep 24) is exchange-specific and old news. GRASS unlock does not touch our coins. No delisting, outage or macro print (Sunday).
- Fills: ADA Buy 274 @ 0.2569 maker, reduce-only, closed (sold 0.2457, about -$3.07 gross). SOL gap below min order. 0 blocked, 0 stop problems. SL SOL 111.52 in place. Maker share 75% (8 fills).
- P&L since v9 start: $-1.56 (-0.8% of budget); uPnL SOL -0.26. Scorecard: 8 runs, Claude value-add $0.00.
