# WI DPI — Wisconsin school district referenda

**Source agency:** Wisconsin Department of Public Instruction (DPI),
School Financial Services.

**Portal:** WiSFPR — Wisconsin School Finance Public Reports,
"School District Referenda Report":
https://sfs.dpi.wi.gov/wisfpr/SchoolDistrictReferendaReport?moduleId=11
(landing/description page: https://dpi.wi.gov/sfs/reporting/safr/referenda-info ).

**Retrieved:** 2026-08-23 via the report's public AJAX endpoint (no
authentication).

## Files
| file | description |
|---|---|
| `wi_dpi_referenda_2005_present.csv` | One row per referendum, 2005-01-01 → present, sorted by vote date. |
| `wi_raw_2005plus.json` | Raw JSON response from the report endpoint (provenance). |

## How it was downloaded
The referenda report is a Telerik Kendo grid whose data source reads from an
`aspnetmvc-ajax` endpoint. The DPI application root (`sfs.dpi.wi.gov`) requires
login, but this report path and its `ReadReport` action are public:

```
POST https://sfs.dpi.wi.gov/wisfpr/SchoolDistrictReferendaReport/ReadReport
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest

page=1&pageSize=100000&sort=&group=&filter=
&ReferendaFromDate=2005-01-01&ReferendaToDate=2026-12-31
&ReferendumTypes=ID&ReferendumTypes=RR&ReferendumTypes=R1
&ReferendumTypes=R2&ReferendumTypes=NR
&ReferendumOutcomes=BV&ReferendumOutcomes=PV
&ReferendumOutcomes=FV&ReferendumOutcomes=EC
```

All referendum **types** and **outcomes** were selected to capture everything:
- Types: `ID` Issue Debt, `RR` Recurring (expands to `R1`/`R2`), `NR` Non-Recurring.
- Outcomes: `BV` Before the Vote date, `PV` Passed, `FV` Failed, `EC` Election Cancelled.

## Coverage
- **Rows:** 2,461 referenda.
- **Date range:** 2005-01-01 → 2026 (VoteDate). This matches the requested
  2005–present window; DPI's report defaults its date filter to the current
  year, so the range was set explicitly.
- **Types:** Issue Debt 1,070; Non-Recurring 1,046; Recurring 307; Recurring
  Type 1 28; Recurring Type 2 10.
- **Outcomes:** Passed 1,562; Failed 817; Before the Vote Date 74;
  Election Cancelled 8.

## Columns
`AgencyCode, AgencyName, Cesa, ReferendumId, VoteDate, ReferendumTypeCode,
ReferendumType, Amount, AnnualAmount, BriefDescription, FullDescription,
YesVotes, NoVotes, ReferendumStatusCode, ReferendumStatus`

## Notes
- 11 rows carry test/placeholder agency codes (`9991`, `9994`, `9995`, `9998`,
  `9999`) with a blank `AgencyName` and negligible amounts/vote counts. They are
  DPI internal test records and were left in place (as returned by the source)
  rather than silently dropped — filter them out for analysis
  (`AgencyCode` >= `9990`).
- `AgencyName` in the JSON is populated for all real districts and includes the
  4-digit district code in parentheses.
- `FullDescription` may contain embedded newlines; the CSV is standard RFC-4180
  quoted, so parse with a real CSV reader (not line splitting).
- `AnnualAmount` applies to recurring/non-recurring revenue-limit referenda;
  `Amount` is the authorization amount (total for debt, annual limit otherwise).
