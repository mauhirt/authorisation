# N1–N5 — the national regression suite (entity panel)

WLS, state-clustered SEs, region FE; controls: ln size, homeownership, 65+,
fractionalization, ln median income, county Dem 2020. **Rule coefficients are
FIRST-STAGE/DESCRIPTIVE (rules PRELIMINARY pass-1); causal readings HELD.**
Townships excluded from headlines (proxy rule), shown as robustness.

## N1 · First stage: OS-evidenced voted $ share ~ rule_strict
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| pooled (4 classes, entity dummies) | | +0.0988 | 0.1165 | 0.85 | 13,928 | 48 |
| school_district | | +0.6902 | 0.1540 | 4.48 | 6,857 | 41 |
| municipal | | +0.2040 | 0.0353 | 5.77 | 3,176 | 37 |
| county | | +0.1078 | 0.0918 | 1.17 | 1,456 | 43 |
| special_district | | +0.1756 | 0.0509 | 3.45 | 2,439 | 37 |
| +townships (proxy rule) robustness | | +0.0895 | 0.1216 | 0.74 | 14,422 | 48 |

**MISSING / TO-DO:** rules pass-2 (all cells); TOWNSHIP rule column (proxy breaks in town-meeting states); rule TIME variation not coded (latest-year rule vs 2005–25 outcomes — reform years unmodeled); state-level TEL/debt-limit controls missing (only big-city TEL exists); issuer-vs-accountable-state mismatch for cross-border conduits; SPECIAL DISTRICTS: no GFD Population — ln size = ln total revenue (fiscal-size proxy), so their lnsize is not comparable to other classes' population control.

## N2 · Composition/substitution: security & purpose ~ rule_strict
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| GO security share (pooled) | | -0.1547 | 0.0861 | -1.80 | 14,273 | 48 |
| GO security share (general-purpose: muni+county) | | -0.2767 | 0.0703 | -3.93 | 4,766 | 46 |
| non-chargeable share (pooled) | | -0.0490 | 0.0457 | -1.07 | 9,280 | 48 |
| non-chargeable share (general-purpose) | | -0.0872 | 0.0541 | -1.61 | 3,340 | 46 |

**MISSING / TO-DO:** nc-share weight is nm_par (classified-$ base not stored in panel — add amt_classified column); schools ~100% nc are degenerate for the nc spec (pooled row diluted — general-purpose row is the object); C2's cell-grain result (−0.162, t −1.83) is the FE-panel cousin; both HELD on pass-2.

## N3 · Extensive margin & survey totals
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| any corpus new-money 2005–25 (LPM) | | +0.0148 | 0.0295 | 0.50 | 56,541 | 48 |
| ln(1+GFD LTD issued 2005–23 p.c.) | | -0.2321 | 0.2167 | -1.07 | 56,541 | 48 |

**MISSING / TO-DO:** GFD no-report→0 assumption (non-response vs true zero unseparated — needs GFD sample-flag pass); corpus truncated at 2005 (EMMA era); levels cross-section = selection into existence of districts not modeled (unit birth/death); population denominators for specials are weak (county-service-area problem).

## N4 · TEL × rule (big-city subpanel, municipals)
| outcome | β(strict) | β(tel) | β(strict×tel) | SE(s×t) | t | n | clusters |
|---|--:|--:|--:|--:|--:|--:|--:|
| non-chargeable share | +0.005 | +0.345 | -0.638 | 0.494 | -1.29 | 358 | 34 |
| GO security share | -0.109 | +1.019 | -1.227 | 0.821 | -1.49 | 401 | 34 |
| voted $ share | +0.205 | +0.419 | -0.185 | 0.338 | -0.55 | 396 | 34 |

**MISSING / TO-DO:** TEL exists only for ~570 big cities (need a state-level TEL panel for the full universe); TEL stringency is one 2013-vintage index (no time variation); big-city sample = the exit-rich class where D4 predicts weak rule effects — power-limited by design.

## N5 · Moderators: who the rule binds for (national first stage)
| interaction | β(strict) | β(interaction) | SE | t | n | clusters |
|---|--:|--:|--:|--:|--:|--:|
| strict × homeownership (centered) | +0.096 | -0.047 | 0.395 | -0.12 | 13,928 | 48 |
| strict × county Dem share (centered) | +0.194 | -0.651 | 0.326 | -2.00 | 13,928 | 48 |

**MISSING / TO-DO:** moderators at COUNTY grain for schools/specials (SD-grain national requires extending the SAIPE/ACS-SD bridge to 50 states); homeownership here moderates the CHANNEL (first stage), not the RD issuance effect — the causal freeholder test remains the 9-state ACS_RESULTS one; county Dem is 2020 only (no panel).

