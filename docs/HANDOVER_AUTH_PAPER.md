# Handover → Rights-of-Refusal / authorization paper session: the analysis package + what the paper may claim

**From:** meta session (`claude/meta-project-progress-4cesyb` @ ab8fb1ad1a) · 2026-08-24
**Supersedes** the residual caveats in the fold-landing notice (FL gap, EMMA scale
gap, os_projects duplicates — ALL resolved; details in meta/findings/UNITS_OF_ANALYSIS.md).

## The package (output/auth_paper/ on the meta branch)

| file | rows | grain |
|---|---:|---|
| auth_os.csv.gz | 258,762 | one per official statement, ~70 vars |
| issue_canonical.csv.gz | 207,835 | one canonical doc per ISSUANCE (dedup layer) |
| auth_issuer.csv.gz | 43,029 | one per issuer, mode counts + voted_share |
| auth_projects.csv.gz | 2,671,437 | one per use-of-proceeds line, doc context attached |

Codebook: AUTH_PAPER_PACKAGE.md (same directory). Rebuild after upgrades:
`python3 meta/refresh/build_auth_package.py <master> <projects>` — schema-stable.

## SCOPE — what the paper can claim (each clause verified, 2026-08-24)

1. **Universe**: every official statement retrievable from MSRB EMMA for
   municipal issues dated 2005–2025, across all 50 states, DC, and PR/GU/VI:
   **258,762 documents representing 207,835 distinct debt issuances by 43,029
   issuers.** A near-census of EMMA-posted primary-market disclosure, not a sample.
2. **Completeness chain**: state crawls indexed the full EMMA search universe;
   ≥99% of indexed documents yielded usable text; the master carries ~100% of
   usable indexed documents (per-state reconciliation on record; residual gaps
   are single digits per state and explained). No known missing documents at scope.
3. **Deduplication**: preliminary and final filings are collapsed — issuance-grain
   analyses use issue_canonical (one document per issuance; 44,013 multi-doc
   issuances deduped by EMMA-named > par-stated > latest rule). Doc-id patterns
   do NOT distinguish preliminary/final (tested and rejected); the text banner does.
4. **Variable coverage (in-frame)**: authorization mechanism determined **92.7%**
   (council 62.4 / voter 18.3 / refunding 6.1 / statutory 5.9 / unknown 7.3) —
   an in-flight LLM pass over the remaining unknowns is expected to land ~95%+
   with enriched election_date (currently 13.3%); security pledge class 95.8%;
   par 95.4% (with EMMA-derived fills, provenance flagged); political
   accountability: 87.4% assigned to an exact Census government unit + 10.4%
   conduit/pooled BY DESIGN (an answer) → true unknown 2.2%; functional
   classification on 2.67M use lines (118 labels).
5. **What the corpus is NOT**: issues that never post an OS on EMMA (private
   placements, direct bank loans) are out of frame by construction; pre-2005
   issuance outcomes are out of frame (Scope A policy); vote margins are an
   external join on election_date; territories lack the EMMA security-scale layer.

## Methods sentences the paper can use (all backed by committed artifacts)

- Authorization provenance is per-document (`auth_mode_final2_source`); the
  refunding convention (refunding rides prior authorization) is applied
  explicitly, not silently.
- All name-based steps were validated against known-answer subsets with
  measured precision (county geo-parse 96.8%; issue-propagation 93.9% —
  therefore shipped only as a flagged SECONDARY signal; LLM auth answers 89.2%
  agreement with a noisy baseline, abstention-permitted, evidence-quoted, and
  security answers pass a deterministic evidence-in-window guard).
- Cross-state models condition on extract_wave; entity aggregation uses Census
  GID keys; issue-grain facts dedup on issue_id.

## Expected update (no schema change)

The in-flight pass (~19k auth unknowns + ~16k security blanks, window-based,
evidence-guarded) lands within ~a day; the package regenerates by one command.
Claims above are safe to draft against now — coverage numbers only move UP.
