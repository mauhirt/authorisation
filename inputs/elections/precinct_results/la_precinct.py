#!/usr/bin/env python3
"""LA precinct-level results for every local proposition, driven by the
la_sos file (race_id + parish_code + date). Blob:
{YYYYMMDD}/VotesRaceByPrecinct/Votes_{raceID}_{PP}.htm  (YES=choice 3, NO=4)."""
import subprocess, json, csv, os
from concurrent.futures import ThreadPoolExecutor, as_completed

UA="Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36"
B="https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob="
EL="/home/user/muni_universe/data/elections"
OUT=f"{EL}/precinct_results"; os.makedirs(OUT,exist_ok=True)

def fetch(url,tries=3):
    for _ in range(tries):
        p=subprocess.run(["curl","-sS","--max-time","40","-A",UA,url],capture_output=True,text=True)
        if p.returncode==0 and p.stdout.strip():
            try: return json.loads(p.stdout)
            except Exception: return None
    return None
def as_list(x): return [] if x is None else (x if isinstance(x,list) else [x])

props=[]
for r in csv.DictReader(open(f"{EL}/la_sos/la_sos_local_propositions_2005_present.csv")):
    d=r["election_date"]; mm,dd,yy=(d.split("/") if "/" in d else (d[5:7],d[8:10],d[:4]))
    ymd=f"{yy}{mm}{dd}" if "/" not in d else f"{d.split('/')[2]}{d.split('/')[0]}{d.split('/')[1]}"
    # election_date is ISO yyyy-mm-dd in the file
    y,m,day=r["election_date"].split("-"); ymd=f"{y}{m}{day}"
    props.append((ymd,r["parish_code"],r["race_id"],r["parish"],r["election_date"]))

def one(t):
    ymd,pp,rid,parish,edate=t
    j=fetch(f"{B}{ymd}/VotesRaceByPrecinct/Votes_{rid}_{pp}.htm")
    out=[]
    for pr in as_list((j or {}).get("Precincts",{}).get("Precinct")):
        ch={c["ID"]:int(c["VoteTotal"]) for c in as_list(pr.get("Choice")) if str(c.get("VoteTotal","")).lstrip("-").isdigit()}
        yes,no=ch.get("3"),ch.get("4"); tot=(yes or 0)+(no or 0)
        out.append({"state":"LA","election_date":edate,"parish_code":pp,"parish":parish,
            "precinct":pr.get("Precinct"),"race_id":rid,"votes_yes":yes,"votes_no":no,
            "total":tot,"pct_yes":round(100*yes/tot,2) if (yes is not None and tot) else None,
            "voters_qualified":pr.get("VoterCountQualified"),"voters_voted":pr.get("VoterCountVoted")})
    return out

rows=[]
with ThreadPoolExecutor(max_workers=14) as ex:
    futs=[ex.submit(one,t) for t in props]; done=0
    for f in as_completed(futs):
        rows.extend(f.result()); done+=1
        if done%1000==0: print(f"  {done}/{len(props)} props, {len(rows)} precinct rows",flush=True)

rows.sort(key=lambda r:(r["election_date"],r["parish_code"],r["race_id"],r["precinct"] or ""))
cols=["state","election_date","parish_code","parish","precinct","race_id","votes_yes","votes_no",
      "total","pct_yes","voters_qualified","voters_voted"]
with open(f"{OUT}/la_precinct_results.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"DONE LA precinct: {len(rows)} rows across {len({(r['election_date'],r['parish_code'],r['race_id']) for r in rows})} propositions",flush=True)
