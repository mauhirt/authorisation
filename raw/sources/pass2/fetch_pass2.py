#!/usr/bin/env python3
"""Fetch and archive primary statutory/constitutional texts for the rules
pass-2 worklist (RETRIEVAL ONLY -- no summarising, no classification).

Each entry is saved verbatim; HTML pages are additionally rendered to PDF via
the local headless chromium for a stable archival copy. MANIFEST.csv records
url, retrieval date, HTTP status, bytes, sha256 for every file.

TLS note: outbound HTTPS goes through the session's agent proxy. Two state
sites (cga.ct.gov, billstatus.ls.state.ms.us) serve incomplete certificate
chains, so the CA file used here is the proxy bundle + system roots + the two
missing intermediates (GoDaddy G2, GlobalSign RSA OV 2018), fetched from the
CAs' own repositories. Verification stays ON for every request.
"""
import csv, datetime as dt, glob, hashlib, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CA = os.environ.get("PASS2_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CHROMES = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))
CHROME = CHROMES[-1] if CHROMES else None

# stem, url, note  (order matches the worklist: definitional first, township-relevant last)
ITEMS = [
 # -- Part 1 · definitional disagreements ------------------------------------
 ("MS_21-33-307_HB711-2023-reprint",
  "https://billstatus.ls.state.ms.us/documents/2023/html/HB/0700-0799/HB0711IN.htm",
  "Miss. Code 21-33-307 as set out verbatim in MS HB 711 (2023, as introduced); official code portal is LexisNexis-only and mirrors block automated retrieval -- verify against enacted text at ruling time"),
 ("TN_9-21-205_lawserver",
  "https://www.lawserver.com/law/state/tennessee/tn-code/tennessee_code_9-21-205",
  "Tenn. Code Ann. 9-21-205 (LawServer mirror; official code portal is LexisNexis-only)"),
 ("TN_9-21-206_lawserver",
  "https://www.lawserver.com/law/state/tennessee/tn-code/tennessee_code_9-21-206",
  "Tenn. Code Ann. 9-21-206 (protest petition mechanics)"),
 ("TN_9-21-207_lawserver",
  "https://www.lawserver.com/law/state/tennessee/tn-code/tennessee_code_9-21-207",
  "Tenn. Code Ann. 9-21-207 (election after petition)"),
 ("WI_stat_ch67",
  "https://docs.legis.wisconsin.gov/statutes/statutes/67.pdf",
  "Wis. Stat. ch. 67 (official PDF; 67.05 is the referendum section)"),
 ("MA_MGL_c44_s7", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleVII/Chapter44/Section7",
  "M.G.L. c.44 s.7 (city/town borrowing purposes; two-thirds vote)"),
 ("MA_MGL_c44_s8", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleVII/Chapter44/Section8",
  "M.G.L. c.44 s.8 (borrowing purposes continued)"),
 ("MA_MGL_c59_s21C", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleIX/Chapter59/Section21C",
  "M.G.L. c.59 s.21C (Proposition 2-1/2; debt-exclusion ballot is a tax question)"),
 ("ME_30A_5772", "https://legislature.maine.gov/statutes/30-A/title30-Asec5772.html",
  "30-A M.R.S. 5772 (municipal bonds; town-meeting authorisation)"),
 ("NH_RSA_33-8", "https://www.gencourt.state.nh.us/rsa/html/III/33/33-8.htm",
  "N.H. RSA 33:8 (two-thirds/three-fifths meeting vote)"),
 ("NH_RSA_33-8-a", "https://www.gencourt.state.nh.us/rsa/html/III/33/33-8-a.htm",
  "N.H. RSA 33:8-a (ballot vote at SB2 meetings)"),
 # -- Part 2 · factual disagreements -----------------------------------------
 ("KY_Const_s157", "https://apps.legislature.ky.gov/Law/Constitution/Constitution/ViewConstitution?rsn=183",
  "Ky. Const. s.157 (tax-rate limits; voter assent for excess)"),
 ("KY_Const_s158", "https://apps.legislature.ky.gov/Law/Constitution/Constitution/ViewConstitution?rsn=184",
  "Ky. Const. s.158 (indebtedness limits)"),
 ("KY_KRS_ch66_index", "https://apps.legislature.ky.gov/law/statutes/chapter.aspx?id=37351",
  "KRS ch. 66 (Issuance of Bonds and Control of Funds) -- official section index"),
 ("VA_Const_artVII_s10", "https://law.lis.virginia.gov/constitution/article7/section10/",
  "Va. Const. art. VII s.10 (county referendum requirement; city/town exemption)"),
 # -- Part 3 · structural not-codables ---------------------------------------
 ("IL_65ILCS5_art8_div4",
  "https://www.ilga.gov/legislation/ILCS/details?MajorTopic=GOVERNMENT&Chapter=MUNICIPALITIES&ActName=Illinois%20Municipal%20Code.&ActID=802&ChapterID=14&ChapAct=65%20ILCS%205%2F&SeqStart=84900000&SeqEnd=87700000",
  "65 ILCS 5/ Art. 8 Div. 4 (Issuance of Bonds; 8-4-1 referendum + home-rule exemption)"),
 ("MN_475-58", "https://www.revisor.mn.gov/statutes/cite/475.58",
  "Minn. Stat. 475.58 (election required; enumerated exceptions)"),
 ("IA_384-24", "https://www.legis.iowa.gov/docs/code/384.24.pdf",
  "Iowa Code 384.24 (definitions; essential vs general corporate purpose)"),
 ("IA_384-25", "https://www.legis.iowa.gov/docs/code/384.25.pdf",
  "Iowa Code 384.25 (essential corporate purpose bonds; no election)"),
 ("IA_384-26", "https://www.legis.iowa.gov/docs/code/384.26.pdf",
  "Iowa Code 384.26 (general corporate purpose bonds; 60% election)"),
 ("IN_6-1.1-20_lawserver", "https://www.lawserver.com/law/state/indiana/in-code/indiana_code_6-1.1-20",
  "IC 6-1.1-20 chapter index (controlled projects; petition/remonstrance and referendum) -- iga.in.gov is a JS app that blocks automated retrieval"),
 ("IN_6-1.1-20-3.5_lawserver", "https://www.lawserver.com/law/state/indiana/in-code/indiana_code_6-1.1-20-3.5",
  "IC 6-1.1-20-3.5 (referendum threshold provision)"),
 ("NV_NRS_ch350", "https://www.leg.state.nv.us/NRS/NRS-350.html",
  "NRS ch. 350 (municipal obligations; debt commission path vs voted GO)"),
 ("PA_53PaCS_ch80", "https://www.legis.state.pa.us/WU01/LI/LI/CT/HTM/53/00.080..HTM",
  "53 Pa.C.S. ch. 80 (LGUDA: nonelectoral vs electoral debt)"),
 ("NY_LFN_33.00", "https://newyork.public.law/laws/n.y._local_finance_law_section_33.00",
  "N.Y. Local Finance Law 33.00 (bond resolution; vote requirements)"),
 ("NY_LFN_35.00", "https://newyork.public.law/laws/n.y._local_finance_law_section_35.00",
  "N.Y. Local Finance Law 35.00 (permissive referendum on petition)"),
 ("NY_LFN_36.00", "https://newyork.public.law/laws/n.y._local_finance_law_section_36.00",
  "N.Y. Local Finance Law 36.00 (referendum mechanics)"),
 ("NY_LFN_37.00", "https://newyork.public.law/laws/n.y._local_finance_law_section_37.00",
  "N.Y. Local Finance Law 37.00 (mandatory referendum cases)"),
 ("KS_ch10_index", "https://www.ksrevisor.gov/statutes/ksa_ch10.html",
  "K.S.A. ch. 10 (bonds and warrants) -- official section index"),
 ("KS_10-101", "https://www.ksrevisor.gov/statutes/chapters/ch10/010_001_0001.html",
  "K.S.A. 10-101 (general bond law; election provisions entry point)"),
 ("CT_CGS_ch109", "https://www.cga.ct.gov/current/pub/chap_109.htm",
  "C.G.S. ch. 109 (municipal bond issues; 7-369 ff.; charter-dependence)"),
 ("RI_45-12_index", "https://webserver.rilegislature.gov/Statutes/TITLE45/45-12/INDEX.htm",
  "R.I. Gen. Laws ch. 45-12 (indebtedness of towns and cities) -- section index"),
 ("RI_45-12-2", "https://webserver.rilegislature.gov/Statutes/TITLE45/45-12/45-12-2.htm",
  "R.I. Gen. Laws 45-12-2 (maximum indebtedness; charter/enabling-act structure)"),
 ("MD_LocalGovt_19-301",
  "https://mgaleg.maryland.gov/2025RS/Statute_Web/glg/19-301.pdf",
  "Md. Code, Local Gov't 19-301 (municipal borrowing authority; charter structure) -- official PDF; the StatuteText web page is a JS shell"),
 ("DE_title22_index", "https://delcode.delaware.gov/title22/index.html",
  "22 Del. C. -- municipalities title index (charter-by-charter structure)"),
 ("DE_title22_c008", "https://delcode.delaware.gov/title22/c008/index.html",
  "22 Del. C. ch. 8 (municipal borrowing provisions)"),
 ("HI_Const_full", "https://lrb.hawaii.gov/constitution",
  "Haw. Const. (art. VII: taxation and finance; county debt) -- LRB full text"),
 ("HI_HRS_ch47_index", "https://data.capitol.hawaii.gov/hrscurrent/Vol02_Ch0046-0115/HRS0047/HRS_0047-.htm",
  "HRS ch. 47 (county bonds) -- official section index"),
 # -- Part 4 · township / town-meeting column (MA/ME/NH texts above carry over)
 ("VT_24VSA_1755", "https://legislature.vermont.gov/statutes/section/24/053/01755",
  "24 V.S.A. 1755 (Vermont town bond vote -- town-meeting column)"),
 ("CT_CGS_ch98_7-194", "https://www.cga.ct.gov/current/pub/chap_098.htm",
  "C.G.S. ch. 98 (municipal powers; town-meeting structure -- township column)"),
]

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()

def fetch(url, out):
    r = subprocess.run(["curl", "-sL", "--cacert", CA, "-A", UA, "--max-time", "120",
                        "--retry", "2", "--retry-delay", "3",
                        "-o", out, "-w", "%{http_code}\t%{content_type}", url],
                       capture_output=True, text=True)
    code, ctype = (r.stdout.split("\t") + [""])[:2]
    return code.strip(), ctype.strip()

def html_to_pdf(html_path, pdf_path):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={pdf_path}", f"file://{os.path.abspath(html_path)}"],
                   check=True, capture_output=True, timeout=180)

def main():
    today = dt.date.today().isoformat()
    rows = []
    for stem, url, note in ITEMS:
        with tempfile.NamedTemporaryFile(delete=False) as t:
            tmp = t.name
        code, ctype = fetch(url, tmp)
        if code != "200" or not os.path.getsize(tmp):
            print(f"  FAIL {stem}: HTTP {code}")
            rows.append([stem, url, today, code, 0, "", "FETCH FAILED -- " + note])
            os.unlink(tmp); continue
        if "pdf" in ctype:
            final = os.path.join(HERE, stem + ".pdf")
            os.replace(tmp, final)
        else:
            html = os.path.join(HERE, stem + ".html")
            os.replace(tmp, html)
            final = os.path.join(HERE, stem + ".pdf")
            try:
                html_to_pdf(html, final)
            except Exception as e:
                print(f"  pdf-render failed for {stem} ({e}); html kept")
                final = html
        rows.append([stem, url, today, code, os.path.getsize(final), sha256(final), note])
        print(f"  ok {stem} ({os.path.getsize(final):,}B)")
    with open(os.path.join(HERE, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file_stem", "url", "retrieved", "http_status", "bytes", "sha256", "note"])
        w.writerows(rows)
    fails = [r for r in rows if r[3] != "200"]
    print(f"done: {len(rows)-len(fails)}/{len(rows)} archived, {len(fails)} failed")

if __name__ == "__main__":
    sys.exit(main())
