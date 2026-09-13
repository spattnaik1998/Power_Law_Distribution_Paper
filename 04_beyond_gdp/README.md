# Idea 4 - Beyond GDP

*The Second Machine Age*, ch. 8. What the national accounts miss when output
moves to zero-price channels.

## The spine of the analysis

Consumer surplus under constant-elasticity demand has a closed form:
surplus = expenditure / (elasticity - 1). It is the standard way to value a good
that got cheap. Applied to a good that became free, expenditure is zero and the
computed surplus is zero. The method that prices cheapness returns nothing for
the things that stopped being priced.

That degeneracy is why the notebook inverts the question in section 4. Rather
than assert what free services are worth, it computes what they would have to be
worth per adult per year to move measured growth by a tenth, a quarter, or
Gordon's four tenths of a point, and leaves the reader to judge plausibility.

The closed form was verified against numerical integration before shipping
(agreement to ten decimal places on a log-spaced grid).

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `04_beyond_gdp.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached BEA and FRED responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, two CSVs, then the technical summary |

## Running it

Needs `stacklib` 0.4.0, which adds `bea_table` for non-NIPA datasets and
`bea_parameter_values` for asking BEA what table codes exist. Restart the kernel
so the reload picks up the new version.

Section 2 queries the Fixed Assets dataset, which this project has not used
before. It asks BEA for the list of table names, tries three candidates in order,
and prints the line descriptions of whichever one resolves. If none resolve the
notebook skips Figure 2 and carries on rather than failing.

## The five figures

1. `fig1_capitalised_intangibles` - software, R&D and artistic originals as shares of GDP, with the 1999 and 2013 revision dates marked
2. `fig2_intangible_capital_share` - intellectual property as a share of the capital stock
3. `fig3_surplus_priced_it` - computed surplus on priced IT under three elasticities
4. `fig4_required_value_per_adult` - the inversion
5. `fig5_compounding_gap` - what a few tenths of a point compound to over thirty years

## Send back

The PNGs, the BEA Fixed Assets printout, the degeneracy printout from section 3,
the per-adult requirements, and `findings/headline_numbers.json`.
