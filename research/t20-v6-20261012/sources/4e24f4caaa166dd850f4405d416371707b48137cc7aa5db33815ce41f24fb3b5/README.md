# Resumed cooperation interpretation

Start with `RESULT.md`, then `PREMISE_MATRIX.json` and `SOURCE_BINDINGS.json`.

This packet adds a fresh fixed-target semantic attempt, exhaustive bounded searches and 23 checked Lean declarations. It establishes family-scoped obstructions and a limited outcome/provenance separation. It does not establish a full philosophical countermodel, universal cooperation-impossibility or a newly proved metaphysical premise.

## Contents

- `DESIGN.md`: prospectively stated signature and discriminators.
- `RESULT.md`: analytic result, T17/B5 reconciliation and residuals.
- `PREMISE_MATRIX.json`: exact retained/disputed premise preservation and missing clauses.
- `SOURCE_BINDINGS.json`: directly read retained input identities and precise locators.
- `src/search.py`: explicit additive, all-Boolean-map, saturation, intrinsic-graph and ownership checks.
- `src/test_search.py`: 15 discriminating positive and negative tests.
- `src/FixedTarget.lean`: 23 mathematical declarations, including general family-level proofs.
- `src/Readback.lean`: generated declaration/axiom readback.
- `results/SEARCH_RESULT.json`: complete checked finite results and concrete fixtures.
- `VERIFICATION.json`: exact commands, actual timestamps, exit codes and logs.
- `DECLARATIONS.json`, `RESULT_REGISTRY.json`: theorem/result scope and source mappings.
- `WORK_RECORD.json`: actual observed work boundaries and research/verification distinction.
- `AUTHOR_MANIFEST.json`, `SHA256SUMS`: author-packet byte freeze; independent review is separate.

## Reproduce

From the workspace, run:

    python tranche20/research-resumption/cooperation/build_packet.py

The script uses the already installed Lean 4.19.0 named in `VERIFICATION.json`, Python's standard library, and no new downloads. It regenerates timestamps, output and readback receipts, so it changes the frozen packet's verification bytes. For independent review of the frozen author packet, copy the new packet first or invoke proofs/tests with outputs stored in the review directory. No previous source package, archive or repository is rebuilt.

The initial Lean development attempt failed because an ownership Decidable instance did not unfold its definition. That log is retained. The corrected final source passed compilation and independent module readback; no failure was hidden.
