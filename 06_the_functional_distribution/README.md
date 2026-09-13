# Idea 6 - The Functional Distribution

*The Second Machine Age*, ch. 9. How national income splits between capital and
labour, and whether technology moved it.

## What this has to settle

Idea 5 found a 36-point productivity-pay gap surviving the deflator correction,
which implies labour's share fell about 14 per cent. That was an inference from
two series. This notebook measures the share directly.

## The measurement problem at the centre

Proprietors' income is the earnings of the self-employed and mixes a return to
labour with a return to capital. The accounts do not split it, and how you
handle that one line changes both the level and the trend. Gollin's 2002 paper
is about nothing else. The notebook computes the share three ways (narrow,
broad, and Gollin's proportional adjustment) and shows the spread. If all three
fall, the finding is robust to the assumption.

The three formulas were checked on constructed inputs first: the proportional
construction must lie between the narrow and broad bounds, and must equal the
narrow one when self-employment is zero. Both hold.

## The guard added after Idea 5

Idea 5 shipped a figure whose series were mislabelled, because identifiers were
guessed from a search and labels written from memory. Here every series
resolves, fetches its official FRED title, and asserts the title contains the
words the label claims. A wrong series stops the run instead of drawing a wrong
chart. `stacklib.fred_titles` (0.6.0) supplies the titles.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `06_functional_distribution.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached FRED and BEA responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, the three constructions as CSV, then the technical summary |

## The five figures

1. `fig1_labour_share` - the official series against the 64.3 per cent postwar norm
2. `fig2_proprietors_problem` - labour's share computed three ways
3. `fig3_labour_and_profits` - both as shares of GDP, on one axis
4. `fig4_international` - four rich economies, from the Penn World Table
5. `fig5_kn_mechanism` - the relative price of equipment against the labour share

## Send back

The PNGs, the resolution printout with verified titles, the three-construction
table, the international levels, and `findings/headline_numbers.json`. The
three-construction table decides how strongly the article can put this.
