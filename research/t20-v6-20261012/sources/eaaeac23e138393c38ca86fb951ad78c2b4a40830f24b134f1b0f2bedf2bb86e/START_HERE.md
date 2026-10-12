# Criterion transport reviewed intermediate V2

This is a reviewed intermediate research packet for question 4 of the Seventh Orthemology v5 tranche. It preserves a source-bound retained-standard checker experiment, exact transport proofs, and a conditional recipient/version-aware draft-repair model. It does not yet contain an executable transition that installs the replacement governing criterion itself. That separately scoped extension is in progress and is not covered by this packet.

## Results

- The pinned Candidate E owner is unchanged: 3,013 bytes, SHA256 e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359. The exact historical packet is recovered and assessed without treating it as an admitted theorem.
- The C0-to-C1 checker experiment is retained-standard repair. Its source-fidelity standard remains in the full basis; the stronger radical full-basis correction existence claim remains unresolved.
- Proof transport is sound under backward evidence-class coverage and judgment preservation. Coverage is necessary only for the stated uniform all-predicate result, not for every fixed judgment.
- The typed guarded draft transition preserves source and history and binds the modeled actor, target, version, epoch, operation and validity interval. Grants and authentic source/currentness inputs remain independent premises.
- No N2, T0, Wisdom, source unity or R5 defeat is established.

## Verification

Independent review re-fetched the canonical owner and all five substantive historical packet files, verified their hashes, compiled the Lean proofs, passed all 25 Python tests, reproduced the 393,216-case bounded audit, and independently replayed every shared CSV fixture. The Python and Lean outputs agree on all 393,216 six-field projections; both output hashes are 41a4caed22aa892bbc1da5a706172b261fdab618c1980530154cc38519b5edaf. All nine reported central Lean theorem axiom lists are empty.

The finite fixture comparison is not universal Python-to-Lean refinement, actual caller authentication, a hardened external parser, compiler correctness, or a physical non-bypass theorem. The initial deliberately incorrect baseline is marked RED and is evidence of test sensitivity, not the delivered implementation.

## Read in this order

1. TRANSPORT_ARGUMENT.md
2. CANDIDATE_E_COLD_ASSESSMENT.md
3. SUPPORT_AND_DEPENDENCY_LEDGER.md
4. PRIMARY_SOURCE_REVIEW.md
5. Proof/code files and evidence JSON records

The reported earlier extra-newline recovery event is author-observed history. The independent review verified the source bytes and both relevant digests; it did not independently witness that earlier write.

## Reproduce

Use Python 3.12 and Lean 4.19.0 (commit 6caaee842e94; no mathlib required). From this folder:

- python verify_bundle.py
- python -m unittest discover -s tests -v
- python bounded_audit.py
- lean CriterionTransport.lean
- lean -o TypedCriterionGuard.olean TypedCriterionGuard.lean
- python shared_fixture_check.py generate
- LEAN_PATH=. lean --run ReplayCriterionFixtures.lean
- python shared_fixture_check.py compare --label green

The generated CSVs are deliberately omitted because they are rebuildable from the included generator and verified source bytes. Their exact hashes are retained in evidence/SHARED_FIXTURE_MANIFEST.json. Full replay of actual source bytes takes several minutes.

## Admission boundary

Canonical Candidate E remains DEFERRED_INSUFFICIENT_AUDIT. This packet makes no canonical adoption, GitHub mutation, whole-tranche closure, or stronger criterion-installation claim.
