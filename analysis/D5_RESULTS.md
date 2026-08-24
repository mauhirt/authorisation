# D5 — heterogeneity of the authorization effect (GO issuance ≤6y, bw ±10)

Frame 11889; county-grain moderators matched 11582 (97.4%).
County moderators are a proxy for district electorates (first pass; ACS key
upgrade path in `acs_pull.py`). Split at the within-frame median.

| subgroup | n | τ | SE | z | n L/R |
|---|--:|--:|--:|--:|---|
| ALL (reference) | 11889 | +0.146 | 0.033 | 4.47 | 1596/2743 |
| 65+ share < median (0.128) | 5737 | +0.057 | 0.053 | 1.07 | 621/1151 |
| 65+ share ≥ median | 5845 | +0.201 | 0.041 | 4.87 | 975/1589 |
| fractionalization < median (0.565) | 5773 | +0.167 | 0.041 | 4.05 | 923/1427 |
| fractionalization ≥ median | 5809 | +0.125 | 0.051 | 2.45 | 673/1313 |
| median HH income < median (56670.000) | 5512 | +0.119 | 0.045 | 2.66 | 845/1301 |
| median HH income ≥ median | 6070 | +0.178 | 0.048 | 3.72 | 751/1439 |
| on-cycle (Nov, even yr) | 3167 | +0.252 | 0.057 | 4.39 | 476/1005 |
| off-cycle | 8722 | +0.099 | 0.039 | 2.52 | 1120/1738 |

**Read (descriptive, not asserted):** the effect concentrates in OLDER counties
(τ +0.201 vs +0.057) and ON-CYCLE elections (+0.252 vs +0.099) — authorization by a
broad, older electorate binds hardest, while off-cycle refusals (frequent, low-salience
election dates) are easiest to reverse, consistent with the re-submission mechanism.
Income splits mildly positive-rich; FRACTIONALIZATION runs slightly AGAINST the naive
H3 read (+0.167 low vs +0.125 high) — H3 is partially supported, not uniformly.
