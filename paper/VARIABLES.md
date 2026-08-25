# Variable inventory by section (draft §§4–9)

*Reference document, 2026-08-24, computed on the current panels (corpus package
v3). "Panel" = the 40,924 crosswalked referenda; "RD frame" = rd_sample ∩
bond_go, 11,889 measures. Coverage figures are non-blank counts from the
committed files, not estimates. Conditional variables state their own
denominator. British spelling; no em dashes.*

---

## §4 · Data (identity, treatment definition, validation)

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `unit_id` / GID | 9-char Census government ID (state2+type1+county3+unit3) | unit | crosswalk | 40,924/47,235 referenda (86.6%) | exact tiers ~100% verified; fuzzy tier 95.1% RA-audited |
| `pct_yes` | yes share of the vote | referendum | 9 state registries | 75% of panel; **100% of RD frame** | IL/IN carry results only (no margin) |
| `threshold_centered_margin` | pct_yes − applicable threshold | referendum | derived; CA threshold per measure from CDIAC | 75% / **100%** | the running variable |
| `rd_sample` | at a genuine mandatory-ballot statutory cutoff | referendum | rules coding of the 9 states (direct, not the national panel) | 23,577 flagged | RD-state cutoffs are bedrock statutes, outside the pass-2 worklist |
| `purpose_class` | bond_go / bond_other / tax etc. | referendum | per-state purpose mapping | 100% | MN school classification gap flagged |
| `auth_mode_final2` | OS-evidenced authorisation mode (voter / council_or_board / statutory) | document | corpus extraction | 93.7% of docs determined (v3) | validated: date match 67.9% pooled, 95.4% WI; matched→passed 91.3% |
| `op_referendum_strict` (+ ordinal, threshold_num) | coded rule, state × entity × purpose × year | state×entity×year | rules panel | 89% of panel rows; muni cell codable in 37 states | **PRELIMINARY pass-1; 21-cell pass-2 with owner** |

## §5 · Landscape and fifty-state first stage

**Grain: one row per local government (entity panel, 90,604 units) or per
document (corpus).**

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `nm_docs`, `nm_par` | new-money issues and par, 2005–25, canonical per issue | unit | corpus v3 | 78,672 typed nm issues; 46 states ≥50 docs | 5 small states below gate (DC/DE/HI/VT/WY); 5 legacy states 72–87% flag coverage (MN/MA/MO/MD/ID) |
| `sec_go_sh` … `sec_sptax_sh` | par shares by security pledge class | unit | corpus | where nm_par>0 | GO / revenue / lease / special_tax |
| `voted_sh_par`, `council_sh_par`, `statutory_sh_par` | mode shares of determined nm $ | unit | corpus | 13,875 units with a determined split | the first-stage outcome |
| `nc_share_project` | non-chargeable share of classified project $ | unit | B3 doc flags (118-label map, 0 unmapped) | ~18% of units | classified printed-amount lines only |
| ballot purposes (M2 panel A) | normalised keyword categories | referendum | 9 registries | 19,600 bond measures | stand-in for a formal B1 taxonomy (flagged) |
| votes cast / yes-needed (M3) | counts and threshold×total | referendum | TX/WI/LA/NC registries | 7,473 GO measures | CA has % only; 3,188 TX placeholder rows excluded; LA also carries voters_qualified/voted |
| GFD characteristics | pop or enrolment, revenue, own-source, property tax, LTD out | unit, latest yr ≥2012 | national GFD | 100% of entity panel | specials lack Population (revenue-size proxy in N-suite) |
| ACS covariates | homeownership, 65+, fractionalisation, median income | place (munis) / county (rest) | ACS5-2019 national pulls | ~100% | county layer uniform; place upgrade for cities |
| `county_dem2p_2020` | county Dem two-party share | county | MEDSL | 99–100% | 2020 only |
| FOG institutions | form of gov, initiative, referendum, partisan, districts | city | FOG panel | ~570 big cities | subpanel only |
| TEL stringency; ACS-2022; city Dem; mayor party | big-city extras | city | municipal-analysis panels | ~570 cities each | 2013-vintage TEL, no time variation |
| rule (per class) | strict for the unit's entity class | state×entity | rules panel | county 94% · schools 93% · specials 79% · munis 68% · townships 50% (proxy) | township column = pass-2 Part C |

## §6 · The RD core (frame: 11,889 GO measures)

| variable | definition | level | source | coverage in RD frame | window |
|---|---|---|---|---|---|
| `issued_6y` | any issuance ≤6y | referendum | corpus link | **100%** | (0, +6y] |
| GO issuance ≤6y | issued_6y ∧ go_share>0 | referendum | corpus | 100% (go_share observed for 64%, else 0-issue) | headline outcome |
| `nm_par_6y`, `ln_par_pc_6y` | new-money par; ln(1+par p.c.) | referendum | corpus + GFD denominator | 100% / 86% | denominator = gfd_pop, enrolment for schools (65% of frame are schools) |
| `ln_gfd_ltd_pc_6y` | survey LTD issued p.c. (EMMA-independent row) | referendum | GFD + IUF FY23/24 | 73% | fiscal [y+1,y+6]; IUF validated 99.9% |
| capital outlay p.c. (pay-go bound row) | GFD Total_Capital_Outlays p.c. | referendum | GFD | 83% with a 6y window (8,489/10,244 with denominator) | ends FY2023 (IUF has no outlay); total outlay only |
| `ev_m2…ev_p5` | any nm issue in relative year k | referendum×year | corpus | 100% | event study |
| balance covariates | pre-vote GFD pop, revenue p.c., debt p.c., taxes, enrolment, prior failure | referendum | GFD | 94–98% | 0/7 imbalanced |
| McCrary/density inputs | binned margin counts | bin | derived | full frame | TX-driven excess |

## §7 · The response margin (denominators are conditional)

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| `resubmitted_4y`, hazard, KM | same-unit+class return ≤4y | failed measure | panel sequences | 2,680 failed GO measures (the denominator) | risk sets censored at registry end |
| return pass / amount ratio | outcome of the return | return | registries | 1,418 returns; 1,354 with amounts | amounts CA/TX/WI |
| fate table categories | converted / returned / issued-anyway / extinguished | failed measure | corpus + sequences | 1,233 (2005–19 full windows); 422 close | mutually exclusive |
| first-issue authoriser | mode of first post-vote nm issue | referendum | corpus | close window n=2,234 | transition matrix |
| continuation (B5) | window doc sharing the ballot's purpose category | measure×doc | FN2CAT bridge | 3,854 close categorisable measures | bridge precision 80.0% / recall 88.9% (blind audit); reruns on v4 |
| bundle recomposition | categories kept/dropped on return | failure→return pair | bridge | 1,129 pairs | |
| P3 chain | pass→first-issue timing; 8y issuance | conversion | corpus | 132 CA conversions (118 capped / 14 uncapped) | uncapped cell too thin (P4 not confirmed) |

## §8 · Heterogeneity (moderators; split at within-frame medians)

| variable | definition | level (grain) | source | coverage in RD frame | notes |
|---|---|---|---|---|---|
| `acs_homeown/share65/frac/medinc` | proper-grain moderators | **place 2,103 · SD 4,152 · county 5,329** | ACS5 2010/2019 (pre-vote vintage rule) | 97% attached | proper-grain-only splits use the 6,255 place+SD rows |
| `sd_childpov_rate` | district child poverty (income proxy) | school district | SAIPE name-bridge | 35% of frame (4,153 schools) | match rates vary (MN 91% … CA 44%); within-matched validity |
| county moderators | 65+, frac, income (first-pass proxy) | county | CC-EST + SAIPE | 97.4% | superseded by proper grain where available |
| `county_dem2p` (pre-vote) | partisanship | county | MEDSL | 85.7% | null result |
| city Dem share, mayor party | large-city partisanship | city (precinct-built) | municipal-analysis | 1,932 municipal measures in 577-city panel; 178 within ±10 | replicate-the-null only |
| Gini (D6) | B19083 | place/SD/county | new CA pull (2010+2019) | CA cells (blocked-majority analysis) | D6 is CA-only by construction |
| election timing | on-cycle = Nov of even year | referendum | dates | 100% | |
| entity class (fork) | census_type | unit | crosswalk | 100% | schools 7,690 · GP 2,623 · specials 1,576 |

## §9 · Agenda margin and politics

| variable | definition | level | source | coverage | notes |
|---|---|---|---|---|---|
| proposals /100 districts/yr; median ask; on-cycle share | E4 regime comparison | state×year | registries + GFD district counts | CA/TX/WI (MN = classification gap) | |
| pass rates by regime | E3 | regime | registries | 11,888 with margins | invariance at 50 vs 55; breaks at 66.7 |
| props/election; multi-prop share | TX-2019 unbundling | district×election | TX BRB | 2014–25 | reporting-mandate caveat |
| W1/W2 wedge cells | issuance by support band × regime | band×state group | panel | 50–55 band: CA 187 / TX+WI 653 | the DiD-at-fixed-support |
| reform events | attempts/outcomes since 1990 | state×event | web compilation | 11 rows | secondary_unverified (owner) |
| Prop 39 / M56 DiD outcomes | ln per-pupil (per-capita) LTD issued | state×year cells | national GFD 1997–2013 | schools ≥20 districts/cell, 39–48 states | state-mean grain; district-level upgrade deferred |

---

### The three load-bearing coverage facts a referee will probe
1. **RD outcomes are 100%/86% covered in-frame** (binary/intensive) and the
   survey replication row (73%) is symmetric across the cutoff; crosswalk
   selection is Lee-bounded.
2. **Moderator grains are honest**: place for cities, district for schools
   (SAIPE/ACS-SD), county fallback (all specials); splits are within-matched
   and labelled; nothing is imputed.
3. **National corpus coverage post-v3**: 46 states above the 50-doc gate; the
   residuals are five thin small states and five legacy partial-fill states,
   both listed; rule coding 68–94% by class with the township proxy flagged.
