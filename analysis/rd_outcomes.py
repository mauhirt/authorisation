#!/usr/bin/env python3
"""RD on the full outcome set (frame: rd_sample ∩ bond_go). Three blocks:
 A. Intensive margin + EMMA-independent GFD outcomes (+ pre-period placebo).
 B. Authorization-channel composition (substitution evidence).
 C. Event study: tau_k for relative years k=-2..+5 on 1(any new-money issue in
    year k) — pre-years are placebos, the profile is the D1 dynamic figure.
Writes analysis/OUTCOMES_RESULTS.md. All numbers from this script."""
import csv, math
from collections import Counter
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
def f(x):
    try: return float(x)
    except: return None
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
for r in S: r["_m"]=f(r["threshold_centered_margin"])
print("frame:",len(S))

def dep_ln_ffc(r):
    v=f(r["gfd_ltd_ffc_6y"]); pop=f(r["gfd_pop"]) or f(r["gfd_enrollment"])
    if v is None or not pop or pop<=0: return None
    return math.log1p(max(0.0,v)*1000/pop)
def dep_ln_ng(r):
    v=f(r["gfd_ltd_ng_6y"]); pop=f(r["gfd_pop"]) or f(r["gfd_enrollment"])
    if v is None or not pop or pop<=0: return None
    return math.log1p(max(0.0,v)*1000/pop)
def dep_ln_pre(r):
    v=f(r["gfd_ltd_iss_pre3"]); pop=f(r["gfd_pop"]) or f(r["gfd_enrollment"])
    if v is None or not pop or pop<=0: return None
    return math.log1p(max(0.0,v)*1000/pop)

DEPS=[
 ("ln_par_pc_6y","ln(1+ EMMA new-money par p.c.), 6y", lambda r: f(r["ln_par_pc_6y"])),
 ("ln_gfd_ltd_pc_6y","ln(1+ GFD LTD issued p.c.), 6y  [EMMA-independent]", lambda r: f(r["ln_gfd_ltd_pc_6y"])),
 ("ln_gfd_ffc_pc_6y","ln(1+ GFD FFC (guaranteed) issued p.c.), 6y", dep_ln_ffc),
 ("ln_gfd_ng_pc_6y","ln(1+ GFD nonguaranteed issued p.c.), 6y", dep_ln_ng),
 ("ln_gfd_pre3","PLACEBO: ln(1+ GFD LTD issued p.c.), years −3..−1", dep_ln_pre),
]
L=["# RD — full outcome set (rd_sample ∩ bond_go)\n",
   f"Frame n = {len(S)}. Local-linear, triangular kernel, HC0 SEs (`rdlib.py`).",
   "GFD windows use fiscal years [y+1, y+6]; GFD ends FY2023, so recent votes have",
   "partial windows — symmetric across the cutoff, so the RD contrast is unaffected.\n",
   "## A · Intensive margin + EMMA-independent outcomes",
   "| outcome | bw | τ | SE | z | n L/R | left mean |","|---|--:|--:|--:|--:|---|--:|"]
for key,lab,fn in DEPS:
    for bw in (5,10):
        pairs=[(r["_m"],fn(r)) for r in S]
        res=rd(pairs,bw)
        if res:
            L.append(f"| {lab} | ±{bw} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} "
                     f"| {res['nL']}/{res['nR']} | {res['aL']:.3f} |")
L.append("")

# B: composition
L+=["## B · Authorization channel of post-vote EMMA issuance (substitution)",
    "council_share_6y = council/(voter+council) among the unit's window docs (conditional on ≥1 determined doc).",
    "| outcome | bw | τ | SE | z | n L/R | left mean |","|---|--:|--:|--:|--:|---|--:|"]
for key,lab in [("council_share_6y","council share of authorized window docs"),
                ("n_voter_6y","# voter-authorized docs, 6y"),
                ("n_council_6y","# council-authorized docs, 6y")]:
    for bw in (5,10):
        pairs=[(r["_m"],f(r[key])) for r in S]
        res=rd(pairs,bw)
        if res:
            L.append(f"| {lab} | ±{bw} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} "
                     f"| {res['nL']}/{res['nR']} | {res['aL']:.3f} |")
L.append("")

# C: event study
L+=["## C · Event study: τ_k on 1(any new-money EMMA issue in relative year k), bw ±10",
    "| rel. year k | τ_k | SE | z | left mean |","|---|--:|--:|--:|--:|"]
for c,k in [("ev_m2","−2"),("ev_m1","−1"),("ev_0","0"),("ev_p1","+1"),
            ("ev_p2","+2"),("ev_p3","+3"),("ev_p4","+4"),("ev_p5","+5")]:
    pairs=[(r["_m"],f(r[c])) for r in S]
    res=rd(pairs,10)
    if res:
        L.append(f"| {k} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} | {res['aL']:.3f} |")
L.append("\nPre-vote years (−2, −1) are placebos: τ should be ≈0 there and jump at 0/+1.")

open("analysis/OUTCOMES_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
