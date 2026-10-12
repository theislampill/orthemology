# Information, Composition, and Self-Revision
## Local Descriptions and Operative Access

This is the fifth delivery of one research manuscript. Delivery identifiers occur in filenames and this evidence package, not in the paper's title, headers or body.

## Files

`information-composition-and-self-revision-v5.pdf` is the research paper, with all eight numbered results and complete proofs. The corresponding `.tex` is its editable source. `assessment/review-and-preservation.pdf` and `.md` contain the separate review adjudication, scope and preservation argument. No substantive theorem is displaced into that assessment.

`comparison-baseline/` preserves the exact fourth-delivery LaTeX source and historical comparison records. `assessment/edit-contract.json` and `source-diff.patch` identify the five permitted prose replacements and the one additional bibliography entry. `assessment/semantic-preservation.{json,csv}` retains the 115 inherited obligations with current locators; `inherited-workflow-obligations.json` retains the twelve obligations added in the fourth delivery. Counts identify declared inventories, not a proof of exhaustive semantics.

`verification/` contains six byte-unchanged inherited mathematical checkers, the additional finite boundary-sensitivity checker, and the current document checker. The delivered outputs are in `verification/results/`. The new checks cover receipt changes at fixed identity/interrupt state, incoherent combinations of atomic field reads, effect-scoped acceptance, and deliberate violation of label meaning. They are abstract finite cases, not tests of a concurrent implementation or a general noninterference proof.

`assessment/source-checks-current.json` identifies the fresh reading scope for Dijkstra and Herlihy–Wing. Earlier source records are separately labelled historical. Third-party article PDFs and font files are not redistributed.

## Rebuild and verify

Requirements: Python 3 with the packages in `requirements.txt`, TeX Live with `pdflatex` and the LaTeX packages declared in the source, and Pandoc for the assessment. From the package root:

```sh
bash build.sh
bash verify.sh
```

Both commands write only to `build/`; delivered PDF and evidence files remain unchanged. The verification suites test general finite cases within their declared scope. The document checker compares the source with the exact edit contract, all eight complete statement/proof blocks, all displayed mathematical blocks, inherited bibliography and labels, current obligation locations, and PDF metadata/layout. It includes negative controls. The edition number of a cited source is not a version label of this manuscript; the initial false-positive check and its corrected scope are recorded in `verification/results/instrument-notes.json`.

To verify supplied payload bytes on a system with `sha256sum`:

```sh
sha256sum -c MANIFEST.sha256
```

`MANIFEST.json` and `MANIFEST.sha256` describe payload files while excluding themselves. The outer ZIP identity is in the separately delivered `information-composition-and-self-revision-v5-delivery.json`; no circular archive self-hash is attempted. Rebuild metadata may differ across environments. The original delivery's clean extraction was compared by rendered pixels and extracted text as well as package hashes.

## Limits

Exact bytes establish identity, not truth. Preservation of unchanged results does not certify their historical originality. The results remain conditional on their mathematical premises. No peer review, proof-assistant certification, deployed-system verification, timing or speedup experiment, venue acceptance, or universal improvement claim is represented by these files. The finalised *The Cost of a Decisive Revision* is unchanged and is not revised or repackaged here.
