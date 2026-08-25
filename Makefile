# Who Must Agree -- build targets.
# `make exhibits` regenerates every journal exhibit (CSV + .tex + SVG + PDF)
# from the FROZEN corpus package v3 (inputs/corpus/, pinned in README.md) and
# the committed analysis caches. No manual edits to exhibits/out/.

PY := python3

.PHONY: exhibits caches clean-exhibits

exhibits:
	$(PY) exhibits/build_rd_tables.py
	$(PY) exhibits/build_desc_tables.py
	$(PY) exhibits/build_figures.py
	$(PY) exhibits/make_pdfs.py

# Rebuild the analysis caches from the frozen v3 package (only needed if
# analysis/*.csv.gz caches are absent; exhibits read the caches).
caches:
	$(PY) analysis/cache_inputs.py
	$(PY) analysis/build_b3.py

clean-exhibits:
	rm -rf exhibits/out
