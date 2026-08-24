#!/usr/bin/env python3
"""Link each crosswalked referendum to the issuance package on the shared Census
unit_id (== pol_accountable_unit_id), and attach post-referendum issuance outcomes.

Referendum side  : data/elections/crosswalk/referendum_unit_crosswalk.csv (ASSIGNED)
                   + vote margin / pass-fail re-read from each state source.
Issuance side    : scratchpad/auth/auth_os.csv.gz (meta branch output/auth_paper/),
                   grouped by pol_accountable_unit_id; issue-grain dedup on issue_id.

Outputs analysis/referendum_issuance_link.csv (one row per ASSIGNED referendum) with:
  margin (pct_yes - statutory threshold), passed, issued_6y, n_issues_6y, par_6y,
  go_share_6y, voter_auth_share_6y, os_confirms_election (OS's own election_date
  matches this referendum's date on this unit = a self-validated link)."""
import csv,gzip,re,datetime as dt
from collections import defaultdict
XW="inputs/elections/crosswalk/referendum_unit_crosswalk.csv"
EL="inputs/elections"
AUTH="inputs/corpus/auth_os.csv.gz"
OUT=f"analysis/referendum_issuance_link.csv"
WINDOW_Y=6

def money(s):
    if not s: return None
    m=re.search(r"\$?\s*([0-9][0-9,]*(?:\.\d+)?)",str(s))
    if not m: return None
    try: v=float(m.group(1).replace(",",""))
    except: return None
    return v if v<1e12 else None
def pct_from(y,n,g=None):
    if g not in (None,"","NA"):
        v=re.sub(r"[^0-9.]","",str(g))
        try:
            f=float(v)
            if f>0: return f
        except: pass
    y,n=money(y),money(n)
    if y is None or n is None or y+n==0: return None
    return 100*y/(y+n)
# stem-based so 'Defeated'/'Rejected'/'Failed' match (trailing 'ed' breaks a \bword\b anchor)
PASS=re.compile(r"pass|approv|adopt|carr|success|prevail|\bwon\b|\byes\b|\bfor\b",re.I)
FAIL=re.compile(r"fail|defeat|reject|lost|unsuccess|\bno\b|against|voted down",re.I)
def passed(s):
    if not s: return None
    s=str(s).strip()
    if PASS.search(s) and not FAIL.search(s): return True
    if FAIL.search(s) and not PASS.search(s): return False
    return {"p":True,"y":True,"1":True,"f":False,"n":False,"0":False}.get(s.lower())
def thr(st,r):
    if st=="CA":
        tv=(r.get("Threshold Value") or "").strip().lower()
        if tv.startswith("two"): return 66.67
        if tv.startswith("55"): return 55.0
    return 50.0
SPECS={  # st: (path, amt, yes, no, pct, result, date, threshold_row?)
 "CA":(f"{EL}/cdiac/cdiac_elections_all.csv",None,None,"% Yes","Election Result","Election Date",True),
 "TX":(f"{EL}/tx_brb/tx_brb_bond_elections_all.csv","votesfor","votesagainst",None,"result","electiondate",False),
 "WI":(f"{EL}/wi_dpi/wi_dpi_referenda_2005_present.csv","YesVotes","NoVotes",None,"ReferendumStatus","VoteDate",False),
 "LA":(f"{EL}/la_sos/la_sos_local_propositions_2005_present.csv","votes_yes","votes_no","pct_yes","result","election_date",False),
 "MA":(f"{EL}/ma_dls/ma_prop2_5_borrowing_votes.csv","votes_yes","votes_no",None,"result","vote_date",False),
 "NC":(f"{EL}/nc_ncsbe/nc_ncsbe_bond_referenda_2005_present.csv","votes_for","votes_against","pct_for","result","election_date",False),
 "IL":(f"{EL}/il_sbe/il_sbe_referenda_1995_present.csv",None,None,None,"result","election_year",False),
 "IN":(f"{EL}/in_dlgf/in_dlgf_referenda_2009_present.csv",None,None,None,"result","election_year",False),
 "MN":(f"{EL}/mn_sos/mn_sos_ballot_questions_2020_2025.csv","yes_votes","no_votes","pct_yes","outcome","election_date",False),
}
# referendum master keyed by ST:i
ref={}
for st,(path,yc,nc,pc,rc,dc,thr_row) in SPECS.items():
    for i,r in enumerate(csv.DictReader(open(path))):
        pct=pct_from(r.get(yc),r.get(nc),r.get(pc)) if (yc or pc) else None
        t=thr(st,r); margin=(pct-t) if pct is not None else None
        d=(r.get(dc) or ""); m=re.search(r"(19|20)\d{2}(-\d\d-\d\d)?",d)
        edate=m.group(0) if m else None
        ref[f"{st}:{i}"]=dict(pct=pct,margin=margin,passed=passed(r.get(rc)),edate=edate)

# issuance by unit_id
iss=defaultdict(list)  # unit -> [(date, issue_id, par, pledge, voter, os_edate)]
def parse_d(s,yr):
    s=(s or "")[:10]
    try: return dt.date.fromisoformat(s)
    except: pass
    try: return dt.date(int(yr),7,1)
    except: return None
with gzip.open(AUTH,"rt") as f:
    for r in csv.DictReader(f):
        u=r.get("pol_accountable_unit_id") or ""
        if not u: continue
        d=parse_d(r.get("dated_date"),r.get("year"))
        iss[u].append((d,r.get("issue_id") or "",money(r.get("par_effective")),
                       r.get("security_pledge_class") or "",str(r.get("auth_is_voter2")).lower() in ("true","1"),
                       (r.get("election_date") or "")[:10]))

COLS=["state","referendum_row_id","unit_id","census_name","census_type","county","election_date",
      "pct_yes","threshold_centered_margin","passed","issued_6y","n_issues_6y","par_6y",
      "go_share_6y","voter_auth_share_6y","os_confirms_election"]
out=[]
for r in csv.DictReader(open(XW)):
    if r["match_status"]!="ASSIGNED" or not r["unit_id"]: continue
    rid=r["referendum_row_id"]; meta=ref.get(rid,{})
    ed=meta.get("edate") or (r["election_date"] or "")[:10]
    try: rd=dt.date.fromisoformat(ed[:10])
    except: rd=None
    pool=iss.get(r["unit_id"],[])
    win=[x for x in pool if x[0] and rd and rd < x[0] <= rd + dt.timedelta(days=int(WINDOW_Y*365.25))]
    seen=set(); parts=[]; go=v=0; par=0.0
    for d,iid,pv,pl,vt,oe in win:
        k=iid or id((d,pv))
        if k in seen: continue
        seen.add(k); parts.append(1)
        if pv: par+=pv
        if pl=="GO": go+=1
        if vt: v+=1
    ni=len(seen)
    os_conf=any(oe and ed and oe==ed[:10] for *_,oe in pool)
    out.append(dict(state=r["state"],referendum_row_id=rid,unit_id=r["unit_id"],census_name=r["census_name"],
        census_type=r["census_type"],county=r["county"],election_date=ed,
        pct_yes=(f"{meta['pct']:.2f}" if meta.get("pct") is not None else ""),
        threshold_centered_margin=(f"{meta['margin']:.2f}" if meta.get("margin") is not None else ""),
        passed=("" if meta.get("passed") is None else int(meta["passed"])),
        issued_6y=int(ni>0),n_issues_6y=ni,par_6y=(f"{par:.0f}" if par else ""),
        go_share_6y=(f"{go/ni:.3f}" if ni else ""),voter_auth_share_6y=(f"{v/ni:.3f}" if ni else ""),
        os_confirms_election=int(os_conf)))
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(out)
print(f"wrote {OUT}: {len(out)} linked referenda")
