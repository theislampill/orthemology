import Moment
import PolynomialBridge
import ScalarSupport

namespace FullPolynomialCountermodel
open MvPolynomial FullFunctionalPolynomialBridge

/-- The actual Schur-recursive linear functional on the whole bivariate algebra. -/
noncomputable def Λ : Polynomial →ₗ[ℝ] ℝ := functional FullFunctionalMoment.moment

/-- Unbounded strict square positivity, with no semantic positivity premise. -/
theorem strict_square_positive (p : Polynomial) (hp : p ≠ 0) : 0 < Λ (p^2) := by
  apply square_strict_positive FullFunctionalMoment.moment
    (fun n => FullFunctionalMoment.gram_positive n) p hp

@[simp] theorem normalized : Λ 1 = 1 := by
  exact (functional_one _).trans FullFunctionalMoment.moment_zero

noncomputable def witness : Polynomial :=
  1 + X (0 : Fin 2)^4 * X (1 : Fin 2)^2 +
    X (0 : Fin 2)^2 * X (1 : Fin 2)^4 - X (0 : Fin 2)^2 * X (1 : Fin 2)^2

theorem witness_negative : Λ witness = -1 := by
  have h0 : FullFunctionalMoment.moment 0 = 1 := FullFunctionalMoment.moment_zero
  norm_num [witness, Λ, map_add, map_sub, h0]

theorem witness_eval (x : Fin 2 → ℝ) :
    eval x witness = FullPolynomialMomentSupport.F (x 0) (x 1) := by
  simp [witness,FullPolynomialMomentSupport.F]

theorem witness_lower_bound (x : Fin 2 → ℝ) : (3:ℝ)/4 ≤ eval x witness := by
  rw [witness_eval]
  exact FullPolynomialMomentSupport.F_lower_bound _ _

theorem square_nonnegative (p : Polynomial) : 0 ≤ Λ (p^2) := by
  by_cases hp : p = 0
  · simp [hp]
  · exact le_of_lt (strict_square_positive p hp)

theorem finite_sum_squares_nonnegative {α : Type*} (s : Finset α) (p : α → Polynomial) :
    0 ≤ Λ (∑ i ∈ s, p i ^ 2) := by
  rw [map_sum]
  exact Finset.sum_nonneg (fun i _ => square_nonnegative (p i))

/-- This explicitly constructed functional separates strict square positivity
from positivity on pointwise nonnegative polynomials. -/
theorem full_polynomial_countermodel :
    ∃ L : Polynomial →ₗ[ℝ] ℝ,
      L 1 = 1 ∧
      (∀ p : Polynomial, p ≠ 0 → 0 < L (p^2)) ∧
      (∀ x : Fin 2 → ℝ, (3:ℝ)/4 ≤ eval x witness) ∧ L witness = -1 :=
  ⟨Λ, normalized, strict_square_positive, witness_lower_bound, witness_negative⟩

/-- Every representation positive on all pointwise nonnegative polynomials is
excluded. This theorem does not hide a positivity assumption on Λ itself. -/
theorem not_pointwise_positive :
    ¬ (∀ p : Polynomial, (∀ x : Fin 2 → ℝ, 0 ≤ eval x p) → 0 ≤ Λ p) := by
  intro h
  have hw := h witness (fun x => le_trans (by norm_num) (witness_lower_bound x))
  rw [witness_negative] at hw
  norm_num at hw

#print axioms strict_square_positive
#print axioms normalized
#print axioms witness_negative
#print axioms witness_lower_bound
#print axioms full_polynomial_countermodel
#print axioms not_pointwise_positive
end FullPolynomialCountermodel
