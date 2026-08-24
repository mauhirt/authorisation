#!/usr/bin/env python3
"""Extend paper_panel.csv with the full outcome set (fast: reads the caches).

EMMA outcomes (issuance_subset), window (vote date, +6y]:
  nm_par_6y        new-money par (has_new_money & !has_refunding weight par_effective;
                   dedup on issue_id)
  ln_par_pc_6y     ln(1 + nm_par_6y / gfd_pop)
  n_voter_6y/n_council_6y/n_statutory_6y   auth-mode counts among window docs
  council_share_6y council/(voter+council) among determined window docs ('' if none)
  ev_m2..ev_p5     1(any new-money issue in relative year k), k=-2..+5 (event study)

GFD outcomes (gfd_subset) — EMMA-INDEPENDENT (catches bank loans/private placements):
  gfd_ltd_iss_6y / _ffc_6y / _ng_6y   sum of Total_LTD_Issued (and FFC/NG) over
                                      fiscal years [y+1, y+6]
  gfd_ltd_iss_pre3                    sum over [y-3, y-1] (placebo/baseline)
  ln_gfd_ltd_pc_6y                    ln(1 + ltd_iss_6y*1000 / gfd_pop)  (GFD $ are $k)
Writes paper_panel.csv in place (adds columns)."""
import csv, gzip, math, datetime as dt
from collections import defaultdict

PANEL="analysis/paper_panel.csv"
rows=list(csv.DictReader(open(PANEL)))
def fl(x):
    try: return float(x)
    except: return None
def pdate(s):
    try: return dt.date.fromisoformat((s or "")[:10])
    except: return None

# ---- EMMA issuance by unit ----
iss=defaultdict(list)
with gzip.open("analysis/cache/issuance_subset.csv.gz","rt") as f:
    for r in csv.DictReader(f):
        u=(r["pol_accountable_unit_id"] or "")[:9]
        d=pdate(r["dated_date"])
        if not d:
            y=r.get("year") or ""
            d=dt.date(int(y),7,1) if y.isdigit() else None
        if not d: continue
        nm=(r.get("has_new_money","").lower() in ("true","1")) and (r.get("has_refunding","").lower() not in ("true","1"))
        iss[u].append((d,r["issue_id"] or r["doc_id"],fl(r["par_effective"]),
                       r.get("auth_mode_final2") or "",nm))

# ---- GFD flows by unit-year ----
gf=defaultdict(dict)   # unit9 -> year -> (ltd_iss, ffc, ng)
with gzip.open("analysis/cache/gfd_subset.csv.gz","rt") as f:
    for r in csv.DictReader(f):
        g=r["GOVSid"].strip(); y=int(r["Year4"])
        gf[g][y]=(fl(r["Total_LTD_Issued"]) or 0.0, fl(r["Total_LTD_Iss_FFC"]) or 0.0,
                  fl(r["Total_LTD_Iss_NG"]) or 0.0)
# IUF extension (FY2023/24, validated 99.9% vs GFD-2022; totals only, no FFC/NG split)
import os
if os.path.exists("analysis/cache/iuf_extension.csv"):
    next_=0
    for r in csv.DictReader(open("analysis/cache/iuf_extension.csv")):
        g=r["unit9"]; y=int(r["year"]); v=fl(r["ltd_iss_k"])
        if v is not None and y not in gf[g]:
            gf[g][y]=(v,0.0,0.0); next_+=1
    print(f"IUF extension merged: {next_} unit-years added")

NEW=["nm_par_6y","ln_par_pc_6y","n_voter_6y","n_council_6y","n_statutory_6y","council_share_6y",
     "ev_m2","ev_m1","ev_0","ev_p1","ev_p2","ev_p3","ev_p4","ev_p5",
     "gfd_ltd_iss_6y","gfd_ltd_ffc_6y","gfd_ltd_ng_6y","gfd_ltd_iss_pre3","ln_gfd_ltd_pc_6y"]
W6=dt.timedelta(days=2192)
for r in rows:
    for c in NEW: r[c]=""
    d=pdate(r["election_date"]); u=(r["unit_id"] or "")[:9]
    if not d or not u: continue
    pop=fl(r["gfd_pop"])
    if (not pop or pop<=0): pop=fl(r["gfd_enrollment"])   # schools: enrollment is the scale var
    # EMMA window
    seen=set(); par=0.0; nv=nc=ns=0
    ev=[0]*8   # k=-2..+5
    for dd,iid,pv,am,nm in iss.get(u,[]):
        rel=(dd-d).days/365.25
        k=math.floor(rel)
        if -2<=k<=5 and nm: ev[k+2]=1
        if not (dt.timedelta(0)<dd-d<=W6): continue
        if iid in seen: continue
        seen.add(iid)
        if nm and pv: par+=pv
        if am=="voter": nv+=1
        elif am=="council_or_board": nc+=1
        elif am=="statutory": ns+=1
    r["nm_par_6y"]=f"{par:.0f}"
    if pop and pop>0: r["ln_par_pc_6y"]=f"{math.log1p(par/pop):.4f}"
    r["n_voter_6y"],r["n_council_6y"],r["n_statutory_6y"]=nv,nc,ns
    if nv+nc>0: r["council_share_6y"]=f"{nc/(nv+nc):.3f}"
    for i,c in enumerate(["ev_m2","ev_m1","ev_0","ev_p1","ev_p2","ev_p3","ev_p4","ev_p5"]):
        r[c]=ev[i]
    # GFD window (fiscal years)
    ys=gf.get(u,{})
    post=[ys[y] for y in range(d.year+1,d.year+7) if y in ys]
    pre=[ys[y] for y in range(d.year-3,d.year) if y in ys]
    if post:
        t=sum(x[0] for x in post); fc=sum(x[1] for x in post); ng=sum(x[2] for x in post)
        r["gfd_ltd_iss_6y"]=f"{t:.0f}"; r["gfd_ltd_ffc_6y"]=f"{fc:.0f}"; r["gfd_ltd_ng_6y"]=f"{ng:.0f}"
        if pop and pop>0: r["ln_gfd_ltd_pc_6y"]=f"{math.log1p(max(0.0,t)*1000/pop):.4f}"
    if pre: r["gfd_ltd_iss_pre3"]=f"{sum(x[0] for x in pre):.0f}"

with open(PANEL,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
n6=sum(1 for r in rows if r["gfd_ltd_iss_6y"]!="")
print(f"outcomes added to {len(rows)} rows; GFD 6y-flow coverage {n6} ({n6/len(rows):.1%})")
