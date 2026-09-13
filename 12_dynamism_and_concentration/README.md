# Idea 12 - Dynamism and Concentration

**Phase two. Zero to One, chapters 3, 5 and 7, against Brynjolfsson and McAfee.**

## The claim being tested

Both books need concentration, for opposite reasons. Thiel argues a serious
business escapes competition and becomes a monopoly, and that the economy is
renewed by new firms going from zero to one and displacing the incumbents they
beat. Brynjolfsson and McAfee argue that low marginal cost and network effects
hand the winner a share the loser cannot contest.

They differ on one testable point. Thiel's account requires churn. New firms
arriving and old ones dying is what makes concentration legitimate rather than
merely large. If concentration rose while entry fell, the economy is
concentrating without the creative destruction that is supposed to justify it.

## Why this question and not the tail

Idea 7 could not test the power law in household income because the ACS stops
resolving at $200,000. Census business data has the same problem in a different
costume: the largest firm class is "10,000 employees and over", so Thiel's
monopolists live inside the last bin.

Dynamism escapes that ceiling. Entry and exit are rates over all firms, not
properties of the largest one, so top-coding does not touch them.

## What this notebook does

| Section | Question | Figure |
|---|---|---|
| Discovery | What does BDS actually publish? | none, printed |
| - | Do the share and index estimators recover planted values? | none, asserted |
| A | Has establishment entry fallen? | 1 |
| B | Has employment moved toward large firms? | 2 |
| C | Both, on one time axis | 3 |
| D | Within sectors, or reallocation between them? | 4 |
| E | Do young firms still hold the jobs? | 5 |

Section D is a shift-share decomposition and satisfies an exact identity, which
the notebook asserts before reporting the result.

## The caveat that matters most

BDS counts employment, not revenue, profit or market value. A software firm can
dominate a market with few employees, so employment concentration understates
digital concentration. The test is therefore biased against both books rather
than toward them, which makes a positive result stronger and a null weaker.

## Sources

Census Business Dynamics Statistics, national, 1978 to 2023, via
api.census.gov/data/timeseries/bds. Every variable name, geography level and
categorical code is read from the API's own metadata endpoints. Nothing is
typed from memory.

## Run order

Run top to bottom. The three discovery cells print the variable listing, the
geography listing and the code lists for firm size, firm age and sector. If a
later cell warns, or the size and age labels look wrong, send that output back
and the selections can be re-pointed without repeating the fetches.
