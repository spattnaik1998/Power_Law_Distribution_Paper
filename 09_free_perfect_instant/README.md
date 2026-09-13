# Idea 9 - Free, Perfect, Instant

**Machines, Platforms, Crowds, Chapter 6: The Economics of Bits**

## The claim being tested

Digital goods are free (zero marginal cost per copy), perfect (bit-identical
copies, no generational loss) and instant (the network moves a copy anywhere at
the same cost). The notes make the sharpest point about the third: free and
perfect are properties of the copy and create no value until copies can reach
people who want them.

## What this notebook does

| Section | Question | Figure |
|---|---|---|
| A | Did information-good prices behave differently from everything else? | 1 |
| B | Does the estimator recover a planted answer? | none, an assertion |
| C | Are the information goods special, or is this general deflation? | 2 |
| D | Did zero marginal cost unbundle the album and then rebundle it? | 3 |
| E | Did real music consumption rise while revenue fell? (Waldfogel) | 4 |
| F | What happened to newspaper employment, against who took the revenue? | 5 |

Section C is the benchmark. It scores the annualised price change for every
detailed consumption category BEA publishes and locates the information goods
in that distribution, so Section A's result is read against the whole basket
rather than against two hand-picked controls. This is the same discipline that
produced the nulls in Ideas 3 and 7.

## Not attempted

- **Network effects and winner-take-most.** Needs firm-level data the public
  statistics do not carry.
- **Consumer surplus on zero-price goods.** Idea 4 established that the standard
  constant-elasticity method returns exactly zero when price is zero. Cross-
  referenced rather than repeated.
- **Music quality.** The national accounts measure price and quantity, not
  quality, so Waldfogel's actual finding cannot be reproduced here. Section E
  answers the divisible part of it.

## Sources

BEA NIUnderlyingDetail tables U20403, U20404 and U20405 (real, price and
current-dollar PCE by type of product), table codes confirmed against
`GetParameterValues` rather than assumed. FRED CES employment series for
newspaper publishers, internet publishing, software publishers and motion
picture and sound recording, each resolved against its official title before
use. Newspaper revenue composition for 1995 is from the reading notes
(Newspaper Association of America) and is literature, not data.

## Run order

Run top to bottom. Two cells print catalogues of available BEA line
descriptions; if a later `pick_lines` call prints a WARNING, send those
catalogues back and the regex can be re-pointed without rerunning anything.
