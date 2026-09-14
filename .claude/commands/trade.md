---
description: Manual crypto trade helper with rule validation. Usage — /trade BTCUSDT 0.0005 buy
---

Execute a manual crypto trade with full rule validation. Refuse if any rule fails.

Args: PAIR QTY SIDE (buy or sell). If missing, ask. PAIR is slash-formatted,
e.g. BTCUSDT. CRYPTO ONLY — refuse any stock or option outright.

1. Pull state: `bash scripts/pnl.sh` (the $200 book), `bybit.sh quote PAIR`
   (capture ask price P).
2. For BUY, validate the full gate:
   - Total positions after fill <= 5
   - Trades this week + 1 <= 3
   - QTY * P <= 20% of equity (~$40 at $200)
   - QTY * P <= available cash
   - PAIR is Bybit spot tradable (`bybit.sh instruments PAIR`), clears
     minOrderAmt, and is NOT a stablecoin
   - QTY >= that pair's min_order_size
   - Spread <= 1%
   - Catalyst documented (ask for the thesis if not in today's RESEARCH-LOG)
   - R:R >= 2:1 after ~0.5% round-trip fees
   If any fail, STOP and print the failed checks.
3. For SELL, confirm the position exists with at least that qty. No other checks.
4. Print the order JSON + validation results, ask "execute? (y/n)".
5. On confirm (market BUY qty is in USDT and needs marketUnit quoteCoin):
   bash scripts/bybit.sh order '{"category":"spot","symbol":"PAIR","side":"Buy","orderType":"Market","qty":"<USDT>","marketUnit":"quoteCoin","timeInForce":"IOC","orderLinkId":"tb-<sleeve>-SYMUSDT-<epoch_ms>"}'
6. For BUYs, immediately place the resting stop 20% below the ACTUAL fill:
   bash scripts/bybit.sh order '{"category":"spot","symbol":"PAIR","side":"Sell","orderType":"Limit","qty":"<wallet bal floored>","triggerPrice":"<fill*0.80>","price":"<fill*0.80*0.95>","orderFilter":"tpslOrder","timeInForce":"GTC","orderLinkId":"tb-<sleeve>-SYMUSDT-<epoch_ms>"}'
   Size it from the WALLET BALANCE, not execQty. If the stop fails twice,
   CLOSE the position and say so — never leave crypto unstopped.
7. Log to memory/TRADE-LOG.md: fill price, notional, -15% cut, stop trigger/limit,
   thesis, target, R:R, fees.
8. bash scripts/clickup.sh with the trade details.
