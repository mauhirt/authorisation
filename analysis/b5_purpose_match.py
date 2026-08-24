#!/usr/bin/env python3
"""B5 — purpose matching: ballot purposes ↔ OS use functions (round-2, Tier 3).

METHOD (two layers, per the audit protocol):
  1. DETERMINISTIC BRIDGE (this script): ballot text → category via the M2
     keyword map (multi-hit here: a bundle can carry several categories);
     OS use lines → the same categories via the committed FN2CAT map below.
     A window doc CONTINUES a measure's project if ≥1 of its use lines maps to
     ≥1 of the measure's categories.
  2. LLM AUDIT (separate step): a stratified BLIND sample of (measure, doc)
     pairs — ballot text + the doc's use labels, bridge verdict withheld — is
     labeled independently; precision/recall of the bridge is reported in
     B5_RESULTS.md before any number is cited.

Outputs: continuation RD (does the same project get financed, either side of the
cutoff), continuation timing, bundle recomposition on re-submission, and the
blind audit sample (analysis/cache/b5_audit_sample.csv).
Frame: rd_sample ∩ bond_go, |margin|≤10, ballot text categorizable, new-money
window docs ≤6y. Writes analysis/B5_RESULTS.md (audit section appended later)."""
import csv, gzip, re, datetime as dt, hashlib
from collections import defaultdict
import sys; sys.path.insert(0,"analysis")
from rdlib import rd

def f(x):
    try: return float(x)
    except: return None
def pdate(s):
    try: return dt.date.fromisoformat((s or "")[:10])
    except: return None

NORM=[  # shared with m2_balloted_submerged.py (keep in sync)
 ("K-12 schools",            r"school|k-?12|elementary|high school|isd\b|education|classroom|campus"),
 ("higher education",        r"college|university"),
 ("water / sewer / drainage",r"water|sewer|drain|wastewater|storm|sanita"),
 ("roads / streets / bridges",r"road|street|highway|bridge|sidewalk|paving"),
 ("fire / EMS",              r"fire|ems|emergency|ambulance"),
 ("police / jail / safety",  r"police|public safety|law enforcement|jail|correction|sheriff|justice"),
 ("parks / recreation",      r"park|recreation|trail|pool|open space|golf"),
 ("hospital / health",       r"hospital|health|medical|clinic"),
 ("library",                 r"librar"),
 ("transit / rail",          r"transit|rail|bus rapid|metro"),
 ("flood / levee",           r"flood|levee|hurricane"),
 ("housing",                 r"housing|homeless"),
 ("stadium / athletics",     r"stadium|athletic|sports|arena|natatorium"),
 ("technology / equipment",  r"technolog|equipment|bus(es)?\b|vehicle"),
 ("civic buildings / general",r"city hall|town hall|public building|courthouse|civic|municipal building|general government|capital improvement"),
 ("electric / gas utility",  r"electric|gas|utility|power|broadband"),
 ("port / airport",          r"port|airport|harbor"),
]
def cats_of(text):
    t=(text or "").lower()
    return {lab for lab,pat in NORM if re.search(pat,t)}

FN2CAT={  # functional_activity -> ballot category (project functions only)
 **{k:"K-12 schools" for k in ("k12_capital_improvements_general","k12_new_school_construction",
    "k12_renovation_modernization","k12_technology_equipment","k12_athletic_facility",
    "charter_school_facility","education_administrative_facility")},
 **{k:"higher education" for k in ("higher_ed_academic_building","higher_ed_research_facility",
    "community_college_facility","student_housing_dormitory")},
 **{k:"water / sewer / drainage" for k in ("potable_water_supply","water_distribution_mains",
    "water_treatment_plant","wastewater_treatment_plant","sewer_collection_system",
    "stormwater_drainage","recycled_water_system","dam_reservoir")},
 **{k:"roads / streets / bridges" for k in ("arterial_local_roads","street_resurfacing_improvement",
    "highways_freeways","bridges_overpasses","sidewalks_streetscape","traffic_signals_its",
    "street_lighting")},
 **{k:"fire / EMS" for k in ("fire_station","fire_apparatus_equipment","emergency_medical_ems",
    "emergency_communications_911","emergency_operations_center","combined_public_safety_facility")},
 **{k:"police / jail / safety" for k in ("police_station_facility","jail_detention_correctional",
    "courthouse_justice_facility","juvenile_facility","public_safety_training_facility")},
 **{k:"parks / recreation" for k in ("parks_open_space","recreation_community_center",
    "aquatic_center_pool","trails_greenways","golf_course","marina_waterfront","zoo_aquarium")},
 **{k:"hospital / health" for k in ("public_hospital_facility","community_health_clinic",
    "mental_behavioral_health_facility","long_term_skilled_nursing","medical_equipment",
    "public_health_laboratory")},
 "public_library_facility":"library",
 **{k:"transit / rail" for k in ("public_transit_bus","rail_transit_light_heavy",
    "commuter_passenger_rail","multimodal_transportation_program","ferry_marine_transit")},
 "flood_control_infrastructure":"flood / levee","seismic_retrofit_hazard_mitigation":"flood / levee",
 **{k:"housing" for k in ("affordable_multifamily_housing","single_family_homeownership",
    "senior_housing","supportive_homeless_housing","public_housing_rehabilitation",
    "homeless_services_facility")},
 "sports_stadium_arena":"stadium / athletics",
 **{k:"technology / equipment" for k in ("information_technology_systems","general_capital_equipment",
    "vehicles_fleet_equipment")},
 **{k:"civic buildings / general" for k in ("city_county_hall","civic_administrative_center",
    "community_facility_center","public_works_corporation_yard")},
 **{k:"electric / gas utility" for k in ("electric_generation","electric_transmission_distribution",
    "natural_gas_utility","district_heating_cooling","broadband_telecommunications")},
 **{k:"port / airport" for k in ("airport_terminal","airport_runway_airfield","airport_parking_access",
    "port_infrastructure","seaport_marine_terminal","public_parking_facility")},
}

# ---- frame ----
rows=list(csv.DictReader(open("analysis/paper_panel.csv")))
EL="inputs/elections"
raw={}
for st,path,fx in [("CA","cdiac/cdiac_elections_all.csv",lambda r:(r["Purpose"] or "")+" "+(r["Measure Name"] or "")),
                   ("TX","tx_brb/tx_brb_bond_elections_all.csv",lambda r:(r["purposedescription"] or r["purpose"] or "")),
                   ("WI","wi_dpi/wi_dpi_referenda_2005_present.csv",lambda r:(r["BriefDescription"] or "")+" "+(r["FullDescription"] or "")[:200]),
                   ("LA","la_sos/la_sos_local_propositions_2005_present.csv",lambda r:(r["specific_title"] or "")),
                   ("NC","nc_ncsbe/nc_ncsbe_bond_referenda_2005_present.csv",lambda r:(r["contest_name"] or ""))]:
    raw[st]=[fx(r) for r in csv.DictReader(open(f"{EL}/{path}"))]
S=[]
for r in rows:
    if str(r["rd_sample"])!="1" or r["purpose_class"]!="bond_go": continue
    m=f(r["threshold_centered_margin"]); d=pdate(r["election_date"])
    if m is None or m==0 or abs(m)>10 or not d or not r["unit_id"]: continue
    st,idx=r["referendum_row_id"].split(":")
    try: txt=raw[st][int(idx)]
    except (KeyError,IndexError,ValueError): continue
    cats=cats_of(txt)
    if not cats: continue
    S.append(dict(r=r,m=m,d=d,txt=txt.strip()[:160],cats=cats,u=r["unit_id"][:9]))
print(f"frame: {len(S)} close categorizable measures")

# window new-money docs per unit
need_units={s["u"] for s in S}
docs=defaultdict(list)   # unit -> [(date, doc_id)]
with gzip.open("analysis/cache/issuance_subset.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        u=(r["pol_accountable_unit_id"] or "")[:9]
        if u not in need_units: continue
        d=pdate(r["dated_date"])
        nm=(r.get("has_new_money","").lower() in ("true","1")) and (r.get("has_refunding","").lower() not in ("true","1"))
        if d and nm: docs[u].append((d,r["doc_id"]))
need_docs={doc for u in docs for _,doc in docs[u]}
doc_cats=defaultdict(set); doc_labels=defaultdict(list)
with gzip.open("inputs/corpus/auth_projects.csv.gz","rt") as fh:
    for row in csv.DictReader(fh):
        if row["doc_id"] not in need_docs or row["side"]!="use" or row["is_subtotal_row"]=="True": continue
        fa=row["functional_activity"]
        c=FN2CAT.get(fa)
        if c: doc_cats[row["doc_id"]].add(c)
        if row["label"] and len(doc_labels[row["doc_id"]])<6:
            doc_labels[row["doc_id"]].append(row["label"][:60])
W6=dt.timedelta(days=2192)
for s in S:
    first=None; hit=0
    for dd,doc in sorted(docs.get(s["u"],[])):
        if dt.timedelta(0)<dd-s["d"]<=W6 and doc_cats.get(doc) and (doc_cats[doc] & s["cats"]):
            hit=1
            if first is None: first=(dd-s["d"]).days/365.25
    s["cont"]=hit; s["t_first"]=first

L=["# B5 — purpose matching: project continuation & bundle recomposition\n",
   f"Generated by `b5_purpose_match.py`. Frame: {len(S)} rd_sample ∩ bond_go measures,",
   "|margin|≤10, ballot text categorizable (M2 map, multi-hit); window = new-money",
   "docs ≤6y; doc side = committed FN2CAT bridge (functional_activity → category).",
   "NUMBERS BELOW ARE BRIDGE-BASED — cite only with the blind-audit precision in the",
   "audit section at the end of this file.\n",
   "## Project continuation at the cutoff",
   "| spec | barely-passed | barely-failed | RD τ (bw10) | z |","|---|--:|--:|--:|--:|"]
pairs=[(s["m"],float(s["cont"])) for s in S]
res=rd(pairs,10)
p5=[s for s in S if 0<s["m"]<=5]; f5=[s for s in S if -5<=s["m"]<0]
L.append(f"| same-purpose financing ≤6y | {sum(s['cont'] for s in p5)/len(p5):.1%} (n={len(p5)}) "
         f"| {sum(s['cont'] for s in f5)/len(f5):.1%} (n={len(f5)}) | {res['tau']:+.3f} | {res['z']:.2f} |")
def medt(G):
    v=sorted(s["t_first"] for s in G if s["t_first"] is not None)
    return v[len(v)//2] if v else None
L.append(f"\nTiming among continuers: median years to first same-purpose doc — "
         f"passed **{medt(p5):.2f}**, failed **{medt(f5):.2f}**.")
# by big category
L+=["\n### By ballot purpose (|margin|≤5 sides)","| category | passed cont. (n) | failed cont. (n) |","|---|--:|--:|"]
for cat in ("K-12 schools","water / sewer / drainage","roads / streets / bridges","parks / recreation"):
    a=[s for s in p5 if cat in s["cats"]]; b=[s for s in f5 if cat in s["cats"]]
    if len(a)>=20 and len(b)>=10:
        L.append(f"| {cat} | {sum(s['cont'] for s in a)/len(a):.1%} ({len(a)}) | {sum(s['cont'] for s in b)/len(b):.1%} ({len(b)}) |")

# ---- bundle recomposition on re-submission ----
seq=defaultdict(list)
for r in rows:
    d=pdate(r["election_date"])
    if r["unit_id"] and d and r["purpose_class"]=="bond_go":
        seq[r["unit_id"]].append((d,r))
for k in seq: seq[k].sort(key=lambda x:x[0])
kept=[]; dropped=[]; added=[]; nret=0
for r in rows:
    if r["purpose_class"]!="bond_go" or r["passed"]!="0" or not r["unit_id"]: continue
    d=pdate(r["election_date"])
    if not d: continue
    st,idx=r["referendum_row_id"].split(":")
    try: c0=cats_of(raw[st][int(idx)])
    except (KeyError,IndexError,ValueError): continue
    if not c0: continue
    ret=None
    for dj,rj in seq[r["unit_id"]]:
        if dt.timedelta(0)<dj-d<=dt.timedelta(days=1461):
            stj,idxj=rj["referendum_row_id"].split(":")
            try: cj=cats_of(raw[stj][int(idxj)])
            except (KeyError,IndexError,ValueError): continue
            if cj: ret=cj; break
    if ret is None: continue
    nret+=1
    kept.append(len(c0&ret)/len(c0)); dropped.append(len(c0-ret)/len(c0))
    added.append(len(ret-c0)/max(1,len(ret)))
def mean(v): return sum(v)/len(v) if v else float("nan")
L+=["","## Bundle recomposition on re-submission (failed → first categorizable return ≤4y)",
    f"Returns analyzed: **{nret}**. Category retention (share of original categories kept):",
    f"mean **{mean(kept):.1%}**; dropped **{mean(dropped):.1%}**; share of the RETURN that is",
    f"new categories: **{mean(added):.1%}**. Read with the amount finding (median ratio 1.00):",
    "districts return with the same purposes at the same ask — recomposition is the",
    "exception, not the rule." if mean(kept)>0.7 else "recomposition is substantial — see table.",""]

# ---- blind audit sample ----
import random
pos=[(s,doc,dd) for s in S for dd,doc in docs.get(s["u"],[])
     if dt.timedelta(0)<dd-s["d"]<=W6 and doc_cats.get(doc) and (doc_cats[doc] & s["cats"])]
neg=[(s,doc,dd) for s in S for dd,doc in docs.get(s["u"],[])
     if dt.timedelta(0)<dd-s["d"]<=W6 and doc_cats.get(doc) and not (doc_cats[doc] & s["cats"])]
def dsort(x): return hashlib.md5((x[0]["r"]["referendum_row_id"]+x[1]).encode()).hexdigest()
pos=sorted(pos,key=dsort)[:30]; neg=sorted(neg,key=dsort)[:30]
sample=sorted(pos+neg,key=dsort)   # interleaved, verdict withheld
with open("analysis/cache/b5_audit_sample.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["pair_id","state","ballot_text","doc_use_labels"])
    for s,doc,dd in sample:
        w.writerow([hashlib.md5((s["r"]["referendum_row_id"]+doc).encode()).hexdigest()[:10],
                    s["r"]["state"],s["txt"]," | ".join(doc_labels.get(doc,[]))])
with open("analysis/cache/b5_audit_key.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["pair_id","bridge_match"])
    for s,doc,dd in sample:
        w.writerow([hashlib.md5((s["r"]["referendum_row_id"]+doc).encode()).hexdigest()[:10],
                    1 if (doc_cats[doc] & s["cats"]) else 0])
L.append(f"## Audit protocol\nBlind sample written: {len(sample)} (measure, doc) pairs "
         "(30 bridge-matched / 30 unmatched, hash-ordered, verdict withheld) → "
         "`cache/b5_audit_sample.csv`; key in `cache/b5_audit_key.csv`. Precision/recall "
         "appended after independent labeling.")
open("analysis/B5_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
