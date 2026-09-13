# %% [markdown]
# # Idea 6 - The Functional Distribution
#
# **The claim (Second Machine Age, ch. 9).** Technology has changed how national
# income splits between the owners of capital and the people who work. The notes
# record Fleck, Glaser and Sprague putting labour's share at an average of 64.3
# percent from 1947 to 2000, Karabarbounis and Neiman finding the decline is
# global and present within most countries and industries, and Marx and Ricardo
# predicting two centuries ago that mechanisation would end badly for workers.
#
# **Why this follows Idea 5.** The productivity-pay gap that survived the
# deflator correction was 36 index points, which implies labour's share of output
# fell about 14 percent. That was an inference from two series. This notebook
# measures the thing directly and asks whether the inference holds.
#
# **The measurement problem that decides the answer.** Proprietors' income is the
# earnings of the self-employed, and it mixes a return to their labour with a
# return to their capital. The national accounts do not split it. How you handle
# that one line item changes both the level and the trend of the labour share,
# which is why Gollin's 2002 paper is about nothing else and why Elsby, Hobijn
# and Sahin revisit it. This notebook computes the labour share three ways and
# shows the spread, in the same spirit as Idea 5's deflator treatment.
#
# **The five questions.**
#
# 1. Has labour's share fallen, and by how much against the 64.3 percent norm?
# 2. Does the answer survive the proprietors' income problem?
# 3. Where did the share go? Profits, as a share of the same GDP.
# 4. Is it global, as Karabarbounis and Neiman claim?
# 5. Does their proposed mechanism show up? They argue the cause is the falling
#    relative price of investment goods, which is exactly what Idea 1 measured.
#
# **A procedural change.** Idea 5 shipped a figure whose series were mislabelled
# because identifiers were guessed and labels written from memory. Every series
# here resolves, fetches its official FRED title, and asserts that the title
# contains the words it should. A wrong series now stops the notebook.

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
assert sl.__version__ >= "0.6.0", "needs stacklib 0.6.0 for fred_titles"

DIRS = sl.dirs_for("06_the_functional_distribution")
KEYS = sl.load_keys()
sl.apply_theme()
FRED = sl.require(KEYS, "FRED")
BEA = sl.require(KEYS, "BEA")

POSTWAR_NORM = 64.3      # Fleck, Glaser and Sprague, 1947-2000 average

# %% [markdown]
# ## 1. Resolve every series, and verify its title
#
# `resolve` fetches the data, looks up the official title, and fails loudly if
# the title does not contain the words the label claims. This is the guard that
# Idea 5 lacked.

# %%
def resolve(candidates, label, expect, **kw):
    sid, s = sl.fred_first_available(candidates, FRED, cache_dir=DIRS["data"], **kw)
    title = sl.fred_titles([sid], FRED).iloc[0]["title"]
    print("  %-26s %-20s %s" % (label, sid, title))
    missing = [w for w in expect if w.lower() not in str(title).lower()]
    if missing:
        raise AssertionError(
            "Series %s is titled %r, which is missing %s. Expected a series for %r. "
            "Fix the candidate list rather than the label." % (sid, title, missing, label))
    return sid, title, sl.to_annual(s)

print("=== searching for candidates ===")
for term in ["labor share nonfarm business", "compensation of employees paid",
             "proprietors income", "corporate profits after tax",
             "share of labour compensation in GDP"]:
    print("\n--- %s ---" % term)
    df = sl.fred_search(term, FRED, limit=5)
    print(df.to_string(index=False) if len(df) else "(nothing)")

# %%
print("\n=== resolving, with title verification ===")
ls_id,   ls_title,   LS_OFFICIAL = resolve(["PRS85006173"], "labour share index",
                                           ["labor share"])
coe_id,  coe_title,  COE  = resolve(["COE"], "compensation of employees",
                                    ["compensation", "employees"])
pi_id,   pi_title,   PI   = resolve(["A041RC1Q027SBEA", "PROPINC"], "proprietors' income",
                                    ["proprietors"])
gdp_id,  gdp_title,  GDPN = resolve(["GDP"], "nominal GDP", ["gross domestic product"])
cp_id,   cp_title,   CP   = resolve(["CPATAX", "CP"], "corporate profits", ["corporate profits"])

# %% [markdown]
# ## Figure 1 - Labour's share against the postwar norm
#
# The official BLS series first, as published, with the 64.3 percent average the
# notes record from Fleck, Glaser and Sprague drawn across it. The BLS series is
# an index rather than a percentage, so it is rescaled to sit on a share basis
# using its own 1947-2000 mean.

# %%
ls = LS_OFFICIAL.dropna()
pre2000 = ls[ls.index <= 2000]
ls_pct = ls / pre2000.mean() * POSTWAR_NORM      # rescale the index onto a share basis

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot(ls_pct.index, ls_pct.values, color=sl.PALETTE[0], lw=2.2)
ax.axhline(POSTWAR_NORM, color=sl.PALETTE[1], lw=1.4, ls=(0, (5, 3)))
ax.text(ls_pct.index.min() + 1, POSTWAR_NORM + 0.4,
        "1947-2000 average, %.1f%%" % POSTWAR_NORM, color=sl.PALETTE[1], fontsize=9.5)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_ylabel("Labour share of nonfarm business output")
ax.set_title("Labour's share of what it produces")
ax.annotate("%.1f%% in %d" % (ls_pct.iloc[-1], ls_pct.index[-1]),
            xy=(ls_pct.index[-1], ls_pct.iloc[-1]), xytext=(-10, -24),
            textcoords="offset points", ha="right", color=sl.INK["secondary"], fontsize=10)
sl.save_fig(fig, "fig1_labour_share", DIRS)
plt.show()
print("rescaled labour share: %.1f%% now against a %.1f%% postwar average (%.1f%% lower)"
      % (ls_pct.iloc[-1], POSTWAR_NORM, 100 * (1 - ls_pct.iloc[-1] / POSTWAR_NORM)))

# %% [markdown]
# ## Figure 2 - The proprietors' income problem
#
# Three constructions of the same concept.
#
# * **Narrow.** Employee compensation over GDP. Counts none of the
#   self-employed's earnings as labour income, which understates the level.
# * **Broad.** Compensation plus all proprietors' income over GDP. Counts every
#   dollar the self-employed earn as a return to their labour, which overstates it.
# * **Proportional.** Gollin's adjustment: compensation over GDP excluding
#   proprietors' income. Assumes the self-employed split their earnings between
#   labour and capital the way the rest of the economy does.
#
# If all three fall, the finding is robust to the assumption. If they disagree,
# the article has to say which one it is using and why.

# %%
common = COE.index.intersection(PI.index).intersection(GDPN.index)
coe, pi, gdp = COE.loc[common], PI.loc[common], GDPN.loc[common]

shares = pd.DataFrame({
    "Narrow (employees only)": coe / gdp * 100,
    "Broad (all proprietors' income counted)": (coe + pi) / gdp * 100,
    "Proportional (Gollin adjustment)": coe / (gdp - pi) * 100,
}).dropna()

fig, ax = plt.subplots(figsize=(9.5, 5.4))
for (name, color) in zip(shares.columns, sl.PALETTE[:3]):
    ax.plot(shares.index, shares[name].values, color=color, lw=2.0, label=name)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_ylabel("Share of GDP")
ax.set_title("Labour's share, computed three ways")
ax.legend(loc="lower left")
sl.save_fig(fig, "fig2_proprietors_problem", DIRS)
plt.show()

peaks = {c: {"peak_year": int(shares[c].idxmax()), "peak": float(shares[c].max()),
             "latest": float(shares[c].iloc[-1]),
             "fall_from_peak_pct": float(100 * (1 - shares[c].iloc[-1] / shares[c].max()))}
         for c in shares.columns}
print(pd.DataFrame(peaks).T.round(2).to_string())

# %% [markdown]
# ## Figure 3 - Where the share went
#
# Labour's share and corporate profits as shares of the same denominator, so one
# axis serves both. This is the notes' Figure 9.2, which the book draws with two
# vertical scales. One scale is better: it makes the sizes comparable and removes
# the temptation to align two unrelated series by eye.

# %%
cp_share = (CP / GDPN * 100).dropna()
lab = shares["Proportional (Gollin adjustment)"]
st = max(lab.index.min(), cp_share.index.min())
lab, cp_share = lab[lab.index >= st], cp_share[cp_share.index >= st]

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot(lab.index, lab.values, color=sl.PALETTE[0], lw=2.2, label="Labour share")
ax.plot(cp_share.index, cp_share.values, color=sl.PALETTE[1], lw=2.2, label="Corporate profits")
sl.label_last(ax, lab, "Labour", sl.PALETTE[0])
sl.label_last(ax, cp_share, "Profits", sl.PALETTE[1])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_ylabel("Share of GDP")
ax.set_xlim(st, lab.index.max() + 7)
ax.set_title("Labour and profits, on one scale")
ax.legend(loc="center left")
sl.save_fig(fig, "fig3_labour_and_profits", DIRS)
plt.show()
print("labour %.1f%% -> %.1f%% | profits %.1f%% -> %.1f%%  (%d to %d)"
      % (lab.iloc[0], lab.iloc[-1], cp_share.iloc[0], cp_share.iloc[-1], st, lab.index[-1]))

# %% [markdown]
# ## Figure 4 - Is it global?
#
# Karabarbounis and Neiman argue the decline shows up within most countries. The
# Penn World Table publishes a comparable labour share for each. Each identifier
# is title-verified, so a country that does not resolve is reported rather than
# silently mislabelled.

# %%
COUNTRIES = {"United States": "LABSHPUSA156NRUG", "Germany": "LABSHPDEA156NRUG",
             "Japan": "LABSHPJPA156NRUG", "United Kingdom": "LABSHPGBA156NRUG"}
def trim_flat_prefix(s):
    """
    The Penn World Table carries a country's earliest observed value backwards
    as a constant, so Germany appears to hold one exact share for thirty years.
    A run of identical leading values is padding, not observation, and plotting
    it invents three flat decades of history.
    """
    v = s.values
    i = 0
    while i + 1 < len(v) and v[i + 1] == v[0]:
        i += 1
    return s.iloc[i:] if i > 0 else s

intl, padding = {}, {}
for name, sid in COUNTRIES.items():
    try:
        _, _, s = resolve([sid], name, ["labour compensation"])
        s = s.dropna() * 100
        raw_start = int(s.index[0])
        s = trim_flat_prefix(s)
        intl[name] = s
        padding[name] = {"raw_start": raw_start, "real_start": int(s.index[0]),
                         "padded_years": int(s.index[0]) - raw_start}
        if padding[name]["padded_years"]:
            print("     %s: dropped %d padded years; real data starts %d"
                  % (name, padding[name]["padded_years"], padding[name]["real_start"]))
    except Exception as e:
        print("  %-26s unavailable (%s)" % (name, str(e)[:70]))

if intl:
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    for (name, s), color in zip(intl.items(), sl.PALETTE[:4]):
        ax.plot(s.index, s.values, color=color, lw=2.0, label=name)
        sl.label_last(ax, s, name, color, fontsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
    ax.set_ylabel("Labour compensation as a share of GDP")
    ax.set_xlim(min(s.index.min() for s in intl.values()),
                max(s.index.max() for s in intl.values()) + 11)
    ax.set_title("Labour's share in four rich economies")
    ax.legend(loc="lower left")
    sl.save_fig(fig, "fig4_international", DIRS)
    plt.show()
    for name, s in intl.items():
        print("  %-16s %.1f%% (%d) -> %.1f%% (%d) | peak %.1f%% in %d"
              % (name, s.iloc[0], s.index[0], s.iloc[-1], s.index[-1],
                 s.max(), int(s.idxmax())))
else:
    print("No international series resolved; skipping Figure 4.")

# %% [markdown]
# ## Figure 5 - Testing the proposed mechanism
#
# Karabarbounis and Neiman do not merely report the decline; they explain it. In
# their account the cause is the falling relative price of investment goods,
# which makes capital cheaper than labour and, when the two substitute easily,
# shifts income toward capital.
#
# Idea 1 measured that relative price directly. Plotting it against the labour
# share tests their mechanism on this data. A downward-sloping relation is what
# the theory predicts. It is a correlation between two trending series, so it
# cannot confirm the mechanism, but a flat or upward-sloping relation would be
# awkward for it.

# %%
prices = sl.bea_nipa_table("T50304", BEA, frequency="A", cache_dir=DIRS["data"])
eq_price = sl.pick_lines(prices, {"Equipment": 9, "Structures": 3})["Equipment"].dropna()
consumer = sl.to_annual(sl.fred_series("CPIAUCSL", FRED, cache_dir=DIRS["data"]))
rel_price = (eq_price / consumer.reindex(eq_price.index)).dropna()
rel_price = rel_price / rel_price.iloc[0] * 100

pair = pd.DataFrame({"rel_price": rel_price, "labour_share": lab}).dropna()
x, y = np.log(pair["rel_price"].values), pair["labour_share"].values
slope, intercept = np.polyfit(x, y, 1)
r = float(np.corrcoef(x, y)[0, 1])

fig, ax = plt.subplots(figsize=(8.6, 5.6))
ax.plot(x, y, color=sl.INK["axis"], lw=1.0, zorder=1)
ax.scatter(x, y, s=28, color=sl.PALETTE[0], zorder=2, linewidths=0.8,
           edgecolors=sl.INK["surface"])
xs = np.linspace(x.min(), x.max(), 40)
ax.plot(xs, intercept + slope * xs, color=sl.PALETTE[1], lw=1.8, ls=(0, (5, 3)), zorder=3)
for yr in [pair.index.min(), 1980, 2000, int(pair.index.max())]:
    if yr in pair.index:
        i = list(pair.index).index(yr)
        ax.annotate(str(yr), (x[i], y[i]), xytext=(7, -10), textcoords="offset points",
                    fontsize=9, color=sl.INK["secondary"])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_xlabel("log relative price of equipment (against consumer prices)")
ax.set_ylabel("Labour share of GDP")
ax.set_title("The mechanism Karabarbounis and Neiman propose")
ax.annotate("slope %.1f   r = %.2f" % (slope, r), xy=(0.03, 0.06), xycoords="axes fraction",
            color=sl.INK["secondary"], fontsize=10)
ax.grid(axis="x")
sl.save_fig(fig, "fig5_kn_mechanism", DIRS)
plt.show()

# %% [markdown]
# ## 2. Bank the numbers

# %%
payload = {
    "stacklib_version": sl.__version__,
    "postwar_norm_pct": POSTWAR_NORM,
    "series_used": {"labour_share": ls_id, "compensation": coe_id, "proprietors": pi_id,
                    "gdp": gdp_id, "corporate_profits": cp_id,
                    "international": {k: v for k, v in COUNTRIES.items() if k in intl}},
    "series_titles": {"labour_share": ls_title, "compensation": coe_title,
                      "proprietors": pi_title, "gdp": gdp_title, "corporate_profits": cp_title},
    "official_labour_share_rescaled_latest": float(ls_pct.iloc[-1]),
    "official_decline_vs_norm_pct": float(100 * (1 - ls_pct.iloc[-1] / POSTWAR_NORM)),
    "three_constructions": peaks,
    "labour_vs_profits": {"start_year": int(st),
                          "labour_start": float(lab.iloc[0]), "labour_end": float(lab.iloc[-1]),
                          "profits_start": float(cp_share.iloc[0]),
                          "profits_end": float(cp_share.iloc[-1])},
    "international": {k: {"first_year": int(s.index[0]), "first": float(s.iloc[0]),
                          "last_year": int(s.index[-1]), "last": float(s.iloc[-1]),
                          "peak_year": int(s.idxmax()), "peak": float(s.max()),
                          "fall_from_peak_points": float(s.max() - s.iloc[-1])}
                      for k, s in intl.items()},
    "international_padding_note": padding,
    "kn_mechanism": {"slope": float(slope), "r": r, "n": int(len(x)),
                     "years": [int(pair.index.min()), int(pair.index.max())]},
    "idea5_implied_decline_pct": 14.0,
}
sl.write_findings(payload, DIRS)
shares.to_csv(pathlib.Path(DIRS["findings"]) / "labour_share_three_ways.csv")
print("\nDone. Figures in figures/, numbers in findings/.")

# %% [markdown]
# ## Caveats to carry into the prose
#
# 1. **GDP is the wrong denominator, strictly.** It includes depreciation and
#    taxes on production, neither of which is available to pay anyone. Net
#    domestic product or business-sector value added would be cleaner and moves
#    the level by several points. The trend is much less affected than the level.
# 2. **The proprietors' assumption is doing real work.** Figure 2 exists to show
#    how much. Quote whichever construction the article uses, by name.
# 3. **The BLS index is rescaled, not a published percentage.** Figure 1 puts the
#    index onto a share basis using its own pre-2000 mean and the 64.3 percent
#    figure from the notes. The shape is the series; the level is a construction.
# 4. **Corporate profits are pre-tax and include foreign earnings.** They are not
#    the mirror image of the domestic labour share, so the two lines in Figure 3
#    do not have to add to anything.
# 5. **Figure 5 is a correlation between two trending series.** Idea 3 showed how
#    little that is worth on its own. It can embarrass the mechanism but not
#    confirm it.
# 6. **Rognlie's objection is not tested here.** He argues the rise in capital's
#    share is concentrated in housing rather than in productive capital, which
#    would sever the link to automation entirely. Testing it needs a housing
#    split this notebook does not attempt.
#
# **Send back:** the five PNGs, the resolution printout with the verified titles,
# the three-construction table, the international levels, and
# `findings/headline_numbers.json`. The three-construction table is the one that
# decides how strongly the article can put this.
