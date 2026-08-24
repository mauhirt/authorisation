# Referendum → Census unit crosswalk (8 states)

Maps each bond/referendum row in `data/elections/` to a Census of Governments
`unit_id`, so referenda join to municipal **issuance** for free through the
existing issuer→unit spine. Built per `../REFERENDA_CROSSWALK_PLAN.md`.

**States:** MA, WI (code-keyed pass) + TX, CA, IL, IN, LA, NC (name-match pass).
**Built:** 2026-08-23.

## Files
| file | what |
|---|---|
| `referendum_unit_crosswalk.csv` | one row per referendum → `unit_id`, graded (46,545 rows) |
| `referendum_unit_crosswalk_weakest_tier.csv` | fuzzy + unresolved rows, for review |
| `referenda_x_issuance_demo.csv` | per unit: referendum count + whether it also appears as a debt issuer |
| `build_ma_wi_crosswalk.py`, `build_6state_crosswalk.py` | reproducible builders |

## Inputs (read-only, from `claude/msrb-issuer-census-assignment-kjm4na`)
Blobless-fetched, not copied: per-state `census_government_universe_*.csv`
(match targets), `issuer_assignments_ALL.csv` (spine → `accountable_unit_id`),
`NOTE_DEPENDENT_FOLD_RULES_ISD.md` (fold rules).

## Method
Shared matcher: canonicalize names (strip `CITY/TOWN/COUNTY/PARISH OF` prefixes
and trailing type words; `MT`→`MOUNT`, `ST`→`SAINT`; census school abbreviations
`SCH/UNIF/ELEM/CU/IND/…` folded out); **county-block** every match; enforce
**type-consistency** (referendum kind ↔ census type group); keep the most recent
CoG vintage record per name. Exact normalized match → `3b_NAME_EXACT`; guarded
fuzzy (difflib ≥0.90, first-token match, **and equal district numbers**) →
`4_NAME_FUZZY` (flagged REVIEW); else `UNRESOLVED`.

Per-state adapters:
- **MA/WI** — see the code-keyed pass (`build_ma_wi_crosswalk.py`): MA municipality
  → municipal/township; WI DPI district → school_district.
- **TX** — `governmenttype` → kind (CITY/COUNTY/ISD/CCD/WD…); numbered ISDs/MUDs
  matched **number-in-county** first, then name.
- **CA** — kind inferred from `Agency Name`; school/city/county/special, county-blocked.
- **IL** — derived `gov_type` → kind; numbered school districts matched by
  **number-in-county** (e.g. `CCSD 168`).
- **IN** — derived `gov_type` → kind; county-blocked name match.
- **LA** — parse entity + type from `specific_title`: parishwide → parish (county
  unit); municipal → municipal; **sub-parish school districts fold to the parish
  school board** (independent in LA); dependent sub-parish agencies (fire/water/
  sewer/ambulance/mosquito/…) fold to parish; levee/port stay independent.
- **NC** — parse jurisdiction from `contest_name`; **school & community-college
  bonds fold to the COUNTY** (NC has zero independent school governments — ISD
  confirms all 173 dependent); city/county measures match directly.

## Coverage
| state | referenda | ASSIGNED | exact / fuzzy | UNRESOLVED |
|---|---:|---:|---|---:|
| MA | 7,022 | 7,022 (100%) | 7,022 / 0 | 0 |
| WI | 2,450 | 2,334 (95.3%) | 2,279 / 17 | 116 |
| TX | 10,519 | 8,171 (77.7%) | 8,106 / 45 | 2,348 |
| CA | 7,149 | 5,988 (83.8%) | 5,782 / 140 | 1,161 |
| IL | 11,942 | 9,628 (80.6%) | 9,324 / 162 | 2,314 |
| IN | 290 | 280 (96.6%) | 264 / 0 | 10 |
| LA | 6,895 | 6,589 (95.6%) | 6,580 / 5 | 306 |
| NC | 278 | 278 (100%) | 278 / 0 | 0 |
| MN | 690 | 634 (91.9%) | 228* / 0 | 56 |
| **total** | **47,235** | **40,924 (86.6%)** | 39,863 / 369 | 6,311 |

\* MN schools resolve on the ISD-number **key** (`3_KEY_MATCH`), not `3b_NAME_EXACT`.

**LA re-worked for selection (fix #1, 2026-08-23):** the LA classifier now folds
every non-municipal / non-school / non-levee-port body to the parish (dependent per
the ISD rules) unless it matches an **independent** CoG special unit; handles the
four **consolidated city-parish governments** (Baton Rouge, Lafayette, New Orleans,
Houma — municipal-typed, no county unit), the `TERREBONNE`→`TERREBONE` county
spelling in the CoG file, and a robust `City/Town/Village of X` name extraction.
LA rose **70.1% → 95.5%** (+1,756), which **eliminated LA's close-window selection
gap** (+4.5pp → −1.7pp, n.s.) and cut the pooled threshold discontinuity from
+3.46pp (z=4.06) to +2.30pp (z=3.08). See `review/selection/SELECTION_FINDINGS.md`.

**Second-opinion review applied (fix, 2026-08-24):** an adversarial pass
(`review/second_opinion_flags.csv`) over the units-needing-review file confirmed
**every flagged row was already UNRESOLVED here** — i.e. it found *no* false
assignment of ours; the cross-function accepts it caught (fire→park, JCD→WCID) were
the external adjudicator's, which our guards already reject. Its actionable flags
were all recall misses, now closed: WI `J1`==`Joint School District 1` (builder),
hyphen suffix `1-H`==`01H` (builder + `school_key` number regex), and 208
same-body spelling/abbreviation variants via a **function-guarded overlay**
(`apply_second_opinion.py`, `1_ADJUDICATED`). Overall **86.0% → 86.7%**. See
`review/SECOND_OPINION_RESPONSE.md`.

**Fuzzy-tier precision measured (2026-08-24):** the full 388-row `4_NAME_FUZZY`
tier was RA-labeled (`review/fuzzy_review_labeled.csv`; 213 distinct matches).
**Precision = 95.1%** (369/388 rows; 204/213 matches). The 9 wrong matches — all
cross-type look-alikes (Union-High vs Elementary; `ID`/`LID`/`JCD`/`MMD` vs
`WCID`/`MUD`) — are resolved: 6 reassigned to the correct unit (11 rows), 3 demoted
to UNRESOLVED (body absent from the CoG universe: TX MMDs / county Improvement
Districts). Confirmed rows carry `fuzzy_reviewed_correct` in `notes`. **No open
verification items remain.** See `review/FUZZY_REVIEW_RESPONSE.md`.

**Build order:** `build_ma_wi_crosswalk.py` → `build_6state_crosswalk.py` →
`apply_ra_adjudications.py` → `apply_second_opinion.py` → `apply_fuzzy_review.py`.

**RA review applied (2026-08-23):** a 535-row stratified sample was hand-labeled
(`review/`). Exact/key tiers verified ~100% correct; 4 fuzzy wrongs found. Fixes
shipped: an empty-key guard; a leading-zero-safe number guard (01==1) with exact
lettered-suffix + **conditional** entity-type rejection; district-type
canonicalization (MUD↔Municipal Utility District) + abbreviation normalization
(net **+396 assigned**, risky fuzzy tier 1,278 → 385); 68 RA corrections overlaid
at `1_ADJUDICATED`; and a committed regression test. See `review/REVIEW_RESPONSE.md`.
(Fuzzy-tier precision was later measured at **95.1%** — see the fuzzy-review note
above.) Deferred recall items need external files (MN MDE ISD#→name, LA ballot-text
parse, WI DPI codes).

MN uses the ISD-number **key** for schools (`3_KEY_MATCH`) and scope-typed name
match for city/township; issuance-join 87%. Residual 57 are SSD/CSD/renumbered
ISDs.

`evidence_strength`: `3b_NAME_EXACT` (high confidence), `4_NAME_FUZZY` (review),
`5_UNRESOLVED`.

## Validation — issuance join (`referendum.unit_id == spine.accountable_unit_id`)
Share of assigned referenda whose unit also appears as a debt issuer:
**MA 96% · TX 97% · IN 99% · NC 97% · CA 91% · WI 86% · IL 60% · LA 63%.**
The high rates confirm the crosswalk is in the same key space as issuance. IL/LA
are lower **by nature, not error** — many small IL school/park/library/township
and LA fire/water/sewer districts hold referenda but never issued MSRB debt (or
weren't in the OS read); their higher unresolved share also contributes.

## Known limitations (residuals are in the weakest-tier file, not forced)
- **NC (now 0 unresolved):** re-harvested with the per-precinct county retained,
  which enabled school/CC→county folding, county-blocked city matching, and a
  longest-municipal-prefix match — closing NC from 61% to 100%.
- **LA (2,063):** entity/type are parsed from ballot-title text; propositions
  whose title doesn't expose the type, and independent sub-parish special
  districts, remain unresolved.
- **IL (2,603) / TX (2,587):** residual numbered districts and special districts
  with no exact number-in-county counterpart; the number guard deliberately
  refuses same-place/different-number fuzzy matches (a precision fix — it removed
  ~840 false TX MUD matches).
- **WI (217):** hyphenated/numbered districts — closeable with an NCES↔CoG bridge.
- Matches are on `unit_id`, never on names; DEP school units are never direct
  targets (folded per the ISD rules).
