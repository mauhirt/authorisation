#!/usr/bin/env python3
"""D4 — the chargeability fork: schools bind, utilities reroute.

Frame rd_sample ∩ bond_go, split by entity class (the ballot-purpose proxy):
  schools   census_type school_district           (non-chargeable purpose)
  utilities census_type special_district          (TX MUD/WCID etc — chargeable)
  general   municipal + township + county
Per class: RD (bw ±10) on GO issuance, ANY issuance, council share; plus the
re-submission rate among failures (response path). New B3-based outcome:
chargeable share of post-vote window project dollars (docs joined via
cache/b3_doc_flags). Prediction: refusal BINDS schools (drop + re-submit; nothing
chargeable to exit to) but utilities REROUTE (smaller issuance drop, higher
chargeable/NG share persists). Writes analysis/D4_RESULTS.md."""
import csv, gzip, datetime as dt
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None
def pdate(s):
    try: return dt.date.fromisoformat((s or "")[:10])
    except: return None

# doc -> (ch$, nc$)
b3={}
with gzip.open("analysis/cache/b3_doc_flags.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        b3[r["doc_id"]]=(f(r["amt_chargeable"]) or 0.0, f(r["amt_non_chargeable"]) or 0.0)
# unit -> [(date, doc_id)]
iss=defaultdict(list)
with gzip.open("analysis/cache/issuance_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        d=pdate(r["dated_date"])
        if d: iss[(r["pol_accountable_unit_id"] or "")[:9]].append((d,r["doc_id"]))

rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
W6=dt.timedelta(days=2192)
for r in S:
    r["_m"]=f(r["threshold_centered_margin"])
    d=pdate(r["election_date"]); ch=nc=0.0
    if d:
        for dd,doc in iss.get((r["unit_id"] or "")[:9],[]):
            if dt.timedelta(0)<dd-d<=W6 and doc in b3:
                a,b=b3[doc]; ch+=a; nc+=b
    r["_chsh"]=(ch/(ch+nc)) if ch+nc>0 else None

CLS={"schools":lambda r:r["census_type"]=="school_district",
     "utilities (special districts)":lambda r:r["census_type"]=="special_district",
     "general-purpose":lambda r:r["census_type"] in ("municipal","township","county")}
def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0

L=["# D4 — the chargeability fork (rd_sample ∩ bond_go, bw ±10)\n",
   "Entity class proxies ballot purpose: schools = non-chargeable purpose;",
   "special districts (TX MUD/WCID etc.) = chargeable utilities.\n",
   "| class | n | τ GO-issue | z | τ ANY-issue | z | τ council share | z | fail→re-submit ≤4y | window chargeable $ share (mean) |",
   "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
for lab,sel in CLS.items():
    G=[r for r in S if sel(r)]
    r1=rd([(r["_m"],go(r)) for r in G],10)
    r2=rd([(r["_m"],f(r["issued_6y"])) for r in G],10)
    r3=rd([(r["_m"],f(r["council_share_6y"])) for r in G],10)
    fails=[r for r in G if r["passed"]=="0" and r["resubmitted_4y"] in ("0","1")]
    rs=(sum(1 for r in fails if r["resubmitted_4y"]=="1")/len(fails)) if fails else float("nan")
    chs=[r["_chsh"] for r in G if r["_chsh"] is not None]
    mch=(sum(chs)/len(chs)) if chs else float("nan")
    def fmt(x,k): return f"{x[k]:+.3f}" if x else "–"
    def fz(x): return f"{x['z']:.2f}" if x else "–"
    L.append(f"| {lab} | {len(G)} | {fmt(r1,'tau')} | {fz(r1)} | {fmt(r2,'tau')} | {fz(r2)} "
             f"| {fmt(r3,'tau')} | {fz(r3)} | {rs:.1%} | {mch:.1%} |")
# chargeable-share RD within utilities (does refusal shift composition?)
U=[r for r in S if r["census_type"]=="special_district"]
r4=rd([(r["_m"],r["_chsh"]) for r in U],10)
if r4:
    L.append(f"\nWithin utilities: RD on window chargeable-$ share τ={r4['tau']:+.3f} (z={r4['z']:.2f}, n {r4['nL']}/{r4['nR']}).")
open("analysis/D4_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
