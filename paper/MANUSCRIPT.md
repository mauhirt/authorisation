# Who Must Agree: Empirical Sections

*Working conference draft. Every number traces to a committed results file
(script-to-results map in `analysis/ANALYSIS_REVIEW.md`). **[PENDING]** marks
claims held on a named data pass. The draft is frozen on corpus package v3.
Sections 1 to 3 (theory and institutional framework) are maintained
separately.*

---

## 4 · Data: seeing consent from statute to bond

The story this paper tells is simple. American local governments build
schools, water systems and roads with borrowed money. In some states, for
some kinds of government, the law says the voters must agree first. The
empirical sections ask three questions in turn: how borrowing is actually
authorised, and by whom (Section 5); what winning or losing that vote causes
(Section 6); and what happens after a refusal (Section 7). Sections 8 and 9
ask where the requirement bites hardest and how it shapes what is proposed
in the first place. Answering these questions takes three datasets, described
here in the order the argument uses them.

**First, the borrowing: the official-statement corpus.** When a local
government sells bonds, it publishes an official statement, a disclosure
document describing the issue. The corpus assembled for this paper contains
258,762 such documents, covering 2005 to 2025, all fifty states and 43,030
issuers. Three things are read out of each document. The first is what was
borrowed: the amount, and the security behind it, from **general-obligation
(GO) debt**, backed by the government's power to tax, to revenue bonds and
leases, which are backed by user charges or appropriations and typically
need no election. The second is what the money is for, with each project
line classified into 118 functional activities. The third is the variable
the paper turns on: **on whose authority the debt was issued**. An official
statement must state the legal authority for the issue, so nearly every
issue (93.7% of documents) can be coded as authorised by the voters, by the
governing board, or directly by statute. Where voters authorised the issue,
the document usually cites the election date, which allows the coding to be
checked against actual election records; the checks are summarised in
Appendix Table A13 and behave exactly as registry coverage predicts. Census
survey data play two narrow supporting roles later on (a survivorship check
and a bound on debt-free construction) and are introduced where used.

**Scale and context.** Figure [[VOLREF]] shows the landscape the rest of the paper
dissects. Accountable local governments issued $1.57 trillion of new-money
debt over 2005 to 2025 (74,395 issues by 13,235 governments, roughly $75
billion a year), with a further $617 billion flowing through conduit vehicles
that answer to no electorate. Of every determined dollar, 32 cents was
authorised by voters, 54 cents by a governing board and 14 cents directly by
statute; general-obligation debt, the instrument the referendum rules govern,
carries 54 cents. The voted layer is the smaller one throughout, but it is
where the growth has been: voter-authorised volume has roughly trebled since
its post-2011 trough.

[[FIG:F0_volume|Local borrowing and who authorised it, 2005--2025. Annual new-money issuance by accountable local governments, in billions of dollars, stacked by the authorisation mode evidenced in the offering documents. Undetermined modes (6.3% of documents) omitted from the stacks. Source: official-statement corpus.]]

**Second, the rules.** Which governments must ask? A fifty-state panel codes,
for every state and type of government, whether the default path to GO debt
runs through a mandatory ballot, and at what threshold. The coding follows
one definition throughout: a rule is **strict** when a government that wants
to issue GO debt must, by default, put the question to an election at the
polls. Rules that require only a town-meeting vote (New England), a
referendum only if citizens petition for one (Mississippi, Tennessee,
Wisconsin cities), or a vote only above a debt limit or for certain
purposes, are coded non-strict: under all of them a government can normally
borrow without facing an electorate. **[PENDING]** The panel is a first-pass
machine coding, cross-validated against an independent hand coding, with a
human verification pass in progress on the disputed cells; until it lands,
every rule coefficient is read as an association, not a causal estimate,
and each table note repeats this.

**Third, the elections.** Nine states publish administrative registries of
local bond and tax elections (California, Texas, Wisconsin, Louisiana,
North Carolina, Massachusetts, Minnesota, Illinois, Indiana). Compiled,
these give 47,235 ballot measures, of which 40,924 are matched to their
government in the Census of Governments, so that a vote can be joined to
the same government's later borrowing in the corpus. The causal design of
Section 6 uses the subset where a statute, not a local choice, sets the
pass threshold: **11,889 GO bond measures**, each with its yes share and
its statutory threshold, so that a single **running variable**, the yes
share minus the threshold, puts every measure on a common scale where zero
is the pass/fail line. Table 1 summarises the frame and its restriction
cascade. One registry caution matters for interpretation and is flagged
where relevant: the registries differ in scope (Wisconsin's covers school
referenda only), so cross-state comparisons of what appears on ballots are
never based on the registries alone.

[[EX:T1_sample]]

---

## 5 · Who must agree, and for what

This section establishes the descriptive foundation of the paper: who
authorises local borrowing in practice, which public goods ever face a
ballot, and whether the written rules actually govern behaviour. The central
observation, developed as Fact 1 below, is that "who must agree" is not one
institution. The same constitutional sentence lands on governments with
utterly different escape routes, and that variation, not the text of the
rule, is what organises everything the later sections find.

### 5.1 How borrowing is authorised: the menu, by type of government

Table 2 is the paper's descriptive anchor. For every type of local
government, it shows who authorised the borrowed dollars (voters, the
board, or statute) and what security stood behind them; Table 3 shows what
the money was for.

[[EX:D1_how_authorised]]

[[EX:D2_what_for]]

Read together, the two tables say something the institutional literature
tends to miss. **School districts are the voted sector of the local state.**
Nearly two-thirds of their dollars are voter-authorised, four-fifths are
GO debt, and essentially everything they borrow for is education. At the
other pole, **municipalities are the unvoted sector**: barely a tenth of
their dollars pass through an electorate, and the majority are revenue
bonds backed by charges rather than taxes. Counties and special districts
sit between, and townships look like small schools (mostly GO, substantially
voted), a point Section 5.4 returns to.

**Fact 1: the consent requirement lands on different menus.** Why do the
types differ so sharply? Not mainly because their statutes differ, but
because their *services* differ. A school district builds classrooms:
goods that cannot be charged to users, financeable only by taxes, hence by
GO debt, which is precisely the instrument the law makes voters approve. A
city runs water systems, car parks and utilities: chargeable services that
support revenue bonds, leases and conduit borrowing, none of which faces an
electorate. The referendum requirement is therefore not a single
institution applied uniformly; it is a constraint whose bite depends on the
**menu of exits** each government's service mix provides. Where the menu is
empty, the rule is the gatekeeper of provision. Where the menu is rich, the
rule guards one instrument among many. This single observation generates
the paper's main predictions: the causal effect of authorisation should be
large for menu-poor governments and absent for menu-rich ones (Section 8
confirms exactly this ordering), and political fights over the rule should
concentrate on the menu-poor class (Section 9 shows they do). The full
matrix of security by authorisation mode, per type and rule regime, is
Appendix Table A5.

### 5.2 Which public goods face voters

Table 4 turns from who borrows to what the public is asked about, measured
in the national corpus rather than in any state's election registry, so the
composition of a registry cannot skew it.

[[EX:D3_function_voted]]

The gradient is steep and it runs along chargeability. Education dollars
are voted on nearly two-thirds of the time. The civic middle (parks, public
safety, roads, water) is voted on a quarter to a half of the time. The
chargeable perimeter is essentially never voted: utilities, housing and
general-government office debt run at single digits. And the table
understates the pattern, because it covers governments with an identifiable
electorate; the conduit authorities that finance hospitals, multifamily
housing and power projects have none, and at the fine activity grain those
functions are voted on around 2% of the time (Appendix Table A6 lists them:
$197.7B of hospital projects, $70.0B of multifamily housing, $67.1B of
power generation, essentially none of it balloted). What the consent
requirement governs, in practice, is the class of goods that cannot be
charged to users. That is worth stating plainly: the referendum is not how
America governs local borrowing; it is how America governs the
non-chargeable core of local borrowing, which is why school districts,
whose output is entirely non-chargeable, live under it almost alone.

### 5.3 The coalitions the same rule convenes

The written rule names a threshold, but a threshold is not a coalition. What
a "50% requirement" demands depends entirely on who turns out, and turnout
is a function of what kind of government is asking and when. Table 5 makes
this concrete with the four states whose registries print vote counts.

[[EX:A5c_coalitions]]

The same Texas sentence that made Harris County assemble half a million
yes-votes for its road programme authorised a developer's municipal utility
district on **two votes of two cast**. This is not an anomaly; it is the
institutional design. Special districts are drawn around handfuls of
initial residents, often the developer's own employees, and their elections
occur before anyone else lives there. School bonds, held off-cycle, are
decided by hundreds of voters; city measures timed to presidential
elections are decided by hundreds of thousands. The law's language is
constant while the consenting public varies by five orders of magnitude.
Two implications follow. Empirically, election timing and electorate
composition are candidate moderators of the authorisation effect, which
Section 8 tests. Substantively, a threshold rule delegates the size of the
required coalition to whoever controls the timing and the boundaries of
the electorate, an agenda power taken up in Section 9. (Registry rows with
placeholder vote counts are excluded and documented; no estimate in the
paper depends on them.)

### 5.4 Does the written rule govern behaviour?

Everything so far describes behaviour. This subsection connects it to the
coded rules: comparing governments of the same type across state lines, is
more of their borrowing voter-authorised where the statute makes the ballot
mandatory? The test is a regression of the voted share of each government's
borrowed dollars on the strict-rule indicator, within type, across the
90,604 local governments of the national panel, with the usual demographic
and fiscal controls, region fixed effects, and standard errors clustered by
state (Table 6). Because the question is "does the rule move behaviour
within a class", the informative columns are the class-by-class ones; the
pooled column mixes classes with completely different baselines and is
shown only for completeness.

[[EX:R1_firststage]]

The rule shows up exactly where Fact 1 says it must. For school districts,
moving from a non-strict to a strict state raises the voted share of
borrowing by 69 percentage points, roughly the difference between borrowing
like a Texas district (most dollars voted) and an Ohio one (almost none).
In raw shares, 68% of school dollars are voted under strict rules against
7% under non-strict ones. For
municipalities the coefficient is a fifth the size, and for counties it is
indistinguishable from zero, not because cities ignore the law but because
so little of what they finance runs through the GO instrument the law
regulates. Figure 1 maps the result: the voted share of local borrowing
ranges from roughly 80% in Oklahoma to under 3% in New York, Pennsylvania,
Tennessee and Kentucky, the states whose statutes require no local ballot.

[[FIG:F4_consent_map|The geography of consent. Voted share of local new-money dollars by state, official-statement corpus 2005--25. States below the coverage gate (DC, DE, HI, VT, WY) are shown as no-data.]]

One reversal is instructive rather than embarrassing. Townships show the
opposite gradient (more voted borrowing under nominally non-strict rules),
because the panel assigns them their state's municipal rule, and New
England towns in fact borrow by town-meeting vote in states coded
non-strict for cities. The anomaly is the coding's, not the world's; a
township-specific rule column is on the verification worklist.
**[PENDING: rules pass-2.]**

### 5.5 Where the rule binds, governments change instruments

If a strict rule makes the GO instrument costly to use, a government with
alternatives should shift towards them, and a government without
alternatives should simply ask more often. Table 7 tests the first half on
the menu-rich class, general-purpose governments, in three steps: does the
rule change *what security* they issue (columns 1 and 2), does it change
*what kind of projects* their borrowing finances (columns 3 and 4), and
does it change *how much they borrow at all* (columns 5 and 6)?

[[EX:R2_substitution]]

The answers are: yes, yes, and no. Cities and counties under strict rules
carry a GO share of borrowing 28 percentage points lower than their
counterparts in non-strict states; their borrowing also tilts away from
non-chargeable projects (the schools-roads-parks class that only GO can
finance) and towards chargeable ones, a shift of about 5 percentage points
on the robust count basis (column 4; columns 3 and 4 measure the same
outcome in dollars and in project-line counts, and the count basis is the
one robust to a documented coverage imbalance, Appendix Table A4). But the
extensive margin is quiet: whether a government borrows at all, and how
much it raises in total, is unrelated to the rule. The requirement
redirects borrowing across instruments and purposes; it does not stop
borrowing. That is the cross-sectional face of the causal finding in the
next section, that refusal delays provision rather than preventing it.
Institutional and demographic interactions (tax-and-expenditure limits,
homeownership, partisanship) are uniformly weak (reported in the replication exhibits).

---

## 6 · What authorisation causes: evidence from close elections

**Whose elections are these?** The 11,889 GO measures at statutory
thresholds are dominated by the menu-poor sector: 65% school districts,
18% municipalities, 13% special districts and 4% counties, across Texas
and Wisconsin (50% threshold), California (55% for schools, 66.7%
otherwise), Louisiana and North Carolina. The average effects below are
therefore mostly school-district effects, and Section 8 splits every
result by type; the split is not a robustness exercise but, per Fact 1,
the theory's central prediction.

**The design, in plain terms.** A district that wins its bond election
with 50.4% and one that loses with 49.6% are the same kind of place on the
same day; the only difference is which side of the statutory line the
count landed. Comparing many near-winners with near-losers therefore
isolates what authorisation itself causes. Table 8 verifies the premise:
none of seven pre-vote characteristics (prior borrowing, size, income,
homeownership, age structure, prior failed measures) differs across the
cutoff. The one wrinkle, visible in Figure 2, is that slightly more
measures sit just above the line than just below it, concentrated in
Texas: governments time proposals they expect to win, a fact documented
since Cellini, Ferreira and Rothstein (2010) that is itself evidence for
the agenda story of Section 9. Estimates that discard the contested sliver
around the cutoff are, if anything, larger (Appendix Table A1).

[[EX:T2_covariate_continuity]]

[[FIG:F5_density|Density of the vote margin by state. Histograms of the running variable within ±10pp; the discreteness of small Texas electorates is visible. McCrary log-density discontinuity: pooled +0.24 (z 4.6) at h = 5pp, +0.14 (z 2.6) over this full ±10pp window; Texas +0.21 (z 2.7); all other states approximately zero.]]

**Authorisation raises issuance by about eleven percentage points.** Passed
measures are followed by borrowing far more often than failed ones (36%
against 15% within six years), but most of that gap is selection: popular
projects both pass and proceed. At the cutoff, where selection is removed,
authorisation raises the probability of GO issuance by 11 percentage
points (Table 9, Figure 3). The estimate replicates in every adequately
powered state, across three different thresholds, at very similar
magnitudes (Appendix Table A2); placebo thresholds show nothing (Appendix
Table A3). Borrowed amounts roughly double at the cutoff, and, decisively
for the worry that refused governments simply borrow in unrecorded ways,
the same doubling appears in Census survey data, which capture the bank
loans and private placements no official statement records.

[[EX:T3_main_results]]

[[FIG:F1_rd|Issuance at the authorisation threshold. Share of measures followed by any issuance within six years, in 0.5pp bins of the running variable sized by cell count, with local-linear fits and the RBC estimate annotated.]]

**Why a six-year window?** Passed authorisations are drawn down in series:
the median barely-passed issuer reaches the market within four months of
the vote, but districts routinely issue against an authorisation for years
(Texas districts draw on decade-old ones). A six-year window is long
enough to capture the drawdown and, more importantly, to give the refused
side time to catch up through re-votes, which Section 7 shows is the main
thing they do; a shorter window would overstate the effect by counting
delay as denial. The choice is not load-bearing: the effect is visible at
every horizon from one to six years (Appendix Figure A1), and the event
study in Figure 4 shows it arrives immediately, in the vote year itself,
with no differences before the vote and a persistent level shift after.

[[FIG:F2_event_study|Event study. Coefficient on issuance in each year relative to the vote, with robust confidence intervals.]]

**Delay, and a wedge that does not close.** Figure 5 accumulates issuance
on both sides of the cutoff. The refused side starts a year late (median
first issue 1.15 years against 0.33) and, despite six years of re-votes
and catch-up, never reaches the authorised side's level: by year six, half
of barely-refused governments have still issued nothing, against 40% of
barely-authorised ones. That ten-point wedge is the durable cost of
refusal. The full battery of robustness checks (donuts, clustering
variants, bounds for crosswalk selection, randomisation inference,
bandwidths) is Appendix Table A1; one final row there deserves mention in
text, the **pay-go bound**: rerunning the whole design with Census capital
spending as the outcome shows construction falling with borrowing at a
ratio near one. Refused districts do not quietly build anyway out of
savings; refusal delays the building itself.

[[FIG:F3_wedge|The cumulative wedge. Cumulative any-issuance for barely-passed (solid) and barely-failed (dashed) measures; the shaded area is the wedge; median market-entry times annotated.]]

---

## 7 · What happens when a measure fails

The theory's distinctive claim is that a coalition requirement prices
delay, not denial. This section follows every refused measure forward.
Table 10 collects the accounting; the text walks through it.

[[EX:T5_response]]

**Refusal is a pause, not a verdict.** Of 2,680 failed GO measures, well
over half return to the ballot within four years, most at the very next
election, and when they return they usually win. Districts do not come
back chastened: the median returning measure asks for exactly the original
amount, and four-fifths of the original purposes survive into the
re-submission. Adding up the fates of 100 barely-refused measures: 54 are
re-approved by voters within four years, 13 more have returned and await a
verdict, 9 issue on authorisations their voters had approved earlier
(banked authority, not evasion), only 5 borrow through a board or
statutory channel, and 18 are extinguished within the horizon. The
transition matrix beneath Table 10 makes the same point from the other
side: what the cutoff moves is voter-authorised issuance against no
issuance at all, while board-channel issuance sits near 8% on both sides
of the line. For the menu-poor sector, the board channel is a floor, not
an escape route.

**The project itself usually survives.** Matching each measure's stated
purpose to the classified purposes of the government's subsequent bonds, a
third of narrowly refused projects are financed within six years anyway,
against 45% of narrowly passed ones, arriving over a year later. Refusal
costs time and forces a second campaign; it only rarely kills the school
extension. And the pay-go bound of Section 6 closes the remaining
loophole: the gap is not being filled by debt-free construction.

**One exception: supermajority near-misses bank consent that stalls.**
Within California, measures that won a majority but missed the
supermajority threshold behave differently. They re-submit far more often
than decisive failures and convert to passage at four times the rate, yet
the authorisations they eventually win sit undrawn: median time from
re-vote to first issue is over six years, against under three for ordinary
passes, and their issuance deficit widens rather than closes between years
six and eight (Appendix Table A10). Where the bar is a supermajority, even
re-assembled consent does not become borrowing on the study horizon. A
candidate mechanism, statutory tax-rate caps metering the drawdown, could
be neither supported nor excluded on the available cells; the fact stands
documented and unexplained.

---

## 8 · Where the requirement binds: exits and electorates

Everything above averages over the frame. The theory says the average is
the wrong object: the effect should live where the menu is empty and die
where it is rich, and it should depend on who the convened electorate is.
Both predictions hold, and they are the paper's core results as much as
the average is.

**By type of government: the fork.** Table 11 re-estimates the design
within each class and sets the estimates against each class's national
menu from Section 5. School districts, the menu-poor class, show the
binding effect and the highest re-submission rate: for them, the ballot is
the gate. General-purpose governments, the menu-rich class, show no
discontinuity at all and rarely re-submit: for them, refusal is nearly
costless, because the same project can usually be financed through an
instrument that needs no election. Special districts sit between, and
their GO-specific jump shrinks once all instruments are counted, direct
evidence of the rerouting that Table 7 showed in cross-section. The
ordering across the three classes, binding, intermediate, absent, is
exactly the menu ordering of Table 2, estimated from entirely different
data.

[[EX:T7_fork_menu]]

**By electorate: the stable propertied public.** Splitting the frame at
its median on electorate characteristics (Table 12), the effect is
carried by places with high homeownership, older populations, and
on-cycle elections, and it is absent in renter-heavy, diverse, off-cycle
places. It is ownership, not affluence: the income split is flat. And it
is institutional, not partisan: neither city partisanship nor mayoral
party moderates anything. A natural first guess, that heterogeneity makes
coalitions harder to assemble and so weakens the effect, fails on its own
sign; the profile instead favours a **stable propertied public** account,
in which authorisation binds where the consenting public is durable
enough for its refusals to stay refused and its approvals to licence
years of drawdown. This reading was adopted after seeing the pattern and
is flagged as such. The incidence is regressive in one documented sense:
in California, the measures that win majorities but die under
supermajority thresholds come disproportionately from poorer,
mid-composition districts.

[[EX:T6_moderators]]

---

## 9 · The agenda margin and the politics of the rule

**Rules discipline what is asked before any vote is cast.** Under
California's 55% bar, school districts bring far fewer, larger, better
timed proposals than under Texas's 50% bar (Table 13): 9 against 20
proposals per hundred districts per year, at median asks of $39M against
$15M, mostly on-cycle against mostly off-cycle. Pass rates barely differ
between the 50% and 55% regimes and collapse only at two-thirds: a
moderate bar is absorbed by the agenda, an extreme bar defeats even what
careful selection permits. Texas's 2019 unbundling reform closes the loop
within one state: when stadiums and performing-arts facilities had to be
separate propositions, proposition counts jumped within two cycles.
Bundling, timing and ask size are choices the rule shapes, and the excess
of near-winners at the cutoff (Section 6) is the same behaviour seen from
below.

[[EX:A4_agenda]]

**At fixed voter support, the rule alone moves outcomes.** In the band
between 50% and 55%, the identical election result authorises a Texan or
Wisconsin district and refuses a Californian one. Comparing issuance
across that band yields an estimate of the rule's effect at fixed support,
+11.5 points (SE 4.8), indistinguishable from the RD estimate obtained
from an entirely different comparison. This out-of-design agreement is
the strongest single check in the paper.

**The polity fights over the rule exactly where the menu is empty.** Since
1990, nearly every attempt to lower a local borrowing threshold has
targeted schools: California's Propositions 170, 26 and 39 (the last
passing 53 to 47, schools only, behind a $30M campaign), Washington's
stalled school-bond bills, Idaho's dozen failed attempts. The one recent
non-school attempt, California's Proposition 5 (2024), failed. Where exits
exist, nobody spends thirty million dollars to lower the bar; where they
do not, the rule is worth fighting over, which is precisely Fact 1 read as
politics. (The reform record is compiled from secondary sources, marked
secondary-unverified pending primary checks, and cited as evidence on
reform politics only. The cleanest reform event, Proposition 39 itself,
does not yet yield a credible state-level causal estimate, because the
survey's pre-2005 security split is degenerate for schools and California's
state matching-bond waves confound the totals margin; the causal weight of
the paper rests on the within-state designs of Section 6.)

---
