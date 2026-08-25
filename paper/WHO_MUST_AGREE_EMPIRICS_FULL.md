# Who Must Agree: Empirical Sections (round-3 regeneration)

*Draft 2026-08-24 (round 3). Every number traces to a committed RESULTS file
(script-to-results map in `analysis/ANALYSIS_REVIEW.md`). **[PENDING]** marks
claims held on a named data pass. The honesty record (nulls, pending items,
data limits) is included below as Appendix H. House style applied throughout:
impersonal constructions, no em dashes, British spelling. **The conference
draft is FROZEN on corpus package v3** (the finance-flag fix, verified);
package v4 and the B5 rerun land post-APSA only.*

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
corpus as the outcome of record. The conference draft is pinned to corpus
package v3 (verified 2026-08-24); later package versions enter only in the
journal revision.

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
channel 72.5%; measured in classified line counts, which are robust to the
regime imbalance in line-level dollar coverage (appendix Table A-C1), the
gradient is 17.9%, 34.5% and 54.0%. Composition exhibits report both bases. What the consent requirement governs, overwhelmingly, is the
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
counterparts in lax states; the non-chargeable project gap is −8.7 points
(t = −1.6) in dollars and **−4.7 points (t = −2.3)** in classified line
counts, the count basis being robust to the regime imbalance in classified
dollar coverage documented in appendix Table A-C1 (Table 5.5 reports both;
the text cites the count-based coefficient). This is the fifty-state
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
only; full-window cohort = votes through roughly 2017–18, outlay ending at
fiscal 2023). Nothing in the battery is hidden; the table shows all of it.

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
re-approved by voters within four years; 13 more return and wait; 5.2 borrow
through the board or statutory channel; 9.0 issue on pre-existing voter
authority; 18 are extinguished** within the horizon. The 9.0 issuing on
pre-existing voter authority draw on authorisations banked before the refused
measure and are not evidence of evading it; the substitution reading attaches
only to the 5.2 board-or-statutory cell. The
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
the broad durable electorate is the one consulted. All moderation tables run
on the 6,255 proper-grain measures (place grain for cities, district grain
for schools); special districts are excluded pending sub-county demographics
(TWDB interpolation), as each table notes. It is ownership, not affluence
(the income split is flat: +0.129 against +0.122), and institutional, not
partisan: precinct-built city partisanship and mayoral party in the 577-city
panel show no moderation (all n.s.). The coarser county-grain partisanship
splits (2020 vintage, county grain) agree and sit in the appendix.
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

*The honesty record is Appendix H below; the variable inventory is Appendix V;
the round-4 appendix tables (A-C1, A-P1) follow the main text.*

---

# Appendix A · Round-4 tables

## Table A-C1 · nc_share selection check (classified-line coverage by regime)

Coverage = corpus-active unit (nm_docs>0) with any B3-classified project $.
Weighted coverage weights units by nm_par. Regime = op_referendum_strict
(PRELIMINARY labels).

## By regime
| sample | regime | units | unit coverage | $ coverage |
|---|---|--:|--:|--:|
| all classes | strict | 12,838 | 63.5% | 82.7% |
| all classes | non-strict | 2,040 | 77.6% | 83.9% |
| all classes | not codable | 3,450 | 48.3% | 80.1% |
| general-purpose (muni+county) | strict | 3,776 | 68.7% | 90.3% |
| general-purpose (muni+county) | non-strict | 1,006 | 75.1% | 84.9% |
| general-purpose (muni+county) | not codable | 1,926 | 60.9% | 92.5% |
| schools | strict | 6,763 | 66.7% | 80.7% |
| schools | non-strict | 263 | 90.9% | 96.1% |
| schools | not codable | 604 | 3.8% | 7.7% |

Regime gaps (unit, $): all classes: 14.1%/1.1%; general-purpose (muni+county): 6.4%/5.4%; schools: 24.1%/15.4% → **UNBALANCED (>5pp) — count-based versions produced below**.

## By state (≥20 corpus-active units)
| state | units | unit cov | $ cov |
|---|--:|--:|--:|
| TX | 2,131 | 50.1% | 74.1% |
| IL | 1,345 | 60.7% | 75.3% |
| NY | 1,164 | 65.1% | 89.8% |
| CA | 927 | 46.7% | 79.9% |
| MN | 805 | 79.8% | 94.5% |
| MI | 790 | 72.2% | 91.3% |
| MO | 741 | 70.0% | 91.6% |
| NE | 741 | 72.6% | 92.0% |
| WI | 701 | 85.2% | 97.9% |
| IA | 693 | 74.6% | 93.6% |
| PA | 603 | 3.8% | 7.5% |
| IN | 566 | 4.8% | 9.1% |
| OH | 547 | 77.7% | 89.3% |
| OK | 534 | 56.0% | 88.1% |
| CO | 513 | 45.8% | 74.4% |
| KS | 452 | 88.3% | 96.7% |
| FL | 425 | 42.1% | 90.0% |
| WA | 404 | 75.0% | 89.2% |
| NJ | 399 | 60.7% | 80.6% |
| MA | 314 | 85.0% | 96.0% |
| GA | 284 | 50.7% | 71.9% |
| KY | 283 | 89.8% | 98.1% |
| AR | 255 | 71.0% | 84.7% |
| AL | 248 | 96.0% | 97.5% |
| OR | 245 | 74.3% | 89.9% |
| ND | 219 | 67.1% | 93.4% |
| AZ | 202 | 73.8% | 95.0% |
| CT | 164 | 90.2% | 96.9% |
| SD | 159 | 74.8% | 90.1% |
| TN | 157 | 66.9% | 91.3% |
| MS | 155 | 50.3% | 65.2% |
| SC | 129 | 54.3% | 64.7% |
| UT | 128 | 80.5% | 86.1% |
| LA | 114 | 60.5% | 80.0% |
| NM | 113 | 65.5% | 97.3% |
| NC | 112 | 82.1% | 97.0% |
| MT | 111 | 40.5% | 51.2% |
| ID | 91 | 65.9% | 82.6% |
| VA | 75 | 74.7% | 95.6% |
| ME | 60 | 85.0% | 98.0% |
| WV | 40 | 85.0% | 86.9% |
| MD | 37 | 67.6% | 96.0% |
| NH | 36 | 80.6% | 97.5% |
| RI | 34 | 88.2% | 96.8% |
| NV | 30 | 96.7% | 99.8% |
| WY | 29 | 55.2% | 79.2% |

## Count-based B3 channel sorting (classified LINES, not $)
| auth mode | ch lines | nc lines | chargeable share (count) |
|---|--:|--:|--:|
| voter | 15,707 | 71,961 | 17.9% |
| council_or_board | 62,488 | 118,544 | 34.5% |
| statutory | 7,912 | 6,727 | 54.0% |
| refunding_no_new_election | 3,174 | 4,311 | 42.4% |
| unknown | 3,840 | 6,993 | 35.4% |

## Count-based N2 (general-purpose): nc line share ~ strict + controls
β(strict) = **-0.0470**, state-cluster SE 0.0209, t -2.25, n 4,600, clusters 46.
(Dollar-based v3 counterpart: −0.087, t −1.61.) The text may cite whichever
the coverage table justifies; both appear in the appendix.

## Table A-P1 · County-grain partisanship (demoted from the text)

County presidential two-party splits of the authorisation effect (GO issuance
≤6y, bw ±10; county Dem share attached to 85.7% of the RD frame): below-median
+0.121 (z 2.60) against above-median +0.111 (z 2.30); terciles +0.163 (most
Republican) / +0.072 / +0.120 (most Democratic), non-monotone. National
first-stage interaction (entity panel, v3): strict × county Dem −0.65
(t −2.0), descriptive. Caveat: 2020 vintage only, county grain, a coarse
proxy for district electorates. The main text's partisanship null cites the
precinct-built 577-city panel only, which agrees (all subgroups n.s.).

---

# Appendix H · The honesty record

*Moved verbatim from the main text per the round-3 adjudication, updated for
P4/P5. The register of informative nulls, pending items and known data limits
that the paper carries.*

## Informative nulls
- Partisanship (three measures, two grains: county presidential, precinct
  city-footprint, mayoral party): no moderation of the authorisation effect.
- The extensive margin nationally: the coded rule does not predict whether a
  government borrows at all, only the channel and composition.
- Entity midwifery: no detectable spawning of new issuers in refused units'
  counties (coarse grain, low power).
- The D2b signal test: no jump in the response at the symbolic 50% line among
  institutional failures.
- TEL by rule on the big-city subpanel: null, power-limited by design (large
  cities are the exit-rich class).
- P4 rate-cap split: the banked-authorisation mechanism is neither supported
  nor excluded (9 uncapped conversions; point direction opposite); the fact
  stands unexplained.

## Pending items, each blocking a specific claim
- Rules human pass-2 (21 cells, with the owner): C2/H2 finals; causal upgrades
  of the fifty-state first-stage and substitution results; the township rule
  column (town-meeting states break the municipality proxy).
- Proposition 39 district-level design (state matching-fund controls; CDIAC
  pre-2005 issuance for the composition margin): journal-version item, not to
  be started before the conference draft ships.
- B5 audit disagreement review (9 pairs; upgrades the 80% bridge precision).
- Ten-year-plus horizon pass on the re-approved-but-unissued cohort.
- Special-district demographics beyond county proxy (TWDB and shapefile
  interpolation).
- R1 reform table: secondary_unverified pending the owner's primary-record
  verification.
- IL and IN vote margins (harvest scoped and paused).

## Appendix tables added in round 4
- **Table A-C1 (nc_share selection check):** classified-amount-line coverage
  by state and regime, unit- and dollar-weighted (`NC_COVERAGE_RESULTS.md`).
  Coverage is regime-UNBALANCED on the unit margin (schools 24.1pp,
  general-purpose 6.4pp), so every composition exhibit reports a count-based
  version beside the dollar-based one; the text cites the count-based
  general-purpose coefficient (−0.047, t −2.25) and both channel-sorting
  gradients (dollars 11.3/60.0/72.5; counts 17.9/34.5/54.0).
- **Table A-P1 (county partisanship, demoted from the text):** county
  presidential two-party splits of the authorisation effect (+0.121 against
  +0.111; terciles +0.163/+0.072/+0.120, non-monotone) and the national
  first-stage interaction (−0.65, t −2.0). Caveat: 2020 vintage only, county
  grain (a coarse proxy for district electorates). The text's partisanship
  null cites the precinct-built 577-city panel only.
- **Moderation-table note (all D5/H3 tables):** estimates run on the 6,255
  proper-grain measures (place for cities, SAIPE/ACS district grain for
  schools); special districts excluded pending sub-county demographics (TWDB
  interpolation).
- **Fate-table labels:** "issued anyway" is split into board/statutory
  channel (5.2) and pre-existing voter authority (9.0); the latter is not
  evidence of evasion of the refused measure.
- **Version pin:** the conference draft is frozen on corpus package v3;
  package v4 and the B5 rerun are journal-revision items.
- **Pay-go bound cohort:** the outlay row's full-window cohort is votes
  through roughly 2017–18 with outlay ending at fiscal 2023.

## Known data limits, stated where used
- Louisiana parish-fold grain (outcome mixes measures within a parish).
- Minnesota school-purpose classification gap (empty E4 cell is a
  classification fact, not evidence).
- GFD security split (FFC/NG) unreported after 2005 for every entity type and
  degenerate for schools before (FFC is 100% of school long-term debt by
  classification); the corpus security class carries that outcome.
- GFD capital outlay: total only (construction not itemised in the compact;
  F-33 not in the repo); no outlay items in the 2024 public-use continuation,
  so outlay windows end at fiscal 2023.
- Texas BRB counts-unknown placeholder rows ("1-0", 3,188 rows) excluded from
  coalition-size panels; no RD estimate affected.
- Corpus truncation at 2005 (EMMA era).
- Moderator coverage is within-matched (ACS and SAIPE bridges); matched
  subsets are not representative of unmatched units.
- Consent-map coverage: ten states carry no determined-mode dollars (an
  extraction-coverage fact, shown as missing rather than imputed).

---

# Appendix V · Variable inventory by section (§§4–9)

*Reference document, 2026-08-24, computed on the current panels (corpus package
v3). "Panel" = the 40,924 crosswalked referenda; "RD frame" = rd_sample ∩
bond_go, 11,889 measures. Coverage figures are non-blank counts from the
committed files, not estimates. Conditional variables state their own
denominator. British spelling; no em dashes.*

---

## §4 · Data (identity, treatment definition, validation)

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `unit_id` / GID | 9-char Census government ID (state2+type1+county3+unit3) | unit | crosswalk | 40,924/47,235 referenda (86.6%) | exact tiers ~100% verified; fuzzy tier 95.1% RA-audited |
| `pct_yes` | yes share of the vote | referendum | 9 state registries | 75% of panel; **100% of RD frame** | IL/IN carry results only (no margin) |
| `threshold_centered_margin` | pct_yes − applicable threshold | referendum | derived; CA threshold per measure from CDIAC | 75% / **100%** | the running variable |
| `rd_sample` | at a genuine mandatory-ballot statutory cutoff | referendum | rules coding of the 9 states (direct, not the national panel) | 23,577 flagged | RD-state cutoffs are bedrock statutes, outside the pass-2 worklist |
| `purpose_class` | bond_go / bond_other / tax etc. | referendum | per-state purpose mapping | 100% | MN school classification gap flagged |
| `auth_mode_final2` | OS-evidenced authorisation mode (voter / council_or_board / statutory) | document | corpus extraction | 93.7% of docs determined (v3) | validated: date match 67.9% pooled, 95.4% WI; matched→passed 91.3% |
| `op_referendum_strict` (+ ordinal, threshold_num) | coded rule, state × entity × purpose × year | state×entity×year | rules panel | 89% of panel rows; muni cell codable in 37 states | **PRELIMINARY pass-1; 21-cell pass-2 with owner** |

## §5 · Landscape and fifty-state first stage

**Grain: one row per local government (entity panel, 90,604 units) or per
document (corpus).**

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `nm_docs`, `nm_par` | new-money issues and par, 2005–25, canonical per issue | unit | corpus v3 | 78,672 typed nm issues; 46 states ≥50 docs | 5 small states below gate (DC/DE/HI/VT/WY); 5 legacy states 72–87% flag coverage (MN/MA/MO/MD/ID) |
| `sec_go_sh` … `sec_sptax_sh` | par shares by security pledge class | unit | corpus | where nm_par>0 | GO / revenue / lease / special_tax |
| `voted_sh_par`, `council_sh_par`, `statutory_sh_par` | mode shares of determined nm $ | unit | corpus | 13,875 units with a determined split | the first-stage outcome |
| `nc_share_project` | non-chargeable share of classified project $ | unit | B3 doc flags (118-label map, 0 unmapped) | ~18% of units | classified printed-amount lines only |
| ballot purposes (M2 panel A) | normalised keyword categories | referendum | 9 registries | 19,600 bond measures | stand-in for a formal B1 taxonomy (flagged) |
| votes cast / yes-needed (M3) | counts and threshold×total | referendum | TX/WI/LA/NC registries | 7,473 GO measures | CA has % only; 3,188 TX placeholder rows excluded; LA also carries voters_qualified/voted |
| GFD characteristics | pop or enrolment, revenue, own-source, property tax, LTD out | unit, latest yr ≥2012 | national GFD | 100% of entity panel | specials lack Population (revenue-size proxy in N-suite) |
| ACS covariates | homeownership, 65+, fractionalisation, median income | place (munis) / county (rest) | ACS5-2019 national pulls | ~100% | county layer uniform; place upgrade for cities |
| `county_dem2p_2020` | county Dem two-party share | county | MEDSL | 99–100% | 2020 only |
| FOG institutions | form of gov, initiative, referendum, partisan, districts | city | FOG panel | ~570 big cities | subpanel only |
| TEL stringency; ACS-2022; city Dem; mayor party | big-city extras | city | municipal-analysis panels | ~570 cities each | 2013-vintage TEL, no time variation |
| rule (per class) | strict for the unit's entity class | state×entity | rules panel | county 94% · schools 93% · specials 79% · munis 68% · townships 50% (proxy) | township column = pass-2 Part C |

## §6 · The RD core (frame: 11,889 GO measures)

| variable | definition | level | source | coverage in RD frame | window |
|---|---|---|---|---|---|
| `issued_6y` | any issuance ≤6y | referendum | corpus link | **100%** | (0, +6y] |
| GO issuance ≤6y | issued_6y ∧ go_share>0 | referendum | corpus | 100% (go_share observed for 64%, else 0-issue) | headline outcome |
| `nm_par_6y`, `ln_par_pc_6y` | new-money par; ln(1+par p.c.) | referendum | corpus + GFD denominator | 100% / 86% | denominator = gfd_pop, enrolment for schools (65% of frame are schools) |
| `ln_gfd_ltd_pc_6y` | survey LTD issued p.c. (EMMA-independent row) | referendum | GFD + IUF FY23/24 | 73% | fiscal [y+1,y+6]; IUF validated 99.9% |
| capital outlay p.c. (pay-go bound row) | GFD Total_Capital_Outlays p.c. | referendum | GFD | 83% with a 6y window (8,489/10,244 with denominator) | ends FY2023 (IUF has no outlay); total outlay only |
| `ev_m2…ev_p5` | any nm issue in relative year k | referendum×year | corpus | 100% | event study |
| balance covariates | pre-vote GFD pop, revenue p.c., debt p.c., taxes, enrolment, prior failure | referendum | GFD | 94–98% | 0/7 imbalanced |
| McCrary/density inputs | binned margin counts | bin | derived | full frame | TX-driven excess |

## §7 · The response margin (denominators are conditional)

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `resubmitted_4y`, hazard, KM | same-unit+class return ≤4y | failed measure | panel sequences | 2,680 failed GO measures (the denominator) | risk sets censored at registry end |
| return pass / amount ratio | outcome of the return | return | registries | 1,418 returns; 1,354 with amounts | amounts CA/TX/WI |
| fate table categories | converted / returned / issued-anyway / extinguished | failed measure | corpus + sequences | 1,233 (2005–19 full windows); 422 close | mutually exclusive |
| first-issue authoriser | mode of first post-vote nm issue | referendum | corpus | close window n=2,234 | transition matrix |
| continuation (B5) | window doc sharing the ballot's purpose category | measure×doc | FN2CAT bridge | 3,854 close categorisable measures | bridge precision 80.0% / recall 88.9% (blind audit); reruns on v4 |
| bundle recomposition | categories kept/dropped on return | failure→return pair | bridge | 1,129 pairs | |
| P3 chain | pass→first-issue timing; 8y issuance | conversion | corpus | 132 CA conversions (118 capped / 14 uncapped) | uncapped cell too thin (P4 not confirmed) |

## §8 · Heterogeneity (moderators; split at within-frame medians)

| variable | definition | level (grain) | source | coverage in RD frame | notes |
|---|---|---|---|---|---|
| `acs_homeown/share65/frac/medinc` | proper-grain moderators | **place 2,103 · SD 4,152 · county 5,329** | ACS5 2010/2019 (pre-vote vintage rule) | 97% attached | proper-grain-only splits use the 6,255 place+SD rows |
| `sd_childpov_rate` | district child poverty (income proxy) | school district | SAIPE name-bridge | 35% of frame (4,153 schools) | match rates vary (MN 91% … CA 44%); within-matched validity |
| county moderators | 65+, frac, income (first-pass proxy) | county | CC-EST + SAIPE | 97.4% | superseded by proper grain where available |
| `county_dem2p` (pre-vote) | partisanship | county | MEDSL | 85.7% | null result |
| city Dem share, mayor party | large-city partisanship | city (precinct-built) | municipal-analysis | 1,932 municipal measures in 577-city panel; 178 within ±10 | replicate-the-null only |
| Gini (D6) | B19083 | place/SD/county | new CA pull (2010+2019) | CA cells (blocked-majority analysis) | D6 is CA-only by construction |
| election timing | on-cycle = Nov of even year | referendum | dates | 100% | |
| entity class (fork) | census_type | unit | crosswalk | 100% | schools 7,690 · GP 2,623 · specials 1,576 |

## §9 · Agenda margin and politics

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| proposals /100 districts/yr; median ask; on-cycle share | E4 regime comparison | state×year | registries + GFD district counts | CA/TX/WI (MN = classification gap) | |
| pass rates by regime | E3 | regime | registries | 11,888 with margins | invariance at 50 vs 55; breaks at 66.7 |
| props/election; multi-prop share | TX-2019 unbundling | district×election | TX BRB | 2014–25 | reporting-mandate caveat |
| W1/W2 wedge cells | issuance by support band × regime | band×state group | panel | 50–55 band: CA 187 / TX+WI 653 | the DiD-at-fixed-support |
| reform events | attempts/outcomes since 1990 | state×event | web compilation | 11 rows | secondary_unverified (owner) |
| Prop 39 / M56 DiD outcomes | ln per-pupil (per-capita) LTD issued | state×year cells | national GFD 1997–2013 | schools ≥20 districts/cell, 39–48 states | state-mean grain; district-level upgrade deferred |

---

### The three load-bearing coverage facts a referee will probe
1. **RD outcomes are 100%/86% covered in-frame** (binary/intensive) and the
   survey replication row (73%) is symmetric across the cutoff; crosswalk
   selection is Lee-bounded.
2. **Moderator grains are honest**: place for cities, district for schools
   (SAIPE/ACS-SD), county fallback (all specials); splits are within-matched
   and labelled; nothing is imputed.
3. **National corpus coverage post-v3**: 46 states above the 50-doc gate; the
   residuals are five thin small states and five legacy partial-fill states,
   both listed; rule coding 68–94% by class with the township proxy flagged.
