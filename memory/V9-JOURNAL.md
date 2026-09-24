# V9 journal - one short entry per run

## 2026-09-24 18:13 UTC (18:00 bar) - first v9 run
- Strategy: SHORT ADA $67.24 (z +1.64), LONG DOT $49.27 (z -1.93); other 10 flat. Book held nothing before.
- Decided: approve both. News scan: ADA up on Mastercard/x402 news, DOT on the 21Shares spot ETF and a short squeeze. No hack, delisting, unlock or macro print inside the 6h hold. Chasing momentum against the signal is the override that has cost money before.
- Fills: ADA Sell 274 @ 0.2457, DOT Buy 42.5 @ 1.1584, both maker (100%), fees $0.02. SL ADA 0.2653 / DOT 1.0642. 0 blocked, 0 stop problems.
- P&L since v9 start: status shows $-7.62, but the positions account for only about $-0.08 (uPnL plus fees). The rest is stablecoin peg drift: P&L = USD totalEquity of the whole demo wallet ($129k USDT + $50k USDC). A 0.05% peg wobble moves it about $90, near the -$100 auto-halt. Owner should switch the P&L to a USDT/position basis.
- 2026-09-24 18:42 UTC owner-side fix: P&L now measured on the USDT coin's equity (not the wallet's USD total incl. USDC), re-baselined; P&L since start -$0.22. Auto-halt can no longer trip on stablecoin peg noise.
