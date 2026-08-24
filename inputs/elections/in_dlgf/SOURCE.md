# IN DLGF — Indiana local referenda (school & civil units)

**Source agency:** Indiana Department of Local Government Finance (DLGF),
"Referendum Information" hub: https://www.in.gov/dlgf/referendum-information/ .

**Captured:** 2026-08-23 (plain HTTP, no bot wall).

## Why this source
Under Indiana's 2008 referendum law, local governments hold a voter referendum
to issue debt / undertake a "controlled project" above statutory thresholds, and
to exceed operating levy limits. DLGF administers and certifies these and
publishes the certified outcome for every one — schools **and** civil units.

## Files
| file | rows | description |
|---|---:|---|
| `in_dlgf_referenda_2009_present.csv` | 290 | one row per referendum (deliverable) |
| `raw/*_fulltext.txt`, `raw/*.txt` | — | verbatim DLGF page text per section (provenance) |

This dataset supersedes the earlier 253-row scrape on this branch: it is the
same DLGF source captured more completely (290 rows incl. "not on ballot" /
pending), and adds `amount_or_rate` and the verbatim `result_raw`.

## Columns
`state, election, election_year, election_month, referendum_type, gov_unit_name,
county, gov_type, amount_or_rate, result_raw, result`
- `referendum_type` (DLGF "page"): `Controlled Project` (capital/debt — the
  bond-relevant class), `School Operating/Capital Levy`, `School Safety`,
  `Bond Refunding`.
- `gov_type`: derived from `gov_unit_name` (school / library / park / township /
  town / city / county / transit / hospital / other).
- `amount_or_rate`: verbatim where the page lists it (31 rows, mostly 2009–2011
  levy rates e.g. `$0.1900 on each $100 of assessed value`; one dollar figure).
- `result_raw`: verbatim DLGF wording; `result`: normalized
  (Passed / Failed / Not on ballot / blank=pending-uncertified).

## Coverage
- **290 referenda:** Controlled Project 92, School Operating/Capital Levy 192,
  School Safety 4, Bond Refunding 2.
- **Years 2009–2025.** Indiana's referendum regime began 2009 — there is no
  2005–2008 data (petition/remonstrance only before the 2008 law).
- Outcomes: 187 Passed, 97 Failed, 3 Not on ballot, 3 blank (pending).

## Known limitation (amounts & vote counts)
DLGF's HTML lists jurisdiction / county / date / type / pass-fail only. For
**2012+** entries the millage/dollar amount and the actual YES/NO **vote counts**
are not on the web pages — they live inside each entry's linked "Findings and
Final Determination" PDF (~250+ PDFs). Extracting those is a separate, larger job
(download + PDF parse), not done here. `amount_or_rate` is therefore populated
only for the older (2009–2011) rows that list the rate inline. For the bond
subset, filter `referendum_type == "Controlled Project"` (+ `Bond Refunding`).
