# RD — full outcome set (rd_sample ∩ bond_go)

Frame n = 11889. Local-linear, triangular kernel, HC0 SEs (`rdlib.py`).
GFD windows use fiscal years [y+1, y+6]; GFD ends FY2023, so recent votes have
partial windows — symmetric across the cutoff, so the RD contrast is unaffected.

## A · Intensive margin + EMMA-independent outcomes
| outcome | bw | τ | SE | z | n L/R | left mean |
|---|--:|--:|--:|--:|---|--:|
| ln(1+ EMMA new-money par p.c.), 6y | ±5 | +0.910 | 0.430 | 2.12 | 931/1219 | 4.054 |
| ln(1+ EMMA new-money par p.c.), 6y | ±10 | +0.918 | 0.307 | 2.99 | 1537/2627 | 4.088 |
| ln(1+ GFD LTD issued p.c.), 6y  [EMMA-independent] | ±5 | +1.065 | 0.381 | 2.80 | 727/937 | 6.849 |
| ln(1+ GFD LTD issued p.c.), 6y  [EMMA-independent] | ±10 | +1.036 | 0.272 | 3.81 | 1202/2039 | 6.894 |
| ln(1+ GFD FFC (guaranteed) issued p.c.), 6y | ±5 | -0.028 | 0.261 | -0.11 | 727/937 | 0.827 |
| ln(1+ GFD FFC (guaranteed) issued p.c.), 6y | ±10 | -0.188 | 0.189 | -0.99 | 1202/2039 | 0.930 |
| ln(1+ GFD nonguaranteed issued p.c.), 6y | ±5 | +0.160 | 0.071 | 2.25 | 727/937 | -0.003 |
| ln(1+ GFD nonguaranteed issued p.c.), 6y | ±10 | +0.066 | 0.041 | 1.60 | 1202/2039 | 0.011 |
| PLACEBO: ln(1+ GFD LTD issued p.c.), years −3..−1 | ±5 | +0.434 | 0.385 | 1.13 | 909/1182 | 4.539 |
| PLACEBO: ln(1+ GFD LTD issued p.c.), years −3..−1 | ±10 | +0.377 | 0.274 | 1.38 | 1495/2551 | 4.409 |

## B · Authorization channel of post-vote EMMA issuance (substitution)
council_share_6y = council/(voter+council) among the unit's window docs (conditional on ≥1 determined doc).
| outcome | bw | τ | SE | z | n L/R | left mean |
|---|--:|--:|--:|--:|---|--:|
| council share of authorized window docs | ±5 | -0.030 | 0.044 | -0.68 | 520/849 | 0.307 |
| council share of authorized window docs | ±10 | -0.064 | 0.031 | -2.03 | 860/1821 | 0.317 |
| # voter-authorized docs, 6y | ±5 | +0.064 | 0.187 | 0.34 | 967/1267 | 1.300 |
| # voter-authorized docs, 6y | ±10 | +0.194 | 0.125 | 1.55 | 1596/2743 | 1.168 |
| # council-authorized docs, 6y | ±5 | +0.337 | 0.257 | 1.31 | 967/1267 | 0.803 |
| # council-authorized docs, 6y | ±10 | +0.147 | 0.172 | 0.85 | 1596/2743 | 0.843 |

## C · Event study: τ_k on 1(any new-money EMMA issue in relative year k), bw ±10
| rel. year k | τ_k | SE | z | left mean |
|---|--:|--:|--:|--:|
| −2 | +0.007 | 0.020 | 0.34 | 0.103 |
| −1 | +0.022 | 0.019 | 1.15 | 0.079 |
| 0 | +0.236 | 0.030 | 7.83 | 0.229 |
| +1 | -0.008 | 0.025 | -0.33 | 0.178 |
| +2 | -0.033 | 0.024 | -1.39 | 0.153 |
| +3 | -0.024 | 0.020 | -1.16 | 0.107 |
| +4 | -0.000 | 0.019 | -0.01 | 0.084 |
| +5 | -0.006 | 0.018 | -0.34 | 0.081 |

Pre-vote years (−2, −1) are placebos: τ should be ≈0 there and jump at 0/+1.

## Interpretation & caveats
1. **The effect is real in two independent measurement systems.** Barely-authorized
   districts issue **+0.92 log points more EMMA new-money par per capita** (z=2.99)
   AND **+1.04 log points more Census-surveyed LTD per capita** (z=3.81) within 6
   years. The GFD outcome is collected by the Census Bureau from the governments
   themselves and includes debt that never posts an OS (bank loans, private
   placements) — the survivorship critique of the EMMA corpus cannot explain it.
   The pre-period placebo is insignificant (+0.38, z=1.38).
2. **The dynamic profile is a timing effect with partial catch-up.** Event study:
   pre-vote placebos ≈ 0 (τ₋₂=+0.007, τ₋₁=+0.022, n.s.); a sharp **+23.6pp jump in
   the year of the vote (z=7.83)**; years +1…+5 ≈ 0 to slightly negative. Barely-
   authorized districts issue immediately; barely-refused ones partially catch up —
   consistent with the 53% re-submission rate. Refusal chiefly *delays*; the 6-year
   cumulative wedge (+15pp extensive, ~+1 log point intensive) is what remains
   after catch-up.
3. **Substitution evidence (H1b):** after a narrow refusal, the authorization mix
   of what the unit still issues tilts toward the council channel — council share
   τ=−0.064 (z=−2.03, bw10; the sign means barely-PASSED units are less
   council-reliant). Modest but in the theory's direction.
4. **Caveat — FFC/NG split is half-reported:** only 53.4% of GFD unit-years with
   positive LTD issuance carry a nonzero FFC/NG decomposition, so the
   guaranteed-vs-nonguaranteed results are exploratory; the TOTAL LTD result
   (fully reported) is the reliable EMMA-independent outcome.
5. Scaling: per-capita uses GFD Population, falling back to Enrollment for school
   districts (population is structurally absent for schools in the survey).
