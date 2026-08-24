#!/usr/bin/env python3
"""Cross-validate our PRELIMINARY rules panel against the independently-coded
state_bond_referenda_requirements.csv from the municipal-analysis repo (row-18-
style external check; feeds the rules pass-2). Comparison at state level for
MUNICIPAL GO debt (their table's object), year 2024."""
import csv
theirs={r["state_abb"]:r for r in csv.DictReader(open("inputs/external_municipal_analysis/state_bond_referenda_requirements.csv"))}
ours={}
for r in csv.DictReader(open("inputs/elections/rules/state_debt_rules.csv")):
    if r["entity_type"]=="municipality" and r["purpose"]=="go_debt" and r["year"]=="2024":
        ours[r["state"]]=r
agree=dis=nc=0; rowsL=[]
for st in sorted(set(theirs)&set(ours)):
    t=theirs[st]; o=ours[st]
    t_req=t["go_voter_approval_required"]=="1"
    o_strict=o.get("op_referendum_strict")
    if o.get("op_codable")!="1" or o_strict=="":
        nc+=1; rowsL.append((st,"NOT CODABLE (ours)",t_req,"")); continue
    o_req=o_strict=="1"
    if t_req==o_req: agree+=1
    else: dis+=1; rowsL.append((st,"DISAGREE",t_req,o_req))
L=["# Rules cross-validation — our panel vs independent green-bond-paper coding\n",
   "Municipal GO debt, 2024 cells; theirs = state_bond_referenda_requirements.csv",
   "(50 states, sourced to Ballotpedia/state law), ours = PRELIMINARY AI pass-1.\n",
   f"**Agreement on 'voter approval required': {agree}/{agree+dis} codable-both states "
   f"({agree/(agree+dis):.0%}); {nc} not-codable in ours (conditional/home-rule cells).**\n",
   "| state | status | theirs: required | ours: strict |","|---|---|---|---|"]
for st,stat,tv,ov in rowsL: L.append(f"| {st} | {stat} | {tv} | {ov} |")
L.append("\nDisagreements + not-codables above are the priority worklist for the human")
L.append("pass-2 (two independent codings disagreeing = a genuinely hard cell).")
open("analysis/RULES_CROSSVAL_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L[:8]))
print(f"... {len(rowsL)} flagged rows written")
