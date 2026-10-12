# The Last Moat — Edition 3

**Physical Realisability, Cross-Substrate Communication, and Holarchic Agency**  
Research manuscript, 10 September 2026, v3.0. AI-assisted draft developed from a user-originated research dialogue. Not submitted to arXiv, not peer reviewed, and not experimentally validated as a framework.

## Contents and evidence level

The PDF has 58 pages and 39 references. There are 29 named mathematical results with written proofs: 21 retained from Edition 2 and eight added to this exposition. This is not a claim of 29 or eight historically new theorems. The package executes 42 top-level checks: 27 inherited and 15 added. Counts do not measure independent scientific corroboration.

The principal new worked object is a two-state parity-memory contract, a digital implementation, and a **stipulated** bistable reset/ODE model. The paper proves the sampled correspondence and model-level state-preserving handovers under declared bounds. Both numerical implementations in this package run on conventional computing hardware. No physical alternative-substrate execution, laboratory calibration, paired hardware handover, or autonomous substrate acquisition was performed.

A second worked object shows that two correct state machines and a working message channel can nevertheless fail continuation when the exported state loses a distinction needed for future outputs. A fully informed conventional contract assessment reaches the same verdict as its orthemic annotation. The demonstration does not claim empirical superiority over conventional methods.

## Read or edit

- `the_last_moat_e3.tex` is the modular manuscript entry point.
- The included `.tex` modules supply all its dependencies.
- `manuscript_flattened.tex` is an equivalent single-file manuscript, including references.
- `references.tex` contains the manually maintained numbered bibliography.
- `CHANGES.md` records the post-Edition-2 changes.
- `source_register.json` distinguishes fresh primary-source inspection from inherited source coverage.
- `proof_register.json` maps every named result to its current page and number, lineage, and proof/check scope.
- `REVIEW_SCOPE.md` and `PROOF_REVIEW_NOTES.md` state what the preparation verified and what it did not.
- `build_audit.json` records the final clean-build and PDF checks.
- `MANIFEST.sha256` authenticates the files in this archive except the manifest itself. It is an integrity record, not scientific certification.

The accompanying PDF is delivered separately as `The_Last_Moat_Edition_3.pdf`.

## Reproduce the checks

Use Python 3.10 or later. The verified environment was Python 3.13.5. The three checker files use only Python's standard library and must remain in the same directory. No network requests, hardware access, device probing, or package downloads are performed.

```sh
python -B verify_models.py --output verification_results.json
python -B -O verify_models.py --output verification_results_optimized.json
```

The script exits nonzero on any failed check. Its guards remain active with Python optimisation enabled. `verify_models_e2.py` and `verify_models_v1.py` preserve the inherited functions used by the Edition 3 harness; they are not separately endorsed physical implementations.

The supplied reports show **42/42 passing** in both modes with identical individual check results. The report metadata records each exact checker hash and the Python optimisation level. Numerical trajectory sampling and step refinement are consistency checks, not a rigorous integration error certificate. The continuous model guarantee comes from the written invariant-region proof.

## Build the PDF

A standard TeX installation with `latexmk` and `pdflatex` is required. Packages include Latin Modern, geometry, AMS mathematics, mathtools, mathrsfs, microtype, booktabs, array, longtable, enumitem, needspace, natbib, hyperref, xurl, and fancyhdr.

Modular build:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error the_last_moat_e3.tex
```

Single-file alternative:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript_flattened.tex
```

The two clean builds produced the same 58-page extracted text and no LaTeX warnings, overfull boxes, or underfull boxes. PDF binary bytes can differ because of job names, timestamps, or metadata. No font files or third-party paper PDFs are distributed in this archive.

## Interpret results correctly

Written mathematical proof, model-level numerical checking, published physical evidence, a proposed laboratory protocol, and independent experimental validation are different evidence classes. The literature review is focused, not exhaustive. Individual source records state when only an abstract or selected pages were inspected. Neither the external 2026 Navier–Stokes proof nor a Lean formalisation was independently verified here.

The original Edition 2 PDF and source ZIP were left unchanged. No publication, repository write, or persistent Library mutation was performed by preparing Edition 3.
