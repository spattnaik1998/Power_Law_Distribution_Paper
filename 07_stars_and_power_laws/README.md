# Idea 7 - Stars, Superstars and the Power Law

*The Second Machine Age*, ch. 10. When pay tracks relative rather than absolute
performance, the earnings distribution grows a fat tail.

## What is being tested

The notes make a falsifiable claim: the US income distribution is a mixture of a
log-normal body and a power law tail, with the power law fitting the top best.
A power law is a straight line on log-log axes, so this can be checked rather
than asserted.

## The two things that make this notebook honest

**A built-in benchmark.** A straight line on log-log axes is necessary for a
power law, not sufficient. Before the real R-squared means anything, the
notebook runs the identical test on data generated from a log-normal, which is
not a power law by construction. In offline testing that scored 0.98. The real
data has to beat that benchmark to say anything, and the notebook prints an
explicit verdict comparing the two. Same discipline as Idea 3's placebo.

**A stated extrapolation boundary.** Public tabulations stop at "$200,000 or
more", so the superstar region is inside the last bracket and cannot be
resolved. Figure 3's counts above that line are extrapolation from a fit, marked
as such, and must never be quoted as counts of anybody.

The fitting machinery was validated first: the hand-rolled normal CDF agrees
with `math.erf` to 7e-08, and the grid fit recovers planted log-normal
parameters and a planted Pareto exponent exactly.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `07_stars_and_power_laws.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached Census and FRED responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, the bracket and quintile tables, then the technical summary |

## Running it

First use of the Census API in this project, so it tries the latest ACS 1-year
release and falls back two years if that is not published yet. It asserts that
the sixteen brackets reconstruct the published household total before using
them. Needs stacklib 0.7.0, which adds `fred_resolve` (title-verified series
resolution, promoted from Idea 6).

## The five figures

1. `fig1_lognormal_fit` - the distribution against a fitted log-normal
2. `fig2_tail_test` - the log-log survival plot, with both fits
3. `fig3_tail_predictions` - what each fit predicts above high thresholds
4. `fig4_quintile_shares` - income shares by fifth of households over time
5. `fig5_wage_dispersion` - 90/10, 90/50 and 50/10 earnings ratios

## Send back

The PNGs, the bracket table, both fit lines, **the benchmark verdict**, the
threshold comparison, the quintile table, and `findings/headline_numbers.json`.
The benchmark verdict decides how strongly the article can put this.
