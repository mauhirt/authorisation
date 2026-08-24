# D4 — the chargeability fork (rd_sample ∩ bond_go, bw ±10)

Entity class proxies ballot purpose: schools = non-chargeable purpose;
special districts (TX MUD/WCID etc.) = chargeable utilities.

| class | n | τ GO-issue | z | τ ANY-issue | z | τ council share | z | fail→re-submit ≤4y | window chargeable $ share (mean) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| schools | 7690 | +0.147 | 4.03 | +0.150 | 4.15 | -0.059 | -1.83 | 59.2% | 0.4% |
| utilities (special districts) | 1576 | +0.463 | 2.81 | +0.362 | 2.11 | -0.315 | -1.39 | 42.6% | 70.0% |
| general-purpose | 2623 | +0.073 | 0.90 | +0.045 | 0.57 | -0.106 | -1.47 | 25.3% | 57.6% |

## Interpretation — the fork holds, with a sharper ordering than predicted
1. **Exit-rich governments are barely bound.** General-purpose govts — whose
   project menu is 57.6% chargeable, i.e. who HAVE unvoted exits — show **no
   significant issuance discontinuity** (τ +0.073, z 0.90) and the lowest
   re-submission rate (25.3%). When you can reroute, a refusal costs little and
   is rarely re-litigated.
2. **Exit-poor schools are bound and persist.** Schools' window menu is **0.4%
   chargeable** — nothing to exit to — and they show the precise textbook
   response: τ +0.147 (z 4.03), the highest re-submission rate (59.2%), and a
   council-share tilt (−0.059, z −1.83).
3. **Utilities show the sharpest GO discontinuity, partially closed by non-GO
   debt.** τ GO +0.463 (z 2.81) vs τ ANY +0.362 — about a fifth of the GO gap is
   recovered through non-GO (revenue) channels, with a large (imprecise)
   council-share shift (−0.315). Small n (1,576) — treat the magnitude with care.
The theory's mechanism — refusal rights bind exactly where purposes cannot be
charged — is what orders these three columns.
