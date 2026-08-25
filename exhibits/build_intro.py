#!/usr/bin/env python3
"""Introduction exhibits (one corpus pass, package v3 frozen):

  F0_volume.svg / .csv : annual local new-money borrowing 2005--25, stacked by
                         authorisation mode (voter / board / statute), $B
  D0_aggregates.csv    : the headline aggregates the introduction cites
                         (totals, mode shares, security shares, issuer counts)

Universe as in build_desc2.py: canonical new-money documents, accountable
local governments (state/territory and unassigned-conduit issues excluded from
the stacked series; conduit total reported as a memo aggregate).
Greyscale-safe: three lightness steps, 2px white gaps between segments."""
import gzip, csv
from collections import defaultdict
import sys; sys.path.insert(0, "exhibits")
from exlib import OUT, write_csv

CLASSES = {"school_district", "municipal", "county", "township", "special_district"}
MODES = ["voter", "council_or_board", "statutory"]

canon = set()
with gzip.open("inputs/corpus/issue_canonical.csv.gz", "rt") as fh:
    for r in csv.DictReader(fh):
        canon.add(r["canonical_doc_id"])

tot = 0.0; n = 0; issuers = set(); conduit = 0.0
mode = defaultdict(float); sec = defaultdict(float)
yr = defaultdict(lambda: defaultdict(float))
go_ref = 0.0; voted_ref = 0.0
with gzip.open("inputs/corpus/auth_os.csv.gz", "rt") as fh:
    for r in csv.DictReader(fh):
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
        if r["has_refunding"] == "True" and cls in CLASSES:
            if r["security_pledge_class"] == "GO":
                go_ref += par
            if r["auth_mode_final2"] == "voter":
                voted_ref += par
        if r["has_new_money"] != "True" or r["has_refunding"] == "True":
            continue
        if cls not in CLASSES:
            conduit += par; continue
        tot += par; n += 1; issuers.add(r["issuer_id"])
        m = r["auth_mode_final2"]
        if m in MODES:
            mode[m] += par
        s = r["security_pledge_class"] or "?"
        sec[s if s in ("GO", "revenue", "lease") else "other"] += par
        y = r["year"]
        if y and y.isdigit() and 2005 <= int(y) <= 2025:
            yr[int(y)][m if m in MODES else "undetermined"] += par

det = sum(mode.values())
write_csv("D0_aggregates", ["statistic", "value"], [
    ["local new-money issues 2005-25", n],
    ["accountable local issuers", len(issuers)],
    ["total local new-money par ($B)", round(tot/1e9, 1)],
    ["average per year ($B)", round(tot/21/1e9, 1)],
    ["conduit/unassigned additional par ($B)", round(conduit/1e9, 1)],
    ["voter share of determined $ (%)", round(mode["voter"]/det*100, 1)],
    ["board share of determined $ (%)", round(mode["council_or_board"]/det*100, 1)],
    ["statutory share of determined $ (%)", round(mode["statutory"]/det*100, 1)],
    ["GO share of $ (%)", round(sec["GO"]/tot*100, 1)],
    ["revenue share of $ (%)", round(sec["revenue"]/tot*100, 1)],
    ["lease share of $ (%)", round(sec["lease"]/tot*100, 1)],
    ["voter-authorised new-money $ ($B)", round(mode["voter"]/1e9, 1)],
    ["GO new-money $ ($B)", round(sec["GO"]/1e9, 1)],
    ["GO refunding $ ($B)", round(go_ref/1e9, 1)],
    ["voter-mode refunding $ ($B)", round(voted_ref/1e9, 1)],
])
rows = []
for y in range(2005, 2026):
    rows.append([y] + [round(yr[y][m]/1e9, 2) for m in MODES] +
                [round(yr[y]["undetermined"]/1e9, 2)])
write_csv("F0_volume", ["year", "voter_$B", "board_$B", "statutory_$B", "undetermined_$B"], rows)

# ---------------- the figure ----------------
INK = "#111111"; MID = "#8a8a8a"; LIGHT = "#d9d9d9"; GREY = "#777777"
W, H = 760, 400
x0, y0, pw, ph = 64, 52, 660, 290
years = list(range(2005, 2026))
stacks = [[yr[y][m]/1e9 for m in MODES] for y in years]
ymax = 150.0
bw = pw/len(years) - 6
S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
     f'<rect width="{W}" height="{H}" fill="white"/>',
     f'<text x="24" y="26" font-size="15" font-weight="bold" fill="{INK}">Local borrowing and who authorised it, 2005–2025</text>',
     f'<text x="24" y="42" font-size="10.5" fill="{GREY}">New-money issues by accountable local governments, $ billions; stacked by authorisation mode</text>']
for gy in range(0, 151, 50):
    yy = y0 + ph - gy/ymax*ph
    S.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0+pw}" y2="{yy:.1f}" stroke="#eeeeee" stroke-width="1"/>')
    S.append(f'<text x="{x0-8}" y="{yy+3.5:.1f}" font-size="9.5" fill="{GREY}" text-anchor="end">{gy}</text>')
COLS = [INK, MID, LIGHT]
for i, y in enumerate(years):
    x = x0 + i*(pw/len(years)) + 3
    base = y0 + ph
    for j, v in enumerate(stacks[i]):
        hgt = v/ymax*ph
        if hgt <= 0:
            continue
        S.append(f'<rect x="{x:.1f}" y="{base-hgt:.1f}" width="{bw:.1f}" height="{max(hgt-2,0.5):.1f}" fill="{COLS[j]}"/>')
        base -= hgt
    if y % 5 == 0:
        S.append(f'<text x="{x+bw/2:.1f}" y="{y0+ph+16}" font-size="9.5" fill="{GREY}" text-anchor="middle">{y}</text>')
lx = x0 + 8
for lab, col in [("Voter-authorised", INK), ("Board", MID), ("Statute", LIGHT)]:
    S.append(f'<rect x="{lx}" y="{y0+2}" width="10" height="10" fill="{col}" stroke="#bbbbbb" stroke-width="0.5"/>')
    S.append(f'<text x="{lx+15}" y="{y0+11}" font-size="10" fill="{INK}">{lab}</text>')
    lx += 15 + 8*len(lab) + 18
S.append(f'<text x="{x0}" y="{y0+ph+34}" font-size="9" fill="{GREY}">Undetermined modes (6.3% of documents) omitted from stacks. Source: official-statement corpus, package v3.</text>')
S.append("</svg>")
open(f"{OUT}/F0_volume.svg", "w").write("\n".join(S))
print(f"intro exhibits done: total ${tot/1e9:,.0f}B, voter {mode['voter']/det*100:.1f}%")
