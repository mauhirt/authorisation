# MN SoS — Minnesota local ballot questions (with vote counts)

**Source agency:** Minnesota Secretary of State — downloadable election-results
files (`https://electionresultsfiles.sos.mn.gov/{YYYYMMDD}/{School,City}Questions.txt`).

**Captured:** 2026-08-23. The `sos.mn.gov` hosts are Radware bot-walled to plain
curl; captured via a browser-class fetch (see the wider note in
`../STATE_AVAILABILITY.md`).

## Why MN stands out
Unlike the other states here, MN publishes machine-readable results with **actual
YES/NO vote counts** for every local ballot question, and a **stable id**
(`district_or_muni_id`: ISD/SSD/CSD number for schools, MN municipality code for
cities/townships). The ISD number is a true key into the Census school universe.

## Files
| file | rows | description |
|---|---:|---|
| `mn_sos_ballot_questions_2020_2025.csv` | 690 | one row per local ballot question |
| `raw/{school,city}_YYYYMMDD.txt` | — | verbatim merged rows per election (provenance) |

## Columns
`state, election_date, scope, question_id, question_name, district_or_muni_id,
yes_votes, no_votes, total_votes, pct_yes, outcome`
- `scope`: `School (referendum/bond)` (461), `City` (155), `Township` (74).
- `district_or_muni_id`: **key** — ISD/SSD/CSD number (schools) or MN municipality
  code (city/township); populated for all 690 rows.
- `question_name`: carries the ISD number (schools) or place name (city/township)
  in parentheses.

## Coverage
- **690 questions**, six November general/municipal elections **2020–2025**
  (2020=98, 2021=89, 2022=148, 2023=107, 2024=148, 2025=100).
- Outcomes: 434 Passed, 256 Failed. Per-row arithmetic validated
  (yes+no==total, 0 failures); school totals independently checksum-verified.

## Notes & caveats
- **Vote counts present** (the key differentiator); **dollar amount / millage is
  NOT** — that lives in each question's ballot text on the SoS question pages.
- School = the core bond/levy data; City/Township include bonds/levies/local sales
  taxes **and** some non-fiscal items (charter, ranked-choice) — filter
  `question_name` for fiscal-only.
- **Available on request via the same method** (not pulled here): older elections
  (2012–2019), **County questions**, and **precinct-level breakdowns**
  (`local.txt`, `*ByPct.txt`) — the finer grain for within-jurisdiction analysis.
- Crosswalk: schools resolve via the **ISD-number key** (deterministic), cities/
  townships via scope-typed name match. See `../crosswalk/SOURCE.md`.
