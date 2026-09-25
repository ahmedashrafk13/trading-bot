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
