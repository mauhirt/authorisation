# Authorization-paper analysis package

Three analysis-ready grains, 2005–2025 frame, built from the canonical master
(`claude/fold-scopeA-final` @b92ba4b504) + the meta crosswalks + the auth
quick-win overlay. Rebuild anytime with:
`python3 meta/refresh/build_auth_package.py <os_master.csv.gz> <os_projects_clean.csv.gz>`
(deterministic; re-run after tier-2 lands to pick up the upgraded auth layer).

## Files

### 1. `auth_os.csv.gz` — one row per official statement (~258.8k)
The core estimation table. Column groups:

- **Keys/frame**: doc_id, issue_id, issuer_id, issuer_name, state, year, dated_date.
- **Bond characteristics**: par_amount + `par_effective`/`par_source` (stated,
  else EMMA fill), instrument_type, n_series, maturity_first/last, sale_method,
  tax_designation, federal_tax_status, bank_qualified, security_type_normalized
  + `security_level` (ordinal) + `security_pledge_class` (GO/revenue/lease/
  special_tax/conduit), underlying ratings (S&P/Moody's/Fitch), credit_enhancer,
  covenants (additional_bonds_test, rate_covenant), redemption/sinking fund.
- **EMMA security layer**: emma_has_scale, n_securities, total principal,
  coupon min/max, maturity range, `emma_issue_shared_by_n_docs` (dedup guard —
  if >1, issue-level totals span several docs; dedup on issue_id before summing).
- **AUTHORIZATION — use `auth_mode_final2`** (voter / council_or_board /
  statutory / refunding_no_new_election / unknown): the master's resolved stack
  PLUS the definitional refunding overlay (3,544 docs). Provenance in
  `auth_mode_final2_source` (recode | reextract | refunding_inferred |
  refunding_inferred_meta | none). `auth_determined2`, `auth_is_voter2` are the
  ready-made DV inputs. Non-exclusive signals kept: voter_approved,
  board_action, auth_mode_detailed (joint voter+council visible).
  `election_date` (the margin-join key), voter_auth_status, council action
  block, enabling-statute flag. `auth_mode_issue_propagated` is a SECONDARY
  signal (93.9% measured precision) — robustness only, never the primary DV.
- **Projects rollup**: n_projects, functional_classified, primary function/
  activity, finance_types, has_new_money/has_refunding, classified_amount_usd,
  any_green_eligibility.
- **Political jurisdiction**: pol_accountable_unit_id (Census GID — NOT FIPS,
  read as string, ~8% leading zeros), name/type/county, classification,
  assignment_status (assigned | conduit_private | pooled | unassigned — the
  last three are answers, not gaps); jurisdiction_class, county_fips/coverage/
  basis (accountability analyses filter county_basis=political).
- **Comparability**: prompt_version, extract_wave — condition on wave in any
  cross-state model.

### 2. `auth_issuer.csv.gz` — one row per issuer (~45k)
Issuer identity + political assignment + activity aggregates: n_docs,
year_first/last, total_par_docgrain_usd (doc-grain sum — shared-issue double
counting possible; for exact issue-grain totals dedup via the OS file),
mode counts (n_voter/n_council/n_statutory/n_refunding_auth),
`voted_share_determined`, n_election_dates, primary_function, n_green_docs.
Issuer-year panels: derive from auth_os (group by issuer_id × year).

### 3. `auth_projects.csv.gz` — one row per use-of-proceeds line (~2.85M)
The cleaned project table (zero duplicate line keys) filtered to the frame,
with per-line: label (160 chars), amount_usd (+amount_is_missing — only ~36%
of lines print dollars; use line-share × doc_par allocation), side,
functional_activity (118-label enum), finance_type, green eligibility,
is_subtotal_row (exclude from sums), and attached doc context: state, year,
issuer_id, auth_mode_final2, pol_accountable_unit_id, security_pledge_class,
doc_par_effective.

## The four rules that must hold in any aggregation
1. Group political entities on `pol_accountable_unit_id`, never on name.
2. conduit_private / pooled / unassigned are answers — filter, never fill.
3. Security/EMMA facts are issue-grain: dedup on issue_id before summing.
4. Condition cross-state models on `extract_wave`.

## Known state & upgrades in flight
- auth determination (final2) ~90.8% in-frame; tier-2 LLM pass running (the
  remaining ~18.9k unknowns + election_date enrichment) — re-run the builder
  when meta/targeted_pass/RESULT.md lands to lift to ~95% with more
  election_dates. Wave-state election_date is thin until then.
- security ladder ~92%; same tier-2 pass lifts toward ~97%.
- MSRB vote-margin joins: election_date + state + issuer → owner's external
  election-results crosswalk (downstream merge, not extracted).
