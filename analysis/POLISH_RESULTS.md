# Estimation polish (map item 9) — headline: GO issuance ≤6y

Estimation sample n=11872.

## 1 · IK MSE-optimal bandwidth
- pilots: h1=6.20, f̂(0)=0.0186, σ̂²=0.2364, m3=4.567e-05, h2=(3.20,2.68), m2=(-0.001767,-0.07023)
- **h_IK = 1.81pp**; τ(h_IK) = **-0.001 (SE 0.075, z -0.02)**, n=353/452  |  τ(±10) = +0.146 (z 4.47)

## 2 · Clustered SEs (bw ±10)
| variance | τ | SE | z | clusters |
|---|--:|--:|--:|--:|
| HC0 (baseline) | +0.146 | 0.033 | 4.47 | – |
| cluster: unit | +0.146 | 0.036 | 4.11 | 2480 |
| cluster: county | +0.146 | 0.042 | 3.47 | 650 |

## 3 · Lee bounds vs crosswalk selection (pooled close-window trim p=2.52%)
τ(±10) point +0.146; **sharp bounds [+0.138, +0.163]** (binary outcome; over-represented right side trimmed toward 1s / 0s).
Zero-selection benchmark states (MA/NC, p=0) reported in RD_RESULTS.md.

## 4 · Randomization inference (|margin|≤2, 5000 permutations, seed 42)
observed diff-in-means +0.142; **RI p-value = 0.0000** (n=900)

## 5 · McCrary log-density by state (bin 0.5, h=10)
| state | θ | SE | z |
|---|--:|--:|--:|
| CA | +0.101 | 0.096 | 1.05 |
| TX | +0.206 | 0.076 | 2.71 |
| WI | +0.012 | 0.183 | 0.07 |
| LA | -0.002 | 0.216 | -0.01 |
| NC | -0.183 | 0.496 | -0.37 |
| POOLED | +0.140 | 0.054 | 2.58 |

## 6 · LA diagnostic
LA frame n=361; GO-issue base rate 59.3% (parish-fold grain: measures fold to the parish, so the outcome mixes many measures' issuance).
Pooled τ excluding LA (bw10): **+0.162 (z 4.87)** vs +0.146 with LA — LA's negative cell does not drive the headline; treat LA as fold-grain caveat, not signal.

## Interpretation

The headline estimate survives the full battery, with one nuance to report transparently.

1. **The IK bandwidth is the nuance.** h_IK = 1.81pp is extremely small (the variance
   term dominates because f̂(0) is low — only ~805 obs within ±2pp of the cutoff), and
   at that window a local-linear fit spends 4 of its effective parameters on slopes
   estimated from ~1.8pp of support: τ(h_IK) = −0.001 (SE 0.075) is noise-dominated,
   not a contradiction. Two design-based checks at the SAME near-cutoff window say the
   effect is there: (a) randomization inference on the diff-in-means at |margin|≤2
   gives +0.142 with p < 0.0002 (0/5000 permutations as extreme), and (b) the donut RD
   (excluding |margin|<0.5–1) is **larger**, +0.19 to +0.20 (MCCRARY_DONUT_RESULTS.md).
   The honest reading: at tiny bandwidths the slope terms eat the signal; the
   diff-in-means at the same window, every bandwidth from ±3 to ±10, and the donut
   variants agree on a robust positive effect. Report τ(h_IK) in the robustness table
   with this note, not as the headline.
2. **Clustering does not threaten inference**: z = 4.11 clustered by unit (2,480
   clusters), z = 3.47 clustered by county (650) — the conservative end still >3.
3. **Crosswalk selection is bounded tightly**: Lee bounds [+0.138, +0.163] around
   +0.146 — the 2.52% match-rate imbalance cannot move the estimate materially, and
   the zero-selection states (MA/NC) provide the p=0 benchmark.
4. **McCrary is a TX phenomenon**: pooled θ = +0.140 (z 2.58) decomposes into
   TX +0.206 (z 2.71) with every other state flat (CA +0.101 z 1.05; WI/LA/NC ≈ 0).
   Consistent with the small-electorate discreteness caveat (AGENDA_RESULTS: many tiny
   TX districts where a handful of votes = several pp of margin, producing lumpy
   margins near 0) rather than manipulation; and the donut RDs — the direct answer to
   density concerns — are stable-to-larger.
5. **LA's fold-grain cell is a caveat, not a driver**: excluding LA moves the pooled
   estimate to +0.162 (z 4.87).

