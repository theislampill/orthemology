# Independent Mealy solver extension audit

## Disposition

The separate stage-2 seal passes an independent source and rebuild audit. It genuinely supplies executable rational probabilities for the actual finite Mealy output law. It does not retroactively turn the stage-1 existential proof into an extracted algorithm or certify a separate Python solver.

Exact archive: `private-locator:bec32805a9a6ec0d46f5`

SHA256: `be139a29c285da780a20609b2b60e3cf3551338793030560b61da9ff8656523d`

Every file in `sealed-v2` matched its archive bytes and SHA256SUMS. All stage-1 Lean source hashes matched the previously independently rebuilt stage-1 sources. Fresh stage-2 outputs are confined to `observer-measure-audit/solver-build`, with imports resolved against that directory, the independently rebuilt stage-1 audit outputs, and the exact pinned Mathlib/package caches. No source tree or canonical repository was modified.

## Reproduction

`audit_solver.py`, `solver-audit.log`, `solver-receipts/`, and `SOLVER_STAGE_AUDIT_RESULT.json` provide commands, source hashes, regenerated artifact hashes, exits, durations, and the eleven new type/axiom readbacks.

- `MealySolver.lean`: exit 0
- `MealySolverFixtures.lean`: exit 0
- `SolverVerification.lean`: exit 0
- Eleven requested axiom footprints remain within `propext`, `Classical.choice`, `Quot.sound`
- Executable results: constant-machine hit 1, copy-machine hit 0, split-machine hit 1/2, gambler hit 2/3, gambler defect 1/3

All commands used Lean 4.19.0 commit `6caaee842e94`, `-j1`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

## Actual new content

`reachSet` begins with the finite, already-correct D test and repeatedly adds states with a successor in the existing set. It retains existing members, so the sequence is monotone. `reachSet_stable` uses finite cardinality plus the deterministic recurrence to prove stabilization after at most m expansions; the proof does not assume a reachability oracle, or assume an unproved simple-path bound.

`reaching_word_mem` and `reaches_of_mem_reachSet` separately prove both semantic directions. The resulting `reachesBit` computes literal finite-word reachability of D.

`hittingMatrix` has identity rows on D and on states unable to reach D; every other row is exactly `2h(q) − h(next(q,false)) − h(next(q,true))`. `hittingMatrix_mulVec` connects the executable coefficients to the stage-1 semantic system, preserving the essential zero boundaries on closed non-D components.

The determinant is proved nonzero using the previously audited maximum-principle injectivity. `solveHitting` is explicitly the Cramer replaced-column determinant divided by this determinant. Its definition contains no classical choice, noncomputable inverse or unbounded search. The displayed `#print` confirms the actual executable definition and its finite/decidable input structure.

`solveHitting_matrix_equation` uses the exact Cramer identity and the proved nonzero denominator. The rational result is cast into the real semantic system, where uniqueness identifies it with the fair infinite-product hitting probability. `solveDefect_correct` then combines the already-audited atomic-mass/hitting equality with `1−solveHitting`.

## Non-dyadic fixture

The four-state gambler has a constant-output sink at state 0 and a permanently copying sink at state 3. States 1 and 2 form the two interior positions of a fair gambler's-ruin walk. The proof establishes D = {0}, backward reachability = {0,1,2}, and the exact rational solution vector `(1,2/3,1/3,0)`.

The actual output law at state 1 consequently has atomic mass 2/3 and defect 1/3. These are kernel theorems about the measured law, not merely finite enumeration or floating-point regression results.

## Boundaries

This qualifies the new Lean determinant solver, assuming its concrete finite state presentation and supplied transition/output functions. It does not prove correctness of the predecessor Python Gaussian-elimination code, extract a polynomial-time algorithm, establish practical scalability, supply every singleton's rational mass, or prove realizability of every rational defect. The author's separate 260-table Python agreement remains supplementary regression evidence and was not used to replace any formal or independent rebuild check here.
