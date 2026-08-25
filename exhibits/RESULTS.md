# Exhibit cross-checks (required by INSTRUCTION_exhibits build requirement 2)

Generated with the exhibit build; regenerate context with `make exhibits`.
Draft = `paper/EMPIRICS_DRAFT.md` (round-4 state, v3 freeze).

## List 1 — draft numbers with no exhibit home

Checked every quantitative claim in §§4–9 against the exhibit set. Two gaps were found
and **filled during this build** (they are exhibits now, listed for the record):

1. §5 channel dollar sorting (11.3% / 60.0% / 72.5% of dollars in voted, mixed,
   non-voted channels) — had no table; now **A5d_channel_sorting** (from
   `analysis/B3_RESULTS.md`).
2. §5 raw voted-dollar shares by class under strict vs non-strict rules (schools 68.4
   vs 7.4; municipalities 22.2 vs 3.7; counties 23.3 vs 5.4) — cited in prose around
   T4's regression coefficients but had no descriptive home; now **A5e_firststage_raw**
   (from `analysis/NATIONAL_ENTITY_RESULTS.md`).

Remaining numbers with no exhibit home: **none material**. Two deliberate exceptions,
left in prose only: (a) §4 corpus-build engineering counts (page/parse tallies) —
process description, not results; (b) §7's single KM survival figure at 4y (58.2%) is a
cell of T5 Panel B, cited directly.

## List 2 — exhibit cells with no draft sentence

1. **T3 row "Voter-mode first issuance ≤6y"** (RBC +0.184 [+0.089, +0.278], p<0.001).
   The draft discusses mode composition of post-pass issuance but never states this RD
   directly. Recommend one sentence in §6.
2. **A2 placebo-threshold table** (all four pseudo-cutoffs null at 5%). §6 asserts
   placebo checks pass but cites no specific estimates. Recommend one sentence citing
   A2; note the pseudo-45 marginal p = 0.057 (see NUMBERS_DIFF.md item 4) so the
   sentence should say "null at the 5% level" rather than "precisely zero".
3. **A1a horizons figure / A1b bandwidth-sensitivity curve** — referenced generically
   ("robust across horizons and bandwidths") without pointing at the figures. Recommend
   adding the figure cross-references to the §6 robustness paragraph.
4. **A4b passage-rates-by-threshold CSV and A4c TX-2019 unbundling table** — §9 gives
   the headline pair and the unbundling narrative; the full grids are exhibit-only.
   Acceptable as appendix-only detail; no action needed.

## Notes

- The five instruction-vs-record conflicts (map no-data count, event window, density
  test, bandwidth convention, PRELIMINARY notes) are flagged in `EXHIBITS.md`.
- Values that moved under final (RBC-convention) specifications are in
  `NUMBERS_DIFF.md`; the draft still carries the older conventional citations until
  the next text pass.
