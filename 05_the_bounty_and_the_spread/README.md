# Idea 5 - The Bounty and the Spread

*The Second Machine Age*, ch. 9 and 11. Output per person rises; the typical
household stops sharing in it.

## The methodological decision

The productivity-versus-pay gap is the most contested chart in American
economics, and much of the dispute is about deflators. Output per hour is
deflated by the prices of what workers produce; real compensation is normally
deflated by the prices of what workers consume. Those indexes diverge, so a gap
appears even when labour's share of output has not moved.

Feldstein raised this in 2008 and Stansbury and Summers worked it through in
2017. This notebook draws the gap both ways and reports what share of it is
deflator choice and what share survives.

The decomposition was validated against synthetic data first. In a constructed
world with a 14.5 per cent fall in labour's share and consumer prices outrunning
output prices, the surviving gap recovered the labour-share decline exactly
(0.855 against 0.855). Whatever survives in the real data is therefore
interpretable as the labour-share story, which is Idea 6.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `05_bounty_and_spread.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached FRED responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, the gap series as CSV, then the technical summary |

## Running it

FRED only, no BEA. This notebook needs more series than any previous one, so it
searches FRED first, prints the candidates with their coverage, then resolves
each series through an ordered fallback list and prints which identifier it
actually used. Two sections degrade gracefully rather than failing: the earnings
by education series and the mean household income series both skip with a
message if nothing resolves.

## The five figures

1. `fig1_bounty_and_spread` - real GDP per capita against real median household income
2. `fig2_deflator_decomposition` - productivity and pay under two deflators
3. `fig3_productivity_and_employment` - Bernstein's decoupling, extended past 2011
4. `fig4_earnings_by_education` - real weekly earnings by credential
5. `fig5_mean_vs_median` - how far the average sits above the middle

## Send back

The PNGs, the FRED candidate printouts, the resolution list showing which
identifier each series used, the deflator decomposition printout, and
`findings/headline_numbers.json`.
