# Bounded Lean verification target

Verify an actual finite ordered-rule tree representation whose guards inspect exact ordered child supports. Prove structural replacement through arbitrary one-hole contexts, preservation of validity and exact support from same-judgement/same-support replacement, and cost monotonicity. Prove that pruning a proper descendant with the same state strictly decreases occurrence count and cannot increase nonnegative occurrence cost. If feasible, derive repetition-free representatives; the sharp height bound and saturation will be separately reported if not checked.

No guard monotonicity, validity of a replacement context, source authentication, metadata correctness, substantive rule admission soundness, metaphysical truth, or closure status may be silently assumed. Finite-grammar interpretation and effective comparisons are distinct from these structural statements.

Controls: a genuinely nonmonotone two-premise ordered support guard; equal-support replacement by a differently shaped cheaper proof; reversal of premise order rejected; smaller support replacement rejected; negative local cost defeats pruning nonincrease. Lean must reject deliberately false mutations, with no sorry/custom axioms/native_decide in production.
