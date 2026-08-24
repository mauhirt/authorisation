#!/usr/bin/env python3
"""N1–N5 — the national regression suite on the 50-state entity panel.

All specs: WLS, cluster-robust (STATE) SEs, Census-region FE, entity dummies
where pooled. RULES ARE PRELIMINARY PASS-1: every rule coefficient is a
FIRST-STAGE / DESCRIPTIVE association, not a causal estimate — the causal
versions are HELD for the human pass-2. Townships EXCLUDED from headline rows
(proxy rule; town-meeting reversal documented in NATIONAL_ENTITY_RESULTS.md),
shown as a robustness row. Each block ends with MISSING/TO-DO flags.

  N1  first stage: voted $ share (determined) ~ rule_strict + controls
  N2  composition: GO security share; non-chargeable project share
  N3  extensive margin: any corpus new-money 2005–25 (LPM);
      ln(1+GFD LTD issued 2005–23 per capita) with no-report→0 assumption
  N4  TEL × rule (big-city subpanel, n≈570)
  N5  moderators: rule × homeownership; rule × county Dem share
Controls: ln size (pop; enrollment for schools), homeownership, 65+ share,
fractionalization, ln median income, county Dem 2020.
Writes analysis/N_RESULTS.md."""
import csv, gzip, math
from collections import defaultdict

def fl(x):
    try: return float(x)
    except: return None

REGION={"CT":"NE","ME":"NE","MA":"NE","NH":"NE","RI":"NE","VT":"NE","NJ":"NE","NY":"NE","PA":"NE",
"IL":"MW","IN":"MW","MI":"MW","OH":"MW","WI":"MW","IA":"MW","KS":"MW","MN":"MW","MO":"MW","NE":"MW","ND":"MW","SD":"MW",
"DE":"S","FL":"S","GA":"S","MD":"S","NC":"S","SC":"S","VA":"S","DC":"S","WV":"S","AL":"S","KY":"S","MS":"S","TN":"S","AR":"S","LA":"S","OK":"S","TX":"S",
"AZ":"W","CO":"W","ID":"W","MT":"W","NV":"W","NM":"W","UT":"W","WY":"W","AK":"W","CA":"W","HI":"W","OR":"W","WA":"W"}

rows=[]
with gzip.open("analysis/national_entity_panel.csv.gz","rt") as fh:
    for r in csv.DictReader(fh): rows.append(r)

def size_of(r):
    p=fl(r["pop"]); e=fl(r["enrollment"])
    if r["entity_type"]=="school_district": return e if e and e>0 else p
    if p and p>0: return p
    if e and e>0: return e
    if r["entity_type"]=="special_district":
        v=fl(r["total_rev_k"])          # specials carry no Population in GFD:
        return v if v and v>0 else None  # ln fiscal size proxy (FLAGGED in notes)
    return None
def controls(r):
    """returns dict of control values or None if any missing"""
    s=size_of(r)
    ho,s65,fr=fl(r["acs_homeown"]),fl(r["acs_share65"]),fl(r["acs_frac"])
    mi=fl(r["acs_medinc"]); dem=fl(r["county_dem2p_2020"])
    if not s or s<=0 or None in (ho,s65,fr,dem) or not mi or mi<=0: return None
    return dict(lnsize=math.log(s),homeown=ho,share65=s65,frac=fr,
                lnminc=math.log(mi),dem=dem)

def linsolve(A,b):
    n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(M[r][c]))
        if abs(M[p][c])<1e-10: M[p][c]=1e-10
        M[c],M[p]=M[p],M[c]
        for r in range(n):
            if r!=c:
                f=M[r][c]/M[c][c]
                for k in range(c,n+1): M[r][k]-=f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

def reg(obs, xnames, report):
    """obs: list of (xdict, y, w, cluster). Returns {name:(b,se,t)} for report names."""
    p=len(xnames)
    XtX=[[0.0]*p for _ in range(p)]; Xty=[0.0]*p
    for xd,y,w,cl in obs:
        x=[xd.get(n,0.0) for n in xnames]
        for i in range(p):
            wxi=w*x[i]; Xty[i]+=wxi*y
            for j in range(i,p): XtX[i][j]+=wxi*x[j]
    for i in range(p):
        for j in range(i): XtX[i][j]=XtX[j][i]
    beta=linsolve(XtX,Xty)
    inv=[]
    for c in range(p):
        e=[0.0]*p; e[c]=1.0
        inv.append(linsolve([row[:] for row in XtX],e))
    inv=[[inv[j][i] for j in range(p)] for i in range(p)]
    G=defaultdict(lambda:[0.0]*p)
    for xd,y,w,cl in obs:
        x=[xd.get(n,0.0) for n in xnames]
        e=y-sum(b*xi for b,xi in zip(beta,x))
        g=G[cl]
        for i in range(p): g[i]+=w*x[i]*e
    meat=[[0.0]*p for _ in range(p)]
    for g in G.values():
        for i in range(p):
            for j in range(p): meat[i][j]+=g[i]*g[j]
    nc=len(G); dof=nc/(nc-1) if nc>1 else 1.0
    out={}
    for name in report:
        k=xnames.index(name)
        tmp=[sum(inv[k][a]*meat[a][j] for a in range(p)) for j in range(p)]
        v=dof*sum(tmp[a]*inv[a][k] for a in range(p))
        se=math.sqrt(max(v,0.0))
        out[name]=(beta[k],se,(beta[k]/se if se>0 else 0.0))
    return out,len(obs),nc

def xbase(r,c,ents,pooled):
    x=dict(const=1.0,strict=float(r["rule_strict"]),**c)
    reg_=REGION.get(r["state"],"W")
    for rg in ("MW","S","W"): x[f"rg_{rg}"]=1.0 if reg_==rg else 0.0
    if pooled:
        for e in ents[1:]: x[f"e_{e}"]=1.0 if r["entity_type"]==e else 0.0
    return x
BASE=["const","strict","lnsize","homeown","share65","frac","lnminc","dem","rg_MW","rg_S","rg_W"]
ENTS=["school_district","municipal","county","special_district"]
POOL_X=BASE+[f"e_{e}" for e in ENTS[1:]]

L=["# N1–N5 — the national regression suite (entity panel)\n",
   "WLS, state-clustered SEs, region FE; controls: ln size, homeownership, 65+,",
   "fractionalization, ln median income, county Dem 2020. **Rule coefficients are",
   "FIRST-STAGE/DESCRIPTIVE (rules PRELIMINARY pass-1); causal readings HELD.**",
   "Townships excluded from headlines (proxy rule), shown as robustness.\n"]

def block(title, specs, notes):
    global L
    L.append(f"## {title}")
    L.append("| spec | sample | β(strict) | SE (state-cluster) | t | n | clusters |")
    L.append("|---|---|--:|--:|--:|--:|--:|")
    for lab,obs,xn in specs:
        if len(obs)<50:
            L.append(f"| {lab} | – | – | – | – | {len(obs)} | – |"); continue
        out,n,ncl=reg(obs,xn,["strict"])
        b,se,t=out["strict"]
        L.append(f"| {lab} | | {b:+.4f} | {se:.4f} | {t:.2f} | {n:,} | {ncl} |")
    L+= ["", "**MISSING / TO-DO:** "+notes, ""]

# ---- N1 first stage ----
def mk(sel,yk,wk,pooled=True,extra=None):
    obs=[]
    for r in rows:
        if r["rule_strict"]=="" or not sel(r): continue
        y=fl(r[yk]); w=fl(r[wk]) if wk else 1.0
        if y is None or not w or w<=0: continue
        c=controls(r)
        if c is None: continue
        x=xbase(r,c,ENTS,pooled)
        if extra: extra(r,x)
        obs.append((x,y,w,r["state"]))
    return obs
NOTWN=lambda r: r["entity_type"]!="township"
specs=[("pooled (4 classes, entity dummies)",mk(NOTWN,"voted_sh_par","determined_par"),POOL_X)]
for e in ENTS:
    specs.append((e,mk(lambda r,e=e:r["entity_type"]==e,"voted_sh_par","determined_par",pooled=False),BASE))
specs.append(("+townships (proxy rule) robustness",mk(lambda r:True,"voted_sh_par","determined_par"),POOL_X))
block("N1 · First stage: OS-evidenced voted $ share ~ rule_strict",specs,
 "rules pass-2 (all cells); TOWNSHIP rule column (proxy breaks in town-meeting states); "
 "rule TIME variation not coded (latest-year rule vs 2005–25 outcomes — reform years unmodeled); "
 "state-level TEL/debt-limit controls missing (only big-city TEL exists); "
 "issuer-vs-accountable-state mismatch for cross-border conduits; "
 "SPECIAL DISTRICTS: no GFD Population — ln size = ln total revenue (fiscal-size proxy), "
 "so their lnsize is not comparable to other classes' population control.")

# ---- N2 composition ----
specs=[("GO security share (pooled)",mk(NOTWN,"sec_go_sh","nm_par"),POOL_X),
       ("GO security share (general-purpose: muni+county)",mk(lambda r:r["entity_type"] in ("municipal","county"),"sec_go_sh","nm_par"),BASE),
       ("non-chargeable share (pooled)",mk(NOTWN,"nc_share_project","nm_par"),POOL_X),
       ("non-chargeable share (general-purpose)",mk(lambda r:r["entity_type"] in ("municipal","county"),"nc_share_project","nm_par"),BASE)]
block("N2 · Composition/substitution: security & purpose ~ rule_strict",specs,
 "nc-share weight is nm_par (classified-$ base not stored in panel — add amt_classified column); "
 "schools ~100% nc are degenerate for the nc spec (pooled row diluted — general-purpose row is the object); "
 "C2's cell-grain result (−0.162, t −1.83) is the FE-panel cousin; both HELD on pass-2.")

# ---- N3 extensive margin ----
def mkext():
    obs=[]
    for r in rows:
        if r["rule_strict"]=="" or r["entity_type"]=="township": continue
        c=controls(r)
        if c is None: continue
        y=1.0 if r["nm_docs"]!="" else 0.0
        obs.append((xbase(r,c,ENTS,True),y,1.0,r["state"]))
    return obs
def mkgfd():
    obs=[]
    for r in rows:
        if r["rule_strict"]=="" or r["entity_type"]=="township": continue
        c=controls(r); s=size_of(r)
        if c is None or not s: continue
        v=fl(r["gfd_ltd_iss_0523_k"]) or 0.0   # no-report -> 0 ASSUMPTION (flagged)
        y=math.log1p(max(0.0,v)*1000/s)
        obs.append((xbase(r,c,ENTS,True),y,1.0,r["state"]))
    return obs
block("N3 · Extensive margin & survey totals",
      [("any corpus new-money 2005–25 (LPM)",mkext(),POOL_X),
       ("ln(1+GFD LTD issued 2005–23 p.c.)",mkgfd(),POOL_X)],
 "GFD no-report→0 assumption (non-response vs true zero unseparated — needs GFD "
 "sample-flag pass); corpus truncated at 2005 (EMMA era); levels cross-section = "
 "selection into existence of districts not modeled (unit birth/death); population "
 "denominators for specials are weak (county-service-area problem).")

# ---- N4 TEL x rule (big-city subpanel) ----
def mktel(yk,wk):
    obs=[]
    for r in rows:
        if r["rule_strict"]=="" or r["tel_stringency"]=="" or r["entity_type"]!="municipal": continue
        y=fl(r[yk]); w=fl(r[wk]) if wk else 1.0
        te=fl(r["tel_stringency"]); c=controls(r)
        if y is None or not w or w<=0 or te is None or c is None: continue
        x=xbase(r,c,ENTS,False)
        x["tel"]=te/100.0; x["strictXtel"]=x["strict"]*te/100.0
        obs.append((x,y,w,r["state"]))
    return obs
L.append("## N4 · TEL × rule (big-city subpanel, municipals)")
L.append("| outcome | β(strict) | β(tel) | β(strict×tel) | SE(s×t) | t | n | clusters |")
L.append("|---|--:|--:|--:|--:|--:|--:|--:|")
for lab,yk,wk in [("non-chargeable share","nc_share_project","nm_par"),
                  ("GO security share","sec_go_sh","nm_par"),
                  ("voted $ share","voted_sh_par","determined_par")]:
    obs=mktel(yk,wk)
    if len(obs)<50: L.append(f"| {lab} | – | – | – | – | – | {len(obs)} | – |"); continue
    out,n,ncl=reg(obs,BASE+["tel","strictXtel"],["strict","tel","strictXtel"])
    b1,_,_=out["strict"]; b2,_,_=out["tel"]; b3,se3,t3=out["strictXtel"]
    L.append(f"| {lab} | {b1:+.3f} | {b2:+.3f} | {b3:+.3f} | {se3:.3f} | {t3:.2f} | {n} | {ncl} |")
L+=["","**MISSING / TO-DO:** TEL exists only for ~570 big cities (need a state-level "
    "TEL panel for the full universe); TEL stringency is one 2013-vintage index "
    "(no time variation); big-city sample = the exit-rich class where D4 predicts "
    "weak rule effects — power-limited by design.",""]

# ---- N5 moderators ----
L.append("## N5 · Moderators: who the rule binds for (national first stage)")
L.append("| interaction | β(strict) | β(interaction) | SE | t | n | clusters |")
L.append("|---|--:|--:|--:|--:|--:|--:|")
for lab,var in [("strict × homeownership (centered)","homeown"),
                ("strict × county Dem share (centered)","dem")]:
    obs=[]
    vals=[fl(r["acs_homeown" if var=="homeown" else "county_dem2p_2020"]) for r in rows
          if r["rule_strict"]!="" and r["entity_type"]!="township"]
    vals=[v for v in vals if v is not None]
    mu=sum(vals)/len(vals)
    for r in rows:
        if r["rule_strict"]=="" or r["entity_type"]=="township": continue
        y=fl(r["voted_sh_par"]); w=fl(r["determined_par"]); c=controls(r)
        if y is None or not w or w<=0 or c is None: continue
        x=xbase(r,c,ENTS,True)
        x["inter"]=x["strict"]*(c[var]-mu)
        obs.append((x,y,w,r["state"]))
    out,n,ncl=reg(obs,POOL_X+["inter"],["strict","inter"])
    b1,_,_=out["strict"]; b2,se2,t2=out["inter"]
    L.append(f"| {lab} | {b1:+.3f} | {b2:+.3f} | {se2:.3f} | {t2:.2f} | {n:,} | {ncl} |")
L+=["","**MISSING / TO-DO:** moderators at COUNTY grain for schools/specials "
    "(SD-grain national requires extending the SAIPE/ACS-SD bridge to 50 states); "
    "homeownership here moderates the CHANNEL (first stage), not the RD issuance "
    "effect — the causal freeholder test remains the 9-state ACS_RESULTS one; "
    "county Dem is 2020 only (no panel).",""]
open("analysis/N_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
