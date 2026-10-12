import Mathlib.LinearAlgebra.Vandermonde
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
# Finite-support moment recovery

Fresh formal verification of the finite algebraic core of
`tensor-moment-continuation-20261009/RESULT.md`, Theorem 1.
The support is known and pairwise distinct, weights are arbitrary, and N is arbitrary.
No interpolation, recovery, or nonsingularity is assumed. These facts are proved
from the Vandermonde determinant product and the distinctness hypothesis.
-/

noncomputable section

open scoped BigOperators
open Matrix

namespace FiniteMoment

variable {K : Type*} [Field K] {N : ℕ}

/-- Degree-r scalar moment, including the degree-zero total mass. -/
def moment (a w : Fin N → K) (r : ℕ) : K := ∑ j, w j * a j ^ r

/-- The retained degrees are exactly 0 through N-1, even for N=0. -/
def record (a w : Fin N → K) : Fin N → K := fun r => moment a w r.val

/-- Recovery coefficients depend on the known support alone. -/
def recoveryCoefficient (a : Fin N → K) (j r : Fin N) : K :=
  (Matrix.vandermonde a)⁻¹ r j

/-- Explicit linear reconstruction from a prospective moment record. -/
def recover (a : Fin N → K) (s : Fin N → K) : Fin N → K :=
  fun j => ∑ r, s r * recoveryCoefficient a j r

/-- Proved from the determinant product; no invertibility premise is hidden here. -/
theorem determinant_ne_zero (a : Fin N → K) (ha : Function.Injective a) :
    (Matrix.vandermonde a).det ≠ 0 := by
  rw [Matrix.det_vandermonde]
  apply Finset.prod_ne_zero_iff.mpr
  intro i _
  apply Finset.prod_ne_zero_iff.mpr
  intro j hj
  apply sub_ne_zero.mpr
  exact fun h => (Finset.mem_Ioi.mp hj).ne' (ha h)

/-- The actual finite moment record is multiplication by the Vandermonde matrix. -/
theorem record_eq_vecMul (a w : Fin N → K) :
    record a w = w ᵥ* Matrix.vandermonde a := rfl

/-- The displayed reconstruction is multiplication by its nonsingular inverse. -/
theorem recover_eq_vecMul (a s : Fin N → K) :
    recover a s = s ᵥ* (Matrix.vandermonde a)⁻¹ := rfl

/-- All arbitrary field-valued weights are recovered from degrees 0 through N-1. -/
theorem recover_record (a : Fin N → K) (ha : Function.Injective a) (w : Fin N → K) :
    recover a (record a w) = w := by
  rw [recover_eq_vecMul, record_eq_vecMul, Matrix.vecMul_vecMul,
    Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.mpr (determinant_ne_zero a ha)),
    Matrix.vecMul_one]

/-- Conversely, reconstruction produces exactly the proposed finite moment tuple. -/
theorem record_recover (a : Fin N → K) (ha : Function.Injective a) (s : Fin N → K) :
    record a (recover a s) = s := by
  rw [record_eq_vecMul, recover_eq_vecMul, Matrix.vecMul_vecMul,
    Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr (determinant_ne_zero a ha)),
    Matrix.vecMul_one]

/-- For known distinct support, the finite moment record is an explicit linear equivalence. -/
def recordLinearEquiv (a : Fin N → K) (ha : Function.Injective a) :
    (Fin N → K) ≃ₗ[K] (Fin N → K) :=
  { (Matrix.vandermonde a).vecMulLinear with
    invFun := recover a
    left_inv := recover_record a ha
    right_inv := record_recover a ha }

/-- Coordinate version of the explicit finite reconstruction formula. -/
theorem weight_eq_sum_moments (a : Fin N → K) (ha : Function.Injective a)
    (w : Fin N → K) (j : Fin N) :
    w j = ∑ r : Fin N, moment a w r.val * recoveryCoefficient a j r := by
  exact (congrFun (recover_record a ha w) j).symm

/-- Equal first N moments of known distinct support determine every weight. -/
theorem weights_eq_of_moments_eq (a : Fin N → K) (ha : Function.Injective a)
    (w z : Fin N → K) (h : ∀ r : Fin N, moment a w r.val = moment a z r.val) :
    w = z := by
  have hr : record a w = record a z := funext h
  calc
    w = recover a (record a w) := (recover_record a ha w).symm
    _ = recover a (record a z) := congrArg (recover a) hr
    _ = z := recover_record a ha z

/-- The retained moment record is injective as a function of arbitrary weights. -/
theorem record_injective (a : Fin N → K) (ha : Function.Injective a) :
    Function.Injective (record a) := by
  intro w z h
  exact weights_eq_of_moments_eq a ha w z (congrFun h)

/-- Therefore equality of the finite records entails equality of every higher moment. -/
theorem all_moments_eq_of_record_eq (a : Fin N → K) (ha : Function.Injective a)
    (w z : Fin N → K) (h : record a w = record a z) :
    ∀ r : ℕ, moment a w r = moment a z r := by
  have hw := record_injective a ha h
  subst z
  exact fun _ => rfl

/-- Every scalar observable on known support is a fixed linear function of the record. -/
theorem observable_reconstruction (a : Fin N → K) (ha : Function.Injective a)
    (w f : Fin N → K) :
    ∑ j, w j * f j =
      ∑ r : Fin N, moment a w r.val * (∑ j, recoveryCoefficient a j r * f j) := by
  conv_lhs => arg 2; ext j; rw [weight_eq_sum_moments a ha w j]
  simp_rw [Finset.sum_mul, mul_assoc]
  rw [Finset.sum_comm]
  simp_rw [Finset.mul_sum]

/-- In particular, all higher scalar moments have explicit support-dependent coefficients. -/
theorem higher_moment_reconstruction (a : Fin N → K) (ha : Function.Injective a)
    (w : Fin N → K) (k : ℕ) :
    moment a w k =
      ∑ r : Fin N, moment a w r.val *
        (∑ j, recoveryCoefficient a j r * a j ^ k) := by
  exact observable_reconstruction a ha w (fun j => a j ^ k)

/-- Vector-valued observables, including any chosen tensor powers, obey the same formula.
No tensor/ODE infrastructure or analytic inference is asserted by this algebraic theorem. -/
theorem vector_observable_reconstruction {V : Type*} [AddCommGroup V] [Module K V]
    (a : Fin N → K) (ha : Function.Injective a) (w : Fin N → K) (f : Fin N → V) :
    ∑ j, w j • f j =
      ∑ r : Fin N, moment a w r.val • (∑ j, recoveryCoefficient a j r • f j) := by
  conv_lhs => arg 2; ext j; rw [weight_eq_sum_moments a ha w j]
  simp_rw [Finset.sum_smul, MulAction.mul_smul]
  rw [Finset.sum_comm]
  simp_rw [Finset.smul_sum]

end FiniteMoment
