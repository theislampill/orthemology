# Decision 0007 — Profile-space definition (Π_A)

**Date:** 2026-07-20 · **Decider:** Claude Fable 5 under the owner's standing autonomy mandate (R2 closure) · **Status:** implemented.

**Question.** The corpus used the profile space `Π_A` (candidate families range over it; placements live in it) without a definition site — an issue flagged in the theory review and deliberately kept OUT of the D1 candidate package by the D1 scope audit (bundling it would have been silent scope expansion). Should the separately drafted optional definition be integrated, and in what form?

**Decision.** Integrate, as manuscript **Definition 10 (Profile space, partial profiles)** in §5.2, with the symbol-normalization corrections of Decision 0005. The definition supplies:

- **complete profiles** — assignments over the factorized axes: at most one *alternatives*-marked value per axis, any set of *co-holding* values, no violation of declared cross-axis **consistency constraints**; `Π_A` is the set of complete profiles;
- **partial profiles** — per-axis sets of still-admissible values; `Π_A^∂` ⊇ `Π_A`;
- the relations among the **true profile** `O*(m; A) ∈ Π_A`, the **candidate set** `Ĉ_{A,α,t}(m) ⊆ Π_A`, the **inferred partial profile** `p̂_{A,α,t}(m) ∈ Π_A^∂`, and optional **belief weights** — with the explicit non-conflation rule: a candidate set of several complete profiles is a different epistemic state from one vaguer partial profile.

Subsequent definitions renumber (+1): Metaortheme → 11, Residual disposition → 12, False closure → 13, Target profile set → 14. The core's inherited-notation block and `Π_A` gloss now cite Definition 10 and type `p̂ ∈ Π_A^∂`.

**Provenance.** Drafted during the M1 gate as an optional patch, explicitly deferred; the deferral record is preserved in the private reconciliation workspace. Integration here is the editorial adoption the deferral anticipated.

**Non-decision.** No change to ground truth (Decision 0001), to candidate-family typing, or to any verdict.
