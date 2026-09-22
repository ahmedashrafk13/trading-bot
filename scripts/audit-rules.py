"""Audit every prompt and doc for statements that contradict the current rules.

Run it after ANY amendment:  python scripts/audit-rules.py


The bot's rules live in twelve files that all restate them. Every amendment so
far has left at least one file behind, and a stale restatement is not cosmetic:
a run reads ONE prompt and obeys whatever it says.

This has already bitten three times: the sizing amendment left the sleeve
inference inverted ($40=CORE when CORE had become ~$20), the circuit-breaker
change left eight files cutting only at -15%, and the CORE trail change left
the 20% ladder in ten prompts. Each was found by accident.

Add a BAD entry whenever a rule changes: the old wording becomes the pattern.
Lines that EXPLAIN a removed rule are skipped via the keyword filter, so a
handful of false positives on prohibition lines is expected and harmless.
"""
import pathlib
import re

# (label, regex, why it is wrong now)
BAD = [
    ('old CORE stop at entry', r'fill \* 0\.80|stop 20% below fill', 'CORE stop is 15% below fill'),
    ('v1 tactical 6% stop', r'TACTICAL -> stop\s+6% below fill|stop 6% below entry', 'TACTICAL trails 10% in v2'),
    ('old CORE trail 20%', r'20% below high-water|trail 20%', 'CORE trail is 15% since 2026-09-15'),
    ('old CORE rung 14%', r'14% (?:once|at) \+30', 'CORE tightens to 12% at +30%'),
    ('old circuit breaker 3%', r'3%[- ]daily|3% of equity \(~\$6|<= *-?0?\.?03 of equity', 'breaker is 5%'),
    ('old fixed sizing', r'\$40 \(20%\)|\$40 = CORE|\$20 = TACTICAL|\$40 CORE / \$20'
     r'|(?:CORE|TACTICAL).{0,12}:\s*\$(?:40|20)', 'size is risk-derived, from state.sh'),
    ('deployment floor', r'75-85%|75%-85%', 'deployment has a ceiling only'),
    ('split machinery', r'\[SPLIT ok\]|SPLIT the qty|split: ~half|ORPHAN CHECK', 'split removed'),
    ('resting take-profit', r'entry\s*\*\s*1\.14|fill\s*\*\s*1\.14|rests its \+?14% TARGET|resting LIMIT at the \+14%',
     'no resting take-profit exists'),
    ('blanket -15% cut', r'any position at unrealized_plpc <= -0\.15', 'TACTICAL cuts at -10%'),
    # --- v4, 2026-09-22: perps/shorts/leverage enabled, trade ceiling removed.
    # The v4 commit missed routines/research.md entirely and this audit could not
    # catch it, because no pattern described the OLD wording. These are those
    # patterns. Add one for every rule you change, or the audit is decorative.
    ('v1 spot-only mandate', r'SPOT ONLY|spot only, long only|never a short|never perps'
     r'|no perpetuals|Long only\.', 'v4 enables linear perps, shorts and leverage <=5x'),
    ('v1 long-only mandate', r'never attempt a short|long only, never|Long only\.',
     'shorts are enabled via linear perps since 2026-09-22'),
    ('old fee budget 4%', r'4\.0% \(~\$8\.00\)|\$8\.00 MONTHLY|4\.0% of equity \(~\$8',
     'fee budget is 20.0% (~$40.00)/month since 2026-09-22'),
    ('old 2/day quota as a ceiling-era rule', r'>= 2 TACTICAL entries/day quota|/ 2 minimum',
     'there is NO trade ceiling; 2/day is a floor that should never bind'),
    ('reverted 24h time stop', r'24h time stop|24h TIME STOP|24 HOURS after fill',
     'time stop is 72h: 24h was measured on the hourly cache (-83.97% vs -75.24%) and reverted'),
    ('old sleeve counts', r'TACTICAL 6(?![0-9])|6-position TACTICAL|4-position CORE|combined <= 7',
     'CORE 1 / TACTICAL 12 / SHORT 12'),
    ('REJECTED STOP SHAPE - limit stop, rejected at activation',
     '"orderType":"Limit".*"orderFilter":"StopOrder"|price":"<trig[*]0[.]95>|trigger [*] 0[.]95',
     'spot stops are conditional MARKET orders with no price field (2026-09-22)'),
    ('deployment ceiling superseded by margin', r'deployment <= 50% of equity|total deployment after fill',
     'v4 uses MARGIN <=50% of budget + GROSS NOTIONAL <=300%'),
    # `\bused this week` is anchored: without the word boundary it also matched
    # "ca-used this week's ..." in SHADOW-LOG.md data rows (false positive,
    # found 2026-09-17 weekly review).
    ('v1 weekly fee budget', r'1\.5%.{0,24}\(~?\$3|weekly fee budget|weekly ceiling|\bused this week|resets Monday',
     'budget is 1.0% MONTHLY, resets on the 1st'),
    ('v1 85% deployment ceiling', r'85% (?:of equity|deployment)|deployment (?:<=|after fill <=) ?85%'
     r'|CEILING 85%|85% deployment ceiling|deployment <= 85',
     'deployment ceiling is 50% since 2026-09-17 (hypothesis #3)'),
    ('v1 4-slot CORE / 5 combined', r'Max positions \| 4|positions after fill <= 4|max 4\)'
     r'|Combined cap: 5|Combined positions after fill <= 5|4/1 slot split',
     'CORE is 1 slot, combined cap 2, since 2026-09-18 (hypothesis #6)'),
    ('reintroduced take-profit leg', r'"takeProfit"|BOTH LEGS ATTACHED|that both legs exist|stop, TP,',
     'neither sleeve has a profit target — only a stopLoss leg is ever attached'),
    ('streak carried across UTC days', r'3 stops tactical for the day\)',
     'the 3-loss streak is scoped to the UTC day and resets at 00:00 UTC'),
    ('superseded 30d momentum inversion', r'30-day momentum is INVERTED|30-day momentum likewise|IC -0\.037',
     '30d momentum is POSITIVE (+0.025 test); only <=1d is inverted (corrected 2026-09-16)'),
    ('ghost second scan routine', r'scan\.md.? ?x2|scan-2|37 \* \* \* \*|EVERY 30 MIN',
     'there is ONE scan routine, hourly at :07'),
    ('v1 48h age rule', r'open >\s*~?48h|48h reassess|closed for being 48h', 'no time limit in v2'),
    ('v1 slot counts', r'after fill <= 3, cost ~\$(?:40|20)|Combined .{0,20}<= 6', 'caps are 4 CORE / 1 TACTICAL / 5 total'),
    ('alpaca leftovers', r'(?i)alpaca|stop_limit|time_in_force|crypto-bars',
     'the venue is Bybit spot — no Alpaca surface may remain'),
]

# Append-only RECORDS, not instructions. They quote superseded rules by design
# (that is what a log of superseded rules is for), so scanning them produces
# nothing but false positives. Added HYPOTHESIS/OBSERVATIONS/SHADOW/SCAN-GATE
# 2026-09-17: no run obeys these files, it only appends to them.
# A line that NARRATES a repealed rule ("v1-v3 read X — REVOKED", "superseding
# the old Y") is documentation, not a stale restatement. Without this the audit
# flags its own changelog and trains you to ignore it.
HISTORY = ('REVOKED', 'superseded', 'SUPERSEDED', 'v1-v3 read', 'previously',
           'used to', 'was REVOKED', 'no longer', 'replacing the old',
           'historical note', 'Historical note')

SKIP = {'memory/TRADE-LOG.md', 'memory/RESEARCH-LOG.md', 'memory/WEEKLY-REVIEW.md',
        'memory/HYPOTHESIS-LOG.md', 'memory/OBSERVATIONS.md', 'memory/SHADOW-LOG.md',
        'memory/SCAN-GATE-LOG.md', 'DAILY-SUMMARY.md'}


def main():
    root = pathlib.Path('.')
    files = [p for p in root.rglob('*.md') if '.git' not in p.parts
             and 'archive' not in p.parts]
    files += list(root.glob('scripts/*.sh'))

    findings = 0
    for p in sorted(files):
        rel = p.as_posix().lstrip('./')
        if rel in SKIP:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        for i, line in enumerate(text.split('\n'), 1):
            # Lines that EXPLAIN the old rule are fine; lines that INSTRUCT are not.
            if re.search(r'removed|was |old |legacy |since 2026-09-15|NEVER infer|no longer|expired|REJECTED|STALE|SUPERSEDED|BANNED|grandfathered|v1 ',
                         line, re.I):
                continue
            if any(h.lower() in line.lower() for h in HISTORY):
                continue
            for label, pat, why in BAD:
                if re.search(pat, line, re.I):
                    print(f'  {rel}:{i}  [{label}] {why}')
                    print(f'      {line.strip()[:100]}')
                    findings += 1
    print(f'\n{findings} suspect line(s)')
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())
