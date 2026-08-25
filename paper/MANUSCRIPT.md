# Who Must Agree: Empirical Sections

*Working conference draft. Every number traces to a committed results file
(script-to-results map in `analysis/ANALYSIS_REVIEW.md`). **[PENDING]** marks
claims held on a named data pass. The draft is frozen on corpus package v3.
Sections 1 to 3 (theory and institutional framework) are maintained
separately.*

---

## 4 · Data: observing the consent requirement end to end

The question of this paper is what a voter-approval requirement for local
borrowing actually does. Answering it requires seeing three things at once,
and no single dataset contains them. The first is the **rule**: which
governments must ask voters before borrowing, and what share of the vote they
need. The second is the **asking**: what governments put on the ballot, and
whether it passed. The third is the **borrowing**: what was ultimately
issued, for what purpose, and, critically, on whose authority. This section
describes how each is measured. Readers familiar with municipal finance data
can skim to Table 1, which summarises the samples; a full variable inventory
with sources and coverage is Appendix V.

**The referendum panel: 47,235 ballot measures.** Nine states publish
administrative registries of local bond and tax elections: California (the
CDIAC database), Texas (Bond Review Board), Wisconsin (Department of Public
Instruction), Louisiana (Secretary of State), North Carolina (State Board of
Elections), Massachusetts (Division of Local Services), Minnesota, Illinois
and Indiana. Compiled, these give 47,235 measures. Each measure is then
matched ("crosswalked") to its government in the Census of Governments, so
that election outcomes can be joined to that government's later borrowing:
40,924 measures (86.6%) resolve to a Census identifier, with the exact-match
tiers verified at close to 100% and the fuzzy-match tier independently
audited at 95.1% accuracy.

Not every measure is useful for causal analysis. The design of Section 6
needs measures where a statute, not a local choice, sets a pass threshold and
makes the ballot mandatory. Restricting to such measures leaves 23,577.
Restricting further to **general-obligation (GO) bond measures**, bonds
backed by the government's taxing power, which is the instrument statutes
typically make voters approve, leaves the analysis frame: **11,889 GO
measures** (Texas 8,062, California 2,189, Wisconsin 999, Louisiana 361,
North Carolina 278). These sit at three statutory thresholds: 50% (Texas,
Wisconsin, Louisiana, North Carolina), 55% (California school measures) and
66.7% (California non-school measures), with each Californian measure's
threshold taken from CDIAC. Two derived variables matter throughout:
`pct_yes`, the yes share of the vote, and the **running variable**,
`pct_yes` minus the threshold that applied to that measure, so that zero
always marks the pass/fail line.

[[EX:T1_sample]]

**The outcome of record: the official-statement corpus.** When a local
government sells bonds publicly, it files an official statement, a disclosure
document describing the issue. The corpus assembled here contains **258,762
official statements** covering 2005 to 2025, all fifty states and 43,030
issuers. From each document are extracted the par amount, the security class
(GO, revenue, lease, special tax), the use-of-proceeds lines classified into
118 functional activities, and the variable the paper turns on: the
**authorisation mode the document itself evidences**. An official statement
states the legal authority for the issue, so each issue can be coded as
authorised by voters (usually with the election date cited), by the governing
board, or by statute. This is the richest available measure of what was
borrowed, for what, and on whose authority, and every headline claim about
provision (issuance, channel, purpose, project continuation) rests on it.

Census survey data enter in exactly two supporting roles, each a single table
row. The Government Finance Database debt items (1967 to 2023, 2.1 million
local unit-years) provide a survivorship check: the corpus only sees publicly
sold debt, the survey also counts bank loans and private placements, so
finding the same effect in both rules out the concern that refused
governments simply borrow off-market. The survey capital-outlay items provide
a bound on the one channel the corpus cannot see by construction: building
without borrowing (the pay-go bound, Section 6). Neither use displaces the
corpus as the outcome of record.

**Validating the extracted authorisation mode.** Because the authorisation
mode is read out of documents rather than taken from an administrative
source, it is checked against the election record before use. Where an
official statement cites an election date, that date matches an independently
observed referendum for the same government 67.9% of the time pooled, and
95.4% in Wisconsin, the one state whose registry is known to be complete;
conditional on a match, 91.3% of cited elections are passed measures (98.0%
in California, 98.8% in North Carolina). The shortfalls sit exactly where
registry coverage is known to be short: Minnesota's registry begins in 2020,
and Massachusetts records votes at month grain. A related check runs the
other way: 76.2% of voter-mode new-money documents have a passed referendum
within the previous six years in the records, and the gap is driven by
authorisations older than the observation window (Texas districts routinely
issue against decade-old voter authorisations in series). On the survey
side, the 2022 public-use issuance item matches the Government Finance
Database within 0.5% for 99.9% of bridged units. The full validation table
is Appendix Table A11.

**The rules panel.** The fifty-state analysis of Section 5 needs a coding of
each state's rule: for every state, entity type (county, municipality,
township, school district, special district), borrowing purpose and year,
does the default path to GO debt run through a mandatory ballot, and at what
threshold? The working definition of a **strict rule** is that a pre-issuance
ballot referendum at the polls is the mandatory default path. Rules that
demand a town-meeting vote, a referendum only if petitioned, or a vote only
above a debt limit or for certain purposes are coded non-strict, because in
each case a government can normally borrow without convening an electorate at
the polls. **[PENDING]** The current panel is a first-pass machine coding,
cross-validated at 78% (29 of 37 codable states) against an independent hand
coding; a 21-cell human verification pass is in progress, with archived
statutory texts. Until it lands, every rule coefficient in this paper is
presented as a first stage, the association between the coded rule and
observed authorisation behaviour, never as a causal estimate. Each table note
repeats the convention.

---

## 5 · The national landscape: rules, menus and the fifty-state first stage

This section widens the lens from nine states to all fifty. It proceeds in
four steps. Section 5.1 builds the national panel and defines its outcome
variables. Section 5.2 documents three facts about the institutional
landscape that motivate everything after. Section 5.3 asks the first-stage
question: does the coded rule show up in observed authorisation behaviour
(Table 5)? Section 5.4 asks what governments do instead where the rule binds
(Table 6), and Section 5.5 states honestly what reform events can and cannot
yet identify.

### 5.1 A panel of every local government

The unit of analysis is the individual local government. The panel covers
**90,604 units**: every county, municipality, township, school district and
special district in the national Government Finance Database universe. Each
unit carries four blocks of variables. First, the coded rule for its state
and class (Section 4). Second, its borrowing 2005 to 2025 from the corpus:
the count and par of new-money issues, and for each issue its security class
and authorisation mode. The headline outcome, the **voted dollar share**, is
the share of a unit's determined new-money dollars that the documents
evidence as voter-authorised. Third, its borrowing 2005 to 2023 from the
survey. Fourth, demographic and fiscal controls: population (for special
districts, which lack a population concept, ln total revenue serves as the
size control), homeownership, the share aged 65 and over, racial
fractionalisation, median household income, and county presidential
partisanship; place-grain values for cities, county-grain otherwise. A
subpanel of roughly 570 large cities adds institutional detail:
form of government, tax-and-expenditure-limit stringency, city-level
partisanship and mayoral party.

Two composition outcomes recur and deserve definition. The **GO security
share** is the fraction of a unit's new-money dollars issued as
general-obligation debt rather than revenue bonds, leases or other
instruments that typically need no vote. The **non-chargeable share** is the
fraction of classified project dollars flowing to functions that cannot be
billed to users (schools, roads, parks, jails), as opposed to chargeable ones
(water systems, airports, hospitals) whose revenue streams support unvoted
revenue bonds. Because line-level dollar coverage differs across rule
regimes, the non-chargeable share is measured on two bases, dollars and
classified line counts; Appendix Table A4 documents the imbalance and the
count basis is the one the text cites where they differ.

### 5.2 Three facts about the landscape

**Fact 1: different kinds of government hold radically different menus of
exits from the voted channel.** Table 2 tabulates, for the national
new-money corpus (78,672 canonical issues), the share of determined dollars
authorised without a vote, by entity type. School districts route only
**36.6%** of new-money dollars through non-voted channels. At the other end,
municipalities route **88.7%**, counties 83.1%, and authority-class issuers
(housing, hospital and utility conduits) 97.6%; townships (62.0%) and
special districts (73.8%) sit between. The reason is visible in the full
matrix of security class by authorisation mode: a school district's menu is
essentially GO-or-nothing, while a city can finance most of what it does
through revenue bonds, leases and conduit authorities that never face an
electorate. "Who must agree" is not one institution. It is a menu that
varies by the kind of government doing the asking.

[[EX:A5a_menu]]

**Fact 2: voters are shown the civic core; the chargeable perimeter never
votes.** Classifying ballot purposes across 19,600 bond measures, K-12
schools alone account for 38.2% of everything put before voters, followed by
water and sewer, roads, parks and fire protection (Table 3, Panel A). Panel
B lists the corpus functions whose dollars are voted on less than 2% of the
time: public hospitals ($197.7B of local project dollars), multifamily
housing ($70.0B), electric generation ($67.1B), gas utilities, airport
terminals. The contrast is concrete. A $0.84B Harris County Hospital
District line, San Francisco's multifamily housing revenue programme and
Energy Northwest's generation debt faced no ballot; Los Angeles Unified's
$9.0B school ask in 2024 did. At the channel level the sorting is stark: the
voted channel carries **11.3%** chargeable dollars, the board channel 60.0%
and the statutory channel 72.5% (in classified line counts: 17.9%, 34.5%
and 54.0%, the basis robust to coverage; Appendix Table A5 gives the dollar
matrix by channel). What the consent requirement governs,
overwhelmingly, is the class of goods that cannot be charged to users,
precisely the class the theory says it should.

[[EX:A5b_submerged]]

**Fact 3: the same legal sentence assembles coalitions that differ by five
orders of magnitude.** Where vote counts exist (Texas, Wisconsin, Louisiana
and North Carolina; 7,473 GO measures, since California reports percentages
only), the median school bond was decided by **768** yes-votes, the median
off-cycle city measure by 1,179, and the median special-district election by
**34**. Under the identical Texas 50% rule, Harris County's road programme
required 511,375 yes-votes of 1,022,748 cast, while a developer municipal
utility district was authorised by **two votes of two cast** (Table 4). The
coalition a referendum requirement demands is not a constant of the law but
a variable of the electorate the law convenes. Section 8 returns to this
observation. (Texas rows carrying the registry's counts-unknown placeholder,
3,188 rows recorded "1-0", are excluded and documented; no RD estimate is
affected.)

[[EX:A5c_coalitions]]

### 5.3 The first stage: does the rule show up in behaviour?

The first-stage question is simple: comparing governments of the same class
under strict and non-strict rules, is more of their borrowing voter-
authorised where the statute says it must be? Table 5 reports the regression:
the voted dollar share on the strict-rule indicator, estimated by weighted
least squares with region fixed effects, the controls of Section 5.1 and
standard errors clustered by state, pooled and then class by class.

[[EX:R1_firststage]]

The rule shows up, and it shows up most where the theory says it must. Under
a strict rule the voted share of new-money dollars is higher by **+0.690 for
school districts (t = 4.5)**, +0.204 for municipalities (t = 5.8) and
+0.176 for special districts (t = 3.5); the county coefficient (+0.108) is
not significant. The pooled coefficient is small and insignificant, and
column (1) is reported to show why class-by-class estimation is the right
object: the pooled number averages a large school effect with small
general-purpose effects across very different subsample compositions. Raw
shares tell the same story without any regression: 68.4% of school dollars
are voted under strict rules against 7.4% under non-strict ones; 22.2%
against 3.7% for municipalities; 23.3% against 5.4% for counties (Appendix
Table A6 reports the full grid).

Figure 1 maps the resulting geography of consent for the 46 states passing
the coverage gate: the observed voted share of local new-money debt ranges
from roughly 80% in Oklahoma and two-thirds in Texas to under 3% in New
York, Pennsylvania, Tennessee and Kentucky, the states whose statutes
require no local ballot.

[[FIG:F4_consent_map|The geography of consent. Voted share of local new-money dollars by state, official-statement corpus 2005--25, package v3. States below the 50-document coverage gate (DC, DE, HI, VT, WY) are shown as no-data.]]

One reversal in the class table is itself diagnostic. Townships show 18.2%
voted under nominally strict rules against 46.6% under non-strict ones, the
opposite gradient to every other class. Townships carry a proxy rule in the
panel (the municipal coding of their state), and New England towns borrow by
town-meeting vote in states coded non-strict for cities. The panel is
signalling that the coding needs a township class; the anomaly is flagged
rather than absorbed, and the township column is on the verification
worklist. **[PENDING: rules pass-2.]**

### 5.4 Substitution: what governments do instead

If a strict rule makes the GO instrument costly, governments with
alternatives should shift towards them. Table 6 tests this on the
composition of borrowing, and then asks whether the rule changes the amount
of borrowing at all.

[[EX:R2_substitution]]

Cities under strict rules substitute away from the voted instrument. At the
unit grain with full controls, general-purpose governments in strict states
carry a GO security share **27.7 points lower** (t = −3.9) than their
counterparts in non-strict states (column 2). Their project composition
shifts in the same direction: the non-chargeable gap is −8.7 points
(t = −1.6) measured in dollars and **−4.7 points (t = −2.3)** measured in
classified line counts (columns 3 and 4), the count basis being the one
robust to the coverage imbalance documented in Appendix Table A4. A
state-level fixed-effects version of the same test gives −0.162 (t = −1.83).
This is the fifty-state generalisation of Fact 2: where the GO instrument
requires assembling a coalition, governments that can finance through
chargeable, unvoted instruments do so.

The extensive margin, by contrast, is quiet. Whether a government borrows at
all over 2005 to 2025 (column 5) and how much it issues in survey totals
(column 6) are not significantly associated with the rule. The rule moves
the channel and the composition of borrowing, not its existence, exactly the
pattern the regression-discontinuity results of Section 6 rationalise: the
requirement prices delay and channel, not denial.

Institutional interactions on the big-city subpanel (tax-and-expenditure
limits) and national demographic interactions are reported in Appendix Table
A7; none is significant except a negative interaction with county
Democratic share (t = −2.0), which is county-grain, 2020-vintage and read as
descriptive. **[PENDING: all rule coefficients in this section are
first-stage or descriptive until the rules verification pass.]**

### 5.5 What reform events can and cannot show

The strongest available national causal design is California's Proposition
39 (November 2000), which cut the school threshold from two-thirds to 55%
while leaving every other Californian government and every other state
untouched. It does not yet deliver a verdict at the state-mean grain. The
schools-only difference-in-differences is +0.45 log points (permutation
p = 0.15 across 49 placebo states) with a visible pre-trend, and the
sector-differenced triple-difference is approximately zero. Two data facts
discipline the design rather than the theory: the survey's pre-2005 security
split classifies all school long-term debt as full-faith-credit, so the
composition shift Proposition 39 should produce is invisible in Census data;
and California's state matching-bond waves (Propositions 47 and 55, 2002 and
2004) confound the totals margin. **[PENDING: the publishable version is a
district-level two-way fixed-effects design with enrolment weights,
Conley-Taber inference, matching-fund controls and CDIAC issuance data; a
journal-version item.]** The reform record accordingly appears in Section 9
as evidence on the politics of the rule, and the causal weight of the paper
rests on the within-state designs of Section 6.

---

## 6 · Authorisation at the margin: regression-discontinuity evidence

**The design, in plain terms.** A government that wins its referendum with
50.4% and one that loses with 49.6% are, in every respect that matters,
the same government on the same day; the only thing that differs is which
side of the statutory line the vote landed. Comparing many such near-winners
with near-losers therefore isolates the causal effect of authorisation
itself. Formally, for the 11,889 GO measures at statutory thresholds, the
outcome is regressed on the running variable (the vote share minus the
threshold) separately on each side of zero, local-linear with a triangular
kernel within a ±10 percentage-point bandwidth. Inference follows the
robust bias-corrected (RBC) convention of Calonico, Cattaneo and Titiunik:
each table reports the RBC estimate with its robust confidence interval and
p-value, the conventional local-linear estimate beside it, and the
effective sample on each side of the cutoff.

**Balance.** The design's premise is that near-winners and near-losers are
comparable before the vote. Table 7 checks it: none of seven pre-vote
covariates (lagged issuance, population, enrolment, homeownership, income,
age structure, prior measure count) jumps at the cutoff (maximum |t| = 1.36).

[[EX:T2_covariate_continuity]]

**Density.** One threat is specific to this setting: governments time
proposals to win, so there is excess mass just above the cutoff (McCrary
θ = +0.24, z = 4.6). Figure 2 shows where it lives: it is Texas-specific
(TX +0.21, z 2.7; every other state approximately zero), carries the
signature of endogenous proposal timing documented since Cellini, Ferreira
and Rothstein (2010), and is itself evidence on the agenda margin taken up
in Section 9. Identification survives it: donut estimates that drop the
contested region around the cutoff are stable to larger (+0.19 to +0.20,
z 3.7 to 5.3; Appendix Table A1).

[[FIG:F5_density|Density of the vote margin by state. Histograms of the running variable within ±10pp; the discreteness of small Texas electorates is visible. McCrary log-density discontinuity: pooled +0.24 (z 4.6) at h = 5pp, +0.14 (z 2.6) over this full ±10pp window; Texas +0.21 (z 2.7); all other states approximately zero.]]

**The main result.** Passed measures are followed by issuance 35.6% of the
time against 14.6% for failed ones, but most of that 21-point gap is
selection: better-supported projects both pass and proceed. The design
removes the selection. At the cutoff, authorisation raises six-year GO
issuance by **+11.0 percentage points (RBC, robust z = 2.30; conventional
+14.6, z = 4.47)**; any-issuance gives +11.6 and +14.4 (Table 8, Figure 3).
The effect replicates state by state across three different thresholds:
California +16.6 (z 3.0), Texas +14.1 (z 3.3), Wisconsin +21.2 (z 3.1).
Three statutes, one answer. Louisiana's negative cell (−27.6, z −1.9) is a
data-grain artefact, measures folding to the parish, and excluding it moves
the pooled estimate to +16.2 (Appendix Table A2 reports the state cells;
Appendix Table A3 the placebo thresholds, all null at the 5% level).

[[EX:T3_main_results]]

[[FIG:F1_rd|Issuance at the authorisation threshold. Share of measures followed by any issuance within six years, in 0.5pp bins of the running variable sized by cell count, with local-linear fits on each side and the RBC estimate annotated.]]

**The intensive margin doubles, in two independent sources.** Log new-money
par per capita rises +0.92 (z 3.0) in the disclosure corpus and, decisively
for the survivorship concern, **+0.83 (z 3.3) in the Census survey
measure**, which includes the bank loans and private placements no official
statement records. Both are RBC-stable (+0.94, +0.88) and the survey
pre-period placebo is null (+0.41, z 1.5). This is the survey debt items'
single appearance, as Section 4's architecture prescribes.

**Timing, not denial.** The event study (Figure 4) loads the entire effect
on the vote year (τ₀ = +0.236, z = 7.8; every pre- and post-year
approximately zero). Figure 5 turns the timing into quantities for the
|margin| ≤ 5 window: among six-year issuers, the median barely-authorised
government reaches the market in **0.33 years**, the median barely-refused
one in **1.15**, a delay of 0.8 years, and the refused side never reaches
the authorised side's end-of-vote-year issuance level within six years. By
year six, 50.1% of barely-refused governments have still issued nothing,
against 40.0% of barely-authorised ones: a ten-point wedge that is the
durable residue after all catch-up.

[[FIG:F2_event_study|Event study. RBC coefficient on issuance in each year relative to the vote, with robust 95% confidence intervals; indicators exist for k = −2 to +5.]]

[[FIG:F3_wedge|The cumulative wedge. Cumulative any-issuance for barely-passed (solid) and barely-failed (dashed) measures, |margin| ≤ 5; the shaded area is the wedge; median market-entry times annotated.]]

**Robustness, and the pay-go bound.** The full specification battery is
Appendix Table A1: donut variants, clustering by unit (z 4.11) and county
(z 3.47), Lee bounds for crosswalk selection at trim 2.52% ([+0.138,
+0.163]), randomisation inference in the ±2 window (p < 0.0002; 0 of 5,000
permutations), horizons one to six years, and the bandwidth curve. Two
diagnostics do not reject and are reported with their reconciliation: the IK
bandwidth selects h = 1.8pp, only two points of support, where slope terms
absorb a level shift that the design-based tests at the same window detect
decisively; RBC at ±5 has the same character. The battery's final row is
the **pay-go bound**: rerunning the design with survey capital outlay per
capita as the outcome, the schools post-minus-pre differenced estimate is
**+0.377 (z 2.9; RBC +0.464, z 2.4)** beside an issuance effect of +1.43,
and trimmed levels imply an outlay-to-issuance ratio of **0.92** at the
cutoff. Refused governments do not detectably replace lost borrowing with
debt-free construction. (Caveats: outlay spreads over construction years,
so six-year windows understate long-project differences; the differenced
specification nets the positive pre-period outlay RD that endogenous timing
produces; total outlay only; the full-window cohort is votes through roughly
2017 to 2018 with outlay ending at fiscal 2023.) Nothing in the battery is
hidden; the appendix table shows all of it.

---

## 7 · The response margin: what refusal buys

The theory's distinctive claim is that a coalition requirement prices delay,
not denial. This section follows every refused measure forward and asks what
refusal actually bought. Table 9 collects the accounting.

[[EX:T5_response]]

**Refusal is a pause.** Of 2,680 failed GO measures, the re-submission
hazard is front-loaded: 26.7% return within a year, then 22.8%, 15.8% and
12.4% in the following years, cumulating to **58.2% within four years**,
with the median return at **1.02 years**, which is to say the next election.
Returns win: **61.9%** pass. And districts re-ask rather than concede: the
median returning measure asks for 100% of the original amount (n = 1,354;
only 45.9% downsize).

**The fate of the marginal refusal.** For the 2005 to 2019 cohort with full
observation windows, per 100 barely-refused measures: **54 are re-approved
by voters within four years; 13 more return and await a verdict; 5.2 borrow
through the board or statutory channel; 9.0 issue on pre-existing voter
authority; 18 are extinguished** within the horizon. The 9.0 issuing on
pre-existing authority draw on authorisations banked before the refused
measure, so they are not evidence of evading it; the substitution reading
attaches only to the 5.2 board-or-statutory cell. The transition matrix
beneath Table 9 shows what the cutoff actually moves: voter-mode first
issuance (48.4% for barely-passed against 36.7% for barely-failed) against
no issuance (43.1% against 54.2%), while board-mode first issuance sits
near 8% on both sides. The board channel is a floor, not the treatment
margin. Consistent with this, what barely-refused governments still issue
tilts towards the board channel (council share τ = −0.064, z = −2.0).

**The project itself survives.** Matching ballot purposes to the
use-of-proceeds functions of subsequent issues (a deterministic category
bridge, blind-audited at **80.0% precision and 88.9% recall**), same-purpose
financing appears within six years for 44.7% of barely-passed measures and
**33.4% of barely-failed ones** (RD +0.072, z 2.1; imprecise under RBC:
+0.052, robust p = 0.30), with median arrival 0.32 against 1.67 years. A
third of narrowly refused projects get financed anyway, later. On
re-submission, bundles are not recomposed: 78.2% of original purpose
categories are retained. The pay-go bound of Section 6 closes the remaining
loophole on the provision side: building falls with borrowing at a ratio
near one, so the continuation gap is not being quietly filled by debt-free
construction. **[PENDING: nine disputed audit pairs queued for review.]**

**Authorisation banked, drawdown deferred.** The supermajority regime
produces a distinct fate for near-misses. Within California, failures with
majority support short of the threshold re-submit far more than decisive
failures (42.2% against 27.4%; 51.3% against 30.8% among schools) and show
no jump at the symbolic 50% line: the response tracks proximity to passage,
not the majority label. Yet their issuance is lower, and the deficit is not
a truncation artefact: it **widens** from −5.3 points at six years to −6.4
at eight (schools −6.7 to −8.0). The near-miss chain (Appendix Table A8)
shows why. Near-miss failures convert by re-vote four times as often (107
against 25 passed returns), but the conversions sit undrawn: median
pass-to-first-issue **6.2 years** against 2.9, and only 5.5% see a
voter-mode issue within eight years. Where the bar is a supermajority, even
re-assembled consent does not become borrowing on the study horizon. A
candidate mechanism, that Proposition 39's statutory tax-rate caps meter the
drawdown of 55%-route authorisations, was tested and is neither supported
nor excluded: the uncapped cell is too thin (9 conversions against 118) and
its point direction runs against the cap story (Appendix Table A9). The
fact stands documented and unexplained.

---

## 8 · Where the requirement binds: exits and electorates

The RD average of Section 6 conceals the theory's structure. Two partitions
recover it: by the borrowing government's exit menu, and by the electorate
that the rule convenes.

**By exit menu: the fork.** Table 10 splits the RD frame by entity class
and sets each class's estimate against its independently measured national
menu from Section 5. School districts (non-voted share 29.8% within the
frame) show the binding effect (+0.147, z 4.0; RBC +0.123, z 2.3) and the
highest re-submission rate (59.2%). General-purpose governments (non-voted
share 80.4%) show no discontinuity at all (+0.073, z 0.9; RBC −0.02) and
the lowest re-submission (25.3%). Special districts sit between, with the
largest GO-specific jump, which shrinks at any-issuance as part of the gap
reroutes to non-GO instruments; their cells are small and the ordering, not
the magnitude, is the cited object. The rule binds exactly where the menu
offers no exit; where exits exist, refusal is nearly costless and rarely
re-litigated. This is the same fork the fifty-state substitution results
(Table 6) show in cross-section.

[[EX:T7_fork_menu]]

**By electorate: the stable propertied public.** A naive assembly-cost
reading predicts that the authorisation effect weakens wherever coalitions
are harder to build, and in particular that demographic heterogeneity
raises the price of assembly. The data falsify that version on its own
sign: the effect is carried by homogeneous electorates (+0.232 against
−0.018 in diverse ones), not blocked by them. What the moderator profile
consistently favours is a **stable-propertied-public** account:
authorisation binds where the consenting public is durable and propertied,
because those are the electorates whose refusals stay refused and whose
approvals licence long-horizon drawdown. Homeownership above the frame
median gives τ = **+0.182 (z 3.5)** against +0.056 below (Table 11); the
65-plus split gives +0.194 against +0.036 in levels (the formal difference
is not significant under RBC); the effect is stronger on-cycle (+0.252
against +0.099), when the broad durable electorate is the one consulted. It
is ownership, not affluence: the income split is flat (+0.129 against
+0.122). And it is institutional, not partisan: precinct-built city
partisanship and mayoral party in the 577-city panel show no moderation
(all n.s.; the coarser county-grain splits agree and sit in Appendix Table
A12). All moderation tables run on the 6,255 proper-grain measures (place
grain for cities, district grain for schools); special districts are
excluded pending sub-county demographics. The reframing is stated as it is:
an account adopted after seeing the homogeneity sign, offered with its
transmission story, and flagged as post hoc rather than pre-registered.

[[EX:T6_moderators]]

**The incidence of the higher bar.** Blocked majorities, measures with
majority support short of a supermajority threshold (California only, by
construction), arise in places that sit between decisive-failure and
comfortable-passage places on renter share, diversity and inequality; among
schools they are the poorer places (median household income −$3.8k against
cleared places, SE 1.5k; Appendix Table A10). Descriptive, but it locates
the supermajority's demographic cost: majorities in less affluent,
mid-composition districts.

---

## 9 · The agenda margin and the politics of the rule

**Rules discipline what is asked.** The coalition requirement operates
before any vote is cast. Under California's 55% bar, school districts bring
**8.8 proposals per 100 districts per year** at a median $39M, 62.7%
on-cycle; under Texas's 50% bar, **20.1** per 100 at $15M, 14.1% on-cycle;
Wisconsin sits between on all three margins (Table 12). Fewer, larger,
better timed. Pass rates make the same point in reverse: nearly invariant
between the 50% and 55% regimes (79.2% against 77.6%) and collapsing only
at two-thirds (47.6%). A moderate bar is absorbed by the agenda; an extreme
bar defeats even what selection permits. The Texas 2019 reform (HB 3)
closes the loop within-state: when the state mandated separate propositions
for stadiums, natatoria and performing-arts facilities, propositions per
election jumped from 1.5 to 1.7 before the reform to 2.0 to 2.4 after, and
the multi-proposition share doubled within two cycles. Bundling is a
rule-governed choice, not a habit. The near-cutoff excess mass of Section 6
belongs to the same family: proposals are timed to win.

[[EX:A4_agenda]]

**At fixed voter support, the rule alone moves outcomes.** In the 50 to 55%
band, the identical electoral result is a failure for a Californian school
district and a success for a Texan or Wisconsin one. The
difference-in-differences across the adjacent band gives **+11.5 points of
six-year issuance (SE 4.8)** attributable to the rule at fixed support,
indistinguishable from the RD estimate obtained from an entirely different
comparison: an out-of-design calibration regarded here as the strongest
single check in the paper.

**The polity fights over the rule exactly where the theory predicts.** Since
1990, nearly every attempt to lower a local borrowing threshold has targeted
schools, the class Table 2 shows holding the poorest exit menu: California's
Propositions 170 (1993, failed), 26 (2000, failed) and 39 (2000, passed 53
to 47, schools only, with a $30M elite-financed bipartisan campaign);
Washington's 2023 to 2025 school-bond bills (all stalled); Idaho's roughly
eleven legislative attempts (none passed). The one recent non-school
attempt, California's Proposition 5 (2024), which would have extended the
55% bar to housing and infrastructure, failed. Where exits exist, no one
spends thirty million dollars to lower the bar. **[PENDING: the reform
table is compiled from secondary sources and marked secondary-unverified
pending primary-record checks; it is cited as evidence on reform politics,
not as a causal estimate.]**

---
