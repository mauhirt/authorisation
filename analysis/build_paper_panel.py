#!/usr/bin/env python3
"""Build the paper's estimation panel from the referendum-issuance link.

Adds to each linked referendum:
  purpose_class  bond_go | bond_other | tax | other   (per-state rules below)
  is_resubmission      an earlier same-unit, same-purpose-class measure FAILED <=4y before
  prior_fail_4y        any earlier same-unit+class FAILURE <=4y before (regardless of own result)
  resubmitted_4y       (failed measures) a later same-unit+class measure appears <=4y after
  GFD pre-vote covariates (last fiscal year strictly before the election year,
  looking back <=6y): gfd_year, pop, enrollment, total_rev, property_tax,
  debt_out, ltd_out, and per-capita variants.
Output: analysis/paper_panel.csv + a RESULTS block printed (numbers only from here).

Purpose rules: TX/NC all bond_go (bond-election registers). CA by CDIAC type
(GO Bond -> bond_go; other Bond/Debt -> bond_other; Tax -> tax). WI 'Issue Debt'
-> bond_go, else tax (operating). IL/IN referendum_type Bond -> bond_go, Tax ->
tax, else other. LA title: BOND -> bond_go, MILL/S&U/FEE/TAX -> tax, else other.
MA debt_exclusion -> bond_other (borrowing permission), capital_exclusion -> tax.
MN question text BOND/BUILDING -> bond_go; LEVY/OPERATING/TAX -> tax; else other."""
import csv, gzip, re, datetime as dt
from collections import defaultdict

EL="inputs/elections"; GFD="inputs/gfd"
LINK="analysis/referendum_issuance_link.csv"
OUT="analysis/paper_panel.csv"

# ---------- purpose per referendum_row_id ----------
def purpose_map():
    P={}
    for i,r in enumerate(csv.DictReader(open(f"{EL}/cdiac/cdiac_elections_all.csv"))):
        t=(r["Type of Tax/Debt"] or "").upper()
        P[f"CA:{i}"]=("bond_go" if "GENERAL OBLIGATION" in t else
                      "bond_other" if ("BOND" in t or "DEBT" in t) else
                      "tax" if "TAX" in t else "other")
    n=sum(1 for _ in csv.DictReader(open(f"{EL}/tx_brb/tx_brb_bond_elections_all.csv")))
    for i in range(n): P[f"TX:{i}"]="bond_go"
    for i,r in enumerate(csv.DictReader(open(f"{EL}/wi_dpi/wi_dpi_referenda_2005_present.csv"))):
        P[f"WI:{i}"]="bond_go" if (r["ReferendumType"] or "")=="Issue Debt" else "tax"
    for i,r in enumerate(csv.DictReader(open(f"{EL}/il_sbe/il_sbe_referenda_1995_present.csv"))):
        t=(r["referendum_type"] or "").upper()
        P[f"IL:{i}"]="bond_go" if "BOND" in t else ("tax" if "TAX" in t else "other")
    for i,r in enumerate(csv.DictReader(open(f"{EL}/in_dlgf/in_dlgf_referenda_2009_present.csv"))):
        t=(r["referendum_type"] or "").upper()
        P[f"IN:{i}"]="bond_go" if ("BOND" in t or "CONSTRUCTION" in t) else ("tax" if ("TAX" in t or "OPERATING" in t or "REFERENDUM" in t) else "other")
    for i,r in enumerate(csv.DictReader(open(f"{EL}/la_sos/la_sos_local_propositions_2005_present.csv"))):
        t=(r["specific_title"] or "").upper()
        P[f"LA:{i}"]=("bond_go" if ("BOND" in t or re.search(r"\bG\.?O\.?\b",t)) else
                      "tax" if re.search(r"MILL|S&U|SALES|FEE|TAX|ACREAGE",t) else "other")
    for i,r in enumerate(csv.DictReader(open(f"{EL}/ma_dls/ma_prop2_5_borrowing_votes.csv"))):
        P[f"MA:{i}"]="bond_other" if (r["measure_class"] or "")=="debt_exclusion" else "tax"
    n=sum(1 for _ in csv.DictReader(open(f"{EL}/nc_ncsbe/nc_ncsbe_bond_referenda_2005_present.csv")))
    for i in range(n): P[f"NC:{i}"]="bond_go"
    for i,r in enumerate(csv.DictReader(open(f"{EL}/mn_sos/mn_sos_ballot_questions_2020_2025.csv"))):
        q=((r.get("question_name") or "")+" ").upper()
        P[f"MN:{i}"]=("bond_go" if ("BOND" in q or "BUILDING" in q) else
                      "tax" if ("LEVY" in q or "OPERATING" in q or "TAX" in q) else "other")
    return P

# ---------- GFD covariates: unit9 -> sorted [(year, dict)] (link units only) ----------
def gfd_lookup(link_units):
    G=defaultdict(list)
    files=["gfd_school_compact.csv.gz","gfd_municipal_compact.csv.gz","gfd_township_compact.csv.gz",
           "gfd_county_compact.csv.gz","gfd_special_compact.csv.gz"]
    for fn in files:
        with gzip.open(f"{GFD}/{fn}","rt") as f:
            for r in csv.DictReader(f):
                g=r["GOVSid"].strip()
                if g not in link_units: continue
                def num(c):
                    v=(r.get(c) or "").strip()
                    try: return float(v)
                    except: return None
                G[g].append((int(r["Year4"]),dict(pop=num("Population"),enr=num("Enrollment"),
                    rev=num("Total_Revenue"),ptax=num("Property_Tax"),
                    debt=num("Total_Debt_Outstanding"),ltd=num("Total_Long_Term_Debt_Out"))))
    for g in G: G[g].sort()
    return G

rows=list(csv.DictReader(open(LINK)))
P=purpose_map()
units={r["unit_id"][:9] for r in rows if r["unit_id"]}
print("loading GFD for",len(units),"units ...")
G=gfd_lookup(units)

# ---------- re-submission on (unit_id, purpose_class) ----------
def pdate(s):
    s=(s or "")[:10]
    try: return dt.date.fromisoformat(s)
    except: pass
    m=re.match(r"(\d{4})$",s[:4])
    return dt.date(int(s[:4]),7,1) if (s[:4].isdigit() and len(s)>=4) else None
seq=defaultdict(list)   # (unit, class) -> [(date, rid, passed)]
meta={}
for r in rows:
    pc=P.get(r["referendum_row_id"],"other")
    d=pdate(r["election_date"])
    meta[r["referendum_row_id"]]=(pc,d)
    if r["unit_id"] and d:
        seq[(r["unit_id"],pc)].append((d,r["referendum_row_id"],r["passed"]))
for k in seq: seq[k].sort()
W=dt.timedelta(days=1461)
resub_flags={}
for k,lst in seq.items():
    for i,(d,rid,p) in enumerate(lst):
        prior_fail=any(pj=="0" and dt.timedelta(0)<d-dj<=W for dj,rj,pj in lst[:i])
        later=any(dt.timedelta(0)<dj-d<=W for dj,rj,pj in lst[i+1:])
        resub_flags[rid]=(int(prior_fail),int(later))

# ---------- assemble ----------
NEW=["purpose_class","is_resubmission","prior_fail_4y","resubmitted_4y",
     "gfd_year","gfd_pop","gfd_enrollment","gfd_total_rev","gfd_property_tax",
     "gfd_debt_out","gfd_ltd_out","gfd_rev_pc","gfd_debt_pc"]
n_cov=0
for r in rows:
    rid=r["referendum_row_id"]; pc,d=meta[rid]
    pf,lat=resub_flags.get(rid,(0,0))
    r["purpose_class"]=pc
    r["is_resubmission"]=pf if r["passed"] in ("0","1") else pf
    r["prior_fail_4y"]=pf
    r["resubmitted_4y"]=lat if r["passed"]=="0" else ""
    cov=dict.fromkeys(["gfd_year","gfd_pop","gfd_enrollment","gfd_total_rev","gfd_property_tax","gfd_debt_out","gfd_ltd_out","gfd_rev_pc","gfd_debt_pc"],"")
    if r["unit_id"] and d:
        hist=G.get(r["unit_id"][:9],[])
        pre=[(y,v) for y,v in hist if d.year-6<=y<d.year]
        if pre:
            y,v=pre[-1]; n_cov+=1
            cov["gfd_year"]=y
            for k,src in [("gfd_pop","pop"),("gfd_enrollment","enr"),("gfd_total_rev","rev"),
                          ("gfd_property_tax","ptax"),("gfd_debt_out","debt"),("gfd_ltd_out","ltd")]:
                cov[k]="" if v[src] is None else f"{v[src]:.0f}"
            if v["pop"] and v["pop"]>0:
                if v["rev"] is not None: cov["gfd_rev_pc"]=f"{1000*v['rev']/v['pop']:.1f}"
                if v["debt"] is not None: cov["gfd_debt_pc"]=f"{1000*v['debt']/v['pop']:.1f}"
    r.update(cov)
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

from collections import Counter
print(f"paper_panel.csv: {len(rows)} rows")
print("purpose_class:",dict(Counter(r['purpose_class'] for r in rows)))
rd=[r for r in rows if str(r['rd_sample'])=='1']
print("rd_sample purpose:",dict(Counter(r['purpose_class'] for r in rd)))
print(f"rows with pre-vote GFD covariates: {n_cov} ({n_cov/len(rows):.1%}); in rd_sample: "
      f"{sum(1 for r in rd if r['gfd_year'])} ({sum(1 for r in rd if r['gfd_year'])/len(rd):.1%})")
fails=[r for r in rows if r["passed"]=="0"]
print(f"failed measures: {len(fails)}; resubmitted within 4y: {sum(1 for r in fails if r['resubmitted_4y']=='1' or r['resubmitted_4y']==1)} "
      f"({sum(1 for r in fails if str(r['resubmitted_4y'])=='1')/len(fails):.1%})")
