# Revision execution plan — APSA draft → political-economy paper

Crosswalk from `WhoMustAgree_revision_directive.md` to concrete actions.
Empirics are FROZEN (Part 4): reuse verbatim, re-order and re-narrate only.
Status: DONE (in repo) / READY (awaiting owner files) / OWNER (owner text) /
POST-APSA (Part 5 TODO).

## Concordance with the data audit
Part 2's binding constraints are exactly the audit findings
(`authorisation_data_audit.md`): $R_j$ continuous/function-level/predetermined;
no graded de jure $L^{\text{law}}$; `op_referendum_strict` is $\theta$, a
state$\times$type binary (0/160 within-government variation); type is the
ordinal $L$ for the fork; the continuous $R_j\times L^{\text{law}}$ match is an
R&R extension. Nothing below claims a continuous de jure $L$.

## Inputs still needed from the owner (blockers for the prose restructure)
1. `Revised_Framework__De_Jure_Exit__Franchise__and_Electorate_Heterogeneity.md`
   — the formal apparatus, predictions, stages, inferential hierarchy, compact
   statement. NOT in repo. Required for the framework prose (Parts 1, 3).
2. `WhoMustAgree_section2_draft.tex` — the drafted §2 to insert verbatim
   (carries $R_j$, de jure $L$, the $R\times L$ match, the franchise cases).
   NOT in repo. Required for §2 (Part 3).
3. The owner's **current `main.tex`** (the hand-rewritten version with the
   "When Does a Political Constraint Constrain?" intro, §2, origins). The repo's
   `MANUSCRIPT.md` / `INTRO_ARGUMENT_HISTORY.md` have diverged from it. Required
   so the Part 3 section rewrites edit live text, not stale text.

## Part 3 section-by-section map

| Directive item | Action | Status |
|---|---|---|
| Intro "When Does a Political Constraint Constrain?" — mechanism-first, thesis sentence, five facts by p.3, history out of the opening | Rewrite intro | OWNER text; needs current main.tex + Revised_Framework |
| §2 The Institution: Scope, Height, Exit — replace with `WhoMustAgree_section2_draft.tex`, trim continuous-$L$ phrasing per Part 2 | Insert draft, trim | READY on receipt of the §2 file |
| §3 Origins — compress to short institutional-background; keep (not appendix); retain franchise/capture + five-state genealogy | Compress owner §3 | OWNER text; genealogy table already built (`T_genealogy`) |
| Data section — add $R_j$ (function-level, predetermined) and $L$ (type as de jure exit proxy; graded $L^{\text{law}}$ named as build target); state predetermined-primitives ordering | Add definitions | READY (short insert; I can draft against current data section) |
| Results national (Stage I) — relabel the "first stage" table as institutional validation / descriptive association; present $R_j\times\theta$ as substitution | Relabel R1; reframe R2 | **DONE** (see below) |
| Results close elections (Stage II) — keep RD; foreground +11.5 out-of-design agreement as "two designs, one answer" | Re-order narration | OWNER text (RD/agenda tables unchanged) |
| Results where consent binds (Stage III) — lead with predetermined school-vs-general-purpose fork; $\tau_k$ schedule with honest CIs, as heterogeneity across non-random groups | Re-narrate T7 fork + T6 | OWNER text; exhibits unchanged |
| Response to refusal (Stage IV) — keep accounting; frame as delay not denial | Re-narrate T5 | OWNER text; exhibit unchanged |
| Electorates and the cost of consent — NEW separate section; homeownership/homogeneity/age/timing as $C_V(\theta,e_i)$, exploratory, post-hoc, load-bearing for nothing; do not conflate with exit strata | Split T6 moderators into own section | OWNER text; needs Revised_Framework notation |
| Exit and institutional persistence — keep as tested descriptive implication (threshold-change attempts by sector), not a second contribution | Re-narrate A4/reform | OWNER text |
| Contribution — three points; restore who-pays clause (paying public / ratepayers, no vote) | Rewrite | OWNER text |
| Conclusion — incidence = f(constraint, alternatives); compress; no new historical theory | Rewrite | OWNER text |

## Empirics relabelling (DONE — Part 3 "Results national", Part 4 reuse)
`exhibits/build_reg_tables.py`, regenerated:
- **R1** (`tab:r1`): caption "The fifty-state first stage…" → **"Institutional
  validation: the referendum rule ($\theta$) and the voted share of borrowing
  (descriptive association)"**; note now states the rule is $\theta$ (not the
  exit menu $L$), varies only across states (0/160 within-government), Stage I
  cross-state descriptive association, "not a first stage and not causal."
- **R2** (`tab:r2`): caption "Substitution away from the voted instrument…" →
  **"The substitution test ($R_j\times\theta$): composition adjusts, aggregate
  quantity does not"**; note frames it as P1 (substitution needs a feasible
  legal exit) and P3 (composition adjusts before quantity), $\theta$
  cross-state associational, Stage I, not the exit match.
No numbers changed — caption/notes only (frozen-empirics safe). Drop-in `.tex`
in `exhibits/out/R1_firststage.tex`, `exhibits/out/R2_substitution.tex`.

## No exhibit claims a continuous de jure $L^{\text{law}}$ (Part 2.6 check)
Grepped the exhibit set: the only "menu" object is the realised non-voted share
(`m1_menu_matrix.py`, Table A5 / `tab:menu`), which is used descriptively as the
class-level menu in the fork, never as a de jure $L$. The R1/R2 notes now name
`op_referendum_strict` as $\theta$. No exhibit asserts $E=g(R,L^{\text{law}})$
with a continuous de jure $L$.

## Part 5 — post-APSA identification hardening (TODO markers to insert in text)
- Kolesár--Rothe honest CIs for the discrete running variable (Texas mass
  points) — the correct inference object; resolves the MSE-optimal null.
- Donut as the default RD spec.
- Lead the cleaner states; show Texas separately as the manipulated case.
- Covariate-adjusted RD as main spec + joint balance test (the income jump,
  T2 row `ln median household income` $t=2.1$).
- Fix ACS vintage for mid-decade votes (vintage ending before the vote year;
  show robustness). Audit Check 4 flagged the ACS5-window straddle.

## Part 6 — the open decision (write to the fallback now)
Framework and results are written to the fallback: $R_j$ (continuous) $\times$
type (ordinal $L$); the continuous $R_j\times L^{\text{law}}$ match is stated as
an extension / R&R target. A build spec for a de jure $L^{\text{law}}$ (graded
index of lawfully-available exempt forms per type$\times$state, from the pass-2
archive) is the separate deliverable that would promote the match from extension
to result; feasibility (can the archive code every type$\times$state cell, or
only a handful of states?) to be scoped before committing.
