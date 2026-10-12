import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases

/-!
# Exact four-point positive-probability control

The finite laws below have common distinct real support `(0, 1/3, 2/3, 1)`.
All eight weights are strictly positive, and each vector has total mass one.
Their moments in degrees zero, one, and two agree; their third moments differ
by exactly `1/54`. Everything is expressed using actual sums over `Fin 4`.

`law` is the atomic probability mass function on the real support, not a
measure-theoretic integral. `moment` accepts any natural degree, including
zero with Lean's usual convention `x ^ 0 = 1`.
-/

noncomputable section

namespace FiniteMomentRecovery.FourPoint

open scoped BigOperators

/-- The four real support points, in the displayed order. -/
def x : Fin 4 → ℝ := ![0, 1 / 3, 2 / 3, 1]

/-- The first probability-weight vector. -/
def wPlus : Fin 4 → ℝ := ![5 / 24, 9 / 24, 3 / 24, 7 / 24]

/-- The second probability-weight vector. -/
def wMinus : Fin 4 → ℝ := ![7 / 24, 3 / 24, 9 / 24, 5 / 24]

/-- The finite power moment, defined uniformly for every natural degree. -/
def moment (w : Fin 4 → ℝ) (degree : ℕ) : ℝ :=
  ∑ i : Fin 4, w i * x i ^ degree

/-- Atomic mass at an arbitrary real point. -/
def law (w : Fin 4 → ℝ) (t : ℝ) : ℝ := by
  classical
  exact ∑ i : Fin 4, if x i = t then w i else 0

theorem support_pairwise_distinct : Pairwise (fun i j : Fin 4 => x i ≠ x j) := by
  intro i j hij
  fin_cases i <;> fin_cases j <;> norm_num [x] at *

theorem support_in_unit_interval (i : Fin 4) : 0 ≤ x i ∧ x i ≤ 1 := by
  fin_cases i <;> norm_num [x]

theorem wPlus_positive (i : Fin 4) : 0 < wPlus i := by
  fin_cases i <;> norm_num [wPlus]

theorem wMinus_positive (i : Fin 4) : 0 < wMinus i := by
  fin_cases i <;> norm_num [wMinus]

theorem wPlus_total : (∑ i : Fin 4, wPlus i) = 1 := by
  norm_num [wPlus, Fin.sum_univ_succ]

theorem wMinus_total : (∑ i : Fin 4, wMinus i) = 1 := by
  norm_num [wMinus, Fin.sum_univ_succ]

theorem moment_zero_plus : moment wPlus 0 = 1 := by
  norm_num [moment, wPlus, x, Fin.sum_univ_succ]

theorem moment_one_plus : moment wPlus 1 = 1 / 2 := by
  norm_num [moment, wPlus, x, Fin.sum_univ_succ]

theorem moment_two_plus : moment wPlus 2 = 7 / 18 := by
  norm_num [moment, wPlus, x, Fin.sum_univ_succ]

theorem moments_zero_one_two (degree : Fin 3) :
    moment wPlus degree.val = moment wMinus degree.val := by
  fin_cases degree <;> norm_num [moment, wPlus, wMinus, x, Fin.sum_univ_succ]

theorem moments_agree_through_two (degree : ℕ) (hdegree : degree ≤ 2) :
    moment wPlus degree = moment wMinus degree :=
  moments_zero_one_two ⟨degree, Nat.lt_succ_of_le hdegree⟩

theorem moment_three_plus : moment wPlus 3 = 37 / 108 := by
  norm_num [moment, wPlus, x, Fin.sum_univ_succ]

theorem moment_three_minus : moment wMinus 3 = 35 / 108 := by
  norm_num [moment, wMinus, x, Fin.sum_univ_succ]

theorem third_moment_difference : moment wPlus 3 - moment wMinus 3 = 1 / 54 := by
  norm_num [moment_three_plus, moment_three_minus]

theorem third_moments_differ : moment wPlus 3 ≠ moment wMinus 3 := by
  norm_num [moment_three_plus, moment_three_minus]

theorem weights_differ : wPlus ≠ wMinus := by
  intro h
  exact third_moments_differ (congrArg (fun w => moment w 3) h)

theorem law_at_support (w : Fin 4 → ℝ) (i : Fin 4) : law w (x i) = w i := by
  classical
  unfold law
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hji
    simp [support_pairwise_distinct hji]
  · intro hi
    exact False.elim (hi (Finset.mem_univ i))

theorem law_plus_at_zero : law wPlus 0 = 5 / 24 := by
  norm_num [law, wPlus, x, Fin.sum_univ_succ]

theorem law_minus_at_zero : law wMinus 0 = 7 / 24 := by
  norm_num [law, wMinus, x, Fin.sum_univ_succ]

theorem laws_differ : law wPlus ≠ law wMinus := by
  intro h
  apply weights_differ
  funext i
  have hi := congrFun h (x i)
  simpa only [law_at_support] using hi

/-- A single statement collecting the positive-probability counterexample. -/
theorem positive_probability_counterexample :
    Pairwise (fun i j : Fin 4 => x i ≠ x j) ∧
    (∀ i : Fin 4, 0 < wPlus i) ∧
    (∀ i : Fin 4, 0 < wMinus i) ∧
    (∑ i : Fin 4, wPlus i) = 1 ∧
    (∑ i : Fin 4, wMinus i) = 1 ∧
    (∀ degree : ℕ, degree ≤ 2 → moment wPlus degree = moment wMinus degree) ∧
    moment wPlus 3 - moment wMinus 3 = 1 / 54 ∧
    law wPlus ≠ law wMinus := by
  exact ⟨support_pairwise_distinct, wPlus_positive, wMinus_positive,
    wPlus_total, wMinus_total, moments_agree_through_two,
    third_moment_difference, laws_differ⟩

end FiniteMomentRecovery.FourPoint
