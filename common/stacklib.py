"""
stacklib -- shared helpers for the "14 Ideas" article project.

Used by every idea notebook. Handles:
  * locating the project root and the current idea's folders
  * tolerant .env parsing (the file mixes "NAME: value" and "NAME=value", CRLF)
  * cached pulls from BEA, FRED, BLS and Census
  * a single matplotlib theme so all 14 ideas' figures look like one system

Nothing here calls an API without a key you supply from your own .env.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import time

import numpy as np
import pandas as pd
import requests

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

__version__ = "0.8.0"   # bump when this file changes

__all__ = [
    "__version__", "project_root", "dirs_for", "load_keys", "require",
    "bea_nipa_table", "bea_table", "bea_parameter_values", "pick_lines", "fred_series", "fred_search", "fred_first_available", "fred_titles", "fred_resolve", "bls_series", "census_timeseries", "census_group_labels",
    "to_annual", "apply_theme", "PALETTE", "INK", "save_fig", "label_last", "loglinear_fit",
    "chow_test", "write_findings",
]


# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------

def project_root(start: str | os.PathLike | None = None) -> pathlib.Path:
    """Walk up from `start` (default: cwd) until we find common/stacklib.py."""
    p = pathlib.Path(start or os.getcwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / "common" / "stacklib.py").exists():
            return cand
    raise FileNotFoundError(
        "Could not find the project root above %s -- expected a 'common/stacklib.py'. "
        "Run the notebook from inside the Stack_Article tree." % p
    )


def dirs_for(idea_slug: str | None = None, start=None) -> dict:
    """Return {root, idea, data, figures, findings} and create the last three."""
    root = project_root(start)
    if idea_slug:
        base = root / idea_slug
    else:
        p = pathlib.Path(start or os.getcwd()).resolve()
        base = None
        for cand in [p, *p.parents]:
            if cand.parent == root:
                base = cand
                break
        if base is None:
            raise FileNotFoundError(
                "Could not infer which idea folder you are in; pass idea_slug explicitly."
            )
    d = {"root": root, "idea": base, "data": base / "data",
         "figures": base / "figures", "findings": base / "findings"}
    for k in ("data", "figures", "findings"):
        d[k].mkdir(parents=True, exist_ok=True)
    return d


# --------------------------------------------------------------------------
# keys
# --------------------------------------------------------------------------

_KEY_LINE = re.compile(r"^\s*([A-Za-z0-9_. ]+?)\s*[:=]\s*(.*?)\s*$")


def _canon(name: str) -> str:
    s = name.upper().replace("API", "").replace("KEY", "")
    return re.sub(r"[^A-Z]", "", s)


def load_keys(env_path=None, verbose: bool = True) -> dict:
    """
    Parse the project .env. Tolerates:
      NAME: value   and   NAME = value
      a space inside the name ("BEA API_KEY")
      CRLF line endings, a UTF-8 BOM, quoted values, blank lines, # comments
    Returns {"BEA": ..., "CENSUS": ..., "FRED": ..., "BLS": ...}.
    """
    root = project_root()
    path = pathlib.Path(env_path) if env_path else root / ".env"
    if not path.exists():
        raise FileNotFoundError("No .env found at %s" % path)
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    keys = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _KEY_LINE.match(line)
        if not m:
            continue
        name, val = m.group(1), m.group(2).strip().strip('"').strip("'")
        if val:
            keys[_canon(name)] = val
    if verbose:
        found = ", ".join(sorted(keys)) or "(none)"
        print("Keys loaded from %s: %s" % (path.name, found))
    return keys


def require(keys: dict, name: str) -> str:
    if name not in keys or not keys[name]:
        raise KeyError(
            "No %s key found in .env. Expected a line like '%s_API_KEY = ...'." % (name, name)
        )
    return keys[name]


# --------------------------------------------------------------------------
# BEA
# --------------------------------------------------------------------------

BEA_URL = "https://apps.bea.gov/api/data/"


def bea_nipa_table(table_name: str, key: str, frequency: str = "A", year: str = "ALL",
                   cache_dir=None, refresh: bool = False) -> pd.DataFrame:
    """
    Pull one NIPA table (e.g. 'T50304') and return a tidy frame:
        line | description | year | period | value | series_code
    Caches to cache_dir so re-running the notebook costs no API calls.
    """
    cache = None
    if cache_dir is not None:
        cache = pathlib.Path(cache_dir) / ("bea_%s_%s.csv" % (table_name, frequency))
        if cache.exists() and not refresh:
            print("BEA %s: reading cache %s" % (table_name, cache.name))
            return pd.read_csv(cache)

    params = {"UserID": key, "method": "GetData", "datasetname": "NIPA",
              "TableName": table_name, "Frequency": frequency, "Year": year,
              "ResultFormat": "JSON"}
    r = requests.get(BEA_URL, params=params, timeout=90)
    r.raise_for_status()
    try:
        payload = r.json()
    except ValueError:
        raise RuntimeError("BEA returned non-JSON (first 300 chars): %s" % r.text[:300])

    api = payload.get("BEAAPI", {})
    if "Error" in api:
        raise RuntimeError("BEA API error: %s" % api["Error"])
    results = api.get("Results", {})
    if isinstance(results, list):
        results = results[0] if results else {}
    if "Error" in results:
        raise RuntimeError("BEA API error for %s: %s" % (table_name, results["Error"]))
    data = results.get("Data")
    if not data:
        raise RuntimeError("BEA returned no rows for %s. Check the TableName." % table_name)

    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(
        df["DataValue"].astype(str).str.replace(",", "", regex=False), errors="coerce")
    df["year"] = pd.to_numeric(df["TimePeriod"].astype(str).str[:4], errors="coerce")
    df["line"] = pd.to_numeric(df["LineNumber"], errors="coerce")
    df = df.rename(columns={"LineDescription": "description",
                            "TimePeriod": "period", "SeriesCode": "series_code"})
    out = (df[["line", "description", "year", "period", "value", "series_code"]]
           .dropna(subset=["year"])
           .sort_values(["line", "year"])
           .reset_index(drop=True))
    print("BEA %s: %d rows, %d lines, %d-%d"
          % (table_name, len(out), out["line"].nunique(),
             int(out["year"].min()), int(out["year"].max())))
    if cache is not None:
        out.to_csv(cache, index=False)
    return out



def bea_table(dataset: str, table_name: str, key: str, frequency: str = "A",
              year: str = "ALL", cache_dir=None, refresh: bool = False,
              **extra) -> pd.DataFrame:
    """
    Generic BEA fetch for any dataset that returns Results.Data rows
    (NIPA, FixedAssets, ...). Same tidy shape as bea_nipa_table.
    """
    cache = None
    if cache_dir is not None:
        cache = pathlib.Path(cache_dir) / ("bea_%s_%s_%s.csv" % (dataset, table_name, frequency))
        if cache.exists() and not refresh:
            print("BEA %s/%s: reading cache" % (dataset, table_name))
            return pd.read_csv(cache)

    params = {"UserID": key, "method": "GetData", "datasetname": dataset,
              "TableName": table_name, "Frequency": frequency, "Year": year,
              "ResultFormat": "JSON"}
    params.update(extra)
    r = requests.get(BEA_URL, params=params, timeout=120)
    r.raise_for_status()
    api = r.json().get("BEAAPI", {})
    if "Error" in api:
        raise RuntimeError("BEA API error: %s" % api["Error"])
    results = api.get("Results", {})
    if isinstance(results, list):
        results = results[0] if results else {}
    if "Error" in results:
        raise RuntimeError("BEA error for %s/%s: %s" % (dataset, table_name, results["Error"]))
    data = results.get("Data")
    if not data:
        raise RuntimeError("BEA returned no rows for %s/%s." % (dataset, table_name))

    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(
        df["DataValue"].astype(str).str.replace(",", "", regex=False), errors="coerce")
    df["year"] = pd.to_numeric(df["TimePeriod"].astype(str).str[:4], errors="coerce")
    df["line"] = pd.to_numeric(df["LineNumber"], errors="coerce")
    df = df.rename(columns={"LineDescription": "description",
                            "TimePeriod": "period", "SeriesCode": "series_code"})
    out = (df[["line", "description", "year", "period", "value", "series_code"]]
           .dropna(subset=["year"]).sort_values(["line", "year"]).reset_index(drop=True))
    print("BEA %s/%s: %d rows, %d lines, %d-%d"
          % (dataset, table_name, len(out), out["line"].nunique(),
             int(out["year"].min()), int(out["year"].max())))
    if cache is not None:
        out.to_csv(cache, index=False)
    return out


def bea_parameter_values(dataset: str, parameter: str, key: str,
                         contains: str = None) -> pd.DataFrame:
    """
    Ask BEA what values a parameter accepts, e.g. every TableName in the
    FixedAssets dataset. Use it instead of guessing a table code.
    """
    r = requests.get(BEA_URL, params={"UserID": key, "method": "GetParameterValues",
                                      "datasetname": dataset, "ParameterName": parameter,
                                      "ResultFormat": "JSON"}, timeout=90)
    r.raise_for_status()
    api = r.json().get("BEAAPI", {})
    if "Error" in api:
        raise RuntimeError("BEA API error: %s" % api["Error"])
    rows = api.get("Results", {}).get("ParamValue", [])
    df = pd.DataFrame(rows)
    if contains and len(df):
        col = "Description" if "Description" in df.columns else df.columns[-1]
        df = df[df[col].astype(str).str.contains(contains, case=False, na=False)]
    print("BEA %s.%s: %d values%s" % (dataset, parameter, len(df),
                                      (" matching %r" % contains) if contains else ""))
    return df.reset_index(drop=True)


def pick_lines(tidy: pd.DataFrame, wanted: dict, strict: bool = False) -> pd.DataFrame:
    """
    Select BEA lines by number or by description.

    wanted maps a label to either:
        an int   -- the BEA line number (preferred once you have seen the table)
        a string -- a regex matched case-insensitively against the description

    Returns a wide frame indexed by year, one column per label, and prints the
    line each label resolved to so a wrong pick is visible rather than silent.
    A label that matches nothing is skipped with a warning unless strict=True.
    """
    descs = tidy[["line", "description"]].drop_duplicates().copy()
    descs["description"] = descs["description"].astype(str).str.strip()
    cols = {}
    for label, sel in wanted.items():
        if isinstance(sel, (int, np.integer)):
            hit = descs[descs["line"] == int(sel)]
            how = "line %d" % int(sel)
        else:
            hit = descs[descs["description"].str.contains(sel, case=False, regex=True, na=False)]
            how = repr(sel)
        if hit.empty:
            msg = "No BEA line matched %s for label %r." % (how, label)
            if strict:
                print("\nAvailable line descriptions:")
                for _, row in descs.iterrows():
                    print("   %4d  %s" % (row["line"], row["description"]))
                raise LookupError(msg)
            print("WARNING: " + msg + " Skipping this series.")
            continue
        line_no = int(hit.iloc[0]["line"])
        matched = hit.iloc[0]["description"]
        if len(hit) > 1:
            others = ", ".join(str(int(v)) for v in hit["line"].tolist()[1:])
            print("NOTE  %-24s %s is ambiguous (also lines %s); using %d"
                  % (label, how, others, line_no))
        print("match %-24s -> line %3d  %s" % (label, line_no, matched))
        s = (tidy[tidy["line"] == line_no]
             .drop_duplicates(subset=["year"])
             .set_index("year")["value"])
        cols[label] = s
    if not cols:
        raise LookupError("pick_lines matched nothing at all -- check the table name.")
    wide = pd.DataFrame(cols).sort_index()
    wide.index = wide.index.astype(int)
    return wide


# --------------------------------------------------------------------------
# FRED / BLS / Census
# --------------------------------------------------------------------------

def fred_series(series_id: str, key: str, cache_dir=None, refresh: bool = False,
                **params) -> pd.Series:
    """One FRED series as a float Series indexed by date."""
    cache = None
    if cache_dir is not None:
        cache = pathlib.Path(cache_dir) / ("fred_%s.csv" % series_id)
        if cache.exists() and not refresh:
            print("FRED %s: reading cache" % series_id)
            s = pd.read_csv(cache, index_col=0, parse_dates=True).iloc[:, 0]
            s.name = series_id
            return s
    url = "https://api.stlouisfed.org/fred/series/observations"
    q = {"series_id": series_id, "api_key": key, "file_type": "json"}
    q.update(params)
    r = requests.get(url, params=q, timeout=60)
    if r.status_code != 200:
        raise RuntimeError("FRED %s failed (%s): %s" % (series_id, r.status_code, r.text[:300]))
    obs = r.json().get("observations", [])
    if not obs:
        raise RuntimeError("FRED %s returned no observations." % series_id)
    df = pd.DataFrame(obs)
    s = pd.Series(pd.to_numeric(df["value"].replace(".", np.nan), errors="coerce").values,
                  index=pd.to_datetime(df["date"]), name=series_id).dropna()
    print("FRED %s: %d obs, %s-%s" % (series_id, len(s), s.index.min().date(), s.index.max().date()))
    if cache is not None:
        s.to_frame().to_csv(cache)
    return s




def census_group_labels(base_url: str, group: str) -> pd.DataFrame:
    """
    Fetch the official variable labels for a Census table group.

    Census labels encode a hierarchy with "!!" separators, e.g.
    "Estimate!!Total:!!Male:!!Management, business, science, and arts occupations:".
    The depth of that path is what lets a notebook select one level of the
    occupation tree instead of guessing which variable numbers mean what.

    No key required; this is metadata. Returns: name | label | depth | leaf.
    """
    url = "%s/groups/%s.json" % (base_url.rstrip("/"), group)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    variables = r.json().get("variables", {})
    rows = []
    for name, meta in variables.items():
        if not name.endswith("E"):
            continue
        label = str(meta.get("label", ""))
        parts = [p for p in label.split("!!") if p]
        rows.append({"name": name, "label": label, "depth": len(parts),
                     "leaf": parts[-1].rstrip(":") if parts else ""})
    df = pd.DataFrame(rows).sort_values("name").reset_index(drop=True)
    print("Census %s: %d estimate variables, depths %s"
          % (group, len(df), sorted(df["depth"].unique())))
    return df


def fred_search(text: str, key: str, limit: int = 15) -> pd.DataFrame:
    """
    Find FRED series by text. Use this instead of guessing an ID: print the
    candidates, read the titles and coverage, then hard-code the winner.
    """
    r = requests.get("https://api.stlouisfed.org/fred/series/search",
                     params={"search_text": text, "api_key": key, "file_type": "json",
                             "limit": limit, "order_by": "popularity", "sort_order": "desc"},
                     timeout=60)
    r.raise_for_status()
    rows = r.json().get("seriess", [])
    if not rows:
        print("No FRED series matched %r" % text)
        return pd.DataFrame()
    df = pd.DataFrame(rows)[["id", "title", "frequency_short", "units_short",
                             "observation_start", "observation_end", "popularity"]]
    df["observation_start"] = df["observation_start"].str[:4]
    df["observation_end"] = df["observation_end"].str[:4]
    return df.rename(columns={"frequency_short": "freq", "units_short": "units",
                              "observation_start": "from", "observation_end": "to"})


def fred_first_available(candidates, key: str, cache_dir=None, **params):
    """
    Try each candidate FRED id in order and return (id, Series) for the first
    that resolves. Keeps one retired or renamed series from killing a notebook.
    """
    errors = []
    for sid in candidates:
        try:
            return sid, fred_series(sid, key, cache_dir=cache_dir, **params)
        except Exception as e:
            errors.append("%s: %s" % (sid, str(e)[:90]))
    raise RuntimeError("None of the candidate FRED series resolved.\n  " + "\n  ".join(errors))




def fred_titles(series_ids, key: str) -> pd.DataFrame:
    """
    Look up the official title of each series id. Use this to LABEL a chart.

    Guessing an identifier and then labelling it from memory is how a chart ends
    up saying "bachelor's degree" over a line that is really high-school
    dropouts. Fetch the titles, print them, and copy the labels from the source.
    """
    rows = []
    for sid in ([series_ids] if isinstance(series_ids, str) else series_ids):
        try:
            r = requests.get("https://api.stlouisfed.org/fred/series",
                             params={"series_id": sid, "api_key": key, "file_type": "json"},
                             timeout=45)
            r.raise_for_status()
            info = r.json()["seriess"][0]
            rows.append({"id": sid, "title": info.get("title"),
                         "units": info.get("units_short"), "freq": info.get("frequency_short"),
                         "from": str(info.get("observation_start"))[:4],
                         "to": str(info.get("observation_end"))[:4]})
        except Exception as e:
            rows.append({"id": sid, "title": "LOOKUP FAILED: %s" % str(e)[:70],
                         "units": None, "freq": None, "from": None, "to": None})
    return pd.DataFrame(rows)



def fred_resolve(candidates, label: str, expect, key: str, cache_dir=None, **kw):
    """
    Fetch a FRED series, look up its official title, and refuse to return it if
    the title does not contain every word in `expect`.

    Idea 5 shipped a chart whose lines were labelled from memory rather than
    from the source, and it said "bachelor's degree" over high-school dropouts.
    This makes that failure loud instead of silent. Returns (id, title, series).
    """
    sid, s = fred_first_available(candidates, key, cache_dir=cache_dir, **kw)
    title = fred_titles([sid], key).iloc[0]["title"]
    print("  %-30s %-20s %s" % (label, sid, title))
    missing = [w for w in expect if w.lower() not in str(title).lower()]
    if missing:
        raise AssertionError(
            "Series %s is titled %r, missing %s. Expected a series for %r. "
            "Fix the candidate list, not the label." % (sid, title, missing, label))
    return sid, title, s


def to_annual(s: pd.Series, drop_partial: bool = True, how: str = "mean") -> pd.Series:
    """
    Collapse a dated series to calendar years.

    Monthly and quarterly series almost always end mid-year, and averaging a
    partial year against full ones drags the endpoint. With drop_partial the
    final year is kept only if it has as many observations as a typical year.
    """
    counts = s.groupby(s.index.year).size()
    out = getattr(s.groupby(s.index.year), how)()
    out.index = out.index.astype(int)
    if drop_partial and len(counts) > 2:
        full = int(counts.iloc[:-1].mode().iloc[0])
        incomplete = counts[counts < full]
        if len(incomplete):
            dropped = [int(y) for y in incomplete.index]
            out = out.drop(index=dropped, errors="ignore")
            print("   dropped partial year(s) %s (had %s of %d observations)"
                  % (dropped, list(incomplete.values), full))
    return out


def bls_series(series_ids, key: str, start_year: int, end_year: int,
               cache_dir=None, refresh: bool = False) -> pd.DataFrame:
    """BLS v2 timeseries. Returns tidy: series_id | year | period | value."""
    if isinstance(series_ids, str):
        series_ids = [series_ids]
    tag = "-".join(series_ids)[:60]
    cache = None
    if cache_dir is not None:
        cache = pathlib.Path(cache_dir) / ("bls_%s_%s_%s.csv" % (tag, start_year, end_year))
        if cache.exists() and not refresh:
            print("BLS %s: reading cache" % tag)
            return pd.read_csv(cache)
    frames = []
    for i in range(0, len(series_ids), 50):          # 50 series per request
        chunk = series_ids[i:i + 50]
        for y0 in range(start_year, end_year + 1, 20):   # 20 years per request
            y1 = min(y0 + 19, end_year)
            body = {"seriesid": chunk, "startyear": str(y0), "endyear": str(y1),
                    "registrationkey": key}
            r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                              json=body, timeout=90)
            r.raise_for_status()
            js = r.json()
            if js.get("status") != "REQUEST_SUCCEEDED":
                raise RuntimeError("BLS error: %s" % js.get("message"))
            for s in js["Results"]["series"]:
                for row in s["data"]:
                    frames.append({"series_id": s["seriesID"], "year": int(row["year"]),
                                   "period": row["period"], "value": row["value"]})
            time.sleep(0.4)
    out = pd.DataFrame(frames)
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    print("BLS: %d rows across %d series" % (len(out), out["series_id"].nunique()))
    if cache is not None:
        out.to_csv(cache, index=False)
    return out


def census_timeseries(url: str, params: dict, key: str, cache_dir=None,
                      refresh: bool = False, tag: str = "census") -> pd.DataFrame:
    """Generic Census API pull -- first row of the response is the header."""
    cache = None
    if cache_dir is not None:
        cache = pathlib.Path(cache_dir) / ("%s.csv" % tag)
        if cache.exists() and not refresh:
            print("Census %s: reading cache" % tag)
            return pd.read_csv(cache)
    q = dict(params)
    q["key"] = key
    r = requests.get(url, params=q, timeout=90)
    if r.status_code != 200:
        raise RuntimeError("Census failed (%s): %s" % (r.status_code, r.text[:300]))
    rows = r.json()
    out = pd.DataFrame(rows[1:], columns=rows[0])
    print("Census %s: %d rows" % (tag, len(out)))
    if cache is not None:
        out.to_csv(cache, index=False)
    return out


# --------------------------------------------------------------------------
# chart theme -- one system across all 14 ideas
# --------------------------------------------------------------------------

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

INK = {"surface": "#fcfcfb", "primary": "#0b0b0b", "secondary": "#52514e",
       "muted": "#898781", "grid": "#e1e0d9", "axis": "#c3c2b7"}


def apply_theme():
    mpl.rcParams.update({
        "figure.facecolor": INK["surface"],
        "axes.facecolor": INK["surface"],
        "savefig.facecolor": INK["surface"],
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial", "sans-serif"],
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.labelsize": 9.5,
        "axes.labelcolor": INK["secondary"],
        "axes.edgecolor": INK["axis"],
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": INK["grid"],
        "grid.linewidth": 0.8,
        "xtick.color": INK["muted"],
        "ytick.color": INK["muted"],
        "xtick.labelcolor": INK["secondary"],
        "ytick.labelcolor": INK["secondary"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "legend.fontsize": 9,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "figure.dpi": 110,
        "figure.constrained_layout.use": True,
    })
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=PALETTE)


def save_fig(fig, name: str, dirs: dict, dpi: int = 200, svg: bool = True):
    """Save a figure into <idea>/figures as PNG (+SVG). Returns the PNG path."""
    png = pathlib.Path(dirs["figures"]) / ("%s.png" % name)
    fig.savefig(png, dpi=dpi, bbox_inches="tight", facecolor=INK["surface"])
    if svg:
        fig.savefig(pathlib.Path(dirs["figures"]) / ("%s.svg" % name),
                    bbox_inches="tight", facecolor=INK["surface"])
    print("saved -> %s" % png)
    return png


def label_last(ax, series: pd.Series, text: str, color: str, dx: float = 0.6,
               fontsize: float = 9.5, va: str = "center"):
    """Direct-label the right-hand end of a line (used instead of a busy legend)."""
    s = series.dropna()
    if s.empty:
        return
    ax.text(s.index[-1] + dx, s.iloc[-1], text, color=color, fontsize=fontsize,
            va=va, ha="left", fontweight="semibold", clip_on=False)


# --------------------------------------------------------------------------
# small statistics helpers
# --------------------------------------------------------------------------

def loglinear_fit(s: pd.Series, label: str = "") -> dict:
    """
    Fit ln(y) = a + b*t. Returns the annual compound rate implied by b,
    R^2, the doubling/halving time, and the sample window.
    """
    s = s.dropna()
    s = s[s > 0]
    if len(s) < 5:
        return {"label": label, "n": len(s), "note": "too few observations"}
    t = np.asarray(s.index, dtype=float)
    y = np.log(np.asarray(s.values, dtype=float))
    b, a = np.polyfit(t, y, 1)
    fit = a + b * t
    ss_res = float(np.sum((y - fit) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    rate = np.expm1(b)                       # compound annual growth rate
    half = np.log(0.5) / b if b != 0 else np.nan
    return {"label": label, "start": int(t[0]), "end": int(t[-1]), "n": len(s),
            "annual_pct": 100 * rate, "r2": r2,
            "halving_years": abs(half), "slope_ln": b, "rss": ss_res}


def chow_test(s: pd.Series, break_year: int):
    """Chow test for a break in the log-linear trend at break_year. F and (if scipy) p."""
    s = s.dropna()
    s = s[s > 0]
    pre, post = s[s.index <= break_year], s[s.index > break_year]
    if len(pre) < 5 or len(post) < 5:
        return {"break": break_year, "note": "not enough data either side"}
    full = loglinear_fit(s)
    f1, f2 = loglinear_fit(pre), loglinear_fit(post)
    k, n = 2, len(s)
    num = (full["rss"] - (f1["rss"] + f2["rss"])) / k
    den = (f1["rss"] + f2["rss"]) / (n - 2 * k)
    F = num / den
    out = {"break": break_year, "F": F, "n": n,
           "pre_annual_pct": f1["annual_pct"], "post_annual_pct": f2["annual_pct"]}
    try:
        from scipy import stats
        out["p"] = float(1 - stats.f.cdf(F, k, n - 2 * k))
    except Exception:
        out["p"] = None
    return out


def write_findings(payload: dict, dirs: dict, name: str = "headline_numbers.json"):
    """Dump the numbers the write-up will quote, so the prose cites the run."""
    path = pathlib.Path(dirs["findings"]) / name
    def _clean(o):
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_clean(v) for v in o]
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if np.isnan(o) else round(float(o), 6)
        if isinstance(o, (pd.Timestamp,)):
            return str(o.date())
        return o
    path.write_text(json.dumps(_clean(payload), indent=2), encoding="utf-8")
    print("findings -> %s" % path)
    return path
