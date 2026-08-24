#!/usr/bin/env python3
"""One-time cache builder: pre-filter the two big inputs to link-relevant rows so
iterative analysis runs in seconds instead of minutes. Deterministic; re-run only
when inputs/ or the crosswalk change.
  analysis/cache/gfd_subset.csv.gz      GFD rows for crosswalked units only
  analysis/cache/issuance_subset.csv.gz auth_os rows with a pol unit, slim columns"""
import csv, gzip, os
os.makedirs("analysis/cache",exist_ok=True)

units=set()
for r in csv.DictReader(open("inputs/elections/crosswalk/referendum_unit_crosswalk.csv")):
    if r["match_status"]=="ASSIGNED" and r["unit_id"]: units.add(r["unit_id"][:9])
print("link units:",len(units))

n=0
with gzip.open("analysis/cache/gfd_subset.csv.gz","wt",newline="") as fo:
    w=None
    for fn in ("gfd_school_compact","gfd_municipal_compact","gfd_township_compact",
               "gfd_county_compact","gfd_special_compact"):
        with gzip.open(f"inputs/gfd/{fn}.csv.gz","rt") as fi:
            rd=csv.DictReader(fi)
            if w is None:
                w=csv.DictWriter(fo,fieldnames=rd.fieldnames); w.writeheader()
            for r in rd:
                if r["GOVSid"].strip() in units: w.writerow(r); n+=1
print("gfd_subset rows:",n)

KEEP=["doc_id","issue_id","state","year","dated_date","par_effective","security_pledge_class",
      "auth_mode_final2","auth_is_voter2","election_date","pol_accountable_unit_id",
      "has_new_money","has_refunding","primary_major_function"]
n=0
with gzip.open("inputs/corpus/auth_os.csv.gz","rt") as fi, \
     gzip.open("analysis/cache/issuance_subset.csv.gz","wt",newline="") as fo:
    rd=csv.DictReader(fi); w=csv.DictWriter(fo,fieldnames=KEEP); w.writeheader()
    for r in rd:
        u=r.get("pol_accountable_unit_id") or ""
        if u and u[:9] in units:
            w.writerow({k:r.get(k,"") for k in KEEP}); n+=1
print("issuance_subset rows:",n)
