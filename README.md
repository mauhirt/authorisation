# Who Must Agree — analysis repo

Bond authorisation rules as coalition requirements. Data infrastructure (raw state
election harvests, crosswalk QA, precinct scrapers) lives in `mauhirt/muni_universe`;
this repo holds the frozen analysis inputs, the analysis code, and results.
Single source of truth for scope: `BRIEF.md`. Provenance pins: `PROVENANCE.md`.

## Layout
- `inputs/elections/` — 9-state referendum datasets, precinct tables (NC, LA),
  the referendum→Census-unit crosswalk (86.6% assigned, verified), state debt-rules
  panel (PRELIMINARY).
- `inputs/corpus/` — the EMMA official-statement corpus extracts (auth_os 258,762
  docs; issue_canonical; auth_issuer; auth_projects 2.67M use lines + codebook).
- `inputs/gfd/` — Government Finance Database compact panels, unit×year 1967–2023,
  all five government types (2.10M rows), with the debt block (LTD issued FFC/NG,
  outstanding, retired) + FIPS bridge. `GOVSid == unit_id[:9] == pol_accountable_unit_id[:9]`.
- `analysis/` — the referendum↔issuance link (40,924 rows), rules merge + rd_sample
  flag, Step-0 reconcile, E1 margin-band gate, findings. Scripts run from repo root:
  `python3 analysis/build_referendum_issuance_link.py`, then `add_rules_to_link.py`.

## State of play (2026-08-24)
- rd_sample = 23,577 referenda at genuine mandatory-ballot cutoffs (TX/CA/LA/WI-sch/MN-sch/NC).
- First stage, CA/WI/TX core: naive +21pp passed-vs-failed issuance gap collapses to
  +6.3pp GO-issuance at ±5pp of the threshold (z=3.92); ~31% of barely-failed
  measures still issue within 6y (H1b raw material).
- 98.7% of crosswalked units have GFD fiscal records → balance tables, per-capita
  scaling, and an EMMA-independent LTD-issued outcome are unlocked.

## Conventions (from BRIEF)
Immutable inputs; provenance for every external file; each stage ends with a
RESULTS.md carrying raw numbers and dropped-row counts; no number outside script
output; anomalies flagged, never silently fixed.
