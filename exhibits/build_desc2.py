#!/usr/bin/env python3
"""Front-loaded descriptive exhibits computed in one pass over the corpus
(package v3, frozen): who authorises borrowing, and what each type of
government borrows for.

  D1_how_authorised : by government type -- $B, authorisation-mode shares of
                      determined dollars, security-class shares of dollars
  D2_what_for       : by government type -- top functional purposes ($ shares)
  D3_function_voted : by functional purpose -- $B and the voted share of
                      determined dollars (the corpus-based replacement for the
                      registry-skewed ballot-composition panel)

Universe: canonical new-money documents (has_new_money, not has_refunding;
one document per issue), local governments only (state and territory issuers
excluded; documents without an accountable local government excluded and
counted in the notes). Dollar-weighted by effective par."""
import gzip, csv
from collections import defaultdict
import sys; sys.path.insert(0, "exhibits")
from exlib import OUT, write_csv, tex_table, fn

CLASSES = ["school_district", "municipal", "county", "township", "special_district"]
CLABEL = {"school_district": "School districts", "municipal": "Municipalities",
          "county": "Counties", "township": "Townships",
          "special_district": "Special districts"}
FLABEL = {"education": "education", "water_sewer_environment": "water / sewer / environment",
          "transportation": "transportation", "housing_community_dev": "housing / community dev.",
          "general_government": "general government", "economic_development": "economic development",
          "parks_recreation_culture": "parks / recreation / culture",
          "public_safety_justice": "public safety / justice",
          "health_hospitals": "health / hospitals", "utilities": "utilities",
          "human_social_services": "human / social services"}
MODES = ["voter", "council_or_board", "statutory"]

canon = set()
with gzip.open("inputs/corpus/issue_canonical.csv.gz", "rt") as fh:
    for r in csv.DictReader(fh):
        canon.add(r["canonical_doc_id"])

# Authorisation is measured from auth_mode_detailed, which keeps the both-case
# (voter_and_council) instead of collapsing it. A voted GO bond is normally
# jointly authorised -- the referendum authorises, the board resolution
# implements -- so the correct "was there a vote" partition of DETERMINED
# dollars is: voter-any (voter_only + voter_and_council) / board-only
# (council_only) / statute. The single-valued auth_mode_final2 buries most of
# voter_and_council under the board label and understates voter authorisation
# by ~9% of the voter dollar mass; it is reported as an explicit lower bound.
DET_MODES = ("voter_only", "voter_and_council", "council_only", "statutory")
par_cls = defaultdict(float); n_cls = defaultdict(int)
auth_cls = defaultdict(lambda: defaultdict(float))   # voter_any / board_only / statute
joint_cls = defaultdict(float)                        # voter_and_council $
collapsed_voter_cls = defaultdict(float)             # final2==voter $ (lower bound)
det_cls = defaultdict(float)
sec_cls = defaultdict(lambda: defaultdict(float))
fun_cls = defaultdict(lambda: defaultdict(float))
fun_tot = defaultdict(float); fun_voted = defaultdict(float)
fun_det = defaultdict(float); fun_n = defaultdict(int)
excl_unassigned = 0

def auth_bucket(detailed):
    if detailed in ("voter_only", "voter_and_council"):
        return "voter_any"
    if detailed == "council_only":
        return "board_only"
    if detailed == "statutory":
        return "statute"
    return None  # unknown / refunding_no_new_election -> undetermined

with gzip.open("inputs/corpus/auth_os.csv.gz", "rt") as fh:
    for r in csv.DictReader(fh):
        if r["has_new_money"] != "True" or r["has_refunding"] == "True":
            continue
        if r["issue_id"] and r["doc_id"] not in canon:
            continue
        cls = r["pol_accountable_type"]
        if cls in ("state", "territory"):
            continue
        try:
            par = float(r["par_effective"] or 0)
        except ValueError:
            par = 0.0
        if par <= 0:
            continue
        detailed = r["auth_mode_detailed"]
        bucket = auth_bucket(detailed)
        fun = r["primary_major_function"]
        if cls not in CLASSES:
            excl_unassigned += 1
        else:
            par_cls[cls] += par; n_cls[cls] += 1
            if bucket:
                auth_cls[cls][bucket] += par; det_cls[cls] += par
            if detailed == "voter_and_council":
                joint_cls[cls] += par
            if r["auth_mode_final2"] == "voter":
                collapsed_voter_cls[cls] += par
            sec = r["security_pledge_class"] or "unclassified"
            sec_cls[cls][sec if sec in ("GO", "revenue", "lease") else "other"] += par
            if fun and fun != "financing_nonproject":
                fun_cls[cls][fun] += par
        if fun and fun != "financing_nonproject" and cls in CLASSES:
            fun_tot[fun] += par; fun_n[fun] += 1
            if bucket:
                fun_det[fun] += par
                if bucket == "voter_any":
                    fun_voted[fun] += par

# ---------------- D1 ----------------
body = []; csvr = []
for c in CLASSES:
    det = det_cls[c] or 1.0
    tot = par_cls[c] or 1.0
    va = auth_cls[c]["voter_any"] / det
    bo = auth_cls[c]["board_only"] / det
    st = auth_cls[c]["statute"] / det
    jt = joint_cls[c] / det
    go = sec_cls[c]["GO"] / tot; rev = sec_cls[c]["revenue"] / tot
    lea = sec_cls[c]["lease"] / tot
    body.append(f"{CLABEL[c]} & {fn(n_cls[c])} & {par_cls[c]/1e9:,.0f} & "
                f"{va*100:.1f} & {jt*100:.1f} & {bo*100:.1f} & {st*100:.1f} & "
                f"{go*100:.1f} & {rev*100:.1f} & {lea*100:.1f} \\\\")
    csvr.append([CLABEL[c], n_cls[c], round(par_cls[c]/1e9, 1),
                 round(va*100, 1), round(jt*100, 1), round(bo*100, 1), round(st*100, 1),
                 round(go*100, 1), round(rev*100, 1), round(lea*100, 1)])
write_csv("D1_how_authorised",
          ["government type", "n issues", "$B", "voter-any %", "of which joint %",
           "board-only %", "statutory %", "GO %", "revenue %", "lease %"], csvr)
tex_table("D1_how_authorised",
          "How local borrowing is authorised, by type of government",
          "tab:d1", "lccccccccc",
          "  & & & \\multicolumn{4}{c}{Authorised by (\\% of determined \\$)} & \\multicolumn{3}{c}{Security (\\% of \\$)} \\\\\n"
          "\\cmidrule(lr){4-7}\\cmidrule(lr){8-10}\n"
          "Government type & Issues & \\$B & Voters & \\emph{joint} & Board & Statute & GO & Revenue & Lease \\\\",
          body,
          "Canonical new-money issues, official-statement corpus 2005--25 (package v3), "
          "local governments only; dollar-weighted by effective par. Authorisation is the "
          "detailed partition of determined dollars (93.7\\% of documents): Voters = any "
          "voter authorisation (voter-only plus jointly voter-and-board), of which the "
          "\\emph{joint} sub-column is the both-authorised case; Board = board only; Statute "
          "= statutory. A voted general-obligation bond is normally jointly authorised (the "
          "referendum authorises, the board resolution implements), so the both-case is "
          "counted as voter authorisation. The single-valued collapse used elsewhere in the "
          "municipal-finance literature assigns joint issues to the board and so understates "
          "voter authorisation; the collapsed voter share is a lower bound (schools 63.4\\% "
          "against 68.2\\%; all classes 32.1\\% against 35.0\\%). Security shares are of all "
          "dollars ('other' and unclassified omitted). Conduit issues without an accountable "
          f"local government ({fn(excl_unassigned)} documents, largely authority-class "
          "vehicles) are excluded here and appear in the menu matrix (Table A5).",
          "Voter authorisation is the school-district norm and the exception everywhere "
          "else; the security mix mirrors it, with GO dominant for schools and revenue "
          "debt dominant for general-purpose and special-purpose governments.")

# ---------------- D2 ----------------
body = []; csvr = []
for c in CLASSES:
    tot = sum(fun_cls[c].values()) or 1.0
    top = sorted(fun_cls[c].items(), key=lambda kv: -kv[1])[:3]
    cells = "; ".join(f"{FLABEL.get(f,f)} {v/tot*100:.0f}\\%" for f, v in top)
    body.append(f"{CLABEL[c]} & {tot/1e9:,.0f} & {cells} \\\\")
    csvr.append([CLABEL[c], round(tot/1e9, 1)] +
                [x for f, v in top for x in (FLABEL.get(f, f), round(v/tot*100, 1))])
write_csv("D2_what_for",
          ["government type", "classified $B", "f1", "share1", "f2", "share2", "f3", "share3"], csvr)
tex_table("D2_what_for",
          "What each type of government borrows for",
          "tab:d2", "lc>{\\raggedright\\arraybackslash}p{0.55\\linewidth}",
          "Government type & Project \\$B & Largest purposes (share of the type's project dollars) \\\\",
          body,
          "Same universe as Table \\ref{tab:d1}; project dollars by the document's primary "
          "major function, excluding pure financing mechanics. Shares are of the "
          "type's own classified project dollars.",
          "Each type of government is a different bundle of services, which is why the "
          "consent requirement cannot be one institution: the goods behind the ballot "
          "differ by who is asking.")

# ---------------- D3 ----------------
body = []; csvr = []
for f, tot in sorted(fun_tot.items(), key=lambda kv: -kv[1]):
    if tot < 5e9:
        continue
    det = fun_det[f]
    vs = (fun_voted[f] / det * 100) if det > 0 else float("nan")
    body.append(f"{FLABEL.get(f,f)} & {tot/1e9:,.0f} & {vs:.1f} & {fn(fun_n[f])} \\\\")
    csvr.append([FLABEL.get(f, f), round(tot/1e9, 1), round(vs, 1), fun_n[f]])
write_csv("D3_function_voted",
          ["function", "$B", "voted share % of determined $", "n issues"], csvr)
tex_table("D3_function_voted",
          "Which public goods are voted on",
          "tab:d3", "lccc",
          "Purpose (major function) & \\$B & Voted share of \\$ (\\%) & Issues \\\\",
          body,
          "Same universe as Table \\ref{tab:d1}: canonical new-money issues by local "
          "governments, by the document's primary major function; voted share is any "
          "voter authorisation (voter-only plus jointly voter-and-board) as a fraction of "
          "determined dollars within the function. Measured in the national corpus, so "
          "it is not affected by the composition of any state's election registry. "
          "The finer 118-activity grain, including the near-zero-voted functions "
          "(hospitals, multifamily housing, power generation), is Appendix Table A6.",
          "Voters are consulted about schools and civic infrastructure; the chargeable "
          "perimeter of the local state is financed without them.")

print("desc2 done: D1, D2, D3")
