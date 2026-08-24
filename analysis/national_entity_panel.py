#!/usr/bin/env python3
"""THE 50-STATE ENTITY PANEL — every local government type, nationwide.

One row per local government (Census GID) in the national GFD universe, all
five types: county (1), municipal (2), township (3), special district (4),
school district (5). The muni-only national_city_panel.csv remains the
city-focused view; this is the general file. Three levels of depth:
  L1  ALL ENTITIES nationwide: rules + county-grain covariates + outcomes
  L2  LARGE CITIES (fips7 subpanel ~570): FOG, TEL, ACS-2022, city
      partisanship, mayor party (munis only)
  L3  RD-STATE DRILL-DOWN linkage: n_referenda / n_rd_sample per unit joins
      this file to paper_panel.csv (referendum grain) on gid == unit_id[:9]

RULES: (state, entity) go_debt, latest codable year, PRELIMINARY pass-1 —
first-stage/descriptive use only. Townships carry MUNICIPALITY rules
(rule_entity_proxy=1): the panel has no township class.
COVARIATES: uniform national county-grain ACS-2019 layer for every type
(cty_*); municipalities upgraded to place grain where matched (acs_grain).
Schools/specials stay county-proxy at national scale (SD grain exists only in
the RD states via SAIPE — the established grain ladder).
OUTCOMES: corpus new-money 2005–25 (canonical per issue): par by SECURITY
class, par by OS-EVIDENCED auth mode, voted share ($ and n), B3 non-chargeable
project share; GFD LTD issued 2005–23 (totals only: the FFC/NG split is
UNREPORTED post-2005 for ALL types — 0 of 161,815 issuing unit-years).
Writes analysis/national_entity_panel.csv.gz + analysis/NATIONAL_ENTITY_RESULTS.md."""
import csv, gzip
from collections import defaultdict, Counter

def fl(x):
    try: return float(x)
    except: return None

TYPES={"1":("county","gfd_county_compact.csv.gz","county"),
       "2":("municipal","gfd_municipal_compact.csv.gz","municipality"),
       "3":("township","gfd_township_compact.csv.gz","municipality"),
       "4":("special_district","gfd_special_compact.csv.gz","special_district"),
       "5":("school_district","gfd_school_compact.csv.gz","school_district")}

code2st=defaultdict(Counter)
with gzip.open("inputs/corpus/auth_issuer.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        u=r["pol_accountable_unit_id"] or ""
        if len(u)>=2 and r["state"]: code2st[u[:2]][r["state"]]+=1
CODE2ST={c:cnt.most_common(1)[0][0] for c,cnt in code2st.items()}

unit={}; flows=defaultdict(float)
for td,(ent,path,_re) in TYPES.items():
    with gzip.open(f"inputs/gfd/{path}","rt") as fh:
        for r in csv.DictReader(fh):
            g=r["GOVSid"].strip()
            if len(g)!=9 or g[2]!=td: continue
            y=int(r["Year4"])
            if 2005<=y<=2023:
                v=fl(r["Total_LTD_Issued"])
                if v: flows[g]+=v
            if y>=2012 and (g not in unit or y>unit[g]["y"]):
                unit[g]=dict(y=y,ent=ent,name=r["Name"],
                             fs=(r["FIPS_Code_State"] or "").zfill(2),
                             fp=(r["FIPS_Place"] or "").strip(),
                             fc=(r["FIPS_County"] or "").strip(),
                             pop=fl(r["Population"]),enr=fl(r["Enrollment"]),
                             rev=fl(r["Total_Revenue"]),own=fl(r["Gen_Rev_Own_Sources"]),
                             ptax=fl(r["Property_Tax"]),ltd=fl(r["Total_LTD_Out"]))
print("universe:",Counter(u["ent"] for u in unit.values()))

rule={}
for r in csv.DictReader(open("inputs/elections/rules/state_debt_rules.csv")):
    if r["purpose"]=="go_debt" and r["op_codable"]=="1":
        k=(r["state"],r["entity_type"]); y=int(r["year"])
        if k not in rule or y>rule[k][0]:
            rule[k]=(y,fl(r["op_referendum_strict"]),fl(r["op_ordinal"]),fl(r["op_threshold_num"]))

acs_p={}
for r in csv.DictReader(open("analysis/cache/acs_place_national.csv")):
    acs_p[(r["state_fips"],r["place_fips5"])]=r
acs_c={}
for r in csv.DictReader(open("analysis/cache/acs_county_national.csv")):
    acs_c[(r["state_fips"],r["county_fips3"])]=r

cnty=defaultdict(lambda:[0.0,0.0])
for r in csv.DictReader(open("inputs/external_municipal_analysis/countypres_2000-2024.csv")):
    if r["year"]=="2020" and r["office"].upper().startswith("US PRESIDENT"):
        f5=(r["county_fips"] or "").split(".")[0].zfill(5)
        v=fl(r["candidatevotes"]) or 0.0
        if r["party"]=="DEMOCRAT": cnty[f5][0]+=v
        elif r["party"]=="REPUBLICAN": cnty[f5][1]+=v
dem20={k:(d/(d+g) if d+g>0 else None) for k,(d,g) in cnty.items()}

fog={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/fog_institutions_panel_2010_2024.csv")):
    k=(r["FIPS_7digit"] or "").split(".")[0]
    y=int(r["year"]) if r["year"].isdigit() else 0
    if k and (k not in fog or y>fog[k][0]):
        fog[k]=(y,r["fog"],r["initiative"],r["referendum"],r["partisan"],r["districts"])
tel={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/tel.csv")):
    k=(r["fips7"] or "").split(".")[0]; y=int(r["year"]) if r["year"].isdigit() else 0
    if k and (k not in tel or y>tel[k][0]): tel[k]=(y,r["tel_stringency_normalized"])
acs22={(r["fips7"] or "").split(".")[0]: r for r in csv.DictReader(open("inputs/external_municipal_analysis/acs_demographics_2022.csv"))}
citydem={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/city_partisanship_panel.csv")):
    if r["year"]=="2020": citydem[(r["fips"] or "").split(".")[0]]=r["dem_share2p"]
mayor={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/mayor_party.csv")):
    k=(r["fips"] or "").split(".")[0]; y=int(float(r["year"])) if r["year"] else 0
    if k and y<=2023 and (k not in mayor or y>mayor[k][0]): mayor[k]=(y,r["mayor_pid"])

# RD-state drill-down linkage
nref=defaultdict(int); nrd=defaultdict(int)
for r in csv.DictReader(open("analysis/paper_panel.csv")):
    g=(r["unit_id"] or "")[:9]
    if g:
        nref[g]+=1
        if str(r["rd_sample"])=="1": nrd[g]+=1
RD_STATES={"CA","TX","WI","LA","NC","MA","MN","IL","IN"}

canon=set()
with gzip.open("inputs/corpus/issue_canonical.csv.gz","rt") as fh:
    for r in csv.DictReader(fh): canon.add(r["canonical_doc_id"])
C=defaultdict(lambda: dict(n=0,par=0.0,sec=defaultdict(float),mode_d=defaultdict(float),
                           mode_n=defaultdict(int)))
with gzip.open("inputs/corpus/auth_os.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        g=(r["pol_accountable_unit_id"] or "")[:9]
        if g not in unit: continue
        if r["issue_id"] and r["doc_id"] not in canon: continue
        if r["has_new_money"].lower() not in ("true","1"): continue
        if r["has_refunding"].lower() in ("true","1"): continue
        c=C[g]; par=fl(r["par_effective"]) or 0.0
        c["n"]+=1; c["par"]+=par
        c["sec"][r["security_pledge_class"] or "unclassified"]+=par
        m=r["auth_mode_final2"] or "undetermined"
        c["mode_d"][m]+=par; c["mode_n"][m]+=1
b3=defaultdict(lambda:[0.0,0.0])
with gzip.open("analysis/cache/b3_doc_flags.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        g=(r["pol_accountable_unit_id"] or "")[:9]
        if g in unit:
            b3[g][0]+=fl(r["amt_chargeable"]) or 0.0
            b3[g][1]+=fl(r["amt_non_chargeable"]) or 0.0

COLS=["gid","entity_type","state","name","gfd_year","fips_state","fips_place5","fips_county","fips7",
      "rule_strict","rule_ordinal","rule_threshold","rule_entity_proxy",
      "pop","enrollment","total_rev_k","own_source_k","property_tax_k","ltd_out_k",
      "acs_grain","acs_homeown","acs_share65","acs_frac","acs_medinc",
      "cty_homeown","cty_share65","cty_frac","cty_medinc","county_dem2p_2020",
      "fog_form","fog_initiative","fog_referendum","fog_partisan","fog_districts",
      "tel_stringency","bc_pct_college","bc_pct_nonwhite","bc_median_home_value",
      "bc_city_dem2p_2020","bc_mayor_pid",
      "rd_state","n_referenda","n_rd_sample",
      "nm_docs","nm_par","sec_go_sh","sec_rev_sh","sec_lease_sh","sec_sptax_sh",
      "voted_sh_par","voted_sh_n","council_sh_par","statutory_sh_par","determined_par",
      "nc_share_project","gfd_ltd_iss_0523_k"]
rows=[]
for g,u in unit.items():
    st=CODE2ST.get(g[:2],"")
    re_=TYPES[g[2]][2]
    ru=rule.get((st,re_),(None,None,None,None))
    fp5=u["fp"].zfill(5) if u["fp"] and u["fp"]!="0" else ""
    f7=str(int(u["fs"]+fp5)) if fp5 and u["ent"]=="municipal" else ""
    fc3=u["fc"].zfill(3) if u["fc"] and u["fc"] not in ("0","000") else ""
    fc5=(u["fs"]+fc3) if fc3 else ""
    row=dict.fromkeys(COLS,"")
    row.update(gid=g,entity_type=u["ent"],state=st,name=u["name"],gfd_year=u["y"],
               fips_state=u["fs"],fips_place5=fp5,fips_county=fc5,fips7=f7,
               rule_strict=("" if ru[1] is None else str(int(ru[1]))),
               rule_ordinal=("" if ru[2] is None else ru[2]),
               rule_threshold=("" if ru[3] is None else ru[3]),
               rule_entity_proxy=("1" if u["ent"]=="township" else "0"),
               rd_state=("1" if st in RD_STATES else "0"))
    for k,src in [("pop","pop"),("enrollment","enr"),("total_rev_k","rev"),
                  ("own_source_k","own"),("property_tax_k","ptax"),("ltd_out_k","ltd")]:
        if u[src] is not None: row[k]=f"{u[src]:.0f}"
    a=acs_p.get((u["fs"],fp5)) if (fp5 and u["ent"] in ("municipal","township")) else None
    if a:
        row.update(acs_grain="place",acs_homeown=a["homeown"],acs_share65=a["share65"],
                   acs_frac=a["frac"],acs_medinc=a["medinc"])
    ac=acs_c.get((u["fs"],fc3)) if fc3 else None
    if ac:
        row.update(cty_homeown=ac["homeown"],cty_share65=ac["share65"],
                   cty_frac=ac["frac"],cty_medinc=ac["medinc"])
        if not a:
            row.update(acs_grain="county",acs_homeown=ac["homeown"],acs_share65=ac["share65"],
                       acs_frac=ac["frac"],acs_medinc=ac["medinc"])
    if fc5 and dem20.get(fc5) is not None: row["county_dem2p_2020"]=f"{dem20[fc5]:.4f}"
    if f7:
        fo=fog.get(f7); te=tel.get(f7); a22=acs22.get(f7)
        if fo: row.update(fog_form=fo[1],fog_initiative=fo[2],fog_referendum=fo[3],
                          fog_partisan=fo[4],fog_districts=fo[5])
        if te: row["tel_stringency"]=te[1]
        if a22: row.update(bc_pct_college=a22["pct_college_educated"],
                           bc_pct_nonwhite=a22["pct_nonwhite"],
                           bc_median_home_value=a22["median_home_value"])
        if f7 in citydem: row["bc_city_dem2p_2020"]=citydem[f7]
        if f7 in mayor: row["bc_mayor_pid"]=mayor[f7][1]
    if nref.get(g): row["n_referenda"]=nref[g]
    if nrd.get(g): row["n_rd_sample"]=nrd[g]
    c=C.get(g); ch,nc=b3.get(g,[0.0,0.0])
    if c:
        row["nm_docs"]=c["n"]; row["nm_par"]=f"{c['par']:.0f}"
        if c["par"]>0:
            for k,sec in [("sec_go_sh","GO"),("sec_rev_sh","revenue"),
                          ("sec_lease_sh","lease"),("sec_sptax_sh","special_tax")]:
                row[k]=f"{c['sec'].get(sec,0.0)/c['par']:.4f}"
        vd=c["mode_d"].get("voter",0.0); cd=c["mode_d"].get("council_or_board",0.0)
        sd=c["mode_d"].get("statutory",0.0); det=vd+cd+sd
        vn=c["mode_n"].get("voter",0)
        dn_=vn+c["mode_n"].get("council_or_board",0)+c["mode_n"].get("statutory",0)
        if det>0:
            row["voted_sh_par"]=f"{vd/det:.4f}"; row["council_sh_par"]=f"{cd/det:.4f}"
            row["statutory_sh_par"]=f"{sd/det:.4f}"; row["determined_par"]=f"{det:.0f}"
        if dn_>0: row["voted_sh_n"]=f"{vn/dn_:.4f}"
    if ch+nc>0: row["nc_share_project"]=f"{nc/(ch+nc):.4f}"
    if flows.get(g): row["gfd_ltd_iss_0523_k"]=f"{flows[g]:.0f}"
    rows.append(row)
with gzip.open("analysis/national_entity_panel.csv.gz","wt",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=COLS); w.writeheader(); w.writerows(rows)
print(f"panel rows: {len(rows)}")

# ---------- results ----------
L=["# The 50-state entity panel — all local governments\n",
   f"Generated by `national_entity_panel.py`. One row per local government in the",
   f"national GFD universe (latest year ≥2012): **{len(rows):,} units**. Rules",
   "PRELIMINARY pass-1 (first-stage/descriptive only). Townships carry MUNICIPALITY",
   "rules (`rule_entity_proxy=1`). GFD's FFC/NG issuance split is unreported",
   "post-2005 for every type (0 of 161,815 issuing unit-years) — totals only;",
   "the corpus security_pledge_class carries the security outcome.",
   "L3 drill-down: `n_referenda`/`n_rd_sample` join this file to `paper_panel.csv`",
   "(referendum grain, 9 RD states) on gid == unit_id[:9].\n",
   "## Coverage by entity type",
   "| entity | units | rule coded | ACS (place/county) | county Dem | corpus new-money | OS auth split | GFD flows | in RD frame |",
   "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
for ent in ("county","municipal","township","special_district","school_district"):
    G=[r for r in rows if r["entity_type"]==ent]
    def cv(k): return sum(1 for r in G if r[k]!="")
    L.append(f"| {ent} | {len(G):,} | {cv('rule_strict')/len(G):.0%} | {cv('acs_homeown')/len(G):.0%} "
             f"| {cv('county_dem2p_2020')/len(G):.0%} | {cv('nm_docs'):,} | {cv('voted_sh_par'):,} "
             f"| {cv('gfd_ltd_iss_0523_k'):,} | {cv('n_rd_sample'):,} |")

L+=["","## First-stage exhibit: rule × entity → observed channel ($-weighted, corpus 2005–25)",
    "| entity | rule | units | voted $ share | council $ share | GO security share | non-chargeable share |",
    "|---|---|--:|--:|--:|--:|--:|"]
def wsh(G,num,den):
    a=sum(fl(r[num])*fl(r[den]) for r in G if r[num]!="" and r[den]!="")
    b=sum(fl(r[den]) for r in G if r[num]!="" and r[den]!="")
    return a/b if b else None
for ent in ("county","municipal","township","special_district","school_district"):
    for lab,val in [("strict","1"),("non-strict","0")]:
        G=[r for r in rows if r["entity_type"]==ent and r["rule_strict"]==val]
        if sum(1 for r in G if r["voted_sh_par"]!="")<25: continue
        vs=wsh(G,"voted_sh_par","determined_par"); cs=wsh(G,"council_sh_par","determined_par")
        gs=wsh(G,"sec_go_sh","nm_par"); ns=wsh(G,"nc_share_project","nm_par")
        fmt=lambda x: f"{x:.1%}" if x is not None else "–"
        L.append(f"| {ent} | {lab} | {len(G):,} | {fmt(vs)} | {fmt(cs)} | {fmt(gs)} | {fmt(ns)} |")
L+=["","Reading: in FOUR of five classes the coded rule predicts the OS-evidenced",
    "voted share, most dramatically for schools (72.5% vs 7.5%) — the rules panel's",
    "first stage at the grain of the whole local state. The EXCEPTION is townships",
    "(18.2% strict vs 46.6% non-strict) — and townships are the one class carrying a",
    "PROXY rule (municipality go_debt; the panel has no township class): New-England",
    "town-meeting states are coded non-strict for cities while towns borrow by town",
    "meeting VOTE, which flips the cell. This is not noise — it is the panel telling",
    "us townships need their own rule column in pass-2. Causal versions of these",
    "contrasts stay HELD for the rules pass-2.",
    "","The muni-focused `national_city_panel.csv` (with the same corpus blocks and",
    "the big-city subpanel) remains as the city view of this file."]
open("analysis/NATIONAL_ENTITY_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L[9:]))
