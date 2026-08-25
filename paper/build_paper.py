#!/usr/bin/env python3
"""Compile the full working-paper PDF: paper/MANUSCRIPT.md (rewritten text of
record, with inline exhibit markers) + exhibits/out (journal exhibits, frozen
v3) + Appendices H and V from paper/WHO_MUST_AGREE_EMPIRICS_FULL.md.

Markers understood in the manuscript:
  [[EX:stem]]           -> \\input{exhibits/out/stem.tex} at that point
  [[FIG:stem|Caption.]] -> numbered figure with exhibits/out/stem.pdf

Run from the repo root: python3 paper/build_paper.py
Output: paper/WHO_MUST_AGREE_DRAFT.pdf
"""
import datetime as dt, os, re, subprocess, sys

SRC = "paper/MANUSCRIPT.md"
APPX_SRC = "paper/WHO_MUST_AGREE_EMPIRICS_FULL.md"
BUILD = "paper/build"
OUT_PDF = "paper/WHO_MUST_AGREE_DRAFT.pdf"
os.makedirs(BUILD, exist_ok=True)

UNI = [
    ("τ₀", r"$\tau_0$"), ("–", "--"), ("−", r"$-$"), ("×", r"$\times$"),
    ("·", r"$\cdot$"), ("§", r"\S"), ("±", r"$\pm$"), ("≤", r"$\le$"),
    ("≥", r"$\ge$"), ("τ", r"$\tau$"), ("θ", r"$\theta$"), ("β", r"$\beta$"),
    ("→", r"$\rightarrow$"), ("↔", r"$\leftrightarrow$"), ("…", r"\dots{}"),
    ("≈", r"$\approx$"), ("½", r"$\tfrac{1}{2}$"), ("∩", r"$\cap$"),
    ("∧", r"$\wedge$"), ("₀", r"$_0$"), ("ρ", r"$\rho$"), ("Δ", r"$\Delta$"),
]

def esc(s):
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\^{}")]:
        s = s.replace(a, b)
    for a, b in UNI:
        s = s.replace(a, b)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", s)
    s = re.sub(r"`([^`]+)`", r"\\texttt{\1}", s)
    return s

def figure_block(stem, caption):
    return [r"\begin{figure}[!htbp]\centering",
            f"\\includegraphics[width=0.92\\linewidth]{{exhibits/out/{stem}.pdf}}",
            f"\\caption{{{esc(caption)}}}", r"\end{figure}"]

def table_tex(rows, aligns):
    ncol = len(rows[0])
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    maxw = [max(len(r[i]) for r in rows) for i in range(ncol)]
    wide = any(w > 42 for w in maxw)
    if wide:
        tot = sum(min(w, 60) for w in maxw)
        spec = "".join(
            f"p{{{max(0.055, min(w,60)/tot*0.93):.3f}\\linewidth}}" for w in maxw)
    else:
        spec = "".join("r" if a == "r" else ("c" if a == "c" else "l")
                       for a in aligns[:ncol]) or "l" * ncol
    L = [r"{\footnotesize", f"\\begin{{longtable}}{{@{{}}{spec}@{{}}}}",
         r"\toprule",
         " & ".join(esc(c) for c in rows[0]) + r" \\", r"\midrule",
         r"\endhead"]
    for r in rows[1:]:
        L.append(" & ".join(esc(c) for c in r) + r" \\")
    L += [r"\bottomrule", r"\end{longtable}", "}"]
    return L

def convert(md_lines):
    """Paragraph-based conversion so inline markup (**bold**) survives source
    line wraps."""
    out, i, in_list, para = [], 0, False, []

    def flush():
        if para:
            out.append(esc(" ".join(para))); out.append("")
            para.clear()

    def end_list():
        nonlocal in_list
        if in_list:
            out.append(r"\end{itemize}"); in_list = False

    while i < len(md_lines):
        ln = md_lines[i].rstrip()
        m = re.match(r"\[\[EX:([\w.-]+)\]\]", ln.strip())
        if m:
            flush(); end_list()
            out.append(f"\\input{{exhibits/out/{m.group(1)}.tex}}")
            i += 1; continue
        m = re.match(r"\[\[FIG:([\w.-]+)\|(.+)\]\]", ln.strip())
        if m:
            flush(); end_list()
            out += figure_block(m.group(1), m.group(2))
            i += 1; continue
        if not ln.strip():
            flush(); end_list()
            i += 1; continue
        if ln.strip() in ("---", "***"):
            flush(); end_list()
            out.append(r"\medskip"); i += 1; continue
        if ln.startswith("|") and ln.rstrip().endswith("|"):
            flush(); end_list()
            rows, aligns = [], None
            while i < len(md_lines) and md_lines[i].strip().startswith("|") \
                    and md_lines[i].rstrip().endswith("|"):
                cells = [c.strip() for c in md_lines[i].strip().strip("|").split("|")]
                if set("".join(cells)) <= set("-: "):
                    aligns = ["r" if c.endswith(":") and not c.startswith(":")
                              else ("c" if c.startswith(":") and c.endswith(":") else "l")
                              for c in cells]
                else:
                    rows.append(cells)
                i += 1
            out += table_tex(rows, aligns or ["l"] * len(rows[0]))
            continue
        if ln.startswith("> "):
            flush(); end_list()
            buf = []
            while i < len(md_lines) and md_lines[i].startswith("> "):
                buf.append(md_lines[i][2:].rstrip()); i += 1
            out.append(r"{\small\itshape " + esc(" ".join(buf)) + "}")
            continue
        if ln.startswith("### "):
            flush(); end_list()
            out.append(r"\subsection*{" + esc(ln[4:]) + "}")
        elif ln.startswith("## "):
            flush(); end_list()
            out.append(r"\section*{" + esc(ln[3:]) + "}")
        elif ln.startswith("# "):
            flush(); end_list()
            out.append(r"\clearpage\section*{" + esc(ln[2:]) + "}")
        elif ln.startswith("- "):
            flush()
            if not in_list:
                out.append(r"\begin{itemize}\setlength{\itemsep}{1pt}")
                in_list = True
            # pull continuation lines of this bullet into one item
            item = [ln[2:]]
            while (i + 1 < len(md_lines) and md_lines[i+1].strip()
                   and not md_lines[i+1].startswith(("- ", "#", "|", "> ", "[["))
                   and md_lines[i+1].strip() not in ("---", "***")):
                i += 1; item.append(md_lines[i].strip())
            out.append(r"\item " + esc(" ".join(item)))
        else:
            para.append(ln.strip())
        i += 1
    flush(); end_list()
    return out

# Appendix exhibits, in citation order (numbers become A1, A2, ... in sequence).
APPX_TABLES = [
    ("A1_battery",            "A1"),
    ("A3_state_by_state",     "A2"),
    ("A2_placebo_thresholds", "A3"),
    ("AC1_coverage",          "A4"),
    ("A5a_menu",              "A5"),
    ("A5b_submerged",         "A6"),
    ("A5d_channel_sorting",   "A7"),
    ("A5e_firststage_raw",    "A8"),
    ("R3_interactions",       "A9"),
    ("A6a_chain",             "A10"),
    ("A6c_ratecap",           "A11"),
    ("A7_blocked",            "A12"),
    ("A9_validation",         "A13"),
    ("AP1_county_partisanship", "A14"),
]
APPX_FIGS = [("A1a_horizons", "Effect by issuance horizon: RBC estimate and robust CI for windows of one to six years."),
             ("A1b_bandwidth", "Bandwidth sensitivity: RBC estimate (solid), conventional (dashed) and robust CI across bandwidths h of 3 to 15pp.")]

def main():
    md = open(SRC).read().splitlines()
    body_start = next(j for j, l in enumerate(md) if l.strip() == "---")
    preface = [l for l in md[1:body_start] if l.strip()]
    main_tex = convert(md[body_start + 1:])

    # Appendices H and V from the consolidated round-3/4 document.
    appx = open(APPX_SRC).read().splitlines()
    h_start = next(j for j, l in enumerate(appx) if l.startswith("# Appendix H"))
    appx_tex = convert(appx[h_start:])

    L = [r"\documentclass[11pt]{article}",
         r"\usepackage[margin=1.05in]{geometry}",
         r"\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern}",
         r"\usepackage{booktabs,longtable,graphicx,amsmath,caption,textcomp,array}",
         r"\usepackage[hidelinks]{hyperref}",
         r"\newcommand{\sig}[1]{${}^{#1}$}",
         r"\captionsetup{font=small,labelfont=bf}",
         r"\setlength{\parskip}{3pt plus 1pt}",
         r"\begin{document}",
         r"\begin{titlepage}\centering\vspace*{2.2cm}",
         r"{\LARGE\bfseries Who Must Agree\par}\vspace{0.5cm}",
         r"{\large Bond authorisation rules as coalition requirements\par}\vspace{0.35cm}",
         r"{\normalsize Empirical sections and exhibits --- working conference draft\par}\vspace{1.1cm}",
         f"{{\\normalsize Compiled {dt.date.today().strftime('%d %B %Y')} "
         r"from the committed analysis record (corpus package v3, frozen).\par}",
         r"\vspace{1.0cm}\begin{minipage}{0.82\linewidth}\small\emph{",
         esc(" ".join(l.strip("*") for l in preface).strip()),
         r"}\end{minipage}",
         r"\vfill {\small Reading paragraphs under exhibits are drafting aids,"
         r" marked strippable for submission.\par}",
         r"\end{titlepage}"]
    L += main_tex
    L += [r"\clearpage",
          r"\section*{Appendix tables and figures}",
          r"\setcounter{table}{0}\renewcommand{\thetable}{A\arabic{table}}",
          r"\setcounter{figure}{0}\renewcommand{\thefigure}{A\arabic{figure}}"]
    for stem, _ in APPX_TABLES:
        L += [f"\\input{{exhibits/out/{stem}.tex}}", r"\clearpage"]
    for stem, cap in APPX_FIGS:
        L += figure_block(stem, cap)
    L += [r"\clearpage"]
    L += appx_tex
    L += [r"\end{document}"]

    tex = os.path.join(BUILD, "main.tex")
    open(tex, "w").write("\n".join(L) + "\n")
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            f"-output-directory={BUILD}", tex],
                           capture_output=True, text=True)
    if not os.path.exists(os.path.join(BUILD, "main.pdf")):
        print(r.stdout[-3000:]); sys.exit(1)
    errs = [l for l in r.stdout.splitlines() if l.startswith("!")]
    os.replace(os.path.join(BUILD, "main.pdf"), OUT_PDF)
    print(f"built {OUT_PDF}; latex errors: {len(errs)}")
    for e in errs[:10]:
        print(" ", e)

if __name__ == "__main__":
    main()
