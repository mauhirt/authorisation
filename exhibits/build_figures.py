#!/usr/bin/env python3
"""Exhibit stage 3 — figures F1-F5 + A1a/A1b, greyscale-safe SVG.
PDF conversion happens in the Makefile via headless chromium."""
import csv, gzip, math, datetime as dt
from collections import defaultdict
import sys; sys.path.insert(0,"exhibits"); sys.path.insert(0,"analysis")
from exlib import *
from rdlib import rd, rd_rbc

INK="#111111"; GREY="#777777"; LGREY="#cccccc"; FILL="#e8e8e8"
S=rd_frame()
for r in S: r["_m"]=fl(r["threshold_centered_margin"]); r["_any"]=fl(r["issued_6y"])

def svg_open(w,h,title,sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica,Arial,sans-serif">',
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
            f'<text x="18" y="24" font-size="14" font-weight="bold" fill="{INK}">{title}</text>',
            f'<text x="18" y="41" font-size="10.5" fill="{GREY}">{sub}</text>']
def axis(x0,y0,w,h,xt,yt,xl,yl,fmty=lambda v:f"{v:.2f}"):
    out=[f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="{INK}" stroke-width="1"/>',
         f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="{INK}" stroke-width="1"/>']
    for v,px in xt:
        out.append(f'<line x1="{px:.1f}" y1="{y0+h}" x2="{px:.1f}" y2="{y0+h+4}" stroke="{INK}"/>')
        out.append(f'<text x="{px:.1f}" y="{y0+h+16}" font-size="9.5" fill="{INK}" text-anchor="middle">{v}</text>')
    for v,py in yt:
        out.append(f'<line x1="{x0-4}" y1="{py:.1f}" x2="{x0}" y2="{py:.1f}" stroke="{INK}"/>')
        out.append(f'<text x="{x0-7}" y="{py+3:.1f}" font-size="9.5" fill="{INK}" text-anchor="end">{fmty(v)}</text>')
        out.append(f'<line x1="{x0}" y1="{py:.1f}" x2="{x0+w}" y2="{py:.1f}" stroke="{LGREY}" stroke-width="0.6"/>')
    out.append(f'<text x="{x0+w/2}" y="{y0+h+32}" font-size="10.5" fill="{INK}" text-anchor="middle">{xl}</text>')
    out.append(f'<text x="{x0+6}" y="{y0+12}" font-size="9.5" fill="{GREY}">{yl}</text>')
    return out

# ---------- F1 binned RD ----------
def wlin(data,bw):
    """weighted linear fit y = a + b m (triangular weights)."""
    sw=swx=swy=swxx=swxy=0.0
    for m,y in data:
        if y is None or abs(m)>bw or m==0: continue
        w=1-abs(m)/bw
        sw+=w; swx+=w*m; swy+=w*y; swxx+=w*m*m; swxy+=w*m*y
    det=sw*swxx-swx*swx
    a=(swy*swxx-swx*swxy)/det; b=(sw*swxy-swx*swy)/det
    return a,b
bins=defaultdict(lambda:[0,0.0])
for r in S:
    if r["_any"] is None or r["_m"] is None or abs(r["_m"])>10 or r["_m"]==0: continue
    b=math.floor(r["_m"]/0.5)*0.5+0.25
    bins[round(b,2)][0]+=1; bins[round(b,2)][1]+=r["_any"]
W,H=560,360; x0,y0,pw,ph=60,55,470,240
def sx(m): return x0+ (m+10)/20*pw
def sy(v): return y0+ph-(v-0.3)/0.5*ph
Sv=svg_open(W,H,"Issuance at the authorisation threshold",
            "Share with any issuance within six years; 0.5pp bins sized by n; local-linear fits")
Sv+=axis(x0,y0,pw,ph,[(v,sx(v)) for v in (-10,-5,0,5,10)],
         [(v,sy(v)) for v in (0.3,0.4,0.5,0.6,0.7,0.8)],
         "Vote share minus threshold (pp)","share issuing")
Sv.append(f'<line x1="{sx(0)}" y1="{y0}" x2="{sx(0)}" y2="{y0+ph}" stroke="{INK}" stroke-width="1" stroke-dasharray="4,3"/>')
mx=max(n for n,_ in bins.values())
for b,(n,s) in sorted(bins.items()):
    rr=2+4*math.sqrt(n/mx)
    Sv.append(f'<circle cx="{sx(b):.1f}" cy="{sy(s/n):.1f}" r="{rr:.1f}" fill="{GREY}" fill-opacity="0.75"/>')
dl=[(r["_m"],r["_any"]) for r in S if r["_m"] is not None and r["_m"]<0]
dr=[(r["_m"],r["_any"]) for r in S if r["_m"] is not None and r["_m"]>0]
aL,bL=wlin(dl,10); aR,bR=wlin(dr,10)
Sv.append(f'<line x1="{sx(-10)}" y1="{sy(aL+bL*-10):.1f}" x2="{sx(-0.01)}" y2="{sy(aL):.1f}" stroke="{INK}" stroke-width="2"/>')
Sv.append(f'<line x1="{sx(0.01)}" y1="{sy(aR):.1f}" x2="{sx(10)}" y2="{sy(aR+bR*10):.1f}" stroke="{INK}" stroke-width="2"/>')
row=rdrow([(r["_m"],r["_any"]) for r in S])
Sv.append(f'<text x="{sx(0)+8}" y="{y0+16}" font-size="11" fill="{INK}">RBC τ = {row["rbc"]:+.3f} [{row["lo"]:+.3f}, {row["hi"]:+.3f}]</text>')
Sv.append("</svg>")
open(f"{OUT}/F1_rd.svg","w").write("\n".join(Sv))
write_csv("F1_rd_bins",["bin_mid","n","share"],[[b,n,f"{s/n:.4f}"] for b,(n,s) in sorted(bins.items())])

# ---------- F2 event study ----------
ev=[]
for k,col in [(-2,"ev_m2"),(-1,"ev_m1"),(0,"ev_0"),(1,"ev_p1"),(2,"ev_p2"),(3,"ev_p3"),(4,"ev_p4"),(5,"ev_p5")]:
    row=rdrow([(r["_m"],fl(r[col])) for r in S])
    ev.append([k,row["rbc"],row["lo"],row["hi"],row["conv"]])
write_csv("F2_event_study",["k","rbc","ci_lo","ci_hi","conventional"],ev)
W,H=560,340; x0,y0,pw,ph=60,55,470,220
def sxk(k): return x0+(k+2.5)/8*pw
lo=min(e[2] for e in ev); hi=max(e[3] for e in ev)
def syv(v): return y0+ph-(v-lo)/(hi-lo)*ph
Sv=svg_open(W,H,"Event study: issuance by year relative to the vote",
            "RBC coefficients with robust 95% CIs; outcome = any new-money issue in relative year k")
Sv+=axis(x0,y0,pw,ph,[(k,sxk(k)) for k,_,_,_,_ in ev],
         [(round(v,2),syv(v)) for v in (0.0,0.1,0.2)],
         "Years relative to the vote","coefficient")
Sv.append(f'<line x1="{x0}" y1="{syv(0):.1f}" x2="{x0+pw}" y2="{syv(0):.1f}" stroke="{INK}" stroke-width="0.8"/>')
for k,b,l,h_,c in ev:
    x=sxk(k)
    Sv.append(f'<line x1="{x:.1f}" y1="{syv(l):.1f}" x2="{x:.1f}" y2="{syv(h_):.1f}" stroke="{INK}" stroke-width="1.4"/>')
    Sv.append(f'<circle cx="{x:.1f}" cy="{syv(b):.1f}" r="4" fill="{INK}"/>')
Sv.append(f'<text x="{sxk(0)+8:.1f}" y="{syv(ev[2][1])-8:.1f}" font-size="11" fill="{INK}">τ₀ = {ev[2][1]:+.3f}</text>')
Sv.append(f'<text x="{x0+6}" y="{y0+ph-6}" font-size="9.5" fill="{GREY}">event indicators exist for k = −2..+5 (build note in manifest)</text>')
Sv.append("</svg>")
open(f"{OUT}/F2_event_study.svg","w").write("\n".join(Sv))

# ---------- F3 cumulative wedge ----------
iss=defaultdict(list); seen=set()
with gzip.open("analysis/cache/issuance_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        d=pdate(r["dated_date"])
        if not d: continue
        nm=(r.get("has_new_money","").lower() in ("true","1")) and (r.get("has_refunding","").lower() not in ("true","1"))
        if not nm: continue
        key=r["issue_id"] or r["doc_id"]
        if key in seen: continue
        seen.add(key)
        iss[(r["pol_accountable_unit_id"] or "")[:9]].append((d,fl(r["par_effective"]) or 0.0))
KS=list(range(-2,7))
curves={}
for side,sel in [("passed",lambda r:0<r["_m"]<=5),("failed",lambda r:-5<=r["_m"]<0)]:
    G=[r for r in S if sel(r) and pdate(r["election_date"]) and r["unit_id"]]
    A=[]
    for k in KS:
        hit=0
        for r in G:
            d=pdate(r["election_date"])
            if any(-2<= (dd-d).days/365.25 < k+1 for dd,_ in iss.get(r["unit_id"][:9],[])): hit+=1
        A.append(hit/len(G))
    curves[side]=A
write_csv("F3_wedge",["k","passed","failed"],[[k,f"{curves['passed'][i]:.4f}",f"{curves['failed'][i]:.4f}"] for i,k in enumerate(KS)])
W,H=560,340; x0,y0,pw,ph=60,55,470,220
def sxw(k): return x0+(k+2)/8*pw
def syw(v): return y0+ph-v/0.7*ph
Sv=svg_open(W,H,"The cumulative wedge",
            "Cumulative share with any new-money issue since k = −2, |margin| ≤ 5; shaded area = the wedge")
Sv+=axis(x0,y0,pw,ph,[(k,sxw(k)) for k in KS],[(v,syw(v)) for v in (0.0,0.2,0.4,0.6)],
         "Years since the vote","cumulative share")
poly=" ".join(f"{sxw(k):.1f},{syw(curves['passed'][i]):.1f}" for i,k in enumerate(KS))
poly+=" "+" ".join(f"{sxw(k):.1f},{syw(curves['failed'][i]):.1f}" for i,k in reversed(list(enumerate(KS))))
Sv.append(f'<polygon points="{poly}" fill="{FILL}"/>')
for side,dash in (("passed",""),("failed","6,4")):
    pts=" ".join(f"{sxw(k):.1f},{syw(curves[side][i]):.1f}" for i,k in enumerate(KS))
    da=(' stroke-dasharray="'+dash+'"') if dash else ""
    Sv.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2"{da}/>')
Sv.append(f'<line x1="{sxw(0)}" y1="{y0}" x2="{sxw(0)}" y2="{y0+ph}" stroke="{GREY}" stroke-width="1" stroke-dasharray="3,3"/>')
Sv.append(f'<text x="{sxw(5.4):.1f}" y="{syw(curves["passed"][-1])-6:.1f}" font-size="10" fill="{INK}">barely passed (solid)</text>')
Sv.append(f'<text x="{sxw(5.4):.1f}" y="{syw(curves["failed"][-1])+14:.1f}" font-size="10" fill="{INK}">barely failed (dashed)</text>')
Sv.append(f'<text x="{x0+8}" y="{y0+28}" font-size="10.5" fill="{INK}">median delay ≈ 0.8 years; never-issued gap +10.0pp at k = +6</text>')
Sv.append("</svg>")
open(f"{OUT}/F3_wedge.svg","w").write("\n".join(Sv))

# ---------- F4 consent map (greyscale) ----------
src=open("analysis/fig_consent_map.svg").read()
GREYMAP={"#E8EFF8":"#f0f0f0","#BCD3EE":"#cfcfcf","#84ACDD":"#a3a3a3","#4A7FC7":"#6f6f6f","#1F4E8F":"#3a3a3a"}
for a,b in GREYMAP.items(): src=src.replace(a,b)
open(f"{OUT}/F4_consent_map.svg","w").write(src)

# ---------- F5 running-variable density by state ----------
W,H=560,430
Sv=svg_open(W,H,"Density of the vote margin, by state",
            "0.5pp bins within ±10pp of the threshold; the Texas discreteness is visible at the smallest electorates")
states=[("TX","Texas"),("CA","California"),("WI","Wisconsin"),("LA","Louisiana"),("NC","North Carolina")]
pw,ph=150,110
for i,(st,lab) in enumerate(states):
    ox=30+(i%3)*175; oy=60+(i//3)*160
    G=[r["_m"] for r in S if r["state"]==st and r["_m"] is not None and abs(r["_m"])<=10 and r["_m"]!=0]
    bins=defaultdict(int)
    for m in G: bins[math.floor(m/0.5)*0.5]+=1
    mx=max(bins.values()) if bins else 1
    Sv.append(f'<text x="{ox}" y="{oy-6}" font-size="10.5" font-weight="bold" fill="{INK}">{lab} (n={len(G):,})</text>')
    Sv.append(f'<line x1="{ox}" y1="{oy+ph}" x2="{ox+pw}" y2="{oy+ph}" stroke="{INK}" stroke-width="0.8"/>')
    for b,n in bins.items():
        x=ox+(b+10)/20*pw; w=pw/40
        h_=n/mx*ph
        Sv.append(f'<rect x="{x:.1f}" y="{oy+ph-h_:.1f}" width="{w:.1f}" height="{h_:.1f}" fill="{GREY}"/>')
    cx=ox+0.5*pw
    Sv.append(f'<line x1="{cx}" y1="{oy}" x2="{cx}" y2="{oy+ph}" stroke="{INK}" stroke-width="1" stroke-dasharray="3,2"/>')
Sv.append(f'<text x="30" y="{H-18}" font-size="9.5" fill="{GREY}">McCrary log-density: pooled +0.140 (z 2.58); TX +0.206 (z 2.71); all other states n.s. Donut estimates (Table A1) are stable to larger.</text>')
Sv.append("</svg>")
open(f"{OUT}/F5_density.svg","w").write("\n".join(Sv))

# ---------- A1a / A1b small figures ----------
for name,csvf,title,xl in [("A1a_horizons","A1_horizons","Effect by horizon","horizon (years)"),
                           ("A1b_bandwidth","A1_bandwidth_curve","Bandwidth sensitivity","bandwidth h (pp)")]:
    rows=list(csv.DictReader(open(f"{OUT}/{csvf}.csv")))
    xs=[float(list(r.values())[0]) for r in rows]
    b=[float(r["rbc"]) for r in rows]; l=[float(r["ci_lo"]) for r in rows]; h_=[float(r["ci_hi"]) for r in rows]
    c=[float(r["conventional"]) for r in rows]
    W2,H2=430,270; x0,y0,pw,ph=55,45,350,180
    lo2,hi2=min(l),max(h_)
    def sxx(x): return x0+(x-xs[0])/(xs[-1]-xs[0])*pw
    def syy(v): return y0+ph-(v-lo2)/(hi2-lo2)*ph
    Sv=svg_open(W2,H2,title,"RBC (solid, with robust CI band) and conventional (dashed)")
    Sv+=axis(x0,y0,pw,ph,[(int(x),sxx(x)) for x in xs][::max(1,len(xs)//7)],
             [(round(v,2),syy(v)) for v in (0.0,0.1,0.2)],xl,"coefficient")
    band=" ".join(f"{sxx(x):.1f},{syy(l[i]):.1f}" for i,x in enumerate(xs))
    band+=" "+" ".join(f"{sxx(x):.1f},{syy(h_[i]):.1f}" for i,x in reversed(list(enumerate(xs))))
    Sv.append(f'<polygon points="{band}" fill="{FILL}"/>')
    Sv.append(f'<line x1="{x0}" y1="{syy(0):.1f}" x2="{x0+pw}" y2="{syy(0):.1f}" stroke="{INK}" stroke-width="0.8"/>')
    Sv.append('<polyline points="'+" ".join(f"{sxx(x):.1f},{syy(b[i]):.1f}" for i,x in enumerate(xs))+f'" fill="none" stroke="{INK}" stroke-width="2"/>')
    Sv.append('<polyline points="'+" ".join(f"{sxx(x):.1f},{syy(c[i]):.1f}" for i,x in enumerate(xs))+f'" fill="none" stroke="{INK}" stroke-width="1.4" stroke-dasharray="6,4"/>')
    Sv.append("</svg>")
    open(f"{OUT}/{name}.svg","w").write("\n".join(Sv))
print("stage 3 done")
