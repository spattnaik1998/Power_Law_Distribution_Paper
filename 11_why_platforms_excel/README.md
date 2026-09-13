# Idea 11 - Why Platforms Excel

**Machines, Platforms, Crowds, Chapter 8**

## The claim being tested

Platforms beat incumbents three ways. They raise the utilisation of perishable
inventory, they attack information asymmetry, and they price along the demand
curve in ways their own suppliers find painful and cannot match.

The pricing argument is the distinctive one. An incumbent estimates demand from
the range of prices it has historically charged, which is the flat, high-price
end of the curve. If the true curve decays exponentially, the volume far down it
is enormous and invisible from where the incumbent stands, so it concludes a low
price destroys revenue. On a two-sided platform the logic goes further: lower
the price on the elastic side, raise it on the inelastic side, and where the
cross-elasticity is large enough, a negative price is rational.

## What this notebook does

| Section | Question | Figure |
|---|---|---|
| A | How much perishable capacity used to go unsold? | 1 |
| B | Did e-commerce displace the incumbent retail format? | 2 |
| C | How wrong is an incumbent that extrapolates from its own price band? | 3 |
| D | When does the optimal price on one side turn negative? | 4 |
| E | Did hotel prices break away once home-sharing scaled? | 5 |

Sections C and D are simulations with planted answers. Exponential demand is
revenue-maximised at exactly the decay constant, and the zero-cross-elasticity
two-sided problem separates into two textbook monopoly problems. Both closed
forms are asserted before the results are used.

Section E is built to return a null. National series carry no price tier and no
city, so they cannot reproduce the Austin result, and a placebo on a service
with no platform substitute says whether the test measures anything.

## Not attempted

- **The lemons problem.** No public series measures information asymmetry. The
  chapter's deepest idea stays literature.
- **Platform concentration and switching costs.** Firm-level.

## Sources

FRED, with every series resolved by search and verified against its official
title. The search helper filters on identifier prefix as well as title, because
Idea 9 shipped a figure in which a national request resolved to Massachusetts.
Zervas and Proserpio on Airbnb in Austin, and Akerlof on lemons, are cited from
the reading notes as literature.

## Run order

Run top to bottom. Every `pick_fred` call prints its candidate listing. If a
section warns, send that listing back and the query can be re-pointed without a
rerun.
