# Idea 8 - Polanyi's Paradox and the Moving Frontier

*Machines, Platforms, Crowds*, ch. 1-3. We know more than we can tell, so tasks
nobody can specify resist automation. The book argues machine learning dissolves
that bound by requiring examples instead of rules.

## What is being tested

Polanyi and Moravec together predict which jobs go first: work whose rules can
be written down. Work that is tacit, perceptual or manual should be protected,
because nobody can state the procedure. The book's claim is that the protection
is ending. That is a prediction about the composition of employment, and it can
be checked.

## The judgement made openly

Testing this needs a measure of how tacit each occupation is. The standard
source is O*NET's task ratings, whose bulk files need version-specific download
URLs that would have to be guessed, which is the practice that produced a
mislabelled figure in Idea 5. So this notebook writes out its own classification
of occupation groups into Autor's four quadrants, prints it in full, checks that
every group in the data is classified, and invites disagreement. Edit the
`QUADRANT` dictionary and rerun to test an alternative.

## The check on that judgement

Employment composition moves for many reasons unrelated to automation: ageing,
trade, the housing cycle, a pandemic. Figure 5 shuffles the quadrant labels
across occupations two thousand times and asks whether the real classification
separates the trends better than random labels do. It reports a p-value and an
explicit verdict.

Validated first on synthetic data: p = 0.000 against a planted task signal,
p = 0.43 when occupation groups drift at random. It detects a real pattern and
refuses to invent one.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `08_polanyis_paradox.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached Census responses, one per year |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, two CSVs, then the technical summary |

## Running it

Needs stacklib 0.8.0, which adds `census_group_labels`: it reads occupation
labels from the Census metadata endpoint so variables are selected by their
published label hierarchy rather than by assumed variable numbers. Roughly
fifteen API calls on the first run, all cached afterwards.

The notebook stops with a clear message if any occupation group in the data is
missing from the classification, because unclassified groups would silently break
the shares.

## The five figures

1. `fig1_quadrant_shares` - employment share by how codifiable the work is
2. `fig2_frontier_shift` - trend by quadrant, before and after deep learning
3. `fig3_occupation_ranking` - which occupation groups grew and shrank
4. `fig4_headcount_vs_pay` - losing workers, or losing wages
5. `fig5_permutation_benchmark` - does the classification explain anything

## Send back

The PNGs, the printed occupation tree, the unmapped-groups check, the quadrant
share table, the early-against-late comparison, the ranked occupation table, and
`findings/headline_numbers.json`. The permutation verdict decides how much of
this the article can use.
