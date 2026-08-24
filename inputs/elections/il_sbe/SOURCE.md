# IL SBE — Illinois local referenda

**Source agency:** Illinois State Board of Elections (ISBE).

**Portal:** ISBE Referenda Search —
https://www.elections.il.gov/VotingAndRegistrationSystems/ReferendaSearch.aspx .

**Retrieved:** 2026-08-23 by scraping the public ASP.NET search tool (no auth).

## Why this source
ISBE maintains a statewide database of **every local referendum** placed on an
Illinois ballot — all local government types (counties, municipalities,
townships, school & community-college districts, park/library/fire and other
special districts). It records the ballot question, referendum class, and
certified Pass/Fail. It is the authoritative statewide list of IL local
referenda.

## Files
| file | rows | description |
|---|---|---|
| `il_sbe_referenda_1995_present.csv` | 11,942 | **Deliverable** — one row per referendum, with derived fields. |
| `il_sbe_raw_grid.csv` | 11,942 | Raw scraped grid (6 source columns), before any derivation. |
| `il_ballotpedia_votes_2008_2010.csv` | 84 | **Supplementary vote/amount overlay** (Ballotpedia), NOT a replacement — see below. |
| `raw/ballotpedia_il_tables.txt` | — | captured Ballotpedia table rows (provenance). |

## Supplementary: Ballotpedia vote overlay (2008–2010)
`il_ballotpedia_votes_2008_2010.csv` is a small **Ballotpedia**-sourced file
covering SCHOOL bond & tax measures for four elections only — 2008 Primary,
2008 General, 2009 Consolidated, 2010 Primary (84 measures). It adds the two
things the ISBE scrape lacks: **vote splits** (`pct_yes`, `vote_split` — present
only for the 2010 primary, 20 rows) and **dollar amounts** (51 rows). It is an
**overlay for enrichment/validation of a subset**, not the base: ISBE carries
563 Bond+Tax measures across 2008–2010 alone, vs Ballotpedia's 84 school-only.
Use ISBE as the universe; join Ballotpedia by district + election to fill votes
where they overlap. Columns: `state, source, election, date, district, county,
measure_type, amount, rate_or_cap, outcome, pct_yes, vote_split`.

## How it was downloaded
The tool is an ASP.NET WebForms grid with no export/API — a viewstate
POST→302(PRG)→GridView flow. For each of the four referendum types
(`ddlRefType` = Bond, Tax, Miscellaneous, Advisory) the search was run across
**all** elections (`ddlElections=0`) with the grid page size set to "All"
(32767), and the `gvReferenda` table parsed. Source grid columns: Election,
Jurisdiction (county), Gov Unit Name, Type, Result, Description. (Reproducible
via the harvester in `scratchpad/`.)

Then `scratchpad/il_finalize.py` derived the added columns (below) from those
raw columns — deterministic, no re-fetch.

## Columns
`election_name, election_year, election_month, jurisdiction_county,
gov_unit_name, gov_type, referendum_type, result, amount, amount_verbatim,
description`
- `election_year`: parsed from `election_name`.
- `election_month`: **inferred** from the IL election type (General→11,
  General Primary→03, Consolidated→04, Consolidated Primary→02, Nonpartisan→04);
  blank for specials. IL names the election, not an exact date — there is no
  day-level date in the source.
- `gov_type`: derived from `gov_unit_name`.
- `referendum_type`: `Bond`, `Tax`, `Miscellaneous`, `Advisory` (the source
  class).
- `amount` / `amount_verbatim`: the largest dollar figure parsed from the
  ballot-question `description` (handles "$6 Million", "$4,500,000"); blank when
  the question states no amount.
- `description`: full ballot-question text, verbatim.

## Coverage
- **Rows:** 11,942 referenda (Bond 1,996 · Tax 4,433 · Miscellaneous 3,503 ·
  Advisory 2,010).
- **Date span:** 1995 → 2026 (`election_year`). **Rows on/after 2005:** 7,478.
- **Outcomes:** 7,185 Pass · 4,658 Fail · 93 blank · 6 "Ruling Pending".
- Government types present: school, village, city, township, county, fire,
  park, library, community_college, special_district, other.

## Notes & caveats
- **No vote counts.** ISBE does not canvass local referendum tallies — those
  live with the 100+ county clerks. This feed has certified Pass/Fail but not
  Yes/No totals. (Same class of gap as NC amounts / IN votes.)
- **Amount is text-parsed** from the description and present for ~1,060 rows
  (about half of Bond questions state a figure); treat blank `amount` as "not
  stated on the ballot question," not "zero."
- ~90 rows short of ISBE's full count (~12,036) — a small residue the "all
  elections" query did not return; immaterial for analysis, noted for honesty.
- For the bond subset, filter `referendum_type == "Bond"` (add
  `Miscellaneous` where it contains building/construction questions).
