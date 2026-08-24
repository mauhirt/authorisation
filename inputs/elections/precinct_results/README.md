# Precinct-level referendum results (NC, LA)

Sub-jurisdiction (precinct) vote results for local referenda, for the states
whose sources expose precinct data. This is the **finer grain** for within-
jurisdiction analysis (turnout, precinct margins, RD/geographic designs) and is
**additive** to the jurisdiction-level crosswalk — it does not replace it.

## How it fits
```
precinct_results/<state>.csv   (precinct grain: votes per precinct)
        │  join on the referendum identity ↓
referendum_unit_crosswalk.csv  (jurisdiction grain) ── unit_id ──▶ issuance
```
Join keys:
- **NC** — `election_date + contest_name` (matches `nc_ncsbe/…` and the crosswalk).
- **LA** — `election_date + parish_code + race_id` (matches
  `la_sos/…` and the crosswalk).

## Files
| file | rows | grain | join key |
|---|---:|---|---|
| `nc_precinct_results.csv` | 19,799 | contest × county × precinct | `election_date, contest_name` |
| `la_precinct_results.csv` | 247,320 | proposition × parish × precinct | `election_date, parish_code, race_id` |

LA precinct covers all 6,895 propositions (all types, not only bonds — filter via
`la_sos`/crosswalk on the join key); NC covers all 278 bond contests.

## Sources & method
- **NC** — NCSBE `results_pct_{YYYYMMDD}.zip` (the same precinct files behind the
  contest-level `nc_ncsbe` dataset), re-parsed at precinct grain for BOND
  contests. Columns: `state, election_date, county, precinct, contest_name,
  votes_for, votes_against, total, pct_for`. Reproducible: `scratchpad/nc_precinct.py`.
- **LA** — LA SoS blob `{YYYYMMDD}/VotesRaceByPrecinct/Votes_{raceID}_{PP}.htm`
  (YES=choice 3, NO=4), driven by the `race_id`+`parish_code`+date of every
  proposition in the `la_sos` dataset. Columns: `state, election_date,
  parish_code, parish, precinct, race_id, votes_yes, votes_no, total, pct_yes,
  voters_qualified, voters_voted`. Reproducible: `scratchpad/la_precinct.py`.

## Notes
- Precinct results carry **votes only** — the referendum's amount/purpose/type
  and its `unit_id` come from the jurisdiction-level files via the join keys.
- Other states' referenda sources (CA CDIAC, TX BRB, WI DPI, MA DLS, IN DLGF,
  IL ISBE) are measure-level; their precinct results live at county/SoS election
  offices and would be a separate, per-state pull. **MN** precinct files
  (`*ByPct.txt`) exist at the (bot-walled) SoS and can be added via a browser-
  class capture.
