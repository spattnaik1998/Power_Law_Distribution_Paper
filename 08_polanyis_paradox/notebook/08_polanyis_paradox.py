# %% [markdown]
# # Idea 8 - Polanyi's Paradox and the Moving Frontier
#
# **The claim (Machines, Platforms, Crowds, ch. 1-3).** We know more than we can
# tell. A large share of human competence is tacit: we execute it fluently and
# cannot state the rules. Autor's economic formulation, which the notes quote
# twice, is that substituting computers for people is "bounded because there are
# many tasks that people understand tacitly and accomplish effortlessly but for
# which neither computer programmers nor anyone else can enunciate the explicit
# rules or procedures."
#
# The book's argument is that machine learning dissolves the bound by changing
# what has to be specified. Instead of the rules, you supply the goal and the
# examples. The notes call this "the hinge on which the first five chapters
# turn": the boundary of automation is no longer the boundary of what humans can
# explain.
#
# **What that predicts, and how to test it.** Polanyi's paradox and Moravec's
# paradox together make a specific prediction about which jobs disappear. Work
# whose rules can be written down should be automated first. Work that is tacit,
# perceptual or manual should be safe, because nobody can specify it. If the book
# is right that the bound is dissolving, the second category should stop being
# safe.
#
# So the test is the composition of American employment, sorted by how
# codifiable the work is:
#
# 1. Does employment fall where the rules can be written down?
# 2. Does it hold up where the work is tacit, as Polanyi predicts?
# 3. Has the frontier moved, comparing the years before and after deep learning
#    became practical?
# 4. Do wages tell the same story as headcount, or a different one?
# 5. Which occupations actually shrank, named rather than aggregated?
#
# **The judgement this notebook makes openly.** Testing Polanyi needs a measure
# of how tacit each occupation is. The standard source is O*NET's task ratings,
# whose bulk files require guessing version-specific download URLs, which is the
# practice that produced a mislabelled figure in Idea 5. Instead this notebook
# writes out its own classification of occupation groups into Autor's routine and
# non-routine, cognitive and manual quadrants, prints it in full, and invites
# disagreement. It is a judgement, disclosed, in the same way Idea 6 disclosed the
# proprietors' income assumption. Anyone who disputes a cell can move it and
# rerun.
#
# **Data.** Census ACS occupation tables, retrieved with variable labels from the
# API's own metadata endpoint rather than by assuming variable numbers.

# %%
import sys, pathlib, warnings, importlib, json, re
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
assert sl.__version__ >= "0.8.0", "needs stacklib 0.8.0 for census_group_labels"

DIRS = sl.dirs_for("08_polanyis_paradox")
KEYS = sl.load_keys()
sl.apply_theme()
CENSUS = sl.require(KEYS, "CENSUS")

ACS = "https://api.census.gov/data/%d/acs/acs1"
YEARS = [y for y in range(2010, 2024) if y != 2020]     # no ACS 1-year for 2020
EARLY, LATE = (2010, 2014), (2019, 2023)                # before and after deep learning

# %% [markdown]
# ## 1. Read the occupation tree from the source
#
# Census labels encode a hierarchy with "!!" separators. Printing that tree is
# how we choose a level of detail deliberately instead of guessing which variable
# numbers mean what.

# %%
GROUP = "C24010"          # sex by occupation, collapsed; B24010 is the detailed version
labels = sl.census_group_labels(ACS % 2023, GROUP)
print()
for d in sorted(labels["depth"].unique()):
    n = (labels["depth"] == d).sum()
    sample = labels[labels["depth"] == d]["leaf"].head(3).tolist()
    print("  depth %d: %3d variables   e.g. %s" % (d, n, sample))

# %%
# Depth 3 is "Estimate!!Total!!Male/Female"; depth 4 is the major occupation
# groups within sex; depth 5 is the minor groups. We want minor groups summed
# across sex, which is the finest level this table offers.
DEPTH = 5
minor = labels[labels["depth"] == DEPTH].copy()
minor["group"] = minor["leaf"]
print("%d variables at depth %d, covering %d distinct occupation groups"
      % (len(minor), DEPTH, minor["group"].nunique()))
print()
for g in sorted(minor["group"].unique()):
    print("   -", g)

# %% [markdown]
# ## 2. The classification, written out
#
# Autor's two-by-two. **Routine** means the task can be stated as a procedure,
# which is what Polanyi says most human competence cannot be. **Cognitive** and
# **manual** separate desk work from physical work, which is the axis Moravec's
# paradox runs along.
#
# The predictions being tested:
#
# * Routine cognitive should be automated first: the rules are writable.
# * Routine manual should follow, since industrial machinery predates computing.
# * Non-routine manual is Moravec's protected zone: easy for a toddler,
#   historically impossible for a machine.
# * Non-routine cognitive is Polanyi's protected zone: judgement nobody can spell out.
#
# The book's claim is that machine learning is now eating into the two protected
# zones. Disagree with any assignment below by editing the dictionary and
# rerunning; that is the point of printing it.

# %%
QUADRANT = {
    # Routine cognitive: procedural desk work, rules writable
    "Office and administrative support occupations": "Routine cognitive",
    "Sales and related occupations": "Routine cognitive",
    "Business and financial operations occupations": "Routine cognitive",
    # Routine manual: repetitive physical work in a controlled setting
    "Production occupations": "Routine manual",
    "Transportation and material moving occupations": "Routine manual",
    "Construction and extraction occupations": "Routine manual",
    "Farming, fishing, and forestry occupations": "Routine manual",
    # Non-routine manual: Moravec's zone, perception and dexterity in the wild
    "Healthcare support occupations": "Non-routine manual",
    "Building and grounds cleaning and maintenance occupations": "Non-routine manual",
    "Food preparation and serving related occupations": "Non-routine manual",
    "Personal care and service occupations": "Non-routine manual",
    "Installation, maintenance, and repair occupations": "Non-routine manual",
    "Protective service occupations": "Non-routine manual",
    # Non-routine cognitive: Polanyi's zone, judgement and persuasion
    "Management occupations": "Non-routine cognitive",
    "Computer and mathematical occupations": "Non-routine cognitive",
    "Architecture and engineering occupations": "Non-routine cognitive",
    "Life, physical, and social science occupations": "Non-routine cognitive",
    "Community and social service occupations": "Non-routine cognitive",
    "Legal occupations": "Non-routine cognitive",
    "Educational instruction and library occupations": "Non-routine cognitive",
    "Arts, design, entertainment, sports, and media occupations": "Non-routine cognitive",
    "Health diagnosing and treating practitioners and other technical occupations":
        "Non-routine cognitive",
    "Healthcare practitioners and technical occupations": "Non-routine cognitive",
}
ORDER = ["Routine cognitive", "Routine manual", "Non-routine manual", "Non-routine cognitive"]

observed = set(minor["group"].unique())
unmapped = sorted(observed - set(QUADRANT))
unused = sorted(set(QUADRANT) - observed)
print("occupation groups in the data but NOT classified (%d):" % len(unmapped))
for g in unmapped:
    print("   -", g)
print("\nclassifications with no matching group in the data (%d):" % len(unused))
for g in unused:
    print("   -", g)
if unmapped:
    raise AssertionError(
        "Every occupation group must be classified or the shares will not sum to one. "
        "Add the groups listed above to QUADRANT and rerun.")

# %% [markdown]
# ## 3. Pull employment by occupation
#
# One call per year. Variables are selected by the labels fetched above, never by
# assumed variable numbers.

# %%
var_list = minor["name"].tolist()
def fetch_year(year):
    got = sl.census_timeseries(ACS % year, {"get": "group(%s)" % GROUP, "for": "us:1"},
                               CENSUS, cache_dir=DIRS["data"], tag="%s_%d" % (GROUP.lower(), year))
    row = got.iloc[0]
    out = {}
    for _, r in minor.iterrows():
        if r["name"] in got.columns:
            out.setdefault(r["group"], 0.0)
            out[r["group"]] += float(row[r["name"]])
    return out

emp = {}
for y in YEARS:
    try:
        emp[y] = fetch_year(y)
    except Exception as e:
        print("  %d unavailable (%s)" % (y, str(e)[:70]))

E = pd.DataFrame(emp).T.sort_index()
E.index = E.index.astype(int)
print("\nemployment by occupation group, millions:")
print((E[[c for c in E.columns[:4]]] / 1e6).round(2).to_string())

total = E.sum(axis=1)
print("\ntotal employed, millions: %.1f (%d) -> %.1f (%d)"
      % (total.iloc[0]/1e6, total.index[0], total.iloc[-1]/1e6, total.index[-1]))

# %% [markdown]
# ## Figure 1 - Employment by task type
#
# Shares of total employment, so the four quadrants sum to one and the question
# is composition rather than the business cycle.

# %%
Q = pd.DataFrame({q: E[[c for c in E.columns if QUADRANT[c] == q]].sum(axis=1)
                  for q in ORDER})
Qs = Q.div(Q.sum(axis=1), axis=0) * 100
assert abs(Qs.sum(axis=1) - 100).max() < 1e-6, "shares must sum to 100"

# Reindex over the full calendar range so 2020 becomes NaN and matplotlib
# breaks the line there. Drawn straight from YEARS the chart joins 2019 to 2021
# with a segment through the pandemic, inventing a trajectory nobody measured.
Qp = Qs.reindex(range(min(YEARS), max(YEARS) + 1))

fig, ax = plt.subplots(figsize=(7.6, 4.2))
for q, color in zip(ORDER, sl.PALETTE[:4]):
    ax.plot(Qp.index, Qp[q].values, color=color, lw=2.0)

# Direct labels instead of a legend, nudged apart where the three lower lines
# converge within a point of each other in 2023.
NUDGE = {"Non-routine cognitive": 0.0, "Routine cognitive": 0.0,
         "Non-routine manual": 0.55, "Routine manual": -0.55}
for q, color in zip(ORDER, sl.PALETTE[:4]):
    end = Qp[q].dropna()
    ax.text(end.index[-1] + 0.25, end.iloc[-1] + NUDGE.get(q, 0.0), q,
            color=color, fontsize=9.5, va="center", ha="left",
            fontweight="semibold", clip_on=False)

ax.axvspan(2019.15, 2020.85, color=sl.INK["grid"], alpha=0.55, lw=0, zorder=0)
ax.text(2020, Qp.max().max() + 2.4, "no 2020\nACS release", color=sl.INK["muted"],
        fontsize=8, ha="center", va="top", linespacing=1.25)

ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%.0f%%" % v))
ax.set_ylabel("Share of employment")
ax.set_xlim(Qp.index.min() - 0.4, Qp.index.max() + 3.6)
ax.set_ylim(Qp.min().min() - 2.1, Qp.max().max() + 2.9)
ax.set_xticks(range(min(YEARS), max(YEARS) + 1, 2))
ax.set_title("American employment by how codifiable the work is")
sl.save_fig(fig, "fig1_quadrant_shares", DIRS)
plt.show()
print(Qs.round(2).to_string())

# %% [markdown]
# ## Figure 2 - Did the frontier move?
#
# Average annual change in each quadrant's employment share, comparing the early
# window with the late one. Polanyi's prediction is that the non-routine bars
# stay flat or positive. The book's claim is that they turn down in the later
# period.

# %%
def window_rate(df, lo, hi):
    w = df[(df.index >= lo) & (df.index <= hi)]
    return (w.iloc[-1] - w.iloc[0]) / (w.index[-1] - w.index[0])

early = window_rate(Qs, *EARLY)
late = window_rate(Qs, *LATE)
comp = pd.DataFrame({"%d-%d" % EARLY: early, "%d-%d" % LATE: late}).loc[ORDER]

fig, ax = plt.subplots(figsize=(9.4, 5.2))
idx = np.arange(len(ORDER)); w = 0.36
ax.bar(idx - w/2, comp.iloc[:, 0].values, width=w, color=sl.PALETTE[0],
       edgecolor=sl.INK["surface"], linewidth=1.2, label=comp.columns[0])
ax.bar(idx + w/2, comp.iloc[:, 1].values, width=w, color=sl.PALETTE[1],
       edgecolor=sl.INK["surface"], linewidth=1.2, label=comp.columns[1])
ax.axhline(0, color=sl.INK["axis"], lw=1.0)
ax.set_xticks(idx); ax.set_xticklabels([q.replace(" ", "\n", 1) for q in ORDER], fontsize=9)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%+.2f" % v))
ax.set_ylabel("Change in employment share, points per year")
ax.set_title("Where the frontier was moving, before and after")
ax.legend(loc="best")
sl.save_fig(fig, "fig2_frontier_shift", DIRS)
plt.show()
print(comp.round(3).to_string())

# %% [markdown]
# ## Figure 3 - Which occupations actually shrank
#
# The quadrants are an interpretation. The occupation groups underneath them are
# data. This ranks them by change in employment share so the reader can check the
# classification against the outcome.

# %%
share = E.div(E.sum(axis=1), axis=0) * 100
chg = (share.loc[share.index.max()] - share.loc[share.index.min()]).sort_values()
colors = [sl.PALETTE[ORDER.index(QUADRANT[g]) % 4] for g in chg.index]

fig, ax = plt.subplots(figsize=(9.4, 7.4))
ax.barh(range(len(chg)), chg.values, color=colors,
        edgecolor=sl.INK["surface"], linewidth=1.0)
ax.set_yticks(range(len(chg)))
ax.set_yticklabels([g.replace(" occupations", "") for g in chg.index], fontsize=8.5)
ax.axvline(0, color=sl.INK["axis"], lw=1.0)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "%+.1f" % v))
ax.set_xlabel("Change in employment share, %d to %d (points)"
              % (share.index.min(), share.index.max()))
ax.set_title("Which kinds of work grew and shrank")
ax.grid(axis="x")
handles = [plt.Line2D([0], [0], color=sl.PALETTE[i], lw=6) for i in range(4)]
ax.legend(handles, ORDER, loc="lower right", fontsize=8.5)
sl.save_fig(fig, "fig3_occupation_ranking", DIRS)
plt.show()
print(chg.round(3).to_string())

# %% [markdown]
# ## Figure 4 - Headcount against pay
#
# Employment share is one signal and it is ambiguous: a shrinking occupation may
# be automated or may simply be unfashionable. Median earnings are a second
# signal. Work being replaced should lose both; work being complemented by
# machines should shed workers while paying the survivors more.

# %%
EARN_GROUP = "B24011"      # sex by occupation and median earnings
earn = {}
try:
    elabels = sl.census_group_labels(ACS % 2023, EARN_GROUP)
    ekeep = elabels[(elabels["depth"] == 3) & (elabels["leaf"].isin(QUADRANT))]
    print("matched %d earnings variables to classified occupation groups" % len(ekeep))
    for y in [share.index.min(), share.index.max()]:
        got = sl.census_timeseries(ACS % y, {"get": "group(%s)" % EARN_GROUP, "for": "us:1"},
                                   CENSUS, cache_dir=DIRS["data"],
                                   tag="%s_%d" % (EARN_GROUP.lower(), y))
        row = got.iloc[0]
        earn[y] = {r["leaf"]: float(row[r["name"]])
                   for _, r in ekeep.iterrows()
                   if r["name"] in got.columns and float(row[r["name"]]) > 0}
except Exception as e:
    print("earnings table unavailable (%s)" % str(e)[:100])

if len(earn) == 2:
    y0, y1 = min(earn), max(earn)
    common = sorted(set(earn[y0]) & set(earn[y1]) & set(chg.index))
    ew = pd.DataFrame({"earn_change_pct": [earn[y1][g] / earn[y0][g] * 100 - 100 for g in common],
                       "share_change": [chg[g] for g in common]}, index=common)
    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    for q, color in zip(ORDER, sl.PALETTE[:4]):
        sub = ew[[QUADRANT[g] == q for g in ew.index]]
        ax.scatter(sub["share_change"], sub["earn_change_pct"], s=48, color=color,
                   edgecolors=sl.INK["surface"], linewidths=0.9, label=q, zorder=2)
    ax.axhline(0, color=sl.INK["axis"], lw=0.9, zorder=0)
    ax.axvline(0, color=sl.INK["axis"], lw=0.9, zorder=0)
    ax.set_xlabel("Change in employment share, points")
    ax.set_ylabel("Change in nominal median earnings, %d to %d (%%)" % (y0, y1))
    ax.set_title("Losing workers, or losing wages?")
    # NOTE: nominal. Consumer prices rose about 40 per cent across this window,
    # so every occupation gains and the chart mostly shows inflation. The
    # technical summary redraws this in real terms, where the relationship
    # inverts: the occupations that shed the most workers got the largest real
    # pay rises. Deflate before reading anything into this figure.
    ax.legend(loc="best", fontsize=8.5)
    ax.grid(axis="x")
    sl.save_fig(fig, "fig4_headcount_vs_pay", DIRS)
    plt.show()
    print(ew.round(2).to_string())
else:
    ew = None
    print("Skipping Figure 4; earnings data did not resolve for both endpoints.")

# %% [markdown]
# ## Figure 5 - The benchmark
#
# Employment composition shifts for many reasons that have nothing to do with
# automation: ageing, trade, the housing cycle, the pandemic. Before reading a
# task story into Figure 2, ask how much of the movement a task classification
# explains at all.
#
# The test: shuffle the quadrant labels across occupation groups at random, many
# times, and recompute the spread between quadrant trends. If the real spread
# sits inside the distribution of random spreads, the classification is carrying
# no information and the article should say so.

# %%
rng = np.random.default_rng(11)
real_spread = float(late.max() - late.min())
groups = list(chg.index)
sizes = share.loc[share.index.max()]

null_spreads = []
for _ in range(2000):
    perm = rng.permutation(groups)
    assign = {g: QUADRANT[p] for g, p in zip(groups, perm)}
    Qp = pd.DataFrame({q: E[[c for c in E.columns if assign[c] == q]].sum(axis=1)
                       for q in ORDER}).fillna(0.0)
    Qps = Qp.div(Qp.sum(axis=1), axis=0) * 100
    r = window_rate(Qps, *LATE)
    null_spreads.append(float(r.max() - r.min()))
null_spreads = np.array(null_spreads)
pval = float((null_spreads >= real_spread).mean())

fig, ax = plt.subplots(figsize=(9.0, 5.0))
ax.hist(null_spreads, bins=40, color=sl.PALETTE[2], edgecolor=sl.INK["surface"], linewidth=0.8)
ax.axvline(real_spread, color=sl.PALETTE[1], lw=2.4)
ax.annotate("the real classification\n%.3f points per year" % real_spread,
            xy=(real_spread, ax.get_ylim()[1]*0.82), xytext=(12, 0),
            textcoords="offset points", color=sl.PALETTE[1], fontsize=9.5, va="center")
ax.set_xlabel("Spread between quadrant trends, %d-%d" % LATE)
ax.set_ylabel("Random classifications")
ax.set_title("Does the task classification explain anything?")
sl.save_fig(fig, "fig5_permutation_benchmark", DIRS)
plt.show()
print("real spread %.4f points/year; %d random classifications; p = %.3f"
      % (real_spread, len(null_spreads), pval))
print("VERDICT:", "the classification carries information" if pval < 0.05
      else "the classification is NOT distinguishable from random labels")

# %% [markdown]
# ## 4. Bank the numbers

# %%
payload = {
    "stacklib_version": sl.__version__,
    "acs_group": GROUP, "earnings_group": EARN_GROUP,
    "years": [int(y) for y in Qs.index],
    "quadrant_map": QUADRANT,
    "quadrant_shares_pct": Qs.round(3).to_dict(orient="index"),
    "quadrant_trend_points_per_year": {"early_window": list(EARLY), "late_window": list(LATE),
                                       "early": early.round(4).to_dict(),
                                       "late": late.round(4).to_dict()},
    "occupation_share_change_points": chg.round(3).to_dict(),
    "headcount_vs_pay": (None if ew is None else ew.round(3).to_dict(orient="index")),
    "permutation_test": {"real_spread": real_spread, "draws": len(null_spreads),
                         "p_value": pval,
                         "null_mean": float(null_spreads.mean()),
                         "null_95th": float(np.percentile(null_spreads, 95))},
}
sl.write_findings(payload, DIRS)
Qs.to_csv(pathlib.Path(DIRS["findings"]) / "quadrant_shares.csv")
chg.to_frame("share_change_points").to_csv(
    pathlib.Path(DIRS["findings"]) / "occupation_share_change.csv")
print("\nDone. Figures in figures/, numbers in findings/.")

# %% [markdown]
# ## Caveats to carry into the prose
#
# 1. **The classification is a judgement, not a measurement.** Every assignment
#    in QUADRANT was made by hand. The permutation test in Figure 5 is the check
#    on whether it carries information; quote that verdict alongside any claim
#    built on the quadrants.
# 2. **Occupations are not tasks.** Autor's own point is that automation replaces
#    tasks within jobs, not whole jobs. An occupation can keep its headcount while
#    most of its work changes, and this data cannot see that at all.
# 3. **Fourteen years is short and includes a pandemic.** The late window covers
#    2019 to 2023, which contains the largest labour-market disruption in eighty
#    years. Attributing its shape to machine learning requires an argument this
#    notebook does not supply.
# 4. **Nominal earnings.** Figure 4 compares nominal medians across years, so
#    every point is lifted by inflation. Only the relative positions mean anything.
# 5. **Composition, not level.** Shares can fall because one category shrinks or
#    because others grow. Check the underlying counts before saying a kind of
#    work is disappearing.
#
# **Send back:** the five PNGs, the printed occupation tree, the unmapped-groups
# check, the quadrant share table, the early-against-late comparison, the ranked
# occupation table, and `findings/headline_numbers.json`. The permutation verdict
# in Figure 5 decides how much of this the article can use.
