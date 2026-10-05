# Typed-context nucleus

A bounded parallel finite calculus combining syntax-generated typed telescopes with arbitrary PER-valued domains. Its universal relational soundness theorem is derived from finite formation and typing evidence.

The result retains the accepted source polynomials and raw conversion exactly. It adds typed proof-irrelevant identity, dependent Pi, represented Sigma, finite impredicative leaves, and exact two-coordinate contextual J. It does not add dependent All, recover every old typing derivation, or complete full U11.

## Package map

- `CHECKED_SCOPE.md`: final mathematical statement, construction, controls, and precise limits
- `SOURCE_CUSTODY.json`: exact accepted-source and toolchain identities, preservation limits
- `INPUT_IDENTITIES.json`: inherited source hashes
- `sources/TypedSyntax.lean`: finite syntax-only inference rules
- `sources/TypedPredicates.lean`: raw F/G/D/E/H and reindexing equations
- `sources/TypedLaws.lean`, `TypedPiLaws.lean`, `TypedSigmaLaws.lean`: smaller-premise law lemmas
- `sources/TypedSoundness.lean`: universal simultaneous formation/typing soundness
- `sources/TypedAlgebra.lean`, `TypedStructural.lean`: literal finite typed substitution
- `sources/TypedRepresentation.lean`, `TypedContextualJ.lean`: exact intrinsic representation
- `sources/TypedPositiveControls.lean`, `TypedNegativeControls.lean`, `TypedBoundaryResults.lean`: required controls and public law packaging
- `sources/TypedLegacy.lean`: exact restricted old-rule-tree comparison
- `sources/TypedReadback.lean`: definition, theorem-type, and axiom readbacks
- `logs/`: retained commands, compiler outputs, and exit statuses

`FINAL_DISPOSITION.json` and the final manifest determine qualification status. `CANDIDATE_v1.json`, `VERIFICATION_v1.json`, and `RESULT_SCOPE.md` are immutable historical review-input records. A successful example or helper-module compile is not an acceptance record.

## Source-only public projection

This projection changes packaging helpers only. All proof sources, accepted review records, and historical compiler logs are unchanged. `PUBLIC_PROJECTION_MANIFEST.json` records the exact changes and the two omitted preparation-only reconstruction/snapshot helpers. The retained `MANIFEST.json` describes the original accepted packet; the projection manifest is authoritative for this projection's membership and helper changes.

Reproduction requires an explicitly supplied, readable `TOOLCHAIN_ENV` file setting `LEAN_ROOT` and the existing pinned Mathlib `LEAN_PATH`. The helper verifies the Lean 4.19.0 binary digest and invokes that exact binary, independently of PATH. No toolchain is downloaded or installed. Missing or unreadable environment files are rejected before compilation.

With the existing pinned environment supplied, run `TOOLCHAIN_ENV=/path/to/environment.sh bash scripts/check-all.sh`. This compiles the source modules serially with `-j1`, default proof limits, and 180 seconds per module. New output goes to `reproduction/logs/`; the archived `logs/` and `review/logs/` remain historical evidence. After the main build, the optional review wrapper can compile controls such as `IndependentNucleusContracts`; it searches the review sources and then the freshly built main payload sources, and writes separately to `review/reproduction/logs/`.

The portability replay is packaging verification, not a new mathematical result or new scientific completion credit. Historical binary-resolution evidence and all replay checks are recorded in `PUBLIC_PROJECTION_VERIFICATION.json`.
