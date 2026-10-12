# General exact-reset continuation formalization plan

Goal: certify the two directions of the exact backward-dependency closure theorem and its coarsest deterministic-summary property over every finitely enumerable full Boolean product.

Specification: ../constructive-t20-20261009/revocation-dependency/THEOREM.md, Theorem 1, reviewed in ../constructive-t20-reset-review-20261009/REVIEW.md.

Architecture: use a coordinate type with an explicit finite exhaustive list; states are all functions from coordinates to Bool. Coupled actions are arbitrary total state maps. The action alphabet also contains both independent resets at each coordinate. Define essentiality by an actual one-coordinate witness, and closure independently by inductive base/dependency rules. Define continuation equivalence separately by all finite action words. Prove equality of the two relations, then construct zero-filled projection updates and prove that every deterministic output-decoding summary refines this projection.

Toolchain: official Lean 4.19.0, core/Std only. No additional package installation is planned. Scratch package only; no canonical repository modifications.

Tasks:
1. Establish toolchain and record exact version/source. Compile declaration-presence red target.
2. Prove finite-coordinate essentiality support lemma by sequential coordinate replacement.
3. Prove finite reset-context word realizes an arbitrary witness outside one coordinate.
4. Prove strengthened backward-closure necessity by induction over generated closure; prove sufficiency by finite-word induction.
5. Construct projection/zero-fill decoder and updates; prove coarseness for arbitrary deterministic summaries.
6. Compile all sources with warnings-as-errors; print theorem axiom dependencies; recompile from a clean build; run signature and rejection controls; record scope and excluded claims.

Review focus: zero coordinates, constant outputs, arbitrary differences outside the coordinate being exposed, dependency chains of arbitrary depth, and the role of both Boolean values/reset labels. The general proofs cover all five; no finite example is a substitute.

Out of scope for this first package: cardinality arithmetic, optimal/fixed-width encoding lower bounds, explicit distinguishing-word length bounds, positive-certificate specialization, project-specific source interpretations, and metaphysical or human-warrant claims. These will not be claimed merely because the core result is proved.
