# EXHIBITS.md — journal exhibit manifest

Regenerate everything with `make exhibits` (repo root). All exhibits build from the
FROZEN corpus package v3 (`inputs/corpus/`, pinned in `README.md`) and the committed
analysis caches; no manual edits to `exhibits/out/`. Each table is emitted as CSV +
`\input`-able .tex; each figure as CSV (plot data) + SVG + PDF. RD rows follow the
rdrobust (Calonico–Cattaneo–Titiunik) convention: RBC coefficient with robust 95% CI
beneath, robust p, conventional estimate, bandwidth h, effective N (L/R). Stars use the
house `\sig{}` macro. `\textbf{Reading.}` paragraphs are wrapped in
`% BEGIN READING … % END READING` comments for stripping at submission.

The two cross-check lists required by the instruction (draft numbers with no exhibit
home; exhibit cells with no draft sentence) are in `exhibits/RESULTS.md`.
Values that changed from the draft under final specifications are in
`exhibits/NUMBERS_DIFF.md`.

## Main text — tables

| Exhibit | Files | Script | Source results file(s) | Draft section citing it |
|---|---|---|---|---|
| T1 Sample and summary statistics | `T1_sample.{csv,tex}` | `build_desc_tables.py` | `analysis/OUTCOMES_RESULTS.md` (cascade), `analysis/NATIONAL_ENTITY_RESULTS.md` (corpus/panel B); computed from `analysis/paper_panel.csv` + v3 `auth_os` | §4 |
| T2 Covariate continuity | `T2_covariate_continuity.{csv,tex}` | `build_rd_tables.py` | `analysis/RD_RESULTS.md`, `analysis/P1_RESULTS.md`; recomputed via `analysis/rdlib.py` | §6 |
| T3 Main results | `T3_main_results.{csv,tex}` | `build_rd_tables.py` | `analysis/RD_RESULTS.md`, `analysis/P1_RESULTS.md`, `analysis/B5_RESULTS.md` (continuation), `analysis/P5_RESULTS.md` (pay-go row), `analysis/IUF_RESULTS.md` (Census survivorship row) | §6 (pay-go row also §7 battery, §8) |
| T4 Fifty-state first stage | `T4_first_stage.{csv,tex}` | `build_desc_tables.py` | `analysis/N_RESULTS.md`, `analysis/NC_COVERAGE_RESULTS.md` (count-based line) | §5 |
| T5 Response margin | `T5_response.{csv,tex}` | `build_desc_tables.py` | `analysis/TRANSITION_FATE_RESULTS.md`, `analysis/FAILURE_PATHS_RESULTS.md` | §7 |
| T6 Where it binds (moderators) | `T6_moderators.{csv,tex}` | `build_rd_tables.py` | `analysis/D5_RESULTS.md` (proper grain, specials excluded per round 4) | §8 |
| T7 Exits: fork against the menu | `T7_fork_menu.{csv,tex}` | `build_rd_tables.py` | `analysis/RD_RESULTS.md` (class RDs), `analysis/M1_RESULTS.md` (menu shares), `analysis/FAILURE_PATHS_RESULTS.md` (re-submission) | §8 |

## Main text — figures

| Exhibit | Files | Script | Source results file(s) | Draft section |
|---|---|---|---|---|
| F1 The RD | `F1_rd.{svg,pdf}` + `F1_rd_bins.csv` | `build_figures.py` | `analysis/RD_RESULTS.md`, `analysis/P1_RESULTS.md` | §6 |
| F2 Event study | `F2_event_study.{svg,pdf,csv}` | `build_figures.py` | `analysis/RD_RESULTS.md` (horizon indicators) | §6 |
| F3 Cumulative wedge | `F3_wedge.{svg,pdf,csv}` | `build_figures.py` | `analysis/MIDWIFERY_WEDGE_RESULTS.md`, `analysis/P2_RESULTS.md` | §6 |
| F4 Consent map | `F4_consent_map.{svg,pdf}` | `build_figures.py` (greyscale recolour of `analysis/fig_consent_map.svg`) | `analysis/F61_MAP_VALUES.md` | §5 |
| F5 Running-variable density | `F5_density.{svg,pdf}` | `build_figures.py` | `analysis/MCCRARY_DONUT_RESULTS.md` | §6 |

## Appendix

| Exhibit | Files | Script | Source results file(s) | Draft section |
|---|---|---|---|---|
| A1 Specification battery | `A1_battery.{csv,tex}`, `A1_horizons.csv`, `A1_bandwidth_curve.csv`, `A1a_horizons.{svg,pdf}`, `A1b_bandwidth.{svg,pdf}` | `build_rd_tables.py` (+`build_figures.py`) | `analysis/P1_RESULTS.md`, `analysis/POLISH_RESULTS.md` (Lee bounds, RI, clustering), `analysis/MCCRARY_DONUT_RESULTS.md` (donuts) | §6, App H |
| A2 Placebo thresholds | `A2_placebo_thresholds.{csv,tex}` | `build_rd_tables.py` | recomputed (see NUMBERS_DIFF note on pseudo-45) | §6 (no sentence yet; see RESULTS.md) |
| A3 State-by-state | `A3_state_by_state.{csv,tex}` | `build_rd_tables.py` | `analysis/RD_RESULTS.md` | §6 |
| A4 Agenda margin | `A4_agenda.{csv,tex}`, `A4b_passrates.csv`, `A4c_tx2019.csv` | `build_desc_tables.py` | `analysis/AGENDA_RESULTS.md` | §9 |
| A5a Menu matrix | `A5a_menu.{csv,tex}` | `build_desc_tables.py` | `analysis/M1_RESULTS.md` | §5 |
| A5b Balloted vs submerged | `A5b_submerged.{csv,tex}` | `build_desc_tables.py` | `analysis/M2_RESULTS.md` | §5 |
| A5c Absolute coalitions | `A5c_coalitions.{csv,tex}` | `build_desc_tables.py` | `analysis/M3_RESULTS.md` | §5 |
| A5d Channel dollar sorting | `A5d_channel_sorting.{csv,tex}` | `build_desc_tables.py` | `analysis/B3_RESULTS.md` | §5 (gap fill) |
| A5e Raw first-stage shares | `A5e_firststage_raw.{csv,tex}` | `build_desc_tables.py` | `analysis/NATIONAL_ENTITY_RESULTS.md` | §5 (gap fill) |
| A6a–c Banked authorisation + rate cap | `A6a_chain.{csv,tex}`, `A6b_chain_timing.csv`, `A6c_ratecap.{csv,tex}` | `build_desc_tables.py` | `analysis/P3_RESULTS.md`, `analysis/P4_RESULTS.md` | §7 |
| A7 Blocked-majority demography | `A7_blocked.{csv,tex}` | `build_desc_tables.py` | `analysis/D6_RESULTS.md` | §8 |
| A8 Variable definitions | `A8_variables.{csv,tex}` | `build_desc_tables.py` | `paper/VARIABLES.md` (single source) | App V |
| A9 Validation | `A9_validation.{csv,tex}` | `build_desc_tables.py` | `analysis/VALIDATION_RESULTS.md`, `analysis/LINK_FINDINGS.md` | §4 |
| A-C1 Coverage check | `AC1_coverage.{csv,tex}`, `AC1b_count_sorting.csv` | `build_desc_tables.py` | `analysis/NC_COVERAGE_RESULTS.md` | §5 fn, App (round 4) |
| A-P1 County partisanship (demoted) | `AP1_county_partisanship.{csv,tex}` | `build_desc_tables.py` | `analysis/D5_EXTERNAL_RESULTS.md` | App (round 4), §8 caveat |

## Instruction-vs-record conflicts (FLAGGED, not silently obeyed)

1. **F4 "ten no-data states".** The instruction describes ten no-data states; under the
   frozen v3 package the map has **five** (DC, DE, HI, VT, WY — below the ≥50-document
   gate). Ten was the pre-v3 count; v3 recovered KY, TN, PA, NY, MS as real values. The
   figure shows five.
2. **F2 event window −3..+6.** The committed horizon indicators exist for k = −2..+5
   only (`_horiz` construction in `analysis/outcomes`); the figure plots −2..+5 and says
   so in its note. Extending to −3/+6 would need a panel rebuild — deferred (would touch
   the frozen frame).
3. **F5 density test statistics.** McCrary-style discontinuity and donut stability are
   reported (`analysis/MCCRARY_DONUT_RESULTS.md`); a Cattaneo–Jansson–Ma local-polynomial
   density test is **not implemented** (stdlib-only environment). The figure note states
   McCrary only.
4. **"MSE-optimal bandwidth h" in RD rows.** House convention (per the Appendix A1
   reconciliation) is bandwidth **fixed at ±10pp** with the IK/MSE-optimal row and the
   bandwidth-sensitivity curve in A1; every table note states this. The h column
   therefore reads ±10 rather than a per-row MSE-optimal value.
5. **PRELIMINARY rule notes** remain on T4, F4, A5e, and the rules-dependent appendix
   rows until the owner's pass-2 on the strict-rule coding (worklist:
   `analysis/RULES_PASS2_WORKLIST.md`).
