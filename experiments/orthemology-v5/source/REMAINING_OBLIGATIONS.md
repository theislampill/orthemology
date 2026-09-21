# Exact remaining frontier

No item is closed by calling it future work. These blockers survive this reference-verified checkpoint. The mathematical work is not abandoned because of them.

## U01 — Real Lean/kernel acceptance

Blocker: No installed compiler; official asset/network and artifact-size routes failed with retained diagnostics.

Method: Obtain exact 4.19.0 or document a deliberate migration; run verify.py, repair all actual elaboration errors without weakening statements and inspect all required declarations.

Sources: [formal_targets.json](formal_targets.json), [TOOLCHAIN_LOCK.json](TOOLCHAIN_LOCK.json), [evidence/current/TOOLCHAIN_ACTUAL.txt](evidence/current/TOOLCHAIN_ACTUAL.txt), [evidence/current/TOOLCHAIN_CONNECTOR_DIAGNOSTICS.json](evidence/current/TOOLCHAIN_CONNECTOR_DIAGNOSTICS.json).

## U02 — Actual transitive assumption and statement fidelity audit

Blocker: The emitted in-Lean audit command is uncompiled; no actual footprint is known.

Method: Build all twelve modules, require every declared name/type, compile RequiredAudit with #ortho_audit, inspect the actual smaller footprint and review theorem statements against AC01–AC16.

Sources: [lean/AuditSupport.lean](lean/AuditSupport.lean), [build_gate.py](build_gate.py), [examples/RequiredAudit.preview.lean.txt](examples/RequiredAudit.preview.lean.txt).

## U03 — Whole deployed parser/checker/exporter refinement

Blocker: Python/JSON behaviour and eight examples are finitely checked, not universally verified.

Method: Extract the finite checker or prove raw decode/structural validation/substitution/check/serialize refinement, including budgets and rejection paths.

Sources: [reference.py](reference.py), [boundaries.py](boundaries.py), [proof_export.py](proof_export.py), [lean/FiniteBridge.lean](lean/FiniteBridge.lean), [lean/GeneratedExamples.lean](lean/GeneratedExamples.lean).

## U04 — Operational formal model to actual registry/lock implementation

Blocker: Typed Plan model abstracts resource refusal and does not contain the full mutable issuer registry or probability grammar.

Method: State a simulation over complete Gamma/issued-record/lock states and prove successful concrete transitions refine abstract checked transitions, including failure atomicity and concurrency linearisation.

Sources: [operational.py](operational.py), [lean/OperationalKernel.lean](lean/OperationalKernel.lean), [PROOFS_V4.md](PROOFS_V4.md).

## U05 — Actual measure-theoretic formalisation

Blocker: Q1–Q8 measure and computability arguments are ordinary proofs; preserved AlmostSureBoundary is only a logical abstraction.

Method: Pin Mathlib; define positive singleton support, countability, restrictions, pushforwards, all-event property, sums and weak limits; prove Q1–Q4/Q7 and formalise the Q8 reduction separately.

Sources: [PROOFS_V4.md](PROOFS_V4.md), [lean/AlmostSureBoundary.lean](lean/AlmostSureBoundary.lean).

## U06 — Unbounded typed sampler and productive observer semantics

Blocker: Bounded source APIs and ideal ordinary stream arguments are not a mechanised probability space.

Method: Give a guarded/coinductive stream semantics, prefix cylinder law and stopping-time measure; prove total mass, certified leaves, exact tails/expectations and finite-cap relation to Python.

Sources: [guarded_sampler.py](guarded_sampler.py), [productive_observer.py](productive_observer.py), [PROOFS_V4.md](PROOFS_V4.md).

## U07 — Computational cost and entropy-law assurance

Blocker: Counters exclude parsing, allocation, validation, entropy acquisition and real CPU costs; fair input law is a premise.

Method: Choose an explicit instruction/bit-cost model and entropy assumption; prove implementation costs or measure separately, never infer time from expected bits.

Sources: [guarded_sampler.py](guarded_sampler.py), [PROOFS_V4.md](PROOFS_V4.md).

## U08 — General fixed-point correspondence

Blocker: A concrete singleton correspondence is solved ordinarily; no general compactness/selection theorem has been formalised here.

Method: Use a pinned existing Kakutani development, define the actual safe domain and correspondence and discharge all hypotheses; separately prove effective realisation or exhibit its impossibility.

Sources: [PROOFS_V4.md](PROOFS_V4.md), [PRIOR_ART_COMPARISON.md](PRIOR_ART_COMPARISON.md).

## U09 — Finite-source normalisation and conversion-completeness bridges

Blocker: Preserved System F translation and compatible SKI confluence/completeness arguments remain unmechanised.

Method: Mechanise translation/substitution, nonempty reduction simulation and exact modulo-conversion counterexample; keep K t Omega semantic obstruction unchanged.

Sources: [lean/NormalisationAndNumerals.lean](lean/NormalisationAndNumerals.lean), [history/Orthemology_v3_Critical_Handoff/inputs/v3/MATHEMATICAL_PROOF.md](history/Orthemology_v3_Critical_Handoff/inputs/v3/MATHEMATICAL_PROOF.md).

## U10 — Full logical relations / semantic parametricity

Blocker: New R1 only treats finite pure derivations; its source is uncompiled.

Method: Compile it, then specify and prove stronger relation-environment/identity-extension/effect/dependent rules only with the needed hypotheses; compare Pistone Theorems 5.21/7.1.

Sources: [lean/RelationalFragment.lean](lean/RelationalFragment.lean), [PRIOR_ART_COMPARISON.md](PRIOR_ART_COMPARISON.md).

## U11 — Contextual dependent substitution, J and universe rules

Blocker: Existing Pi/Sigma/coherence semantics is not a full dependent calculus or decidable kernel.

Method: Specify contexts, substitutions, dependent eliminators and judgmental equalities, prove substitution/soundness and explain the exact universe closure excluded by SCUU.

Sources: [lean/EffectsAndDependence.lean](lean/EffectsAndDependence.lean), [PROOFS_V4.md](PROOFS_V4.md).

## U12 — Exact-length trace and backend/contextual correctness

Blocker: Finite symbolic traces are tested and exportable but the full length-indexed simulation and contextual compiler refinement are absent.

Method: Introduce an indexed trace relation, prove each replay step and strategy cost; define effect/observable contexts and verify backend lowering before any performance claim.

Sources: [extensions.py](extensions.py), [proof_export.py](proof_export.py), [lean/BoundaryResults.lean](lean/BoundaryResults.lean).

## U13 — Novelty, priority and foundational importance

Blocker: Only a bounded source-grounded comparison exists; no independent specialist review occurred.

Method: Compare exact hypotheses/conclusions with closest complete primary work, obtain independent review, and distinguish elementary application/engineering from new mathematics.

Sources: [PRIOR_ART_COMPARISON.md](PRIOR_ART_COMPARISON.md), [SOURCES.json](SOURCES.json).

## U14 — Real-world law binding and distributed authority

Blocker: The host declares law models and owns local mutable state; no external authenticated law oracle or distributed revocation is implemented.

Method: Specify independent evidence provenance and an external system model; verify authentication, freshness, discovery and multi-process consistency if that deployment is pursued.

Sources: [OPERATIONAL_CONTRACT.md](OPERATIONAL_CONTRACT.md), [operational.py](operational.py), [observations.py](observations.py).
