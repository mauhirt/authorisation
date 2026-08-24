# CDIAC — California local bond & tax elections

**Source agency:** California Debt and Investment Advisory Commission (CDIAC),
Office of the California State Treasurer.

**Portal:** DebtWatch — https://debtwatch.treasurer.ca.gov/ (the "Elections"
dataset / `fa-vote-yea` view).

**Retrieved:** 2026-08-23 via the DebtWatch public API (no authentication).

## Files
| file | description |
|---|---|
| `cdiac_elections_all.csv` | Full "Election" dataset, one row per ballot measure. |
| `cdiac_elections_schema.json` | Column definitions / tooltips returned by the API (data dictionary). |

## How it was downloaded
DebtWatch is a React SPA backed by a JSON API at
`https://debtwatch.treasurer.ca.gov/api`. The elections dataset id is
`elections`. The CSV was produced by the same call the site's "export" uses:

```
PUT https://debtwatch.treasurer.ca.gov/api/dataset/elections/search?format=csv
Content-Type: application/json

{"filters":{},"pagination":{"pageNumber":1,"pageSize":100000},
 "searchTerm":"","sorting":{"columnId":"ElectionDate","ascending":false}}
```

(The plain `GET /api/dataset/elections/export/tabular` endpoint returns JSON but
is capped at 1,000 rows; the `search?format=csv` route returns the full set.)

## Coverage
- **Rows:** 7,149 measures.
- **Date range:** 1986-11-04 → 2026-06-02 (Election Date).
- **Rows on/after 2005-01-01:** 5,088. (The task asked for 2005–present; the
  full history is retained here as a superset — filter on `Election Date` for
  the 2005+ window.)

## Columns
`Election Date, Agency Name, County, Election Type, Measure Name,
Type of Tax/Debt, Amount of Bond/Tax, % Yes, % No, Threshold Value,
Election Result, Purpose`

See `cdiac_elections_schema.json` for the per-column descriptions.

## Notes
- Covers all local ballot measures CDIAC tracks (general obligation bonds,
  parcel/sales/special taxes, etc.), not only bonds — filter `Type of Tax/Debt`
  / `Purpose` as needed.
- `Threshold Value` records the approval threshold (e.g. `55%`, `Majority`,
  `2/3`); `Election Result` is `Pass`/`Fail`.
- Amounts are stored as free text (`Amount of Bond/Tax`), often including rate
  language, so parse with care.
