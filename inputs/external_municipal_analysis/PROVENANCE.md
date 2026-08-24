# External inputs from mauhirt/municipal-analysis (the green-bond paper repo)

Copied 2026-08-24 from branch `claude/data-consolidation` @ 85cd801bd563f824a73df4c9de5cd6d6f1345fb3 (read-only
attach). Catalog: that repo's DATA_CATALOG.md. Grain caveat: tel.csv, fog panel,
acs_demographics_2022, city_partisanship_panel cover the ~578-large-city panel
(fips7 place GEOID) — partial overlap with our mostly-small-place municipal
frame; state_* files and countypres are national.

| file | grain | use here |
|---|---|---|
| state_bond_referenda_requirements.csv | state | independent rules coding — cross-validation of our PRELIMINARY panel; + bond commission / debt-limit / approval-body institutions |
| state_bond_banks.csv | state | substitution infrastructure moderator |
| countypres_2000-2024.csv | county×election (MEDSL) | partisanship moderator, national |
| tel.csv | city-year | TEL stringency (second coalition constraint), large cities |
| fog_institutions_panel_2010_2024.csv | city-year | form of government, initiative/referendum powers |
| acs_demographics_2022.csv | city (fips7) | college/nonwhite/median home value, large cities |
| city_partisanship_panel.csv | city×election | precinct-aggregated Dem share, 577 cities |

Also available there (not copied): 2022/23/24 Census Individual Unit File zips
(4.1M etc.) — queued to extend the GFD-style survey outcome to FY2024.
