#!/usr/bin/env python3
"""D6 support — pull ACS B19083 (Gini index of income inequality) for CA at the
panel's grains (county, place, school districts), vintages 2010 + 2019.
Usage: CENSUS_KEY=... python3 analysis/acs_gini_pull.py
Writes analysis/cache/acs_gini_ca.csv keyed like acs_covariates.csv."""
import csv,os,sys,json,time,urllib.request,urllib.error
KEY=os.environ.get("CENSUS_KEY","")
if not KEY: sys.exit("set CENSUS_KEY")
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url,timeout=120) as r:
                b=r.read()
                return json.loads(b) if b.strip() else None
        except urllib.error.HTTPError as e:
            if e.code in (204,404): return None
            if i==2: raise
            time.sleep(5*(i+1))
        except json.JSONDecodeError: return None
    return None
out=[["vintage","state_fips","geo_type","geo_id","name","gini"]]
for vint in ("2010","2019"):
    for geo in ("county","place","school district (unified)",
                "school district (elementary)","school district (secondary)"):
        u=(f"https://api.census.gov/data/{vint}/acs/acs5?get=NAME,B19083_001E"
           f"&for={urllib.parse.quote(geo)}:*&in=state:06&key={KEY}")
        import urllib.parse
        u=(f"https://api.census.gov/data/{vint}/acs/acs5?get=NAME,B19083_001E"
           f"&for={urllib.parse.quote(geo)}:*&in=state:06&key={KEY}")
        js=get(u)
        if not js: print(f"{vint} {geo}: empty"); continue
        hdr=js[0]; gi=len(hdr)-1   # geo code is last col
        for row in js[1:]:
            g=row[gi]; nm=row[0]; v=row[1]
            try: gv=float(v)
            except (TypeError,ValueError): continue
            if gv<0: continue
            out.append([vint,"06",geo,str(g).zfill(5),nm,f"{gv:.4f}"])
        print(f"{vint} {geo}: {sum(1 for r in out[1:] if r[0]==vint and r[2]==geo)} rows")
with open("analysis/cache/acs_gini_ca.csv","w",newline="") as fh:
    csv.writer(fh).writerows(out)
print(f"wrote {len(out)-1} rows")
