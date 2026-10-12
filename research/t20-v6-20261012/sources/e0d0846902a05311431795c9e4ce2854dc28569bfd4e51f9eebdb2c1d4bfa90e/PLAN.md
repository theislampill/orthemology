# Guarded Saturation Implementation Plan

Goal: verify an actual numeric table update and the previously written height-inductive semantics.
Architecture: finite ordered support tuples drawn from the fixed grammar's finite support union; candidates read only the preceding table; choose each exact key's least candidate price. Prove separate soundness and minimum completeness invariants, then global stability from the frozen height bound.
Tech stack: installed Lean 4.19.0 and mathlib; no installation.
Spec: SPEC.md.

Constraints: scratch-only scoped package, frozen predecessors, no commits/integration. The assignment explicitly calls for direct implementation and final independent semantic review, so no extra planning approval or repository mutation.

- [x] Candidates.lean: finite tuple candidates, old-value retention, finite minimum selector, candidate characterization. Verify Lean with warnings as errors.
- [x] Saturation.lean: zero table and successive updates; height induction; global minima, stable bound, full-price-table early stopping. Verify Lean with axiom reports.
- [x] Controls.lean: nullary guard, unsupported and zero cycles, unchanged keys with improving prices. Verify positive theorems and rejected false controls.
- [x] Fresh full replay, predecessor hashes, independent semantic review, bounded RESULT.md and machine-readable receipts.

Review focus: no circular min-semantics definition; ordered premise supports preserved; arbitrary guards and noncomputability disclosed; zero-cost cycle handling; key stability not confused with price stability.
