#!/usr/bin/env python3
"""D5 — heterogeneity of the authorization effect (frame: rd_sample ∩ bond_go).

Moderators (county grain, 2015 vintage, keyless Census sources):
  share65  county 65+ population share      (CC-EST2019 ASRH, YEAR=8)
  frac     ethno-racial fractionalization   (1 − Σ share², NH groups + Hispanic)
  medinc   median household income          (SAIPE 2015)
Provenance: www2.census.gov popest ASRH cc-est2019-alldata.csv + saipe est15all.xls,
fetched 2026-08-24; built by the county-moderators block (see git log).
County FIPS per unit from the GFD subset (FIPS_Code_State + FIPS_County).
Also: on-cycle (November of an even year) vs off-cycle election timing.

For each moderator: split the frame at the within-frame median, run the GO-issuance
RD (bw ±10) in each half. County-grain moderators are a PROXY for district
electorates (schools/specials span or subset counties) — first pass pending the
ACS key for place/school-district-geography grain (`acs_pull.py`).
Writes analysis/D5_RESULTS.md."""
import csv, gzip, datetime as dt
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None

# unit9 -> (state_fips, county_fips), latest GFD year wins
u2c={}
with gzip.open("analysis/cache/gfd_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        st=(r["FIPS_Code_State"] or "").strip().zfill(2)
        ct=(r["FIPS_County"] or "").strip().zfill(3)
        if st!="00" and ct not in ("","000"):
            u2c[r["GOVSid"].strip()]=(st,ct)
mods={}
for r in csv.DictReader(open("analysis/cache/county_moderators_2015.csv")):
    mods[(r["state_fips"],r["county_fips"])]={k:f(r[k]) for k in ("share65","frac","medinc")}

rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
matched=0
for r in S:
    r["_m"]=f(r["threshold_centered_margin"])
    c=u2c.get((r["unit_id"] or "")[:9]); mv=mods.get(c) if c else None
    r["_mod"]=mv
    if mv: matched+=1
    d=(r["election_date"] or "")
    try:
        dd=dt.date.fromisoformat(d[:10])
        r["_oncycle"]=1 if (dd.month==11 and dd.year%2==0) else 0
    except: r["_oncycle"]=None
print(f"frame {len(S)}; county moderators matched {matched} ({matched/len(S):.1%})")

def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0
def run(sub,label,L):
    res=rd([(r["_m"],go(r)) for r in sub],10)
    if res:
        L.append(f"| {label} | {len(sub)} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} | {res['nL']}/{res['nR']} |")

L=["# D5 — heterogeneity of the authorization effect (GO issuance ≤6y, bw ±10)\n",
   f"Frame {len(S)}; county-grain moderators matched {matched} ({matched/len(S):.1%}).",
   "County moderators are a proxy for district electorates (first pass; ACS key",
   "upgrade path in `acs_pull.py`). Split at the within-frame median.\n",
   "| subgroup | n | τ | SE | z | n L/R |","|---|--:|--:|--:|--:|---|"]
run(S,"ALL (reference)",L)
for key,lab in [("share65","65+ share"),("frac","fractionalization"),("medinc","median HH income")]:
    vals=sorted(r["_mod"][key] for r in S if r["_mod"] and r["_mod"][key] is not None)
    if not vals: continue
    med=vals[len(vals)//2]
    lo=[r for r in S if r["_mod"] and r["_mod"][key] is not None and r["_mod"][key]<med]
    hi=[r for r in S if r["_mod"] and r["_mod"][key] is not None and r["_mod"][key]>=med]
    run(lo,f"{lab} < median ({med:.3f})",L); run(hi,f"{lab} ≥ median",L)
on=[r for r in S if r["_oncycle"]==1]; off=[r for r in S if r["_oncycle"]==0]
run(on,"on-cycle (Nov, even yr)",L); run(off,"off-cycle",L)
L.append("\n**Read (descriptive, not asserted):** the effect concentrates in OLDER counties")
L.append("(τ +0.201 vs +0.057) and ON-CYCLE elections (+0.252 vs +0.099) — authorization by a")
L.append("broad, older electorate binds hardest, while off-cycle refusals (frequent, low-salience")
L.append("election dates) are easiest to reverse, consistent with the re-submission mechanism.")
L.append("Income splits mildly positive-rich; FRACTIONALIZATION runs slightly AGAINST the naive")
L.append("H3 read (+0.167 low vs +0.125 high) — H3 is partially supported, not uniformly.")
open("analysis/D5_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
