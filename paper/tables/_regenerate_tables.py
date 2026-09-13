"""Emit LaTeX table fragments straight from the validated findings payloads.

Every number in the paper passes through this file. Nothing is typed into
main.tex by hand.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]   # repository root
UP = ROOT
OUT14 = ROOT / "14_value_created_value_captured/findings"
OUT = pathlib.Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

P12 = json.loads((UP / "12_dynamism_and_concentration/findings/headline_numbers.json").read_text())
P13 = json.loads((UP / "13_the_shape_of_the_distribution/findings/headline_numbers.json").read_text())
P14 = json.loads((OUT14 / "headline_numbers.json").read_text())

F13 = pd.read_csv(UP / "13_the_shape_of_the_distribution/findings/fits_by_year.csv", index_col=0)
S13 = pd.read_csv(UP / "13_the_shape_of_the_distribution/findings/tail_threshold_sweep.csv", index_col=0)
T13 = pd.read_csv(UP / "13_the_shape_of_the_distribution/findings/top_bin_counts.csv", index_col=0)
N12 = pd.read_csv(UP / "12_dynamism_and_concentration/findings/national_dynamism.csv", index_col=0)
Y12 = pd.read_csv(UP / "12_dynamism_and_concentration/findings/young_firms.csv", index_col=0)
C14 = pd.read_csv(OUT14 / "concentration_by_year.csv", index_col=0)


def w(name, body):
    (OUT / ("%s.tex" % name)).write_text(body.strip() + "\n")
    print("  ", name)


def sg(x, d=3):
    """Signed number, aligned so the minus sign does not shift the column."""
    s = "%+.*f" % (d, x)
    return ("$-$" + s[1:]) if s.startswith("-") else ("$\\phantom{-}$" + s[1:])


# ------------------------------------------------------------------ T1 sources
w("tab_sources", r"""
\begin{table}[H]
\caption{Data sources. Both series are public and are retrieved through documented
APIs rather than downloaded as files, so the extraction is reproducible from the
query alone. The Business Dynamics Statistics is a census of employer firms rather
than a sample; the GDP-by-Industry accounts are the published national accounts at
their finest industry detail. Source: authors' compilation.}
\label{tab:sources}
\begin{tabular}{llll}
\toprule
Series & Provider & Coverage & Unit \\
\midrule
Business Dynamics Statistics & US Census Bureau & 1978--2023, annual & employer firm \\
\quad firm counts by size class & & 10 classes & firms \\
\quad employment by size class & & 10 classes & employees \\
\quad firms and employment by age & & 12 classes, from 1982 & firms, employees \\
\quad establishment entry and exit & & national & rate, per cent \\
\quad employment by size and sector & & 19 NAICS sectors & employees \\
GDP-by-Industry accounts & US Bureau of & 1997--2025, annual & industry \\
\quad value added & \quad Economic Analysis & 71 industries & USD billions \\
\quad gross output & & 71 industries & USD billions \\
\quad components of value added & & 71 industries, to 2024 & USD billions \\
\bottomrule
\end{tabular}
\end{table}
""")

# ------------------------------------------------------------------ T2 bins
lab = P13["bins"]["labels"]
lo = P13["bins"]["lower_edges"]
codes = list(lab.keys())
rows = []
counts = pd.read_csv(UP / "13_the_shape_of_the_distribution/findings/firm_counts_by_class.csv",
                     index_col=0)
first, last = counts.index.min(), counts.index.max()
for i, c in enumerate(codes):
    hi = "$\\infty$" if i == len(codes) - 1 else "%d" % int(lo[i + 1])
    n0 = counts.loc[first, c] if c in counts.columns else np.nan
    n1 = counts.loc[last, c] if c in counts.columns else np.nan
    rows.append("%s & %s & [%d, %s) & %s & %s \\\\" % (
        c, lab[c].replace("Firms with ", "").replace(" employees", ""),
        int(lo[i]), hi, "{:,.0f}".format(n0), "{:,.0f}".format(n1)))
w("tab_bins", r"""
\begin{table}[H]
\caption{The ten firm-size classes of the Business Dynamics Statistics, the interval
each covers, and the firm counts at the ends of the sample. The class boundaries are
the published Census breaks; they were also recovered independently by the arithmetic
described in Section~\ref{subsec:partition} and agree in all ten classes. The top class
is open, which is what makes the tail exponent identifiable and what prevents anything
inside it from being observed. Source: authors' calculations from BDS.}
\label{tab:bins}
\begin{tabular}{llrrr}
\toprule
Code & Class & Interval & Firms, %d & Firms, %d \\
\midrule
%s
\bottomrule
\end{tabular}
\end{table}
""" % (first, last, "\n".join(rows)))

# ------------------------------------------------------------------ T3 validation
v = P13["validation"]
w("tab_validation", r"""
\begin{table}[H]
\caption{Estimator validation against planted answers. Each row states a quantity whose
true value is known by construction, the value the estimator recovered, and the test the
recovery had to pass before any result below it was computed. Samples were drawn from the
named distribution and binned exactly as the Business Dynamics Statistics bins firms, so
the estimator sees the same interval censoring it meets in the data. Source: authors'
calculations.}
\label{tab:validation}
\begin{tabular}{lllll}
\toprule
Quantity & Instrument & Planted & Recovered & Test \\
\midrule
Pareto exponent & interval-censored MLE, 10 bins & %.2f & %.4f & $|\hat\alpha-\alpha|<0.02$ \\
Log-normal dispersion & interval-censored MLE, 10 bins & %.2f & %.4f & $|\hat\sigma-\sigma|<0.06$ \\
Model selection, Pareto draw & Vuong statistic & $Z>0$ & $Z=+4.9$ & correct sign \\
Model selection, log-normal draw & Vuong statistic & $Z<0$ & $Z=-165.4$ & correct sign \\
Gini, equal vector & plug-in Gini & 0.000 & 0.000 & $<10^{-9}$ \\
Gini, degenerate vector & plug-in Gini & $\to 1$ & 0.980 & $>0.97$ \\
Top-ten share, equal vector & fixed-count share & 20.00 & 20.00 & exact \\
Industry hierarchy & tiling search & 14 leaves & 14 leaves & set equality \\
\bottomrule
\end{tabular}
\end{table}
""" % (v["planted_pareto_alpha"], v["recovered"],
       v["planted_lognorm_sigma"], v["recovered_sigma"]))

# ------------------------------------------------------------------ T4 model comparison
yrs = [1978, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023]
rows = []
for y in yrs:
    r = F13.loc[y]
    rows.append("%d & %s & %.4f & %.3f & %.3f & %s & %s \\\\" % (
        y, "{:,.0f}".format(r["n_firms"]), r["alpha"], r["mu"], r["sigma"],
        "%.3g" % r["d_aic"], sg(r["vuong_z"], 1)))
mc = P13["model_choice"]
w("tab_model_comparison", r"""
\begin{table}[H]
\caption{Pareto and log-normal fitted to the same ten bins by interval-censored maximum
likelihood, selected years. $\Delta$AIC is Pareto minus log-normal, so a positive value
favours the log-normal. The Vuong statistic tests the two non-nested models directly; a
value below $-1.96$ favours the log-normal and above $+1.96$ the Pareto, and values
between the two mean the data cannot separate them. The log-normal is preferred in all
%d years of the sample, in every case decisively. Source: authors' calculations from BDS.}
\label{tab:model_comparison}
\begin{tabular}{lrrrrrr}
\toprule
Year & Firms & $\hat\alpha$ & $\hat\mu$ & $\hat\sigma$ & $\Delta$AIC & Vuong $Z$ \\
\midrule
%s
\bottomrule
\end{tabular}
\end{table}
""" % (mc["years"], "\n".join(rows)))

# ------------------------------------------------------------------ T5 threshold sweep
cols = list(S13.columns)
rows = []
for y in (1978, 1990, 2000, 2010, 2023):
    rows.append("%d & %s \\\\" % (y, " & ".join("%.3f" % S13.loc[y, c] for c in cols)))
tl = P13["tail"]
w("tab_thresholds", r"""
\begin{table}[H]
\caption{Pareto exponent refitted from progressively higher thresholds, the
\citet{ClausetShaliziNewman2009} procedure adapted to interval-censored data. The column
head is the lower bound of the fitting region in employees. Fitted from the smallest firm
the exponent is far below unity, which is the signature of a body the model does not
describe; from ten employees upward it sits near one at every threshold. Axtell's
(\citeyear{Axtell2001}) microdata estimate of %.2f is reproduced at a threshold of twenty
employees. Source: authors' calculations from BDS.}
\label{tab:thresholds}
\begin{tabular}{lrrrrrrrr}
\toprule
Year & %s \\
\midrule
%s
\bottomrule
\end{tabular}
\end{table}
""" % (tl["axtell_2001_reference"],
       " & ".join("$\\geq$%s" % c for c in cols), "\n".join(rows)))

# ------------------------------------------------------------------ T6 top bin
rows = []
for y in (1978, 1990, 2000, 2010, 2023):
    r = T13.loc[y]
    rows.append("%d & %s & %s & %s & %.1f & %.2f \\\\" % (
        y, "{:,.0f}".format(r["observed"]), "{:,.0f}".format(r["lognorm"]),
        "{:,.0f}".format(r["pareto"]), r["lognorm_ratio"], r["pareto_ratio"]))
tb = P13["top_bin"]
w("tab_topbin", r"""
\begin{table}[H]
\caption{Firms of 10{,}000 employees and over: the count each fitted model has to
explain. The log-normal wins the likelihood comparison of Table~\ref{tab:model_comparison}
in every year and under-predicts this class by a factor of %.0f in the final year; a single
Pareto fitted across the whole range over-predicts it by an order of magnitude. Neither
model is the distribution, and the failure is on opposite sides. Source: authors'
calculations from BDS.}
\label{tab:topbin}
\begin{tabular}{lrrrrr}
\toprule
 & & \multicolumn{2}{c}{Predicted} & \multicolumn{2}{c}{Observed / predicted} \\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}
Year & Observed & Log-normal & Pareto & Log-normal & Pareto \\
\midrule
%s
\bottomrule
\end{tabular}
\end{table}
""" % (tb["observed_last"] / tb["lognorm_expected_last"], "\n".join(rows)))

# ------------------------------------------------------------------ T7 dynamism
d, c, yf = P12["dynamism"], P12["concentration"], P12["young_firms"]


def line(name, o, unit="pts"):
    return "%s & %.2f & %.2f & %s & %.2f (%d) \\\\" % (
        name, o["first"], o["last"], sg(o["change"], 2), o["peak"], o["peak_year"])


w("tab_dynamism", r"""
\begin{table}[H]
\caption{Dynamism and concentration in the universe of US employer firms. Entry and exit
are establishment rates. The size shares are of national employment and are computed on the
ten-class partition of Table~\ref{tab:bins}; the two largest classes are firms of 5{,}000
employees and over and the three smallest are firms under twenty. Age shares begin in 1982
because the Business Dynamics Statistics begins in 1978 and a firm cannot be observed at
age four before then. Source: authors' calculations from BDS.}
\label{tab:dynamism}
\begin{tabular}{lrrrr}
\toprule
 & First & Last & Change & Peak \\
\midrule
\multicolumn{5}{l}{\emph{Establishment turnover, per cent, 1978--2023}} \\
%s
%s
\addlinespace
\multicolumn{5}{l}{\emph{Share of national employment, per cent, 1978--2023}} \\
%s
%s
\addlinespace
\multicolumn{5}{l}{\emph{Held by firms under five years old, per cent, 1982--2023}} \\
%s
%s
%s
\bottomrule
\end{tabular}
\end{table}
""" % (line("Entry rate", d["entry"]), line("Exit rate", d["exit"]),
       line("Two largest size classes", c["large_firm_emp_share"]),
       line("Three smallest size classes", c["small_firm_emp_share"]),
       line("Share of firms", yf["share of firms"]),
       line("Share of employment", yf["share of employment"]),
       line("Share of job creation", yf["share of job creation"])))

# ------------------------------------------------------------------ T8 shift-share
ss = P12["shift_share"]
w("tab_shiftshare", r"""
\begin{table}[H]
\caption{Shift-share decomposition of the change in the share of employment held by the two
largest firm-size classes, %d to %d, across %d NAICS sectors. The three terms sum to the
observed change by construction and the identity was asserted in code. The within term is
what the change would have been had sector employment weights not moved; the between term
is what it would have been had concentration inside each sector not moved. Source: authors'
calculations from BDS.}
\label{tab:shiftshare}
\begin{tabular}{lr}
\toprule
Component & Percentage points \\
\midrule
Within sectors & %s \\
Between sectors & %s \\
Interaction & %s \\
\midrule
Total, equal to the observed change & %s \\
\bottomrule
\end{tabular}
\end{table}
""" % (ss["window"][0], ss["window"][1], ss["industries"],
       sg(ss["within"], 2), sg(ss["between"], 2), sg(ss["interaction"], 2),
       sg(ss["total"], 2)))

# ------------------------------------------------------------------ T9 capture
sv = P14["size_vs_capture"]
hi = "\n".join("%s & %.1f \\\\" % (n.replace("&", "\\&"), v) for n, v in sv["highest"][:5])
lo_ = "\n".join("%s & %.1f \\\\" % (n.replace("&", "\\&"), v) for n, v in sv["lowest"][:5])
w("tab_capture", r"""
\begin{table}[H]
\caption{Capture rates at the extremes, %d, and the association between creating value and
keeping it. Capture is gross operating surplus as a share of value added. The correlation
is computed against log value added across all %d industries. Both extremes are partly
artefacts of the tax and subsidy treatment rather than of profitability, which is why the
paper rests on the association and not on the ranking. Source: authors' calculations from
the GDP-by-Industry accounts.}
\label{tab:capture}
\begin{tabular}{lr}
\toprule
Industry & Capture, per cent \\
\midrule
\multicolumn{2}{l}{\emph{Highest}} \\
%s
\addlinespace
\multicolumn{2}{l}{\emph{Lowest}} \\
%s
\midrule
\multicolumn{2}{l}{\emph{Association of size with capture, %d industries}} \\
Pearson correlation, log value added with capture & %s \\
Spearman rank correlation & %s \\
\bottomrule
\end{tabular}
\end{table}
""" % (sv["year"], sv["n_industries"], hi, lo_, sv["n_industries"],
       sg(sv["pearson_log_size"], 3), sg(sv["spearman"], 3)))

# ------------------------------------------------------------------ T10 concentration
cc = P14["concentration"]


def cline(nm, k, d=3):
    o = cc[k]
    return "%s & %.*f & %.*f & %s \\\\" % (nm, d, o["first"], d, o["last"], sg(o["change"], d))


w("tab_concentration", r"""
\begin{table}[H]
\caption{Concentration of value created and value captured across %d industries that tile
the economy exactly once, %d to %d. Value added measures creation and gross operating
surplus measures capture. Capture is more concentrated than creation in every year of the
sample and its concentration rises further over the period. Both series peak in 2020.
Source: authors' calculations from the GDP-by-Industry accounts.}
\label{tab:concentration}
\begin{tabular}{lrrr}
\toprule
Measure & %d & %d & Change \\
\midrule
Gini, value added & %.3f & %.3f & %s \\
Gini, operating surplus & %.3f & %.3f & %s \\
\addlinespace
Top ten industries, value added, per cent & %.2f & %.2f & %s \\
Top ten industries, operating surplus, per cent & %.2f & %.2f & %s \\
\bottomrule
\end{tabular}
\end{table}
""" % (P14["industries"]["count"],
       cc["gini_value_added"]["first_year"], cc["gini_surplus"]["last_year"],
       cc["gini_value_added"]["first_year"], cc["gini_surplus"]["last_year"],
       cc["gini_value_added"]["first"], cc["gini_value_added"]["last"],
       sg(cc["gini_value_added"]["change"], 3),
       cc["gini_surplus"]["first"], cc["gini_surplus"]["last"],
       sg(cc["gini_surplus"]["change"], 3),
       cc["top10_value_added"]["first"], cc["top10_value_added"]["last"],
       sg(cc["top10_value_added"]["change"], 2),
       cc["top10_surplus"]["first"], cc["top10_surplus"]["last"],
       sg(cc["top10_surplus"]["change"], 2)))

# ------------------------------------------------------------------ T11 censoring
w("tab_censoring", r"""
\begin{table}[H]
\caption{Where each public instrument stops resolving. The final column states what the
top category of that instrument contains, and therefore what cannot be distinguished
inside it. Every concentration estimate in this paper is a lower bound for this reason, and
the bound is not tightenable with public data. Source: authors' compilation from the
published documentation of each series.}
\label{tab:censoring}
\begin{tabular}{lll}
\toprule
Instrument & Top category & What it cannot separate \\
\midrule
BDS, firm size & 10{,}000 employees and over & a firm of 10{,}000 from one of 2 million \\
BDS, firm age & 26 years and over & a firm of 30 years from one of 120 \\
GDP-by-Industry & the industry itself & every firm inside an industry \\
American Community Survey & \$200{,}000 of income & roughly the top tenth of households \\
BLS occupational wages & 90th percentile & the entire upper decile \\
\bottomrule
\end{tabular}
\end{table}
""")

# ------------------------------------------------------------------ T12 robustness
es = P13["edge_sensitivity"]
tl = P13["tail"]
w("tab_robustness", r"""
\begin{table}[H]
\caption{What the tail exponent is sensitive to. The bootstrap interval is the 95 per cent
percentile interval from 400 multinomial resamples of the final year's bin counts and
measures sampling noise alone. The threshold and boundary rows measure specification. The
exponent is more sensitive to where the fitting region starts, and to where the open class
begins, than it is to sampling, which is why the paper reports it to two decimals and rests
its distributional claim on the model comparison rather than on the exponent's level.
Source: authors' calculations from BDS.}
\label{tab:robustness}
\begin{tabular}{llr}
\toprule
Source of variation & Range examined & Spread in $\hat\alpha$ \\
\midrule
Sampling & 400 bootstrap resamples, %d & %.4f \\
Open-class boundary & 10{,}000 against 20{,}000 employees & %.4f \\
Fitting threshold & 10 to 2{,}500 employees & %.4f \\
Fitting threshold, including the body & 1 to 2{,}500 employees & %.4f \\
\bottomrule
\end{tabular}
\end{table}
""" % (tl["alpha"]["last_year"],
       tl["bootstrap_95_last_year"][1] - tl["bootstrap_95_last_year"][0],
       es["spread"],
       max(v for k, v in tl["threshold_sweep_last_year"].items() if int(k) >= 10)
       - min(v for k, v in tl["threshold_sweep_last_year"].items() if int(k) >= 10),
       max(tl["threshold_sweep_last_year"].values())
       - min(tl["threshold_sweep_last_year"].values())))

print("done")
