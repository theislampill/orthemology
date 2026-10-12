# Constructive exact solver extension

Stage 1 is immutable in `sealed-v1`. Stage 2 adds `MealySolver.lean` and `MealySolverFixtures.lean` without changing the sealed proof sources.

## New constructive content

- `reachSet` performs executable backward expansion from the finite computed D set. `reachSet_stable` derives stabilization after at most m expansions using finite-set cardinality and deterministic recurrence. This does not assume an oracle or an unproved simple-path bound.
- `reaches_iff_mem_reachSet` connects that finite computation to the literal existential finite-word reachability predicate.
- `reachesBit` is consequently a terminating decision procedure for arbitrary finite-word reachability of D.
- `hittingMatrix` explicitly supplies the rational coefficients. Rows in D or outside reverse reachability are identity rows; every remaining row is `2 h(q)-h(next(q,false))-h(next(q,true))`.
- `hittingMatrix_mulVec` proves those explicit coefficients implement the Stage-1 semantic system. `hittingMatrix_det_ne_zero` derives a nonzero determinant from the checked maximum principle.
- `solveHitting` is executable Cramer's rule: one replaced-column determinant divided by the system determinant. The definition contains no classical choice, noncomputable matrix inverse, or unbounded search.
- `solveHitting_correct` identifies its rational result with actual fair infinite-input hitting probability; `solveDefect_correct` identifies `1-solveHitting` with the actual nonatomic output defect.

This supplies source correspondence for the new Lean solver only. It does not retroactively validate the predecessor Python Gaussian-elimination source. The determinant algorithm is terminating and exact; no polynomial runtime or practical scalability claim is made.

The four-state gambler fixture proves an actual non-dyadic atomic mass 2/3 and defect 1/3. Additional executable checks return 1, 0, 1/2, 2/3, and 1/3 for the relevant examples. They supplement the kernel theorem rather than replacing it.

## Supplementary independent-implementation regression

`SolverProbe.lean` enumerates all 4 labeled one-state and all 256 labeled two-state binary Mealy tables under an explicit base-(2m) encoding, and runs the proved Lean solver. `compare_small.py` independently decodes those tables and compares all 260 results with the predecessor exact-fraction Python solver. Every result matches; `solver-small-comparison.json` records that fact. This is finite regression evidence, not a proof of the Python program.
