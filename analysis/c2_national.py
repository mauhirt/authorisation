#!/usr/bin/env python3
"""C2 — H2 national test: non-chargeable share of new-money project dollars vs
referendum-rule stringency, state + entity-type FE, clustered by state.

Data: cache/b3_doc_flags.csv.gz (doc grain) -> unit-year outcome
      nc_share = amt_nc/(amt_ch+amt_nc) over classified project dollars;
      entity type from the Census GID type digit (unit9[2]);
      treatment from rules/state_debt_rules.csv at (state, entity, go_debt, year):
      op_referendum_strict (headline), op_ordinal and op_threshold_num (variants).
Estimator: cells at (state, entity, year) grain (treatment's own grain), weighted
by classified dollars; two-way FE via dummies; cluster-robust (state) SEs.
CAVEATS carried: rules PRELIMINARY (verified=0); doc state = issuer state; only
labeled lines with printed dollars enter. Writes analysis/C2_RESULTS.md."""
import csv, gzip
from collections import defaultdict

def f(x):
    try: return float(x)
    except: return None
TYPE_DIGIT={"1":"county","2":"municipality","3":"municipality","4":"special_district","5":"school_district"}

# rules: (state, entity, year) -> row
rule={}
for r in csv.DictReader(open("inputs/elections/rules/state_debt_rules.csv")):
    if r["purpose"]=="go_debt":
        rule[(r["state"],r["entity_type"],r["year"])]=r
def get_rule(st,ent,yr):
    for y in (yr,"2024","2020","2015"):
        k=(st,ent,y)
        if k in rule: return rule[k]
    return None

# unit-year aggregation of classified project dollars
cell=defaultdict(lambda:[0.0,0.0])   # (state, entity, year) -> [ch$, nc$]
with gzip.open("analysis/cache/b3_doc_flags.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        u=(r["pol_accountable_unit_id"] or "")
        if len(u)<3: continue
        ent=TYPE_DIGIT.get(u[2])
        if not ent: continue
        ch=f(r["amt_chargeable"]) or 0.0; nc=f(r["amt_non_chargeable"]) or 0.0
        if ch+nc<=0: continue
        cell[(r["state"],ent,r["year"])][0]+=ch
        cell[(r["state"],ent,r["year"])][1]+=nc

# build cell rows with treatment
rows=[]
for (st,ent,yr),(ch,nc) in cell.items():
    ru=get_rule(st,ent,yr)
    if not ru or ru.get("op_codable")!="1": continue
    strict=f(ru.get("op_referendum_strict")); ordn=f(ru.get("op_ordinal")); thr=f(ru.get("op_threshold_num"))
    if strict is None: continue
    rows.append(dict(st=st,ent=ent,yr=yr,w=ch+nc,y=nc/(ch+nc),strict=strict,ordn=ordn,thr=thr))
print(f"cells: {len(rows)}  (states {len(set(r['st'] for r in rows))}, years {len(set(r['yr'] for r in rows))})")

def linsolve(A,b):
    n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(M[r][c]))
        if abs(M[p][c])<1e-12: M[p][c]=1e-12
        M[c],M[p]=M[p],M[c]
        for r in range(n):
            if r!=c:
                fkt=M[r][c]/M[c][c]
                for k in range(c,n+1): M[r][k]-=fkt*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

def wls_fe(rows,tvar):
    R=[r for r in rows if r.get(tvar) is not None]
    states=sorted(set(r["st"] for r in R)); ents=sorted(set(r["ent"] for r in R))
    sidx={s:i for i,s in enumerate(states[1:])}; eidx={e:i for i,e in enumerate(ents[1:])}
    p=1+1+len(sidx)+len(eidx)   # intercept + treatment + FEs
    def xrow(r):
        x=[1.0,r[tvar]]+[0.0]*(len(sidx)+len(eidx))
        if r["st"] in sidx: x[2+sidx[r["st"]]]=1.0
        if r["ent"] in eidx: x[2+len(sidx)+eidx[r["ent"]]]=1.0
        return x
    XtX=[[0.0]*p for _ in range(p)]; Xty=[0.0]*p
    for r in R:
        x=xrow(r); w=r["w"]
        for i in range(p):
            wxi=w*x[i]
            Xty[i]+=wxi*r["y"]
            for j in range(i,p): XtX[i][j]+=wxi*x[j]
    for i in range(p):
        for j in range(i): XtX[i][j]=XtX[j][i]
    beta=linsolve(XtX,Xty)
    # cluster-robust (state) sandwich
    XtXinv_col=None
    # invert XtX via solving p systems (only need full inverse row for var of beta[1]; compute full inverse)
    inv=[]
    for c in range(p):
        e=[0.0]*p; e[c]=1.0
        inv.append(linsolve([row[:] for row in XtX],e))
    inv=[[inv[j][i] for j in range(p)] for i in range(p)]  # transpose (symmetric anyway)
    meat=[[0.0]*p for _ in range(p)]
    bystate=defaultdict(list)
    for r in R: bystate[r["st"]].append(r)
    for s,rs in bystate.items():
        g=[0.0]*p
        for r in rs:
            x=xrow(r); e=r["y"]-sum(b*xi for b,xi in zip(beta,x))
            for i in range(p): g[i]+=r["w"]*x[i]*e
        for i in range(p):
            for j in range(p): meat[i][j]+=g[i]*g[j]
    # V = inv * meat * inv ; need V[1][1]
    tmp=[sum(inv[1][k]*meat[k][j] for k in range(p)) for j in range(p)]
    v11=sum(tmp[k]*inv[k][1] for k in range(p))
    G=len(bystate); dof=G/(G-1)
    se=(dof*v11)**0.5
    return beta[1],se,len(R),G

L=["# C2 — non-chargeable share vs referendum-rule stringency (H2, national)\n",
   f"Cells (state × entity × year, treatment grain): weighted by classified project $;",
   "state + entity-type FE; SEs clustered by state. Rules panel PRELIMINARY (verified=0).\n",
   "| treatment | β | SE (cluster) | t | cells | states |","|---|--:|--:|--:|--:|--:|"]
for tvar,lab in [("strict","op_referendum_strict (0/1)"),("ordn","op_ordinal (hurdle intensity)"),
                 ("thr","op_threshold_num (pass share)")]:
    b,se,n,G=wls_fe(rows,tvar)
    L.append(f"| {lab} | {b:+.4f} | {se:.4f} | {b/se:.2f} | {n} | {G} |")
gp=[r for r in rows if r["ent"] in ("municipality","county")]
b,se,n,G=wls_fe(gp,"strict")
L.append(f"| strict — GENERAL-PURPOSE only (muni+county; schools ~100% nc are degenerate) | {b:+.4f} | {se:.4f} | {b/se:.2f} | {n} | {G} |")
# descriptive: mean nc share by strict, within entity
L+=["\n## Descriptive: $-weighted non-chargeable share by rule, per entity type",
    "| entity | strict=1 | strict=0 |","|---|--:|--:|"]
for ent in ("school_district","municipality","county","special_district"):
    def m(sv):
        rr=[r for r in rows if r["ent"]==ent and r["strict"]==sv]
        W=sum(r["w"] for r in rr)
        return f"{sum(r['w']*r['y'] for r in rr)/W:.1%}" if W>0 else "–"
    L.append(f"| {ent} | {m(1.0)} | {m(0.0)} |")
open("analysis/C2_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
