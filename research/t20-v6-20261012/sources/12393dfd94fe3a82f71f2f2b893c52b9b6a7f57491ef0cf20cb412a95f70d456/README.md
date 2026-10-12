# Ninth controller: independent scientific review

This source-only package presents three bounded, independently checked mathematical milestones:

- Finite shared-state primitives with exact accepted-step refinement
- Reconstruction of accepted finite histories from explicit finite samples
- An executable ordered 21-path controller for the stated initial epoch-zero fixture

Read PUBLIC_ACCEPTANCE.md for claims and limits. This is not completion of the broader research programme, a deployment, an arbitrary-state serializer, or an active nonzero synchronization service.

The package contains exact custom Lean source closures, independently used review controls, source-neutral evidence, provenance hashes, pinned external dependency inventories, and a portable replay driver. It contains no build objects or dependency cache binaries.

## Replay

Supply the official Lean 4.19.0 distribution and Mathlib source/cache snapshot identified in dependencies/. All outputs must be written to a new directory outside this package and both dependency roots.

python replay.py --lean-root /path/to/lean-4.19.0-linux --mathlib-root /path/to/mathlib-c44e0c8 --output /path/to/new-review-output

The driver verifies package contents and external dependency pins without changing them, uses a sanitized compiler environment, freshly builds all 49 custom source modules, checks 166 scientific theorem readbacks, and executes 17 independent control stages. One stage must fail specifically because the predecessor choice-ordered labelList has no executable code. That expected compiler failure is not a semantic refutation.

Every compiler stage has a maximum 180-second timeout and runs sequentially. The official precompiled Lean/Mathlib objects are trusted external inputs; this replay does not verify compiler correctness or rebuild those libraries. Exactly five separately documented cache-fetcher trace-metadata hash variants are allowed; no scientific object is excepted.

The scientific proofs use standard Lean axioms where reported. Compiled-interpreter assertions are recorded separately from kernel proof statements. No standalone linked C executable is established here.
