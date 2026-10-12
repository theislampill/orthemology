# P02 attempt-0002 candidate qualification, 2026-09-30

## Result

All 130 previously authored theorem candidates (119 attempt-0002, 11 preserved predecessor candidates) compile under exact Lean 4.19.0 / commit 6caaee842e94, Lake 5.0.0-6caaee8 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. Every original pinned dependency revision was checked with a clean tracked checkout. All 130 declaration types and transitive axiom dependencies were read back. Dependencies are confined to propext, Classical.choice and Quot.sound; no sorryAx or native evaluation axiom is admitted.

Every theorem statement header is unchanged up to whitespace. The retained original source hash inventory, exact repaired source hashes, fresh nonempty artifact hashes and source-header comparison are recorded. Twelve of the fifteen inventoried source modules required proof/elaboration repairs. Flow, ObserverCore and SimplexStationary were unchanged.

Primary sealed result: receipts/qualification-20260930T134433Z/QUALIFIED_RESULT.json
SHA-256: 1e963ab5c8558a2e633b1f0f83e08628cd23d09058ebfdd577a9f0e944e4b52c

This is qualification of an isolated shadow. It changes no repository, canonical theorem, owner-adoption decision, Integration DAG status or publication. It is not completion of every P02 obligation. In particular, absent fair-Cantor/code/hierarchy bridges were not magically supplied by compiling ObserverCore.

## Preserved input

The consumed attempt-0002 outer ZIP has SHA-256 f90e399269ccd33c1df42b13c085f09d4e85ea6e2ecfd6f6ee9501de6671d0e2, 4,347,878 bytes and 265 members (input verification provided by the coordinating task). The extracted input and nested predecessor are untouched. Original source hashes are in receipts/ORIGINAL_SOURCE_HASHES.json. The shadow's Lake configuration uses the exact inspected local dependency checkout instead of retrieving Git dependencies; that configuration adaptation has no mathematical scope effect.

## Repair inventory

- MeasureCore: use the pinned Set.diff_subset identifier
- Mixture: expose the NNReal-to-ENNReal scalar action in normalization
- Fibres: open Function notation, use the ENNReal positivity theorem, and supply explicit finite mass/diffuse-mass expressions to toReal_add
- Refinement: open Function and ENNReal notation scopes
- Observation: instantiate both coherence rewrites at the intended n and points; discharge an event-definition equality by reflexivity
- Stationary: qualify Finset.smul_sum and use the pinned IsMaxOn binder convention
- AllNParity: add whitespace that prevents the 1≤ms token from being parsed as a measure-order token
- FiniteLaw: explicitly distribute event conditionals through finite sums and evaluate the single contributing fibre
- ParityBridge: use Bool.and_eq_true_iff
- FiniteMeasureBridge: explicitly distribute event conditionals, push a rational cast through if, and expose the pointwise scalar action
- Predecessor MeasureCore: open ENNReal notation
- Predecessor T300ThreeBit: use decide +kernel so rational reduction is performed by the kernel; native_decide is not used

## Failed and excluded evidence

The initial unmodified candidate build failed in multiple modules; raw errors are retained. The repaired complete incremental build succeeded in receipts/all-build-02.log. A parallel fresh build was then interrupted after several minutes of little progress; it gives no pass credit. A subsequent serial fresh build succeeded for every module. The first aggregate readback failed only because the harness requested the unsupported pp.width option; despite printing declarations, that nonzero-exit run is excluded from successful audit credit. The corrected audit exited zero and supplies the sealed readbacks. These outcomes are not hidden or mislabeled as theorem failures.

The reproduction runner qualify.py uses serial module builds and two Lean runtime threads to avoid excessive parallel import pressure. Its failed receipts are retained. seal_qualification.py independently verifies the corrected audit, the fresh-build command exits/artifacts, exact source hashes, statement preservation and axiom ceiling before producing the sealed result.

## Scope now genuinely checked

The compiled candidates include actual countable positive singleton support; restrictions and pushforwards; countable-mixture mass; normalized weighted-fibre mass and defect; measurable finite/full-history observations; finite telescopes and the exact infinite residual decomposition; constructed compact-convex Cesàro fixed points and finite row correspondences; exact finite rational law-to-Measure transport; and all-length parity mask counts linked to enumerated events.

They do not prove the full ordinary hierarchy classification, byte-code simulation, arbitrary-measurable-observer computation, weak-limit examples, optional martingale extensions, or coordinate-level parity wrappers. Those source gaps stay distinct from the now-resolved execution problem.

## New Q8 research extension

Q8Measure.lean, Q8Machine.lean and Q8Compiler.lean are separate subsequent research files, not part of the original 130-candidate result or its seal. Their final verification and precise boundary must be read from the separate Q8 receipt. They retain the distinction between a actual switched-law theorem, a concrete bounded-counter-machine theorem, register-level LOOP compilation, a byte-code theorem and a computability-index reduction.
