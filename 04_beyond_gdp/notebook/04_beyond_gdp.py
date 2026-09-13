# %% [markdown]
# # Idea 4 - Beyond GDP
#
# **The claim (Second Machine Age, ch. 8).** What we care about in an economy of
# bits is increasingly ideas rather than things, and GDP does not measure it.
# The notes record Brynjolfsson's estimates of internet value per user, Gordon's
# view that official numbers miss about 0.4 percent of growth a year, and the
# Stiglitz, Sen and Fitoussi case for overhauling the statistics. Samuelson's
# defence of the national accounts is recorded alongside them.
#
# **The analytical spine of this notebook.** Consumer surplus under a
# constant-elasticity demand curve has a closed form. If quantity demanded is
# Q = A·P^(−ε) with ε > 1, then the surplus enjoyed above the going price works
# out to
#
#     surplus = expenditure / (ε − 1)
#
# That formula is the standard way to value a good that got cheap. Apply it to a
# good that became free and expenditure is zero, so the computed surplus is zero.
# The method that prices cheapness returns nothing for the things that stopped
# being priced at all. That degeneracy is the chapter's argument written as
# algebra, and it is why the second half of this notebook inverts the question
# instead of answering it directly.
#
# **The four steps.**
#
# 1. **What the accounts already added.** Software was capitalised in 1999, R&D
#    and artistic originals in 2013. Their share of GDP is the size of what
#    counting differently put on the books.
# 2. **Surplus we can compute.** Apply the formula to priced information
#    technology and see how much it adds under a range of elasticities.
# 3. **The degeneracy.** Show the same formula returning zero for free goods.
# 4. **The inversion.** Rather than assert what free services are worth, compute
#    what they would have to be worth per person to move measured growth by a
#    tenth, a quarter, or Gordon's four tenths of a point, and let the reader
#    judge whether that figure is plausible.
#
# **Data.** BEA NIPA and Fixed Assets, FRED for GDP and population. The BEA
# tables are discovered through the API's own parameter list rather than guessed.

# %%
import sys, pathlib, warnings, importlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

_here = pathlib.Path.cwd()
for _cand in [_here, *_here.parents]:
    if (_cand / "common" / "stacklib.py").exists():
        sys.path.insert(0, str(_cand / "common"))
        break
import stacklib as sl
importlib.reload(sl)

warnings.filterwarnings("ignore", category=FutureWarning)
print("stacklib version:", sl.__version__)

DIRS = sl.dirs_for("04_beyond_gdp")
KEYS = sl.load_keys()
sl.apply_theme()

BEA = sl.require(KEYS, "BEA")
FRED = sl.require(KEYS, "FRED")
ELASTICITIES = [1.5, 2.0, 3.0]
GROWTH_GAPS = [0.1, 0.2, 0.3, 0.4]      # percentage points of annual GDP growth

# %% [markdown]
# ## 1. What the accounts added when they changed the rules
#
# Software entered measured investment in the 1999 comprehensive revision; R&D
# and entertainment originals entered in 2013. Before those dates the same
# spending was treated as a cost of doing business and vanished from the
# investment account. Their current share of GDP is a direct measure of what
# recounting put on the books.

# %%
inv_cur = sl.bea_nipa_table("T50305", BEA, frequency="A", cache_dir=DIRS["data"])
LINES = {"All fixed investment": 1, "Info processing equip.": 10, "Computers": 11,
         "Intellectual property": 16, "Software": 17, "Research and development": 18,
         "Artistic originals": 19}
EXPECT = {1: "private fixed investment", 10: "information processing", 11: "computers",
          16: "intellectual property", 17: "software", 18: "research and development",
          19: "entertainment"}
descs = dict(zip(inv_cur["line"], inv_cur["description"].astype(str).str.strip().str.lower()))
bad = {ln: descs.get(ln) for ln, w in EXPECT.items() if w not in (descs.get(ln) or "")}
if bad:
    raise AssertionError("BEA line numbering has moved. Mismatches: %s" % bad)
print("line numbering verified\n")
CUR = sl.pick_lines(inv_cur, LINES) / 1000.0   # BEA millions -> billions, to match FRED GDP

def annual(s):
    a = s.groupby(s.index.year).mean(); a.index = a.index.astype(int); return a

gdp_id, gdp_raw = sl.fred_first_available(["GDPA", "GDP"], FRED, cache_dir=DIRS["data"])
GDPN = annual(gdp_raw)                                  # nominal GDP, $bn
rgdp_id, rgdp_raw = sl.fred_first_available(["GDPCA", "GDPC1"], FRED, cache_dir=DIRS["data"])
RGDP = annual(rgdp_raw)
pop_id, pop_raw = sl.fred_first_available(["CNP16OV", "POPTHM"], FRED, cache_dir=DIRS["data"])
POP = annual(pop_raw) / 1000.0                          # thousands -> millions
print("\nGDP %s, real GDP %s, population %s (millions, %.1f in %d)"
      % (gdp_id, rgdp_id, pop_id, POP.iloc[-1], POP.index[-1]))

# Units guard. BEA NIPA values arrive in millions of dollars and FRED GDP in
# billions; dividing one by the other without rescaling silently inflates every
# share by 1000. Private fixed investment has run between 12 and 25 per cent of
# GDP for the whole postwar period, so anything outside that band is a unit bug.
_check = float(CUR["All fixed investment"].dropna().iloc[-1] / GDPN.dropna().iloc[-1] * 100)
assert 10 < _check < 30, ("Units look wrong: private fixed investment computes to "
                          "%.0f%% of GDP. Check the BEA millions-to-billions rescaling." % _check)
print("units guard passed: private fixed investment is %.1f%% of GDP" % _check)

# %%
capitalised = pd.DataFrame({
    "Software (counted from 1999)": CUR["Software"] / GDPN * 100,
    "R&D (counted from 2013)": CUR["Research and development"] / GDPN * 100,
    "Artistic originals (2013)": CUR["Artistic originals"] / GDPN * 100,
}).dropna()

fig, ax = plt.subplots(figsize=(9.5, 5.2))
for (name, color) in zip(capitalised.columns, sl.PALETTE[:3]):
    ax.plot(capitalised.index, capitalised[name].values, color=color, lw=2.0, label=name)
for yr in (1999, 2013):
    ax.axvline(yr, color=sl.INK["muted"], lw=1.0, ls=(0, (4, 3)), zorder=0)
    ax.text(yr + 0.6, ax.get_ylim()[1] * 0.96, str(yr), color=sl.INK["muted"], fontsize=9, va="top")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.1f%%" % v))
ax.set_ylabel("Share of GDP")
ax.set_title("What counting differently put on the books")
ax.legend(loc="upper left")
sl.save_fig(fig, "fig1_capitalised_intangibles", DIRS)
plt.show()
added = capitalised.iloc[-1].sum()
print("\nCombined share of GDP now counted as investment that once was not: %.2f%%" % added)

# %% [markdown]
# ## 2. The capital stock, and the part of it nobody counts
#
# The Fixed Assets tables are discovered from the API's own parameter list
# rather than guessed. Read the printout, then the chosen table's line
# descriptions, before trusting the figure.

# %%
tables = sl.bea_parameter_values("FixedAssets", "TableName", BEA,
                                 contains="current-cost net stock of private fixed assets")
print(tables.head(12).to_string(index=False) if len(tables) else "(no match; widen the filter)")

# %%
stock = None
for candidate in ["FAAt401", "FAAt101", "FAAt201"]:
    try:
        stock = sl.bea_table("FixedAssets", candidate, BEA, frequency="A", cache_dir=DIRS["data"])
        print("\nusing Fixed Assets table %s" % candidate)
        break
    except Exception as e:
        print("  %s did not work (%s)" % (candidate, str(e)[:80]))

if stock is not None:
    print("\nFirst 25 lines of the chosen table:")
    for _, row in stock[["line", "description"]].drop_duplicates().head(25).iterrows():
        print("   %4d  %s" % (row["line"], row["description"]))

# %%
if stock is not None:
    # FAAt401 is "by industry group": line 1 is the total and lines 2-4 split it,
    # after which the same four labels repeat for each industry. Address by
    # number, and verify the descriptions before trusting them.
    _d = dict(zip(stock["line"], stock["description"].astype(str).str.strip().str.lower()))
    _want = {1: "fixed assets", 2: "equipment", 3: "structures", 4: "intellectual property"}
    _bad = {k: _d.get(k) for k, v in _want.items() if v not in (_d.get(k) or "")}
    if _bad:
        raise AssertionError("Fixed Assets line numbering unexpected: %s" % _bad)
    S = sl.pick_lines(stock, {"All private fixed assets": 1, "Equipment": 2,
                              "Structures": 3, "Intellectual property": 4})
    if "Intellectual property" in S.columns and "All private fixed assets" in S.columns:
        ip_share = (S["Intellectual property"] / S["All private fixed assets"] * 100).dropna()
        fig, ax = plt.subplots(figsize=(9.2, 4.8))
        ax.plot(ip_share.index, ip_share.values, color=sl.PALETTE[0], lw=2.2)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
        ax.set_ylabel("Share of the private capital stock")
        ax.set_title("Intellectual property as a share of measured capital")
        ax.set_xlim(ip_share.index.min() - 2, ip_share.index.max() + 2)
        ax.annotate("%.1f%% in %d" % (ip_share.iloc[-1], ip_share.index[-1]),
                    xy=(ip_share.index[-1], ip_share.iloc[-1]), xytext=(-14, -30),
                    textcoords="offset points", ha="right", color=sl.INK["secondary"],
                    fontsize=10, arrowprops=dict(arrowstyle="-", color=sl.INK["axis"], lw=0.9))
        ax.annotate("%.1f%% in %d" % (ip_share.iloc[0], ip_share.index[0]),
                    xy=(ip_share.index[0], ip_share.iloc[0]), xytext=(16, 12),
                    textcoords="offset points", ha="left", color=sl.INK["secondary"], fontsize=10)
        sl.save_fig(fig, "fig2_intangible_capital_share", DIRS)
        plt.show()
    else:
        print("Could not locate the needed lines; skipping Figure 2.")
        ip_share = None
else:
    ip_share = None
    print("Fixed Assets unavailable; skipping Figure 2.")

# %% [markdown]
# ## 3. Surplus we can actually compute
#
# Under Q = A·P^(−ε), the surplus above the going price is expenditure/(ε − 1).
# The integral only converges for ε > 1, and the result is extremely sensitive to
# an elasticity nobody observes directly, so the figure shows a range rather than
# a number. Idea 1's price-quantity scatter is the closest thing we have to an
# empirical anchor for ε, and it is descriptive rather than identified.

# %%
it_spend = (CUR["Info processing equip."] + CUR["Software"]).dropna()
surplus = pd.DataFrame({("e = %.1f" % e): it_spend / (e - 1) / GDPN * 100
                        for e in ELASTICITIES}).dropna()

fig, ax = plt.subplots(figsize=(9.5, 5.0))
for (name, color) in zip(surplus.columns, sl.PALETTE[:3]):
    ax.plot(surplus.index, surplus[name].values, color=color, lw=2.0, label=name)
    sl.label_last(ax, surplus[name], name, color)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_ylabel("Implied surplus, share of GDP")
ax.set_xlim(surplus.index.min(), surplus.index.max() + 7)
ax.set_title("Surplus on priced information technology, by assumed elasticity")
ax.legend(loc="upper left")
sl.save_fig(fig, "fig3_surplus_priced_it", DIRS)
plt.show()
print(surplus.tail(1).round(2).to_string())

# %% [markdown]
# ### The degeneracy
#
# The same formula, applied to a good with a price of zero. This cell exists to
# be quoted rather than to produce a figure.

# %%
for label, expenditure in [("Priced IT investment, latest year", float(it_spend.iloc[-1])),
                           ("Web search", 0.0), ("Email", 0.0), ("Online maps", 0.0)]:
    row = ["%-34s expenditure $%9.1fbn" % (label, expenditure)]
    for e in ELASTICITIES:
        row.append("  e=%.1f: $%.1fbn" % (e, expenditure / (e - 1)))
    print("".join(row))
print("\nThe formula is not broken. It is answering the question it was asked,")
print("which is how much value sits above a price. With no price there is no")
print("integral to take, and the national accounts inherit the same silence.")

# %% [markdown]
# ## 4. The inversion
#
# Instead of asserting what unpriced digital services are worth, ask what they
# would have to be worth. For a given addition to annual real GDP growth, how
# much value per adult per year must be created and left uncounted?
#
# The calculation. Adding g percentage points to the growth rate of a GDP of Y
# requires uncounted output of roughly g/100 × Y in that year. Divided by the
# adult population, that gives dollars per adult per year. The figure shows the
# requirement for a few reference years so the reader can judge plausibility
# against their own use of these services.

# %%
years = [1995, 2010, int(min(GDPN.index.max(), POP.index.max()))]
gaps = np.linspace(0.05, 0.6, 60)

fig, ax = plt.subplots(figsize=(9.2, 5.2))
required = {}
for yr, color in zip(years, sl.PALETTE[:3]):
    y_gdp = float(GDPN.loc[yr]) * 1e9
    adults = float(POP.loc[yr]) * 1e6
    dollars = gaps / 100.0 * y_gdp / adults
    required[yr] = pd.Series(dollars, index=gaps)
    ax.plot(gaps, dollars, color=color, lw=2.2, label=str(yr))
for g in GROWTH_GAPS:
    ax.axvline(g, color=sl.INK["grid"], lw=0.9, zorder=0)
ax.set_xlabel("Percentage points added to annual real GDP growth")
ax.set_ylabel("Required uncounted value, dollars per adult per year")
ax.set_title("What free services would have to be worth")
ax.legend(loc="upper left", title="Year")
sl.save_fig(fig, "fig4_required_value_per_adult", DIRS)
plt.show()

latest = years[-1]
print("In %d, GDP of $%.1f trillion and %.0f million adults means closing a gap of:"
      % (latest, GDPN.loc[latest] / 1000.0, POP.loc[latest]))
for g in GROWTH_GAPS:
    need = float(required[latest].iloc[int(np.argmin(np.abs(gaps - g)))])
    print("   %.1f pp  ->  ${:,.0f} per adult per year".format(need) % g)

# %% [markdown]
# ## 5. Why the size of the gap matters more than it looks
#
# A few tenths of a point sounds like a rounding error. Compounded across three
# decades it is not. The figure shows measured real GDP per capita against the
# same series adjusted upward by the gaps Gordon and Brynjolfsson estimate.

# %%
START = 1995
rgdp_pc = (RGDP / POP.reindex(RGDP.index)).dropna()
rgdp_pc = rgdp_pc[rgdp_pc.index >= START]
base = rgdp_pc / rgdp_pc.iloc[0] * 100
t = np.arange(len(base))

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot(base.index, base.values, color=sl.PALETTE[0], lw=2.2, label="As measured")
for g, color in zip([0.3, 0.4], sl.PALETTE[1:3]):
    adj = base.values * (1 + g / 100.0) ** t
    ax.plot(base.index, adj, color=color, lw=2.0, ls=(0, (5, 3)),
            label="Plus %.1f pp a year" % g)
    ax.annotate("+%.0f%% by %d" % (adj[-1] - base.values[-1], base.index[-1]),
                xy=(base.index[-1], adj[-1]), xytext=(-8, 6), textcoords="offset points",
                ha="right", color=color, fontsize=9.5)
ax.set_ylabel("Real GDP per capita, %d = 100" % START)
ax.set_title("How much a few tenths of a point compound to")
ax.legend(loc="upper left")
sl.save_fig(fig, "fig5_compounding_gap", DIRS)
plt.show()

# %% [markdown]
# ## 6. Bank the numbers

# %%
payload = {
    "stacklib_version": sl.__version__,
    "gdp_series": gdp_id, "real_gdp_series": rgdp_id, "population_series": pop_id,
    "capitalised_shares_pct_latest": capitalised.iloc[-1].round(3).to_dict(),
    "capitalised_total_pct_of_gdp": float(added),
    "intangible_capital_share_pct": (None if ip_share is None
                                     else {"year": int(ip_share.index[-1]),
                                           "share": float(ip_share.iloc[-1])}),
    "surplus_pct_of_gdp_latest": surplus.iloc[-1].round(3).to_dict(),
    "elasticities_used": ELASTICITIES,
    "required_dollars_per_adult": {
        str(yr): {("%.1fpp" % g): float(required[yr].iloc[int(np.argmin(np.abs(gaps - g)))])
                  for g in GROWTH_GAPS} for yr in years},
    "compounding_start_year": START,
    "compounding_end_year": int(base.index[-1]),
    "measured_index_end": float(base.iloc[-1]),
    "adjusted_index_end": {("%.1fpp" % g): float((base.values * (1 + g / 100.0) ** t)[-1])
                           for g in [0.3, 0.4]},
    "series_used": {k: int(v) for k, v in LINES.items()},
}
sl.write_findings(payload, DIRS)
capitalised.to_csv(pathlib.Path(DIRS["findings"]) / "capitalised_shares.csv")
surplus.to_csv(pathlib.Path(DIRS["findings"]) / "surplus_by_elasticity.csv")
print("\nDone. Figures in figures/, numbers in findings/.")

# %% [markdown]
# ## Caveats to carry into the prose
#
# 1. **The surplus figures are an assumption wearing a number.** Everything in
#    Figure 3 scales as 1/(ε − 1), and ε is not observed. At ε = 1.1 the surplus
#    is ten times expenditure; below ε = 1 the integral does not converge at all.
#    Report the range and the sensitivity, never a point estimate.
# 2. **Business investment is not consumption.** The surplus computed here
#    accrues to firms buying equipment, not to households using free services.
#    It is the wrong side of the economy for the chapter's argument, and it is
#    included because it is the side that has prices.
# 3. **The inversion is arithmetic, not evidence.** Figure 4 says what free
#    services would have to be worth. It does not say what they are worth. Its
#    value is that it converts an unfalsifiable claim into a number a reader can
#    weigh against their own experience.
# 4. **GDP was never meant to measure welfare.** Kuznets said so when he built
#    it. Criticising it for failing at a job it does not claim is the weakest
#    version of this chapter's argument, and the strongest version is the
#    narrower one: the accounts mismeasure *production* when output moves to
#    zero-price channels.
#
# **Send back:** the five PNGs, the BEA Fixed Assets table printout, the
# degeneracy printout from section 3, the per-adult requirements, and
# `findings/headline_numbers.json`.
