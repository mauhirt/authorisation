# MA DLS — Massachusetts local borrowing authorizations (Prop 2½)

**Source agency:** Massachusetts Department of Revenue, Division of Local
Services (DLS), Data Analytics & Resources Bureau — the "Municipal Databank."

**Portal:** DLS Databank Prop 2½ reports (Logi Analytics), served from
`https://dls-gw.dor.state.ma.us/reports/`. Databank landing:
https://www.mass.gov/collections/DLS-databank-reports .

**Retrieved:** 2026-08-23 via the reports' native-Excel export (no auth).

## Why this is the MA analog to a bond election
Massachusetts municipalities authorize **borrowing** at the ballot via a
**Proposition 2½ debt exclusion** (temporary levy-limit increase to pay debt
service on a specific project) or a **capital outlay exclusion**. These are the
voter-authorization instruments for local capital borrowing — the functional
equivalent of a GO-bond referendum. (Operating **overrides/underrides** are a
different instrument — a permanent operating-levy change, *not* borrowing — and
are deliberately excluded from the combined file below. That report exists at
`Votes.Prop2_5.OverrideUnderride` if ever needed.)

## Files
| file | rows | description |
|---|---|---|
| `ma_prop2_5_borrowing_votes.csv` | 7,022 | **Combined deliverable** — one row per debt-exclusion or capital-exclusion vote. |
| `ma_debt_exclusion_votes.xlsx` | 5,408 | Raw: debt-exclusion votes (result + Yes/No; no dollar amount). |
| `ma_capital_exclusion_votes.xlsx` | 1,614 | Raw: capital-exclusion votes (includes a dollar `Amount`). |
| `ma_debt_exclusion_amounts.xlsx` | 44,225 | Raw: "Debt Exclusion Amount Applied to the Levy Limit" — the **annual** excluded debt-service schedule (many rows per vote, one per fiscal year excluded). Kept for anyone reconstructing levy-limit impact; NOT one row per vote. |

## How it was downloaded
Each Logi report renders all municipalities by default. The native-Excel export
is a session-scoped POST that builds a file and 302-redirects to a one-time
download URL; a sticky AWS load-balancer cookie must be carried across the two
requests. Reproduced by `scratchpad/ma_fetch.sh`:
```
GET  .../rdPage.aspx?rdReport=<REPORT>                      # establish session
POST .../rdPage.aspx?rdReport=<REPORT>&rdReportFormat=NativeExcel
        &rdExportTableID=<TABLE>&rdExcelOutputFormat=Excel2007   # -> 302 Location
GET  <Location>                                             # the .xlsx
```
Reports used: `Votes.Prop2_5.DebtExclusionVotes` (`tblProp2_5Votes`),
`Votes.Prop2_5.Capital` (`tblProp2_5Votes`),
`Votes.Prop2_5.DebtExclusionLevyAmt` (`tblDebtExcLevyAmt`).

## Combined CSV columns
`measure_class` (debt_exclusion | capital_exclusion), `dor_code`, `municipality`,
`fiscal_year`, `vote_date`, `description`, `department`, `amount`, `result`
(Pass=WIN / Fail=LOSS), `votes_yes`, `votes_no`.

## Coverage
- **Rows:** 7,022 votes (5,408 debt exclusions + 1,614 capital exclusions).
- **Date span:** 1982 → 2026 (vote date). **Rows on/after 2005-01-01:** 3,137.
- **Outcomes:** 5,831 pass, 1,191 fail (failed measures ARE included).

## Notes & caveats
- **Government type:** all 351 MA cities & towns (municipal). MA has very few
  independent special districts, so this is effectively all-local-government for
  MA; school capital appears as a `department` = education line inside municipal
  votes, not as a separate district.
- **Amount availability:** capital exclusions carry a clean project `Amount`.
  Debt-exclusion **votes** do NOT carry a principal amount — the only dollar
  figure DLS publishes for them is the *annual* excluded debt service in
  `ma_debt_exclusion_amounts.xlsx` (keyed by DOR code + vote date + description,
  repeated per fiscal year). Treat debt-exclusion `amount` as NULL in the
  combined file; reconstruct levy-limit impact from the amounts xlsx if needed.
- `description` is the project/purpose; `department` is DLS's functional
  category (Public Works, Culture and Recreation, General Government, education…).
- `vote_date` is the ballot date; `fiscal_year` is the FY the exclusion first
  applied.
