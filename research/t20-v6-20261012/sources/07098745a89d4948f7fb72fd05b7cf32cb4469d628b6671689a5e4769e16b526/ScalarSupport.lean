import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
Scalar support for the full-polynomial moment countermodel.

This file checks only the displayed scalar polynomial and seed arithmetic.
It does not formalize the recursive infinite moment functional, positive
 definiteness of all its Gram matrices, or the nonexistence of a representing
measure. Those claims require the accompanying mathematical construction.
-/

namespace FullPolynomialMomentSupport

/-- The globally positive polynomial separated by the proposed functional. -/
def F (x y : ℝ) : ℝ :=
  1 + x ^ 4 * y ^ 2 + x ^ 2 * y ^ 4 - x ^ 2 * y ^ 2

/-- An elementary bound in the nonnegative variables `u = x²`, `v = y²`. -/
theorem nonnegative_variables_lower_bound (u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) :
    (3 : ℝ) / 4 ≤ 1 + u ^ 2 * v + u * v ^ 2 - u * v := by
  have huv : 0 ≤ u * v := mul_nonneg hu hv
  by_cases hs : 1 ≤ u + v
  · have hprod : 0 ≤ u * v * (u + v - 1) :=
      mul_nonneg huv (by linarith)
    nlinarith [hprod]
  · have hsum : 0 ≤ u + v := add_nonneg hu hv
    have hrest : 0 ≤ 1 - (u + v) := by linarith
    have hsum_square : (u + v) ^ 2 ≤ 1 := by
      nlinarith [mul_nonneg hsum hrest]
    have huv_upper : u * v ≤ (1 : ℝ) / 4 := by
      nlinarith [sq_nonneg (u - v)]
    have hpositive : 0 ≤ u * v * (u + v) := mul_nonneg huv hsum
    nlinarith [hpositive]

/-- The scalar polynomial is uniformly bounded away from zero on all of `ℝ²`. -/
theorem F_lower_bound (x y : ℝ) : (3 : ℝ) / 4 ≤ F x y := by
  have h := nonnegative_variables_lower_bound (x ^ 2) (y ^ 2)
    (sq_nonneg x) (sq_nonneg y)
  dsimp [F]
  nlinarith [h]

theorem F_positive (x y : ℝ) : 0 < F x y := by
  have h := F_lower_bound x y
  linarith

/-- The seed values prescribed for the four monomials of `F` give `-1`.
This is scalar arithmetic, not yet a formal definition of a linear functional. -/
theorem separating_seed_value : (1 : ℝ) + 1 + 1 - 4 = -1 := by
  norm_num

#print axioms nonnegative_variables_lower_bound
#print axioms F_lower_bound
#print axioms F_positive
#print axioms separating_seed_value

end FullPolynomialMomentSupport
