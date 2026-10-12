# Fair-input finite Mealy qualification, Stage 3

This immutable snapshot extends the previously sealed exact measure bridge and constructive rational solver. It additionally establishes exact target singleton probabilities, effective atomic support enumeration, actual point-atomic measure reconstruction, and a terminating finite-approximation modulus.

Read `ATOMIC_STAGE3.md` for exact new guarantees and limitations and `ATOMIC_AUDIT_MAP.md` for the semantic readback. Historical Stage-1/2 summaries are preserved separately; their earlier open boundaries are superseded only where the later qualified declarations explicitly close them.

## Main results now qualified

- Atomic output mass is the actual fair infinite-product probability of eventually reaching D
- Exact finite-word/cardinality interpretation and the sharp finite-horizon `(1-2^(-(2m-1)))^j` bound
- Rational total atomic mass/nonatomic defect, with a terminating executable exact Lean solver proved correct
- Exact rational singleton mass for each finite-state-generated target
- Each positive atom is ultimately periodic and has an explicit finite generator and rational mass
- An Option-valued enumeration with skips that is sound, complete and duplicate-free, with exact singleton weights
- Equality of the actual point-atomic restriction with the countable sum of those weighted Dirac measures
- Exact finite partial measure sums and exact rational residual mass
- A terminating computable cutoff whose every later partial sum omits less than `2^(-k)` actual atomic measure

## What is not claimed

- A total nth-positive-atom selector, a support-finiteness decision, or a promise of another positive entry after finite support is exhausted
- A singleton-mass algorithm for an arbitrary infinite target without a finite-state presentation
- Polynomial time or practical scalability of the naive finite-refinement/determinant/enumeration algorithms
- Source correctness of the predecessor Python solver; its 260-case agreement is supplementary finite regression evidence
- A Lean proof realizing every rational in [0,1] as a defect; the present concrete non-dyadic fixture is defect1/3
- Any physical, empirical, observability, ethical-authority, or substrate-adequacy conclusion beyond the explicit finite mathematical model

## Reproduction and pins

`verify-atoms.sh` runs the complete earlier replay first, then fresh-compiles all Stage-3 proof sources, checks 8 supplementary target/approximation executions, and prints all main types and axiom dependencies. Across the three stages there are 81 audited principal declarations. The permitted axiom ceiling is propext, Classical.choice, Quot.sound; no proof holes or native-decision axiom are accepted.

Lean: 4.19.0, compiler commit6caaee842e94; mathlib: c44e0c8ee63ca166450922a373c7409c5d26b00b, with its unchanged package manifest. The included shell scripts use the original environment's absolute paths. A portable replay must remap paths and supply the pinned official dependencies; the proof source bytes need no changes.

Fresh predecessor source order: PERRefinement, MealyRefinement, BlockMismatch, P02A2/MeasureCore, Q8Measure. New proof order is documented in the staged reports and scripts. The canonical repository and all predecessor files were not modified.
