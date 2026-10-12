# Exact rational cuts for the unchanged numeric observer

## Result

The existing rational threshold table was already proved in ordinary mathematics by P02 C2-09–C2-12 and V5 CV-C. This additive increment supplies its previously missing **kernel-checked upper-cut normal forms and computational matrices** for the existing `evaluateIndex` output law. It claims neither a new ordinary classification nor a new hardness reduction.

Write M(e) for the original `P02A2.mass (outputLaw (evaluateIndex e))`, d(e) for the original real-valued defect 1−M(e), and r_i for the existing total decoder `rationalOfCode i`. Define only these two wrapper predicates:

- L(q,e,i,k,n): q<r_i<1 and the unchanged `membershipMatrix e i k n`.
- U(q,e,i,k,n): r_i<q implies the unchanged `membershipMatrix e i k n`.

The proven exact forms are:

- M(e)>q iff exists i,k, forall n, L(q,e,i,k,n).
- M(e)>=q iff forall i, exists k, forall n, U(q,e,i,k,n), with q<=1.
- The other two mass cuts are the exact logical negations.
- For every nonnegative rational q<=1, d(e)<q uses the first form at 1−q, d(e)<=q uses the second, and the reverse inequalities use their exact negations.
- d(e)=q is exactly the conjunction of its non-strict cuts.

The strict form keeps a **single positive rational margin for all horizons**. A finite-horizon strict inequality at the target itself is not substituted for that margin. The semantic proofs explicitly instantiate the retained exact `atomic_mass_formula`, finite-cylinder rational law bridge, and actual numeric evaluator.

The `Computable` proofs first cover each fixed q. The `RationalThresholdUniform` module then proves the stronger **joint** result in the original threshold code j and all four matrix naturals. Its new primitive-recursive comparator handles both zero-denominator conventions exactly. An explicit primitive-recursive `complementCode` satisfies `rationalOfCode (complementCode j)=1−rationalOfCode j`, including j with denominator 0. Composing it proves joint computability for the actual defect-cut matrices as well. No variable-program `Primrec` claim is made: the original evaluator and membership matrix remain uniformly `Computable`.

## Boundary and equality controls

At q=1 the closed mass-cut wrapper is propositionally the old membership matrix. At q=0 its closed cut is true. The strict mass-cut wrapper at 1 is impossible. Zero-denominator witness codes and a witness equal to the strict target cannot satisfy the strict wrapper; redundant fractions have identical meaning.

The literal original L1 program `hiddenMixturePacked` has an all-input checked evaluator equation. It hides the first fair bit, outputs 0 at time 0, and thereafter copies each available bit precisely when that hidden bit is 1. Exact finite kernel controls give heavy counts 2, 3, 5, 9 at horizons 1, 2, 3, 4 and mass 9/16 at horizon 4.

The separately labelled ordinary all-horizon argument identifies the program's law as a prefixed half-point/half-fair mixture. Its atomic mass is 1/2, while every finite heavy mass at k=1 is strictly greater than 1/2. It therefore witnesses the equality-case obstruction in the actual unchanged program representation. These finite checks do not masquerade as a kernel proof of the infinite-law identity. The root's half-point/half-fair control is credited in HIDDEN_MIXTURE_DERIVATION.md.

## Evidence and replay

The full 77-module original membership-computability source closure was extracted byte-for-byte from the retained archive and rebuilt with Lean 4.19.0 `--trust=0`. Mathlib and package versions match the original archive lock, including mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. Missing official cache artifacts were installed solely into this new additive directory. Mathlib itself is an upstream cached dependency, not a fresh source rebuild.

Run `python rational-threshold-formal-extension-20261011/replay_frozen.py` from the workspace for a fresh candidate replay, all 38 theorem-axiom audits, four intentionally false statement controls, and before/after checks of the original source/archive and replay inputs. The final author replay also verifies all 8,117 pinned cached Mathlib/package/toolchain objects before and after execution; these are integrity checks, not a source rebuild of those dependencies. Read AUTHOR_REPLAY.json for the frozen author success record. The replay command writes only a new verified-* output directory and leaves that record and all previous bytes unchanged. Prior failed elaboration snapshots and logs are retained in candidate-* directories and the first baseline failure directory; they are diagnostics, not successful proof credit.

The four negative controls must fail because they assert: an equality witness is strictly above the target; a zero-denominator threshold has complement 0 rather than 1; the hidden-mixture residual count is 8 rather than 9; or the old vacuous rational-one branch can serve as a strict witness.

## Scope

Under the conventional arithmetical normal-form interpretation these computational forms provide the expected Sigma2/Pi2 and Pi3/Sigma3 **upper** bounds. A general hierarchy-library theorem, formalized compile_shift lower reductions, and formal completeness remain outside this increment. The full ordinary completeness table keeps its previous owners. Signed negative and out-of-range rational defect thresholds are not newly formalized; their trivial range consequences are not silently counted as Lean targets.

No source evaluator, mass/defect, membershipMatrix, P01DF, Has, HasPlus or HasE definition is edited or substituted. The type-theoretic identities are outside this P02 proof closure. No philosophical consequence, protected change, integration, owner acceptance, historical time compliance or T20 closure is claimed. T20 remains active.
