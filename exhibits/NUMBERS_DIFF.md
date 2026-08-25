# NUMBERS_DIFF.md — values that changed from the draft under final specifications

Required by INSTRUCTION_exhibits build requirement 3 ("it should be empty; if not, say
why"). It is not empty. Every difference below comes from one cause: the exhibits adopt
the rdrobust convention (RBC estimate with robust inference is the headline number),
while the draft text sometimes cites the conventional local-linear estimate. No data,
frame, or specification changed; the frozen v3 package and the ±10pp bandwidth are
identical throughout. The conventional estimates in the tables reproduce the draft's
numbers.

1. **T3 same-purpose continuation.** Draft (§6) cites the conventional estimate
   **+0.072 (z ≈ 2.1)**. Under RBC the row is **+0.052 [−0.047, +0.152], robust
   p = 0.302** — imprecise. The table shows both; the draft sentence should be
   softened to "positive but imprecise under robust bias-corrected inference"
   (the Conv. column shows +0.073, the draft's number to rounding). Note the
   continuation frame is 3,868 measures here vs 3,854 in `analysis/B5_RESULTS.md` — a
   cosmetic difference from margin-exactly-0 handling in the rebuild; it moves the
   conventional estimate from +0.072 to +0.073 and nothing else at reported precision.

2. **T6 65+ split.** Draft (§8) reads the 65+ gradient from the high/low levels. The
   levels keep their pattern (below-median +0.043 n.s.; above-median +0.097 n.s.), but
   the formal **difference row is null under RBC: +0.054, p = 0.646**. The draft's
   ordering claim survives; any stronger wording should be dropped.

3. **F2 event-study τ0.** Draft cites **+0.236** (conventional). The figure annotates
   the RBC estimate **+0.246 [+0.159, +0.333]**; the CSV carries both. Same estimand,
   reporting-convention difference only.

4. **A2 pseudo-cutoff 45 (50%-regime states).** New computation for this build (no
   draft number to diff, recorded for honesty): RBC **+0.143 [−0.004, +0.290], robust
   p = 0.057** — marginal, conventional +0.012 essentially zero. Both-sides-fail
   placebo windows are thin on the right (effective N 786/687) and the RBC estimate is
   noisy there; the other three placebos are comfortably null. Report as "null at the
   5% level".

5. **T2/T3 headline rows.** For the record, the leads did **not** move: any-GO ≤6y RBC
   +0.110 [+0.016, +0.204] and pay-go RBC +0.464 / conventional +0.377 match the
   draft's citations exactly (the draft already used RBC for these after round 3).
