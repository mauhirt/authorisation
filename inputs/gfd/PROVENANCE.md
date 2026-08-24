# GFD pull — provenance

**Source:** Government Finance Database (Pierson, Hand & Thompson 2015, PLoS ONE
10.1371/journal.pone.0130119), Willamette University.
**Page:** https://my.willamette.edu/site/mba/public-datasets (fetched 2026-08-24).
**Files downloaded 2026-08-24** (Google Drive, per-type zips; CSV vintage 2025-10-03,
years 1967–2023; each zip ships the PLoS paper + appendix + 2006 classification
manual + 2017 Individual Unit File disclaimer):

| type | Drive file id | raw CSV | compact rows |
|---|---|---:|---:|
| school district | 1drQFOrso91fcfTfhrUedeGJjq5Gcomjz | 907 MB | 650,062 |
| municipal | 1oiH2jRpupXYtnxDWwys3_Z_aAcHxoHYp | — | 452,685 |
| township | 1HtjG3Iu_2piXG_Bet2Pg1MP3Pb-4ekHz | — | 329,694 |
| special district | 1TCLany_5oy1eOpraxijrrX2VjAcyfId4 | 680 MB | 545,729 |
| county | 1bMD7eHGDrIiipfKMH0unO7kXJee2p-Kl | — | 119,027 |

**Compact panels** (`gfd_<type>_compact.csv.gz`, 36 columns, national, all years;
total 2,097,197 unit-year rows, ~68 MB gzipped) are produced by `extract_compact.py`
and destined for the `who-must-agree` paper repo (too large for the data repo).
Columns kept: GOVSid, year, ids/FIPS bridge, Population, Enrollment, revenue block
(total/own-source/taxes/property tax/IG fed+state), expenditure + capital outlays,
and the full debt block: Total_Debt_Outstanding, LTD out (begin/end, FFC/NG/utility),
**Total_LTD_Issued split FFC vs NG vs unspecified**, LTD_Retired, interest.

**Key identity (verified):** `GOVSid` (9-char: state2+type1+county3+unit3) ==
our `unit_id[:9]` == corpus `pol_accountable_unit_id[:9]`.
