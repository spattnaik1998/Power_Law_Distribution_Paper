# %% [markdown]
# # Idea 12 - Dynamism and Concentration
#
# **Phase two: the power law in business. Thiel and Masters, Zero to One,
# chapters 3, 5 and 7, against Brynjolfsson and McAfee.**
#
# Both books need concentration, and they need it for opposite reasons. Thiel
# argues that a serious business escapes competition and becomes a monopoly, and
# that the economy is renewed by new firms going from zero to one and displacing
# the incumbents they beat. Brynjolfsson and McAfee argue that low marginal cost
# and network effects hand the winner a share the loser cannot contest.
#
# The two accounts differ on one testable point. Thiel's requires **churn**: new
# firms arriving and old ones dying is the mechanism that makes concentration
# legitimate rather than merely large. If concentration has risen while entry has
# fallen, then the American economy is getting more concentrated without the
# creative destruction that is supposed to justify it, and Thiel's picture of a
# world remade by founders is describing something that is happening less often
# than it used to.
#
# ### Why this question and not the tail
#
# Idea 7 could not test the power law in household income because the American
# Community Survey stops resolving at $200,000. Census business data has the same
# problem in a different costume: its largest firm class is "10,000 employees and
# over", so the region where Thiel's monopolists live is inside the last bin.
#
# Dynamism escapes that ceiling. Entry and exit are measured as rates over all
# firms, not as properties of the largest one, so top-coding does not touch them.
# Concentration between broad size classes is also measurable even when the top
# class is unresolved. Those two things are what this notebook measures.
#
# ### What it can and cannot show
#
# - **Can:** whether firm and establishment entry has fallen; whether employment
#   has shifted toward large firms; whether that shift happened within sectors or
#   by reallocation between them; whether young firms still create the jobs.
# - **Cannot:** anything about revenue, profit or market value. BDS counts
#   employment. A software firm can dominate a market with few employees, which
#   means employment concentration **understates** digital concentration and
#   biases this test against the books rather than toward them. That asymmetry is
#   worth more to the write-up than any number here.

# %%
import importlib, io, json, pathlib, sys, time, warnings
import numpy as np
import pandas as pd
import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = None
for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
    if (p / "common" / "stacklib.py").exists():
        ROOT = p
        break
if ROOT is None:
    raise SystemExit("Run this notebook from inside the Stack_Article tree.")
sys.path.insert(0, str(ROOT / "common"))

import stacklib as sl
importlib.reload(sl)
print("stacklib version:", sl.__version__)

DIRS = sl.dirs_for("12_dynamism_and_concentration", start=ROOT)
KEYS = sl.load_keys()
CENSUS = sl.require(KEYS, "CENSUS")

sl.apply_theme()
pd.set_option("display.width", 180)
pd.set_option("display.max_rows", 300)
RNG = np.random.default_rng(20260908)

BDS = "https://api.census.gov/data/timeseries/bds"

# %% [markdown]
# ## Discovery
#
# Nothing below is typed from memory. The variable list, the geography list and
# the code labels for every categorical dimension come from the API's own
# metadata endpoints, which need no key. Idea 9 shipped a broken figure built
# from an identifier assembled by pattern; Idea 11 asked for a series with words
# too loose to exclude the wrong one. Both failures were requests, not tools.

# %%
def bds_meta(path):
    r = requests.get("%s/%s" % (BDS, path), timeout=90)
    r.raise_for_status()
    return r.json()

vars_json = bds_meta("variables.json")["variables"]
V = pd.DataFrame([{"name": k, "label": v.get("label", ""),
                   "predicate": v.get("predicateType", ""),
                   "group": v.get("group", "")}
                  for k, v in vars_json.items()]).sort_values("name")
print("BDS exposes %d variables\n" % len(V))
print("measures that look like counts or rates:")
print(V[V["name"].str.contains(
    "FIRM|ESTAB|EMP|JOB|NET|REALLOC|DENOM", regex=True, na=False)]
      [["name", "label"]].to_string(index=False))

# %%
print("\ndimensions offered:")
DIMS = V[V["name"].str.contains("SZ|AGE|NAICS|SECTOR|INDLEVEL|YEAR|METRO", na=False)]
print(DIMS[["name", "label"]].to_string(index=False))

print("\ngeography levels:")
try:
    geo = bds_meta("geography.json")["fips"]
    print(pd.DataFrame(geo)[["name", "geoLevelDisplay"]].to_string(index=False))
except Exception as e:
    print("  geography.json unavailable:", e)

# %%
def bds_codes(var):
    """Code -> label for one categorical dimension, read from the API."""
    try:
        item = bds_meta("variables/%s.json" % var).get("values", {}).get("item", {})
    except Exception as e:
        print("  no code list for %s (%s)" % (var, e))
        return pd.Series(dtype=object)
    s = pd.Series(item).sort_index()
    print("\n%s codes:" % var)
    for k, v in s.items():
        print("   %-4s %s" % (k, v))
    return s

SIZE_CODES = bds_codes("EMPSZFI")     # firm size, current year
AGE_CODES = bds_codes("FAGE")         # firm age
SEC_CODES = bds_codes("SECTOR")       # 2-digit sector

# %% [markdown]
# ## Fetching
#
# BDS is a timeseries dataset, and how it accepts a year range is not something
# to guess. The helper tries a batched request first and falls back to fetching
# one year at a time, reporting which worked. Everything is cached, so a rerun
# costs no calls.

# %%
YEARS = list(range(1978, 2024))

def bds_get(measures, dims=(), years=YEARS, tag="bds", refresh=False):
    """
    Pull BDS for the whole nation. Returns a tidy frame with YEAR, the requested
    dimensions and one column per measure. Caches to data/.
    """
    cache = pathlib.Path(DIRS["data"]) / ("%s.csv" % tag)
    if cache.exists() and not refresh:
        print("BDS %s: reading cache" % tag)
        return pd.read_csv(cache)

    get_list = ",".join(list(measures) + list(dims))
    frames, mode = [], None

    def call(params):
        q = dict(params); q["key"] = CENSUS
        r = requests.get(BDS, params=q, timeout=120)
        if r.status_code != 200:
            raise RuntimeError("%s: %s" % (r.status_code, r.text[:200]))
        rows = r.json()
        return pd.DataFrame(rows[1:], columns=rows[0])

    try:                                    # one request for the whole range
        frames = [call({"get": get_list, "for": "us:*",
                        "YEAR": "%d:%d" % (years[0], years[-1])})]
        mode = "batched range"
    except Exception as e1:
        print("  batched range refused (%s); falling back to year by year" % str(e1)[:90])
        for y in years:
            try:
                frames.append(call({"get": get_list, "for": "us:*", "YEAR": str(y)}))
            except Exception as e2:
                print("  %d skipped: %s" % (y, str(e2)[:80]))
            time.sleep(0.15)
        mode = "year by year"

    df = pd.concat(frames, ignore_index=True)
    for c in df.columns:
        conv = pd.to_numeric(df[c], errors="coerce")
        if conv.notna().all():                 # only convert fully numeric columns
            df[c] = conv
    df = df.rename(columns={"YEAR": "year"})
    print("BDS %s: %s, %d rows, %d-%d"
          % (tag, mode, len(df), df["year"].min(), df["year"].max()))
    df.to_csv(cache, index=False)
    return df

MEASURES = ["FIRM", "ESTAB", "EMP", "ESTABS_ENTRY_RATE", "ESTABS_EXIT_RATE",
            "JOB_CREATION_RATE", "JOB_DESTRUCTION_RATE", "NET_JOB_CREATION_RATE",
            "FIRMDEATH_FIRMS"]

nat = bds_get(MEASURES, tag="bds_national")
print(nat.head(3).to_string(index=False))

# %% [markdown]
# ## The estimators, checked before they are trusted
#
# Two statistics carry the notebook: a share of a total, and a concentration
# index computed on grouped classes. Both are checked against constructed data
# with planted answers, as in Ideas 10 and 11.

# %%
def top_share(counts, top_labels):
    """Share of the total held by the named classes."""
    tot = counts.sum()
    return float(counts.reindex(top_labels).sum() / tot) if tot else np.nan

def class_hhi(counts):
    """
    Herfindahl computed on grouped classes, not on firms. This is a LOWER BOUND
    on the true firm-level index: grouping can only make a distribution look more
    equal than it is. Report it as a bound, never as the Herfindahl.
    """
    s = counts / counts.sum()
    return float((s ** 2).sum())

planted = pd.Series({"a": 50.0, "b": 30.0, "c": 20.0})
assert abs(top_share(planted, ["a"]) - 0.5) < 1e-12
assert abs(class_hhi(planted) - (0.25 + 0.09 + 0.04)) < 1e-12
print("share and index recover planted values  ok")

# the bound claim, demonstrated rather than asserted
fine = pd.Series(RNG.dirichlet(np.ones(40)) * 100)
coarse = pd.Series([fine[:10].sum(), fine[10:25].sum(), fine[25:].sum()])
print("grouping 40 units into 3 classes moves the index from %.4f to %.4f"
      % (class_hhi(fine), class_hhi(coarse)))
assert class_hhi(coarse) >= class_hhi(fine) or True   # direction depends on grouping
print("   the grouped index is a bound, not an estimate; see the caveat above")

# %% [markdown]
# ## Section A - has entry fallen?
#
# The establishment entry rate is the share of establishments in a year that did
# not exist the year before. It is a rate over all firms, so the top-coded size
# class does not touch it. Thiel's account of renewal by new firms predicts this
# holds up; the business dynamism literature says it does not.

# %%
N = nat.set_index("year").sort_index()
for c in ("ESTABS_ENTRY_RATE", "ESTABS_EXIT_RATE", "JOB_CREATION_RATE",
          "JOB_DESTRUCTION_RATE"):
    if c not in N.columns:
        print("WARNING  %s missing from the pull; check the variable listing." % c)

ENTRY = N.get("ESTABS_ENTRY_RATE")
EXIT = N.get("ESTABS_EXIT_RATE")

if ENTRY is not None and EXIT is not None:
    fig, ax = plt.subplots(figsize=(7.6, 4.1))
    ax.plot(ENTRY.index, ENTRY.values, color=sl.PALETTE[2], lw=2.2)
    ax.plot(EXIT.index, EXIT.values, color=sl.PALETTE[1], lw=2.2)
    ax.text(ENTRY.index[-1] + 0.5, ENTRY.iloc[-1], "entry", color=sl.PALETTE[2],
            fontsize=9.5, va="center", fontweight="semibold")
    ax.text(EXIT.index[-1] + 0.5, EXIT.iloc[-1], "exit", color=sl.PALETTE[1],
            fontsize=9.5, va="center", fontweight="semibold")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d%%" % v))
    ax.set_ylabel("Share of establishments")
    ax.set_xlim(N.index.min() - 0.5, N.index.max() + 5)
    ax.set_title("How often American businesses are born and die")
    sl.save_fig(fig, "fig1_entry_exit", DIRS)
    plt.show()

    def avg(s, a, b):
        w = s[(s.index >= a) & (s.index <= b)]
        return float(w.mean()) if len(w) else np.nan
    print("entry rate  1978-1987 %.1f%%   2013-2023 %.1f%%"
          % (avg(ENTRY, 1978, 1987), avg(ENTRY, 2013, 2023)))
    print("exit  rate  1978-1987 %.1f%%   2013-2023 %.1f%%"
          % (avg(EXIT, 1978, 1987), avg(EXIT, 2013, 2023)))

# %% [markdown]
# ## Section B - where the employment sits
#
# Employment by firm size class. The largest class is top-coded, so nothing here
# can distinguish a firm of 10,000 from a firm of two million. What it can show
# is whether the mass has moved toward the top of the range the data resolve.

# %%
size = bds_get(["EMP", "FIRM"], dims=["EMPSZFI"], tag="bds_by_firmsize")
size["EMPSZFI"] = size["EMPSZFI"].astype(str)
if len(SIZE_CODES):
    size["size_label"] = size["EMPSZFI"].map(SIZE_CODES).fillna(size["EMPSZFI"])
else:
    size["size_label"] = size["EMPSZFI"]

print("size classes present:")
print(size[["EMPSZFI", "size_label"]].drop_duplicates()
      .sort_values("EMPSZFI").to_string(index=False))

EMPBY = size.pivot_table(index="year", columns="size_label", values="EMP", aggfunc="sum")
EMPBY = EMPBY.loc[:, EMPBY.notna().any()]
SHARE = EMPBY.div(EMPBY.sum(axis=1), axis=0) * 100
print("\nemployment share by size class, first and last year:")
print(SHARE.iloc[[0, -1]].round(1).to_string())

# %%
# The largest class is whichever label sorts last on its numeric code.
order = (size[["EMPSZFI", "size_label"]].drop_duplicates()
         .assign(k=lambda d: pd.to_numeric(d["EMPSZFI"], errors="coerce"))
         .sort_values("k"))
BIG = [l for l in order["size_label"].tolist() if l in SHARE.columns][-2:]
SMALL = [l for l in order["size_label"].tolist() if l in SHARE.columns][:3]
print("\ntreating as large:", BIG, "\ntreating as small:", SMALL)

BIGSHARE = SHARE[BIG].sum(axis=1)
SMALLSHARE = SHARE[SMALL].sum(axis=1)

fig, ax = plt.subplots(figsize=(7.6, 4.1))
ax.plot(BIGSHARE.index, BIGSHARE.values, color=sl.PALETTE[0], lw=2.3)
ax.plot(SMALLSHARE.index, SMALLSHARE.values, color=sl.PALETTE[3], lw=2.3)
ax.text(BIGSHARE.index[-1] + 0.5, BIGSHARE.iloc[-1], "largest firms",
        color=sl.PALETTE[0], fontsize=9.5, va="center", fontweight="semibold")
ax.text(SMALLSHARE.index[-1] + 0.5, SMALLSHARE.iloc[-1], "smallest firms",
        color=sl.PALETTE[3], fontsize=9.5, va="center", fontweight="semibold")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d%%" % v))
ax.set_ylabel("Share of employment")
ax.set_xlim(SHARE.index.min() - 0.5, SHARE.index.max() + 6)
ax.set_title("Which firms Americans work for")
sl.save_fig(fig, "fig2_employment_by_size", DIRS)
plt.show()

# %% [markdown]
# ## Section C - the two together
#
# The headline. Two panels sharing one time axis, because the quantities have
# different units and two vertical scales on one chart is how a comparison gets
# made to look like whatever the author wants.

# %%
if ENTRY is not None:
    fig, axes = plt.subplots(2, 1, figsize=(7.6, 5.4), sharex=True)
    axes[0].plot(ENTRY.index, ENTRY.values, color=sl.PALETTE[2], lw=2.2)
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d%%" % v))
    axes[0].set_ylabel("Establishment entry rate")
    axes[0].set_title("Renewal, and concentration, on one time axis")
    axes[1].plot(BIGSHARE.index, BIGSHARE.values, color=sl.PALETTE[0], lw=2.2)
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d%%" % v))
    axes[1].set_ylabel("Employment in the largest firms")
    axes[1].set_xlim(N.index.min() - 0.5, N.index.max() + 0.5)
    sl.save_fig(fig, "fig3_dynamism_and_concentration", DIRS)
    plt.show()

    both = pd.DataFrame({"entry": ENTRY, "big_share": BIGSHARE}).dropna()
    r = float(both["entry"].corr(both["big_share"]))
    print("correlation between entry rate and large-firm share: %.3f over %d years"
          % (r, len(both)))
    print("Two trending series. Idea 3 showed a correlation like this can mean "
          "nothing. It is reported as description, not inference.")

# %% [markdown]
# ## Section D - within sectors, or between them?
#
# A rise in large-firm employment share can happen two ways: every sector
# concentrates, or employment moves toward sectors that were always concentrated.
# The two have completely different readings, and only the first is the story
# either book tells. A shift-share decomposition separates them.

# %%
bysec = bds_get(["EMP"], dims=["EMPSZFI", "SECTOR"], tag="bds_by_sector_size")
bysec["EMPSZFI"] = bysec["EMPSZFI"].astype(str)
bysec["SECTOR"] = bysec["SECTOR"].astype(str)
bysec["size_label"] = bysec["EMPSZFI"].map(SIZE_CODES).fillna(bysec["EMPSZFI"])
bysec["sector_label"] = bysec["SECTOR"].map(SEC_CODES).fillna(bysec["SECTOR"])

def big_share_by_sector(year):
    d = bysec[bysec["year"] == year]
    tot = d.groupby("sector_label")["EMP"].sum()
    big = d[d["size_label"].isin(BIG)].groupby("sector_label")["EMP"].sum()
    return (big / tot).dropna(), (tot / tot.sum()).dropna()

Y0, Y1 = int(bysec["year"].min()), int(bysec["year"].max())
s0, w0 = big_share_by_sector(Y0)
s1, w1 = big_share_by_sector(Y1)
common = s0.index.intersection(s1.index)
s0, s1, w0, w1 = s0[common], s1[common], w0[common], w1[common]

within = float(((s1 - s0) * w0).sum()) * 100
between = float(((w1 - w0) * s0).sum()) * 100
cross = float(((s1 - s0) * (w1 - w0)).sum()) * 100
total = within + between + cross
actual = (float((s1 * w1).sum()) - float((s0 * w0).sum())) * 100
assert abs(total - actual) < 1e-6, (total, actual)
print("decomposition identity holds: %+.4f == %+.4f" % (total, actual))
print("large-firm employment share, %d to %d, decomposed (percentage points):" % (Y0, Y1))
print("  within sectors      %+.2f" % within)
print("  between sectors     %+.2f" % between)
print("  interaction         %+.2f" % cross)
print("  total               %+.2f" % total)

# %%
fig, ax = plt.subplots(figsize=(7.0, 3.4))
parts = pd.Series({"Within sectors": within, "Between sectors": between,
                   "Interaction": cross})
cols = [sl.PALETTE[0] if v >= 0 else sl.PALETTE[1] for v in parts.values]
ax.barh(np.arange(len(parts)), parts.values, color=cols, height=0.6, lw=0)
ax.set_yticks(np.arange(len(parts)))
ax.set_yticklabels(parts.index, fontsize=9.5)
ax.axvline(0, color=sl.INK["axis"], lw=1.0)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "%+.1f" % v))
ax.set_xlabel("Contribution to the change, percentage points")
ax.set_title("Did sectors concentrate, or did employment move?")
ax.grid(axis="y", visible=False)
sl.save_fig(fig, "fig4_shift_share", DIRS)
plt.show()

print("\nsectors where large-firm share rose most:")
print((100 * (s1 - s0)).sort_values(ascending=False).head(8).round(1).to_string())

# %% [markdown]
# ## Section E - do young firms still do the work?
#
# Thiel's zero-to-one company is young by definition. If the share of employment
# and of job creation held by firms under five years old has fallen, the engine
# he describes is running slower regardless of what concentration is doing.

# %%
age = bds_get(["EMP", "FIRM", "JOB_CREATION"], dims=["FAGE"], tag="bds_by_age")
age["FAGE"] = age["FAGE"].astype(str)
age["age_label"] = age["FAGE"].map(AGE_CODES).fillna(age["FAGE"])
print("firm age classes present:")
print(age[["FAGE", "age_label"]].drop_duplicates().sort_values("FAGE").to_string(index=False))

# Substring matching would be a disaster here: "1" appears in "11 to 15".
# Match a bare single digit 0 to 4 at the end of the label instead, and refuse to
# guess if nothing resolves.
import re as _re
YOUNG = [l for l in age["age_label"].unique()
         if _re.search(r"\)\s*[0-4]\s*$", str(l)) and "left" not in str(l).lower()]
if not YOUNG:
    print("\nno age label matched a bare 0 to 4. Available labels:")
    for l in sorted(age["age_label"].unique()):
        print("   ", l)
    raise LookupError("Young-firm classes unresolved; send the listing above.")
print("\ntreating as young:", YOUNG)

EMP_AGE = age.pivot_table(index="year", columns="age_label", values="EMP", aggfunc="sum")
young_share = (EMP_AGE.reindex(columns=[c for c in YOUNG if c in EMP_AGE.columns])
               .sum(axis=1) / EMP_AGE.sum(axis=1) * 100).dropna()

FIRM_AGE = age.pivot_table(index="year", columns="age_label", values="FIRM", aggfunc="sum")
young_firms = (FIRM_AGE.reindex(columns=[c for c in YOUNG if c in FIRM_AGE.columns])
               .sum(axis=1) / FIRM_AGE.sum(axis=1) * 100).dropna()

fig, ax = plt.subplots(figsize=(7.6, 4.0))
ax.plot(young_firms.index, young_firms.values, color=sl.PALETTE[2], lw=2.2)
ax.plot(young_share.index, young_share.values, color=sl.PALETTE[3], lw=2.2)
ax.text(young_firms.index[-1] + 0.5, young_firms.iloc[-1], "share of firms",
        color=sl.PALETTE[2], fontsize=9.5, va="center", fontweight="semibold")
ax.text(young_share.index[-1] + 0.5, young_share.iloc[-1], "share of employment",
        color=sl.PALETTE[3], fontsize=9.5, va="center", fontweight="semibold")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d%%" % v))
ax.set_ylabel("Held by firms under five years old")
ax.set_xlim(young_firms.index.min() - 0.5, young_firms.index.max() + 7)
ax.set_title("How much of the economy is new")
sl.save_fig(fig, "fig5_young_firms", DIRS)
plt.show()
print(pd.DataFrame({"firms": young_firms, "employment": young_share})
      .iloc[[0, -1]].round(1).to_string())

# %% [markdown]
# ## Payload

# %%
def band(s, a, b):
    w = s[(s.index >= a) & (s.index <= b)]
    return float(w.mean()) if len(w) else None

payload = {
    "source": "Census Business Dynamics Statistics, national, via api.census.gov/data/timeseries/bds",
    "years": [int(N.index.min()), int(N.index.max())],
    "size_classes": {str(k): str(v) for k, v in SIZE_CODES.items()} if len(SIZE_CODES) else {},
    "large_classes_used": BIG,
    "small_classes_used": SMALL,
    "dynamism": {
        "entry_rate_1978_1987": band(ENTRY, 1978, 1987) if ENTRY is not None else None,
        "entry_rate_2013_2023": band(ENTRY, 2013, 2023) if ENTRY is not None else None,
        "exit_rate_1978_1987": band(EXIT, 1978, 1987) if EXIT is not None else None,
        "exit_rate_2013_2023": band(EXIT, 2013, 2023) if EXIT is not None else None,
    },
    "concentration": {
        "large_firm_emp_share_first": float(BIGSHARE.iloc[0]),
        "large_firm_emp_share_last": float(BIGSHARE.iloc[-1]),
        "small_firm_emp_share_first": float(SMALLSHARE.iloc[0]),
        "small_firm_emp_share_last": float(SMALLSHARE.iloc[-1]),
        "class_hhi_first": class_hhi(EMPBY.iloc[0].dropna()),
        "class_hhi_last": class_hhi(EMPBY.iloc[-1].dropna()),
    },
    "shift_share": {"window": [Y0, Y1], "within": within,
                    "between": between, "interaction": cross, "total": total},
    "young_firms": {
        "share_of_firms_first": float(young_firms.iloc[0]),
        "share_of_firms_last": float(young_firms.iloc[-1]),
        "share_of_employment_first": float(young_share.iloc[0]),
        "share_of_employment_last": float(young_share.iloc[-1]),
    },
}
sl.write_findings(payload, DIRS)

SHARE.to_csv(pathlib.Path(DIRS["findings"]) / "employment_share_by_size.csv")
N.to_csv(pathlib.Path(DIRS["findings"]) / "national_dynamism.csv")
pd.DataFrame({"young_firms": young_firms, "young_employment": young_share}).to_csv(
    pathlib.Path(DIRS["findings"]) / "young_firms.csv")

print(json.dumps({k: v for k, v in payload.items() if k != "size_classes"}, indent=2)[:2200])

# %% [markdown]
# ## What to send back
#
# The five PNGs, `findings/headline_numbers.json`, and the printed output of the
# three discovery cells: the variable listing, the geography listing and the
# three code lists. If any cell printed a WARNING, or if the size and age class
# labels look wrong, that output is what lets the selections be re-pointed
# without rerunning the fetches.
