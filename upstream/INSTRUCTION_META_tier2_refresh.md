# INSTRUCTION — Meta session: auth-package tier-2 refresh (24 Aug 2026)

*From the analysis session (repo `mauhirt/authorisation`, round 3). Priority 1 is
a newly DIAGNOSED defect with a precise symptom list; priorities 2–4 are the
previously queued tier-2 items. Conventions as ever: versioned package, same
file names and column contract, per-state coverage table in the package README,
changelog for any semantic change to `auth_mode_final2`.*

## 1 · PRIORITY: the finance-flag gap in wave `w2_3_v3.2`

**Defect.** `has_new_money` (and apparently `has_refunding`) is BLANK for
essentially 100% of documents in a subset of states processed in extraction
wave `w2_3_v3.2`, while other states in the SAME wave carry full flags. Since
every downstream new-money outcome filters on `has_new_money`, these states
silently vanish from the menu matrix, the national entity/city panels' corpus
outcomes, the consent map, and the N-suite voted-share estimations.

**Evidence (from `auth_os.csv.gz`, new-money definition = has_new_money true &
has_refunding not true):**

| state | all docs | nm=true | nm blank | wave |
|---|--:|--:|--:|---|
| NY | 25,974 | 2 | 25,972 | w2_3_v3.2 |
| PA | 10,240 | 3 | 10,210 | w2_3_v3.2 |
| IN | 7,780 | 0 | 7,780 | w2_3_v3.2 |
| CO | 4,407 | 0 | 4,407 | w2_3_v3.2 |
| AL | 4,067 | 0 | 4,067 | w2_3_v3.2 |
| WA | 3,685 | 0 | 3,685 | w2_3_v3.2 |
| TN | 3,571 | 6 | 3,565 | w2_3_v3.2 |
| GA | 3,331 | 1 | 3,329 | w2_3_v3.2 |
| AZ | 2,952 | 0 | 2,952 | w2_3_v3.2 |
| VA | 2,688 | 10 | 2,675 | w2_3_v3.2 |
| SC | 2,257 | 5 | 2,250 | w2_3_v3.2 |
| **NC** | 2,159 | 1 | 2,158 | w2_3_v3.2 |
| — positive controls, same wave — | | | | |
| KY | 5,097 | 3,245 | 111 | w2_3_v3.2 |
| OK | 6,701 | 6,138 | 27 | w2_3_v3.2 |
| FL | (nm 3,350 at 98% determined) | | | w2_3_v3.2 |
| TX (w1 control) | 32,510 | 21,353 | 1,498 | w1_v3 |

NC matters doubly: it is an RD state, and its corpus new-money outcomes are
currently near-empty (its RD cell rides GFD survey outcomes).

**What to check, in order:**
1. Which pipeline stage populates `has_new_money`/`has_refunding`/`finance_types`
   (extractor prompt field vs post-hoc join from `finance_types`), and whether
   `w2_3_v3.2` ran that stage for the affected states or the join dropped them
   (key mismatch? partial batch? truncated run?).
2. Whether `classified_amount_usd`, `n_projects` and the `auth_projects` line
   labels are affected for the same states (downstream B3/M2 line-level work
   appears intact, which suggests the gap is isolated to the finance-type
   flags; please confirm from the pipeline side).
3. Whether `auth_mode_final2` determination for those states used any
   finance-type input (if so, determination may need a re-pass there too;
   observed determination rates are high where docs ARE flagged).

**Acceptance criteria for the refreshed package:**
- Every state with >500 documents has non-blank `has_new_money` on ≥90% of
  docs (the affected list above reaching KY/OK-like coverage).
- Already-covered states unchanged: TX and CA new-money doc counts and total
  `par_effective` stable within 1% of the current package (regression guard).
- Package README carries the per-state flag-coverage table.
- Version bump + changelog entry naming the wave fix.

## 2 · Queued tier-2 items (unchanged, secondary to §1)
- `election_date` enrichment (raises the validation-join match ceiling in
  states where OS cites exist but dates were not extracted).
- B4 authorisation-mode pass-2 where flagged in the package notes.

## 3 · Downstream contract (what reruns on receipt, this side)
One command each, in order: rebuild caches (`issuance_subset`, `b3_doc_flags`)
from the new package; `national_entity_panel.py`; `national_city_panel.py`;
`m1_menu_matrix.py`; `m2_balloted_submerged.py`; `f61_consent_map.py` (the
≥50-doc gate stays; the map should gain ~10 states); `national_regressions.py`
(N-suite cluster counts should rise; expect mostly STRICT states to enter —
WA, IN, NC, VA, AZ are referendum-strict, so first-stage cells fill
asymmetrically and the coverage sentence in the draft will be updated);
`b5_purpose_match.py` (frame may grow; audit protocol reruns on the new frame).
RD headline estimates do not move (they ride the referendum panel + GFD);
NC's corpus outcomes and the EMMA-side event study gain coverage.

## 4 · Reference
Diagnosis committed in `mauhirt/authorisation`: `analysis/F61_MAP_VALUES.md`
(coverage note), `analysis/ANALYSIS_REVIEW.md` §5b (consequence register),
commit "Diagnose consent-map NAs: w2_3 finance-flag gap; gate map at >=50
flagged docs".
