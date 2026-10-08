# Veracity Boundary Implementation Plan

This historical plan was written before implementation. Its later independent review is recorded separately.

**Goal:** Check the dependency/equivalence audit without claiming new warrant for T0.

**Architecture:** A generic Init-only model keeps assertion, content truth, knowledge, exact-content awareness, controlled presentation, fittingness, and declarative shortcoming separate. One core module proves the controlled-token implication and explicit extensions; a second module provides finite relative interpretations and controls. A replay script checks cold compilation, declaration/axiom readbacks, expected rejected strengthenings, source bindings and hashes.

**Tech Stack:** Existing official Lean 4.19.0 executable; Init only; ordinary kernel `decide`; Python standard library for orchestration only.

**Spec:** PROPOSED_DESIGN.md and PROPOSED_CONTROLS.md, corrected pursuant to review approval on 2026-10-07; proposal-v1/ preserves originals.

## Global Constraints

- Work only inside this isolated veracity-boundary directory; no repository or remote changes, installs, canonical adoption, or registry verdict changes.
- No custom axioms, `sorry`, `admit`, `native_decide`, `Lean.ofReduceBool`, or external proof import. Standard classical reasoning may occur and must be reported.
- K is the limited epistemic fragment used by the implication, not a complete theory of perfect knowledge.
- Weak A/C stress controls do not preserve the full T17 profile. Strong informed ownership makes A/C semantic projections.
- D is a respect-specific shortcoming; N is the source-specific all-context incompatibility with fitting exercise. Never collapse them by definition.
- All report/guide citations come from sealed SOURCE_PASSAGES.json; preserve positive appraisal and critic.
- Stop after sealing for independent review. Do not claim universal prerequisite status for this sufficient route.

## Review Focus

- False known assertion with fitting exercise: fails N while preserving D/P.
- Controlled truth implication accidentally promoted to every weak assertion: blocked by explicit A/C coverage and local/global control.
- Poor K signature misrepresented as omniscience: prevented by strong ownership projections and scope statements.
- Renamed no-counterfeit principle advertised as independent warrant: exposed by equivalence under semantic coverage/factivity.
- Empty/vacuous conditional masquerading as nonvacuity: positive two-source fixture has a true owned source assertion and a false created-speaker assertion, with causal provision separated from ownership.

## Task 1: Core logical interface

Files: src/VeracityBoundary.lean; tests/APIContract.lean; development/ red/green logs.

- [x] Write API acceptance checks for Model, K/A/C/D/N/P, controlled_token_true, veracity_of_coverage, counterfeit_iff_false_under_coverage, veracity_iff_no_counterfeit, false_excludes_package, strong_awareness, strong_control, strong_veracity.
- [x] Run the contract before the module exists and retain the expected missing-module failure.
- [x] Implement the minimal separate predicates and proofs. StrongAssert is a strengthened interpretation, never a theorem identifying it with all genuine assertions.
- [x] Compile and rerun the contract; inspect exact theorem signatures and used axioms.

## Task 2: Relative controls and nonvacuity

Files: src/VeracityControls.lean; tests/Acceptance.lean; tests/rejected/*.lean.

- [x] Write tests for six scoped deletions K/A/C/D/N/P, a positive inhabited source/created-speaker model, truthful-but-nonconforming control, local/global separation, and strong-ownership noncollapse.
- [x] Run before control definitions exist; retain the expected unknown-declaration failure.
- [x] Implement finite truth-table interpretations with ordinary kernel decide. Each deletion explicitly proves all five retained premises, exercise bridge/factivity, failure of its named premise, and failure of T0.
- [x] Implement expected-rejection files trying to assert T0 for each deletion model and trying to infer generic conformance from the truthful nonconverse model. Verify failures are false-proposition rejections, not import/elaboration errors.
- [x] Run the complete isolated suite and check the positive fixture contains an actual source assertion, distinct false speaker, extra fitting exercise, and causal provision without source assertion ownership.

## Task 3: Source bindings, replay, seal

Files: SOURCE_PREMISE_MAP.json; SOURCE_BINDINGS.json; README.md; CHANGE_RECORD.md; reproduce.py; validation/; SHA256SUMS; REVIEW_HANDOFF.md.

- [x] Copy exact selected source passages, with source file hashes and passage-text hashes; compare to sealed input. Bind K/A/C as semantic audit interfaces, D/N/P to their distinct T17 paragraphs, and exclusions/reuse to T19/Seventh/grounded-attestation.
- [x] Create a replay that pins the existing compiler SHA-256, uses a fresh output directory, compiles both modules, checks all acceptance/expected-rejection files, prints declaration types/proof bodies/axioms, and records import closure and file hashes.
- [x] Run a fresh final replay; inspect every result and all axiom readbacks. Keep developmental failures distinct from final passing evidence.
- [ ] Seal the candidate with its scope, verification, limits and review location. Independent review was pending at the time of this plan.

## Process adaptation

This preimplementation plan governed an isolated local research package outside the repository. No git commit or repository mutation was part of its scope. The ledger and developmental evidence remain preserved for review.
