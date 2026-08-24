#!/usr/bin/env python3
"""ACS 5-yr covariate pull — REQUIRES a free Census API key
(https://api.census.gov/data/key_signup.html; keyless access now returns
'Missing Key'). Usage: CENSUS_KEY=... python3 analysis/acs_pull.py
Pulls, per state in the panel, for vintages 2010 and 2019:
  county + place grain: tenure (B25003: homeownership), age 65+ (B01001),
  race/ethnicity (B03002: fractionalization), median HH income (B19013).
Writes analysis/cache/acs_covariates.csv keyed (vintage, state_fips, geo_type,
geo_id). Upgrade path over the county-proxy moderators in
cache/county_moderators_2015.csv (school-district geography grain can be added
with for=school district (unified):*)."""
import csv,os,sys,json,urllib.request
KEY=os.environ.get("CENSUS_KEY","")
if not KEY: sys.exit("set CENSUS_KEY (free: api.census.gov/data/key_signup.html)")
STATES={"CA":"06","TX":"48","WI":"55","LA":"22","NC":"37","MN":"27","MA":"25","IL":"17","IN":"18"}
V={"B25003_001E":"tenure_tot","B25003_002E":"tenure_own","B01001_001E":"pop",
   "B19013_001E":"medinc","B03002_003E":"nhwhite","B03002_004E":"nhblack",
   "B03002_006E":"nhasian","B03002_012E":"hisp"}
A65=[f"B01001_{i:03d}E" for i in list(range(20,26))+list(range(44,50))]
def get(url):
    with urllib.request.urlopen(url,timeout=120) as r: return json.load(r)
out=[["vintage","state_fips","geo_type","geo_id","name"]+list(V.values())+["pop65"]]
for vint in ("2010","2019"):
    for st,fips in STATES.items():
        for geo in ("county","place"):
            cols=",".join(["NAME"]+list(V)+A65)
            u=(f"https://api.census.gov/data/{vint}/acs/acs5?get={cols}"
               f"&for={geo}:*&in=state:{fips}&key={KEY}")
            data=get(u); hdr=data[0]
            for row in data[1:]:
                d=dict(zip(hdr,row))
                p65=sum(float(d[a] or 0) for a in A65)
                out.append([vint,fips,geo,d[geo],d["NAME"]]+[d[k] for k in V]+[f"{p65:.0f}"])
os.makedirs("analysis/cache",exist_ok=True)
with open("analysis/cache/acs_covariates.csv","w",newline="") as f:
    csv.writer(f).writerows(out)
print(f"wrote {len(out)-1} geo rows")
