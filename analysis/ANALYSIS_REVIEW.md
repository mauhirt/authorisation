# Analysis review — "Who Must Agree" empirical record

**Date:** 2026-08-24 · **Repo:** `mauhirt/authorisation` @ `7608697` · Every number
below is copied from a committed RESULTS file; the script→results map is at the end.
Purpose: an adversarial review copy — each result carries a verdict, its threats,
and what a referee will ask.

**Verdict legend:** SOLID (survives the battery) · SUPPORTED/CAVEAT (real, with a
stated limitation) · UNDERPOWERED (direction only) · DESCRIPTIVE (no causal claim)
· PRELIMINARY (blocked on a data pass).

---

## 1 · Data & frame

47,235 local referenda (9 states) → 40,924 crosswalked to a Census government
(86.6%; exact tiers ~100%, fuzzy tier 95.1% RA-verified) → 23,577 at a genuine
mandatory-ballot cutoff (`rd_sample`) → **11,889 GO-bond measures**
(TX 8,062 · CA 2,189 · WI 999 · LA 361 · NC 278) at three thresholds
(50; CA 55 schools / 66.7 others, per-measure from CDIAC).

Outcomes: EMMA OS corpus (258,762 docs) + Census GFD surveys + IUF FY2023/24
extension, joined on the shared 9-char Census GID.

Measurement licences (each verified, each cited where used):
- Crosswalk fuzzy tier RA-measured at 95.1%; selection bounded by Lee bounds (below).
- OS `election_date` matches an independently observed referendum 67.9% pooled
  (95.4% in WI, the most complete registry); matched docs point to a *passed*
  measure 91.3% (VALIDATION_RESULTS.md).
- IUF item codes validated against GFD-2022: 29U and 49U within 0.5% for **99.9%**
  of matched units (IUF_RESULTS.md).
- B3 chargeable map: all 118 labels explicitly mapped, zero unmapped, ambiguous
  never guessed (B3_RESULTS.md).
- Rules panel: AI pass-1, cross-validated 78% (29/37) against an independent
  coding — **PRELIMINARY**, human pass-2 worklist = 8 disagreements + 13
  not-codable cells (RULES_CROSSVAL_RESULTS.md).

## 2 · Identification & estimator

Sharp RD in the threshold-centered vote margin at statutory authorization cutoffs.
Local-linear, triangular kernel, HC0 (baseline) in `rdlib.py`; frame
`rd_sample ∩ bond_go`. Supporting designs: DiD at fixed support (W1), discrete-time
hazard (D3), state×entity×year FE panel (C2).

## 3 · Findings under review

### F1 · Authorization binds — VERDICT: SOLID
GO issuance ≤6y τ = **+0.146 (z 4.47)** bw ±10; +0.114 (z 2.48) bw ±5; any-issuance
+0.144 (z 4.45). Naive passed-vs-failed gap is +21.0pp — most of it selection, which
the RD removes. Per state (bw10): CA +0.166 (z 2.97) · TX +0.141 (z 3.32) ·
WI +0.212 (z 3.06) · NC +0.216 (n.s., n=69) · LA −0.276 (z −1.93; see threat #4).
Three states, three thresholds, one answer.

### F2 · Validity battery — VERDICT: SOLID (McCrary openly reported)
Balance 0/7 covariates at ±5 (|t| max 1.36). McCrary θ = +0.244 (z 4.55, h5) —
excess mass above the cutoff, TX-driven (per-state: TX +0.206 z 2.71; CA +0.101
n.s.; WI/LA/NC ≈ 0); treated as endogenous proposal timing (Cellini–Ferreira–
Rothstein precedent), itself H1a evidence. Donut-RD is the answer to density
concerns: τ = +0.195/+0.186/+0.199 (z 5.33/4.52/3.65) at δ = 0.5/1/2pp — stable
or larger. Event-study pre-years n.s. (τ₋₂ +0.007, τ₋₁ +0.022); GFD pre-period
placebo n.s. (+0.412, z 1.51).

### F3 · Intensive margin, replicated off-EMMA — VERDICT: SOLID
ln(1+EMMA new-money par p.c.) τ = **+0.918 (z 2.99)** bw10. EMMA-independent
GFD outcome (includes bank loans / private placements that never post an OS):
**+0.827 (z 3.27)** with IUF-extended windows (+1.036 before extension — stable).
Survivorship critique of the disclosure corpus cannot explain a survey-data
replication. FFC/NG split only 53.4%-reported → exploratory only.

### F4 · A timing effect — VERDICT: SOLID
Event study: τ₀ = **+0.236 (z 7.83)**; all pre and post years ≈ 0 (max |z| 1.4).
Authorization accelerates; refusal delays; the 6y cumulative wedge is what
remains after catch-up.

### F5 · Refusal is a pause, not a stop — VERDICT: SOLID
n=2,680 failures. Hazard front-loaded: 26.7% → 22.8% → 15.8% → 12.4%;
KM 58.2% return within 4y; median time-to-return **1.02y** (the next election).
61.9% of returns pass. Median amount ratio return/original **1.00** (n=1,354) —
districts re-ask, they don't concede.

### F6 · Proximity gradient — VERDICT: SUPPORTED/CAVEAT
Within CA (composition-clean): majority-failures re-submit 42.2% vs 27.4%;
regime×purpose: CA schools 51.3% vs 30.8%. Signal test (D2b) at the 50 line among
CA school failures: null (τ −0.14, z −1.0, n=326; low power). OPEN PUZZLE:
majority-failures show *lower* 6y issuance (23.5% vs 34.6%) despite re-submitting
more — flagged, unexplained.

### F7 · Council-channel substitution — VERDICT: SUPPORTED/CAVEAT
Council share of window docs τ = −0.064 (z −2.03, bw10). Modest, in the theory's
direction; bw5 n.s. (−0.030, z −0.68).

### Transition matrix & fate of refusal — VERDICT: SOLID (descriptive frame, causal margin)
First post-vote issue (|margin|≤5): voter-mode 48.4% vs 36.7%; council ~8% BOTH
sides (a floor, not the treatment margin); no-issue 43.1% vs 54.2%. Fate per 100
barely-refused (2005–19 cohort, n=422): **54.3 converted by re-vote · 13.3
returned/unconverted · 14.2 issued anyway (5.2 council/statutory + 9.0 old voter
authority) · 18.2 extinguished**. Refusal permanently stops <1 in 5 marginal
proposals.

### D4 · Chargeability fork — VERDICT: SUPPORTED/CAVEAT (utilities cell small)
Schools (menu 0.4% chargeable): τ +0.147 (z 4.03), re-submit 59.2%. Utilities
(menu 70.0%): τ GO +0.463 (z 2.81) vs ANY +0.362 — ~a fifth rerouted to non-GO;
n=1,576, treat magnitude with care. General-purpose (menu 57.6%): τ +0.073
(z 0.90, n.s.), re-submit 25.3%. The fork orders exactly as H2 predicts.

### B3/C2 · National sorting & H2 — VERDICT: B3 DESCRIPTIVE · C2 PRELIMINARY
B3: voted channel carries **11.1%** chargeable dollars vs council 60.5% /
statutory 72.5% — the sorting the theory predicts, descriptive. C2 (rules on the
RHS): pooled null; general-purpose β = −0.162 (t −1.83, 45 states) — right sign,
marginal, and BLOCKED on the rules pass-2 before it can be cited as a finding.
Descriptive anchor: muni nc-share 29.3% (strict) vs 59.2% (lax).

### W1 · Institutional wedge — VERDICT: SUPPORTED/CAVEAT
DiD at fixed support (CA 55 vs TX/WI 50, schools): the rule itself moves 6y
issuance **+0.115 (SE 0.048)** — within sampling error of the RD (+0.146) from an
entirely different identification. W2 (within-CA) underpowered (n=13/88 cells);
note, don't cite. Midwifery (new issuers in county): honest null (τ −0.026, z −0.79).

### Agenda suite — VERDICT: SUPPORTED/CAVEAT (TX bunching confounded by discreteness)
E4: CA schools propose 8.8/100 districts/yr vs TX 20.1, at 2.6× median size
($39M vs $15M), 4.4× more on-cycle (62.7% vs 14.1%) — fewer, larger, better-timed.
E3: pass rates near-invariant at moderate bars (CA-55 77.6% ≈ TX-50 79.2%), break
at 66.7 (47.6%). E2 bunching concentrated in TX (ratio 1.55, z 3.42) where
tiny-electorate discreteness confounds. TX-2019 unbundling: props/election
1.5–1.7 → 2.0–2.4, multi-prop share ≈25% → 49–60% at the mandate.
(MN E4 cell = classification gap, not evidence.)

### D5/H3 · Who the requirement binds for — VERDICT: SUPPORTED/CAVEAT
Freeholder headline (proper grain): homeownership ≥median τ = **+0.182 (z 3.47)**
vs +0.056 (n.s.). Ownership, not income: income split flat (+0.129 vs +0.122);
SAIPE district child poverty repeats the gradient (+0.184 vs +0.099). Stability
profile: 65+ +0.194 vs +0.036; homogeneity +0.232 vs −0.018 — the
fractionalization sign runs AGAINST naive assembly-cost H3; theory session must
adjudicate. On-cycle +0.252 vs off-cycle +0.099. Partisanship: informative null
at county grain (+0.121 vs +0.111; terciles non-monotone) AND at large-city grain
(precinct Dem share, mayor party — all n.s.). Moderator profile is institutional/
proprietary, not ideological.

## 4 · Robustness battery (estimation polish)

| check | result | reading |
|---|---|---|
| Cluster by unit (2,480) | z = 4.11 | robust |
| Cluster by county (650) | z = 3.47 | robust |
| Lee bounds (trim 2.52%) | [+0.138, +0.163] | crosswalk selection cannot move it |
| Randomization inference, \|m\|≤2 | +0.142, p < 0.0002 | design-based, near-cutoff |
| Donut δ=0.5/1/2 | +0.186 to +0.199 | stable/larger |
| IK MSE-optimal bw | h=1.81pp; τ = −0.001 (SE 0.075) | noise-dominated at tiny bw — see threat #3 |
| Excl. LA | +0.162 (z 4.87) | LA not driving |
| McCrary by state | TX +0.206 (z 2.71); others ≈0 | TX discreteness story |

## 5 · Threats, ranked

1. **Rules panel is PRELIMINARY** (pass-1, 78% ICR). Blocks C2/H2 national
   claims. FIX: human pass-2 on the 21-cell worklist. Does NOT touch the RD track.
2. **McCrary excess mass** (θ +0.244 pooled). The referee's first question.
   Defense in place: TX-concentrated; CFR precedent; donut-RD stable/larger;
   0/7 balance. Framed as H1a evidence, reported openly.
3. **IK bandwidth tension.** τ(h_IK=1.81pp) ≈ 0 while RI at the SAME window gives
   +0.142 (p<0.0002) and donuts are larger: local-linear slopes eat the signal on
   1.8pp of support. Must be reported in the robustness table with this
   reconciliation, never hidden.
4. **LA cell is negative** (−0.276, z −1.93) at parish-fold grain (outcome mixes
   many measures). Treated as grain artifact; headline shown with and without LA.
5. **Crosswalk selection** — bounded: Lee [+0.138, +0.163]; MA/NC zero-selection
   benchmarks.
6. **EMMA survivorship** — answered: GFD/IUF replication (+0.827, z 3.27).
7. **Purpose classification gaps** — MN school bonds unclassified (E4 cell empty);
   IL/IN lack margins entirely (harvest paused). Frame-honesty issue, not bias.
8. **SAIPE/ACS match selectivity** — matched subsets not representative
   (CA 44%, IL 21%); splits are within-matched and internally valid; labeled.
9. **GFD FFC/NG half-reported** (53.4%) — exploratory only, labeled.
10. **F6 open puzzle** — majority-failures re-submit more but issue less (≤6y);
    unexplained; flagged in FINDINGS.md.

## 6 · Open before submission

- Rules human pass-2 (21 cells) → then C2/H2 final estimates.
- B5 purpose matching (project continuation, bundle recomposition — map rows 3/10).
- Cumulative-wedge figure (delay N years / extinguish 18.2%).
- Specials demographics: TWDB/shapefile interpolation (only class on county proxy).
- IL margin harvest (paused; plan committed upstream).
- Upstream auth tier-2 corpus refresh → one-command link rerun.

## 7 · Reviewer decision points

1. Present IK-bandwidth row with reconciliation note, or lead with CCT-style
   robust CI once implemented? (Current: report + note.)
2. Headline with or without LA? (Current: with, + exclusion shown.)
3. Fractionalization sign vs H3 — reframe H3 as "stable propertied public"?
4. Utilities τ +0.463 — cite magnitude or direction only (n=1,576)?
5. C2 general-purpose t=−1.83 — hold entirely until pass-2, or show as suggestive?

## 8 · Script → results map

| script | results | finding |
|---|---|---|
| `rd_analysis.py` | RD_RESULTS.md | F1, balance, density bins |
| `mccrary_donut.py` | MCCRARY_DONUT_RESULTS.md | F2 |
| `rd_outcomes.py` | OUTCOMES_RESULTS.md | F3, F4, F7 |
| `failure_paths.py` | FAILURE_PATHS_RESULTS.md | F5, F6 |
| `transition_fate.py` | TRANSITION_FATE_RESULTS.md | matrix, fate |
| `d4_fork.py` | D4_RESULTS.md | D4 |
| `b3_chargeable.py` / `c2_national.py` | B3/C2_RESULTS.md | B3, C2 |
| `midwifery_wedge.py` | MIDWIFERY_WEDGE_RESULTS.md | W1/W2, midwifery |
| `agenda_suite.py` | AGENDA_RESULTS.md | E2–E4, TX-2019 |
| `d5_heterogeneity.py` / `attach_acs.py` / `attach_saipe_sd.py` | D5/ACS/SAIPE_SD_RESULTS.md | D5, H3 |
| `d5_external.py` / `d5_largecity.py` | D5_EXTERNAL / D5_LARGECITY | partisanship nulls |
| `validation_join.py` | VALIDATION_RESULTS.md | row-18 licence |
| `iuf_extension.py` | IUF_RESULTS.md | FY23/24 extension |
| `rules_crossval.py` | RULES_CROSSVAL_RESULTS.md | pass-2 worklist |
| `estimation_polish.py` | POLISH_RESULTS.md | robustness battery |
