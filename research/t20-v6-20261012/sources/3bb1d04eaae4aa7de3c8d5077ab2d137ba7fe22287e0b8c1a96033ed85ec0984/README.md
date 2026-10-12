# The Last Moat — Edition 2
## Physical Realisability, Cross-Substrate Communication, and Holarchic Agency

10 September 2026 · Edition 2 (v2.0)

An arXiv-style, AI-assisted conceptual research manuscript. Not submitted to
arXiv, not peer-reviewed, and not a report of a physical experiment.

The paper develops an evidence-aware account of cross-substrate comparison,
physical communication contracts, and operator-governed host-relative
continuity. It distinguishes a physical carrier from storage, execution and
maintenance, and distinguishes source-grounded assessment from an implemented
general discovery faculty.

## Read and build

The main file is `the_last_moat_e2.tex`. Its section files and numbered
bibliography are included. A one-file alternative is `manuscript_flattened.tex`.
Compile **one** of these, not both in the same document.

A conventional TeX Live or MiKTeX installation with the packages in the preamble
is sufficient. No network access, custom fonts, external graphics, or BibTeX
run is needed during the build.

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error the_last_moat_e2.tex
```

Or run `pdflatex` on that file three times to resolve the contents, references,
and citations. The result is `the_last_moat_e2.pdf`.

## Reproduce the finite checks

Python 3.9 or newer; standard library only:

```sh
python3 verify_models.py --output verification_results.json
python3 -O verify_models.py --output verification_results_optimized.json
```

The script exits with code zero only when all **27** top-level checks pass:
13 retained edition-1 checks and 14 edition-2 additions. The checks use explicit
exceptions, so Python optimisation does not disable them. The script imports
`verify_models_v1.py`, included alongside it.

The reports contain per-check values, test-source hashes, the Python version,
and success/failure status. These are finite/dimensionless consistency checks,
**not** machine-checked proofs of the paper's 21 general results, independent
physical validation, or evidence that any proposed physical architecture exists.
No devices, networks or isolation boundaries are accessed.

## Guide to the edition

Sections 1–5 establish the question, source status, experimental prior art,
physical roles and kernel contracts. Section 6 gives the NS bridge, including a
residual-to-state estimate and a bounded-observation consequence. Section 7
contains the robust signalling results, including calibration uncertainty.
Sections 8–10 address Orthemology, evidence consolidation, representation,
Neuralese, and joint-witness composition. Sections 11–15 retain and strengthen
information cuts, migration, support independence, orchestration, computability,
viability and progress. Section 16 separates agency and authorship claims from
physical communication. Sections 17–18 state comparative research hypotheses
and conclusions. Appendices provide notation, examples, revision history, proof
scope and a claim audit.

## Accompanying records

- `CHANGES.md`: substantive revision map and corrected inferences.
- `REVIEW_SCOPE.md`: what was checked and what remains unverified.
- `source_register.json`: primary-source URLs and the scope of consultation.
- `proof_register.json`: named results, current numbering, page and test scope.
- `verification_results.json`: executed normal-mode checks.
- `verification_results_optimized.json`: executed optimised-mode checks.
- `build_audit.json`: build, layout and artifact checks.
- `MANIFEST.sha256`: checksums for the packaged files (excluding itself).

The current Orthemology definitions are pinned to repository commit
`f50dc1aee52356cc6adbef342387576b02afc124`; older saved candidates were not treated
as canonical. The terminology remains a proposed research vocabulary.

The source package contains no operational covert-channel discovery engine,
no physical experiment, and no model self-preservation or escape mechanism.
Its statements of feasibility remain conditional on actual interfaces,
resources, evidence, authority, and specified behavioural obligations.
