#!/usr/bin/env python3
"""M1 — the menu matrix: which entity types hold which exits (round-2, Tier 1).

National corpus (inputs/corpus/auth_os.csv.gz), NEW-MONEY docs only
(has_new_money & !has_refunding), deduped to one canonical doc per issue
(issue_canonical.csv.gz). For each pol_accountable entity type × state-regime
class (op_referendum_strict from the PRELIMINARY rules panel, go_debt, latest
year — labels only, no estimation): share of new-money dollars (par_effective)
and issue counts by security_pledge_class and auth_mode_final2.

"Authority" CONFLICT FLAG: the instruction lists 'authority' as an entity type;
pol_accountable_type has no such class (authorities fold to their accountable
government). Memo rows use the ISSUER's jurisdiction_class
(housing / health_hospital / utility_district) as the authority proxy.

Exit-menu richness := share of new-money $ authorized council_or_board or
statutory among determined (voter+council+statutory) docs. D4 alignment:
τ recomputed from paper_panel.csv exactly as d4_fork.py (no copied numbers).
Writes analysis/M1_RESULTS.md."""
import csv, gzip
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None

# canonical doc per issue
canon=set()
with gzip.open("inputs/corpus/issue_canonical.csv.gz","rt") as fh:
    for r in csv.DictReader(fh): canon.add(r["canonical_doc_id"])

# rules: (state, entity) -> strict for go_debt, latest codable year
rule={}
for r in csv.DictReader(open("inputs/elections/rules/state_debt_rules.csv")):
    if r["purpose"]=="go_debt" and r["op_codable"]=="1":
        k=(r["state"],r["entity_type"])
        y=int(r["year"])
        if k not in rule or y>rule[k][0]: rule[k]=(y,f(r["op_referendum_strict"]))
E2R={"school_district":"school_district","municipal":"municipality","township":"municipality",
     "county":"county","special_district":"special_district"}
def strict_of(st,ent):
    k=(st,E2R.get(ent,""))
    v=rule.get(k)
    return None if v is None or v[1] is None else int(v[1])

ENTS=["school_district","municipal","township","county","special_district"]
AUTH_JC={"housing","health_hospital","utility_district"}
MODES=["voter","council_or_board","statutory","refunding_no_new_election",""]
MLAB={"voter":"voter","council_or_board":"council","statutory":"statutory",
      "refunding_no_new_election":"refund-auth","":"undetermined"}
SECS=["GO","revenue","lease","special_tax",""]

# cell[(rowkey, regime)] -> {(sec,mode):[n,$]}, plus determined tallies
cell=defaultdict(lambda: defaultdict(lambda:[0,0.0]))
det=defaultdict(lambda: [0.0,0.0])   # rowkey-agg (all regimes): [nonvoted$, determined$]
det_n=defaultdict(lambda: [0,0])
nm_docs=0
with gzip.open("inputs/corpus/auth_os.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        if r["issue_id"] and r["doc_id"] not in canon: continue
        if r["has_new_money"].lower() not in ("true","1"): continue
        if r["has_refunding"].lower() in ("true","1"): continue
        ent=r["pol_accountable_type"]; st=r["state"]
        rows=[]
        if ent in ENTS: rows.append(ent)
        if r["jurisdiction_class"] in AUTH_JC: rows.append("authority-class issuer (memo)")
        if not rows: continue
        nm_docs+=1
        par=f(r["par_effective"]) or 0.0
        sec=r["security_pledge_class"] if r["security_pledge_class"] in SECS else ""
        mode=r["auth_mode_final2"] if r["auth_mode_final2"] in MODES else ""
        sc=strict_of(st,ent)
        reg={1:"referendum-strict",0:"non-strict"}.get(sc,"rule not codable")
        for rk in rows:
            cell[(rk,reg)][(sec,mode)][0]+=1
            cell[(rk,reg)][(sec,mode)][1]+=par
            if mode in ("voter","council_or_board","statutory"):
                det[rk][1]+=par; det_n[rk][1]+=1
                if mode!="voter": det[rk][0]+=par; det_n[rk][0]+=1

L=["# M1 — the menu matrix: entity types × exits (national new-money corpus)\n",
   f"New-money docs (canonical per issue, has_new_money & !has_refunding, typed): **{nm_docs:,}**.",
   "Regime class = `op_referendum_strict` (go_debt, latest codable year) from the",
   "**PRELIMINARY** rules panel — descriptive labels only, no estimation rides on it.",
   "CONFLICT FLAG: 'authority' is not a `pol_accountable_type`; the memo row proxies it",
   "with issuer `jurisdiction_class` ∈ {housing, health_hospital, utility_district}.\n"]

ROWS=ENTS+["authority-class issuer (memo)"]
for rk in ROWS:
    regs=[g for g in ("referendum-strict","non-strict","rule not codable")
          if (rk,g) in cell]
    for reg in regs:
        C=cell[(rk,reg)]
        tot_n=sum(v[0] for v in C.values()); tot_d=sum(v[1] for v in C.values())
        if tot_n<50: continue
        L.append(f"### {rk} · {reg}  (issues {tot_n:,}, new-money ${tot_d/1e9:.1f}B)")
        L.append("| security \\ mode | "+" | ".join(MLAB[m] for m in MODES)+" |")
        L.append("|---|"+"--:|"*len(MODES))
        for sec in SECS:
            slab=sec or "unclassified"
            vals=[]
            for m in MODES:
                n,d=C.get((sec,m),[0,0.0])
                vals.append(f"{d/tot_d:.1%}" if tot_d>0 and d>0 else ("·" if n==0 else "0.0%"))
            if any(v not in ("·",) for v in vals):
                L.append(f"| {slab} | "+" | ".join(vals)+" |")
        L.append("")

L.append("## Exit-menu richness (share of determined new-money $ in non-voted channels)")
L.append("| entity type | non-voted $ share | non-voted issue share | determined $B |")
L.append("|---|--:|--:|--:|")
rich={}
for rk in ROWS:
    nv,dt=det[rk]; nn,dn=det_n[rk]
    if dt>0:
        rich[rk]=nv/dt
        L.append(f"| {rk} | {nv/dt:.1%} | {nn/dn:.1%} | {dt/1e9:.1f} |")
L.append("")

# ---- D4 alignment (recomputed, not copied) ----
rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0
CLS={"schools (school_district)":(lambda r:r["census_type"]=="school_district","school_district"),
     "utilities (special_district)":(lambda r:r["census_type"]=="special_district","special_district"),
     "general-purpose (muni+twp+county)":(lambda r:r["census_type"] in ("municipal","township","county"),None)}
# combined general-purpose richness
gp_nv=sum(det[e][0] for e in ("municipal","township","county"))
gp_dt=sum(det[e][1] for e in ("municipal","township","county"))
L.append("## The fork against the menu (D4 τ recomputed · bw ±10)")
L.append("| class | exit-menu richness (non-voted $ share) | τ GO-issue | z | τ ANY-issue | z |")
L.append("|---|--:|--:|--:|--:|--:|")
for lab,(sel,ent) in CLS.items():
    G=[r for r in S if sel(r)]
    res=rd([(f(r["threshold_centered_margin"]),go(r)) for r in G],10)
    res2=rd([(f(r["threshold_centered_margin"]),f(r["issued_6y"])) for r in G],10)
    rv=rich.get(ent) if ent else (gp_nv/gp_dt if gp_dt>0 else float("nan"))
    L.append(f"| {lab} | {rv:.1%} | {res['tau']:+.3f} | {res['z']:.2f} | {res2['tau']:+.3f} | {res2['z']:.2f} |")
L.append(f"\nRead: schools — the poorest menu ({rich.get('school_district',float('nan')):.1%} non-voted $) — are bound (significant τ,"
         "\nGO ≈ ANY: nothing to reroute to). General-purpose governments — the richest menu —"
         "\nshow no discontinuity at all. Special districts sit between: the largest GO-specific"
         "\nτ, shrinking at ANY-issue as part of the gap reroutes to non-GO channels. The menu"
         "\ncolumn is measured on the national corpus, independent of the RD frame.")
open("analysis/M1_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
