# Bounded Lean support: scalar positive witness

## Verified result

Lean 4.19.0 with `--trust=0` checks the following statements with no `sorry`, `admit`, new axiom, `native_decide`, or `implemented_by` declarations:

- `FullPolynomialMomentSupport.nonnegative_variables_lower_bound`: if `u,v ≥ 0`, then `1 + u²v + uv² - uv ≥ 3/4`.
- `FullPolynomialMomentSupport.F_lower_bound`: for all real `x,y`, `F(x,y) = 1 + x⁴y² + x²y⁴ - x²y² ≥ 3/4`.
- `FullPolynomialMomentSupport.F_positive`: for all real `x,y`, `F(x,y)>0`.
- `FullPolynomialMomentSupport.separating_seed_value`: the real scalar arithmetic `1+1+1-4=-1`.

All four printed axiom lists contain only Lean/Mathlib's standard `propext`, `Classical.choice`, and `Quot.sound`.

The proof sets `u=x²`, `v=y²`. If `u+v≥1`, the nonconstant part `uv(u+v-1)` is nonnegative. Otherwise, `(u-v)²≥0` and `0≤u+v≤1` imply `uv≤1/4`; dropping the nonnegative term `uv(u+v)` yields the claimed bound. The bound is sufficient; no claim of optimality is made.

## Scope boundary

This support certificate does **not** formalize:

- The enumeration of all bivariate monomials and the midpoint-index lemma.
- The well-founded infinite recurrence for `j_n`.
- A linear functional on all of `ℝ[x,y]`.
- Positive definiteness of every finite Gram matrix.
- Positivity of that functional on every polynomial square.
- The representing-measure contradiction or universal nonexistence of a measure.

In particular, the scalar seed-arithmetic theorem is **not** a proof that an encoded Lean linear functional takes the value `-1` on an encoded Lean polynomial. No such functional is defined in this support file. The accompanying mathematical construction must supply those universal arguments.

## Matrix dependency findings

The trust-zero probe `RetainedMatrixProbe.lean` successfully imports the retained lower-level modules:

- `Mathlib.LinearAlgebra.Matrix.NonsingularInverse`
- `Mathlib.Data.Matrix.Block`
- `Mathlib.Algebra.MvPolynomial.Basic`

`Matrix.mul_nonsing_inv`, `Matrix.nonsing_inv_mul`, determinant, matrix-vector multiplication, block matrices, and `MvPolynomial` are available. Source inspection additionally identifies `Matrix.mulVec_injective_iff_isUnit`, `Matrix.isUnit_iff_isUnit_det`, and `Matrix.invertibleOfIsUnitDet` as the relevant route from positive definiteness to a usable inverse.

The direct retained objects for `Mathlib.LinearAlgebra.Matrix.PosDef`, `SchurComplement`, `Spectrum`, and `Mathlib.LinearAlgebra.QuadraticForm.Basic` are missing. The explicit-source-import graph of `SchurComplement` has 3,461 modules, of which 711 retained objects are missing; `PosDef` has 3,460 modules, of which 710 objects are missing. These are inventory counts, not attempted or estimated compilation work. The corresponding closure counts for `NonsingularInverse` and `MvPolynomial.Basic` contain no missing retained objects. No baseline or missing dependency was rebuilt.

The current library's source `SchurComplement.lean` contains the elementary completed-square identity `Matrix.schur_complement_eq₁₁` and positive-semidefinite block criteria. Importing that entire module would pull the unavailable positive-definiteness and spectral infrastructure.

## Possible no-large-rebuild route

A future formalization can instead stay within the retained algebraic imports:

1. Define real-matrix positive definiteness directly by `∀ c ≠ 0, 0 < cᵀ A c`, together with symmetry.
2. Deduce injectivity of `A.mulVec`; use the retained injectivity/unit/determinant lemmas for its inverse.
3. Prove directly the completed-square identity for `[[A,v],[vᵀ,1+vᵀA⁻¹v]]`. Its quadratic form is `(c+tA⁻¹v)ᵀ A (c+tA⁻¹v)+t²`, so it is strictly positive away from zero.
4. Formalize the exponent-pair enumeration and prove each pairwise-even off-diagonal product uses an earlier midpoint index. This is essential to making the recurrence depend only on earlier moment values.
5. Establish the initial `diag(1,1,1,4)` Gram matrix, run induction on the full Gram recurrence, and bridge finitely supported polynomial coefficients to a sufficiently large finite Gram matrix.
6. Define the actual `MvPolynomial` functional and prove its witness value and square positivity.

This is a prospective proof plan based on verified retained infrastructure. Steps 1–6 have **not** been formalized here, and no elapsed-time estimate is asserted.

## Replay and evidence

From the workspace root, run:

`python3 full-polynomial-moment-countermodel-20261010/lean-support/check_support.py`

This script replays the scalar certificate and import probe at trust zero, verifies printed axioms, records direct-import digests, inventories existing objects, and confirms two false scalar claims are rejected by proof checking rather than missing imports. It never invokes Lake or rebuilds the retained baseline.

- Main source: `ScalarSupport.lean`
- Main proof log: `logs/scalar-trust-zero.log`
- Probe log: `logs/retained-matrix-probe.log`
- Verification receipt: `SUPPORT_RECEIPT.json`
- Matrix inventory: `MATRIX_DEPENDENCY_ASSESSMENT.json`
- Direct object digests: `DIRECT_IMPORTS.json`
- Negative-control logs: `logs/wrong_seed_value.log`, `logs/wrong_origin_value.log`
