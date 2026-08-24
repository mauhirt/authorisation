# Referendum ↔ issuance linkage — first results

**Built:** 2026-08-24. Marries the two halves of the authorization paper on the
shared Census government key.

## The join (verified)
- **Key:** my crosswalk `unit_id` == the issuance package's `pol_accountable_unit_id`
  (both are 14-digit Census GID; same key space, no translation). Confirmed against
  the same issuer→unit spine the crosswalk was built on.
- **Coverage:** 62.5% of my 7,689 crosswalked referendum units also appear as an
  issuance accountable unit; the rest held referenda but never posted EMMA debt in
  frame (small districts / non-EMMA financing / failed measures — the last is a
  *feature*).
- **Self-validation:** in **1,368** referenda the issuance OS's *own* extracted
  `election_date` equals my referendum date on the same unit — an independent
  confirmation the two datasets describe the same events. This grows as the auth
  package's tier-2 `election_date` enrichment lands (only 4.7% of docs carry one now).

## What the referendum data adds that the issuance corpus structurally cannot
The EMMA corpus is a **survivorship universe** — only debt that was issued. The
referendum data supplies the two things the codebook flags as the external
"downstream merge": **vote margins** (the running variable) and **failed referenda**
(the counterfactual). Both land on the same key.

## First-stage headline — does authorization bind? (`referendum_issuance_link.csv`)
Extensive margin: any issuance by the unit within 6 years of the vote.

| comparison | passed / win | failed / loss | Δ |
|---|--:|--:|--:|
| **Naive** (all referenda) | 35.6% | 14.6% | **+21.0pp** |
| **Close ±5pp** — any issue | 38.0% | 36.9% | +1.1pp |
| **Close ±5pp — GO issue** | 35.2% | 32.8% | **+2.4pp** |
| Close ±2pp — GO issue | 36.1% | 34.2% | +1.8pp |
| Close ±10pp — GO issue | 35.9% | 32.3% | +3.6pp |

**The naive 21pp gap is almost entirely selection** — it collapses to ~2pp at the
threshold. This is the paper's core motivation in one table: comparing passed vs
failed referenda without a design badly overstates how much voter authorization
binds; near the margin, barely-failing a bond vote moves GO issuance only a few
points (governments re-vote, or turn to council/statutory/revenue routes). The
"right of refusal" is softer than the raw contrast implies. The properly-estimated
RD (below) will pin the number.

## Strong, analyzable heterogeneity (±5pp, GO issuance, passed−failed)
TX **+13.9pp**, WI +7.4, MN +4.4, NC +41.7 (n=25) — but **MA −9.8**, LA −5.3, and
**CA 0.0% both sides**. The negatives and CA are informative:
- **CA 0% GO is a data-mapping flag, not a finding** — CA local bonds are GO but the
  issuance `security_pledge_class` isn't labeling them GO for CA; resolve before
  estimating (likely a CA-specific pledge-class coding).
- **MA −9.8** — MA Prop 2½ *debt exclusions* only *permit* borrowing (not mandate),
  and a failed exclusion near the margin can still borrow within the levy limit; the
  sign may be real. Probe, don't dismiss.

## Caveats (these are raw contrasts, not the estimate)
Band means, not a local-linear RD; no density/balance test yet; re-votes
(fail→re-pass) not yet handled; extensive margin only (par/cost intensive margin
next). Treat the table as motivation and a smoke test that the join produces
analyzable variation — which it does.

## State debt-rules integration (institutional treatment)
Merged the state debt-rules panel (`../rules/state_debt_rules.csv`, PRELIMINARY /
AI-coded, ICR 78–88% — descriptive/spec use only, not final estimates) onto the link
at (state, entity_type←census_type, purpose=go_debt, year). This adds the **`rd_sample`
flag** — referenda sitting at a *genuine institutional cutoff*: a mandatory ballot
referendum (`op_referendum_strict=1`), codable, with a margin.

- **rd_sample = 23,577** referenda: TX 8,062 · CA 5,987 · LA 6,581 · WI-schools 2,263
  · MN-schools 406 · NC 278. Thresholds: 50% everywhere except CA (55% school /
  66.7% muni-special, from CDIAC per measure).
- **IL drops** (no vote margins — the running variable is absent), **MA drops**
  (Prop 2½ is a levy exclusion, and go_debt authorization is town-meeting ⅔, not a
  ballot referendum → `strict=0`), **IN drops** (cost-threshold trigger, NA). This is
  the institutionally correct restriction, not a data loss.
- Key clarification the rules resolved: **school GO bonds are mandatory-ballot-
  referendum in 7 states** (CA 55; IL/LA/MN/NC/TX/WI 50) even where the *municipal*
  rule is home-rule (IL) or petition-triggered (WI) — so schools are a valid RD
  sample state-wide, which is most of the corpus.

## BUG FIX (2026-08-24, caught by the E1 gate): TX 'Defeated' was dropped
The result parser used `\bdefeat\b`, which does not match "Defeat**ed**" — all
1,930 TX BRB Defeated measures were coded null, so TX contributed zero failures.
Fixed to stem matching in `build_referendum_issuance_link.py` and
`crosswalk/selection_diagnostics.py`; TX now shows 398 failed at ±5pp (schools).
Numbers below are post-fix.

## First stage on the CLEAN RD sample (rd_sample=1)
GO issuance within 6y, barely-passed vs barely-failed, threshold-centered:

**CA/WI/TX causal core (the BRIEF's frame), 16,312 referenda:**

| bandwidth | n win / loss | GO-issue win vs loss | Δ | z |
|---|--:|--:|--:|--:|
| ±10pp | 4,129 / 2,622 | 37.3% vs 31.2% | +6.1pp | 5.11 |
| **±5pp** | 1,976 / 1,570 | 37.0% vs 30.7% | **+6.3pp** | **3.92** |
| ±2pp | 791 / 662 | 36.7% vs 30.7% | +6.0pp | 2.40 |

All rd_sample states (23,577 — adds LA, MN-schools, NC): +3.6pp at ±5 (z=2.60) —
diluted by LA's parish-fold grain. Per the two-track design (nationwide test +
RDD-where-feasible), the RDD frame is **all six rd_sample states**, with CA/WI/TX
as the dense core and LA/MN/NC as supporting cells; the nationwide test runs on the
full corpus × the state-rules panel (no margins needed).

A barely-passed bond referendum raises the probability of GO issuance within 6 years
by **~6pp at the threshold, stable across bandwidths** — real and significant, but far
below the naive +21pp. Voter authorization at the margin binds *modestly*: most
failed measures still lead to issuance within 6y (~31% do), via re-votes or
council/statutory/revenue routes. The naive-vs-RD wedge and the ~31% "issuance after
refusal" base rate are H1b's raw material (response margin: substitute / re-submit /
abandon).

## Files
- `build_referendum_issuance_link.py` — reproducible; reads the crosswalk +
  state sources + `auth_os.csv.gz` (meta-branch `output/auth_paper/`).
- `add_rules_to_link.py` — merges the state debt-rules panel, adds `rd_sample`.
- `referendum_issuance_link.csv` — 40,924 linked referenda; per-row margin,
  passed, issued_6y, n_issues_6y, par_6y, go_share_6y, voter_auth_share_6y,
  os_confirms_election, entity_type, rule_threshold, op_referendum_strict,
  op_codable, rd_sample.
