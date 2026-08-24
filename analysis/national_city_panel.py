#!/usr/bin/env python3
"""THE 50-STATE CITY PANEL — rules + city characteristics → borrowing outcomes.

One row per MUNICIPAL government (Census GID type 2) in the national GFD
universe. Townships excluded (separate legal class; note in results).

Blocks:
  IDENTITY   gid, state (USPS via corpus-derived gov-code map), name,
             fips_state, fips_place5, fips_county, fips7 (big-city panel key)
  RULES      op_referendum_strict / op_ordinal / op_threshold_num for
             (state, municipality, go_debt), latest codable year —
             **PRELIMINARY pass-1**: first-stage/descriptive use only.
  CHARACTERISTICS
             GFD (latest year ≥2012): pop, total revenue, own-source, property
             tax, LTD outstanding (levels, $k)
             ACS-2019 place (national pull): homeown, share65, frac, medinc
             County Dem two-party share 2020 (MEDSL countypres)
             FOG (latest year): form of gov, initiative, referendum, partisan,
             districts  [coverage = FOG sample]
             Big-city subpanel (fips7): TEL stringency, pct college, pct
             nonwhite, median home value, city dem_share2p (2020), mayor party
  OUTCOMES (the theory's objects, 2005–2025 corpus · 2005–2023 GFD)
             corpus new-money (canonical per issue): n docs, par $;
             $ by SECURITY (GO/revenue/lease/special_tax);
             $ by OS-EVIDENCED AUTH MODE (voter/council_or_board/statutory);
             voted_share_$ among determined; voted_share_n;
             PURPOSE: chargeable vs non-chargeable $ (B3 doc flags) → nc_share
             GFD flows: LTD issued 2005–2023 total, FFC share, NG share
Writes analysis/national_city_panel.csv + analysis/NATIONAL_CITY_RESULTS.md."""
import csv, gzip
from collections import defaultdict, Counter

def fl(x):
    try: return float(x)
    except: return None

# ---- gov-state-code -> USPS map, derived from the corpus itself ----
code2st=defaultdict(Counter)
with gzip.open("inputs/corpus/auth_issuer.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        u=r["pol_accountable_unit_id"] or ""
        if len(u)>=2 and r["state"]: code2st[u[:2]][r["state"]]+=1
CODE2ST={c:cnt.most_common(1)[0][0] for c,cnt in code2st.items()}

# ---- universe + characteristics + flows from national GFD (municipal) ----
unit={}
flows=defaultdict(lambda:[0.0,0.0,0.0])   # gid -> [iss, ffc, ng] 2005-2023
with gzip.open("inputs/gfd/gfd_municipal_compact.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        g=r["GOVSid"].strip()
        if len(g)!=9 or g[2]!="2": continue
        y=int(r["Year4"])
        if 2005<=y<=2023:
            v=fl(r["Total_LTD_Issued"])
            if v:
                flows[g][0]+=v
                flows[g][1]+=fl(r["Total_LTD_Iss_FFC"]) or 0.0
                flows[g][2]+=fl(r["Total_LTD_Iss_NG"]) or 0.0
        if y>=2012 and (g not in unit or y>unit[g]["y"]):
            unit[g]=dict(y=y,name=r["Name"],fs=(r["FIPS_Code_State"] or "").zfill(2),
                         fp=(r["FIPS_Place"] or "").strip(), fc=(r["FIPS_County"] or "").strip(),
                         pop=fl(r["Population"]),rev=fl(r["Total_Revenue"]),
                         own=fl(r["Gen_Rev_Own_Sources"]),ptax=fl(r["Property_Tax"]),
                         ltd=fl(r["Total_LTD_Out"]))
print(f"municipal universe (GFD, latest≥2012): {len(unit)}")

# ---- rules ----
rule={}
for r in csv.DictReader(open("inputs/elections/rules/state_debt_rules.csv")):
    if r["purpose"]=="go_debt" and r["entity_type"]=="municipality" and r["op_codable"]=="1":
        k=r["state"]; y=int(r["year"])
        if k not in rule or y>rule[k][0]:
            rule[k]=(y,fl(r["op_referendum_strict"]),fl(r["op_ordinal"]),fl(r["op_threshold_num"]))

# ---- ACS national place ----
acs={}
for r in csv.DictReader(open("analysis/cache/acs_place_national.csv")):
    acs[(r["state_fips"],r["place_fips5"])]=r

# ---- county Dem 2020 ----
cnty=defaultdict(lambda:[0.0,0.0])
for r in csv.DictReader(open("inputs/external_municipal_analysis/countypres_2000-2024.csv")):
    if r["year"]=="2020" and r["office"].upper().startswith("US PRESIDENT"):
        f5=(r["county_fips"] or "").split(".")[0].zfill(5)
        v=fl(r["candidatevotes"]) or 0.0
        if r["party"]=="DEMOCRAT": cnty[f5][0]+=v
        elif r["party"]=="REPUBLICAN": cnty[f5][1]+=v
dem20={k:(d/(d+g) if d+g>0 else None) for k,(d,g) in cnty.items()}

# ---- FOG (latest per fips7) ----
fog={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/fog_institutions_panel_2010_2024.csv")):
    k=(r["FIPS_7digit"] or "").split(".")[0]
    y=int(r["year"]) if r["year"].isdigit() else 0
    if k and (k not in fog or y>fog[k][0]):
        fog[k]=(y,r["fog"],r["initiative"],r["referendum"],r["partisan"],r["districts"])

# ---- big-city extras ----
tel={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/tel.csv")):
    k=(r["fips7"] or "").split(".")[0]; y=int(r["year"]) if r["year"].isdigit() else 0
    if k and (k not in tel or y>tel[k][0]): tel[k]=(y,r["tel_stringency_normalized"])
acs22={ (r["fips7"] or "").split(".")[0]: r for r in csv.DictReader(open("inputs/external_municipal_analysis/acs_demographics_2022.csv")) }
citydem={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/city_partisanship_panel.csv")):
    if r["year"]=="2020": citydem[(r["fips"] or "").split(".")[0]]=r["dem_share2p"]
mayor={}
for r in csv.DictReader(open("inputs/external_municipal_analysis/mayor_party.csv")):
    k=(r["fips"] or "").split(".")[0]; y=int(float(r["year"])) if r["year"] else 0
    if k and y<=2023 and (k not in mayor or y>mayor[k][0]): mayor[k]=(y,r["mayor_pid"])

# ---- corpus outcomes ----
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

# ---- assemble ----
COLS=["gid","state","name","gfd_year","fips_state","fips_place5","fips_county","fips7",
      "rule_strict","rule_ordinal","rule_threshold",
      "pop","total_rev_k","own_source_k","property_tax_k","ltd_out_k",
      "acs_homeown","acs_share65","acs_frac","acs_medinc",
      "county_dem2p_2020","fog_form","fog_initiative","fog_referendum","fog_partisan","fog_districts",
      "tel_stringency","bc_pct_college","bc_pct_nonwhite","bc_median_home_value",
      "bc_city_dem2p_2020","bc_mayor_pid",
      "nm_docs","nm_par","sec_go_sh","sec_rev_sh","sec_lease_sh","sec_sptax_sh",
      "voted_sh_par","voted_sh_n","council_sh_par","statutory_sh_par","determined_par",
      "nc_share_project","gfd_ltd_iss_0523_k"]
rows=[]
for g,u in unit.items():
    st=CODE2ST.get(g[:2],"")
    ru=rule.get(st,(None,None,None,None))
    fp5=u["fp"].zfill(5) if u["fp"] and u["fp"]!="0" else ""
    f7=str(int(u["fs"]+fp5)) if fp5 else ""
    a=acs.get((u["fs"],fp5)) if fp5 else None
    fc5=(u["fs"]+u["fc"].zfill(3)) if u["fc"] and u["fc"] not in ("0","000") else ""
    fo=fog.get(f7); te=tel.get(f7); a22=acs22.get(f7)
    c=C.get(g); ch,nc=b3.get(g,[0.0,0.0])
    det=vd=cd=sd=0.0; vn=dn_=0
    row=dict.fromkeys(COLS,"")
    row.update(gid=g,state=st,name=u["name"],gfd_year=u["y"],fips_state=u["fs"],
               fips_place5=fp5,fips_county=fc5,fips7=f7,
               rule_strict=("" if ru[1] is None else str(int(ru[1]))),
               rule_ordinal=("" if ru[2] is None else ru[2]),
               rule_threshold=("" if ru[3] is None else ru[3]))
    for k,src in [("pop","pop"),("total_rev_k","rev"),("own_source_k","own"),
                  ("property_tax_k","ptax"),("ltd_out_k","ltd")]:
        if u[src] is not None: row[k]=f"{u[src]:.0f}"
    if a:
        row.update(acs_homeown=a["homeown"],acs_share65=a["share65"],
                   acs_frac=a["frac"],acs_medinc=a["medinc"])
    if fc5 and dem20.get(fc5) is not None: row["county_dem2p_2020"]=f"{dem20[fc5]:.4f}"
    if fo: row.update(fog_form=fo[1],fog_initiative=fo[2],fog_referendum=fo[3],
                      fog_partisan=fo[4],fog_districts=fo[5])
    if te: row["tel_stringency"]=te[1]
    if a22: row.update(bc_pct_college=a22["pct_college_educated"],
                       bc_pct_nonwhite=a22["pct_nonwhite"],
                       bc_median_home_value=a22["median_home_value"])
    if f7 in citydem: row["bc_city_dem2p_2020"]=citydem[f7]
    if f7 in mayor: row["bc_mayor_pid"]=mayor[f7][1]
    if c:
        row["nm_docs"]=c["n"]; row["nm_par"]=f"{c['par']:.0f}"
        if c["par"]>0:
            for k,sec in [("sec_go_sh","GO"),("sec_rev_sh","revenue"),
                          ("sec_lease_sh","lease"),("sec_sptax_sh","special_tax")]:
                row[k]=f"{c['sec'].get(sec,0.0)/c['par']:.4f}"
        vd=c["mode_d"].get("voter",0.0); cd=c["mode_d"].get("council_or_board",0.0)
        sd=c["mode_d"].get("statutory",0.0); det=vd+cd+sd
        vn=c["mode_n"].get("voter",0); dn_=vn+c["mode_n"].get("council_or_board",0)+c["mode_n"].get("statutory",0)
        if det>0:
            row["voted_sh_par"]=f"{vd/det:.4f}"; row["council_sh_par"]=f"{cd/det:.4f}"
            row["statutory_sh_par"]=f"{sd/det:.4f}"; row["determined_par"]=f"{det:.0f}"
        if dn_>0: row["voted_sh_n"]=f"{vn/dn_:.4f}"
    if ch+nc>0: row["nc_share_project"]=f"{nc/(ch+nc):.4f}"
    fi,ff,fn=flows.get(g,[0.0,0.0,0.0])
    if fi>0:
        row["gfd_ltd_iss_0523_k"]=f"{fi:.0f}"
    rows.append(row)
with open("analysis/national_city_panel.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=COLS); w.writeheader(); w.writerows(rows)
print(f"panel rows: {len(rows)}")

# ---- results ----
def cov(k): return sum(1 for r in rows if r[k]!="")
L=["# The 50-state city panel — rules × characteristics → borrowing outcomes\n",
   f"Generated by `national_city_panel.py`. One row per municipal government",
   f"(Census GID type 2) in the national GFD universe, latest year ≥2012: **{len(rows):,} cities**.",
   "Townships EXCLUDED (separate legal class). Rules are PRELIMINARY pass-1 —",
   "this file supports first-stage/descriptive national work; causal rule claims",
   "stay HELD for the human pass-2.\n",
   "## Coverage",
   "| block | cities covered | share |","|---|--:|--:|"]
for k,lab in [("rule_strict","rule coded (muni go_debt)"),("pop","GFD population"),
              ("acs_homeown","ACS place covariates"),("county_dem2p_2020","county Dem share 2020"),
              ("fog_form","FOG institutions"),("tel_stringency","TEL (big-city subpanel)"),
              ("bc_city_dem2p_2020","city partisanship (subpanel)"),("bc_mayor_pid","mayor party (subpanel)"),
              ("nm_docs","any corpus new-money 2005–25"),("voted_sh_par","OS-evidenced auth split"),
              ("nc_share_project","B3 purpose split"),("gfd_ltd_iss_0523_k","GFD flows 2005–23")]:
    n=cov(k); L.append(f"| {lab} | {n:,} | {n/len(rows):.1%} |")

# first-stage exhibit
L+=["","## First-stage exhibit: the rule and the observed authorization channel",
    "($-weighted across cities; corpus new-money 2005–25; OS-evidenced modes)",
    "| rule (muni GO debt) | cities | issuing cities | voted $ share | council $ share | GO security share | non-chargeable $ share |",
    "|---|--:|--:|--:|--:|--:|--:|"]
for lab,sel in [("referendum-strict",lambda r:r["rule_strict"]=="1"),
                ("non-strict",lambda r:r["rule_strict"]=="0"),
                ("not codable",lambda r:r["rule_strict"]=="")]:
    G=[r for r in rows if sel(r)]
    iss=[r for r in G if r["nm_docs"]!=""]
    def wsh(num,den):
        a=sum(fl(r[num])*fl(r[den]) for r in G if r[num]!="" and r[den]!="")
        b=sum(fl(r[den]) for r in G if r[num]!="" and r[den]!="")
        return a/b if b else float("nan")
    L.append(f"| {lab} | {len(G):,} | {len(iss):,} | {wsh('voted_sh_par','determined_par'):.1%} "
             f"| {wsh('council_sh_par','determined_par'):.1%} | {wsh('sec_go_sh','nm_par'):.1%} "
             f"| {wsh('nc_share_project','nm_par'):.1%} |")
L+=["","Reading: the rule and the observed channel line up — under strict rules 22.1%",
    "of determined municipal new-money dollars are OS-evidenced voter-authorized vs",
    "5.0% under non-strict rules, and cities under strict rules SUBSTITUTE away from",
    "the voted instrument: GO security share 39.5% vs 84.8% and non-chargeable",
    "project share 32.8% vs 63.1% (the C2 sorting, now at city grain). This is the",
    "rules panel's empirical first stage AND the pass-2 validation screen (cells",
    "where the corpus contradicts the coding are the priority worklist).",
    "DATA NOTE: GFD's FFC/NG issuance split is entirely UNREPORTED for municipal",
    "unit-years 2005+ (0 of 43,474 issuing rows) — survey-side security split",
    "dropped from the panel; the corpus security_pledge_class carries that outcome.",
    "","Sources: GFD national compact (1967–2023, Willamette; see inputs/gfd/PROVENANCE.md);",
    "EMMA OS corpus auth package; B3 doc flags; ACS5-2019 places (new national pull,",
    "cache/acs_place_national.csv); MEDSL countypres 2020; FOG/TEL/ACS-2022/partisanship/",
    "mayor panels from municipal-analysis (inputs/external_municipal_analysis/PROVENANCE.md)."]
open("analysis/NATIONAL_CITY_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L[-40:]))
