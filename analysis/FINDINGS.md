# Who Must Agree — Findings to date

**Date:** 2026-08-24. Every number below is output of a committed script
(`rd_analysis.py`, `mccrary_donut.py`, `rd_outcomes.py`, `failure_paths.py`,
`build_paper_panel.py`, `selection_diagnostics.py` upstream). Frame definitions
in `paper_panel.csv`; estimator: local-linear RD, triangular kernel, HC0 SEs
(`rdlib.py`). This is the working findings record, not the draft.

## The estimation frame
47,235 local referenda (9 states) → 40,924 crosswalked to a Census government
(86.6%; exact tiers ~100% verified, fuzzy tier 95.1% RA-measured) → 23,577 at a
genuine mandatory-ballot statutory cutoff (`rd_sample`) → **11,889 GO-bond
measures** (TX 8,062 · CA 2,189 · WI 999 · LA 361 · NC 278) across three
thresholds (50%; CA 55% schools / 66.7% others). Outcomes: EMMA OS corpus
(258,762 docs) + Census GFD surveys, joined on the shared Census GID.

## F1 · Authorization binds — by ~15pp over six years
Naive passed-vs-failed contrast (all linked referenda): 35.6% vs 14.6% issuance
(+21.0pp) — mostly selection. At the cutoff (rd_sample ∩ bond_go):

| outcome | bw ±5 | bw ±10 |
|---|--:|--:|
| any issuance ≤6y | +0.120 (z 2.65) | **+0.144 (z 4.45)** |
| GO issuance ≤6y | +0.114 (z 2.48) | **+0.146 (z 4.47)** |

Per state (GO, bw10): CA +0.166 (z 2.97) · TX +0.141 (z 3.32) · WI +0.212
(z 3.06) · NC +0.216 (n.s., n=69) · LA −0.276 (z −1.93, n=129, parish-fold grain).
Three states, three different thresholds, one answer.

## F2 · The design validates
- **Balance:** 0 of 7 pre-vote GFD covariates imbalanced at ±5pp (|t| max 1.36).
- **Density:** excess mass above the cutoff is real (McCrary θ=+0.244, z=4.55 at
  h=5) — the endogenous-proposal-timing signature (Cellini–Ferreira–Rothstein),
  itself agenda-margin (H1a) evidence, not vote-count manipulation.
- **Donut-RD:** dropping |margin|≤0.5/1/2pp the GO effect is stable or larger:
  +0.195 (z 5.33) / +0.186 (z 4.52) / +0.199 (z 3.65). Sorting near the cutoff
  cannot be generating the effect.
- **Placebos:** event-study pre-years τ₋₂=+0.007 (z 0.34), τ₋₁=+0.022 (z 1.15);
  GFD pre-period issuance placebo +0.377 (z 1.38) — all n.s.

## F3 · The intensive margin is large — and replicates off-EMMA
| outcome (6y, per capita*) | bw ±5 | bw ±10 |
|---|--:|--:|
| ln(1+ EMMA new-money par p.c.) | +0.910 (z 2.12) | **+0.918 (z 2.99)** |
| ln(1+ **GFD LTD issued** p.c.) — EMMA-independent | +1.065 (z 2.80) | **+1.036 (z 3.81)** |
| PLACEBO: GFD LTD issued, years −3…−1 | +0.434 (z 1.13) | +0.377 (z 1.38) |

The Census-surveyed outcome includes bank loans and private placements that never
post an OS — the survivorship critique of the disclosure corpus cannot explain a
result that replicates in survey data. (*Population; Enrollment for school
districts. GFD FFC/NG split only 53.4%-reported → exploratory: NG +0.160 (z 2.25)
at bw5, FFC ≈ 0.)

## F4 · It is mostly a timing effect: authorization accelerates, refusal delays
Event study, τ_k on 1(any new-money issue in relative year k), bw ±10:

| k | −2 | −1 | **0** | +1 | +2 | +3 | +4 | +5 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| τ_k | +.007 | +.022 | **+.236** | −.008 | −.033 | −.024 | −.000 | −.006 |
| z | 0.3 | 1.2 | **7.8** | −0.3 | −1.4 | −1.2 | −0.0 | −0.3 |

A sharp jump in the vote year, nothing before, ≈0 after: barely-authorized
districts issue immediately; barely-refused ones partially catch up. The 6-year
cumulative wedge (F1/F3) is what remains after catch-up.

## F5 · Refusal is a pause, not a stop (the response margin, H1b)
Failed GO-bond measures, n=2,680 (`failure_paths.py`):
- Re-submission hazard is front-loaded: **26.7%** in year 1 → 22.8% → 15.8% →
  12.4%; Kaplan–Meier **58.2% within 4y**; **median time-to-return 1.02y** — the
  next election.
- **61.9% of returns pass** (878/1,418) → ~36% of failures convert to
  authorization within 4y through re-voting alone.
- **Districts re-ask, they don't concede:** median amount ratio return/original
  **1.00** (n=1,354); only 45.9% downsize.

## F6 · Proximity shapes the response; the symbolic majority does not
Within CA (supermajority regimes; the pooled cross-state version is
composition-confounded and flagged):
- **Majority-failures** (50<yes<threshold) re-submit at **42.2%** vs **27.4%**
  for minority-failures, and route more of their subsequent issuance through
  the council channel (share 0.488 vs 0.396).
- **Signal test (D2b):** among CA school failures — both sides of 50% fail
  institutionally — the re-submission RD at the 50 line is a **null**
  (τ=−0.14, z=−1.0, n=326): the response tracks proximity smoothly; no jump at
  the symbolic majority. (Low power noted.)
- Open puzzle for D5: within CA, majority-failures show *lower* 6y issuance
  (23.5% vs 34.6%) despite re-submitting more.

## F7 · Substitution toward the council channel
After a narrow refusal, the authorization mix of what the unit still issues
tilts toward council authorization: council share τ=−0.064 (z=−2.03, bw10;
barely-passed units are less council-reliant). Modest, in the theory's direction.

## Reading (one paragraph)
The coalition requirement operates exactly as "Who Must Agree" frames it. At the
**agenda margin**, governments time proposals to win (the density asymmetry). At
the **authorization margin**, a narrow yes raises six-year GO issuance by ~15pp
and roughly doubles per-capita borrowing — in disclosure *and* survey data. At
the **response margin**, a narrow no mostly buys delay: the median refused
district returns at the next election with the same ask, 58% return within four
years, 62% of returns pass, and what still issues leans on the council channel.
Voter authorization is a real constraint on *when* and *how*, and a weaker
constraint on *whether*.

## Caveats & pending
- Rules panel is AI pass-1 (`PRELIMINARY`, ICR 78–88%): fine for this record,
  human pass-2 required before final estimates cite it.
- IL/IN lack vote margins (harvest scoped, paused); LA/MN cells small.
- GFD FFC/NG decomposition half-reported (53.4%) → exploratory only.
- MSE-optimal bandwidth + formal Cattaneo density test + Lee bounds on the final
  spec: to run in the estimation polish pass (prep committed).
- Pending upstream: auth tier-2 refresh (election_date enrichment), B4 pass-2;
  B3 chargeable flag → C2/H2; D5 heterogeneity (ACS join).
