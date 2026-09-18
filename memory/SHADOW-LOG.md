# Shadow Log — screened but NOT taken

Purpose: SAMPLE SIZE. This account closes ~2-4 real trades a month, so judging
the entry gate on realised trades alone would take a year. Every candidate that
PASSES a sleeve's technical screen but is not bought is recorded here with its
price, then scored 5 days later. That yields ~40-60 observations a month at zero
cost and zero risk.

What this answers, and nothing else answers:
- Does a screen PASS actually precede an up-move, or is the gate noise?
- Are the trades we DO take better than the ones we skip, or is selection adding
  nothing on top of the screen?
- Would a wider or narrower gate have helped? (Counterfactual, not hindsight.)

RULES
- Append-only. Never delete or edit a row once written; a wrong prediction is the
  entire point of the file.
- Record the price AT THE TIME OF THE SCREEN, from the same `screen.sh` run that
  produced the pass. Never backfill a price later — that is hindsight.
- Score at T+5d in the research run: `outcome` is the % change from screen price,
  and `MFE` is the best close in the window (did it trend at all?).
- Rows are EVIDENCE for the weekly review only. They are NOT a trade trigger and
  never justify an unscheduled amendment.

| date (UTC) | pair | sleeve | screen px | reason not taken | T+5d % | MFE % | scored |
|---|---|---|---|---|---|---|---|
| 2026-09-16 | UNI | CORE | 6.3393 | catalyst stale (~8d old, fee-switch burn), already priced +93%/30d, DeFi narrative has 1 tactical loss (UNI itself, 09-15) | | | |
| 2026-09-16 | ARB | CORE | 0.1538 | same-day token unlock (~$13M, 0.93% supply) is a bearish overhang | | | |
| 2026-09-16 | FIL | CORE | 0.8126 | no confirmed catalyst, momentum/speculation only | | | |
| 2026-09-16 | XTZ | CORE | 0.2448 | catalysts (X mainnet, Etherlink 7.0) undated/ongoing | | | |
| 2026-09-16 | ARB | TACTICAL | 0.1538 | same-day token unlock (~$13M, 0.93% supply) is a bearish overhang | | | |
| 2026-09-16 | XRP | TACTICAL | 1.2944 | catalyst (CLARITY cloture) already failed 09-15, caused this week's tactical stop-out | | | |
| 2026-09-16 | DOT | TACTICAL | 0.9508 | no catalyst found; L1/L2 narrative already has 1 tactical loss (09-14) | | | |
| 2026-09-16 | WIF | TACTICAL | 0.1792 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-16 | BTC | TACTICAL | 75943.8655 | shared FOMC/macro catalyst only, not idiosyncratic | | | |
| 2026-09-16 | HYPE | TACTICAL | 77.2080 | unlock already happened Sept 6, priced in, no fresh trigger | | | |
| 2026-09-16 | SOL | TACTICAL | 97.1300 | no dated catalyst found | | | |
| 2026-09-16 | ETH | TACTICAL | 2403.9500 | shared FOMC/ETF-flow catalyst only; already the account's CORE exposure, would concentrate risk | | | |
| 2026-09-16 | DOGE | TACTICAL | 0.0801 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | ONDO | CORE | 0.3748 | closest CORE name (RWA/SEC roundtable 09-17) but catalyst undated and sector-shared, not idiosyncratic | | | |
| 2026-09-17 | AAVE | CORE | 129.1600 | no dated catalyst; DeFi narrative not bid under >60% dominance | | | |
| 2026-09-17 | FET | CORE | 0.1693 | AI narrative present but no dated idiosyncratic catalyst | | | |
| 2026-09-17 | HYPE | CORE | 83.4100 | Sept-6 unlock already priced, no fresh trigger | | | |
| 2026-09-17 | DOT | CORE | 1.0798 | no catalyst; L1 narrative already carries a tactical loss (09-14) | | | |
| 2026-09-17 | INJ | CORE | 5.7340 | no dated catalyst | | | |
| 2026-09-17 | JUP | CORE | 0.2335 | no dated catalyst | | | |
| 2026-09-17 | XLM | CORE | 0.1863 | no dated catalyst | | | |
| 2026-09-17 | LTC | CORE | 53.9100 | no dated catalyst | | | |
| 2026-09-17 | AVAX | CORE | 7.6190 | no dated catalyst | | | |
| 2026-09-17 | BNB | CORE | 735.1000 | no dated catalyst | | | |
| 2026-09-17 | ASTER | CORE | 0.7460 | no dated catalyst | | | |
| 2026-09-17 | AERO | CORE | 0.5873 | no dated catalyst; negative 7p momentum | | | |
| 2026-09-17 | FLOCK | CORE | 0.0679 | no dated catalyst; -5.1%/7p | | | |
| 2026-09-17 | PIEVERSE | CORE | 1.2949 | leads CORE on momentum (+12.9%/7p) but no catalyst found; widest spread on the shortlist (0.16%) | | | |
| 2026-09-17 | ARB | TACTICAL | 0.1774 | dated BEARISH catalyst: 139.15M-token unlock (1.4% supply) on 09-23 | | | |
| 2026-09-17 | CRV | TACTICAL | 0.3312 | no catalyst; DeFi narrative not bid | | | |
| 2026-09-17 | NEAR | TACTICAL | 3.0010 | no dated catalyst | | | |
| 2026-09-17 | BR | TACTICAL | 0.6734 | no dated catalyst; spread 0.19% | | | |
| 2026-09-17 | PEPE | TACTICAL | 0.0000 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | SHIB | TACTICAL | 0.0000 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | LINK | TACTICAL | 11.3610 | no dated catalyst | | | |
| 2026-09-17 | ENA | TACTICAL | 0.1550 | no dated catalyst | | | |
| 2026-09-17 | ADA | TACTICAL | 0.2028 | no dated catalyst | | | |
| 2026-09-17 | HBAR | TACTICAL | 0.0756 | no dated catalyst | | | |
| 2026-09-17 | BCH | TACTICAL | 232.7000 | no dated catalyst | | | |
| 2026-09-17 | POL | TACTICAL | 0.0977 | no dated catalyst | | | |
| 2026-09-17 | XPL | TACTICAL | 0.0862 | no dated catalyst | | | |
| 2026-09-17 | APT | TACTICAL | 0.5809 | no dated catalyst | | | |
| 2026-09-17 | WLD | TACTICAL | 0.3809 | no dated catalyst | | | |
| 2026-09-18 | ENA | CORE | 0.1654 | no dated catalyst; 40.63M unlock already cleared 09-02 | | | |
| 2026-09-18 | OP | CORE | 0.1121 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | PEPE | CORE | 0.0000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | HYPE | CORE | 91.5100 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | INJ | CORE | 6.5970 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SKY | CORE | 0.0707 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | AERO | CORE | 0.6504 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ZRO | CORE | 1.1246 | dated BEARISH catalyst: $26.4M ZRO unlock in the 09-14..09-20 window | | | |
| 2026-09-18 | FLOCK | CORE | 0.0691 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | APT | CORE | 0.6778 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ZIG | CORE | 0.0508 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ONDO | CORE | 0.3969 | mid-September ONDO unlock pending; RWA story undated and sector-wide | | | |
| 2026-09-18 | XPL | CORE | 0.0930 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | LIT | CORE | 4.8620 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | AAVE | CORE | 139.1300 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SUI | CORE | 0.8056 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | FET | CORE | 0.1846 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | BCH | CORE | 252.6000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ASTER | CORE | 0.7511 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | DOT | CORE | 1.1339 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SOL | CORE | 111.6200 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | AVAX | CORE | 8.1150 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | WLD | CORE | 0.4353 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | XLM | CORE | 0.1918 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | JUP | CORE | 0.2621 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ADA | CORE | 0.2202 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SHIB | CORE | 0.0000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | HBAR | CORE | 0.0787 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | LINK | CORE | 12.1970 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | LTC | CORE | 56.2100 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | BTC | CORE | 81,029.5000 | benchmark itself — buying BTC is not active alpha, pays fees to track | | | |
| 2026-09-18 | BNB | CORE | 761.1000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | MNT | CORE | 0.6047 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | DOGE | CORE | 0.0877 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | STETH | CORE | 2,599.8100 | wrapper on ETH, same exposure, worse liquidity | | | |
| 2026-09-18 | ETH | CORE | 2,600.6300 | no dated catalyst; ETH ETFs in 3rd straight day of net outflows (~$39M) | | | |
| 2026-09-18 | KII | CORE | 0.0820 | no dated catalyst; spread 0.35% — widest on the board | | | |
| 2026-09-18 | GRAM | CORE | 1.3800 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SOL | TACTICAL | 111.6300 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | XPL | TACTICAL | 0.0930 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | XRP | TACTICAL | 1.3852 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | TRUMP | TACTICAL | 2.1310 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ETH | TACTICAL | 2,601.1500 | no dated catalyst; ETH ETFs in 3rd straight day of net outflows (~$39M) | | | |
| 2026-09-18 | STETH | TACTICAL | 2,600.5200 | wrapper on ETH, same exposure, worse liquidity | | | |
| 2026-09-18 | BTC | TACTICAL | 81,029.5000 | benchmark itself — buying BTC is not active alpha, pays fees to track | | | |
| 2026-09-18 | AERO | TACTICAL | 0.6504 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | PEPE | TACTICAL | 0.0000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | INJ | TACTICAL | 6.5970 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | NEAR | TACTICAL | 3.6340 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ARB | TACTICAL | 0.2149 | dated BEARISH catalyst: 139.15M ARB unlock (1.4% supply) 09-23 | | | |
| 2026-09-18 | HYPE | TACTICAL | 91.4900 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | AAVE | TACTICAL | 139.1300 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | LINK | TACTICAL | 12.1970 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | DOGE | TACTICAL | 0.0877 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | VIRTUAL | TACTICAL | 0.6609 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | XLM | TACTICAL | 0.1918 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | AVAX | TACTICAL | 8.1150 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | PENGU | TACTICAL | 0.0078 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | PUMP | TACTICAL | 0.0043 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ONDO | TACTICAL | 0.3969 | mid-September ONDO unlock pending; RWA story undated and sector-wide | | | |
| 2026-09-18 | MNT | TACTICAL | 0.6049 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | GRASS | TACTICAL | 0.3411 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | ADA | TACTICAL | 0.2201 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | BCH | TACTICAL | 252.5000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | APT | TACTICAL | 0.6780 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | HBAR | TACTICAL | 0.0787 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | POL | TACTICAL | 0.1015 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | MON | TACTICAL | 0.0243 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | JUP | TACTICAL | 0.2621 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SHIB | TACTICAL | 0.0000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | BNB | TACTICAL | 761.1000 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | OP | TACTICAL | 0.1121 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | SUI | TACTICAL | 0.8056 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | LTC | TACTICAL | 56.2100 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | GRAM | TACTICAL | 1.3800 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | CRV | TACTICAL | 0.3422 | no dated idiosyncratic catalyst | | | |
| 2026-09-18 | KII | TACTICAL | 0.0820 | no dated catalyst; spread 0.35% — widest on the board | | | |
