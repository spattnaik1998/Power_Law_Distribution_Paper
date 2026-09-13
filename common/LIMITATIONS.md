# Limitations register

Every caveat raised in a technical summary, numbered for use as endnotes in the
article. Stable IDs: the number never changes once assigned, so prose can cite
`L3.2` and stay correct as the register grows. Each entry states what the
limitation is and what it forbids the article from claiming.

---

## Idea 1 - The Second Half of the Chessboard

**L1.1 Hedonic price indexes are model estimates, not observations.**
BEA infers quality adjustment from a statistical model of product
characteristics. Byrne, Oliner and Sichel have argued that the post-2004
computer deflator understates real quality improvement. If they are right, part
of the measured flattening after 2005 is a measurement failure rather than a
technology failure. *Forbids:* "progress slowed." *Permits:* "the measured rate
of price decline slowed."

**L1.2 The category is narrower than "computing."**
BEA line 11 prices computers and peripheral equipment purchased as domestic
business investment. It excludes cloud capacity bought as an operating expense,
semiconductors embedded in other products, and the compute used to train models.
A firm that stopped buying servers and started renting them moved its spending
out of the index, which would produce the observed flattening on its own.
*Forbids:* treating the series as the price of all computing.

**L1.3 Investment prices describe purchases, not the frontier.**
The index prices what businesses bought, weighted by what they bought. It says
nothing about the best machine available in a given year. *Forbids:* inferring
anything about frontier capability from the price series.

**L1.4 The demand elasticity in Figure 5 is descriptive.**
The scatter plots equilibrium outcomes, not an identified demand curve. Supply
moved across the same period. *Forbids:* calling the fitted slope an elasticity
without qualification.

---

## Idea 2 - Innovation: Declining or Recombining?

**L2.1 TFP is a residual, so measurement error lands inside it.**
Total factor productivity is whatever output growth remains after measured
labour and capital are accounted for. Every gap in the national accounts,
including the ones Idea 4 is about, shows up here. If the accounts undercount
output from digital goods, they undercount TFP, and research productivity falls
for reasons unrelated to ideas. *Forbids:* reading falling TFP as direct evidence
about the supply of ideas.

**L2.2 The research productivity level depends heavily on the base year.**
The series is indexed to 1964, at the end of an unusually strong decade for TFP.
A different base changes the headline percentage substantially. The direction and
the shape survive that choice; the figure "2 percent of its 1964 level" does not.
*Permits:* quoting the direction and the order of magnitude only.

**L2.3 The ratio is coarser than the published literature's.**
Bloom, Jones, Van Reenen and Webb divide by researcher counts, domain by domain.
This divides by real R&D investment for the whole economy. *Forbids:* citing this
as a replication of their result.

**L2.4 Business investment is not all research.**
Federal basic research and university work enter these series unevenly, and both
were a larger share of the national total in the 1960s than now. Part of the
early decline may be composition rather than efficiency.

**L2.5 Denominator growth dominates the ratio.**
Real R&D investment rose twelvefold while TFP growth stayed within a narrow band,
so the ratio falls largely because its denominator grows. This is the finding
rather than an artefact, but the series is close to an inverted picture of
research spending, and should not be described as an independent measurement.

**L2.6 Figure 5 is arithmetic, not evidence.**
The combinatorial curves are a property of counting, true regardless of what any
economy does. *Forbids:* presenting it as support for the recombination view.

---

## Idea 3 - The GPT Lag

**L3.1 The lag could not be recovered from aggregate data.**
The differenced correlation peaks at twelve years at r = 0.20, which is not
distinguishable from noise (p = 0.16 before any correction), and the placebo
capital series peaks at r = 0.165. *Forbids:* quoting a specific lag length as an
empirical result of this work. *Permits:* reporting the test and its null.

**L3.2 The levels result is the one to distrust, despite looking better.**
Correlating two trending series manufactures significance. Validation on
synthetic data with a planted fourteen-year lag showed the differenced method
recovering fourteen exactly while the levels method returned a confident and
wrong three. The levels peak of r = 0.33 at nine years is therefore reported and
discarded.

**L3.3 Smoothing destroys most of the effective sample.**
The five-year average applied to TFP growth removes noise and also removes
independent observations. Fifty annual observations carry roughly ten
independent ones, and no result in this notebook survives that correction.

**L3.4 The electrification comparison uses a substitute that does not work.**
US labour productivity before 1947 is not available from BEA, BLS or FRED, so
Figure 2 uses the Federal Reserve industrial production index from 1919, which
measures output rather than productivity. Its shape is dominated by the
Depression at year 13 and by war mobilisation at years 21 to 25. *Forbids:* using
Figure 2 as evidence about electrification's payoff. Rebuilding the book's
Figure 7.2 properly requires Kendrick's series from a library source.

**L3.5 Correlation over seventy annual observations cannot identify causation.**
Two heavily autocorrelated aggregate series, no instrument, no control for the
business cycle. The exercise can rule a lag out of the aggregate data. It cannot
establish one.

---

## Idea 4 - Beyond GDP

**L4.1 The surplus figures are an assumption wearing a number.**
Everything in Figure 3 scales as 1/(elasticity − 1), and that elasticity is not
observed. At 1.1 the implied surplus is ten times expenditure; at or below 1 the
integral does not converge at all. *Forbids:* quoting a point estimate for the
surplus on information technology. *Permits:* the range and its sensitivity.

**L4.2 The computable surplus is on the wrong side of the economy.**
It accrues to firms buying equipment, not to households using free services. It
is included because it is the side of the economy that has prices, which is
itself the point being made.

**L4.3 The inversion is arithmetic, not evidence.**
Figure 4 says what unpriced services would have to be worth to move measured
growth. It does not say what they are worth. Its value is converting an
unfalsifiable claim into a figure a reader can weigh against their own use.

**L4.4 GDP was never built to measure welfare.**
Kuznets said so when he constructed it. Criticising it for failing at a job it
does not claim is the weakest form of this chapter's argument. *Permits:* the
narrower and stronger claim, that the accounts mismeasure *production* when
output moves to zero-price channels.

**L4.5 The revision dates mark counting, not existence.**
BEA back-cast software, R&D and artistic originals through the whole historical
period when it capitalised them, so the series in Figure 1 run before the dates
marked. The vertical lines are when the accounts began counting these as
investment, not when the spending began.

**L4.6 A units error was found and corrected in this notebook.**
BEA NIPA values arrive in millions of dollars and FRED GDP in billions. The
first run divided one by the other and inflated every share by a factor of 1000.
The notebook now carries an assertion that private fixed investment computes to
between 10 and 30 per cent of GDP. Any figure quoted from a run before that
guard existed should be re-checked.

---

## Idea 5 - The Bounty and the Spread

**L5.1 The book's headline claim about 1999 no longer holds.**
The notes record 1999 as the peak year for real median household income. That
was true when the book was written, from data ending shortly after the financial
crisis. It is no longer true: 2007 exceeded 1999, every year from 2015 onward
exceeded it, and the series peaks in 2024 about 16 per cent above the 1999
level. *Forbids:* repeating the 1999 peak as a current fact. *Permits:* stating
it as what the data showed in 2014, and reporting what changed.

**L5.2 The spread is relative, not absolute.**
Real median household income has risen. It has risen far more slowly than output
per person, roughly 39 per cent against 101 per cent since 1984. The defensible
claim is divergence, not decline.

**L5.3 Households are not workers.**
Median household income moves with household size, the number of earners per
household, and taxes and transfers. Part of the flatness in Figure 1 is
demographic rather than about pay.

**L5.4 Compensation is not wages.**
The compensation series includes employer contributions to health insurance and
pensions, which grew faster than cash pay. A worker can receive more
compensation and less money.

**L5.5 The deflator choice decides most of the answer, and it is a real choice.**
About 61 per cent of the headline productivity-pay gap comes from deflating pay
by consumer prices while deflating output by producer prices. Consumer prices
are the right deflator for asking what workers can buy; output prices are the
right one for asking whether pay tracks production. *Forbids:* citing the
headline gap without saying which question is being asked.

**L5.6 The earnings-by-education figure was withdrawn as mislabelled.**
The FRED identifiers used for Figure 4 did not match the labels put on them: the
line called "bachelor's and higher" plotted below the line called "less than
high school", which is impossible. The series were guessed rather than looked
up. `stacklib.fred_titles` now exists to fetch official titles for labelling,
and the figure is excluded from the technical summary until it is rebuilt.

**L5.7 CPS earnings series begin in 2000.**
Even relabelled, these cannot reproduce Acemoglu and Autor's 1962-2008 chart.
They describe the post-2000 period only, which is a different and narrower
claim than the one in the notes.

---

## Idea 6 - The Functional Distribution

**L6.1 GDP is strictly the wrong denominator.**
It includes depreciation and taxes on production, neither of which is available
to pay anyone. Net domestic product or business-sector value added would be
cleaner and would move the level by several points. The trend is much less
affected than the level.

**L6.2 The proprietors' assumption changes the level by seven points.**
Counting none of the self-employed's earnings as labour puts the 2024 share at
51.3 per cent; counting all of it puts it at 58.2; Gollin's proportional
adjustment gives 55.1. All three decline by a similar amount, so the trend is
robust, but the article must name which construction any level it quotes comes
from.

**L6.3 The labour share figure is rescaled, not published.**
BLS publishes an index, not a percentage. Figure 1 places that index on a share
basis using its own pre-2000 mean and the 64.3 per cent figure from Fleck,
Glaser and Sprague. The shape is the data; the level is a construction.

**L6.4 Corporate profits are not the mirror of the labour share.**
They are measured after tax, include earnings from abroad, and cover only the
corporate sector. The two lines in Figure 3 are not required to sum to anything,
and their gap is not a residual anyone receives.

**L6.5 The Penn World Table pads its early years.**
Germany, Japan and the United Kingdom each carry their first observed value
backwards as a constant, producing thirty, twenty and twenty years of invented
flat history. Those years were removed before plotting. Any international
comparison drawn straight from FRED without this trim shows a false postwar
plateau.

**L6.6 Japan is the exception, and how it looks depends on the start date.**
Measured from each country's own peak, all four economies show a declining
labour share. Measured from the first year of data, Japan rises about eight
points, because its 1970 starting value was unusually low. State which
comparison is being made.

**L6.7 Figure 5 is the correlation Idea 3 warned about.**
Two trending series over seventy-eight years, r = 0.80, no instrument and no
control. The same standard that produced a null in Idea 3 applies here. The
result is consistent with the Karabarbounis-Neiman mechanism and cannot confirm it.

**L6.8 Rognlie's objection is untested.**
He argues capital's gain is concentrated in housing rather than in productive
capital, which would sever the link to automation. Testing it needs a housing
split this notebook does not attempt.

---

## Idea 7 - Stars, Superstars and the Power Law

**L7.1 The power law claim could not be tested, and the test that ran failed.**
Fitting the observed tail as a power law returns an R-squared of 0.962. The same
test run on a fitted log-normal, which is not a power law by construction,
returns 0.981. The real data fits a power law *worse* than a non-power-law
benchmark does. *Forbids:* saying the data show a power law in the American
income distribution. *Permits:* saying the public bracketed data cannot
distinguish the two, and that the log-normal is the better description over the
range they resolve.

**L7.2 The superstar region is inside the last bracket.**
ACS stops at "$200,000 or more", roughly the 90th percentile. The chapter's
argument is about the top fraction of one per cent. Every number above $200,000
in Figure 3 is extrapolation from a fitted curve, not a count of anybody.

**L7.3 The fitted exponent is not credible on its own.**
The tail fit returns alpha near 1.2, which would imply an almost undefined mean.
It is low because the fit starts at $50,000, where the distribution is still in
its log-normal body. A defensible exponent needs tail data this source lacks.

**L7.4 The observed top bracket is thinner than a log-normal predicts, not fatter.**
Observed 12.4 per cent of households above $200,000 against 15.7 per cent
predicted. Taken at face value this is the opposite of a fat tail. The
established explanation is survey under-reporting at the top, which is precisely
why tax-based sources are used for this question.

**L7.5 Households are not people, and income excludes capital gains.**
B19001 counts household money income before taxes and omits realised capital
gains, which is a large share of income at the top.

**L7.6 Bracket widths are unequal and were normalised.**
The brackets run $5,000 wide at the bottom and $50,000 at the top. Figure 1 is a
density, share per $1,000 of income; a plot of raw bracket shares would make the
wide upper brackets look populous purely because they are wide.

**L7.7 The wage dispersion figure did not run.**
No FRED earnings-percentile series passed title verification, so the
between-jobs against within-jobs question is unanswered. The guard behaved
correctly by refusing rather than mislabelling.

---

## Idea 8 - Polanyi's Paradox and the Moving Frontier

**L8.1 The task classification is a judgement, and it barely clears its own test.**
Occupation groups were assigned to Autor's quadrants by hand, using keyword rules
printed in full by the notebook. A permutation test shuffling those labels two
thousand times returns p = 0.018, so the classification carries information, but
about one random classification in fifty separates the trends as well. *Permits:*
reporting the quadrant pattern with the p-value attached. *Forbids:* treating the
quadrants as measurement.

**L8.2 The late window is the pandemic.**
The "after" period is 2019 to 2023. Non-routine manual work is food preparation,
personal care and building cleaning, which is precisely what COVID shut down.
Attributing the turn in that quadrant to machine learning requires an argument
this notebook does not supply, and the pandemic explanation is simpler.

**L8.3 Occupations are not tasks.**
Autor's own claim is that automation replaces tasks within jobs. An occupation
can hold its headcount while most of its work changes. Occupation counts cannot
see that at all, so this evidence speaks to job displacement, never to task
displacement.

**L8.4 ACS lumps management with business and financial operations.**
At the level of the tree that partitions total employment, these are one group.
Management belongs in the non-routine zone and business and financial operations
arguably in the routine-cognitive one, and the whole bundle was assigned to
non-routine cognitive. This biases against finding routine-cognitive decline, so
the measured decline is a floor rather than an estimate.

**L8.5 Nominal earnings inverted the reading and were corrected.**
The notebook's Figure 4 plotted nominal median earnings, which rose for every
occupation because consumer prices rose about 40 per cent across the window. The
technical summary redraws it in real terms. Any statement made from the nominal
version is wrong in sign for most groups.

**L8.6 Employment shares are composition, not level.**
A share falls when one category shrinks or when others grow. Total employment
also rose across the period. Check the underlying counts before saying a kind of
work is disappearing.

**L8.7 The 2010-2023 employment series has no 2020 observation.**
The Census Bureau did not release standard ACS one-year estimates for 2020
because pandemic collection failures made them unrepresentative. Figure 1 now
breaks at that year and shades it. An earlier draft drew a straight segment from
2019 to 2021, which invents a trajectory through the sharpest labour-market
dislocation in the sample.

*Forbids:* reading any year-on-year change across 2019-2021 off the chart.
*Permits:* comparing the 2010-2014 and 2019-2023 windows, which is how the
trends in this idea are computed.

**L9.1 The devices got cheap; the content did not.**
Telephone and communication equipment fell 13.3 percent a year from 2000 to
2025 and personal computers 9.8 percent, both inside the fastest half-percent of
398 consumption categories. Recorded music fell 0.6 percent a year and
newspapers and magazines rose 2.3 percent, near the middle of the basket.

*Forbids:* writing that digital goods became free. What became free was the
copy.
*Permits:* the claim that no other category of American consumption has price
behaviour resembling information hardware.

**L9.2 Figure 5 was withdrawn: the employment series were state, not national.**
The FRED search filtered candidate titles on industry words but not on national
coverage, so "Newspaper publishers" resolved to Massachusetts and "Software
publishers" to California. Only the Information sector aggregate was national.

*Forbids:* quoting any newspaper, software or motion-picture employment number
from that run.
*Permits:* the Information sector total, 3.63 million in 2000 against 2.86
million in 2025.

**L9.3 The recorded-music quantity series excludes streaming, so it cannot test
Waldfogel.** BEA's line is "Audio discs, tapes, vinyl, and permanent digital
downloads." Subscription listening sits in a different line, which is where the
consumption went. The 81 percent fall in real quantity after 1999 is the
collapse of music ownership, not of music consumption.

*Forbids:* citing that figure on whether the supply or consumption of music
held up after Napster.
*Permits:* describing the disappearance of purchased recordings.

**L9.4 Spending is measured as a share of all consumption.**
This removes inflation and population growth without choosing a deflator, but
it means every line moves when the denominator moves. A category can lose share
while its real level is flat.

*Forbids:* reading the media lines as dollar amounts per household.
*Permits:* comparisons between the lines and the crossings between them.

**L10.1 The demand relationship is cross-sectional, not causal.**
The slope of 0.88 compares categories to each other over one 25-year window. It
says nothing about what any single category would have done at a different
price, and it cannot separate demand response from supply-side technical change
that lowers price and raises quantity at once.

*Forbids:* calling 0.88 an elasticity, or reading it as what would happen if a
given price were cut.
*Permits:* the statement that categories with steeper price declines saw larger
quantity growth, and that a shuffle does not reproduce it.

**L10.2 BEA's detail table nests subtotals inside their own components.**
"Information processing equipment" appears as a line and so do the personal
computers inside it, so a fast-falling family enters the cloud several times.
Forty-three named aggregates were excluded; seven further intermediate
subtotals were identified by hand.

*Forbids:* treating the 355 categories as a partition of consumption or summing
anything across them.
*Permits:* the slope, which moves only from 0.88 to 0.84 when the seven are
dropped, with a bootstrap interval of 0.66 to 1.05.

**L10.3 The complement pairs are described, not tested.**
Idea 3 showed that two trending aggregates produce a respectable correlation for
no reason at all, and no placebo exists for a named pair. Falling device prices
beside rising service quantities are consistent with the mechanism and cannot
confirm it.

*Forbids:* claiming cheap devices caused service consumption to rise.
*Permits:* reporting the two movements and their sizes.

**L10.4 Freemium, cannibalisation and two-sided pricing are untested.**
Nothing in the public accounts distinguishes a free tier from a paid one, or one
side of a platform from the other. The chapter's strategic claims about
subsidising a side are outside what these data can reach.

*Forbids:* citing this notebook on whether free tiers cannibalise paid ones.
*Permits:* the surplus geometry, which is arithmetic and labelled as such.

**L11.1 The title assertion is only as strong as the words given to it.**
Section E asked for a consumer price index for "services" and resolved to
Medical Care Services, which contains the word and is not the series wanted. The
guard fired correctly and the request was wrong. Expect-words must be specific
enough that only the intended series can satisfy them.

*Forbids:* quoting anything labelled "All services" from this run.
*Permits:* the load factor and e-commerce series, whose titles are unambiguous.

**L11.2 Section E produced no figure and the lodging question is unanswered.**
Only one of three price series resolved, so the placebo design never ran. The
Zervas and Proserpio result stays literature: Airbnb cut Austin hotel revenue by
10 percent over five years, concentrated in lower-priced hotels and those not
serving business travellers.

*Forbids:* any claim about hotel prices from this notebook.
*Permits:* citing the Austin study, and the point it implies, that the question
is never whether a platform displaces an industry but which segments it
substitutes for and what share of profit sits there.

**L11.3 Electronic shopping and department store employment did not resolve.**
The e-commerce displacement figure was built without them. The share of retail
sold electronically, 0.9 percent in 2000 against 16.4 percent in 2025, is sound;
the employment counterpart is missing.

*Forbids:* stating how many retail jobs moved between formats.
*Permits:* the sales share, and accommodation employment, which did resolve.

**L11.4 Figures 3 and 4 are simulations, not measurements.**
The extrapolation loss and the negative-price threshold are properties of the
assumed functional forms, not estimates from data. Both were validated against
closed-form answers before use: exponential demand is revenue-maximised at its
decay constant, and the two-sided problem at zero cross-elasticity separates into
two monopoly problems.

*Forbids:* reporting 46 percent, 72 percent or a crossing at 0.57 as findings
about any real market.
*Permits:* using them to show the shape and direction of the argument, labelled
as arithmetic, in the way Idea 2's combinatorics figure was labelled.

---

## Idea 12 - Dynamism and Concentration

**L12.1 The class labels were unreachable, and the partitions were identified by
arithmetic.** The Census code-list endpoint returned nothing from either machine,
so the size and age classes carry raw numeric codes rather than names. BDS also
publishes totals and intermediate subtotals inside the same dimension as their
own components. The partition used here is the largest set of classes summing to
the national total in every year; on both dimensions it reconciles to 0.0000
percent, and the method was validated against a constructed table with a planted
total and subtotal before it was trusted. It recovers 10 size classes from 14 and
12 age classes from 15.

*Superseded in part by Idea 13.* The label variable `EMPSZFI_LABEL` resolved on the
second attempt and names all ten size classes. Every inferred edge was correct. The
size classes may therefore be named in the prose; the age classes may not, since
`FAGE_LABEL` has not been retrieved.

*Forbids:* naming a size or age class in the prose by its employment range.
*Permits:* "the two largest firm classes", "firms under five years old", and any
comparison of ordered classes, since the codes ascend with size and with age.

**L12.2 The largest class is open-ended.** BDS tops out at firms of 10,000
employees and over. Every instrument in this project censors the top, and this is
that ceiling in its business-side form: the distance between a firm of 10,000 and
a firm of two million is invisible.

*Forbids:* any statement about the very largest firms as against the merely
large, or any tail exponent read off these classes without an interval-censored
estimator.
*Permits:* the share of employment held by the top two classes as a lower bound
on concentration.

**L12.3 The unit is employment, not revenue or profit.** Concentration measured
by headcount understates the digital cases the article cares about most, where a
firm captures a large share of a market with few employees.

*Forbids:* reading the concentration series as a measure of market power or of
value captured.
*Permits:* it as a measure of where Americans work.

**L12.4 The class HHI is a bound, not the index.** Computed on ten grouped
classes rather than on firms. Grouping can only lower a Herfindahl, so 0.1406 in
1978 and 0.1572 in 2023 are floors, and the change between them is not the change
in the firm-level index.

*Forbids:* comparing these values to any published HHI or to a regulatory
threshold.
*Permits:* the direction, and the statement that concentration rose.

**L12.5 The firm-age series begins in 1982, not 1978.** BDS starts in 1978, so no
firm can be observed at age four before 1982, and every firm that already existed
sits in a left-censored class holding 93.0 percent of employment in the first
year. Shares before 1982 are not comparable with later ones.

*Forbids:* extending any young-firm share back to 1978, or citing a 1978 base for
the startup decline.
*Permits:* the 1982 to 2023 comparison, and the 1987-88 peaks.

**L12.6 The correlation between entry and concentration is description.** Entry
falls and large-firm employment share rises across the same forty-six years,
correlating at -0.770. Two trending series. Idea 3 established on this project's
own data that a correlation of this kind can arise with no relationship at all.

*Forbids:* any causal reading, and any claim that falling entry produced rising
concentration or the reverse.
*Permits:* stating that the two moved together over the period.

**L12.7 The shift-share is a decomposition over forty-five years, not an
estimate.** Nineteen NAICS sectors, 1978 against 2023. The all-industry code 00
is published alongside the sectors and was excluded; left in, it carries roughly
half the weight and flattens the result. The identity holds exactly, at +6.25
within, -6.38 between and +5.66 interaction, summing to the +5.53 point change.
The interaction term is nearly as large as the within term, which is what a
window this long does to a decomposition of this kind.

*Forbids:* presenting the three terms as separable causes, or quoting the within
term as the amount of concentration attributable to industries concentrating.
*Permits:* the qualitative reading, that concentration rose inside industries
while employment moved toward less concentrated ones, and the industry-level
changes in the accompanying CSV.

**L12.8 Idea 12 does not test the power law.** Every quantity in it is a share or
a difference of shares. No distribution was fitted and no tail exponent
estimated.

*Forbids:* citing this idea as evidence for or against a power law in firm size.
*Permits:* it as evidence on dynamism and concentration, which are conditions
under which a power law would steepen, not tests of one.

---

## Idea 13 - The Shape of the Distribution

**L13.1 The fit is to ten bins, not to firms.** BDS publishes counts by size class,
so the likelihood is multinomial over intervals and nothing is assumed about where
inside a class a firm sits. This is the correct estimator for the data, and it is
not the estimator Axtell (2001) used: he had the firm-level Census microdata. The
comparison to his 1.06 is a comparison of a binned estimate to a microdata one.

*Forbids:* describing this as a replication of Axtell.
*Permits:* citing the agreement as independent corroboration on coarser data, and
noting that the exponent fitted from twenty employees upward, 1.056 in 2023, lands
on his estimate.

**L13.2 Ten bins are few, and the tail rests on one open class.** Nine interior
edges constrain the whole distribution, and everything above 10,000 employees
enters as a single number. The exponent is identifiable only because that class is
open, which is the same feature that makes it unverifiable from inside.

*Forbids:* any claim about the shape of the distribution above 10,000 employees, or
any statement distinguishing the largest firms from the merely very large.
*Permits:* the exponent as an estimate of the tail's weight, with its interval.

**L13.3 The bin edges were inferred before they were confirmed.** The run recorded
its edges as the arithmetic fallback because the parser did not recognise "or more"
as an open top class. The labels came back in the same call and are stored in the
payload; every one of the ten edges is identical to the inferred value, so no
number in this idea depends on the resolution. The parser is fixed.

*Forbids:* nothing.
*Permits:* stating that the class boundaries are the published Census ones.

**L13.4 One class mean falls outside its own class.** Firms of 5,000 to 9,999
employees average 4,656 over the full period. BDS assigns a firm to a size class on
employment in a reference year that need not be the year its employment is counted
in, which displaces means downward near the top. The other nine classes reconcile.

*Forbids:* using class means as if they were within-class averages of the counted
employment.
*Permits:* the fit, which uses counts and edges and never a class mean.

**L13.5 The log-normal wins on likelihood and fails at the top, and both are the
finding.** Vuong prefers the log-normal in all forty-six years, at a Z of about
-250. The same fitted log-normal expects 57 firms of 10,000 and over in 2023 where
1,210 exist, a factor of 21. A single Pareto has the opposite failure: it expects
11,916. Neither model is the distribution.

*Forbids:* reporting "the log-normal fits best" without the top-bin failure, or
"the firm-size distribution is a power law" without the body.
*Permits:* the mixed description - a log-normal body with a Pareto tail - which is
the same conclusion Idea 7 reached for incomes, now on a second and independent
instrument.

**L13.6 The tail exponent is more sensitive to the edges than to sampling.** Moving
the top class boundary by a factor of two moves the 2023 exponent by 0.047. The
bootstrap interval, which measures only sampling noise, is 0.026 wide. The
threshold sweep moves it further still: 1.056 fitted from twenty employees upward
against 0.952 from five hundred.

*Forbids:* quoting a tail exponent to three decimals, or comparing two of these
estimates as though the difference were measured.
*Permits:* the statement that the exponent sits near one across every threshold
above ten employees, which is the robust result.

**L13.7 The tail became lighter while employment concentrated.** The exponent above
500 employees rises from 0.897 in 1978 to 0.952 in 2023, a lighter tail, over the
same years in which Idea 12 found the large-firm employment share rising by 5.5
points. These measure different things - the count of firms by size against the
share of workers they employ - and are not in contradiction, but the article should
not treat either as evidence for the other.

*Forbids:* writing that firms became more unequal in size, or citing Idea 12's
concentration finding as a steepening power law.
*Permits:* both facts stated side by side, and the observation that concentration
of employment can rise while the size distribution flattens slightly.

---

## Idea 14 - Value Created and Value Captured

**L14.1 Gross operating surplus is not profit.** It is what remains of value added
after compensation and net taxes, and it also contains depreciation, net interest,
and the earnings of unincorporated proprietors, which Idea 6 established cannot be
cleanly split between labour and capital [L6.2]. Every capture rate here is an
upper bound on the profit share.

*Forbids:* quoting a capture rate as a profit margin, or comparing one to a
company's reported margin.
*Permits:* comparison across industries and over time on a consistent definition.

**L14.2 The unit is the industry, and the argument is about firms.** An industry
aggregate averages over the firms inside it, so the one firm capturing everything
and the twenty capturing nothing arrive as a single number. Concentration measured
between industries is a floor on concentration between firms and is not an
estimate of it.

*Forbids:* reading the Gini or the top-ten share as a measure of how concentrated
profit is among companies.
*Permits:* the direction and the comparison between creation and capture, both of
which are measured on the same unit.

**L14.3 The industry partition was recovered, not given.** The API returns rows
sorted by industry code, so BEA's display order - which is what encodes the
hierarchy - is lost, and groupings arrive mixed in with their own components. The
tree was rebuilt by size: working upward from the smallest column, a column is a
grouping if some set of currently unclaimed smaller columns reproduces it in every
year. Twenty-eight groupings resolved, the leaves were then taken by walking down
from GDP, and they reconcile to published GDP within 0.004 percent across
1997-2024. The result is BEA's standard 71-industry summary level.

*Forbids:* nothing about the results; the partition is verified.
*Permits:* stating that the analysis covers 71 industries that tile the economy
exactly once.

**L14.4 One published column is not an industry at all.** BEA's
information-and-communications-technology aggregate cuts across several branches
of the tree and is not even an exact sum of the industries published here - the
closest combination misses by about 51 billion dollars. Because it is reached from
no parent, taking the leaves downward from GDP excludes it; counted as an
industry, it inflated every denominator by six to seven percent.

*Forbids:* using any ICT figure from this dataset.
*Permits:* the 71-industry set, which excludes it by construction.

**L14.5 Value added over gross output is not capture.** It was carried as a second
measure and it does not behave like one: air transportation's ratio is 53 percent,
above many software industries, because the ratio tracks vertical integration -
how much an industry buys in - rather than what it keeps. The surplus share is the
measure the findings rest on.

*Forbids:* citing the value-added margin as evidence about profitability, in
either direction.
*Permits:* it as a description of an industry's reliance on purchased inputs, which
is a different and smaller claim.

**L14.6 Two extremes are subsidy and tax artefacts, not capture.** Surplus plus
compensation reaches 134 percent of value added for government enterprises and 129
percent for farms, because net taxes on production are negative where subsidies
are large; at the other end it falls to 20 percent for funds and trusts. Air
transportation's capture rate goes negative in 2002.

*Forbids:* reading the top and bottom of the 2024 ranking as a league table of
profitability.
*Permits:* the distribution as a whole, and the central finding, which does not
depend on the tails.

**L14.7 The null is the finding, and a null is not proof of absence.** Across 71
industries in 2024 the correlation between log value added and the capture rate is
0.009 by Pearson and -0.047 by Spearman. That is as close to no relationship as
this instrument can show, and it is what Thiel's argument predicts. It remains a
single cross-section on one definition of capture at one level of aggregation.

*Forbids:* stating that size and capture are unrelated as a general economic law.
*Permits:* the statement that in these accounts, in this year, how much an industry
creates says nothing about how much it keeps.

**L14.8 The concentration comparison is the strongest result and the narrowest.**
Between 1997 and 2024 the Gini of value added across industries rose from 0.512 to
0.551 and the Gini of operating surplus from 0.587 to 0.627; the top ten
industries' share of value added rose 3.1 points against 4.6 points for surplus.
Capture is both more concentrated than creation and concentrating faster. Both
series peak in 2020, so the endpoint matters.

*Forbids:* quoting the changes without noting the 2020 peak, or extending the
comparison to firms [L14.2].
*Permits:* the ordering, which holds in every year of the sample.

---

## How to use this file

Cite by ID in the draft, e.g. "the measured rate slowed [L1.1]". When an idea's
technical summary is written, its limitations are appended here in the same
session, so the register stays complete rather than reconstructed at the end.
