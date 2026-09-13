# Idea 3 - The GPT Lag

*The Second Machine Age*, ch. 7, and *Machines, Platforms, Crowds*, ch. 1.
General purpose technologies pay off decades after they arrive.

## What is different about this notebook

The lag is normally asserted by placing two curves side by side, which can only
illustrate a lag that has already been assumed. This notebook estimates it:
correlate IT capital deepening in year t with productivity growth in year t+k
for k from 0 to 25, and find the peak. A placebo capital series gets the
identical treatment, because a lag that appears for every kind of investment
says nothing about general purpose technologies.

The estimator was checked against synthetic data with a planted 14-year lag. It
recovered 14 exactly from first differences, returned a spurious 3 from levels,
and stayed flat on the placebo. Both the levels and the differenced versions are
plotted for that reason.

## A known limitation, stated up front

The book's Figure 7.2 needs US labour productivity back to 1890. BLS major-sector
productivity starts in 1947 and BEA's accounts start in 1929, so that half of the
figure cannot be rebuilt from these APIs. Figure 2 substitutes the Federal
Reserve industrial production index, which reaches 1919 and measures output
rather than productivity. The figure illustrates the shape of an adoption era and
proves nothing on its own; the caption and the write-up both say so.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `03_gpt_lag.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached BEA and FRED responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, two CSVs, then the technical summary |

## The five figures

1. `fig1_it_investment_wave` - IT and structures as shares of investment
2. `fig2_two_eras` - electrification and the IT era, each on its own clock
3. `fig3_lag_profile` - correlation against lag, with the placebo
4. `fig4_peak_lag_scatter` - the underlying points at the preferred lag
5. `fig5_growth_by_window` - TFP growth across the four standard windows

## Send back

The PNGs, the FRED candidate printout, the peak table, the window table, and
`findings/headline_numbers.json`. The placebo row decides how much this section
can claim.
