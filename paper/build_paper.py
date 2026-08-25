#!/usr/bin/env python3
"""Compile the full working-paper PDF from what exists now:
paper/WHO_MUST_AGREE_EMPIRICS_FULL.md (text of record) + exhibits/out (journal
exhibits, frozen v3). Markdown -> LaTeX conversion is deliberately narrow --
it handles exactly the constructs used in the committed documents.
Run from the repo root: python3 paper/build_paper.py
Output: paper/WHO_MUST_AGREE_DRAFT.pdf
"""
import datetime as dt, os, re, subprocess, sys

SRC = "paper/WHO_MUST_AGREE_EMPIRICS_FULL.md"
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

def table_tex(rows, aligns):
    """Longtable with p-columns sized by content when cells are wide."""
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
    out, i, in_list = [], 0, False
    skip_until_next_h2 = False
    while i < len(md_lines):
        ln = md_lines[i].rstrip()
        if ln.startswith("### Exhibit inventory"):
            # planning artefact superseded by the built exhibits
            skip_until_next_h2 = True
            i += 1; continue
        if skip_until_next_h2:
            if ln.startswith("# ") or ln.startswith("## "):
                skip_until_next_h2 = False
            else:
                i += 1; continue
        if in_list and not ln.startswith("- "):
            out.append(r"\end{itemize}"); in_list = False
        if not ln.strip():
            out.append(""); i += 1; continue
        if ln.strip() in ("---", "***"):
            out.append(r"\medskip"); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(md_lines) and md_lines[i].strip().startswith("|"):
                cells = [c.strip() for c in md_lines[i].strip().strip("|").split("|")]
                if set("".join(cells)) <= set("-: "):
                    aligns = ["r" if c.endswith(":") and not c.startswith(":")
                              else ("c" if c.startswith(":") and c.endswith(":") else "l")
                              for c in cells]
                else:
                    rows.append(cells)
                i += 1
            if "aligns" not in dir():
                aligns = ["l"] * len(rows[0])
            out += table_tex(rows, aligns if 'aligns' in dir() else ["l"]*len(rows[0]))
            continue
        if ln.startswith("### "):
            out.append(r"\subsection*{" + esc(ln[4:]) + "}")
        elif ln.startswith("## "):
            out.append(r"\section*{" + esc(ln[3:]) + "}")
        elif ln.startswith("# "):
            out.append(r"\clearpage\section*{" + esc(ln[2:]) + "}")
        elif ln.startswith("> "):
            # exhibit-callout blockquotes: render as small italic placement notes
            buf = []
            while i < len(md_lines) and md_lines[i].startswith("> "):
                buf.append(md_lines[i][2:].rstrip()); i += 1
            out.append(r"{\small\itshape " + esc(" ".join(buf)) + "}")
            continue
        elif ln.startswith("- "):
            if not in_list:
                out.append(r"\begin{itemize}\setlength{\itemsep}{1pt}")
                in_list = True
            out.append(r"\item " + esc(ln[2:]))
        else:
            out.append(esc(ln))
        i += 1
    if in_list:
        out.append(r"\end{itemize}")
    return out

MAIN_TABLES = ["T1_sample", "T2_covariate_continuity", "T3_main_results",
               "T4_first_stage", "T5_response", "T6_moderators", "T7_fork_menu"]
MAIN_FIGS = [("F1_rd", "Figure 1. Issuance at the authorisation threshold"),
             ("F2_event_study", "Figure 2. Event study: issuance by year relative to the vote"),
             ("F3_wedge", "Figure 3. The cumulative wedge"),
             ("F4_consent_map", "Figure 4. The consent map: voted share of local new-money dollars"),
             ("F5_density", "Figure 5. Running-variable density by state")]
APP_TABLES = ["A1_battery", "A2_placebo_thresholds", "A3_state_by_state",
              "A4_agenda", "A5a_menu", "A5b_submerged", "A5c_coalitions",
              "A5d_channel_sorting", "A5e_firststage_raw", "A6a_chain",
              "A6c_ratecap", "A7_blocked", "A9_validation"]
APP_FIGS = [("A1a_horizons", "Figure A1a. RD estimate by issuance horizon"),
            ("A1b_bandwidth", "Figure A1b. Bandwidth sensitivity")]

def figure_block(stem, caption):
    return [r"\begin{figure}[!htbp]\centering",
            f"\\includegraphics[width=0.92\\linewidth]{{exhibits/out/{stem}.pdf}}",
            f"\\caption*{{{esc(caption)}}}", r"\end{figure}"]

def main():
    md = open(SRC).read().splitlines()
    # split off the title header (first heading + preface up to the rule)
    body_start = next(j for j, l in enumerate(md) if l.strip() == "---")
    preface = [l for l in md[1:body_start] if l.strip()]
    # split main text vs appendices at the first top-level appendix heading
    app_start = next(j for j, l in enumerate(md) if l.startswith("# Appendix"))
    main_tex = convert(md[body_start + 1:app_start])
    app_tex = convert(md[app_start:])

    L = [r"\documentclass[11pt]{article}",
         r"\usepackage[margin=1.05in]{geometry}",
         r"\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern}",
         r"\usepackage{booktabs,longtable,graphicx,amsmath,caption,textcomp}",
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
         r"\vfill {\small Sections 1--3 (theory and institutional framework) are"
         r" maintained separately and are not part of this compile. Reading"
         r" paragraphs under each exhibit are drafting aids, marked strippable"
         r" for submission.\par}",
         r"\end{titlepage}"]
    L += main_tex
    L += [r"\clearpage", r"\section*{Main tables}"]
    for t in MAIN_TABLES:
        L += [f"\\input{{exhibits/out/{t}.tex}}", r"\clearpage"]
    L += [r"\section*{Main figures}"]
    for stem, cap in MAIN_FIGS:
        L += figure_block(stem, cap)
    L += [r"\clearpage", r"\section*{Appendix exhibits (specification battery and landscape detail)}",
          r"\setcounter{table}{0}\renewcommand{\thetable}{A\arabic{table}}",
          r"\setcounter{figure}{0}\renewcommand{\thefigure}{A\arabic{figure}}"]
    for t in APP_TABLES:
        L += [f"\\input{{exhibits/out/{t}.tex}}"]
        if t in ("A2_placebo_thresholds", "A5c_coalitions", "A6c_ratecap"):
            L += [r"\clearpage"]
    for stem, cap in APP_FIGS:
        L += figure_block(stem, cap)
    L += [r"\clearpage"]
    L += app_tex
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
