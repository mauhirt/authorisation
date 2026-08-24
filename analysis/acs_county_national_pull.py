#!/usr/bin/env python3
"""National city panel support — ACS5 2019 place-level covariates, ALL states (county grain).
(The 9-state acs_covariates.csv pull generalized; one call per state.)
Usage: CENSUS_KEY=... python3 analysis/acs_county_national_pull.py
Writes analysis/cache/acs_county_national.csv:
  state_fips, county_fips3, name, homeown, share65, frac, medinc, pop
Vintage 2019 acs5 (single vintage — panel characteristics, not pre-vote-timed)."""
import csv,os,sys,json,time,urllib.request,urllib.error
KEY=os.environ.get("CENSUS_KEY","")
if not KEY: sys.exit("set CENSUS_KEY")
V={"B25003_001E":"tenure_tot","B25003_002E":"tenure_own","B01001_001E":"pop",
   "B19013_001E":"medinc","B03002_003E":"nhwhite","B03002_004E":"nhblack",
   "B03002_006E":"nhasian","B03002_012E":"hisp"}
A65=[f"B01001_{i:03d}E" for i in list(range(20,26))+list(range(44,50))]
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(url,timeout=180) as r:
                b=r.read()
                return json.loads(b) if b.strip() else None
        except urllib.error.HTTPError as e:
            if e.code in (204,404): return None
            if i==3: raise
            time.sleep(5*(i+1))
        except (json.JSONDecodeError,TimeoutError):
            if i==3: return None
            time.sleep(5*(i+1))
    return None
def fl(x):
    try:
        v=float(x); return v if v>-1e6 else None
    except: return None
STATES=[f"{i:02d}" for i in list(range(1,57)) if i not in (3,7,14,43,52)]  # 50 states + DC
out=[["state_fips","county_fips3","name","homeown","share65","frac","medinc","pop"]]
cols=",".join(["NAME"]+list(V)+A65)
for st in STATES:
    u=(f"https://api.census.gov/data/2019/acs/acs5?get={cols}&for=county:*&in=state:{st}&key={KEY}")
    js=get(u)
    if not js: print(f"{st}: empty"); continue
    hdr=js[0]; ix={h:i for i,h in enumerate(hdr)}
    n=0
    for row in js[1:]:
        tt,to=fl(row[ix["B25003_001E"]]),fl(row[ix["B25003_002E"]])
        pop=fl(row[ix["B01001_001E"]]); mi=fl(row[ix["B19013_001E"]])
        p65=sum(fl(row[ix[a]]) or 0 for a in A65)
        w,b,a_,h=(fl(row[ix[k]]) for k in ("B03002_003E","B03002_004E","B03002_006E","B03002_012E"))
        frac=None
        if pop and pop>0 and None not in (w,b,a_,h):
            oth=max(0.0,pop-w-b-a_-h); sh=[w/pop,b/pop,a_/pop,h/pop,oth/pop]
            frac=1-sum(x*x for x in sh)
        out.append([st,row[ix["county"]].zfill(3),row[ix["NAME"]],
                    f"{to/tt:.4f}" if tt else "", f"{p65/pop:.4f}" if pop else "",
                    f"{frac:.4f}" if frac is not None else "",
                    f"{mi:.0f}" if mi else "", f"{pop:.0f}" if pop else ""])
        n+=1
    print(f"{st}: {n} places")
with open("analysis/cache/acs_county_national.csv","w",newline="") as fh:
    csv.writer(fh).writerows(out)
print(f"wrote {len(out)-1} places")
