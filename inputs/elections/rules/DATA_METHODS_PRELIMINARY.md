# Using the referendum variable now (Option A — preliminary)

You are using the **AI-coded, not-yet-human-verified** version of the treatment for
analysis now, and will run the human verification (`packages/ra_pass2_validation/`)
before final submission. This note gives you (1) the file to load, (2) how to merge
it, and (3) a ready-to-paste Data & Methods paragraph that states the caveat
honestly.

## 1. The file

`data/derived/referendum_analysis_extract.csv` — regenerate with `make analysis`.
One tidy row per **(state, entity_type, purpose, year)** at the state level
(`unit_stratum = all`), 2005–2026. Sub-state branches (home-rule, city/town, etc.)
live in `data/derived/referendum_operationalized.csv` if you need them.

Columns: `ref_required`, `ref_threshold`, `ref_variation_type` (raw), the six
encodings (`op_any_hurdle`, `op_ballot_required`, `op_referendum_strict`,
`op_ordinal`, `op_threshold_num`, `op_supermajority` — defined in
`docs/operationalizations.md`), and `verified = 0` / `data_status =
PRELIMINARY_pass1_AI_unverified` on every row.

## 2. Merge

```python
import pandas as pd
rules = pd.read_csv("data/derived/referendum_analysis_extract.csv")
muni_go = rules.query("entity_type=='municipality' and purpose=='go_debt'")   # your unit
df = your_bonds.merge(muni_go, on=["state", "year"], how="left")              # + year for the panel
# headline treatment: op_referendum_strict (1 = ballot referendum required)
```

- Match your **issuer type** to `entity_type` and your **instrument** to `purpose`
  (`go_debt` for GO bonds — the HMS-comparable treatment).
- If your data are cross-sectional, pick one year (e.g. 2024) and merge on `state`.
- **Tag cells** (`op_codable = 0`, ~13 states for municipal GO are structural-NA or
  conditional): decide up front to drop them or model `ref_variation_type`. Your
  clean sample is `op_codable == 1`.

## 3. Data & Methods paragraph (paste and edit)

> **Institutional treatment.** We measure each state's local voter-approval
> requirement for [general-obligation debt] from a purpose-built panel of state
> constitutional and statutory rules covering all 50 states, five local
> entity types (municipality, county, school district, special district, authority),
> and the 2005–2026 period. For each state–entity–purpose–year we code whether
> issuance requires voter approval and, if so, the mechanism and passage threshold,
> distinguishing an elected body's authorization (`none`), a petition-triggered
> "reverse" referendum, an open town/district-meeting vote, and a ballot referendum
> at the polls (simple-majority vs. supermajority). We operationalize the treatment
> several ways — an indicator for any voter-approval requirement, an indicator for a
> required ballot referendum, an ordered hurdle-intensity scale, and the required
> passage share — and report robustness across these encodings. Each rule cell is
> sourced to the controlling constitutional or statutory provision (or an official
> summary) with the text archived for replication. **The coding used in this draft
> is a first-pass transcription; a random sample is being independently
> human-verified against primary law, and inter-coder reliability on a pilot sample
> is 78–88% (with disagreement concentrated on conditional, within-state-varying
> cells). Final estimates will use the human-verified coding.**

Drop the last two sentences once verification is complete and the values in
`rules/verified/` pass the estimation gate (`build/04`).

## 4. What this is not

This extract deliberately bypasses the verification gate for provisional work and
says so on every row (`data_status`). It is right for building your specification,
descriptive figures, and a working draft — not for a final published point estimate
until pass-2 is done.
