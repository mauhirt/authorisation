# GFD pull — RESULTS (2026-08-24)

All numbers are script output (`extract_compact.py`, `validate_gfd_join.py`).

## Extraction
2,097,197 unit-year rows, 1967–2023, national, 36 columns, ~68 MB gzipped across
five per-type panels (school 650,062 · special 545,729 · municipal 452,685 ·
township 329,694 · county 119,027). Zero rows dropped; missing-column list empty
for every type.

## Join validation (crosswalked referendum units with GFD fiscal records)
| census_type | my units | in GFD | rate | 2012+ | FIPS_Place fill |
|---|--:|--:|--:|--:|--:|
| school_district | 3,022 | 3,020 | 99.9% | 98.7% | 0% (bridge = NCES/SD geography) |
| municipal | 1,675 | 1,672 | 99.8% | 99.7% | 100% |
| township | 1,035 | 1,035 | 100% | 99.9% | 100% |
| county | 342 | 342 | 100% | 100% | 100% |
| special_district | 1,615 | 1,517 | 93.9% | 91.8% | 0% (county proxy) |
| **total** | **7,689** | **7,586** | **98.7%** | | |

Key identity verified: `GOVSid` == `unit_id[:9]` == `pol_accountable_unit_id[:9]`.

## What this unlocks
- **RD balance tables** on predetermined fiscal covariates (pre-vote debt, revenue,
  property-tax base) — join by construction.
- **Per-capita scaling** (Population column; Enrollment for schools).
- **EMMA-independent outcome:** `Total_LTD_Issued` (with the **FFC vs NG** split)
  captures borrowing that never posts an OS (bank loans, private placements) —
  the H1b substitution channel the corpus alone cannot see.
- **ACS bridge:** FIPS_Place 100% for general-purpose governments; schools via
  NCES/school-district geography; special districts flagged county-proxy.

## Anomalies flagged
- ~1,806 school rows (2012+) carry an empty GOVSid (F-33-only dependent entities);
  excluded from the join, not fixed.
- 103 crosswalked units (mostly special districts) have no GFD record — likely
  post-2017 creations or non-surveyed districts; listed as a residual, not filled.

## Panels' home
The 68 MB of compact panels are staged for the `who-must-agree` paper repo
(pending creation; the GitHub integration cannot create repositories). They
regenerate in ~10 min: download per-type zips (ids in PROVENANCE.md), then
`python3 extract_compact.py <raw.csv> <out.csv.gz> <type>`.
