#!/usr/bin/env python3
"""Merge the state debt-rules panel onto referendum_issuance_link.csv.

Adds per referendum: entity_type (from census_type), the state rule for
(state, entity_type, purpose=go_debt, year) -> op_referendum_strict, op_codable,
rule_threshold; and rd_sample = the institutionally-clean RD subsample
(mandatory ballot referendum required, codable, margin present). purpose is held at
go_debt (the HMS-comparable treatment); CA keeps CDIAC's per-measure threshold, so
the threshold-centered margin already in the panel stays authoritative for CA."""
import csv
EL="inputs/elections"
LINK=f"{EL}/analysis/referendum_issuance_link.csv"
RULES=f"{EL}/rules/state_debt_rules.csv"
CT2ENT={"municipal":"municipality","township":"municipality","county":"county",
        "school_district":"school_district","dep_school_district":"school_district",
        "special_district":"special_district"}
# rules keyed (state, entity_type, purpose, year)
rule={}
for r in csv.DictReader(open(RULES)):
    rule[(r["state"],r["entity_type"],r["purpose"],r["year"])]=r
def lookup(st,ent,yr):
    for y in (yr,"2024","2020"):   # fall back to a representative year if that year missing
        k=(st,ent,"go_debt",y)
        if k in rule: return rule[k]
    return None

rows=list(csv.DictReader(open(LINK)))
newcols=["entity_type","rule_threshold","op_referendum_strict","op_codable","rd_sample"]
out=[]
for r in rows:
    ent=CT2ENT.get(r["census_type"],"")
    yr=(r["election_date"] or "")[:4]
    ru=lookup(r["state"],ent,yr) if ent else None
    strict=(ru or {}).get("op_referendum_strict","")
    codable=(ru or {}).get("op_codable","")
    thr=(ru or {}).get("op_threshold_num","")
    has_margin=r["threshold_centered_margin"] not in ("","None")
    rd=int(bool(ru) and strict=="1" and codable=="1" and has_margin)
    r.update(entity_type=ent,rule_threshold=thr,op_referendum_strict=strict,op_codable=codable,rd_sample=rd)
    out.append(r)
with open(LINK,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(out)
from collections import Counter
print("rd_sample:",dict(Counter(r["rd_sample"] for r in out)))
print("rd_sample=1 by state:",dict(Counter(r["state"] for r in out if r["rd_sample"]=="1" or r["rd_sample"]==1)))
