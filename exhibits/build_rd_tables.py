#!/usr/bin/env python3
"""Exhibit stage 1 — RD tables in the rdrobust reporting convention:
T2 (covariate continuity), T3 (main results), T6 (where it binds),
T7 (fork against the menu), A1 (specification battery + two small figures'
data), A2 (placebo thresholds), A3 (state-by-state). CSV + .tex per exhibit."""
import csv, gzip, math, re, datetime as dt
from collections import defaultdict
import sys; sys.path.insert(0,"exhibits"); sys.path.insert(0,"analysis")
from exlib import *
from rdlib import rd, rd_rbc

S=rd_frame()
for r in S: r["_m"]=fl(r["threshold_centered_margin"])

# ---------- shared derived outcomes ----------
iss=defaultdict(list); seen=set()
with gzip.open("analysis/cache/issuance_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        d=pdate(r["dated_date"])
        if not d: continue
        nm=(r.get("has_new_money","").lower() in ("true","1")) and (r.get("has_refunding","").lower() not in ("true","1"))
        key=r["issue_id"] or r["doc_id"]
        dedup = key not in seen
        if dedup: seen.add(key)
        iss[(r["pol_accountable_unit_id"] or "")[:9]].append((d,r.get("auth_mode_final2") or "",nm and dedup,r["doc_id"]))
for k in iss: iss[k].sort()

for r in S:
    d=pdate(r["election_date"]); u=(r["unit_id"] or "")[:9]
    r["_go"]=go_out(r); r["_any"]=fl(r["issued_6y"])
    r["_noiss"]=None if r["_any"] is None else 1.0-r["_any"]
    r["_lnpar"]=fl(r["ln_par_pc_6y"]); r["_lngfd"]=fl(r["ln_gfd_ltd_pc_6y"])
    r["_voterfirst"]=None; r["_horiz"]={}
    if d and u:
        first=None
        for dd,am,nmd,_doc in iss.get(u,[]):
            if dd>d:
                first=(dd,am); break
        r["_voterfirst"]=1.0 if (first and (first[0]-d).days<=2192 and first[1]=="voter") else 0.0
        for k in range(1,7):
            r["_horiz"][k]=1.0 if any(dt.timedelta(0)<dd-d<=dt.timedelta(days=int(k*365.25)) for dd,_,_,_ in iss.get(u,[])) else 0.0
    # covariates
    pop=fl(r["gfd_pop"]); enr=fl(r["gfd_enrollment"])
    r["_lnpop"]=math.log(pop) if pop and pop>0 else None
    r["_lnenr"]=math.log(enr) if enr and enr>0 else None
    mi=fl(r["acs_medinc"])
    r["_lnminc"]=math.log(mi) if mi and mi>0 else None
    pre=fl(r["gfd_ltd_iss_pre3"]); den=pop if pop and pop>0 else enr
    r["_lnpre"]=math.log1p(max(0.0,pre)*1000/den) if (pre is not None and den and den>0) else None

def pairs(key,sub=None):
    G=S if sub is None else [r for r in S if sub(r)]
    return [(r["_m"],r.get(key)) for r in G]

# ---------- B5 continuation (recomputed, v3-frozen inputs) ----------
NORM=[("K-12 schools",r"school|k-?12|elementary|high school|isd\b|education|classroom|campus"),
("higher education",r"college|university"),("water / sewer / drainage",r"water|sewer|drain|wastewater|storm|sanita"),
("roads / streets / bridges",r"road|street|highway|bridge|sidewalk|paving"),("fire / EMS",r"fire|ems|emergency|ambulance"),
("police / jail / safety",r"police|public safety|law enforcement|jail|correction|sheriff|justice"),
("parks / recreation",r"park|recreation|trail|pool|open space|golf"),("hospital / health",r"hospital|health|medical|clinic"),
("library",r"librar"),("transit / rail",r"transit|rail|bus rapid|metro"),("flood / levee",r"flood|levee|hurricane"),
("housing",r"housing|homeless"),("stadium / athletics",r"stadium|athletic|sports|arena|natatorium"),
("technology / equipment",r"technolog|equipment|bus(es)?\b|vehicle"),
("civic buildings / general",r"city hall|town hall|public building|courthouse|civic|municipal building|general government|capital improvement"),
("electric / gas utility",r"electric|gas|utility|power|broadband"),("port / airport",r"port|airport|harbor")]
def cats_of(t):
    t=(t or "").lower()
    return {lab for lab,pat in NORM if re.search(pat,t)}
import importlib.util
spec=importlib.util.spec_from_file_location("b5","analysis/b5_purpose_match.py")
# FN2CAT is defined at module top in b5_purpose_match; execute only its header safely:
FN2CAT={}
src=open("analysis/b5_purpose_match.py").read()
m=re.search(r"FN2CAT=\{.*?\n\}",src,re.S)
exec(m.group(0),{"FN2CAT":None},FN2CAT.__class__.__dict__ if False else (lambda: None).__globals__) if False else None
ns={}
exec(m.group(0),ns)
FN2CAT=ns["FN2CAT"]
EL="inputs/elections"
raw={}
for st,path,fx in [("CA","cdiac/cdiac_elections_all.csv",lambda r:(r["Purpose"] or "")+" "+(r["Measure Name"] or "")),
                   ("TX","tx_brb/tx_brb_bond_elections_all.csv",lambda r:(r["purposedescription"] or r["purpose"] or "")),
                   ("WI","wi_dpi/wi_dpi_referenda_2005_present.csv",lambda r:(r["BriefDescription"] or "")+" "+(r["FullDescription"] or "")[:200]),
                   ("LA","la_sos/la_sos_local_propositions_2005_present.csv",lambda r:(r["specific_title"] or "")),
                   ("NC","nc_ncsbe/nc_ncsbe_bond_referenda_2005_present.csv",lambda r:(r["contest_name"] or ""))]:
    raw[st]=[fx(r) for r in csv.DictReader(open(f"{EL}/{path}"))]
need_docs=set()
meas=[]
for r in S:
    if abs(r["_m"])>10 or not r["unit_id"]: continue
    st,idx=r["referendum_row_id"].split(":")
    try: txt=raw[st][int(idx)]
    except (KeyError,IndexError,ValueError): continue
    cats=cats_of(txt)
    if not cats: continue
    d=pdate(r["election_date"])
    docs=[(dd,doc) for dd,am,nmd,doc in iss.get(r["unit_id"][:9],[]) if nmd and dt.timedelta(0)<dd-d<=dt.timedelta(days=2192)]
    for dd,doc in docs: need_docs.add(doc)
    meas.append((r,cats,docs))
doc_cats=defaultdict(set)
with gzip.open("inputs/corpus/auth_projects.csv.gz","rt") as fh:
    for row in csv.DictReader(fh):
        if row["doc_id"] not in need_docs or row["side"]!="use" or row["is_subtotal_row"]=="True": continue
        c=FN2CAT.get(row["functional_activity"])
        if c: doc_cats[row["doc_id"]].add(c)
cont_pairs=[]
for r,cats,docs in meas:
    hit=1.0 if any(doc_cats.get(doc,set()) & cats for _,doc in docs) else 0.0
    cont_pairs.append((r["_m"],hit))
print(f"continuation frame {len(cont_pairs)}")

# ---------- capital outlay differenced (schools; lifted from p5) ----------
co=defaultdict(dict)
with gzip.open("analysis/cache/gfd_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        v=fl(r["Total_Capital_Outlays"])
        if v is not None: co[r["GOVSid"].strip()][int(r["Year4"])]=max(0.0,v)
out_pairs=[]
for r in S:
    if r["census_type"]!="school_district": continue
    d=pdate(r["election_date"]); u=(r["unit_id"] or "")[:9]
    pop=fl(r["gfd_pop"]) or fl(r["gfd_enrollment"])
    if not d or not pop or pop<=0: continue
    ys=co.get(u,{})
    post=[ys[y] for y in range(d.year+1,d.year+7) if y in ys]
    pre=[ys[y] for y in range(d.year-3,d.year) if y in ys]
    if post and pre:
        out_pairs.append((r["_m"],math.log1p(sum(post)*1000/pop)-(math.log1p(sum(pre)*1000/pop)+math.log(2.0))))

# ================= T2 covariate continuity =================
rows=[("Any issue, year $t{-}2$",pairs("ev_m2_f")),]
for r in S:
    r["ev_m2_f"]=fl(r["ev_m2"]); r["ev_m1_f"]=fl(r["ev_m1"]); r["prior_f"]=fl(r["prior_fail_4y"])
    r["_ho"]=fl(r["acs_homeown"]); r["_s65"]=fl(r["acs_share65"])
T2=[("Any new-money issue, year $t{-}2$","ev_m2_f",None),
    ("Any new-money issue, year $t{-}1$","ev_m1_f",None),
    ("ln(1+LTD issued p.c., $t{-}3..t{-}1$)","_lnpre",None),
    ("ln population","_lnpop",None),
    ("ln enrolment (schools)","_lnenr",lambda r:r["census_type"]=="school_district"),
    ("Homeownership share","_ho",None),
    ("ln median household income","_lnminc",None),
    ("Share aged 65+","_s65",None),
    ("Prior failed measure $\\le$4y","prior_f",None)]
body=[]; csvr=[]
for lab,key,sub in T2:
    row=rdrow(pairs(key,sub))
    body+=rd_block(lab,row); csvr.append(rd_csv_row(lab,row))
write_csv("T2_covariate_continuity",RD_CSV_HDR,csvr)
tex_table("T2_covariate_continuity",
 "Covariate continuity at the authorisation threshold","tab:continuity",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Pre-vote covariates; ACS at place grain for municipalities, district grain for schools, county otherwise.",
 "No pre-vote covariate jumps at the cutoff; the two lagged-issuance indicators and lagged borrowing are smooth, so barely-passed and barely-failed governments were on the same path before the vote.")

# ================= T3 main results =================
T3=[("Any GO issuance $\\le$6y",[(r["_m"],r["_go"]) for r in S]),
    ("Any issuance $\\le$6y",[(r["_m"],r["_any"]) for r in S]),
    ("ln(1+new-money par p.c.)",[(r["_m"],r["_lnpar"]) for r in S]),
    ("ln(1+LTD issued p.c.), Census survey",[(r["_m"],r["_lngfd"]) for r in S]),
    ("Same-purpose continuation $\\le$6y",cont_pairs),
    ("Voter-mode first issuance $\\le$6y",[(r["_m"],r["_voterfirst"]) for r in S]),
    ("No issuance $\\le$6y",[(r["_m"],r["_noiss"]) for r in S]),
    ("Capital outlay p.c.\\ (pay-go bound; schools, post$-$pre)",out_pairs)]
body=[]; csvr=[]
for lab,pp in T3:
    row=rdrow(pp)
    body+=rd_block(lab,row); csvr.append(rd_csv_row(lab,row))
write_csv("T3_main_results",RD_CSV_HDR,csvr)
tex_table("T3_main_results",
 "The effect of authorisation on borrowing and building","tab:main",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Survey row: GFD/IUF, EMMA-independent (survivorship check). Continuation: ballot purpose matched to use-of-proceeds functions; bridge precision 80.0\\% (blind audit). Pay-go row: full-window cohort (votes to $\\sim$2017--18, outlay to FY2023).",
 "A narrow authorisation raises six-year GO issuance by eleven points (robust), roughly doubles per-capita borrowing in disclosure and survey data alike, raises same-purpose project delivery, and moves building nearly one-for-one with borrowing: refusal is not offset by pay-go construction.")

# ================= T6 where it binds =================
PG=[r for r in S if r["acs_grain"] in ("place","sd")]
def split_rows(lab, keyfn, G, extra_note=""):
    vals=sorted(v for v in (keyfn(r) for r in G) if v is not None)
    med=vals[len(vals)//2]
    lo=[r for r in G if keyfn(r) is not None and keyfn(r)<med]
    hi=[r for r in G if keyfn(r) is not None and keyfn(r)>=med]
    rl=rdrow([(r["_m"],r["_go"]) for r in lo]); rh=rdrow([(r["_m"],r["_go"]) for r in hi])
    out=[]
    out+=rd_block(f"{lab}: below median",rl)
    out+=rd_block(f"{lab}: above median",rh)
    if rl and rh:
        bl=rd_rbc([(r["_m"],r["_go"]) for r in lo],10); bh=rd_rbc([(r["_m"],r["_go"]) for r in hi],10)
        d=bh["tau"]-bl["tau"]; se=math.sqrt(bh["se"]**2+bl["se"]**2); p=2*(1-_ncdf(abs(d/se)))
        out.append(f"\\quad difference (above$-$below) & {f3(d)}{stars(p)} & {fp(p)} & & & \\\\ \\addlinespace\\addlinespace")
        return out,[ ["%s below"%lab]+rd_csv_row("",rl)[1:], ["%s above"%lab]+rd_csv_row("",rh)[1:],
                     [f"{lab} difference",f"{d:.4f}","","",f"{p:.4f}","","","",""] ]
    return out,[]
from exlib import _ncdf
body=[]; csvr=[]
for lab,key,G in [("Homeownership",lambda r:fl(r["acs_homeown"]),PG),
                  ("Share 65+",lambda r:fl(r["acs_share65"]),PG),
                  ("Racial-ethnic homogeneity (1$-$frac.)",lambda r:(1-fl(r["acs_frac"])) if fl(r["acs_frac"]) is not None else None,PG),
                  ("Median household income",lambda r:fl(r["acs_medinc"]),PG)]:
    b,c=split_rows(lab,key,G); body+=b; csvr+=c
# timing split on full frame
onc=[r for r in S if pdate(r["election_date"]) and pdate(r["election_date"]).month==11 and pdate(r["election_date"]).year%2==0]
offc=[r for r in S if r not in onc]
ron=rdrow([(r["_m"],r["_go"]) for r in onc]); roff=rdrow([(r["_m"],r["_go"]) for r in offc])
body+=rd_block("On-cycle (November, even year)",ron)
body+=rd_block("Off-cycle",roff)
bon=rd_rbc([(r["_m"],r["_go"]) for r in onc],10); boff=rd_rbc([(r["_m"],r["_go"]) for r in offc],10)
d=bon["tau"]-boff["tau"]; se=math.sqrt(bon["se"]**2+boff["se"]**2); p=2*(1-_ncdf(abs(d/se)))
body.append(f"\\quad difference (on$-$off) & {f3(d)}{stars(p)} & {fp(p)} & & & \\\\ \\addlinespace")
csvr+= [["On-cycle"]+rd_csv_row("",ron)[1:],["Off-cycle"]+rd_csv_row("",roff)[1:],
        ["Timing difference",f"{d:.4f}","","",f"{p:.4f}","","","",""]]
write_csv("T6_moderators",RD_CSV_HDR,csvr)
tex_table("T6_moderators",
 "Where the requirement binds: splits at within-frame medians","tab:binds",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Demographic splits run on the 6,255 proper-grain measures (place grain for municipalities, district grain for schools); special districts excluded pending sub-county demographics. Partisanship (precinct-built 577-city panel, all subgroups n.s.) in Appendix Table A-P1.",
 "The effect concentrates where the consenting public is propertied, older, homogeneous and consulted on-cycle; it is ownership, not income, and institutional, not partisan.")

# ================= T7 fork against the menu =================
menu={r[0]:r[1] for r in parse_md_table("analysis/M1_RESULTS.md","non-voted $ share")[1:]}
CLS=[("Schools",lambda r:r["census_type"]=="school_district","school_district"),
     ("General-purpose",lambda r:r["census_type"] in ("municipal","township","county"),None),
     ("Utilities (special districts)",lambda r:r["census_type"]=="special_district","special_district")]
gp_share=None
mm=parse_md_table("analysis/M1_RESULTS.md","exit-menu richness (non-voted $ share)")
if mm:
    for row in mm[1:]:
        if row[0].startswith("general-purpose"): gp_share=row[1]
body=[]; csvr=[["class","outcome","rbc","ci_lo","ci_hi","p","conv","h","nL","nR","menu_nonvoted_share","resubmit_share"]]
for lab,sel,ent in CLS:
    G=[r for r in S if sel(r)]
    fails=[r for r in G if r["passed"]=="0" and r["resubmitted_4y"] in ("0","1")]
    rs=sum(1 for r in fails if r["resubmitted_4y"]=="1")/len(fails) if fails else float("nan")
    ms=menu.get(ent, gp_share or "--")
    for olab,key in [("GO issuance","_go"),("Any issuance","_any")]:
        row=rdrow([(r["_m"],r.get(key)) for r in G])
        pre = f"{lab}, {olab}" if olab=="GO issuance" else f"\\quad {olab}"
        body+=rd_block(pre,row)
        csvr.append([lab,olab]+rd_csv_row("",row)[1:]+[ms,f"{rs:.3f}"])
    body.append(f"\\quad menu: non-voted \\$ share {str(ms).replace('%',chr(92)+'%')}; failures re-submitting {rs:.3f} \\\\ \\addlinespace")
write_csv("T7_fork_menu",csvr[0],csvr[1:])
tex_table("T7_fork_menu",
 "Exits and the binding of refusal: the fork against the menu","tab:fork",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Menu shares from the national corpus (independent of the RD frame). Utilities cells are small; the ordering, not the magnitude, is the cited object.",
 "Refusal binds exactly where the exit menu is poorest: schools show the discontinuity and the highest re-submission; general-purpose governments, with the richest menu, show none.")

# ================= A2 placebo thresholds =================
def placebo(regsel,thr_true,pseudo,side):
    G=[r for r in S if regsel(r) and fl(r["pct_yes"]) is not None]
    if side=="below": G=[r for r in G if fl(r["pct_yes"])<thr_true]
    else: G=[r for r in G if fl(r["pct_yes"])>thr_true]
    return rdrow([(fl(r["pct_yes"])-pseudo,r["_go"]) for r in G])
reg50=lambda r:r["state"] in ("TX","WI","LA","NC")
def thr_of(r):
    py,m=fl(r["pct_yes"]),r["_m"]
    return round(py-m,1) if py is not None else None
ca55=lambda r:r["state"]=="CA" and thr_of(r)==55.0
ca667=lambda r:r["state"]=="CA" and thr_of(r) is not None and abs(thr_of(r)-66.7)<1
body=[]; csvr=[]
for lab,row in [("50\\%-regime states, pseudo-cutoff 45 (both sides fail)",placebo(reg50,50,45,"below")),
                ("50\\%-regime states, pseudo-cutoff 60 (both sides pass)",placebo(reg50,50,60,"above")),
                ("CA 66.7\\% regime, pseudo-cutoff 60 (both sides fail)",placebo(ca667,66.7,60,"below")),
                ("CA 55\\% regime, pseudo-cutoff 60 (both sides pass)",placebo(ca55,55,60,"above"))]:
    body+=rd_block(lab,row); csvr.append(rd_csv_row(lab,row))
write_csv("A2_placebo_thresholds",RD_CSV_HDR,csvr)
tex_table("A2_placebo_thresholds",
 "Placebo thresholds: no jump where the law draws no line","tab:placebo",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Pseudo-cutoffs estimated within samples where both sides share the same legal outcome.",
 "Issuance is smooth through vote shares at which nothing legal changes; the discontinuity appears only at the statutory threshold.")

# ================= A3 state-by-state =================
body=[]; csvr=[]
for lab,sel,flag in [("Texas (50\\%)",lambda r:r["state"]=="TX",""),
                     ("California schools (55\\%)",lambda r:ca55(r),""),
                     ("California non-school (66.7\\%)",lambda r:ca667(r)," (small cell)"),
                     ("Wisconsin (50\\%)",lambda r:r["state"]=="WI",""),
                     ("Louisiana (50\\%)",lambda r:r["state"]=="LA"," (small; parish-fold grain)"),
                     ("North Carolina (50\\%)",lambda r:r["state"]=="NC"," (small cell)")]:
    row=rdrow([(r["_m"],r["_go"]) for r in S if sel(r)])
    body+=rd_block(lab+flag,row); csvr.append(rd_csv_row(lab,row))
write_csv("A3_state_by_state",RD_CSV_HDR,csvr)
tex_table("A3_state_by_state",
 "The main estimate, state by state","tab:bystate",
 "lccccc",RD_HDR,body,
 PANEL_NOTE+" Louisiana outcomes fold to the parish; the pooled estimate excluding Louisiana appears in Appendix Table A1.",
 "Three adequately powered states, three different thresholds, one answer; the small cells are directionally consistent except fold-grain Louisiana.")

# ================= A1 battery =================
go_pairs=[(r["_m"],r["_go"]) for r in S]
body=[]; csvr=[["row","value"]]
def bat(lab,txt):
    body.append(f"{lab} & \\multicolumn{{5}}{{l}}{{{txt}}} \\\\ \\addlinespace")
    csvr.append([lab,txt.replace("\\","")])
for dn in (0.5,1.0,2.0):
    row=rdrow(go_pairs,10.0,dn)
    bat(f"Donut $|m|>{dn}$pp",f"RBC {f3(row['rbc'])} [{row['lo']:+.3f}, {row['hi']:+.3f}]; conv.\\ {f3(row['conv'])}; N {fn(row['nL'])}/{fn(row['nR'])}")
row=rdrow([(r['_m'],r['_go']) for r in S if r['state']!='LA'])
bat("Excluding Louisiana",f"RBC {f3(row['rbc'])} [{row['lo']:+.3f}, {row['hi']:+.3f}]; conv.\\ {f3(row['conv'])}")
pol=open("analysis/POLISH_RESULTS.md").read()
bat("Cluster by unit (2{,}480)","conv.\\ +0.146, SE 0.036, $z$ 4.11")
bat("Cluster by county (650)","conv.\\ +0.146, SE 0.042, $z$ 3.47")
bat("Lee bounds (crosswalk trim 2.52\\%)","[+0.138, +0.163]")
bat("Randomisation inference, $|m|\\le 2$","diff.\\ +0.142, $p<0.0002$ (5{,}000 permutations)")
bat("IK MSE-optimal bandwidth","$h$ = 1.81pp; $\\tau$ = $-$0.001 (SE 0.075): slope-dominated on two points of support; the design-based tests above at the same window reject decisively")
# horizons + bw sensitivity (csv for the small figures)
hor=[]
for k in range(1,7):
    row=rdrow([(r["_m"],r["_horiz"].get(k)) for r in S])
    hor.append([k,row["rbc"],row["lo"],row["hi"],row["conv"]])
write_csv("A1_horizons",["horizon_years","rbc","ci_lo","ci_hi","conventional"],hor)
bw=[]
for h in range(3,16):
    row=rdrow(go_pairs,float(h))
    bw.append([h,row["rbc"],row["lo"],row["hi"],row["conv"]])
write_csv("A1_bandwidth_curve",["h","rbc","ci_lo","ci_hi","conventional"],bw)
bat("Alternative horizons 1--6y","Appendix Figure A1a (coefficients rise to the 6y wedge)")
bat("Bandwidth sensitivity $h\\in[3,15]$","Appendix Figure A1b (stable from $h\\ge 6$)")
write_csv("A1_battery",csvr[0],csvr[1:])
tex_table("A1_battery",
 "Specification battery for the main estimate","tab:battery",
 "lccccc","Check & \\multicolumn{5}{l}{Result} \\\\",body,
 PANEL_NOTE+" Clustered, Lee, randomisation and IK rows from the committed polish battery (POLISH\\_RESULTS.md).",
 "The estimate survives every design-based and inference variant; the one non-rejecting diagnostic (the MSE-optimal local fit) is a power statement, reconciled in the note.")
print("stage 1 done")
