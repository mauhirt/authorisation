# Who Must Agree — Findings to date

**Date:** 2026-08-24 (round 2). Every number below is output of a committed
script; the script→results map is in ANALYSIS_REVIEW.md. Frame definitions in
`paper_panel.csv`; estimators: local-linear RD (triangular kernel, HC0) with
**CCT robust bias-corrected inference as the lead convention** (`rdlib.py`:
`rd`, `rd_rbc`). This is the working findings record, not the draft.

## The estimation frame
47,235 local referenda (9 states) → 40,924 crosswalked to a Census government
(86.6%; exact tiers ~100% verified, fuzzy tier 95.1% RA-measured) → 23,577 at a
genuine mandatory-ballot statutory cutoff (`rd_sample`) → **11,889 GO-bond
measures** (TX 8,062 · CA 2,189 · WI 999 · LA 361 · NC 278) across three
thresholds (50%; CA 55 schools / 66.7 others). Outcomes: EMMA OS corpus
(258,762 docs) + Census GFD/IUF surveys, joined on the shared Census GID.

## The stage (round-2 legibility exhibits)
- **M1 · The menu.** Nationally, school districts put only **29.8%** of
  determined new-money dollars through non-voted channels; municipalities
  **82.7%**, counties **80.9%**, special districts **68.5%**, authority-class
  issuers **96.8%**. The D4 fork aligns with this independently measured menu:
  the poorest menu (schools) shows the binding discontinuity; the richest
  (general-purpose) shows none.
- **M2 · What is voted on, and what never is.** The balloted local state is
  K-12 (38.2% of measures), water/sewer, roads, parks, fire. The submerged
  local state — voted <2% of dollars — is hospitals ($197.5B), housing,
  electric generation, gas utilities, airports: the chargeable perimeter,
  financed at scale with essentially no electoral moment.
- **M3 · Absolute coalitions.** Median yes-votes that decided: a school bond
  **768**; an off-cycle city measure **1,179**; a special-district election
  **34**. Same TX 50% rule: Harris County ≈ **511,375** yes-votes; a developer
  MUD **2**. (CDIAC/CA carries no counts — % only; TX total=1 placeholder rows
  excluded, flagged.)

## F1 · Authorization binds — by ~11–15pp over six years
At the cutoff (rd_sample ∩ bond_go), GO issuance ≤6y:

| estimator | bw ±5 | bw ±10 |
|---|--:|--:|
| conventional local-linear | +0.114 (z 2.48) | +0.146 (z 4.47) |
| **RBC (lead)** | +0.039 (z 0.58, uninformative CI) | **+0.110 (robust z 2.30)** |

Per state (conventional, bw10): CA +0.166 (z 2.97) · TX +0.141 (z 3.32) ·
WI +0.212 (z 3.06) · NC +0.216 (n.s.) · LA −0.276 (z −1.93, parish-fold grain;
pooled τ excl. LA +0.162). Three states, three thresholds, one answer.

## F2 · The design validates
Balance 0/7 at ±5 (|t| max 1.36). McCrary θ=+0.244 (z 4.55, h5) — TX-driven
(TX +0.206 z 2.71; all other states ≈0), the endogenous-proposal-timing
signature, itself H1a evidence. Donut-RD stable/larger: +0.186 to +0.199
(z 3.7–5.3). Event-study pre-years n.s.; GFD pre-period placebo n.s.
Full battery (clustered SEs z≥3.47, Lee bounds [+0.138,+0.163], RI p<0.0002,
IK reconciliation): POLISH_RESULTS.md + P1_RESULTS.md.

## F3 · The intensive margin is large — and replicates off-EMMA
ln(1+EMMA new-money par p.c.) +0.918 (z 2.99); **EMMA-independent** GFD/IUF
+0.827 (z 3.27); RBC-stable (+0.937 / +0.878, robust z 2.09 / 2.35); pre-period
placebo n.s. Survey replication defeats the disclosure-survivorship critique.
(FFC/NG split 53.4%-reported → exploratory.)

## F4 · It is mostly a timing effect — now with the wedge quantified (P2)
Event study: τ₀=+0.236 (z 7.83), pre and post ≈0. Cumulative curves
(|margin|≤5): median time to first post-vote issue **0.33y** (passed) vs
**1.15y** (failed) → **median delay ≈0.82y**; the barely-failed side NEVER
reaches the passed side's end-of-year-0 issuance level (0.504) within +6;
never-issued-by-+6: 50.1% vs 40.0% (**+10pp vertical wedge**). Figure:
`fig_cumulative_wedge.svg`.

## F5 · Refusal is a pause, not a stop
Hazard 26.7/22.8/15.8/12.4%; KM 58.2% ≤4y; median return **1.02y**; 61.9% of
returns pass; median amount ratio **1.00**. Fate per 100 barely-refused:
**54.3 converted · 13.3 returned · 14.2 issued anyway · 18.2 extinguished.**

## F6 · Proximity gradient — puzzle adjudicated (P3): re-approved but unissued
Within CA, majority-failures re-submit 42.2% vs 27.4% (schools 51.3 vs 30.8);
no jump at the symbolic 50 (D2b null). The issuance puzzle is NOT 6y truncation:
the deficit **widens** to 8y (−5.3→−6.4pp; schools −6.7→−8.0pp). Mechanism
lead: majority-failures convert by re-vote far more (107 vs 25 passed returns)
but conversions sit unissued — median pass→first-issue **6.21y vs 2.93y**;
voter-mode first issue ≤8y only 5.5% vs 13.5%. Signature: **authorization
re-assembled, drawdown deferred.** (Longer-horizon pass pending.)

## F7 · Substitution toward the council channel
Council share τ=−0.064 (z −2.03, bw10); modest, direction as predicted; read
jointly with the transition matrix (council-mode first issuance ~8% both sides —
a floor, not the treatment margin; voter-mode +11.7pp at the cutoff).

## F8 · The project itself: continuation and recomposition (B5, bridge-audited)
Ballot purpose ↔ OS use functions (deterministic bridge; blind-audit precision
**80.0%**, recall 88.9%, agreement 85.0% — cite with precision attached):
- **Project continuation ≤6y:** 44.7% barely-passed vs 33.4% barely-failed
  (RD +0.072, z 2.09) — a third of barely-refused projects get financed anyway;
  timing 0.32y vs **1.67y**: the project survives, delayed.
- **Bundle recomposition on re-submission:** 78.2% of original purpose
  categories kept; 22% of the return is new — same purposes, same ask
  (amount ratio 1.00): recomposition is the exception.

## D4/H2 · The chargeability fork, D5/H3 · who it binds for (unchanged)
Fork (RBC: schools +0.123 z 2.30 hold; general-purpose null; utilities +0.500
z 1.90, n small). Freeholder headline: homeownership ≥median +0.182 (z 3.47) vs
+0.056; ownership-not-income; partisanship null at two grains; on-cycle
+0.252 vs +0.099. **D6 (new, descriptive, CA-only):** blocked majorities sit
between sub-50 and cleared places on renter share/diversity/Gini, and blocked
school places are POORER than cleared ones (−$3.8k, SE 1.5k) — the
supermajority bar's demographic incidence.

## R1 · The reform record (appendix, secondary_unverified)
Threshold-lowering attempts since 1990 concentrate in SCHOOLS (CA Prop 170/26/39;
WA 2023–25 bills; ID ~11 attempts) — the no-exit sector; the one non-school
attempt (CA Prop 5, 2024, housing/infra) failed. Prop 39 = the W1 wedge's rule;
TX HB 3 (2019) = the unbundling event. `R1_APPENDIX.md`.

## Reading (one paragraph)
The coalition requirement operates exactly as "Who Must Agree" frames it — and
round 2 shows the stage on which it operates. Entity types hold radically
different exit menus (M1); what reaches a ballot is the non-chargeable civic
core while the chargeable perimeter is financed with no electoral moment (M2);
and the deciding coalition ranges from half a million voters to two (M3). At
the agenda margin, governments time and shape proposals (E-suite). At the
authorization margin, a narrow yes raises six-year issuance ~11–15pp (RBC-robust)
and roughly doubles per-capita borrowing in disclosure AND survey data. At the
response margin, refusal buys delay (0.8–1.7 years at the project grain), not
death: 58% return within 4y, the same project gets financed anyway a third of
the time, and only 18 in 100 marginal refusals extinguish — though near-miss
supermajority failures show a distinct fate: re-approved but unissued. The
requirement binds hardest where exits are absent (schools), for stable
propertied electorates, and that is exactly where the polity fights over the
threshold itself (R1).

## Caveats & pending
- Rules panel PRELIMINARY (pass-1, 78% ICR) — C2/H2 finals HELD for human
  pass-2 (worklist with owner). M1 regime labels are descriptive only.
- RBC at ±5 and IK-bandwidth rows are uninformative-not-contradictory
  (reconciled in P1/POLISH); lead convention = RBC at ±10.
- B5 numbers carry the 80% bridge precision; disagreement-review is the upgrade.
- IL/IN margins absent (harvest paused); MN school classification gap; LA
  fold-grain; TX BRB placeholder rows excluded (M3, flagged).
- D6/D5 moderators are within-matched ACS/SAIPE; specials still county-proxy.
- R1 rows secondary_unverified (owner verification before citation).
