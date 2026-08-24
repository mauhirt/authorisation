#!/usr/bin/env python3
"""D5 moderators from the municipal-analysis externals:
 1. PARTISANSHIP: county Dem two-party presidential share (MEDSL countypres,
    mode TOTAL), latest presidential year strictly before the vote; attached via
    FIPS state+county (GFD); RD split at the within-frame median.
 2. BOND BANK: has_bond_bank (state grain). CAUTION: among our 5 RD states this
    is a STATE GROUPING (composition listed) -- descriptive, not causal; theory
    link = substitution infrastructure (prediction: weaker binding where a state
    bond bank eases rerouting). Split on GO issuance + council share.
Frame: rd_sample ∩ bond_go, bw ±10. Writes analysis/D5_EXTERNAL_RESULTS.md."""
import csv, gzip
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None

# county Dem two-party share by (fips5, pres_year)
votes=defaultdict(lambda: [0.0,0.0])
for r in csv.DictReader(open("inputs/external_municipal_analysis/countypres_2000-2024.csv")):
    if r["office"]!="US PRESIDENT" or r.get("mode","TOTAL") not in ("TOTAL","TOTAL VOTES"): continue
    cf=f(r["county_fips"])
    if cf is None: continue
    key=(f"{int(cf):05d}",int(r["year"]))
    v=f(r["candidatevotes"]) or 0.0
    if r["party"]=="DEMOCRAT": votes[key][0]+=v
    elif r["party"]=="REPUBLICAN": votes[key][1]+=v
dem={k:(d/(d+g) if d+g>0 else None) for k,(d,g) in votes.items()}
# unit -> fips5 (state+county) via GFD
u2f={}
with gzip.open("analysis/cache/gfd_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        st=(r["FIPS_Code_State"] or "").strip().zfill(2); ct=(r["FIPS_County"] or "").strip().zfill(3)
        if st!="00" and ct!="000": u2f[r["GOVSid"].strip()]=st+ct
# bond banks
bb={r["state_abb"]:r["has_bond_bank"]=="1" for r in csv.DictReader(open("inputs/external_municipal_analysis/state_bond_banks.csv"))}

rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
PRES=[2000,2004,2008,2012,2016,2020,2024]
n_dem=0
for r in S:
    r["_m"]=f(r["threshold_centered_margin"]); r["_dem"]=None
    vy=(r["election_date"] or "")[:4]
    fp=u2f.get((r["unit_id"] or "")[:9])
    if vy.isdigit() and fp:
        prior=[p for p in PRES if p<int(vy)]
        if prior:
            r["_dem"]=dem.get((fp,prior[-1]))
            if r["_dem"] is not None: n_dem+=1
def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0

L=["# D5 external moderators — partisanship (MEDSL) & bond banks\n",
   f"Frame {len(S)}; county Dem share attached to {n_dem} ({n_dem/len(S):.1%}).\n",
   "## 1 · County presidential partisanship (Dem two-party share, pre-vote)",
   "| subgroup | n | τ GO-issue | SE | z |","|---|--:|--:|--:|--:|"]
have=[r for r in S if r["_dem"] is not None]
vals=sorted(r["_dem"] for r in have); med=vals[len(vals)//2]
for lab,G in [(f"Dem share < median ({med:.3f})",[r for r in have if r["_dem"]<med]),
              ("Dem share ≥ median",[r for r in have if r["_dem"]>=med])]:
    res=rd([(r["_m"],go(r)) for r in G],10)
    if res: L.append(f"| {lab} | {len(G)} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} |")
# terciles for shape
have.sort(key=lambda r:r["_dem"]); k=len(have)//3
for lab,G in [("tercile 1 (most Republican)",have[:k]),("tercile 2",have[k:2*k]),("tercile 3 (most Democratic)",have[2*k:])]:
    res=rd([(r["_m"],go(r)) for r in G],10)
    if res: L.append(f"| {lab} | {len(G)} | {res['tau']:+.3f} | {res['se']:.3f} | {res['z']:.2f} |")
L.append("")
L+=["## 2 · State bond bank (substitution infrastructure) — STATE GROUPING, descriptive",
    "| group (states) | n | τ GO-issue | z | τ council share | z |","|---|--:|--:|--:|--:|--:|"]
for lab,sel in [("bond bank",lambda r: bb.get(r["state"],False)),("no bond bank",lambda r: not bb.get(r["state"],False))]:
    G=[r for r in S if sel(r)]
    sts=sorted(set(r["state"] for r in G))
    r1=rd([(r["_m"],go(r)) for r in G],10)
    r2=rd([(r["_m"],f(r["council_share_6y"])) for r in G],10)
    if r1: L.append(f"| {lab} ({'/'.join(sts)}) | {len(G)} | {r1['tau']:+.3f} | {r1['z']:.2f} | "
                    f"{r2['tau']:+.3f} | {r2['z']:.2f} |" if r2 else f"| {lab} ({'/'.join(sts)}) | {len(G)} | {r1['tau']:+.3f} | {r1['z']:.2f} | – | – |")
open("analysis/D5_EXTERNAL_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
