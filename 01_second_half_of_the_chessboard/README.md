# Idea 1 - The Second Half of the Chessboard

*The Second Machine Age*, ch. 3. Exponential improvement in computing, and why
human intuition misreads it.

## Contents

| Folder | What is in it |
|---|---|
| `notebook/` | `01_chessboard.ipynb` (run this) and `01_chessboard.py`, the same code in percent format |
| `data/` | API responses cached as CSV on first run - delete to force a refresh |
| `figures/` | Five figures, PNG at 200 dpi plus SVG |
| `findings/` | `headline_numbers.json` and `loglinear_fits.csv`, then the technical summary |

## Running it

Needs `pandas`, `numpy`, `matplotlib`, `requests` (`scipy` optional, for the
Chow test p-value). Open the notebook and run all cells. It reads keys from
`../.env` by itself; BEA and FRED are the only ones used here.

Every API call is cached in `data/`, so a second run is offline and instant.
If a BEA line description fails to match, the notebook prints the whole list of
available lines and stops rather than charting the wrong series.

## The five figures

1. `fig1_linear_vs_log` - identical data on linear and log axes
2. `fig2_relative_price_of_computing` - computer prices deflated by GDPDEF
3. `fig3_rolling_rate` - trailing 10-year rate of decline; is the exponent stable?
4. `fig4_chessboard_squares` - cumulative halvings, i.e. which square we are on
5. `fig5_price_vs_quantity` - log-log quantity against price

## Send back

The PNGs, the printed fit table and Chow output, and `findings/headline_numbers.json`.
