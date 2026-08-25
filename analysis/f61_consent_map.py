#!/usr/bin/env python3
"""F6.1 — the geography of consent: observed voted share of local new-money
debt by state (tile grid), with entity-class small multiples for the appendix.

Value per state: Σ(voted_sh_par × determined_par) / Σ determined_par over the
national entity panel (all five classes for the main map; per class for the
multiples). Fixed bins, single-hue sequential ramp on white (validated slots).
Writes analysis/fig_consent_map.svg + analysis/F61_MAP_VALUES.md."""
import csv, gzip
from collections import defaultdict

def fl(x):
    try: return float(x)
    except: return None

num=defaultdict(float); den=defaultdict(float); ndocs=defaultdict(int)
numc=defaultdict(float); denc=defaultdict(float)
with gzip.open("analysis/national_entity_panel.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        v=fl(r["voted_sh_par"]); w=fl(r["determined_par"])
        if v is None or not w or w<=0 or not r["state"]: continue
        num[r["state"]]+=v*w; den[r["state"]]+=w
        ndocs[r["state"]]+=int(fl(r["nm_docs"]) or 0)
        numc[(r["state"],r["entity_type"])]+=v*w; denc[(r["state"],r["entity_type"])]+=w
# COVERAGE GATE (retained after the v3 flag fix): a state qualifies only with
# >=50 new-money docs, so no value rides on a handful of documents. On v3 the
# states below the gate are genuinely thin small local sectors (VT/WY/DE/DC/HI,
# 12-40 docs), not extraction gaps.
MIN_DOCS=50
share={s:num[s]/den[s] for s in den if den[s]>0 and ndocs[s]>=MIN_DOCS}
sharec={k:numc[k]/denc[k] for k in denc if denc[k]>0 and ndocs[k[0]]>=MIN_DOCS}

POS={"AK":(0,0),"ME":(11,0),
"WA":(1,1),"ID":(2,1),"MT":(3,1),"ND":(4,1),"MN":(5,1),"WI":(6,1),"MI":(8,1),"NY":(9,1),"VT":(10,1),"NH":(11,1),
"OR":(1,2),"NV":(2,2),"WY":(3,2),"SD":(4,2),"IA":(5,2),"IL":(6,2),"IN":(7,2),"OH":(8,2),"PA":(9,2),"NJ":(10,2),"MA":(11,2),"RI":(12,2),
"CA":(1,3),"UT":(2,3),"CO":(3,3),"NE":(4,3),"MO":(5,3),"KY":(6,3),"WV":(7,3),"VA":(8,3),"MD":(9,3),"DE":(10,3),"CT":(11,3),
"AZ":(2,4),"NM":(3,4),"KS":(4,4),"AR":(5,4),"TN":(6,4),"NC":(7,4),"SC":(8,4),"DC":(9,4),
"OK":(4,5),"LA":(5,5),"MS":(6,5),"AL":(7,5),"GA":(8,5),
"HI":(0,6),"TX":(4,6),"FL":(9,6)}
BINS=[(0.0,"#E8EFF8"),(0.10,"#BCD3EE"),(0.20,"#84ACDD"),(0.35,"#4A7FC7"),(0.50,"#1F4E8F")]
def col(v):
    c=BINS[0][1]
    for lo,cc in BINS:
        if v>=lo: c=cc
    return c
def dark(v): return v>=0.35
INK="#0b0b0b"; SEC="#52514e"
CELL=54; GAP=5
def grid(x0,y0,vals,cell,label_vals):
    out=[]
    for st,(cx,cy) in POS.items():
        x=x0+cx*(cell+GAP*cell/CELL); y=y0+cy*(cell+GAP*cell/CELL)
        v=vals.get(st)
        fill=col(v) if v is not None else "#f0efeb"
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="4" fill="{fill}"/>')
        tcol="#ffffff" if (v is not None and dark(v)) else INK
        if label_vals:
            out.append(f'<text x="{x+cell/2:.0f}" y="{y+cell/2-4:.0f}" font-size="{cell*0.26:.0f}" font-weight="bold" fill="{tcol}" text-anchor="middle">{st}</text>')
            out.append(f'<text x="{x+cell/2:.0f}" y="{y+cell/2+14:.0f}" font-size="{cell*0.22:.0f}" fill="{tcol}" text-anchor="middle">{f"{v:.0%}" if v is not None else "–"}</text>')
        else:
            out.append(f'<text x="{x+cell/2:.0f}" y="{y+cell/2+3:.0f}" font-size="{cell*0.3:.0f}" fill="{tcol}" text-anchor="middle">{st}</text>')
    return out

W,H=810,1015
S=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
   f'<text x="20" y="30" font-size="17" font-weight="bold" fill="{INK}">The geography of consent</text>',
   f'<text x="20" y="50" font-size="12" fill="{SEC}">Share of local new-money debt (2005–25, $-weighted) authorised by the voters, all local government classes</text>']
S+=grid(20,70,share,CELL,True)
# legend
lx=20; ly=70+7*(CELL+GAP)+18
S.append(f'<text x="{lx}" y="{ly}" font-size="11" fill="{SEC}">voted share of determined new-money $:</text>')
labels=["0–10%","10–20%","20–35%","35–50%","50%+"]
for i,(lo,cc) in enumerate(BINS):
    S.append(f'<rect x="{lx+250+i*92}" y="{ly-11}" width="14" height="14" rx="2" fill="{cc}"/>')
    S.append(f'<text x="{lx+268+i*92}" y="{ly}" font-size="11" fill="{SEC}">{labels[i]}</text>')
# small multiples
S.append(f'<text x="20" y="{ly+45}" font-size="13" font-weight="bold" fill="{INK}">By entity class (appendix)</text>')
mini=26
for i,(ent,lab) in enumerate([("school_district","school districts"),("municipal","municipalities"),
                              ("county","counties"),("special_district","special districts")]):
    mx=20+(i%2)*400; my=ly+65+(i//2)*260
    S.append(f'<text x="{mx}" y="{my-6}" font-size="11.5" font-weight="bold" fill="{SEC}">{lab}</text>')
    vals={st:sharec.get((st,ent)) for st in POS}
    S+=grid(mx,my,vals,mini,False)
S.append("</svg>")
open("analysis/fig_consent_map.svg","w").write("\n".join(S))

missing=[st for st in POS if st not in share]
M=["# F6.1 — consent map values (voted share of determined new-money $, 2005–25)\n",
   f"COVERAGE NOTE (v3): the w2_3 finance-flag gap is FIXED (package v3, verified);",
   f"{len(missing)} states remain below the ≥50-doc gate ({', '.join(sorted(missing))}) —",
   "genuinely small local-issuance volumes (12–40 flagged docs), shown missing",
   "rather than as unstable values. Near-zeros elsewhere are REAL (KY 0.1%,",
   "TN 0.5%, PA 1.6%, NY 2.2% on full coverage). Legacy partial-fill states",
   "(MN 79% / MA 72% / MO 85% / MD 87% / ID 85% flag coverage) still map on",
   "substantial doc counts; their completion is queued with the meta session.\n",
   "| state | all classes | schools | municipal | county | special |","|---|--:|--:|--:|--:|--:|"]
for st in sorted(share,key=lambda s:-share[s]):
    def g(e):
        v=sharec.get((st,e)); return f"{v:.1%}" if v is not None else "–"
    M.append(f"| {st} | {share[st]:.1%} | {g('school_district')} | {g('municipal')} | {g('county')} | {g('special_district')} |")
open("analysis/F61_MAP_VALUES.md","w").write("\n".join(M)+"\n")
print(f"states mapped: {len(share)}; wrote fig_consent_map.svg + F61_MAP_VALUES.md")
print("top:", sorted(share.items(),key=lambda kv:-kv[1])[:5])
print("bottom:", sorted(share.items(),key=lambda kv:kv[1])[:5])
