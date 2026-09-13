# Idea 2 - Innovation: Declining or Recombining?

*The Second Machine Age*, ch. 5. Gordon and Cowen against Weitzman, Romer and
Arthur, adjudicated on research inputs and what they buy.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `02_recombination.ipynb` (run this) and its `.py` mirror |
| `data/` | Cached BEA and FRED responses |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | Headline numbers, three CSVs, then the technical summary |

## Running it

Same requirements as Idea 1. Needs `stacklib` 0.3.0 or later, which the import
cell reloads and reports. Uses the BEA and FRED keys only.

Two guards worth knowing about. The notebook asserts that Table 5.3.5 uses the
same line numbering as 5.3.4 before trusting it, and it searches FRED for the
productivity series rather than hard-coding an ID that may have been retired,
printing the candidates so the choice is visible.

## The five figures

1. `fig1_research_inputs_vs_gdp` - real R&D and software investment against real GDP
2. `fig2_investment_composition` - structures, equipment and intellectual property as shares of investment
3. `fig3_effort_and_payoff` - R&D input and TFP growth by decade, separate panels
4. `fig4_research_productivity` - productivity growth per unit of research input
5. `fig5_combinatorial_arithmetic` - Weitzman's arithmetic, labelled as arithmetic

## Send back

The PNGs, the FRED candidate tables from cell 5, the decade growth table, and
`findings/headline_numbers.json`.
