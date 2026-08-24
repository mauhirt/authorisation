# Who Must Agree — Empirical Sections (full draft for review)

*Draft 2026-08-24, from repo state through the N6 commit. Every number traces to
a committed RESULTS file (script→results map in `analysis/ANALYSIS_REVIEW.md`).
Bracketed **[REVIEW]** notes mark author decisions; **[PENDING]** marks results
that cannot be cited as final until the named data pass lands. Table/figure
callouts name the exhibit that fills the slot.*

---

## 4 · Data: observing the consent requirement end to end

Testing a theory of authorization rules requires observing three things that no
single dataset contains: the **rule** (who must agree, at what threshold), the
**asking** (what governments put before voters, and what happened), and the
**borrowing** (what was ultimately issued, under what security, for what
purpose, and — critically — on whose authority). We assemble all three at the
level of the individual local government, nationwide, and at the level of the
individual referendum in nine states.

**Referenda.** We compile 47,235 local bond and tax referenda from nine state
administrative sources: California (CDIAC), Texas (Bond Review Board), Wisconsin
(DPI), Louisiana (Secretary of State), North Carolina (NCSBE), Massachusetts
(DLS Proposition 2½ databank), Minnesota, Illinois, and Indiana. Each measure is
crosswalked to its Census of Governments unit: 40,924 (86.6%) resolve to a
government ID, with exact tiers verified at ~100% and the fuzzy-match tier
independently audited by a research assistant at 95.1% accuracy. Restricting to
measures at a *genuine mandatory-ballot statutory cutoff* leaves 23,577; the
regression-discontinuity frame is its general-obligation-bond subset, **11,889
GO measures** (Texas 8,062, California 2,189, Wisconsin 999, Louisiana 361,
North Carolina 278) across three thresholds: 50% (TX, WI, LA, NC), 55%
(California schools), and 66.7% (California non-school), with California
thresholds assigned per measure from CDIAC.

**Borrowing, with its authority attached.** The outcome side combines two
independent sources. First, a corpus of 258,762 official statements (2005–2025,
all fifty states; 43,030 issuers), from which we extract, for every issue: par,
security pledge class (GO / revenue / lease / special tax), use-of-proceeds
lines classified into 118 functional activities, and — the variable this paper
turns on — the **authorization mode evidenced in the document itself**: voter
approval (with the election date the OS cites), governing-board action, or
statutory authority. Second, the Census Government Finance Database (1967–2023;
2.1 million local unit-years) and its 2022–24 public-use continuation, giving a
survey-based issuance measure that includes the bank loans and private
placements no official statement records. The two sides share the Census
government ID, so every referendum, every OS, and every survey year of the same
government link deterministically.

**Validation.** Because the authorization mode is extracted, not administrative,
we validate it against the election record before using it (Table 4.1). Where an
OS cites an election date, that date matches a referendum we independently
observe for the same unit 67.9% of the time pooled — and 95.4% in Wisconsin,
the state whose registry is known-complete; conditional on a match, 91.3% of
cited elections are *passed* measures (98.0% in California, 98.8% in North
Carolina). Shortfalls concentrate exactly where registry coverage is
known-short (Minnesota's registry begins in 2020; Massachusetts dates votes at
month grain), and the voter-mode support rate (76.2% of voter-mode new-money
documents have a passed referendum within six years in our records) is a lower
bound driven by authorizations older than our windows — Texas districts issue
against decade-old voter authorizations in series. The survey side is validated
in the other direction: the 2022 public-use file's issuance item matches the GFD
within 0.5% for 99.9% of bridged units.

**The rules panel.** State × entity-type × purpose × year coding of referendum
requirements (threshold, ballot mandate, stringency). **[PENDING]** The panel is
a first-pass machine coding cross-validated at 78% (29/37 codable states)
against an independent hand coding; a 21-cell human verification pass is in
progress. Until it lands, every rule coefficient below is presented as a
*first stage* — the association between the coded rule and observed
authorization behavior — never as a causal estimate. The convention is marked
in each table note.

> **Table 4.1** Validation of extracted authorization fields (by state: date
> match, matched→passed, voter-mode support, council-mode consistency).
> **Table 4.2** Frame construction (universe → crosswalked → cutoff sample → GO
> RD frame), with per-state counts.

---

## 5 · The institutional landscape: what consent governs, and for whom

Before estimating anything, we document the object. Three facts organize
everything that follows.

**Fact 1: entity types hold radically different menus of exits from the voted
channel.** Table 5.1 tabulates, for the national new-money corpus (59,912
canonical issues), the share of determined dollars authorized *without* a vote,
by entity type. School districts route only **29.8%** of new-money dollars
through non-voted channels; townships 48.8%; special districts 68.5%; counties
**80.9%**; municipalities **82.7%**; and authority-class issuers (housing,
health-hospital, utility conduits) **96.8%**. The full matrix (security class ×
authorization mode, per entity and rule regime) shows why: a school district's
menu is essentially GO-or-nothing, while a city can finance most of what it
does through revenue bonds, leases, and conduit authorities that never face an
electorate. "Who must agree" is not one institution: it is a menu that varies
by the kind of government doing the asking.

**Fact 2: the balloted local state is the non-chargeable civic core; the
chargeable perimeter never votes.** Classifying ballot purposes across 19,600
bond measures, K–12 schools alone account for 38.2% of everything put before
voters, followed by water/sewer, roads, parks, and fire protection (Table 5.2,
Panel A). Panel B lists the corpus functions whose dollars are voted on less
than 2% of the time: public hospitals ($197.5B of local project dollars),
multifamily housing ($69.1B), electric generation ($67.0B), gas utilities,
airport terminals. A $0.84B Harris County Hospital District line, San
Francisco's multifamily housing revenue program, Energy Northwest's generation
debt — none faced a ballot; Los Angeles Unified's $9.0B ask in 2024 did. The
nationwide sorting is stark at the channel level: the voted channel carries
**11.1%** chargeable dollars; the board channel 60.5%; the statutory channel
72.5%. What the consent requirement governs, overwhelmingly, is the class of
goods that cannot be charged to users — precisely the goods H2 says it should.

**Fact 3: the same legal sentence assembles coalitions that differ by five
orders of magnitude.** Where vote counts exist (TX, WI, LA, NC; 7,473 GO
measures — California's CDIAC reports percentages only), the median school bond
was decided by **768** yes-votes; the median off-cycle city measure by
**1,179**; the median special-district election by **34**. Under the identical
Texas 50% rule, Harris County's road program required 511,375 yes-votes of
1,022,748 cast, while a developer municipal utility district was authorized by
**two votes of two cast** (Table 5.3). The "coalition" a referendum requirement
demands is not a constant of the law but a variable of the electorate the law
convenes — the observation that motivates the heterogeneity analysis of
Section 9. **[REVIEW: Harris-vs-MUD is the paper's most quotable exhibit —
main text or box?]** (Texas rows with the registry's counts-unknown placeholder
convention — 3,188 rows recorded "1–0" — are excluded and documented; no RD
estimate is affected.)

> **Table 5.1** The menu matrix: non-voted share of new-money dollars by entity
> type (+ security × mode detail in appendix). **Table 5.2** The balloted and
> submerged local state. **Table 5.3** Absolute coalition sizes (votes cast,
> yes-votes required; p10/p50/p90 by entity × election timing).

---

## 6 · The rule and the channel: fifty-state evidence

We first ask whether coded rules predict observed authorization behavior across
the whole local state — the empirical first stage of the institutional claim,
and the validation screen for the rules panel itself.

**Design.** We build a panel of **90,604 local governments** — every county,
municipality, township, school district, and special district in the national
GFD universe — carrying (i) the coded rule for its class (strict referendum
requirement for GO debt vs not), (ii) demographic and fiscal characteristics
(population or enrollment; revenue, property tax, debt stock; ACS homeownership,
age, diversity, income at place grain for cities and county grain otherwise;
county presidential partisanship), and (iii) its borrowing 2005–25 from the
corpus (security class, authorization mode, purpose composition) and 2005–23
from the survey. A ~570-city subpanel adds form-of-government institutions,
tax-and-expenditure-limit stringency, city-level partisanship, and mayoral
party. Estimation: WLS with state-clustered standard errors, Census-region
fixed effects, and the characteristics above as controls.

**The rule shows up in behavior — most where the theory says it must.** Under a
strict rule, the OS-evidenced voted share of determined new-money dollars is
higher by **+0.78 for school districts (t = 7.0)**, +0.20 for special districts
(t = 3.2), +0.17 for municipalities (t = 2.9), and +0.14 (n.s.) for counties
(Table 6.1). Raw magnitudes tell the same story: 72.5% of school dollars are
voted under strict rules against 7.5% under lax ones; 22.1% against 5.0% for
cities. The one reversal — townships, 18.2% strict vs 46.6% non-strict — is
itself diagnostic: townships carry a proxy (municipality) rule in the panel,
and New England towns borrow by town-meeting vote in states coded lax for
cities. The panel is telling us the coding needs a township class; we flag it
rather than absorb it. **[PENDING: rules pass-2; the township column is now on
its worklist.]**

**Cities under strict rules substitute away from the voted instrument.** At the
unit grain with full controls, general-purpose governments in strict states
carry a GO security share **34.5 points lower** (t = −5.1) and a non-chargeable
project share **17.1 points lower** (t = −3.3) than their counterparts in lax
states (Table 6.2). This is the fifty-state generalization of the sorting in
Fact 2: where the GO instrument requires a coalition, governments that *can*
finance through chargeable, unvoted instruments do. The state-level FE version
of the same test (non-chargeable share on rule stringency, weighted, 45 states)
gives −0.162 (t = −1.83). **[PENDING: both are held as first-stage/descriptive
until the rules pass-2; the coefficient stability across grains is the reason
to expect the final version to survive.]**

**The extensive margin is quiet.** Whether a government borrows *at all*
(2005–25) and how much it issues in survey totals are not significantly
associated with the rule (t ≈ −1.3). The rule moves the channel and the
composition, not the existence of borrowing — exactly the pattern the
regression-discontinuity results of Section 7 rationalize: authorization rules
operate on *when* and *how*, less on *whether*.

**Reform events: the honest state of play.** The strongest available national
causal design — California's Proposition 39 (November 2000), which cut the
school threshold from two-thirds to 55% while leaving every other California
government and every other state untouched — does not yet deliver a verdict at
the state-mean grain: the schools-only DiD is +0.45 log points (permutation
p = 0.15 across 49 placebo states) with a visible pre-trend, and the
sector-differenced triple-diff is ≈ 0. Two data facts discipline the design:
GFD's pre-2005 security split is degenerate for schools (FFC ≡ 100% by
classification), so the COP→GO composition shift Prop 39 should produce is
invisible in Census data; and California's state matching-bond waves (Props 47
and 55, 2002/2004) confound the totals margin. **[PENDING: the publishable
version is a district-level two-way-FE design with enrollment weights,
Conley–Taber inference, OPSC matching-fund controls, and the CDIAC issuance
database (CA security types to 1985) for the composition margin. Oregon's
Measure 56 (2008) is retained as a sketch only — it sits on the financial
crisis.]** We therefore let the reform record play its role in Section 10 as
evidence on the *politics* of the rule, and rest the causal weight on the
within-state designs of Section 7.

> **Table 6.1** First stage: voted $ share on strict rule, by entity class
> (controls, region FE, state clusters). **Table 6.2** Substitution: GO
> security share and non-chargeable share on strict rule. **Figure 6.1** The
> geography of consent: observed voted share of local new-money debt by state
> × entity. **[REVIEW: map figure not yet generated — one script away from the
> panel.]**

---

## 7 · Authorization at the margin: regression-discontinuity evidence

**Design.** For the 11,889 GO measures at statutory thresholds we compare
governments that barely won authorization to those that barely lost it, in the
threshold-centered vote margin. Identification requires that nothing else
changes discontinuously at the cutoff; we present the full battery below.
Estimation is local-linear with a triangular kernel; following the round-2
convention we report **robust bias-corrected (RBC) inference as the lead**
(local-quadratic at h, robust variance — the ρ=1 case of Calonico–Cattaneo–
Titiunik) with conventional estimates alongside.

**The naive gap, and what survives design discipline.** Passed measures are
followed by issuance 35.6% of the time against 14.6% for failed ones — a 21-
point gap that is mostly selection. At the cutoff, the six-year effect of
authorization on GO issuance is **+11.0 points (RBC, robust z = 2.30;
conventional +14.6, z = 4.47)** at the ±10 bandwidth; any-issuance gives
+11.6/+14.4. The effect replicates state by state across three different
thresholds — California +16.6 (z 3.0), Texas +14.1 (z 3.3), Wisconsin +21.2
(z 3.1) — three statutes, one answer. Louisiana's negative cell (−27.6,
z −1.9) is a data-grain artifact (measures fold to the parish); excluding it
moves the pooled estimate to +16.2. **[REVIEW: which number leads the abstract —
+0.110 RBC or +0.146 conventional? Current: RBC first, conventional beside.]**

**The intensive margin doubles, in two independent sources.** Log new-money par
per capita rises +0.92 (z 3.0) in the disclosure corpus and — decisively for
the survivorship critique — **+0.83 (z 3.3) in the Census survey measure**,
which includes the bank loans and private placements no OS records; both are
RBC-stable (+0.94, +0.88) and the survey pre-period placebo is null (+0.41,
z 1.5).

**Validity.** Covariate balance: 0 of 7 pre-vote fiscal covariates imbalanced
at ±5 (max |t| = 1.36). Density: there is excess mass just above the cutoff
(McCrary θ = +0.24, z = 4.6) — it is Texas-specific (TX +0.21, z 2.7; every
other state ≈ 0), carries the signature of endogenous proposal timing
documented since Cellini–Ferreira–Rothstein (2010), and is itself agenda-margin
evidence (Section 10); identification survives it, because donut estimates
excluding the contested region are stable to *larger* (+0.19 to +0.20, z
3.7–5.3). Inference: state-of-the-art alternatives agree — clustering by unit
(z 4.11) or county (z 3.47); Lee bounds for crosswalk selection at trim 2.52%
are [+0.138, +0.163]; randomization inference in the ±2 window rejects at
p < 0.0002 (0 of 5,000 permutations). The two flexible-fit diagnostics that do
not reject — the IK bandwidth (h = 1.8pp, τ ≈ 0) and RBC at ±5 (CI
[−0.09, +0.17]) — are reported with their reconciliation: on two points of
support, slope terms absorb a level shift that the design-based tests at the
same window detect decisively. Nothing is hidden; the table shows all of it.

**It is a timing effect — and the wedge is measurable.** The event study loads
the entire effect on the vote year (τ₀ = +0.236, z = 7.8; every pre- and
post-year ≈ 0). Cumulative curves for the |margin| ≤ 5 window (Figure 7.2) turn
this into the paper's quantities: among six-year issuers, the median
barely-authorized government reaches the market in **0.33 years**; the median
barely-refused one in **1.15** — a delay of **0.8 years** — and the refused
side *never* reaches the authorized side's end-of-vote-year issuance level
within six years. By year six, 50.1% of barely-refused governments have still
issued nothing, against 40.0% of barely-authorized ones: a ten-point wedge that
is the durable residue after all catch-up.

> **Table 7.1** Main RD estimates (RBC lead + conventional; extensive and
> intensive margins; per state). **Table 7.2** The validity battery (one row
> per check). **Figure 7.1** Event study. **Figure 7.2** The cumulative wedge
> (committed: `fig_cumulative_wedge.svg`).

---

## 8 · The response margin: what refusal buys

The theory's distinctive claim is that a coalition requirement prices *delay*,
not denial. We follow every refused measure forward.

**Refusal is a pause.** Of 2,680 failed GO measures, the re-submission hazard
is front-loaded — 26.7% return within a year, 22.8% of survivors in the second
— cumulating to **58.2% within four years**, with the median return at **1.02
years**: the next election. Returns win: **61.9%** pass. And districts re-ask
rather than concede: the median returning measure asks for **100% of the
original amount** (n = 1,354; only 45.9% downsize).

**The fate of the marginal refusal.** For the 2005–19 cohort with full
observation windows, per 100 *barely*-refused measures (Table 8.1): **54 are
re-approved by voters within four years; 13 more return and wait; 14 borrow
anyway on other authority** (5 via board or statutory channels, 9 on older
voter authorizations); **18 are extinguished** within the horizon. The
transition matrix behind it shows what the cutoff actually moves: voter-mode
first issuance (48.4% vs 36.7%) against no-issuance (43.1% vs 54.2%), while
board-mode first issuance is ~8% on *both* sides — the board channel is a
floor, not the treatment margin. Consistent with this, the authorization mix of
what barely-refused governments still issue tilts toward the board channel
(council share τ = −0.064, z = −2.0).

**The project itself survives.** Matching ballot purposes to the use-of-
proceeds functions of subsequent issues (deterministic category bridge,
blind-audited at **80.0% precision / 88.9% recall** — all numbers cite the
audit), same-purpose financing appears within six years for 44.7% of
barely-passed measures and **33.4% of barely-failed ones** (RD +0.072,
z = 2.1), with median arrival 0.32 vs **1.67 years**. A third of narrowly
refused *projects* get financed anyway — later. On re-submission, bundles are
not recomposed: 78.2% of original purpose categories are retained.
**[PENDING: nine disputed audit pairs queued for the disagreement review.]**

**The supermajority's distinct signature: re-approved but unissued.** Within
California, near-miss failures (majority support short of the supermajority
threshold) re-submit far more than decisive failures (42.2% vs 27.4%; 51.3% vs
30.8% among schools) and show no jump at the symbolic 50% line — the response
tracks proximity, not the majority label. Yet their issuance is *lower* — and
the deficit is not a truncation artifact: it **widens** from −5.3 points at six
years to −6.4 at eight (schools −6.7 → −8.0), under per-cell observability
restrictions. The chain shows why: near-miss failures convert by re-vote four
times as often (107 vs 25 passed returns) but the conversions sit undrawn —
median pass-to-first-issue **6.2 years** against 2.9 — and only 5.5% see a
voter-mode issue within eight years. Where the bar is a supermajority, even
re-assembled consent does not become borrowing on the study horizon.
**[REVIEW: this is a new stylized fact ("authorization banked, drawdown
deferred") — promote to its own subsection or leave inside the response
margin? A 10y+ horizon pass is queued.]**

> **Table 8.1** The fate table (per 100 barely-refused) + transition matrix.
> **Table 8.2** Re-submission hazard, pass rates, amount ratios. **Table 8.3**
> Project continuation and bundle recomposition (with audit precision).
> **Table 8.4** The near-miss chain (P3).

---

## 9 · Where the requirement binds: exits and electorates

The RD average conceals the theory's structure. Two partitions recover it.

**By exit menu.** Splitting the RD frame by entity class and aligning each
class against its *independently measured* national menu (Section 5, Fact 1):
school districts — non-voted share 29.8%, window-chargeable menu 0.4% — show
the binding effect (+0.147, z 4.0; RBC +0.123, z 2.3) and the highest
re-submission rate (59.2%); general-purpose governments — non-voted share
80.4% — show **no discontinuity at all** (+0.073, z 0.9; RBC −0.02) and the
lowest re-submission (25.3%); special districts sit between, with the largest
GO-specific jump (+0.463, z 2.8) that shrinks at any-issuance (+0.362) as part
of the gap reroutes to non-GO instruments. **[REVIEW: utilities cell is n =
1,576 — current treatment cites the ordering, flags the magnitude.]** The rule
binds exactly where the menu offers no exit; where exits exist, refusal is
nearly costless and rarely re-litigated. This is the fork the fifty-state
substitution results (Section 6) show in cross-section.

**By electorate.** At the proper demographic grain (place for cities, district
for schools), the authorization effect concentrates where property owners
dominate a stable consenting public: homeownership above the frame median,
τ = **+0.182 (z 3.5)** against +0.056 (n.s.) below; 65+ share +0.194 vs
+0.036; racial-ethnic homogeneity +0.232 vs −0.018. It is ownership, not
affluence — the income split is flat (+0.129 vs +0.122) and the district-grain
child-poverty split repeats the affluence gradient only weakly — and it is
institutional, not partisan: county presidential partisanship yields a flat
split (+0.121 vs +0.111, terciles non-monotone), replicated with precinct-level
city partisanship and mayoral party in the 577-city panel (all n.s.), and the
national first stage shows at most a *weaker channel effect* in Democratic
counties (interaction −0.75, t −2.2, descriptive). Timing matters the way a
coalition story predicts: on-cycle measures show +0.252 against +0.099
off-cycle. **[REVIEW: the homogeneity sign runs against a naive assembly-cost
reading of H3 — the "stable propertied public" reframing is drafted but
unadjudicated.]**

**The incidence of the higher bar.** Blocked majorities — measures with
majority support short of a supermajority threshold (California only, by
construction) — arise in places that sit *between* the decisive-failure and
comfortable-passage places on renter share, diversity, and inequality, and
among schools they are the **poorer** places (median household income −$3.8k
vs cleared, SE 1.5k; child poverty −2.0pp *below* cleared — the blocked are
poorer than passers but less poor than decisive failers). Descriptive, but it
locates the supermajority's demographic cost: majorities in less affluent,
mid-composition districts. **[PENDING: within-matched ACS caveat as throughout;
special districts remain on county-proxy demographics until the shapefile
interpolation pass.]**

> **Table 9.1** The fork against the menu. **Table 9.2** Moderator splits
> (ownership, age, homogeneity, income, partisanship ×2 grains, timing).
> **Table 9.3** Demography of blocked majorities.

---

## 10 · The agenda margin and the politics of the rule

**Rules discipline what is asked.** Under California's 55% bar, school
districts bring **8.8 proposals per 100 districts per year** at a median $39M,
62.7% on-cycle; under Texas's 50% bar, **20.1** per 100 at $15M, 14.1%
on-cycle; Wisconsin sits between on all three margins. Fewer, larger,
better-timed: the coalition requirement operates before any vote is cast. Pass
rates make the same point in reverse — nearly invariant between the 50% and
55% regimes (79.2% vs 77.6%), collapsing only at two-thirds (47.6%): a
moderate bar is absorbed by the agenda; an extreme bar defeats even what
selection permits. The Texas 2019 reform (HB 3) closes the loop within-state:
when the state mandated separate propositions for stadiums, natatoriums, and
performing-arts facilities, propositions per election jumped from 1.5–1.7 to
2.0–2.4 and the multi-proposition share doubled within two cycles —
bundling is a rule-governed choice, not a habit. The near-cutoff excess mass of
Section 7 belongs to this same family: proposals are timed to win.

**At fixed voter support, the rule alone moves outcomes.** In the 50–55% band,
the identical electoral result is a failure for a California school district
and a success for a Texan or Wisconsin one. The difference-in-differences
across the adjacent band gives **+11.5 points of six-year issuance (SE 4.8)**
attributable to the rule at fixed support — indistinguishable from the RD
estimate obtained from an entirely different comparison, an out-of-design
calibration that we regard as the single strongest check in the paper.

**The polity fights over the rule exactly where the theory predicts.** Since
1990, nearly every attempt to lower a local borrowing threshold has targeted
schools — the class our menu matrix shows holding the poorest exit menu:
California's Props 170 (1993, failed), 26 (2000, failed), and 39 (2000, passed
53–47, schools only, with a $30M elite-financed bipartisan campaign);
Washington's 2023–25 school-bond bills (all stalled); Idaho's roughly eleven
legislative attempts (none passed). The one recent *non-school* attempt —
California's Proposition 5 (2024), extending the 55% bar to housing and
infrastructure — failed. Where exits exist, no one spends thirty million
dollars to lower the bar. **[PENDING: the reform table is compiled from
secondary sources and marked `secondary_unverified` pending primary-record
verification; the national event-study estimates for Prop 39 remain
inconclusive at the state grain (Section 6) — the reform record is cited here
as evidence on reform *politics*, not as a causal estimate.]**

> **Table 10.1** Proposal behavior by regime; pass-rate invariance. **Table
> 10.2** The institutional wedge (W1). **Table 10.3** The reform record
> (appendix). **Figure 10.1** TX-2019 unbundling.

---

## 11 · What does not appear, and what is still open

For review completeness, the record of honest nulls and pending items that the
paper must carry:

- **Nulls, informative:** partisanship (three measures, two grains); the
  extensive margin nationally; entity midwifery (no detectable spawning of new
  issuers in refused units' counties, coarse grain); the D2b signal test (no
  jump in response at the symbolic 50% among institutional failures); TEL ×
  rule on the big-city subpanel (power-limited by design — big cities are the
  exit-rich class).
- **Pending, blocking specific claims:** rules pass-2 (C2/H2 finals; N-suite
  causal upgrades; township rule column); Prop 39 district-level design (OPSC
  controls; CDIAC issuance pull for the composition margin); B5 audit
  disagreement review (9 pairs); 10y+ horizon for the re-approved-but-unissued
  cohort; specials-grade demographics; R1 primary-source verification; IL/IN
  vote margins (harvest paused).
- **Known data limits, stated where used:** LA parish-fold grain; MN purpose
  classification gap; GFD FFC/NG split unreported post-2005 (and degenerate for
  schools before); TX BRB placeholder rows; EMMA-era truncation (2005+);
  within-matched moderator coverage.

---

### Figure/Table inventory (drafted ↔ to build)
| exhibit | status |
|---|---|
| T4.1 validation · T4.2 frame | numbers final (VALIDATION, LINK) |
| T5.1 menu · T5.2 panels · T5.3 coalitions | numbers final (M1–M3) |
| T6.1 first stage · T6.2 substitution | numbers final, **labels first-stage until pass-2** |
| F6.1 consent map | **to build** (one script on the entity panel) |
| T7.1–T7.2, F7.1 event study | numbers final (RD, P1, POLISH) |
| F7.2 cumulative wedge | **built** (`fig_cumulative_wedge.svg`) |
| T8.1–T8.4 response margin | numbers final (FAILURE, FATE, B5, P3) |
| T9.1–T9.3 heterogeneity | numbers final (D4, ACS, D5*, D6) |
| T10.1–10.3, F10.1 agenda/politics | numbers final (AGENDA, WEDGE, R1) |
