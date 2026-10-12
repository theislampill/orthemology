# Seventh covering/search kernel closure

Additive verification-only formalization of the accepted general opaque-repair covering optimum. Start with SPEC.md and THEOREM_MAP.md. The accepted originals and reviews are copied byte-for-byte under inputs; SOURCE_BINDING.json binds them and the copied root-attribution kernel dependencies.

## Replay

Requirements: official Lean 4.19.0 and Mathlib commit c44e0c8ee63ca166450922a373c7409c5d26b00b, with its compiled dependencies. No lake update or dependency edits are performed.

Run:

    ./verify.sh /absolute/path/to/fresh-output

Defaults use the installed official toolchain and exact Mathlib cache at private-locator:351b8592ab6e0e21df70. LEAN_419 and MATHLIB_C44 may select compatible local installations. The verifier compiles copied dependencies and every new module from source into the selected fresh output directory; it never imports a prebuilt local proof artifact from this packet. It then compiles statement/negative controls, runs bounded Python controls normally and under optimization, rejects six mutated proofs, and rechecks input hashes.

Successful theorem axiom reports contain only standard Lean logical axioms propext, Classical.choice, and Quot.sound. No custom axiom, unproved hole, native_decide, or unsafe definition is used.

## Main files

- CoveringPortfolio.lean: generic complement, cardinality, minimum and binomial cap
- LabelTransport.lean: independence from label names and numeric C(m,b,k)
- OpaqueActions.lean: primary full-action/full-history deterministic and randomized lower bounds
- FullCommandInterface.lean: fresh full-command upper construction and canonical observation law
- SourceCorrespondence.lean: actual-root availability and fixed-map failure witnesses
- RandomizedFinite.lean: finite AE intersection and finite-union probability tools
- OpaqueSearch.lean, RandomizedSearch.lean, CanonicalReplies.lean, ExactCap.lean: simpler adapters and cap iff theorem
- RepairStateBridge.lean: defective-start target-state bridge and already-correct zero-attempt control
- tests/: statement checks, kernel counterexamples, bounded independent semantic controls and mutation harness

Verification does not establish the world's physical/authentication/service premises. This is not a new theorem-novelty claim. See SPEC.md for exact retained limits.
