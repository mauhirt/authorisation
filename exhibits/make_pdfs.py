#!/usr/bin/env python3
"""Convert exhibit SVGs to PDF via the pre-installed headless chromium.
Wraps each SVG in a minimal HTML page sized to the SVG's viewBox so the PDF
page matches the figure exactly (no browser margins). Stdlib only."""
import os, re, subprocess, sys, tempfile, glob

OUT = "exhibits/out"
CANDIDATES = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))
CHROME = os.environ.get("CHROME_BIN") or (CANDIDATES[-1] if CANDIDATES else None)

def svg_size(path):
    head = open(path).read(2000)
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', head)
    if m:
        return float(m.group(1)), float(m.group(2))
    mw = re.search(r'width="(\d+(?:\.\d+)?)"', head)
    mh = re.search(r'height="(\d+(?:\.\d+)?)"', head)
    return float(mw.group(1)), float(mh.group(1))

def to_pdf(svg_path, pdf_path):
    w, h = svg_size(svg_path)
    # CSS px -> inches at 96dpi for --print-to-pdf page size
    win, hin = w / 96.0, h / 96.0
    svg = open(svg_path).read()
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"@page{{size:{win:.4f}in {hin:.4f}in;margin:0}}"
            f"html,body{{margin:0;padding:0}}svg{{display:block}}"
            f"</style></head><body>{svg}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html); tmp = fh.name
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", f"file://{tmp}"],
                       check=True, capture_output=True, timeout=120)
    finally:
        os.unlink(tmp)

def main():
    if not CHROME or not os.path.exists(CHROME):
        print("WARNING: headless chromium not found; skipping PDF generation "
              "(SVGs remain authoritative). Set CHROME_BIN to enable.")
        return 0
    svgs = sorted(glob.glob(f"{OUT}/*.svg"))
    for s in svgs:
        p = s[:-4] + ".pdf"
        to_pdf(s, p)
        print(f"  {os.path.basename(p)}  {os.path.getsize(p):,} bytes")
    print(f"pdfs done: {len(svgs)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
