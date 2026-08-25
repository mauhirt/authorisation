#!/usr/bin/env python3
"""Assemble the full paper as an Overleaf-ready package and zip it.

Sources: paper/INTRO_ARGUMENT_HISTORY.md (owner sections 1-3),
paper/MANUSCRIPT.md (empirical sections 4-9), exhibits/out (tables/figures),
paper/references.tex (best-effort, to verify).

Output: paper/overleaf/{main.tex, sections/*.tex, tables/*.tex, figures/*.pdf,
README.md} and paper/who_must_agree_overleaf.zip.

Run from the repo root: python3 paper/build_overleaf.py
"""
import datetime as dt, os, re, shutil, subprocess, sys
import importlib.util

spec = importlib.util.spec_from_file_location("bp", "paper/build_paper.py")
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
esc, table_tex = bp.esc, bp.table_tex

PKG = "paper/overleaf"
for d in ("", "sections", "tables", "figures"):
    os.makedirs(os.path.join(PKG, d), exist_ok=True)

FIG_LABEL = {"F0_volume": "fig:volume", "F4_consent_map": "fig:map",
             "F5_density": "fig:density", "F1_rd": "fig:rd",
             "F2_event_study": "fig:event", "F3_wedge": "fig:wedge",
             "A1a_horizons": "fig:horizons", "A1b_bandwidth": "fig:bandwidth"}

MAIN_TABLES = ["T_genealogy", "T1_sample", "D1_how_authorised", "D2_what_for",
               "D3_function_voted", "A5c_coalitions", "R1_firststage",
               "R2_substitution", "T2_covariate_continuity", "T3_main_results",
               "T5_response", "T7_fork_menu", "T6_moderators", "A4_agenda"]
APPX_TABLES = ["A1_battery", "A3_state_by_state", "A2_placebo_thresholds",
               "AC1_coverage", "A5a_menu", "A5b_submerged", "A6a_chain",
               "A9_validation"]
MAIN_FIGS = ["F0_volume", "F4_consent_map", "F5_density", "F1_rd",
             "F2_event_study", "F3_wedge"]
APPX_FIGS = [("A1a_horizons", "Effect by issuance horizon: RBC estimate and robust confidence interval for windows of one to six years."),
             ("A1b_bandwidth", "Bandwidth sensitivity: RBC estimate (solid), conventional (dashed) and robust confidence interval across bandwidths of 3 to 15pp.")]

# hard number strings in the two source documents -> labels (descending order!)
REFMAP = [
    ("Appendix Figure A1", "[[F:horizons]]"),
    ("Appendix Table A13", "[[T:validation]]"),
    ("Appendix Table A10", "[[T:chain]]"),
    ("Appendix Table A6", "[[T:submerged]]"),
    ("Appendix Table A5", "[[T:menu]]"),
    ("Appendix Table A4", "[[T:ac1]]"),
    ("Appendix Table A3", "[[T:placebo]]"),
    ("Appendix Table A2", "[[T:bystate]]"),
    ("Appendix Table A1", "[[T:battery]]"),
    ("Table 13", "[[T:agenda]]"), ("Table 12", "[[T:binds]]"),
    ("Table 11", "[[T:fork]]"), ("Table 10", "[[T:response]]"),
    ("Table 9", "[[T:main]]"), ("Table 8", "[[T:continuity]]"),
    ("Table 7", "[[T:r2]]"), ("Table 6", "[[T:r1]]"),
    ("Table 5", "[[T:coalitions]]"), ("Table 4", "[[T:d3]]"),
    ("Table 3", "[[T:d2]]"), ("Table 2", "[[T:d1]]"),
    ("Table 1", "[[T:sample]]"),
    ("Figure 5", "[[F:wedge]]"), ("Figure 4", "[[F:event]]"),
    ("Figure 3", "[[F:rd]]"), ("Figure 2", "[[F:density]]"),
    ("Figure 1", "[[F:map]]"),
    ("Figure [[VOLREF]]", "[[F:volume]]"),
    ("Figure [[MAPREF]]", "[[F:map]]"),
    ("Table [[GENEALOGY]]", "[[T:genealogy]]"),
]

def resolve_markers(t):
    t = re.sub(r"\[\[T:(\w+)\]\]", r"Table~\\ref{tab:\1}", t)
    t = re.sub(r"\[\[F:(\w+)\]\]", r"Figure~\\ref{fig:\1}", t)
    return t

def quotes(t):
    return re.sub(r'"([^"\n]+)"', r"``\1''", t)

def figure_block(stem, caption):
    lab = FIG_LABEL.get(stem, f"fig:{stem}")
    return [r"\begin{figure}[!htbp]\centering",
            f"\\includegraphics[width=0.9\\linewidth]{{figures/{stem}.pdf}}",
            f"\\caption{{{esc(caption)}}}\\label{{{lab}}}",
            r"\end{figure}"]

def convert(md_lines):
    """Paragraph-based md -> tex, numbered sections, markers, quotes."""
    out, i, para = [], 0, []
    def flush():
        if para:
            out.append(quotes(esc(" ".join(para)))); out.append("")
            para.clear()
    while i < len(md_lines):
        ln = md_lines[i].rstrip()
        m = re.match(r"\[\[EX:([\w.-]+)\]\]", ln.strip())
        if m:
            flush(); out.append(f"\\input{{tables/{m.group(1)}.tex}}")
            i += 1; continue
        m = re.match(r"\[\[FIG:([\w.-]+)\|(.+)\]\]", ln.strip())
        if m:
            flush(); out += figure_block(m.group(1), m.group(2))
            i += 1; continue
        if not ln.strip() or ln.strip() in ("---", "***"):
            flush(); i += 1; continue
        if ln.startswith("### "):
            flush()
            t = re.sub(r"^\d+\.\d+\s*", "", ln[4:])
            out.append(r"\subsection{" + esc(t) + "}")
        elif ln.startswith("## "):
            flush()
            t = re.sub(r"^\d+\s*[·.]\s*", "", ln[3:])
            out.append(r"\section{" + esc(t) + "}")
        elif ln.startswith("# "):
            pass  # document-level headers dropped
        else:
            para.append(ln.strip())
        i += 1
    flush()
    return out

def load(path, apply_refmap=True):
    t = open(path).read()
    if apply_refmap:
        for a, b in REFMAP:
            t = t.replace(a, b)
    return t.splitlines()

# ---------------- genealogy table ----------------
GEN = r"""% owner-supplied genealogy (Section 3); [V] cells to resolve against the origins file
\begin{table}[!htbp]\centering\footnotesize
\caption{The genealogy of the focal states' rules}\label{tab:genealogy}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.09\linewidth}>{\raggedright\arraybackslash}p{0.16\linewidth}>{\raggedright\arraybackslash}p{0.13\linewidth}>{\raggedright\arraybackslash}p{0.17\linewidth}>{\raggedright\arraybackslash}p{0.15\linewidth}>{\raggedright\arraybackslash}p{0.18\linewidth}@{}}
\toprule
State & Rule (current) & Origin & Authoring coalition & Veto-holder as written & First major exit \\
\midrule
California & 66.7\% GO; 55\% school (2000) & Const.\ 1879, art.\ [V] & Taxpayer / anti-corporate convention & Two-thirds of electors & Special fund doctrine [V: date] \\ \addlinespace
Kentucky & Voter assent above \S 157 limits & Const.\ 1891, \S\S 157--158 & Taxpayer convention & Two-thirds of voters [V: confirm share] & Holding-company / revenue devices [V] \\ \addlinespace
Texas & Simple majority (GO, by class) & Const.\ 1876, art.\ XI [V] & Post-Reconstruction retrenchment convention [V] & Majority of qualified voters & Statutory districts; landowner-franchise districts (upheld, \emph{Ball v.\ James} 1981) \\ \addlinespace
Wisconsin & Majority; ch.\ 67 referenda & Stat.\ ch.\ 67 [V: origin date] & [V] & Majority of electors & Petition and exemption classes [V] \\ \addlinespace
Louisiana & Majority; bond commission & Const.\ [V: date] & [V] & Majority of electors voting & State commission channel [V] \\
\bottomrule
\end{tabular}
\begin{minipage}{0.96\linewidth}\vspace{2pt}\scriptsize
\emph{Notes:} Rows complete to the paper's archived statutory texts; [V] cells resolve against the origins file before circulation. The table's point survives its pending cells: each rule has a date, a coalition, and a named public.
\end{minipage}
\end{table}
"""

def main():
    open(os.path.join(PKG, "tables", "T_genealogy.tex"), "w").write(GEN)
    # copy exhibit tables and figures
    for t in MAIN_TABLES + APPX_TABLES:
        if t == "T_genealogy":
            continue
        src = f"exhibits/out/{t}.tex"
        tex = open(src).read().replace("exhibits/out/", "tables/")
        open(os.path.join(PKG, "tables", f"{t}.tex"), "w").write(tex)
    for f in MAIN_FIGS + [s for s, _ in APPX_FIGS]:
        shutil.copy(f"exhibits/out/{f}.pdf", os.path.join(PKG, "figures", f"{f}.pdf"))

    intro = convert(load("paper/INTRO_ARGUMENT_HISTORY.md"))
    md = load("paper/MANUSCRIPT.md")
    body_start = next(j for j, l in enumerate(md) if l.strip() == "---")
    emp = convert(md[body_start + 1:])
    body = [resolve_markers(l) for l in intro + emp]

    # split into per-section files
    files, cur, idx = [], [], 0
    names = ["introduction", "argument", "history", "data", "landscape",
             "threshold", "response", "binds", "agenda"]
    for l in body:
        if l.startswith(r"\section{") and cur:
            files.append(cur); cur = []
        cur.append(l)
    files.append(cur)
    sec_inputs = []
    for k, chunk in enumerate(files):
        name = names[k] if k < len(names) else f"section{k+1}"
        open(os.path.join(PKG, "sections", f"{k+1:02d}_{name}.tex"), "w").write("\n".join(chunk) + "\n")
        sec_inputs.append(f"\\input{{sections/{k+1:02d}_{name}}}")

    shutil.copy("paper/references.tex", os.path.join(PKG, "sections", "references.tex"))

    appx = [r"\clearpage", r"\appendix",
            r"\section*{Appendix: additional tables and figures}",
            r"\setcounter{table}{0}\renewcommand{\thetable}{A\arabic{table}}",
            r"\setcounter{figure}{0}\renewcommand{\thefigure}{A\arabic{figure}}"]
    for t in APPX_TABLES:
        appx += [f"\\input{{tables/{t}.tex}}", r"\clearpage"]
    for stem, cap in APPX_FIGS:
        appx += figure_block(stem, cap)
    open(os.path.join(PKG, "sections", "appendix.tex"), "w").write("\n".join(appx) + "\n")

    main_tex = "\n".join([
        r"% Who Must Agree -- Overleaf package (auto-assembled; see README.md)",
        r"\documentclass[12pt]{article}",
        r"\usepackage[margin=1.1in]{geometry}",
        r"\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern}",
        r"\usepackage{booktabs,longtable,graphicx,amsmath,caption,textcomp,array,setspace}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\newcommand{\sig}[1]{${}^{#1}$}",
        r"\captionsetup{font=small,labelfont=bf}",
        r"\setlength{\parskip}{2pt plus 1pt}",
        r"\onehalfspacing",
        r"\title{Who Must Agree\\[6pt]\large Consent Requirements and the Provision of Local Public Goods}",
        r"\author{}",  # add author block
        r"\date{\today\\[4pt]\normalsize Working draft. [PENDING] marks and [V] marks are the authors' own verification flags.}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        r"\noindent American local governments must often ask their voters before borrowing, under rules written into nineteenth-century constitutions. Using a new corpus of 258,762 bond offering documents that states the legal authority behind every issue, this paper measures, for the first time in all fifty states, who actually authorises local debt: voters approve 32 cents of every borrowed dollar, governing boards 54, statutes the rest, with the voted share concentrated almost entirely in school districts. At the statutory thresholds, 11,889 close bond elections identify what consent causes: authorisation raises issuance immediately and durably, doubles borrowing, and moves construction nearly one-for-one. Refusal, followed forward, is a queue rather than a wall: most refused measures return within a year at the same amount and pass, and fewer than one in five blocked projects die. The requirement binds only where governments lack exits into unvoted debt, and hardest where the electorate is propertied, old and homogeneous. The oldest consent institution in American fiscal law survives by leaking: whoever can leave its jurisdiction does, and what remains under it is the unchargeable core of the local state.",
        r"\end{abstract}",
        "",
        *sec_inputs,
        r"\input{sections/references}",
        r"\input{sections/appendix}",
        r"\end{document}",
    ]) + "\n"
    open(os.path.join(PKG, "main.tex"), "w").write(main_tex)

    open(os.path.join(PKG, "README.md"), "w").write(f"""# Who Must Agree -- Overleaf package

Assembled {dt.date.today().isoformat()} from the analysis repository
(corpus package v3, frozen). Upload this folder (or the zip) to Overleaf and
compile `main.tex` with pdfLaTeX.

## Layout
- `main.tex` -- preamble, title, abstract, inputs everything
- `sections/01..09_*.tex` -- one file per section (1-3 owner text; 4-9 empirics)
- `sections/references.tex` -- BEST-EFFORT auto-drafted entries. Verify every
  entry; `[details to verify]` marks the ones the assistant could not confirm.
  The text cites the Yale piece as 1962 in Section 2.2 and Morris 1958 in
  Section 3 -- reconcile.
- `sections/appendix.tex` -- 8 tables + 2 figures (kept light)
- `tables/*.tex`, `figures/*.pdf` -- generated by `make exhibits` in the repo;
  do not hand-edit (regenerate instead)

## Numbers and flags
- Every empirical number traces to a committed results file in the repository
  (see analysis/ANALYSIS_REVIEW.md there). Rule coefficients are PRELIMINARY
  (pass-1 coding) pending the human verification pass; [PENDING]/[V] flags in
  the text are deliberate and should be resolved, not deleted, before
  circulation.
- Cross-references use \\ref throughout; numbering is stable under reordering.
- Reading paragraphs under tables are drafting aids marked strippable
  (%% BEGIN READING ... %% END READING).
""")

    # zip
    zip_path = "paper/who_must_agree_overleaf.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    subprocess.run(["zip", "-qr", os.path.abspath(zip_path), "."], cwd=PKG, check=True)

    # compile check (mirrors Overleaf)
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
                           cwd=PKG, capture_output=True, text=True)
    ok = os.path.exists(os.path.join(PKG, "main.pdf"))
    errs = [l for l in r.stdout.splitlines() if l.startswith("!")]
    log = open(os.path.join(PKG, "main.log")).read()
    pages = re.findall(r"Output written on .* \((\d+) pages", log)
    print(f"package built; compile ok={ok}, pages={pages}, errors={len(errs)}")
    for e in errs[:8]:
        print(" ", e)
    und = re.findall(r"Reference `([^']+)' on page", log)
    if und:
        print("undefined refs:", sorted(set(und)))

if __name__ == "__main__":
    sys.exit(main())
