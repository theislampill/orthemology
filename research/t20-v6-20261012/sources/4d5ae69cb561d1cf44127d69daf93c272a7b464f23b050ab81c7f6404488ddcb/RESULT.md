# Guarded exact-support trees: bounded Lean verification

9 October 2026. Verification of an already written result, not fresh discovery credit. No integration, protected repository edits, adopted-calculus claim, T20 closure, or historical duration credit.

## Checked increment

Lean 4.19.0 checks structural replacement, pruning, and the bounded representative part of `source-sensitive-proof-compilation-20261009/RESULT.md` for **rational occurrence prices**. In particular:

> Every valid finite tree with judgement q and exact support S has another valid q-tree with exactly S, no greater cost, and every branch of length at most |J|(|S|+1). If E is finite, the uniform bound is |J|(|E|+1).

Branch length counts rule occurrences. The theorem does not assume normalized inputs, an existing bounded catalogue, validity of the replaced whole tree, or guard monotonicity. It derives these representative properties from the actual rule-tree syntax and its recursive validity condition.

**Not checked here:** finiteness of all trees below the bound for a finite ground-rule grammar; global minimum-price attainment; the synchronous minimum-table recurrence; witness correspondence with the Python implementation; fixed-point detection; worst-case lower-bound/sharpness construction; arbitrary nonnegative real prices; DAG costs. Thus this is not kernel certification of the whole compilation theorem or executable compiler.

## Mathematical interface

`Grammar J E R` fixes, for every rule label r:

- A finite arity and its ordered premise judgements, indexed by `Fin (arity r)`
- The head judgement and finite local evidence support
- One rational price for each rule occurrence
- An arbitrary fixed predicate on the ordered function of exact child supports

`Tree` is an inductive finite, well-founded rule tree. Support is local support union all child supports. Cost is rule price plus all child costs; repeated occurrences are charged separately. Validity requires every child to be valid, every child judgement to match its assigned premise position, and the rule's guard to hold on the actual ordered child supports.

There is no guard decidability hypothesis in these existence proofs. Effective execution requires decidability and an effective finite rule presentation, neither supplied by classical existence alone. Rational arithmetic is exact. The nonnegative-price hypothesis is explicit in the normalization and pruning theorems.

The exact-root-support bound requires finite J and each tree's finite support; E itself may be infinite. The uniform corollary additionally requires finite E. The checked bound does **not** require finite R. Finiteness of R would be needed for the next finite-family argument establishing minimum-price attainment; this next step has not been formalized here. Nothing in the present formalization assumes a minimum price already exists.

## Proof structure and precise theorem names

`GuardedTree.lean`:

1. `node_replacement`: equal support at every ordered premise position gives the same guard input and resulting support; matching judgements preserve premise typing.
2. `context_replacement`: structural induction through an arbitrary one-hole context derives validity, root judgement equality, and exact support equality after replacement. It assumes the original complete tree and the new subtree are valid. It does not assume the desired new complete-tree validity.
3. `context_cost_mono`: a subtree cost improvement propagates through every context. This additive comparison itself does not need nonnegative prices.
4. `valid_hole`, `hole_cost_le`, `proper_hole_nodes_lt`, `prune_equal_state`: a proper descendant's validity is inherited from its valid containing tree; retaining that descendant cannot increase cost under nonnegative occurrence prices, and strictly reduces occurrence count even when prices are zero.
5. `exists_reduced_representative`: choose a least occurrence count among valid same-state proofs no dearer than the input. Any repeated-state ancestor/descendant anywhere in such a tree would yield a strictly smaller candidate through proved context replacement. Therefore no branch repeats an exact state. This is classical existence, not an extracted normalizer.

`Bound.lean`:

6. `branch_member_context`, `reduced_hole`: connect inductive root-to-descendant branches to the actual contexts used by pruning.
7. `hole_support_subset`, `branch_support_subset`: prove support nesting from union accounting.
8. `reduced_branch_rank_nodup`: equal finite-support cardinalities on a nested branch imply equal supports. Consequently the pair (judgement, support cardinality) cannot repeat on a reduced branch.
9. `reduced_branch_length_le_exact`: those pairs inject into J times the integer range 0 through |S|, giving |J|(|S|+1).
10. `exists_bounded_representative_exact` and `exists_bounded_representative_uniform`: combine the derived normal form with the exact and uniform bounds.

The file also retains the weaker direct exact-state bound |J|2^|E| as `exists_bounded_representative`; the main result is the stronger exact-support-cardinality bound above.

## Nonvacuity and failure controls

`Controls.lean` independently instantiates a finite grammar with an ordered licence requiring exactly {alpha} in premise position 0 and exactly {beta} in position 1. Both premise positions have the same judgement. A wrapper adds cost and structure without changing support.

Checked controls include:

- The guarded original tree is actually valid.
- Replacing its wrapped alpha subtree by a differently shaped cheaper alpha leaf uses `context_replacement` through a nonempty context and preserves validity and exact support.
- Replacing alpha by a valid same-judgement empty-support proof is rejected: support inclusion is insufficient.
- Reversing alpha and beta is rejected even though the union support is unchanged.
- Enlarging one premise support can disable the guard, so it is genuinely not upward-monotone.
- A negative-price wrapper gives a valid equal-state proper-descendant case in which pruning increases cost, checking why the price-sign hypothesis matters.

The alpha/beta roots are declared mathematical identities in an illustrative policy. Distinct labels do not certify independent sources, truthful testimony, correct ancestry, or a substantive two-root epistemic licence.

## Interpretation boundary

All source metadata used by a guard must be fixed as part of the supplied grammar; all non-support judgement scope must be retained in J or fixed rule data. Correctness of that encoding, metadata authenticity, source admission, substantive rule/guard soundness, and faithful applicability to any philosophical or theological argument remain explicit interpretation obligations outside the kernel result. Guards that depend on hidden shape, changing authority, occurrence multiplicity, external inventory, or newly minted identities violate this representation unless the state is enlarged and separately justified.

This work does not show unrestricted provenance-changing cut is admissible, certify FABLE Core B, establish source truth, or add a metaphysical entailment. It checks a structural mathematical component of a declared fragment.

## Replay and trust

Run from any directory:

    private-locator:dbb66048571a41d896b5

The replay uses the existing Lean 4.19.0 toolchain and mathlib checkout at commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. No packages were downloaded or installed. One already installed mathlib source module lacked a cached `.olean`; `LocalFintypeProd.lean` is an exact unchanged local copy of `Mathlib/Data/Fintype/Prod.lean`, compiled only in this task directory. Its SHA-256 is `272b57521233c0e371c9d6cccfe6612b9b148d6a461b96d1228f104fac46fe2d`.

Production files are compiled with warnings treated as errors. The major theorem axiom reports contain only Lean/mathlib's standard `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`, custom axioms, or `native_decide` are used. This is a kernel-checked mathematical proof relative to Lean's kernel, imported library, and the stated standard axioms, not an axiom-free foundational claim.

The exact replay outcome, source hashes, input-preservation checks, and internal AI review are recorded in the sibling receipt files. Development logs may include failed intermediate attempts; only fresh final replay receipts establish the delivered claims. No elapsed wall-clock interval is represented as accumulated active work.
