# N1–N5 — the national regression suite (entity panel)

WLS, state-clustered SEs, region FE; controls: ln size, homeownership, 65+,
fractionalization, ln median income, county Dem 2020. **Rule coefficients are
FIRST-STAGE/DESCRIPTIVE (rules PRELIMINARY pass-1); causal readings HELD.**
Townships excluded from headlines (proxy rule), shown as robustness.

## N1 · First stage: OS-evidenced voted $ share ~ rule_strict
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| pooled (4 classes, entity dummies) | | +0.2483 | 0.1163 | 2.13 | 11,044 | 39 |
| school_district | | +0.7784 | 0.1107 | 7.03 | 5,602 | 33 |
| municipal | | +0.1707 | 0.0596 | 2.86 | 2,575 | 28 |
| county | | +0.1361 | 0.0928 | 1.47 | 1,057 | 34 |
| special_district | | +0.1989 | 0.0632 | 3.15 | 1,810 | 28 |
| +townships (proxy rule) robustness | | +0.2526 | 0.1160 | 2.18 | 11,537 | 39 |

**MISSING / TO-DO:** rules pass-2 (all cells); TOWNSHIP rule column (proxy breaks in town-meeting states); rule TIME variation not coded (latest-year rule vs 2005–25 outcomes — reform years unmodeled); state-level TEL/debt-limit controls missing (only big-city TEL exists); issuer-vs-accountable-state mismatch for cross-border conduits; SPECIAL DISTRICTS: no GFD Population — ln size = ln total revenue (fiscal-size proxy), so their lnsize is not comparable to other classes' population control.

## N2 · Composition/substitution: security & purpose ~ rule_strict
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| GO security share (pooled) | | -0.1241 | 0.1321 | -0.94 | 11,343 | 39 |
| GO security share (general-purpose: muni+county) | | -0.3450 | 0.0671 | -5.14 | 3,736 | 37 |
| non-chargeable share (pooled) | | -0.1008 | 0.0371 | -2.72 | 7,403 | 38 |
| non-chargeable share (general-purpose) | | -0.1713 | 0.0517 | -3.31 | 2,584 | 36 |

**MISSING / TO-DO:** nc-share weight is nm_par (classified-$ base not stored in panel — add amt_classified column); schools ~100% nc are degenerate for the nc spec (pooled row diluted — general-purpose row is the object); C2's cell-grain result (−0.162, t −1.83) is the FE-panel cousin; both HELD on pass-2.

## N3 · Extensive margin & survey totals
| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |
|---|---|--:|--:|--:|--:|--:|
| any corpus new-money 2005–25 (LPM) | | +0.0060 | 0.0415 | 0.14 | 56,541 | 48 |
| ln(1+GFD LTD issued 2005–23 p.c.) | | -0.2321 | 0.2167 | -1.07 | 56,541 | 48 |

**MISSING / TO-DO:** GFD no-report→0 assumption (non-response vs true zero unseparated — needs GFD sample-flag pass); corpus truncated at 2005 (EMMA era); levels cross-section = selection into existence of districts not modeled (unit birth/death); population denominators for specials are weak (county-service-area problem).

## N4 · TEL × rule (big-city subpanel, municipals)
| outcome | β(strict) | β(tel) | β(strict×tel) | SE(s×t) | t | n | clusters |
|---|--:|--:|--:|--:|--:|--:|--:|
| non-chargeable share | -0.131 | +0.385 | -0.305 | 0.532 | -0.57 | 277 | 25 |
| GO security share | -0.545 | +0.102 | -0.257 | 0.825 | -0.31 | 310 | 25 |
| voted $ share | +0.144 | +0.077 | -0.030 | 0.331 | -0.09 | 305 | 25 |

**MISSING / TO-DO:** TEL exists only for ~570 big cities (need a state-level TEL panel for the full universe); TEL stringency is one 2013-vintage index (no time variation); big-city sample = the exit-rich class where D4 predicts weak rule effects — power-limited by design.

## N5 · Moderators: who the rule binds for (national first stage)
| interaction | β(strict) | β(interaction) | SE | t | n | clusters |
|---|--:|--:|--:|--:|--:|--:|
| strict × homeownership (centered) | +0.268 | +0.313 | 0.231 | 1.36 | 11,044 | 39 |
| strict × county Dem share (centered) | +0.358 | -0.760 | 0.359 | -2.12 | 11,044 | 39 |

**MISSING / TO-DO:** moderators at COUNTY grain for schools/specials (SD-grain national requires extending the SAIPE/ACS-SD bridge to 50 states); homeownership here moderates the CHANNEL (first stage), not the RD issuance effect — the causal freeholder test remains the 9-state ACS_RESULTS one; county Dem is 2020 only (no panel).

