# Rules pass-2 — the 21-cell worklist (municipal GO debt)

*Companion fillable file: `analysis/rules_pass2_worklist.csv` (enter verdicts
there; this document is the adjudication guide). Cells = the 8 disagreements
with the independent green-bond-paper coding plus the 13 not-codable states,
from `RULES_CROSSVAL_RESULTS.md`. All cells are (state, municipality, go_debt,
latest year). A 22nd task, the township rule column, is at the end.*

## The definition being verified

`op_referendum_strict = 1` means: **a pre-issuance ballot referendum at the
polls is the mandatory default path** for municipal GO debt. It is 0 when the
default path is a governing-body decision, an open town/district meeting, a
petition-triggered ("reverse") referendum, or when a vote is required only
conditionally (above a debt limit, for certain purposes, by charter opt-in).
The other coding (`state_bond_referenda_requirements.csv`, Ballotpedia-sourced)
asks the looser question "is voter approval required", which counts town
meetings and petition triggers. **Most disagreements are that definitional
gap, not factual error; the pass-2 job is to confirm the mechanism and record
the citation.**

## Part A · The 8 disagreements (theirs: required=True; ours: strict=0)

For six of the eight, our panel already codes a specific non-ballot mechanism;
the verdict needed is "mechanism confirmed (strict=0 stands)" or "mechanism
wrong (recode)". For KY and VA the disagreement is factual.

| state | our mechanism | the adjudication question | starting pointer (verify against current law) |
|---|---|---|---|
| **KY** | none | GENUINE dispute: does municipal GO need any voter approval? Ky. Const. §157–158 require voter assent (2/3) only for debt beyond annual revenue limits — is the default path ordinance-only? | Ky. Const. §§157, 158; KRS ch. 66 |
| **VA** | none | GENUINE dispute: Va. Const. art. VII §10 exempts cities and towns from the referendum requirement it imposes on counties — confirm the municipal default is council-only. Their True likely conflates counties. | Va. Const. art. VII §10(a)–(b) |
| MA | town_meeting (thr 66.7) | Confirm: two-thirds vote of town meeting / city council authorises debt (a Prop 2½ debt-exclusion BALLOT is a tax question, not bond authorisation). | M.G.L. c.44 §§7–8; Prop 2½ (c.59 §21C) |
| ME | town_meeting (thr 50) | Confirm town-meeting majority as the default municipal path. | 30-A M.R.S. §5772 |
| NH | town_meeting (thr 60) | Confirm 3/5 of the (SB2 or traditional) meeting ballot. | RSA 33:8, 33:8-a |
| MS | petition-triggered | Confirm: intent notice, referendum only on protest petition (10% / 1,500 electors), else issue. | Miss. Code §21-33-307 |
| TN | petition-triggered | Confirm the protest-petition mechanism for municipal GO. | Tenn. Code Ann. §9-21-205 et seq. |
| WI | petition-triggered (purpose exceptions) | Confirm: municipal bond resolutions are subject to referendum on petition, with mandatory-referendum carve-outs by purpose. (WI SCHOOLS are separately strict; not this cell.) | Wis. Stat. §67.05(5)–(7) |

## Part B · The 13 not-codable cells (structural variation — pick a defensible coding)

For each: either (i) confirm structural-NA (leave out of the clean sample), or
(ii) adopt the suggested sub-branch coding so the cell enters analysis. The
`ref_variation_type` in the panel names the structure.

| state | variation | the structure to adjudicate | suggested resolution to verify |
|---|---|---|---|
| CT | charter | each municipality's charter decides | default strict=0 (no state mandate); keep charter flag |
| RI | charter | charter/enabling-act dependent | as CT |
| MD | charter | charter counties/municipalities differ | as CT |
| DE | charter | charter-by-charter | as CT |
| IL | home_rule | non-home-rule munis need a referendum (65 ILCS 5/8-4-1); home-rule exempt | SUB-BRANCH: strict=1 non-home-rule, 0 home-rule (unit-level home-rule flag exists via Census pop cutoff + election) |
| IN | project_cost_threshold | petition-and-remonstrance / referendum above cost thresholds (IC 6-1.1-20, post-2008 regime) | conditional: strict=1 for projects above threshold; else 0 |
| IA | project_purpose | essential corporate purpose (no vote) vs general corporate purpose (60% vote), Iowa Code §§384.24–.26 | conditional by purpose; default path non-strict |
| KS | project_purpose | purpose-dependent election/protest provisions | verify K.S.A. ch. 10; likely conditional |
| MN | bond_type | Minn. Stat. §475.58: majority election required UNLESS a listed exception (many) | strict=1 nominal with wide exceptions; verify whether exceptions swallow the default |
| NV | issuer_option | NRS ch. 350: voted GO or debt-management-commission approval without a vote | issuer option → strict=0 |
| NY | local_law_optin | Local Finance Law: towns/villages permissive referendum on petition; cities none | sub-branch by municipal class; default 0 |
| PA | debt_limit_threshold | LGUDA (53 Pa.C.S.): nonelectoral debt to a limit; electoral (referendum) debt beyond | conditional on the limit; default 0 |
| HI | entity_class | no general municipal layer below counties; county GO by ordinance | structural-NA confirmed, or fold to county cell |

## Part C · The township column (new, from the v3 first stage)

The panel has no township class; townships ride the municipality proxy, and
the national first stage flips sign for them (46.5% voted under "non-strict"),
because New England towns borrow by TOWN-MEETING VOTE in states coded
non-strict for cities. Task: add `entity_type = township` rows for the
town-meeting states (CT, MA, ME, NH, RI, VT + township states MI/MN/NY/WI/PA
as applicable), coding the meeting mechanism explicitly (`ref_required =
town_meeting`, threshold where set). Part A's MA/ME/NH citations carry over.

## What each verdict changes downstream
- Part A confirmations mostly LOCK the current coding (strict=0) and convert
  the cross-validation "disagreements" into documented definitional
  differences; KY/VA could flip a cell each.
- Part B resolutions move up to 13 states into the codable sample for N1–N5
  and C2 (the held H2 finals) — the largest single power gain available.
- Part C removes the one first-stage sign anomaly.
- On completion: set `verified=1` on adjudicated rows, re-run
  `rules_crossval.py`, then C2 finals + N-suite causal upgrade.

## How to fill
Enter in `rules_pass2_worklist.csv`: `pass2_strict` (0/1/NA),
`pass2_threshold_num` (if a ballot threshold exists), `pass2_mechanism`
(none / ballot_referendum / town_meeting / petition_trigger / conditional /
charter), `pass2_citation` (constitution/statute section), `pass2_notes`,
`pass2_verified=1`. The pointers above are STARTING POINTS from general legal
knowledge, not verified citations — checking them against current law is the
point of the exercise.
