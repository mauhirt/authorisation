# RD — full outcome set (rd_sample ∩ bond_go)

Frame n = 11889. Local-linear, triangular kernel, HC0 SEs (`rdlib.py`).
GFD windows use fiscal years [y+1, y+6]; GFD ends FY2023, so recent votes have
partial windows — symmetric across the cutoff, so the RD contrast is unaffected.

## A · Intensive margin + EMMA-independent outcomes
| outcome | bw | τ | SE | z | n L/R | left mean |
|---|--:|--:|--:|--:|---|--:|
| ln(1+ EMMA new-money par p.c.), 6y | ±5 | +0.910 | 0.430 | 2.12 | 931/1219 | 4.054 |
| ln(1+ EMMA new-money par p.c.), 6y | ±10 | +0.918 | 0.307 | 2.99 | 1537/2627 | 4.088 |
| ln(1+ GFD LTD issued p.c.), 6y  [EMMA-independent] | ±5 | +0.796 | 0.356 | 2.24 | 751/986 | 7.312 |
| ln(1+ GFD LTD issued p.c.), 6y  [EMMA-independent] | ±10 | +0.827 | 0.252 | 3.27 | 1238/2128 | 7.299 |
| ln(1+ GFD FFC (guaranteed) issued p.c.), 6y | ±5 | -0.043 | 0.253 | -0.17 | 751/986 | 0.808 |
| ln(1+ GFD FFC (guaranteed) issued p.c.), 6y | ±10 | -0.197 | 0.183 | -1.07 | 1238/2128 | 0.901 |
| ln(1+ GFD nonguaranteed issued p.c.), 6y | ±5 | +0.153 | 0.068 | 2.25 | 751/986 | -0.003 |
| ln(1+ GFD nonguaranteed issued p.c.), 6y | ±10 | +0.063 | 0.039 | 1.59 | 1238/2128 | 0.010 |
| PLACEBO: ln(1+ GFD LTD issued p.c.), years −3..−1 | ±5 | +0.484 | 0.384 | 1.26 | 909/1183 | 4.575 |
| PLACEBO: ln(1+ GFD LTD issued p.c.), years −3..−1 | ±10 | +0.412 | 0.273 | 1.51 | 1495/2553 | 4.453 |

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
