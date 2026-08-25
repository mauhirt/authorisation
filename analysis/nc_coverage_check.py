#!/usr/bin/env python3
"""Round 4 item 1 — nc_share selection check.

Question: is B3 classified-amount-line coverage (the base of every composition
result) balanced across rule regimes? Coverage per corpus-active unit
(nm_docs>0) = has any classified project $ (nc_share_project non-blank).
Reported by state and by regime (strict/lax, muni-and-county general-purpose
focus and all classes), unit- and dollar-weighted (weight = nm_par).

If unbalanced (>5pp regime gap on either weighting), COUNT-BASED versions of
the composition results are produced alongside:
  - B3 channel sorting by LINE COUNTS (n_chargeable / n_non_chargeable)
  - N2-style general-purpose WLS on the count-based nc share (same controls,
    region FE, state clusters; weight = classified line count)
Writes analysis/NC_COVERAGE_RESULTS.md."""
import csv, gzip, math
from collections import defaultdict

def fl(x):
    try: return float(x)
    except: return None

units={}
with gzip.open("analysis/national_entity_panel.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        if r["nm_docs"]!="" and int(float(r["nm_docs"]))>0:
            units[r["gid"]]=r

def covtab(sel):
    agg=defaultdict(lambda:[0,0,0.0,0.0])   # key -> [n units, n covered, par, par covered]
    for r in units.values():
        if not sel(r): continue
        k=r["rule_strict"] if r["rule_strict"]!="" else "not codable"
        par=fl(r["nm_par"]) or 0.0
        a=agg[k]; a[0]+=1; a[2]+=par
        if r["nc_share_project"]!="":
            a[1]+=1; a[3]+=par
    return agg

L=["# nc_share selection check (round 4, item 1)\n",
   "Coverage = corpus-active unit (nm_docs>0) with any B3-classified project $.",
   "Weighted coverage weights units by nm_par. Regime = op_referendum_strict",
   "(PRELIMINARY labels).\n","## By regime",
   "| sample | regime | units | unit coverage | $ coverage |","|---|---|--:|--:|--:|"]
gaps={}
for lab,sel in [("all classes",lambda r:True),
                ("general-purpose (muni+county)",lambda r:r["entity_type"] in ("municipal","county")),
                ("schools",lambda r:r["entity_type"]=="school_district")]:
    agg=covtab(sel); row={}
    for k in ("1","0","not codable"):
        if k in agg:
            n,c,p,pc=agg[k]
            row[k]=(c/n if n else 0, pc/p if p>0 else 0)
            L.append(f"| {lab} | {'strict' if k=='1' else ('non-strict' if k=='0' else k)} | {n:,} | {c/n:.1%} | {pc/p:.1%} |")
    if "1" in row and "0" in row:
        gaps[lab]=(abs(row["1"][0]-row["0"][0]), abs(row["1"][1]-row["0"][1]))
L.append("")
unbal=any(max(g)>0.05 for g in gaps.values())
L.append(f"Regime gaps (unit, $): "+"; ".join(f"{k}: {g[0]:.1%}/{g[1]:.1%}" for k,g in gaps.items())
         +f" → **{'UNBALANCED (>5pp) — count-based versions produced below' if unbal else 'BALANCED (≤5pp) — appendix sentence suffices'}**.\n")

# by state (compact: only states with >=20 active units)
L+=["## By state (≥20 corpus-active units)","| state | units | unit cov | $ cov |","|---|--:|--:|--:|"]
st=defaultdict(lambda:[0,0,0.0,0.0])
for r in units.values():
    par=fl(r["nm_par"]) or 0.0
    a=st[r["state"]]; a[0]+=1; a[2]+=par
    if r["nc_share_project"]!="": a[1]+=1; a[3]+=par
for s in sorted(st,key=lambda s:-st[s][0]):
    n,c,p,pc=st[s]
    if n>=20: L.append(f"| {s} | {n:,} | {c/n:.1%} | {pc/p:.1%} |")
L.append("")

if unbal:
    # ---- count-based B3 channel sorting ----
    ch_n=defaultdict(lambda:[0,0])
    with gzip.open("analysis/cache/b3_doc_flags.csv.gz","rt") as fh:
        for r in csv.DictReader(fh):
            m=r["auth_mode_final2"] or "unknown"
            ch_n[m][0]+=int(float(r["n_chargeable"] or 0))
            ch_n[m][1]+=int(float(r["n_non_chargeable"] or 0))
    L+=["## Count-based B3 channel sorting (classified LINES, not $)",
        "| auth mode | ch lines | nc lines | chargeable share (count) |","|---|--:|--:|--:|"]
    for m in ("voter","council_or_board","statutory","refunding_no_new_election","unknown"):
        a,b=ch_n.get(m,[0,0])
        if a+b>0: L.append(f"| {m} | {a:,} | {b:,} | {a/(a+b):.1%} |")
    L.append("")
    # ---- count-based unit nc share + GP WLS ----
    cnt=defaultdict(lambda:[0,0])
    with gzip.open("analysis/cache/b3_doc_flags.csv.gz","rt") as fh:
        for r in csv.DictReader(fh):
            g=(r["pol_accountable_unit_id"] or "")[:9]
            if g in units:
                cnt[g][0]+=int(float(r["n_chargeable"] or 0))
                cnt[g][1]+=int(float(r["n_non_chargeable"] or 0))
    REGION={"CT":"NE","ME":"NE","MA":"NE","NH":"NE","RI":"NE","VT":"NE","NJ":"NE","NY":"NE","PA":"NE",
    "IL":"MW","IN":"MW","MI":"MW","OH":"MW","WI":"MW","IA":"MW","KS":"MW","MN":"MW","MO":"MW","NE":"MW","ND":"MW","SD":"MW",
    "DE":"S","FL":"S","GA":"S","MD":"S","NC":"S","SC":"S","VA":"S","DC":"S","WV":"S","AL":"S","KY":"S","MS":"S","TN":"S","AR":"S","LA":"S","OK":"S","TX":"S",
    "AZ":"W","CO":"W","ID":"W","MT":"W","NV":"W","NM":"W","UT":"W","WY":"W","AK":"W","CA":"W","HI":"W","OR":"W","WA":"W"}
    def linsolve(A,b):
        n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
        for c in range(n):
            p=max(range(c,n),key=lambda r:abs(M[r][c]))
            if abs(M[p][c])<1e-10: M[p][c]=1e-10
            M[c],M[p]=M[p],M[c]
            for r in range(n):
                if r!=c:
                    f2=M[r][c]/M[c][c]
                    for k in range(c,n+1): M[r][k]-=f2*M[c][k]
        return [M[i][n]/M[i][i] for i in range(n)]
    obs=[]
    for g,(a,b) in cnt.items():
        r=units[g]
        if a+b==0 or r["rule_strict"]=="" or r["entity_type"] not in ("municipal","county"): continue
        pop=fl(r["pop"]); ho=fl(r["acs_homeown"]); s65=fl(r["acs_share65"])
        fr=fl(r["acs_frac"]); mi=fl(r["acs_medinc"]); dem=fl(r["county_dem2p_2020"])
        if not pop or pop<=0 or None in (ho,s65,fr,dem) or not mi or mi<=0: continue
        x=dict(const=1.0,strict=float(r["rule_strict"]),lnsize=math.log(pop),
               homeown=ho,share65=s65,frac=fr,lnminc=math.log(mi),dem=dem)
        rg=REGION.get(r["state"],"W")
        for k in ("MW","S","W"): x[f"rg_{k}"]=1.0 if rg==k else 0.0
        obs.append((x, b/(a+b), float(a+b), r["state"]))
    names=["const","strict","lnsize","homeown","share65","frac","lnminc","dem","rg_MW","rg_S","rg_W"]
    p=len(names); XtX=[[0.0]*p for _ in range(p)]; Xty=[0.0]*p
    for x,y,w,cl in obs:
        v=[x[n] for n in names]
        for i in range(p):
            wv=w*v[i]; Xty[i]+=wv*y
            for j in range(i,p): XtX[i][j]+=wv*v[j]
    for i in range(p):
        for j in range(i): XtX[i][j]=XtX[j][i]
    beta=linsolve(XtX,Xty)
    inv=[]
    for c in range(p):
        e=[0.0]*p; e[c]=1.0
        inv.append(linsolve([row[:] for row in XtX],e))
    inv=[[inv[j][i] for j in range(p)] for i in range(p)]
    G=defaultdict(lambda:[0.0]*p)
    for x,y,w,cl in obs:
        v=[x[n] for n in names]; e=y-sum(bb*vv for bb,vv in zip(beta,v))
        g_=G[cl]
        for i in range(p): g_[i]+=w*v[i]*e
    meat=[[0.0]*p for _ in range(p)]
    for g_ in G.values():
        for i in range(p):
            for j in range(p): meat[i][j]+=g_[i]*g_[j]
    k=names.index("strict"); nc_=len(G); dof=nc_/(nc_-1)
    tmp=[sum(inv[k][a]*meat[a][j] for a in range(p)) for j in range(p)]
    se=math.sqrt(max(dof*sum(tmp[a]*inv[a][k] for a in range(p)),0))
    L+=["## Count-based N2 (general-purpose): nc line share ~ strict + controls",
        f"β(strict) = **{beta[k]:+.4f}**, state-cluster SE {se:.4f}, t {beta[k]/se:.2f}, "
        f"n {len(obs):,}, clusters {nc_}.",
        "(Dollar-based v3 counterpart: −0.087, t −1.61.) The text may cite whichever",
        "the coverage table justifies; both appear in the appendix.",""]
open("analysis/NC_COVERAGE_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
