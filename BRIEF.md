# BRIEF — single source of truth (24 Aug 2026). Ignore all prior project descriptions.

**Paper:** "Who Must Agree." Bond authorisation rules are coalition requirements operating at two margins: agenda (what is proposed, which channel, bundling, timing) and response (after refusal: substitute, re-submit, abandon). H1a agenda; H1b response; H2 composition tilts toward chargeable purposes under stricter rules; H3 effects scale with coalition-assembly cost. Causal design: narrowly passed vs narrowly failed local bond referenda, CA/WI/TX, outcomes from the OS corpus. Everything else (gates, covenants beyond one appendix table, cap exemptions, six papers) is out of scope.

**Conventions (all tasks):** immutable /raw; provenance (source, url, date) for every external file; every stage ends with RESULTS.md containing raw numbers, row counts, warnings, dropped-row counts; no number outside script output; no statute summarising; anomalies flagged, never silently fixed.

## Step 0 — Reconcile (first RESULTS.md)
Report repo state against this brief: which of B1–B4 below are already partly done here (crosswalk verification and referendum-rules work may exist); answer K-checks: K1 covenant-field missingness corpus-wide; K2 par_amount coverage; K3 KY determined-n; K4 BRB coverage pre/post-2019; K5 pre-2005 share.

## Builds
**B1. Election data.** Download + archive: CDIAC local bond elections (CA), WI DPI referenda, TX BRB bond elections, 2005–present. Keep: jurisdiction name, entity type, election date, purpose text, amount, yes-share, threshold, passed. Derive: re-submission (later measure, same jurisdiction + purpose, ≤4y).
**B2. Crosswalk.** Election jurisdiction → corpus issuer id → county FIPS. Report match rates by entity type + 20 random pairs per class for eyeball check.
**B3. Functions.** Use-level functional reclassification corpus-wide, excluding refunding uses; add chargeable flag (chargeable: water/sewer/utility/power/parking/ports/airports; non-chargeable: schools/parks/safety/roads/general govt; ambiguous → flag, don't guess).
**B4. Referendum-rules table.** Fields: ref_required {none/petition/mandatory}, threshold, by state × entity type × purpose. First check the archived ACIR A-10 (1961) and SFFF Table 48 (1986) scans for voter-approval columns and transcribe if present; then HMS appendix for modern; CA/WI/TX cells to full precision from state sources. Provenance = secondary until verified.

## Analyses (run as inputs allow; each = script + CSV + markdown table + RESULTS entry)
**Now (corpus only):**
- C1: voter-approved share by security_type_normalized (order: utility_revenue, lease_appropriation, limited_special_obligation, revenue_other, sales_tax, go_limited_property_tax, go_unspecified, go_unlimited_property_tax); by issuer class (classify legal_issuer, test in order: school/isd → school district; county; city of/town of/village of/borough → municipality; authority; district → special district; else other); by state (floor n≥50; always show KY flagged). Universe: auth_determined_final==True. Count + par-weighted panels; TX-excluded variants; report undetermined rate by type/state.
- C3: bundling/term by auth_mode_final ∈ {voter, council_or_board}: n, mean/median n_classified_uses, mean n_projects, median term (year(maturity_last)−year(dated_date); drop <0 or >50, count drops). Panels: all; new-money only (has_new_money & !has_refunding).
- A0: corpus issue counts by state-year vs Census/Willamette long-term debt issued.
- T2x (appendix, if K1 passes): rate covenant / additional bonds test incidence by security type; 2×2 voted × covenanted within type; share unvoted & covenant-free overall.

**On B1:**
- E1 (report before proceeding): counts by state × entity × threshold × margin bands (±2/±5/±10pp), passed/failed; decides event study vs matched DiD.
- E2: vote-share density around each threshold (bunching above cutoff).
- E3: passage rates by threshold regime.
- E4: proposals per capita, mean amount, purposes, on/off-cycle by regime (ACS population).

**On B1+B2 (the core):**
- D1: event study (−2y..+5y), narrow-margin passed vs failed: total new-money par p.c.; unvoted tax-backed share; district/authority share of the PLACE's issuance (aggregate all issuers in the county/place). Estimator per E1; matched DiD fallback: match on entity type, purpose, amount decile, state, year.
- D2: split failures into majority-failures (50<yes<threshold) vs minority-failures (<50); compare re-submission and substitution paths.
- D3: re-submission hazard; returning measures' amount/bundling/timing vs original.
- D5: D1 effects × ACS homeownership, 65+ share, fractionalisation; × on/off-cycle.

**On B1+B2+B3:**
- D4: D1 split by ballot purpose: utility vs school measures (reroute vs re-submit/abandon).
- C2: non-chargeable share of place-level new-money vs ref_required/threshold (B4), national panel, state and entity-type FE.

**Order:** 0 → B1 → E1 (stop, report) → B2 ∥ B4 ∥ B3 → C1/C3/A0/E2–E4 → D1–D3, D5 → D4, C2 → T2x/conditionals.
