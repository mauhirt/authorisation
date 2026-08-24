#!/usr/bin/env python3
"""NC precinct-level bond-referendum results from NCSBE results_pct files.
One row per (election_date, county, precinct, contest) with FOR/AGAINST/total.
Joins to the contest-level file (and crosswalk) on election_date + contest_name."""
import subprocess, csv, io, re, os, zipfile, glob
from collections import defaultdict

OUT="/home/user/muni_universe/data/elections/precinct_results"
TMP="/tmp/claude-0/-home-user-muni-universe/00365a83-f472-577e-acb7-f3d77468ac75/scratchpad/ncp_tmp"
os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
S3="https://s3.amazonaws.com/dl.ncsbe.gov"
def curl(u,o): return subprocess.run(["curl","-sS","--max-time","180",u,"-o",o]).returncode==0

subprocess.run(["curl","-sS","--max-time","60",f"{S3}?list-type=2&prefix=ENRS/&delimiter=/","-o",f"{TMP}/e.xml"])
dates=sorted(d for d in set(re.findall(r'<Prefix>ENRS/([0-9]{4}_[0-9]{2}_[0-9]{2})/</Prefix>',open(f"{TMP}/e.xml").read())) if d>="2005")

def pick(hdr):
    idx={h.strip().lower():i for i,h in enumerate(hdr)}
    def f(*names,contains=None):
        for n in names:
            if n in idx: return idx[n]
        if contains:
            for h,i in idx.items():
                if all(c in h for c in contains): return i
        return None
    return (f("county"),f("precinct"),f("contest name","contest",contains=("contest",)),
            f("choice"),f("total votes","total_votes",contains=("total","vote")))

rows=[]
for d in dates:
    ymd=d.replace("_",""); z=f"{TMP}/r.zip"
    if not curl(f"{S3}/ENRS/{d}/results_pct_{ymd}.zip",z): continue
    try: zf=zipfile.ZipFile(z)
    except Exception: os.remove(z); continue
    name=next((n for n in zf.namelist() if n.lower().endswith((".txt",".csv"))),None)
    if not name: zf.close(); os.remove(z); continue
    raw=zf.read(name).decode("latin-1","replace"); zf.close(); os.remove(z)
    hd=raw.split("\n",1)[0]; delim="\t" if hd.count("\t")>=hd.count(",") else ","
    rdr=csv.reader(io.StringIO(raw),delimiter=delim); hdr=next(rdr,None)
    if not hdr: continue
    coi,pri,ci,chi,tvi=pick(hdr)
    if None in (coi,pri,ci,chi,tvi): continue
    agg=defaultdict(lambda: defaultdict(int))   # (county,precinct,contest) -> for/against
    for row in rdr:
        if len(row)<=max(coi,pri,ci,chi,tvi): continue
        contest=row[ci].strip()
        if "BOND" not in contest.upper(): continue
        ch=row[chi].strip().upper()
        try: v=int((row[tvi] or "0").replace(",","").strip() or 0)
        except ValueError: continue
        k=(row[coi].strip().upper(),row[pri].strip(),contest)
        if ch in ("FOR","YES"): agg[k]["for"]+=v
        elif ch in ("AGAINST","NO"): agg[k]["against"]+=v
    for (county,precinct,contest),c in agg.items():
        fo,ag=c.get("for",0),c.get("against",0); tot=fo+ag
        rows.append({"state":"NC","election_date":d.replace("_","-"),"county":county,
            "precinct":precinct,"contest_name":contest,"votes_for":fo,"votes_against":ag,
            "total":tot,"pct_for":round(100*fo/tot,2) if tot else None})
    print(f"  {d}: {len(agg)} contest-precinct rows",flush=True)

rows.sort(key=lambda r:(r["election_date"],r["contest_name"],r["county"],r["precinct"]))
cols=["state","election_date","county","precinct","contest_name","votes_for","votes_against","total","pct_for"]
with open(f"{OUT}/nc_precinct_results.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
for f in glob.glob(f"{TMP}/*"):
    try: os.remove(f)
    except OSError: pass
print(f"DONE NC precinct: {len(rows)} rows across {len({(r['election_date'],r['contest_name']) for r in rows})} contests",flush=True)
