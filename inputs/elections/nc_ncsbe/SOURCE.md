# NC NCSBE — North Carolina local bond referenda (election results)

**Source agency:** North Carolina State Board of Elections (NCSBE).

**Portal:** NCSBE public data store (Amazon S3), Election Night Reporting System
archive: `https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/`. Landing page:
https://www.ncsbe.gov/results-data/election-results/historical-election-results-data .

**Retrieved:** 2026-08-23 from the S3 precinct-results files (no auth).

## Why this source (and its limit)
NCSBE precinct results carry every ballot contest, including local **bond
referenda** for all government types (counties, cities/towns, community
colleges, county school units, special-purpose bonds). It gives votes and
pass/fail across the whole state. It does **not** carry the bond **dollar
amount** — that lives at the NC Dept. of State Treasurer / Local Government
Commission and is a separate enrichment (see Notes).

## Files
| file | description |
|---|---|
| `nc_ncsbe_bond_referenda_2005_present.csv` | One row per bond contest, aggregated from precinct results, **with home county**. |

Reproduced by `scratchpad/nc_harvest_v2.py` (supersedes the county-less
`nc_harvest.py`).

## How it was downloaded
Reproduced by `scratchpad/nc_harvest.py`:
1. List election-date folders: `GET {S3}?list-type=2&prefix=ENRS/&delimiter=/`
   (filtered to dates ≥ 2005).
2. For each date, download `ENRS/{YYYY_MM_DD}/results_pct_{YYYYMMDD}.zip`,
   unzip the precinct results, keep rows whose contest name contains `BOND`,
   and **aggregate `Total Votes` by contest × choice** (FOR/YES vs AGAINST/NO)
   across all precincts and counties.
3. `result = Pass` when FOR > AGAINST. Files are streamed and deleted per date
   to conserve disk.

The parser handles both layouts in the archive: the modern tab-delimited file
(`Contest Name`, `Choice`, `Total Votes`) and the 2008-era comma file
(`contest`, `choice`, `total votes`).

## Columns
`election_date, contest_name, county, counties, votes_for, votes_against,
pct_for, result`
- `county` = vote-weighted **dominant county** the contest appeared in (the
  precinct files carry a per-row County); `counties` = full `;`-separated list
  for multi-county cities. Retaining the county lets the crosswalk fold NC
  school/community-college bonds to the county and county-block city matches —
  it lifted the NC crosswalk from 61% to **100%** assigned.

## Coverage
- **Rows:** 278 bond contests.
- **Date span:** 2008-11-04 → 2026-03-03. **Outcomes:** 254 pass, 24 fail.
- Includes general, primary, and odd-year municipal elections where NCSBE posted
  precinct results.

## Notes & caveats
- **No dollar amount / purpose column.** The jurisdiction and purpose are inside
  `contest_name` (e.g. "CITY OF CHARLOTTE STREET BONDS", "WAKE COUNTY PUBLIC
  LIBRARIES BONDS REFERENDUM") — parse downstream. Dollar amounts require a join
  to the NC Dept. of State Treasurer / Local Government Commission (Bond Link
  Excel, Bond Reporter PDFs 2018–2020, LGC minutes 2020+; SLGFD@nctreasurer.gov
  for bulk).
- **Coverage floor is 2008.** Pre-2008 precinct files in this feed do not carry
  local bond referenda: the 2006 `results_pct` files use an older schema
  (`contest_name` / `name_on_ballot` / `ballot_count`) and contain **no** BOND
  contests, and there is no 2005 folder. So 2005–2007 is empty from this source,
  not dropped.
- **Genuine source gaps.** Several odd-year municipal elections (e.g.
  2009-09/10/11, 2013-11-05, 2015-05-12) return "Data Unavailable" in the ENRS
  archive and some 2009 dates have no precinct zip — any bond measures on those
  ballots are not recoverable from this feed.
- Contest totals are summed across every precinct and county that voted the
  measure, so a city spanning counties is counted once, correctly.
