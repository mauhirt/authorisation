# Analysis review — "Who Must Agree" empirical record (round 2)

**Date:** 2026-08-24 · **Repo:** `mauhirt/authorisation` (round-2 head) · Every
number is copied from a committed RESULTS file; the script→results map is at the
end. Purpose: an adversarial review copy — each result carries a verdict, its
threats, and what a referee will ask. Round 2 added: M1–M3 legibility exhibits,
D6, CCT-RBC lead inference (P1), the cumulative-wedge figure (P2), the F6
truncation adjudication (P3), B5 purpose matching with a blind audit, and the
R1 reform appendix.

**Verdict legend:** SOLID (survives the battery) · SUPPORTED/CAVEAT (real, with a
stated limitation) · UNDERPOWERED (direction only) · DESCRIPTIVE (no causal claim)
· PRELIMINARY (blocked on a data pass).

---

## 0 · Instruction-conflict log (round 2, flagged not silently fixed)
1. **M3 "CDIAC yes"** — wrong: CDIAC carries % Yes/% No only, no counts; CA is
   excluded from count panels. (LA turns out to carry true turnout denominators.)
2. **M1 "authority" entity type** — not a `pol_accountable_type` class;
   proxied via issuer `jurisdiction_class` ∈ {housing, health_hospital,
   utility_district} as a memo row.
3. **D6 scope** — blocked majorities exist only under supermajority rules:
   CA-only among margin states.
4. **M2 "B1 ballot purposes"** — no formal B1 taxonomy exists in the repo; the
   committed keyword normalization stands in, labeled.
5. **D6 Gini** — not in the ACS cache; new B19083 pull (CA, 2010+2019, all
   grains) added as `cache/acs_gini_ca.csv`.
6. **Data flag caught en route:** TX BRB rows with votesfor+votesagainst=1
   (3,188 rows) are a counts-unknown placeholder convention — excluded in M3;
   no RD estimate affected (those rows sit at margin ≈ +50).

## 1 · Data & measurement licences

47,235 referenda → 40,924 crosswalked (86.6%) → 23,577 `rd_sample` → **11,889
GO-bond measures** (TX 8,062 · CA 2,189 · WI 999 · LA 361 · NC 278); thresholds
50 / 55 / 66.7. Outcomes: EMMA (258,762 docs) + GFD + IUF FY23/24.

| layer | verification | status |
|---|---|---|
| Referendum→unit crosswalk | exact ~100%; fuzzy 95.1% RA-verified; Lee-bounded | SOLID |
| OS authorization fields | date match 67.9% pooled / 95.4% WI; matched→passed 91.3% | SOLID |
| IUF FY23/24 extension | 29U/49U = GFD within 0.5% for 99.9% of matched units | SOLID |
| B3 chargeable map | 118 labels explicitly mapped, zero unmapped | DESCRIPTIVE |
| **B5 purpose bridge (new)** | blind 60-pair audit: precision 80.0%, recall 88.9%, agreement 85.0% | SUPPORTED/CAVEAT |
| Vote counts (M3, new) | TX/WI/LA/NC/MN/MA carry counts; CA % only; TX placeholder rows excluded | SOLID (coverage stated) |
| State debt-rules panel | AI pass-1; 78% ICR vs independent coding; 21-cell worklist | **PRELIMINARY — C2/H2 finals HELD** |
| R1 reform appendix (new) | web-compiled, per-row sources | secondary_unverified |

## 2 · Identification & estimators
Sharp RD in threshold-centered margin. **Lead inference: CCT robust
bias-corrected (local-quadratic at h, HC0 robust variance; `rd_rbc`)**;
conventional local-linear alongside; supporting designs: W1 DiD at fixed
support, D3 hazard, C2 FE panel (held), B5 continuation RD.

## 3 · Findings under review

### F1 · Authorization binds — VERDICT: SOLID (RBC-attenuated)
Conventional +0.146 (z 4.47, bw10); **RBC lead +0.110 (robust z 2.30)**; ANY
+0.144 / RBC +0.116 (z 2.45). Per state CA +0.166 / TX +0.141 / WI +0.212;
LA −0.276 fold-grain (excl. → +0.162). RBC at ±5 uninformative
(CI [−0.09,+0.17]) — reconciled with RI/donut, threat #3.

### F2 · Validity battery — VERDICT: SOLID
0/7 balance; McCrary +0.244 TX-driven (TX +0.206 z 2.71, others ≈0); donuts
+0.186–0.199; placebos n.s.; clusters z≥3.47; Lee [+0.138,+0.163]; RI p<0.0002.

### F3 · Intensive margin, off-EMMA replication — VERDICT: SOLID
EMMA +0.918 (z 2.99) / RBC +0.937 (2.09); GFD +0.827 (z 3.27) / RBC +0.878
(2.35); placebo n.s. FFC/NG exploratory (53.4% reported).

### F4 + P2 · Timing effect, wedge quantified — VERDICT: SOLID
τ₀=+0.236 (z 7.83), pre/post ≈0. Wedge (|m|≤5): median delay **0.82y**
(0.33 vs 1.15 among ≤6y issuers); failed side never reaches passed year-0 level
(0.504) within +6; never-issued +10.0pp (50.1 vs 40.0). `fig_cumulative_wedge.svg`.

### F5 · Pause, not stop — VERDICT: SOLID
Hazard 26.7→12.4%; KM 58.2%; median return 1.02y; 61.9% of returns pass; amount
ratio 1.00. Fate per 100 barely-refused: 54.3 / 13.3 / 14.2 / 18.2.

### F6 + P3 · Proximity gradient; puzzle adjudicated — VERDICT: SUPPORTED/CAVEAT
Re-submission gradient real (42.2 vs 27.4; schools 51.3 vs 30.8; D2b null at 50).
P3: truncation REFUTED — deficit widens to 8y (−6.4pp; schools −8.0pp).
Reframed: majority-failures convert more (107 vs 25) but sit unissued
(pass→issue 6.21y vs 2.93y; voter-mode first issue 5.5% vs 13.5% ≤8y).
Caveat: chain medians ride small n; 10y+ pass pending.

### F7 · Council-channel substitution — VERDICT: SUPPORTED/CAVEAT
τ −0.064 (z −2.03, bw10; bw5 n.s.); transition matrix: council ~8% both sides,
voter-mode +11.7pp — the treatment margin is voter-authorized borrowing vs none.

### F8 · B5 continuation & recomposition — VERDICT: SUPPORTED/CAVEAT (80% bridge)
Continuation ≤6y 44.7% vs 33.4% (RD +0.072, z 2.09); timing 0.32 vs 1.67y;
recomposition rare (78.2% categories kept). Cite only with precision attached;
disagreement-review is the upgrade path.

### M1–M3 · The stage — VERDICT: DESCRIPTIVE (by design)
M1 menu: schools 29.8% non-voted $ vs general-purpose 80.4/82.7% — fork ordering
against an independent menu measure. M2: balloted core (K-12 38.2%) vs submerged
perimeter (hospitals $197.5B, housing, electric, airports — voted <2%).
M3: deciding coalitions 768 (school) / 1,179 (off-cycle city) / 34 (special
district); Harris County 511,375 vs MUD 2 under one rule.

### D4 fork · D5/H3 moderators · W1 wedge — unchanged verdicts
D4 SUPPORTED/CAVEAT (RBC: schools +0.123 z 2.30; general null; utilities +0.500
z 1.90 n=156). D5/H3 SUPPORTED/CAVEAT (freeholder +0.182 z 3.47 vs +0.056;
income flat; partisanship null ×2 grains; frac sign against naive H3 —
adjudication open). W1 +0.115 (SE 0.048) ≈ RD. Midwifery null. Agenda suite
SUPPORTED/CAVEAT (TX bunching = discreteness confound).

### D6 · Blocked majorities — VERDICT: DESCRIPTIVE (CA-only)
Blocked places sit between sub-50 and cleared on renter/diversity/Gini; blocked
school places poorer than cleared (−$3.8k, SE 1.5k). Within-matched caveat.

### B3/C2 · National H2 — VERDICT: B3 DESCRIPTIVE · C2 PRELIMINARY (HELD)
Voted channel 11.1% chargeable $ vs council 60.5 / statutory 72.5. C2
general-purpose β −0.162 (t −1.83) held until rules pass-2 lands.

### P5 · Pay-go bound — VERDICT: SUPPORTED/CAVEAT (deliberately subordinated)
Schools outlay RD differenced +0.377 (z 2.9; RBC +0.464, z 2.4); offset ratio
0.92; general-purpose null; specials thin. Enters as ONE validity-battery row
plus two sentences beside continuation, per the outcome-architecture rule (OS
corpus = outcome of record). Caveats: construction-year spreading; positive
pre-period RD owned via the differenced spec; FY2023 truncation; total outlay
only. Consent map (F6.1) built: OK 80% / TX 67% … NY/PA/KY ≈ 0; 10
no-coverage states flagged as extraction gaps.

### P4 · Rate-cap mechanism — VERDICT: NOT CONFIRMED (underpowered)
118 capped vs 14 uncapped conversions; uncapped cell too thin and
directionally opposite (9.74y vs 4.93y). The banked-authorisation fact stands
unexplained; upgrade: county AV rolls, CDIAC sold-vs-authorised.

### N1–N5 · National panel regressions — VERDICT: FIRST-STAGE (rules PRELIMINARY)
90,604-unit entity panel + 19,539-city view. First stage: schools +0.778
(t 7.0), specials +0.199, munis +0.171; counties n.s.; township reversal =
proxy-rule artifact (pass-2 item). Substitution at unit grain: general-purpose
GO −0.345 (t −5.1), nc −0.171 (t −3.3). Extensive margin n.s. TEL×rule n.s.
(570 cities, power-limited by design). strict×county-Dem −0.75 (t −2.2,
descriptive). MISSING per block (in N_RESULTS.md): rules pass-2; township rule
column; rule time-variation; state-level TEL panel; specials revenue-size
proxy; SD-grain national moderators; GFD no-report→0 assumption.

### N6 · Reform events — VERDICT: NOT YET CONFIRMING (upgrade path named)
Prop 39 state-mean designs: schools DiD +0.451 (permutation p 0.15) with a
visible pre-trend; sector-DDD ≈ 0. FFC composition margin DEGENERATE in GFD
(school FFC ≡ 1.000 by classification — a data finding). Required upgrades:
district-level TWFE with enrollment weights + Conley–Taber CIs; OPSC
state-matching-fund controls; CDIAC issuance database for the COP→GO
composition. Measure 56 = crisis-confounded sketch. Treatment here is the
event, not the coded panel — pass-2 does not gate this design.

### R1 · Reform appendix — VERDICT: secondary_unverified
Threshold-lowering attempts concentrate in schools (CA 170/26/39, WA, ID×11);
the non-school attempt (CA Prop 5 2024) failed; OR tightened then loosened;
TX HB 3 2019 = ballot-structure regulation. Owner verification before citation.

## 4 · Robustness battery (headline: GO issuance ≤6y)

| check | result | reading |
|---|---|---|
| **RBC (lead), bw10** | +0.110, robust z 2.30 | survives bias correction, attenuated ~25% |
| RBC bw5 | +0.039, CI [−0.09,+0.17] | uninformative, not contradictory |
| Cluster unit / county | z 4.11 / 3.47 | robust |
| Lee bounds (trim 2.52%) | [+0.138, +0.163] | selection bounded |
| RI |m|≤2 (5000 perms) | +0.142, p<0.0002 | design-based |
| Donut δ=0.5/1/2 | +0.186…+0.199 | stable/larger |
| IK h=1.81 | τ≈0 (SE 0.075) | slope-dominated; see reconciliation |
| Excl. LA | +0.162 (z 4.87) | LA not driving |
| McCrary by state | TX +0.206; others ≈0 | discreteness story |

## 5 · Threats, ranked
1. **Rules panel pass-1** — blocks C2/H2 finals; worklist with owner; RD track
   untouched; M1 regime labels descriptive.
2. **McCrary excess mass** — TX-concentrated; CFR precedent; donuts larger;
   0/7 balance; framed as H1a evidence.
3. **Small-bandwidth flexibility tension** (IK ≈0; RBC±5 uninformative) —
   resolved by convention: RBC-at-±10 lead + RI/donut at the narrow window;
   reported, never hidden.
4. **RBC attenuation** — headline is ~25% smaller under the lead convention
   (+0.110 vs +0.146); the paper must quote the RBC number first.
5. **LA fold grain** — negative cell; headline shown with and without.
6. **Crosswalk selection** — Lee-bounded tight; MA/NC zero-selection benchmarks.
7. **EMMA survivorship** — answered by GFD/IUF replication.
8. **B5 bridge error** (80% precision) — continuation numbers carry it
   explicitly; disagreement review pending.
9. **Classification gaps** — MN schools (E4 empty cell), IL/IN no margins,
   TX placeholder rows (excluded, flagged).
10. **Moderator match selectivity** — within-matched validity only (D5, D6).
11. **F6 residual** — deficit real at 8y; banked-authorization fate beyond 8y
    unknown (10y+ pass pending).
12. **R1 is secondary_unverified** — appendix only until owner verification.

## 5b · Newly diagnosed (round 3): the finance-flag coverage gap
Extraction wave `w2_3_v3.2` left `has_new_money` blank for a subset of states
(NY, PA, IN, CO, WA, AL, GA, AZ, TN, VA, SC, NC among them) — their documents
exist in the corpus (NY 25,974; PA 10,240; IN 7,780 …) but never enter
new-money outcomes. Consequences now flagged at each use: consent map gated at
≥50 flagged docs per state (34 states qualify; NY/PA no longer shown as false
0%); N-suite corpus outcomes ride the flag-covered states (cluster counts
reflect it); NC (an RD state) has near-empty corpus new-money outcomes — its
RD cell is small and n.s. either way, and GFD outcomes carry it. KY's ≈0%
voted share is REAL (3,245 flagged docs). FIX: the pending auth tier-2 corpus
refresh — this diagnosis is its symptom list.

## 6 · Open before submission
- Rules human pass-2 (21 cells) → C2/H2 + N1–N5 causal upgrades. (With owner.)
- Township rule column in pass-2 (town-meeting states break the muni proxy).
- Prop 39 district-level TWFE + OPSC matching-fund controls; CDIAC issuance
  pull for the COP→GO composition event study.
- State-level TEL panel (full universe; big-city index has no time variation).
- B5 disagreement-review pass (9 disputed pairs; upgrade precision).
- P3 longer-horizon (10y+) issuance pass on the re-approved-but-unissued cohort.
- Specials demographics: TWDB/shapefile interpolation (last county-proxy class).
- IL margin harvest (paused; plan upstream). Auth tier-2 corpus refresh.
- R1 owner verification against primary legislative records.

## 7 · Reviewer decision points
1. RESOLVED (round 2): lead inference = RBC at ±10; IK + RBC±5 reported with
   reconciliation.
2. Headline number in the abstract: +0.110 (RBC) or +0.146 (conventional)?
   Current: RBC first, conventional beside it.
3. LA in/out of headline (current: in, exclusion shown).
4. H3 reframe to "stable propertied public" given the frac sign (open).
5. Utilities: ordering-only vs magnitude (current: ordering).
6. C2 t=−1.83: hold entirely vs suggestive (current: held, PRELIMINARY).
7. M3's placement: main-text exhibit vs appendix (new).

## 8 · Script → results map
| script | results | finding |
|---|---|---|
| rd_analysis.py | RD_RESULTS.md | F1, balance, density |
| mccrary_donut.py | MCCRARY_DONUT_RESULTS.md | F2 |
| estimation_polish.py | POLISH_RESULTS.md | battery, IK, RI, Lee, clusters |
| cct_rbc.py | P1_RESULTS.md | RBC lead convention |
| rd_outcomes.py | OUTCOMES_RESULTS.md | F3, F4, F7 |
| p2_cumulative_wedge.py | P2_RESULTS.md + fig_cumulative_wedge.svg | wedge |
| failure_paths.py | FAILURE_PATHS_RESULTS.md | F5, F6 |
| p3_f6_truncation.py | P3_RESULTS.md | F6 adjudication |
| transition_fate.py | TRANSITION_FATE_RESULTS.md | matrix, fate |
| d4_fork.py | D4_RESULTS.md | fork |
| m1_menu_matrix.py | M1_RESULTS.md | menu, fork-vs-menu |
| m2_balloted_submerged.py | M2_RESULTS.md | balloted/submerged |
| m3_absolute_coalitions.py | M3_RESULTS.md | coalition sizes |
| d6_blocked_majorities.py (+acs_gini_pull.py) | D6_RESULTS.md | blocked majorities |
| b5_purpose_match.py + b5_audit_score.py | B5_RESULTS.md | continuation, recomposition, audit |
| c2_national.py | B3/C2_RESULTS.md | national sorting, H2 (held) |
| midwifery_wedge.py | MIDWIFERY_WEDGE_RESULTS.md | W1/W2 |
| agenda_suite.py | AGENDA_RESULTS.md | E2–E4, TX-2019 |
| attach_acs.py / attach_saipe_sd.py / d5_*.py | ACS/SAIPE_SD/D5* | D5, H3 |
| validation_join.py | VALIDATION_RESULTS.md | row-18 licence |
| iuf_extension.py | IUF_RESULTS.md | FY23/24 |
| rules_crossval.py | RULES_CROSSVAL_RESULTS.md | pass-2 worklist |
| (compiled) | R1_APPENDIX.md | reform record |
