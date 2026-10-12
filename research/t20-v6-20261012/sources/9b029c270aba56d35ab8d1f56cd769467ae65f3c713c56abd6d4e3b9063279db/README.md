# Apoautosis and Apoautotic Transductive Faculties
## Continuity, Re-realisation, and the Preservation of Future Capability

Standalone companion to *The Last Moat*, Third Edition. Version 1, 21 September 2026.

## Read

`Apoautosis_and_Transductive_Faculties_Companion.pdf` is the primary reading copy.
The manuscript has 29 pages, 15 main sections, four appendices and a bibliography.
It is a new paper, not Edition 4. The supplied Edition 3 and other source files
were not edited or replaced.

Its central subject is the distinction between a successful continuation event
and retention of the faculty needed for later re-realisations. It includes
contract-relative definitions, ordinary conditional proofs, finite counterexamples,
source/claim provenance and a bounded research agenda.

## Edit and build

The complete editable LaTeX is in `source/`. Run, from that directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

A TeX installation needs the standard packages named in `main.tex`, including
newtx, amsthm, mathtools, microtype, booktabs, longtable, tabularx, enumitem,
fancyhdr, xurl, hyperref and cleveref. No bibliography processor is needed.
The build produces `source/main.pdf`. Fonts are dependencies of the TeX
installation; no font files are distributed in this package.

## Reproduce the finite checks

Python 3.13.5 was used in this preparation. The checker uses the standard library
and no network or external services. From the package root:

```sh
python verification/check_examples.py --out verification/rerun_normal.json
python -O verification/check_examples.py --out verification/rerun_optimised.json
```

The supplied `results_normal.json` and `results_optimised.json` are byte-identical:
15 groups passed in both modes. The exceptions implementing checks are not
removed by `-O`. The suite enumerates stipulated mathematical examples; it does
not run an autonomous system, hardware migration, environment discovery,
replication, or the original source papers' verification suites.

## Evidence status

- Theorems in the paper have ordinary written conditional proofs.
- The finite checks are instance tests, not kernel verification.
- There has been no independent human or proof-assistant review of this manuscript.
- No physical apoautotic faculty, general interface discovery capability,
  historical mathematical priority, empirical superiority or meniscus break is claimed.
- The primary contribution is conceptual and mathematical synthesis, with
  inherited mechanisms and newly assembled expositions identified explicitly.
- `source_register.json` records the sources, reading scope and hashes where raw
  bytes were available. GF1 was read through extracted text only; raw-byte access
  was unavailable. The private source corpus is not included in this package.
- `REVIEW_NOTES.md` gives the scope of the authoring-stage review and its limits.
- `SHA256SUMS` covers the supplied deliverables, not this checksum file itself.
