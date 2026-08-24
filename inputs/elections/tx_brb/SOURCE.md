# TX BRB — Texas local government bond elections

**Source agency:** Texas Bond Review Board (BRB).

**Portal:** Texas Open Data Portal (Socrata), dataset
"Local Debt Bond Election Results" — https://data.texas.gov/ .
Linked from https://www.brb.texas.gov/local-government-services/ .

**Retrieved:** 2026-08-23 via the Socrata public API (no authentication).

## Files
| file | description |
|---|---|
| `tx_brb_bond_elections_all.csv` | Full "Local Debt Bond Election Results" dataset, one row per proposition. |
| `tx_brb_bond_elections_metadata.json` | Socrata view metadata (column defs, description, last-update time). |

## How it was downloaded
The BRB "authorization" application (`data.texas.gov/bond-review-board/
authorization`) is a disclaimer gate that redirects to the underlying tabular
Socrata dataset `kbmc-qmvg`. The public catalog pointer `djkj-euda` is a
non-tabular `href` record pointing at the same app; the real data is `kbmc-qmvg`.

```
GET https://data.texas.gov/resource/kbmc-qmvg.csv?$limit=50000&$order=electiondate
```

Metadata: `https://data.texas.gov/api/views/kbmc-qmvg.json`.

## Coverage
- **Rows:** 10,519 propositions.
- **Date range:** 1951-07-07 → 2026 (ElectionDate).
- **Rows on/after 2005-01-01:** 8,278. (Task asked for 2005–present; full
  history retained as a superset — filter on `electiondate`.)
- Dataset last updated (Socrata `rowsUpdatedAt`): 2026-08-19.

## Columns
`governmentname, governmenttype, county, electiondate, amount, purpose,
purposedescription, propnumber, votesfor, votesagainst, result, source`

Issuer types covered (`governmenttype`): cities, community college districts,
counties, hospital districts, independent school districts, other special
districts, and water districts.

## Notes
- `result` values are the BRB's own (e.g. `Carried` / `Failed`).
- `source` is the BRB's provenance code for the record (e.g. `TBR`).
- `amount` is numeric (bond authorization amount); `votesfor`/`votesagainst`
  are raw vote counts.
