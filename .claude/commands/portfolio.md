---
description: Read-only crypto snapshot — account, positions, resting stops, coverage gaps
---

Print a clean ad-hoc snapshot. No state changes, no orders, no file writes.

1. bash scripts/bybit.sh account
2. bash scripts/bybit.sh positions
3. bash scripts/bybit.sh orders
4. bash scripts/bybit.sh quote <each held pair>

Format as a single concise summary:

Crypto Portfolio — <UTC date/time>
Equity: $X | Cash: $X (X%) | Deployed: X%
Positions:
  PAIR | qty | Entry -> Last | Unrealized | Stop trigger | Stop present?
Open orders:
  TYPE | PAIR | qty | stop/limit | order_id

Commentary ONLY if something is broken, and these are the things that matter:
- a book position with NO resting trigger sell (naked over a 6h gap)
- a stop whose qty no longer matches its position
- a stop trigger ABOVE current price (would fire instantly)
- a position already past -15% that the stop failed to catch
