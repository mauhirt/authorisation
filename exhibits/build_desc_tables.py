#!/usr/bin/env python3
"""Exhibit stage 2 — descriptive tables assembled from committed results files
and the frozen panels: T1, T4, T5, A4, A5, A6, A7, A9, A-C1, A-P1, A8."""
import csv, gzip, re
from collections import defaultdict
import sys; sys.path.insert(0,"exhibits"); sys.path.insert(0,"analysis")
from exlib import *

def esc(s):
    return (s.replace("\\","").replace("&","\\&").replace("%","\\%").replace("#","\\#")
             .replace("$","\\$").replace("−","-").replace("≤","$\\le$").replace("≥","$\\ge$")
             .replace("×","$\\times$").replace("·","--").replace("→","$\\to$").replace("τ","$\\tau$")
             .replace("β","$\\beta$").replace("**","").replace("*",""))
def md_exhibit(name,caption,label,src,key,notes,reading,max_rows=None,drop_cols=None):
    tab=parse_md_table(src,key)
    if not tab: raise SystemExit(f"table not found: {src} :: {key}")
    hdr=tab[0]; rows=tab[1:]
    if max_rows: rows=rows[:max_rows]
    if drop_cols:
        keep=[i for i in range(len(hdr)) if i not in drop_cols]
        hdr=[hdr[i] for i in keep]; rows=[[r[i] for i in keep if i<len(r)] for r in rows]
    write_csv(name,hdr,rows)
    colspec="l"+"c"*(len(hdr)-1)
    header=" & ".join(esc(h) for h in hdr)+" \\\\"
    body=[" & ".join(esc(c) for c in r)+" \\\\" for r in rows]
    tex_table(name,caption,label,colspec,header,body,notes,reading)
    return hdr,rows

# ================= T1 sample & summary =================
P=panel()
S=rd_frame()
def thr_of(r):
    py,m=fl(r["pct_yes"]),fl(r["threshold_centered_margin"])
    return round(py-m,1) if py is not None and m is not None else None
import statistics
# amounts + counts
EL="inputs/elections"
def money(s):
    m=re.search(r"\$?\s*([0-9][0-9,]*(?:\.\d+)?)",str(s or ""))
    if not m: return None
    try: v=float(m.group(1).replace(",",""))
    except: return None
    return v if 1e4<v<1e12 else None
amt={}; cnt={}
for i,r in enumerate(csv.DictReader(open(f"{EL}/cdiac/cdiac_elections_all.csv"))): amt[f"CA:{i}"]=money(r["Amount of Bond/Tax"])
for i,r in enumerate(csv.DictReader(open(f"{EL}/tx_brb/tx_brb_bond_elections_all.csv"))):
    amt[f"TX:{i}"]=money(r["amount"])
    a,b=fl(r["votesfor"]),fl(r["votesagainst"])
    if a is not None and b is not None and a+b>1: cnt[f"TX:{i}"]=a+b
for i,r in enumerate(csv.DictReader(open(f"{EL}/wi_dpi/wi_dpi_referenda_2005_present.csv"))):
    amt[f"WI:{i}"]=money(r["Amount"])
    a,b=fl(r["YesVotes"]),fl(r["NoVotes"])
    if a is not None and b is not None and a+b>1: cnt[f"WI:{i}"]=a+b
for i,r in enumerate(csv.DictReader(open(f"{EL}/la_sos/la_sos_local_propositions_2005_present.csv"))):
    a,b=fl(r["votes_yes"]),fl(r["votes_no"])
    if a is not None and b is not None and a+b>1: cnt[f"LA:{i}"]=a+b
for i,r in enumerate(csv.DictReader(open(f"{EL}/nc_ncsbe/nc_ncsbe_bond_referenda_2005_present.csv"))):
    a,b=fl(r["votes_for"]),fl(r["votes_against"])
    if a is not None and b is not None and a+b>1: cnt[f"NC:{i}"]=a+b
cells=defaultdict(list)
for r in S:
    t=thr_of(r)
    key=(r["state"], f"{t:.1f}".rstrip("0").rstrip(".") if t else "?")
    cells[key].append(r)
rows=[]; csvr=[]
for (st,t),G in sorted(cells.items()):
    if len(G)<30: continue
    ys=[fl(r["pct_yes"]) for r in G]
    ps=sum(1 for r in G if r["passed"]=="1")/len(G)
    am=sorted(a for a in (amt.get(r["referendum_row_id"]) for r in G) if a)
    el=sorted(c for c in (cnt.get(r["referendum_row_id"]) for r in G) if c)
    am_s=("\\$"+format(int(am[len(am)//2]),",d")) if am else "--"
    el_s=format(int(el[len(el)//2]),",d") if el else "--"
    rows.append(f"{st} ({t}" + "\\%) & " + f"{fn(len(G))} & {statistics.mean(ys):.3f} & {ps:.3f} & "
                + am_s + " & " + el_s + " \\\\")
    csvr.append([f"{st} ({t}%)",len(G),f"{statistics.mean(ys):.3f}",f"{ps:.3f}",
                 int(am[len(am)//2]) if am else "",int(el[len(el)//2]) if el else ""])
rows.append("\\addlinespace")
for lab,n in [("All compiled referenda","47,235"),("Matched to a Census government","40,924"),
              ("At a genuine mandatory-ballot requirement","23,577"),("GO regression-discontinuity frame","11,889")]:
    rows.append(f"\\quad {lab} & {n} & & & & \\\\")
    csvr.append([lab,n,"","","",""])
rows.append("\\addlinespace \\multicolumn{6}{@{}l}{\\emph{Panel B: the official-statement corpus (package v3)}} \\\\ \\addlinespace")
nd=0; det=0; modes=defaultdict(int)
with gzip.open("inputs/corpus/auth_os.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        nd+=1
        m=r["auth_mode_final2"]
        if m in ("voter","council_or_board","statutory","refunding_no_new_election"): det+=1; modes[m]+=1
ent_par=defaultdict(float)
with gzip.open("analysis/national_entity_panel.csv.gz","rt") as fh:
    for r in csv.DictReader(fh):
        v=fl(r["nm_par"])
        if v: ent_par[r["entity_type"]]+=v
for lab,val in [("Documents",fn(nd)),("Issuers","43,030"),
                ("Determination rate",f"{det/nd:.3f}"),
                ("Mode shares (docs): voter / board / statutory",
                 f"{modes['voter']/det:.3f} / {modes['council_or_board']/det:.3f} / {modes['statutory']/det:.3f}"),
                ("New-money par: schools / municipal / county / special / township (\\$B)",
                 " / ".join(f"{ent_par[e]/1e9:.0f}" for e in ("school_district","municipal","county","special_district","township")))]:
    rows.append(f"\\quad {lab} & \\multicolumn{{5}}{{l}}{{{val}}} \\\\")
    csvr.append([lab,val.replace("\\","")])
write_csv("T1_sample",["cell/statistic","n","mean_yes","passed_share","median_amount","median_electorate"],csvr)
tex_table("T1_sample","Sample and summary statistics","tab:sample","lccccc",
 "State (threshold) & N & Mean yes & Passed & Median amount & Median electorate \\\\",rows,
 "Panel A: the referendum frame by state and threshold (cells $\\ge$30 measures); amounts where registries print them (CA/TX/WI); electorate = votes cast where counts exist (TX/WI/LA/NC; counts-unknown placeholder rows excluded). Restriction cascade beneath. Panel B: corpus package v3.",
 "The frame spans three statutory thresholds; the corpus supplies the authorisation mode for 93.7 per cent of a quarter-million documents.")

# ================= T4 fifty-state first stage =================
n1=parse_md_table("analysis/N_RESULTS.md","β(strict)")
rows=[]; csvr=[["spec","beta","se","t","n","clusters"]]
KEEP={"pooled (4 classes, entity dummies)":"Pooled (four classes, entity dummies)",
      "school_district":"School districts","municipal":"Municipalities",
      "county":"Counties","special_district":"Special districts"}
for r in n1[1:]:
    if r[0] in KEEP and len(r)>=7 and r[2] not in ("–","-",""):
        rows.append(f"{KEEP[r[0]]} & {r[2]} & {r[3]} & {r[4]} & {r[5]} & {r[6]} \\\\")
        csvr.append([KEEP[r[0]],r[2],r[3],r[4],r[5],r[6]])
rows.append("\\addlinespace \\multicolumn{6}{@{}l}{\\emph{Municipal substitution (general-purpose)}} \\\\ \\addlinespace")
n2=parse_md_table("analysis/N_RESULTS.md","GO security share (pooled)")
for r in n2[1:]:
    if "general-purpose" in r[0] and "GO" in r[0]:
        rows.append(f"GO security share (\\$) & {r[2]} & {r[3]} & {r[4]} & {r[5]} & {r[6]} \\\\")
        csvr.append(["GO security share ($)",r[2],r[3],r[4],r[5],r[6]])
cc=open("analysis/NC_COVERAGE_RESULTS.md").read()
m=re.search(r"β\(strict\) = \*\*([+\-0-9.]+)\*\*, state-cluster SE ([0-9.]+), t ([+\-0-9.]+), n ([0-9,]+), clusters (\d+)",cc)
rows.append(f"Non-chargeable line share (count basis) & {m.group(1)} & {m.group(2)} & {m.group(3)} & {m.group(4)} & {m.group(5)} \\\\")
csvr.append(["nc line share (count basis)",m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)])
write_csv("T4_first_stage",csvr[0],csvr[1:])
tex_table("T4_first_stage","The fifty-state first stage: rules and observed authorisation","tab:firststage","lccccc",
 "Outcome: voted \\$ share (top) & $\\beta$(strict) & SE & $t$ & N & Clusters \\\\",rows,
 "Entity panel (90,604 local governments), WLS with controls and region FE, state-clustered SEs. RULES PRELIMINARY (pass-1): first-stage associations, not causal estimates. Count-vs-dollar convention for the composition row per Appendix Table A-C1. Townships (proxy rule) excluded.",
 "The coded rule predicts the observed channel in every adequately powered class, and strict-rule cities substitute away from the voted instrument.")

# ================= T5 response margin =================
rows=["\\multicolumn{2}{@{}l}{\\emph{Panel A: the fate of 100 marginal refusals (2005--19 cohort, $|m|\\le 5$, n=422)}} \\\\ \\addlinespace"]
csvr=[["panel","row","value"]]
for lab,v in [("Re-approved by voters $\\le$4y","54.3"),("Returned, not yet converted","13.3"),
              ("Issued via board or statutory channel","5.2"),("Issued on pre-existing voter authority","9.0"),
              ("Extinguished within horizon","18.2")]:
    rows.append(f"\\quad {lab} & {v} \\\\"); csvr.append(["A",lab.replace("\\","") ,v])
rows.append("\\addlinespace \\multicolumn{2}{@{}l}{\\emph{First post-vote authoriser ($|m|\\le5$): barely-passed vs barely-failed}} \\\\")
tm=parse_md_table("analysis/TRANSITION_FATE_RESULTS.md","vote outcome")
for r in tm[1:]:
    rows.append(f"\\quad {esc(r[0])}: voter {r[2]}, board {r[3]}, none {r[6]} & \\\\")
    csvr.append(["A-matrix",r[0],f"voter {r[2]} board {r[3]} none {r[6]}"])
rows.append("\\addlinespace \\multicolumn{2}{@{}l}{\\emph{Panel B: re-submission (2,680 failed GO measures)}} \\\\ \\addlinespace")
for lab,v in [("Hazard, years 1/2/3/4 (\\%)","26.7 / 22.8 / 15.8 / 12.4"),
              ("Cumulative return within 4y (\\%)","58.2"),("Median time to return (years)","1.02"),
              ("Returns that pass (\\%)","61.9"),("Median amount ratio, return/original","1.000"),
              ("Purpose categories retained on return (\\%)","78.2")]:
    rows.append(f"\\quad {lab} & {v} \\\\"); csvr.append(["B",lab.replace("\\",""),v])
write_csv("T5_response",csvr[0],csvr[1:])
tex_table("T5_response","The response margin: what refusal buys","tab:response","l@{\\quad}l",
 "Quantity & Value \\\\",rows,
 "Fates are mutually exclusive per 100 barely-refused measures; issuance on pre-existing voter authority draws on authorisations banked before the refused measure and is not evidence of evading it. Panel B: full failed sample; amounts where registries print them (n=1,354). Retention from the audited purpose bridge (precision 80.0\\%).",
 "Refusal is a pause: most marginal refusals are re-approved at the next election at the same ask, fewer than one in five extinguish, and the board channel is a floor rather than the treatment margin.")

# ================= A4 agenda =================
md_exhibit("A4_agenda","The agenda margin by regime","tab:agenda",
 "analysis/AGENDA_RESULTS.md","#districts",
 "School GO proposal behaviour 2005--25; MN empty by classification (a data fact). Passage-rate and TX-2019 unbundling panels in the CSV companion (A4b, A4c).",
 "Under the higher bar districts propose half as often, at 2.6 times the size, four times more on-cycle; pass rates barely move until two-thirds.")
t=parse_md_table("analysis/AGENDA_RESULTS.md","pass rate"); write_csv("A4b_passrates",t[0],t[1:])
t=parse_md_table("analysis/AGENDA_RESULTS.md","props/election"); write_csv("A4c_tx2019",t[0],t[1:])

# ================= A5 landscape =================
md_exhibit("A5a_menu","The menu matrix: non-voted share of new-money dollars","tab:menu",
 "analysis/M1_RESULTS.md","non-voted $ share",
 "National corpus, canonical new-money issues, package v3; determined dollars.",
 "School districts hold the poorest exit menu; authority-class issuers barely face an electorate at all.")
md_exhibit("A5b_submerged","The submerged local state","tab:submerged",
 "analysis/M2_RESULTS.md","corpus function",
 "Local project functions $\\ge$\\$5B voted under 2\\% of the time; financing mechanics excluded; named examples in text.",
 "Hospitals, housing, power and airports are financed at scale with essentially no electoral moment.")
md_exhibit("A5c_coalitions","Absolute coalition sizes","tab:coalitions",
 "analysis/M3_RESULTS.md","votes cast p10/p50/p90",
 "TX/WI/LA/NC counts; CDIAC reports percentages only; placeholder rows excluded.",
 "The same statutory sentence convenes half a million voters in Harris County and two in a developer district.")

# ================= A6 banked authorisation =================
md_exhibit("A6a_chain","The near-miss chain","tab:chain",
 "analysis/P3_RESULTS.md","years since failure k",
 "CA failed GO measures; per-cell observability restrictions; new-money issues only.",
 "The near-miss deficit widens with the window: not a truncation artefact.")
t=parse_md_table("analysis/P3_RESULTS.md","fail→passed return"); write_csv("A6b_chain_timing",t[0],t[1:])
md_exhibit("A6c_ratecap","The rate-cap split (inconclusive)","tab:ratecap",
 "analysis/P4_RESULTS.md","median pass→first issue",
 "132 conversions; the uncapped cell (14; 9 school) is too thin to test and points against the cap story. Verdict: mechanism neither supported nor excluded.",
 "Re-approved but unissued stands as a documented fact without an adjudicated mechanism.")

# ================= A7 blocked majorities =================
md_exhibit("A7_blocked","Demography of blocked majorities (descriptive; California)","tab:blocked",
 "analysis/D6_RESULTS.md","blocked−cleared",
 "Blocked = majority short of the supermajority threshold; within-matched ACS/SAIPE at the D5 grain ladder; DESCRIPTIVE, no causal claim.",
 "Blocked majorities arise in less affluent, mid-composition school districts: the incidence of the higher bar.")

# ================= A9 validation =================
md_exhibit("A9_validation","Validation of extracted authorisation fields","tab:validation",
 "analysis/VALIDATION_RESULTS.md","T1: docs w/ date",
 "Election-date matches against independently observed referenda; support and consistency tests as defined in the text. GFD bridge: 2022 public-use issuance matches GFD within 0.5\\% for 99.9\\% of bridged units.",
 "Where registries are complete the extracted fields track the election record at ninety per cent or better; shortfalls sit exactly where registry coverage is known-short.")

# ================= A-C1 / A-P1 =================
md_exhibit("AC1_coverage","Classified-line coverage by regime (nc-share selection check)","tab:ac1",
 "analysis/NC_COVERAGE_RESULTS.md","unit coverage",
 "Coverage of B3-classified project dollars among corpus-active units; regime labels PRELIMINARY. Count-based composition versions accompany every dollar-based exhibit.",
 "Coverage is regime-unbalanced on the unit margin, so the text cites the count basis; both bases agree on direction.")
t=parse_md_table("analysis/NC_COVERAGE_RESULTS.md","chargeable share (count)"); write_csv("AC1b_count_sorting",t[0],t[1:])
t=parse_md_table("analysis/D5_EXTERNAL_RESULTS.md","τ GO-issue")
write_csv("AP1_county_partisanship",t[0],t[1:])
rows=[" & ".join(esc(c) for c in r)+" \\\\" for r in t[1:]]
tex_table("AP1_county_partisanship","County-grain partisanship (demoted from the text)","tab:ap1",
 "l"+"c"*(len(t[0])-1)," & ".join(esc(h) for h in t[0])+" \\\\",rows,
 "County presidential two-party share, 2020 vintage, county grain: a coarse proxy for district electorates. The text's partisanship null cites the precinct-built 577-city panel. National first-stage interaction: strict $\\times$ county Dem $-$0.65 ($t$ $-$2.0), descriptive.",
 "The county-grain splits agree with the city-panel null; nothing partisan moderates the authorisation effect.")

# ================= A8 variable definitions =================
V=open("paper/VARIABLES.md").read()
sec=None; out=[["section","variable","definition","level","source","coverage"]]
for ln in V.splitlines():
    if ln.startswith("## "): sec=ln[3:].split("(")[0].strip()
    if ln.strip().startswith("|") and not set(ln.strip())<=set("|-: "):
        c=[x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c)>=5 and c[0] not in ("variable",""):
            out.append([sec,c[0],c[1],c[2],c[3],c[4] if len(c)>4 else ""])
write_csv("A8_variables",out[0],out[1:])
rows=[]
for r in out[1:]:
    rows.append(" & ".join(esc(str(x))[:60] for x in r[1:])+" \\\\")
tex_table("A8_variables","Variable definitions and coverage","tab:vars","p{2.6cm}p{4.5cm}p{1.6cm}p{2.2cm}p{2.6cm}",
 "Variable & Definition & Level & Source & Coverage \\\\",rows,
 "Auto-generated from the variable inventory (paper/VARIABLES.md), the single source; coverage computed on the frozen v3 panels.",
 "Every variable in the paper appears here with its level, source and exact coverage.")
print("stage 2 done")

# ================= A5d / A5e (cross-check gap fills) =================
md_exhibit("A5d_channel_sorting","Chargeable share of classified project dollars by authorisation channel","tab:channels",
 "analysis/B3_RESULTS.md","chargeable share",
 "National corpus, classified printed-amount use lines; count-based version in Table A-C1b.",
 "The voted channel finances the non-chargeable civic core; the unvoted channels carry the chargeable perimeter.")
md_exhibit("A5e_firststage_raw","Observed voted share by rule regime and entity class","tab:fsraw",
 "analysis/NATIONAL_ENTITY_RESULTS.md","voted $ share",
 "Dollar-weighted shares from the entity panel (v3); rules PRELIMINARY; townships carry a proxy municipality rule (the reversal is a coding artefact scheduled for pass-2).",
 "Raw magnitudes behind Table 4: under strict rules two-thirds of school dollars are voted; under lax rules almost none are.")
print("gap fills done")
