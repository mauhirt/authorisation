# PASS2_WORKLIST — the 21 open rule cells, with archived primary sources

*Adjudication file for the owner's pass-2 on the strict-rule coding. Every cell is
(state × municipality × go_debt), the latest-year row of the rules panel. Machine
coding source: `inputs/elections/rules/state_debt_rules.csv` (status
`PRELIMINARY_pass1_AI_unverified`). Independent hand coding:
`inputs/external_municipal_analysis/state_bond_referenda_requirements.csv`
(Ballotpedia-sourced, "is voter approval required"), compared in
`analysis/RULES_CROSSVAL_RESULTS.md`. Verdicts go into
`analysis/rules_pass2_worklist.csv`; the rulings template is at the end of this file.*

*Archived sources are in `raw/sources/pass2/` — retrieved verbatim from the URLs in
`raw/sources/pass2/MANIFEST.csv` (date, HTTP status, sha256 per file), rendered to PDF
where the source is HTML. Retrieval only: nothing was summarised or classified.
The candidate citations below are pass-1 starting pointers — confirming them against
the archived text is the pass-2 job. Three cells (MS, TN, IN) carry second-best
provenance because the official code portals block automated retrieval; the manifest
notes say so per file.*

**Definitional key.** Our `op_referendum_strict = 1` means a pre-issuance ballot
referendum at the polls is the mandatory default path. Town-meeting votes,
petition-triggered ("reverse") referenda, and conditional votes (above a threshold, by
purpose, by charter) are strict=0. Their coding answers the looser "is voter approval
required". A *definitional* disagreement is one where both codings describe the same
mechanism and differ only through that gap; a *factual* disagreement is one where the
mechanism itself is contested.

---

## Part 1 · Definitional disagreements (likely quick: confirm mechanism, record citation)

### 1. MS × municipality × go_debt
- Machine: strict=0, mechanism `petition-triggered` (state_debt_rules.csv, PRELIMINARY pass-1).
- Hand coding: required=True (state_bond_referenda_requirements.csv). Disagreement type: **definitional** (petition-trigger counted as "required" by the looser question).
- Adjudicate: intent resolution + publication; referendum only on protest petition (ten percent or 1,500 electors); otherwise issue without election.
- Candidate citations: Miss. Code Ann. § 21-33-307 (Art. 5, not Art. 7 as the pass-1 pointer had it); §§ 21-33-301 to -315.
- Archived: `raw/sources/pass2/MS_21-33-307_HB711-2023-reprint.pdf` (section text as set out in MS HB 711 (2023); official portal is LexisNexis-only — verify against enacted text when ruling).

### 2. TN × municipality × go_debt
- Machine: strict=0, mechanism `petition-triggered` (PRELIMINARY pass-1).
- Hand coding: required=True. Type: **definitional**.
- Adjudicate: publication of the bond resolution; election only on protest petition (ten percent of registered voters); otherwise issue.
- Candidate citations: Tenn. Code Ann. §§ 9-21-205 to -207 (Local Government Public Obligations Act).
- Archived: `TN_9-21-205_lawserver.pdf`, `TN_9-21-206_lawserver.pdf`, `TN_9-21-207_lawserver.pdf` (mirror; official portal LexisNexis-only).

### 3. WI × municipality × go_debt
- Machine: strict=0, mechanism `petition-triggered` with purpose exceptions (`ref_variation_type = project_purpose`).
- Hand coding: required=True. Type: **definitional** (WI schools are separately strict — different cell, not this one).
- Adjudicate: bond resolutions subject to referendum on petition, with mandatory-referendum carve-outs by purpose in § 67.05(5)–(7).
- Candidate citations: Wis. Stat. § 67.05(5)–(7).
- Archived: `WI_stat_ch67.pdf` (official chapter PDF).

### 4. MA × municipality × go_debt
- Machine: strict=0, mechanism `town_meeting`, threshold 66.7.
- Hand coding: required=True. Type: **definitional** (town-meeting vote counted as voter approval; a Prop 2½ debt-exclusion ballot is a *tax* question, not bond authorisation).
- Adjudicate: two-thirds vote of town meeting / city council authorises debt.
- Candidate citations: M.G.L. c. 44, §§ 7–8; c. 59, § 21C (Prop 2½).
- Archived: `MA_MGL_c44_s7.pdf`, `MA_MGL_c44_s8.pdf`, `MA_MGL_c59_s21C.pdf` (official).

### 5. ME × municipality × go_debt
- Machine: strict=0, mechanism `town_meeting`, threshold 50.
- Hand coding: required=True. Type: **definitional**.
- Adjudicate: town-meeting majority as the default municipal borrowing path.
- Candidate citations: 30-A M.R.S. § 5772.
- Archived: `ME_30A_5772.pdf` (official).

### 6. NH × municipality × go_debt
- Machine: strict=0, mechanism `town_meeting`, threshold 60.
- Hand coding: required=True. Type: **definitional**.
- Adjudicate: three-fifths (or two-thirds traditional) vote of the town/district meeting, ballot at SB2 meetings.
- Candidate citations: N.H. RSA 33:8, 33:8-a.
- Archived: `NH_RSA_33-8.pdf`, `NH_RSA_33-8-a.pdf` (official).

## Part 2 · Factual disagreements (genuine disputes; corpus behaviour corroborates strict=0)

### 7. KY × municipality × go_debt
- Machine: strict=0, mechanism `none`.
- Hand coding: required=True. Type: **factual** — does municipal GO need any voter approval by default?
- Adjudicate: Ky. Const. §§ 157–158 require voter assent (two-thirds) only for debt beyond annual-revenue/indebtedness limits; is the default path ordinance-only? Corpus check: KY municipal voted-dollar share is 0.1% (v3), consistent with strict=0.
- Candidate citations: Ky. Const. §§ 157, 158; KRS ch. 66.
- Archived: `KY_Const_s157.pdf`, `KY_Const_s158.pdf`, `KY_KRS_ch66_index.pdf` (official).

### 8. VA × municipality × go_debt
- Machine: strict=0, mechanism `none` (`ref_variation_type = entity_class`).
- Hand coding: required=True. Type: **factual** — their True likely conflates counties with cities/towns.
- Adjudicate: Va. Const. art. VII § 10 imposes the referendum requirement on counties and exempts cities and towns (subject to debt limits). Corpus check: VA municipal voted share 2.1% vs county 33.2% (v3).
- Candidate citations: Va. Const. art. VII § 10(a)–(b).
- Archived: `VA_Const_artVII_s10.pdf` (official).

## Part 3 · Structural not-codables (pick a defensible coding; suggested resolutions from `RULES_PASS2_WORKLIST.md`)

### 9. IL × municipality × go_debt — variation `home_rule`
- Machine: not codable (op_codable=0). Hand coding: required=True. Type: **structural** (sub-branch exists: non-home-rule municipalities need a referendum; home-rule are exempt).
- Suggested: strict=1 non-home-rule / 0 home-rule (unit-level home-rule flag available).
- Candidate citations: 65 ILCS 5/8-4-1; Ill. Const. art. VII § 6 (home rule).
- Archived: `IL_65ILCS5_art8_div4.pdf` (official; whole Division 4, Issuance of Bonds).

### 10. MN × municipality × go_debt — variation `bond_type`
- Machine: not codable. Hand coding: required=True. Type: **structural** (majority election required unless a listed exception; the question is whether the exceptions swallow the default).
- Candidate citations: Minn. Stat. § 475.58.
- Archived: `MN_475-58.pdf` (official).

### 11. IA × municipality × go_debt — variation `project_purpose`
- Machine: not codable. Hand coding: required=True. Type: **structural** (essential corporate purpose = no vote; general corporate purpose = 60% election).
- Candidate citations: Iowa Code §§ 384.24–384.26.
- Archived: `IA_384-24.pdf`, `IA_384-25.pdf`, `IA_384-26.pdf` (official PDFs).

### 12. IN × municipality × go_debt — variation `project_cost_threshold`
- Machine: not codable. Hand coding: required=True. Type: **structural** (petition-and-remonstrance / referendum above cost thresholds, post-2008 regime).
- Candidate citations: IC 6-1.1-20 (esp. 6-1.1-20-3.5, -3.6).
- Archived: `IN_6-1.1-20_lawserver.pdf`, `IN_6-1.1-20-3.5_lawserver.pdf` (mirror; iga.in.gov blocks automated retrieval).

### 13. NV × municipality × go_debt — variation `issuer_option`
- Machine: not codable. Hand coding: required=True. Type: **structural** (voted GO or debt-management-commission approval without a vote — issuer's option).
- Suggested: issuer option → strict=0.
- Candidate citations: NRS ch. 350 (esp. 350.020).
- Archived: `NV_NRS_ch350.pdf` (official; whole chapter).

### 14. PA × municipality × go_debt — variation `debt_limit_threshold`
- Machine: not codable. Hand coding: required=True. Type: **structural** (nonelectoral debt to a limit; electoral debt by referendum beyond).
- Candidate citations: 53 Pa.C.S. ch. 80 (LGUDA), esp. §§ 8022, 8041.
- Archived: `PA_53PaCS_ch80.pdf` (official; whole chapter).

### 15. NY × municipality × go_debt — variation `local_law_optin`
- Machine: not codable. Hand coding: required=True. Type: **structural** (towns/villages: permissive referendum on petition; cities: none).
- Suggested: sub-branch by municipal class; default 0.
- Candidate citations: N.Y. Local Fin. Law §§ 33.00–37.00.
- Archived: `NY_LFN_33.00.pdf`, `NY_LFN_35.00.pdf`, `NY_LFN_36.00.pdf`, `NY_LFN_37.00.pdf` (public.law edition of the official text).

### 16. KS × municipality × go_debt — variation `project_purpose`
- Machine: not codable. Hand coding: required=True. Type: **structural** (purpose-dependent election/protest provisions).
- Candidate citations: K.S.A. ch. 10 (general bond law), art. 1.
- Archived: `KS_ch10_index.pdf`, `KS_10-101.pdf` (official).

### 17. CT × municipality × go_debt — variation `charter`
- Machine: not codable. Hand coding: required=False (their only False among the 13). Type: **structural** (each municipality's charter decides; no state mandate).
- Suggested: default strict=0, keep charter flag.
- Candidate citations: C.G.S. ch. 109 (§ 7-369 ff.); ch. 98 (municipal powers).
- Archived: `CT_CGS_ch109.pdf` (official; whole chapter).

### 18. RI × municipality × go_debt — variation `charter`
- Machine: not codable. Hand coding: required=True. Type: **structural** (charter/enabling-act dependent).
- Candidate citations: R.I. Gen. Laws ch. 45-12 (esp. § 45-12-2).
- Archived: `RI_45-12_index.pdf`, `RI_45-12-2.pdf` (official).

### 19. MD × municipality × go_debt — variation `charter`
- Machine: not codable. Hand coding: required=True. Type: **structural** (charter counties/municipalities differ).
- Candidate citations: Md. Code, Local Gov't § 19-301 et seq.
- Archived: `MD_LocalGovt_19-301.pdf` (official).

### 20. DE × municipality × go_debt — variation `charter`
- Machine: not codable. Hand coding: required=True. Type: **structural** (charter-by-charter).
- Candidate citations: 22 Del. C. (municipalities), ch. 8.
- Archived: `DE_title22_index.pdf`, `DE_title22_c008.pdf` (official).

### 21. HI × municipality × go_debt — variation `entity_class`
- Machine: not codable. Hand coding: required=False. Type: **structural** (no general municipal layer below counties; county GO by ordinance).
- Suggested: structural-NA confirmed, or fold to the county cell.
- Candidate citations: Haw. Const. art. VII; HRS ch. 47 (county bonds).
- Archived: `HI_Const_full.pdf`, `HI_HRS_ch47_index.pdf` (official).

## Part 4 · The township / town-meeting column (structurally hardest — do last)

Not a single cell but a new `entity_type = township` column for the town-meeting states
(CT, MA, ME, NH, RI, VT) and the township states (MI, MN, NY, WI, PA as applicable),
per Part C of `analysis/RULES_PASS2_WORKLIST.md`. Townships currently ride the
municipality proxy, which flips the national first-stage sign for them (46.5% voted
under nominal "non-strict"). Code the meeting mechanism explicitly
(`ref_required = town_meeting`, threshold where set).
- Carry-over sources: MA/ME/NH texts from Part 1 (cells 4–6); CT from cell 17.
- Additional archived: `VT_24VSA_1755.pdf` (24 V.S.A. § 1755, Vermont town bond vote);
  `CT_CGS_ch98_7-194.pdf` (C.G.S. ch. 98, municipal powers).
- MI/MN/NY/WI/PA township statutes are NOT yet archived — scope which apply before
  fetching (most of their local GO flows through school/county/special classes in the
  panel).

---

## Rulings template

Copy one line per cell (and one per township-column state) — or fill the same fields
directly in `analysis/rules_pass2_worklist.csv` (`pass2_*` columns).

| cell ID | ruling | citation | operative language (verbatim, one sentence) | date | notes |
|---|---|---|---|---|---|
| MS×municipality×go_debt | | | | | |
| TN×municipality×go_debt | | | | | |
| WI×municipality×go_debt | | | | | |
| MA×municipality×go_debt | | | | | |
| ME×municipality×go_debt | | | | | |
| NH×municipality×go_debt | | | | | |
| KY×municipality×go_debt | | | | | |
| VA×municipality×go_debt | | | | | |
| IL×municipality×go_debt | | | | | |
| MN×municipality×go_debt | | | | | |
| IA×municipality×go_debt | | | | | |
| IN×municipality×go_debt | | | | | |
| NV×municipality×go_debt | | | | | |
| PA×municipality×go_debt | | | | | |
| NY×municipality×go_debt | | | | | |
| KS×municipality×go_debt | | | | | |
| CT×municipality×go_debt | | | | | |
| RI×municipality×go_debt | | | | | |
| MD×municipality×go_debt | | | | | |
| DE×municipality×go_debt | | | | | |
| HI×municipality×go_debt | | | | | |
| township column (per state) | | | | | |

*Ruling values: `strict=1` / `strict=0` / `conditional(sub-branch)` / `structural-NA`.
On completion set `pass2_verified=1` in the CSV, re-run `analysis/rules_crossval.py`,
then the C2 finals and the N-suite causal upgrade per
`analysis/RULES_PASS2_WORKLIST.md`.*
