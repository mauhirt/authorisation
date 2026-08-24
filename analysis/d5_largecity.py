#!/usr/bin/env python3
"""Large-city robustness of the partisanship null, using the BETTER measures:
precinct-aggregated city-footprint Dem share (577 cities, 2004-2024) and mayor
party (Harvard/mayor panel). POWER-LIMITED by construction: only 178 GO-bond
measures sit within +/-10pp in these cities, so we (a) pool rd_sample ANY-purpose
measures at their genuine cutoffs for the headline split (labeled), (b) report
bond_go-only as secondary, and (c) interpret as replicate-the-null, not as an
independent discovery. Writes analysis/D5_LARGECITY_RESULTS.md."""
import csv, gzip
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None
u2f7={}
with gzip.open("analysis/cache/gfd_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        st=(r["FIPS_Code_State"] or "").strip().zfill(2); p=(r["FIPS_Place"] or "").strip()
        if st!="00" and p and p!="0": u2f7[r["GOVSid"].strip()]=st+p.zfill(5)
# city dem share by (fips7, election year)
cp=defaultdict(dict)
for r in csv.DictReader(open("inputs/external_municipal_analysis/city_partisanship_panel.csv")):
    f7=str(r["fips"]).split(".")[0].zfill(7)
    cp[f7][int(r["year"])]=f(r["dem_share2p"])
# mayor party by (fips7, year)
mp=defaultdict(dict)
for r in csv.DictReader(open("inputs/external_municipal_analysis/mayor_party.csv")):
    f7=str(r["fips"]).split(".")[0].zfill(7)
    y=r.get("year")
    if y and y.isdigit(): mp[f7][int(y)]=r.get("mayor_pid","")
rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
S=[r for r in rows if str(r["rd_sample"])=="1" and f(r["threshold_centered_margin"]) is not None
   and r["census_type"] in ("municipal","township") and u2f7.get((r["unit_id"] or "")[:9]) in cp]
for r in S:
    r["_m"]=f(r["threshold_centered_margin"]); f7=u2f7[r["unit_id"][:9]]
    vy=int((r["election_date"] or "2000")[:4])
    yrs=[y for y in cp[f7] if y<=vy]
    r["_dem"]=cp[f7][max(yrs)] if yrs else None
    my=[y for y in mp.get(f7,{}) if y<=vy]
    r["_mayor"]=mp[f7][max(my)] if my else ""
def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0
def anyi(r): return f(r["issued_6y"])
L=["# Large-city partisanship robustness — precinct city-footprint + mayor party\n",
   f"rd_sample municipal measures in the 577-city panel: {len(S)} "
   f"(bond_go: {sum(1 for r in S if r['purpose_class']=='bond_go')}). POWER-LIMITED — "
   "read as replicate-the-null, not independent discovery.\n"]
for title,frame in [("ANY purpose (headline for power; tax measures at their genuine cutoffs included)",S),
                    ("bond_go only (secondary)",[r for r in S if r["purpose_class"]=="bond_go"])]:
    L+=[f"## {title}","| split | subgroup | n | τ any-issue | SE | z |","|---|---|--:|--:|--:|--:|"]
    have=[r for r in frame if r["_dem"] is not None]
    if len(have)>=200:
        vals=sorted(r["_dem"] for r in have); med=vals[len(vals)//2]
        for lab,G in [(f"city Dem < med ({med:.2f})",[r for r in have if r["_dem"]<med]),
                      ("city Dem ≥ med",[r for r in have if r["_dem"]>=med])]:
            res=rd([(r["_m"],anyi(r)) for r in G],10)
            if res: L.append(f"| precinct city Dem share | {lab} | {len(G)} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} |")
    hm=[r for r in frame if r["_mayor"] in ("D","R")]
    for lab,G in [("Dem mayor",[r for r in hm if r["_mayor"]=="D"]),("Rep mayor",[r for r in hm if r["_mayor"]=="R"])]:
        res=rd([(r["_m"],anyi(r)) for r in G],10)
        if res: L.append(f"| mayor party at vote | {lab} | {len(G)} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} |")
    L.append("")
open("analysis/D5_LARGECITY_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
