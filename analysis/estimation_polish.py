#!/usr/bin/env python3
"""Estimation polish (map item 9). Frame: rd_sample ∩ bond_go, outcome GO
issuance ≤6y unless stated.
 1. IK (2012) MSE-optimal bandwidth (triangular C_K=3.4375; full pilot steps),
    headline τ re-estimated at h_IK.
 2. Cluster-robust SEs (unit; county) for the local-linear estimator, vs HC0.
 3. Lee bounds vs crosswalk selection: pooled close-window trim p=0.0252
    (selection diagnostics, muni_universe pin); binary-outcome sharp bounds by
    trimming the over-represented (right) side's intercept.
 4. Randomization inference: |margin|<=2 window, 5000 sign permutations
    (seed 42), diff-in-means p-value.
 5. McCrary by state (bin 0.5, h=10) — decomposes the pooled density result.
 6. LA diagnostic: base rates + pooled estimate excluding LA.
Writes analysis/POLISH_RESULTS.md."""
import csv, math, random
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd, wls_side

rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
def f(x):
    try: return float(x)
    except: return None
S=[r for r in rows if str(r["rd_sample"])=="1" and r["purpose_class"]=="bond_go"
   and f(r["threshold_centered_margin"]) is not None]
for r in S: r["_m"]=f(r["threshold_centered_margin"])
def go(r):
    if r["issued_6y"]=="": return None
    gs=f(r["go_share_6y"]); return 1.0 if (r["issued_6y"]=="1" and gs and gs>0) else 0.0
D=[(r["_m"],go(r),r["unit_id"][:9],r["unit_id"][:2]+r["unit_id"][3:6]) for r in S if go(r) is not None and r["_m"]!=0]
X=[d[0] for d in D]; N=len(D)
L=["# Estimation polish (map item 9) — headline: GO issuance ≤6y\n",f"Estimation sample n={N}.\n"]

def polyfit(xs,ys,deg,jump=False):
    """OLS: y = a0 + (a_T*T if jump) + sum a_j x^j; returns coefs list."""
    p=deg+1+(1 if jump else 0)
    def xr(x):
        v=[1.0]+([1.0 if x>=0 else 0.0] if jump else [])
        for j in range(1,deg+1): v.append(x**j)
        return v
    A=[[0.0]*p for _ in range(p)]; b=[0.0]*p
    for x,y in zip(xs,ys):
        v=xr(x)
        for i in range(p):
            b[i]+=v[i]*y
            for j in range(i,p): A[i][j]+=v[i]*v[j]
    for i in range(p):
        for j in range(i): A[i][j]=A[j][i]
    M=[row[:]+[b[i]] for i,row in enumerate(A)]
    n=p
    for c in range(n):
        piv=max(range(c,n),key=lambda r_: abs(M[r_][c]))
        M[c],M[piv]=M[piv],M[c]
        if abs(M[c][c])<1e-12: M[c][c]=1e-12
        for r_ in range(n):
            if r_!=c:
                fk=M[r_][c]/M[c][c]
                for k in range(c,n+1): M[r_][k]-=fk*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

# ---------- 1. IK bandwidth ----------
mean=sum(X)/N; Sx=math.sqrt(sum((x-mean)**2 for x in X)/(N-1))
h1=1.84*Sx*N**(-0.2)
left1=[(x,y) for x,y,_,_ in D if -h1<=x<0]; right1=[(x,y) for x,y,_,_ in D if 0<=x<h1]
fc=(len(left1)+len(right1))/(2*N*h1)
def var_of(g):
    if len(g)<2: return 0.0
    m=sum(y for _,y in g)/len(g); return sum((y-m)**2 for _,y in g)/(len(g)-1)
sig2=(var_of(left1)*len(left1)+var_of(right1)*len(right1))/(len(left1)+len(right1))
med_l=sorted(x for x,*_ in D if x<0)[len([x for x,*_ in D if x<0])//2]
med_r=sorted(x for x,*_ in D if x>0)[len([x for x,*_ in D if x>0])//2]
sub=[(x,y) for x,y,_,_ in D if med_l<=x<=med_r]
co=polyfit([x for x,_ in sub],[y for _,y in sub],3,jump=True)
m3=6*co[4]
Nl=sum(1 for x,*_ in D if x<0); Nr=N-Nl
h2p=3.56*(sig2/(fc*max(m3*m3,0.01)))**(1/7)*Nr**(-1/7)
h2m=3.56*(sig2/(fc*max(m3*m3,0.01)))**(1/7)*Nl**(-1/7)
rt=[(x,y) for x,y,_,_ in D if 0<=x<=h2p]; lt=[(x,y) for x,y,_,_ in D if -h2m<=x<0]
m2p=2*polyfit([x for x,_ in rt],[y for _,y in rt],2)[2] if len(rt)>10 else 0.0
m2m=2*polyfit([x for x,_ in lt],[y for _,y in lt],2)[2] if len(lt)>10 else 0.0
rp=2160*sig2/(max(len(rt),2)*h2p**4); rm=2160*sig2/(max(len(lt),2)*h2m**4)
hIK=3.4375*(sig2/(fc*((m2p-m2m)**2+rp+rm)))**0.2*N**(-0.2)
pairs=[(x,y) for x,y,_,_ in D]
resIK=rd(pairs,hIK); res10=rd(pairs,10)
L+=["## 1 · IK MSE-optimal bandwidth",
    f"- pilots: h1={h1:.2f}, f̂(0)={fc:.4f}, σ̂²={sig2:.4f}, m3={m3:.4g}, "
    f"h2=({h2m:.2f},{h2p:.2f}), m2=({m2m:.4g},{m2p:.4g})",
    f"- **h_IK = {hIK:.2f}pp**; τ(h_IK) = **{resIK['tau']:+.3f} (SE {resIK['se']:.3f}, z {resIK['z']:.2f})**, "
    f"n={resIK['nL']}/{resIK['nR']}  |  τ(±10) = {res10['tau']:+.3f} (z {res10['z']:.2f})",""]

# ---------- 2. cluster-robust SEs ----------
def rd_cluster(D,bw,cidx):
    """local-linear both sides; cluster SE on alpha difference."""
    out={}
    for side in (-1,1):
        pts=[(x,y,c[cidx]) for x,y,*c in [(x,y,u,co_) for x,y,u,co_ in D] if (x<0)==(side<0) and 0<abs(x)<=bw]
        S0=S1=S2=Sy=Smy=0.0
        for x,y,_ in pts:
            w=1-abs(x)/bw; S0+=w; S1+=w*x; S2+=w*x*x; Sy+=w*y; Smy+=w*x*y
        det=S0*S2-S1*S1
        a=(S2*Sy-S1*Smy)/det; b=(S0*Smy-S1*Sy)/det
        inv00,inv01=S2/det,-S1/det
        gsc=defaultdict(lambda:[0.0,0.0])
        for x,y,c in pts:
            w=1-abs(x)/bw; e=y-a-b*x
            gsc[c][0]+=w*e; gsc[c][1]+=w*x*e
        va=0.0
        for g0,g1 in gsc.values():
            s=inv00*g0+inv01*g1; va+=s*s
        G=len(gsc)
        out[side]=(a,va*G/(G-1) if G>1 else va,G,len(pts))
    tau=out[1][0]-out[-1][0]; se=math.sqrt(out[1][1]+out[-1][1])
    return tau,se,out[1][2]+out[-1][2]
D4c=[(x,y,u,co_) for x,y,u,co_ in D]
t_u,se_u,G_u=rd_cluster(D4c,10,0)   # cluster by unit
t_c,se_c,G_c=rd_cluster(D4c,10,1)   # cluster by county
L+=["## 2 · Clustered SEs (bw ±10)","| variance | τ | SE | z | clusters |","|---|--:|--:|--:|--:|",
    f"| HC0 (baseline) | {res10['tau']:+.3f} | {res10['se']:.3f} | {res10['z']:.2f} | – |",
    f"| cluster: unit | {t_u:+.3f} | {se_u:.3f} | {t_u/se_u:.2f} | {G_u} |",
    f"| cluster: county | {t_c:+.3f} | {se_c:.3f} | {t_c/se_c:.2f} | {G_c} |",""]

# ---------- 3. Lee bounds ----------
p=0.0252
aR=res10["aR"]; aL=res10["aL"]
lo=(aR-p)/(1-p)-aL; hi=aR/(1-p)-aL
L+=["## 3 · Lee bounds vs crosswalk selection (pooled close-window trim p=2.52%)",
    f"τ(±10) point {res10['tau']:+.3f}; **sharp bounds [{lo:+.3f}, {hi:+.3f}]** "
    "(binary outcome; over-represented right side trimmed toward 1s / 0s).",
    "Zero-selection benchmark states (MA/NC, p=0) reported in RD_RESULTS.md.",""]

# ---------- 4. randomization inference ----------
random.seed(42)
W=[(x,y) for x,y,_,_ in D if abs(x)<=2]
obs=sum(y for x,y in W if x>0)/len([1 for x,y in W if x>0])-sum(y for x,y in W if x<0)/len([1 for x,y in W if x<0])
ys=[y for _,y in W]; nR_=len([1 for x,_ in W if x>0])
cnt=0; B=5000
for _ in range(B):
    random.shuffle(ys)
    d=sum(ys[:nR_])/nR_-sum(ys[nR_:])/(len(ys)-nR_)
    if abs(d)>=abs(obs): cnt+=1
L+=["## 4 · Randomization inference (|margin|≤2, 5000 permutations, seed 42)",
    f"observed diff-in-means {obs:+.3f}; **RI p-value = {cnt/B:.4f}** (n={len(W)})",""]

# ---------- 5. McCrary by state ----------
L+=["## 5 · McCrary log-density by state (bin 0.5, h=10)","| state | θ | SE | z |","|---|--:|--:|--:|"]
def mccrary(M,h=10,BIN=0.5):
    n=len(M)
    def fit(side):
        c=defaultdict(int)
        for m in M:
            ok=(side<0 and -h<=m<0) or (side>0 and 0<m<=h)
            if ok: c[math.floor(m/BIN)]+=1
        pts=[((b+0.5)*BIN,cnt/(n*BIN)) for b,cnt in sorted(c.items())]
        S0=S1=S2=Sy=Smy=0.0
        for x,y in pts:
            w=1-abs(x)/h
            if w<=0: continue
            S0+=w; S1+=w*x; S2+=w*x*x; Sy+=w*y; Smy+=w*x*y
        det=S0*S2-S1*S1
        if det<=0: return None,None
        a=(S2*Sy-S1*Smy)/det; b_=(S0*Smy-S1*Sy)/det
        inv00,inv01=S2/det,-S1/det
        B00=B01=B11=0.0
        for x,y in pts:
            w=1-abs(x)/h
            if w<=0: continue
            e=y-a-b_*x; we2=(w*e)**2
            B00+=we2; B01+=we2*x; B11+=we2*x*x
        return a,inv00*inv00*B00+2*inv00*inv01*B01+inv01*inv01*B11
    fl_,vl=fit(-1); fr_,vr=fit(1)
    if not fl_ or not fr_ or fl_<=0 or fr_<=0: return None
    th=math.log(fr_)-math.log(fl_); se=math.sqrt(vl/fl_**2+vr/fr_**2)
    return th,se
for st in ["CA","TX","WI","LA","NC","POOLED"]:
    M=[r["_m"] for r in S if (st=="POOLED" or r["state"]==st) and r["_m"]!=0]
    resm=mccrary(M)
    if resm: L.append(f"| {st} | {resm[0]:+.3f} | {resm[1]:.3f} | {resm[0]/resm[1]:.2f} |")
L.append("")

# ---------- 6. LA diagnostic ----------
la=[r for r in S if r["state"]=="LA"]
laI=[go(r) for r in la if go(r) is not None]
exLA=[(r["_m"],go(r)) for r in S if r["state"]!="LA"]
resx=rd(exLA,10)
L+=["## 6 · LA diagnostic",
    f"LA frame n={len(la)}; GO-issue base rate {sum(laI)/len(laI):.1%} (parish-fold grain: "
    "measures fold to the parish, so the outcome mixes many measures' issuance).",
    f"Pooled τ excluding LA (bw10): **{resx['tau']:+.3f} (z {resx['z']:.2f})** vs {res10['tau']:+.3f} with LA — "
    "LA's negative cell does not drive the headline; treat LA as fold-grain caveat, not signal.",""]
open("analysis/POLISH_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
