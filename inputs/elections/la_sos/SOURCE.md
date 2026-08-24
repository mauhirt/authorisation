# LA SoS — Louisiana local propositions (bond / tax / millage)

**Source agency:** Louisiana Department of State (Secretary of State),
Elections Division.

**Portal:** the JSON data layer behind the public results portal
`https://voterportal.sos.la.gov/graphical`. Base blob endpoint (no auth):
`https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=`.

**Retrieved:** 2026-08-23 by harvesting the public JSON blobs.

## Why this source
Louisiana votes on every local bond, tax, and millage as a **"Proposition"**
(the SoS `OfficeLevel 999` race class). Each proposition carries the full ballot
text (amount / millage rate / term / purpose / jurisdiction) plus per-parish vote
totals and an explicit `Outcome`. It is Louisiana's functional equivalent of the
CDIAC / TX-BRB local bond-election file, covering **all** local political
subdivisions (parishwide, municipal, school board, and every special district —
levee, drainage, fire, library, law-enforcement, security, etc.).

## Files
| file | description |
|---|---|
| `la_sos_local_propositions_2005_present.csv` | One row per parish-level proposition, 2005→present. |

## How it was downloaded
Reproduced by `scratchpad/la_harvest.py`:
1. `Data?blob=ElectionDates.htm` → all election dates (filtered to ≥ 2005).
2. per date `Data?blob={YYYYMMDD}/ParishesInElection.htm` → participating parishes.
3. per (date, parish) `Data?blob={YYYYMMDD}/RacesCandidates/ByParish_{PP}.htm`
   → propositions (kept where `OfficeLevel == "999"` / `GeneralTitle ==
   "Proposition"`); each carries `SpecificTitle`, `SummaryText`, `FullText`,
   and a `Choice` list (YES = id 3, NO = id 4).
4. per (date, parish) `Data?blob={YYYYMMDD}/VotesParish/Votes_{PP}.htm`
   → votes joined to races by race `ID`; per-choice `VoteTotal` + `Outcome`
   (`Approved` marks the winning choice).

Bulk fallback (not used here): one Excel per election at
`https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/{YYYYMMDD}/Election+Results+({MM-DD-YYYY}).xlsx`.

## Columns
`election_date, parish_code, parish, race_id, specific_title, summary_text,
full_text, votes_yes, votes_no, pct_yes, voters_qualified, voters_voted, result`

## Notes & caveats
- **Amount / millage / term / purpose / sub-type are embedded in
  `specific_title` and `full_text`**, not discrete columns — parse them
  downstream. `specific_title` also carries the SoS entity-type suffix
  (e.g. `SB` school board, `PJ` police jury, `CC` city council).
- **No approval-threshold field.** Most LA local propositions are simple
  majority; thresholds are not published in this feed.
- `result` = `Pass` if the YES choice is `Approved`, else `Fail`.
- `parish` is resolved from the SoS alphabetical parish code (01 Acadia … 64
  Winn); the code is authoritative, the name is a local lookup.
- A proposition voted across multiple parishes (rare for locals) appears once
  per parish; multi-parish statewide items (`OfficeLevel 998`, constitutional
  amendments) are intentionally excluded.
- Covers all local propositions — bond, tax, millage, sales-tax, and
  non-fiscal — filter `full_text` / `specific_title` for the bond subset.
