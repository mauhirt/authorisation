#!/usr/bin/env python3
"""Validate the GFD<->crosswalk join: share of crosswalked units (unit_id[:9]) with
GFD fiscal records, per census_type, + FIPS_Place fill (the ACS bridge). Pass the
directory holding the gfd_*_compact.csv.gz panels."""
import csv,gzip,sys
from collections import defaultdict
GFD=sys.argv[1] if len(sys.argv)>1 else "."
mine=defaultdict(set)
for r in csv.DictReader(open("inputs/elections/crosswalk/referendum_unit_crosswalk.csv")):
    if r["match_status"]=="ASSIGNED": mine[r["census_type"]].add(r["unit_id"][:9])
T2F={"school_district":"gfd_school_compact.csv.gz","municipal":"gfd_municipal_compact.csv.gz",
     "township":"gfd_township_compact.csv.gz","county":"gfd_county_compact.csv.gz",
     "special_district":"gfd_special_compact.csv.gz"}
tot_m=tot_h=0
for ct,fn in T2F.items():
    gids=set(); gids12=set(); fips=n12=0
    with gzip.open(f"{GFD}/{fn}","rt") as f:
        for r in csv.DictReader(f):
            g=r["GOVSid"].strip()
            if not g: continue
            gids.add(g)
            if r["Year4"]>="2012":
                gids12.add(g); n12+=1
                if (r["FIPS_Place"] or "").strip() not in ("","0"): fips+=1
    m=mine[ct]; hit=len(m&gids); tot_m+=len(m); tot_h+=hit
    print(f"{ct:18} my={len(m):6,} inGFD={hit:6,} ({hit/len(m):.1%})  2012+={len(m&gids12):,} ({len(m&gids12)/len(m):.1%})  FIPS_Place fill={fips/n12:.1%}")
print(f"TOTAL {tot_h:,}/{tot_m:,} = {tot_h/tot_m:.1%}")
