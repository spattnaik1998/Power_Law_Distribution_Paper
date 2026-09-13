# Idea 10 - The Economics of Free

**Machines, Platforms, Crowds, Chapter 7: Paying Complements**

## The claim being tested

Two goods are complements when a fall in the price of A shifts the demand curve
for B outward. Drive a complement's price to zero and quantity of it rises
steeply, consumer surplus on it explodes because every taker captures their full
willingness to pay, and demand for the good you actually sell shifts out. Apple
does not fund Shazam or Angry Birds; it captures the demand shift from
complements the developers pay for.

Consumer surplus is the chapter's key quantity because it appears in nobody's
revenue. That makes it invisible in financial statements and visible in the
national accounts only as an absence.

## What this notebook does

| Section | Question | Figure |
|---|---|---|
| - | Does the rate estimator recover a planted answer? | none, an assertion |
| A | Across 398 categories, does a larger price fall go with larger quantity growth? | 2 |
| A2 | Does the result survive dropping nested subtotals, a rank test and a bootstrap? | none, printed |
| B | How often does a random pairing of prices and quantities produce that slope? | 1 |
| C | Did the collapsed categories lose share of the consumption dollar? | 3 |
| D | The surplus geometry, and the complement shift | 4 |
| E | Two complement pairs, described rather than inferred | 5 |

Section B is the benchmark and it decides how much Section A is worth. Section
A2 exists because BEA's detail table nests subtotals inside their own
components, so a fast-falling family can enter the cloud several times.

## Not attempted

- **Freemium and cannibalisation.** Needs firm-level pricing and conversion
  data. Nothing in the public accounts distinguishes a free tier from a paid one.
- **Consumer surplus in dollars.** Idea 4 established that the standard
  constant-elasticity formula returns exactly zero at a zero price, and is
  otherwise decided by an unobservable elasticity. Section D draws the shape of
  the prediction and labels it as arithmetic.
- **Two-sided network effects.** Firm-level, not in these data.

## Sources

BEA NIUnderlyingDetail tables U20403, U20404 and U20405: real quantity indexes,
price indexes and current-dollar personal consumption expenditures by type of
product. Idea 9's cache is reused when present, so the two notebooks cannot
diverge onto different vintages.

## Run order

Run top to bottom. If Section E or the `MARK` block prints a WARNING, send back
the surrounding output and the patterns can be re-pointed without a rerun.
