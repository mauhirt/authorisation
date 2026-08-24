# Who Must Agree: Empirical Sections (round-3 regeneration)

*Draft 2026-08-24 (round 3). Every number traces to a committed RESULTS file
(script-to-results map in `analysis/ANALYSIS_REVIEW.md`). **[PENDING]** marks
claims held on a named data pass. The honesty record (nulls, pending items,
data limits) now lives in the online appendix
(`paper/ONLINE_APPENDIX_HONESTY.md`). House style applied throughout:
impersonal constructions, no em dashes, British spelling. Corpus package v3
(the finance-flag fix) is folded into every national exhibit below; the
nine-state referendum panel reruns once on v4.*

---

## 4 · Data: observing the consent requirement end to end

Testing a theory of authorisation rules requires observing three things that no
single dataset contains: the **rule** (who must agree, at what threshold), the
**asking** (what governments put before voters, and what happened), and the
**borrowing** (what was ultimately issued, under what security, for what
purpose, and, critically, on whose authority). The analysis assembles all three
at the level of the individual local government nationwide, and at the level of
the individual referendum in nine states.

**Referenda.** The referendum panel compiles 47,235 local bond and tax measures
from nine state administrative sources: California (CDIAC), Texas (Bond Review
Board), Wisconsin (DPI), Louisiana (Secretary of State), North Carolina
(NCSBE), Massachusetts (DLS Proposition 2½ databank), Minnesota, Illinois and
Indiana. Each measure is crosswalked to its Census of Governments unit: 40,924
(86.6%) resolve to a government identifier, with exact tiers verified at
approximately 100% and the fuzzy-match tier independently audited at 95.1%
accuracy. Restricting to measures at a genuine mandatory-ballot statutory
cutoff leaves 23,577; the regression-discontinuity frame is its
general-obligation subset, **11,889 GO measures** (Texas 8,062, California
2,189, Wisconsin 999, Louisiana 361, North Carolina 278) across three
thresholds: 50% (TX, WI, LA, NC), 55% (California schools) and 66.7%
(California non-school), with California thresholds assigned per measure from
CDIAC.

**The outcome architecture.** The outcome of record throughout is the
**official-statement corpus**: 258,762 official statements (2005–2025, all
fifty states; 43,030 issuers), from which are extracted, for every issue, the
par amount, the security pledge class (GO, revenue, lease, special tax),
use-of-proceeds lines classified into 118 functional activities, and the
variable the paper turns on, the **authorisation mode evidenced in the document
itself**: voter approval (with the election date the document cites), governing
board action, or statutory authority. It is the richest available measure of
what was borrowed, for what, and on whose authority, and every headline
provision claim in the paper (issuance, channel, purpose, project continuation)
rides on it. The Census survey data enter in two deliberately subordinated
roles, each occupying a single table row: the Government Finance Database debt
items (1967–2023; 2.1 million local unit-years, extended to fiscal 2024 by the
public-use continuation) serve one purpose, a survivorship robustness check on
the disclosure corpus; and the survey capital-outlay items serve one purpose,
a bound on the channel the corpus cannot see by construction, capital spending
without debt (the pay-go bound, Section 6). Neither survey use displaces the
corpus as the outcome of record.

**Validation.** Because the authorisation mode is extracted rather than
administrative, it is validated against the election record before use
(Table 4.1). Where an official statement cites an election date, that date
matches an independently observed referendum for the same unit 67.9% of the
time pooled, and 95.4% in Wisconsin, the state whose registry is
known-complete; conditional on a match, 91.3% of cited elections are passed
measures (98.0% in California, 98.8% in North Carolina). Shortfalls
concentrate exactly where registry coverage is known-short (Minnesota's
registry begins in 2020; Massachusetts dates votes at month grain), and the
voter-mode support rate (76.2% of voter-mode new-money documents have a passed
referendum within six years in the records) is a lower bound driven by
authorisations older than the observation windows: Texas districts issue
against decade-old voter authorisations in series. The survey side is
validated in the other direction: the 2022 public-use file's issuance item
matches the GFD within 0.5% for 99.9% of bridged units.

**The rules panel.** State by entity-type by purpose by year coding of
referendum requirements (threshold, ballot mandate, stringency). **[PENDING]**
The panel is a first-pass machine coding cross-validated at 78% (29/37 codable
states) against an independent hand coding; a 21-cell human verification pass
is with the owner. Until it lands, every rule coefficient below is presented
as a first stage (the association between the coded rule and observed
authorisation behaviour), never as a causal estimate. The convention is marked
in each table note.

> **Table 4.1** Validation of extracted authorisation fields. **Table 4.2**
> Frame construction (universe, crosswalk, cutoff sample, GO RD frame), with
> per-state counts.

---

## 5 · The institutional landscape and the fifty-state first stage

Before estimating anything, the object itself is documented; the coded rules
are then confronted with observed behaviour across the whole local state.

### 5.1 Three facts about the landscape

**Fact 1: entity types hold radically different menus of exits from the voted
channel.** Table 5.1 tabulates, for the national new-money corpus (78,672
canonical issues, package v3), the share of determined dollars authorised
without a vote, by entity type. School districts route only **36.6%** of
new-money dollars through non-voted channels; townships 62.0%; special
districts 73.8%; counties **83.1%**; municipalities **88.7%**; and
authority-class issuers (housing, health-hospital and utility conduits)
**97.6%**. The full matrix (security
class by authorisation mode, per entity and rule regime) shows why: a school
district's menu is essentially GO-or-nothing, while a city can finance most of
what it does through revenue bonds, leases and conduit authorities that never
face an electorate. "Who must agree" is not one institution: it is a menu that
varies by the kind of government doing the asking.

**Fact 2: the balloted local state is the non-chargeable civic core; the
chargeable perimeter never votes.** Classifying ballot purposes across 19,600
bond measures, K-12 schools alone account for 38.2% of everything put before
voters, followed by water and sewer, roads, parks and fire protection
(Table 5.2, Panel A). Panel B lists the corpus functions whose dollars are
voted on less than 2% of the time: public hospitals ($197.7B of local project
dollars), multifamily housing ($70.0B), electric generation ($67.1B), gas
utilities, airport terminals. A $0.84B Harris County Hospital District line,
San Francisco's multifamily housing revenue programme, Energy Northwest's
generation debt: none faced a ballot; Los Angeles Unified's $9.0B ask in 2024
did. The nationwide sorting is stark at the channel level: the voted channel
carries **11.3%** chargeable dollars, the board channel 60.0%, the statutory
channel 72.5%. What the consent requirement governs, overwhelmingly, is the
class of goods that cannot be charged to users, precisely the goods H2 says it
should.

**Fact 3: the same legal sentence assembles coalitions that differ by five
orders of magnitude.** Where vote counts exist (TX, WI, LA, NC; 7,473 GO
measures, since California's CDIAC reports percentages only), the median
school bond was decided by **768** yes-votes, the median off-cycle city
measure by **1,179**, and the median special-district election by **34**.
Under the identical Texas 50% rule, Harris County's road programme required
511,375 yes-votes of 1,022,748 cast, while a developer municipal utility
district was authorised by **two votes of two cast** (Table 5.3). The
coalition a referendum requirement demands is not a constant of the law but a
variable of the electorate the law convenes, the observation that motivates
the heterogeneity analysis of Section 8. (Texas rows carrying the registry's
counts-unknown placeholder convention, 3,188 rows recorded "1-0", are excluded
and documented; no RD estimate is affected.)

### 5.2 The rule and the channel: the fifty-state first stage

A panel of **90,604 local governments** (every county, municipality, township,
school district and special district in the national GFD universe) carries the
coded rule for its class, demographic and fiscal characteristics (population
or enrolment; revenue, property tax, debt stock; ACS homeownership, age,
diversity and income at place grain for cities and county grain otherwise;
county presidential partisanship), and its borrowing 2005–25 from the corpus
and 2005–23 from the survey. A subpanel of roughly 570 large cities adds
form-of-government institutions, tax-and-expenditure-limit stringency,
city-level partisanship and mayoral party. Estimation: weighted least squares
with state-clustered standard errors, Census-region fixed effects, and the
characteristics above as controls.

**The rule shows up in behaviour, most where the theory says it must.** Under
a strict rule, the OS-evidenced voted share of determined new-money dollars is
higher by **+0.69 for school districts (t = 4.5)**, +0.20 for municipalities
(t = 5.8), +0.18 for special districts (t = 3.5) and +0.11 (n.s.) for
counties (Table 5.4); the pooled coefficient is composition-sensitive across
classes and the per-class rows are the cited object. Raw magnitudes tell the
same story: 68.4% of school dollars are voted under strict rules against 7.4%
under lax ones; 22.2% against 3.7% for cities; 23.3% against 5.4% for
counties. Figure 5.1 maps the resulting geography of consent across 46 states
with full flag coverage: the observed voted share of local new-money debt
ranges from roughly 80% in Oklahoma and two-thirds in Texas to under 3% in
New York, Pennsylvania, Tennessee and Kentucky, the states whose statutes
require no local ballot. The one reversal in the class table, townships
(18.2% strict against 46.6% non-strict), is itself diagnostic: townships
carry a proxy (municipality) rule in the panel, and New England towns borrow
by town-meeting vote in states coded lax for cities. The panel is signalling
that the coding needs a township class; it is flagged rather than absorbed.
**[PENDING: rules pass-2; the township column is on its worklist.]**

**Cities under strict rules substitute away from the voted instrument.** At
the unit grain with full controls, general-purpose governments in strict
states carry a GO security share **27.7 points lower** (t = −3.9) than their
counterparts in lax states; the non-chargeable project gap attenuates to
−8.7 points (t = −1.6) under the fuller v3 coverage, direction preserved
(Table 5.5). This is the fifty-state
generalisation of the sorting in Fact 2: where the GO instrument requires a
coalition, governments that can finance through chargeable, unvoted
instruments do. The state-level fixed-effects version of the same test gives
−0.162 (t = −1.83). **[PENDING: both are held as first-stage or descriptive
until the rules pass-2.]**

**The extensive margin is quiet.** Whether a government borrows at all
(2005–25) and how much it issues in survey totals are not significantly
associated with the rule (t ≈ −1.3). The rule moves the channel and the
composition, not the existence of borrowing, exactly the pattern the
regression-discontinuity results of Section 6 rationalise.

**Reform events: the honest state of play.** The strongest available national
causal design, California's Proposition 39 (November 2000), which cut the
school threshold from two-thirds to 55% while leaving every other California
government and every other state untouched, does not yet deliver a verdict at
the state-mean grain: the schools-only difference-in-differences is +0.45 log
points (permutation p = 0.15 across 49 placebo states) with a visible
pre-trend, and the sector-differenced triple-difference is approximately
zero. Two data facts discipline the design: the GFD's pre-2005 security split
is degenerate for schools (full-faith-credit debt is 100% of school long-term
debt by classification), so the certificates-of-participation-to-GO
composition shift Proposition 39 should produce is invisible in Census data;
and California's state matching-bond waves (Propositions 47 and 55, 2002 and
2004) confound the totals margin. **[PENDING: the publishable version is a
district-level two-way fixed-effects design with enrolment weights,
Conley-Taber inference, state matching-fund controls, and the CDIAC issuance
database for the composition margin; a journal-version item.]** The reform
record accordingly plays its role in Section 9 as evidence on the politics of
the rule, and the causal weight rests on the within-state designs of
Section 6.

> **Table 5.1** The menu matrix. **Table 5.2** The balloted and submerged
> local state. **Table 5.3** Absolute coalition sizes. **Table 5.4** First
> stage by entity class. **Table 5.5** Substitution. **Figure 5.1** The
> geography of consent (built: `analysis/fig_consent_map.svg`; entity-class
> small multiples in the appendix).

---

## 6 · Authorisation at the margin: regression-discontinuity evidence

**Design.** For the 11,889 GO measures at statutory thresholds, governments
that barely won authorisation are compared with those that barely lost it, in
the threshold-centred vote margin. Estimation is local-linear with a
triangular kernel; robust bias-corrected (RBC) inference is the lead
convention (local-quadratic at h with robust variance), with conventional
estimates alongside.

**The naive gap, and what survives design discipline.** Passed measures are
followed by issuance 35.6% of the time against 14.6% for failed ones, a
21-point gap that is mostly selection. At the cutoff, the six-year effect of
authorisation on GO issuance is **+11.0 points (RBC, robust z = 2.30;
conventional +14.6, z = 4.47)** at the ±10 bandwidth; any-issuance gives
+11.6 and +14.4. The effect replicates state by state across three different
thresholds: California +16.6 (z 3.0), Texas +14.1 (z 3.3), Wisconsin +21.2
(z 3.1). Three statutes, one answer. Louisiana's negative cell (−27.6,
z −1.9) is a data-grain artefact (measures fold to the parish); excluding it
moves the pooled estimate to +16.2.

**The intensive margin doubles, in two independent sources.** Log new-money
par per capita rises +0.92 (z 3.0) in the disclosure corpus and, decisively
for the survivorship critique, **+0.83 (z 3.3) in the Census survey measure**,
which includes the bank loans and private placements no official statement
records; both are RBC-stable (+0.94, +0.88) and the survey pre-period placebo
is null (+0.41, z 1.5). This is the survey debt items' single appearance, as
Section 4's architecture prescribes.

**Validity.** Covariate balance: 0 of 7 pre-vote fiscal covariates imbalanced
at ±5 (max |t| = 1.36). Density: there is excess mass just above the cutoff
(McCrary θ = +0.24, z = 4.6); it is Texas-specific (TX +0.21, z 2.7; every
other state approximately zero), carries the signature of endogenous proposal
timing documented since Cellini, Ferreira and Rothstein (2010), and is itself
agenda-margin evidence (Section 9). Identification survives it: donut
estimates excluding the contested region are stable to larger (+0.19 to
+0.20, z 3.7–5.3). Inference alternatives agree: clustering by unit (z 4.11)
or county (z 3.47); Lee bounds for crosswalk selection at trim 2.52% are
[+0.138, +0.163]; randomisation inference in the ±2 window rejects at
p < 0.0002 (0 of 5,000 permutations). The two flexible-fit diagnostics that
do not reject, the IK bandwidth (h = 1.8pp, τ ≈ 0) and RBC at ±5 (confidence
interval [−0.09, +0.17]), are reported with their reconciliation: on two
points of support, slope terms absorb a level shift that the design-based
tests at the same window detect decisively. The battery's final row is **the
pay-go bound**: rerunning the design with survey capital outlay per capita as
the outcome, the schools post-minus-pre differenced estimate is **+0.377
(z 2.9; RBC +0.464, z 2.4)** beside an issuance effect of +1.43, and trimmed
levels imply an outlay-to-issuance ratio of **0.92** at the cutoff. Refused
governments do not detectably replace lost borrowing with pay-go building
(caveats: outlay spreads over construction years, so six-year windows
understate long-project differences; the positive pre-period outlay RD from
endogenous timing is netted by the differenced specification; total outlay
only). Nothing in the battery is hidden; the table shows all of it.

**It is a timing effect, and the wedge is measurable.** The event study loads
the entire effect on the vote year (τ₀ = +0.236, z = 7.8; every pre- and
post-year approximately zero). Cumulative curves for the |margin| ≤ 5 window
(Figure 6.2) turn this into the paper's quantities: among six-year issuers,
the median barely-authorised government reaches the market in **0.33 years**,
the median barely-refused one in **1.15**, a delay of **0.8 years**, and the
refused side never reaches the authorised side's end-of-vote-year issuance
level within six years. By year six, 50.1% of barely-refused governments have
still issued nothing, against 40.0% of barely-authorised ones: a ten-point
wedge that is the durable residue after all catch-up.

> **Table 6.1** Main RD estimates. **Table 6.2** The validity battery,
> including the pay-go-bound row. **Figure 6.1** Event study. **Figure 6.2**
> The cumulative wedge (built: `fig_cumulative_wedge.svg`).

---

## 7 · The response margin: what refusal buys

The theory's distinctive claim is that a coalition requirement prices delay,
not denial. Every refused measure is followed forward.

**Refusal is a pause.** Of 2,680 failed GO measures, the re-submission hazard
is front-loaded (26.7% return within a year, then 22.8%, 15.8%, 12.4%),
cumulating to **58.2% within four years**, with the median return at **1.02
years**: the next election. Returns win: **61.9%** pass. Districts re-ask
rather than concede: the median returning measure asks for **100% of the
original amount** (n = 1,354; only 45.9% downsize).

**The fate of the marginal refusal.** For the 2005–19 cohort with full
observation windows, per 100 barely-refused measures (Table 7.1): **54 are
re-approved by voters within four years; 13 more return and wait; 14 borrow
anyway on other authority** (5 via board or statutory channels, 9 on older
voter authorisations); **18 are extinguished** within the horizon. The
transition matrix behind it shows what the cutoff actually moves: voter-mode
first issuance (48.4% against 36.7%) against no issuance (43.1% against
54.2%), while board-mode first issuance is roughly 8% on both sides. The
board channel is a floor, not the treatment margin. Consistent with this, the
authorisation mix of what barely-refused governments still issue tilts
towards the board channel (council share τ = −0.064, z = −2.0).

**The project itself survives.** Matching ballot purposes to the
use-of-proceeds functions of subsequent issues (deterministic category
bridge, blind-audited at **80.0% precision and 88.9% recall**; every number
cites the audit), same-purpose financing appears within six years for 44.7%
of barely-passed measures and **33.4% of barely-failed ones** (RD +0.072,
z = 2.1), with median arrival 0.32 against **1.67 years**. A third of
narrowly refused projects get financed anyway, later. On re-submission,
bundles are not recomposed: 78.2% of original purpose categories are
retained. The pay-go bound (Section 6) closes the remaining loophole on the
provision side: the same design run on survey capital outlay shows building
falling with borrowing at a ratio near one, so the continuation gap measured
in the corpus is not being quietly filled by debt-free construction.
**[PENDING: nine disputed audit pairs queued for the disagreement review.]**

### 7.1 Authorisation banked, drawdown deferred

The supermajority regime produces a distinct fate for near-misses. Within
California, failures with majority support short of the threshold re-submit
far more than decisive failures (42.2% against 27.4%; 51.3% against 30.8%
among schools) and show no jump at the symbolic 50% line: the response tracks
proximity, not the majority label. Yet their issuance is lower, and the
deficit is not a truncation artefact: it **widens** from −5.3 points at six
years to −6.4 at eight (schools −6.7 to −8.0), under per-cell observability
restrictions. The chain shows why. Near-miss failures convert by re-vote four
times as often (107 against 25 passed returns), but the conversions sit
undrawn: median pass-to-first-issue **6.2 years** against 2.9, and only 5.5%
see a voter-mode issue within eight years. Where the bar is a supermajority,
even re-assembled consent does not become borrowing on the study horizon.

A candidate mechanism, that Proposition 39's statutory tax-rate caps meter
the drawdown of 55%-route authorisations, was tested by splitting Californian
conversions by the route of the passing return: the uncapped two-thirds cell
is too thin to test (9 school conversions against 118 capped) and its point
direction runs against the cap story (median 9.7 years to first issue against
4.9 capped). The mechanism is neither supported nor excluded at this sample
size; the fact stands documented and unexplained, with county assessed-value
rolls and the CDIAC sold-versus-authorised series as the upgrade path.

> **Table 7.1** The fate table and transition matrix. **Table 7.2**
> Re-submission hazard, pass rates, amount ratios. **Table 7.3** Project
> continuation and bundle recomposition (with audit precision). **Table 7.4**
> The near-miss chain and the rate-cap split.

---

## 8 · Where the requirement binds: exits and electorates

The RD average conceals the theory's structure. Two partitions recover it.

**By exit menu.** Splitting the RD frame by entity class and aligning each
class against its independently measured national menu (Section 5, Fact 1):
school districts (non-voted share 29.8%, window-chargeable menu 0.4%) show
the binding effect (+0.147, z 4.0; RBC +0.123, z 2.3) and the highest
re-submission rate (59.2%); general-purpose governments (non-voted share
80.4%) show no discontinuity at all (+0.073, z 0.9; RBC −0.02) and the lowest
re-submission (25.3%); special districts sit between, with the largest
GO-specific jump that shrinks at any-issuance as part of the gap reroutes to
non-GO instruments. The special-district cells are small and the ordering,
not the magnitude, is the cited object. The rule binds exactly where the menu
offers no exit; where exits exist, refusal is nearly costless and rarely
re-litigated. This is the fork the fifty-state substitution results
(Section 5.2) show in cross-section.

**By electorate: the stable propertied public.** The naive assembly-cost
reading of H3 predicts that the authorisation effect weakens wherever
coalition-building is harder, and in particular that demographic
heterogeneity raises the price of assembly. The data falsify that version on
its own sign: at the proper demographic grain, the effect is carried by
homogeneous electorates (+0.232 against −0.018 in diverse ones), not blocked
by them. What the moderator profile consistently favours is a
**stable-propertied-public** account: authorisation binds where the
consenting public is durable and propertied, because it is those electorates
whose refusals stay refused and whose approvals licence long-horizon
drawdown. Homeownership above the frame median gives τ = **+0.182 (z 3.5)**
against +0.056 (n.s.) below; the 65-plus share gives +0.194 against +0.036;
and the effect is stronger on-cycle (+0.252 against +0.099 off-cycle), when
the broad durable electorate is the one consulted. It is ownership, not
affluence (the income split is flat: +0.129 against +0.122), and
institutional, not partisan: county presidential partisanship yields a flat
split (+0.121 against +0.111, terciles non-monotone), replicated with
precinct-level city partisanship and mayoral party in the 577-city panel
(all n.s.), and the national first stage shows at most a weaker channel
association in Democratic counties (interaction −0.75, t −2.2, descriptive).
The reframing is stated as it is: an account adopted after seeing the
homogeneity sign, offered with its transmission story, and flagged as
post hoc rather than pre-registered.

**The incidence of the higher bar.** Blocked majorities (measures with
majority support short of a supermajority threshold; California only, by
construction) arise in places that sit between the decisive-failure and
comfortable-passage places on renter share, diversity and inequality, and
among schools they are the poorer places (median household income −$3.8k
against cleared places, SE 1.5k). Descriptive, but it locates the
supermajority's demographic cost: majorities in less affluent,
mid-composition districts. **[PENDING: within-matched ACS caveat as
throughout; special districts remain on county-proxy demographics.]**

> **Table 8.1** The fork against the menu. **Table 8.2** Moderator splits.
> **Table 8.3** Demography of blocked majorities.

---

## 9 · The agenda margin and the politics of the rule

**Rules discipline what is asked.** Under California's 55% bar, school
districts bring **8.8 proposals per 100 districts per year** at a median
$39M, 62.7% on-cycle; under Texas's 50% bar, **20.1** per 100 at $15M, 14.1%
on-cycle; Wisconsin sits between on all three margins. Fewer, larger, better
timed: the coalition requirement operates before any vote is cast. Pass rates
make the same point in reverse, nearly invariant between the 50% and 55%
regimes (79.2% against 77.6%) and collapsing only at two-thirds (47.6%): a
moderate bar is absorbed by the agenda; an extreme bar defeats even what
selection permits. The Texas 2019 reform (HB 3) closes the loop within-state:
when the state mandated separate propositions for stadiums, natatoria and
performing-arts facilities, propositions per election jumped from 1.5–1.7 to
2.0–2.4 and the multi-proposition share doubled within two cycles. Bundling
is a rule-governed choice, not a habit. The near-cutoff excess mass of
Section 6 belongs to the same family: proposals are timed to win.

**At fixed voter support, the rule alone moves outcomes.** In the 50–55%
band, the identical electoral result is a failure for a California school
district and a success for a Texan or Wisconsin one. The
difference-in-differences across the adjacent band gives **+11.5 points of
six-year issuance (SE 4.8)** attributable to the rule at fixed support,
indistinguishable from the RD estimate obtained from an entirely different
comparison: an out-of-design calibration regarded here as the strongest
single check in the paper.

**The polity fights over the rule exactly where the theory predicts.** Since
1990, nearly every attempt to lower a local borrowing threshold has targeted
schools, the class the menu matrix shows holding the poorest exit menu:
California's Propositions 170 (1993, failed), 26 (2000, failed) and 39
(2000, passed 53–47, schools only, with a $30M elite-financed bipartisan
campaign); Washington's 2023–25 school-bond bills (all stalled); Idaho's
roughly eleven legislative attempts (none passed). The one recent non-school
attempt, California's Proposition 5 (2024), extending the 55% bar to housing
and infrastructure, failed. Where exits exist, no one spends thirty million
dollars to lower the bar. **[PENDING: the reform table is compiled from
secondary sources and marked `secondary_unverified` pending primary-record
verification; the national event-study estimates for Proposition 39 remain
inconclusive at the state grain (Section 5.2). The reform record is cited
here as evidence on reform politics, not as a causal estimate.]**

> **Table 9.1** Proposal behaviour by regime; pass-rate invariance.
> **Table 9.2** The institutional wedge. **Table 9.3** The reform record
> (appendix). **Figure 9.1** TX-2019 unbundling.

---

### Exhibit inventory (drafted ↔ to build)
| exhibit | status |
|---|---|
| T4.1 validation · T4.2 frame | numbers final |
| T5.1 menu · T5.2 panels · T5.3 coalitions · T5.4 first stage · T5.5 substitution | numbers final (rule rows labelled first-stage until pass-2) |
| F5.1 consent map | **built** (`fig_consent_map.svg`) |
| T6.1 RD · T6.2 battery incl. pay-go row · F6.1 event study | numbers final |
| F6.2 cumulative wedge | **built** (`fig_cumulative_wedge.svg`) |
| T7.1–7.4 response margin incl. rate-cap split | numbers final |
| T8.1–8.3 heterogeneity | numbers final |
| T9.1–9.3, F9.1 agenda and politics | numbers final |

*The honesty record (informative nulls, pending items, known data limits) is
the online appendix: `paper/ONLINE_APPENDIX_HONESTY.md`.*
