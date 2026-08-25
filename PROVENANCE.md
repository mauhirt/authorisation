# Provenance — every external input, pinned

| input | origin | pinned ref |
|---|---|---|
| inputs/elections/* (9 state datasets, precinct tables, crosswalk, rules) | mauhirt/muni_universe @ branch claude/download-cdiac-dpi-brb-bonds-08qstz | de0d0c8e4af03783d5ed6efbc1f4637ea8ce453f |
| inputs/corpus/* (auth_os, auth_issuer, issue_canonical, auth_projects + codebook) | mauhirt/muni_universe @ branch claude/meta-project-progress-4cesyb, output/auth_paper/ | c5aed9c586cdd0aea493c26d3d400c8e57941859 |
| inputs/gfd/* | Government Finance Database, Willamette Univ. (vintage 2025-10-03, yrs 1967–2023); Drive ids + method in inputs/gfd/PROVENANCE.md | fetched 2026-08-24 |
| inputs/elections/rules/state_debt_rules.csv | owner-supplied state debt-rules panel, AI pass-1, PRELIMINARY (ICR 78–88%, verified=0) | uploaded 2026-08-24 |
| raw/sources/pass2/* (40 statutory/constitutional texts for the pass-2 worklist) | state legislature / code-revisor sites (3 mirror fallbacks flagged); per-file url, date, sha256 in raw/sources/pass2/MANIFEST.csv; fetch script raw/sources/pass2/fetch_pass2.py | fetched 2026-08-25 |

The crosswalk (referendum → Census unit_id) is fully verified upstream: exact tiers
~100%, fuzzy tier 95.1% RA-measured with all errors adjudicated, selection at the
threshold measured and neutralized. QA artifacts and regression tests live in
muni_universe at data/elections/crosswalk/ (same pin).
