import Mathlib

/-!
Scoped finite certificates for the sparse-prior packet.

This file proves loss separation and a finite adjacent-minimum identity.
It does not formalize the infinite prior, Bayes selector, concentration,
integrability criterion, or endpoint-atom theorem.
-/
namespace SparsePriorGeometry

noncomputable section
open Finset

/-- Both-truth weak acceptance for the exact inherited excesses. -/
def Accepted (a epsilon q : ℝ) : Prop :=
  q ^ 2 - (1 / 4 : ℝ) - a * epsilon * (1 + epsilon) ≤ 0 ∧
  (1 - q) ^ 2 - (1 / 4 : ℝ) + a * epsilon * (1 - epsilon) ≤ 0

/-- The hypothesis-specific affine report has its exact negative margin. -/
theorem own_report_margin (a epsilon : ℝ) :
    ((1 / 2 : ℝ) + epsilon * a) ^ 2 - (1 / 4 : ℝ) -
        a * epsilon * (1 + epsilon) = -epsilon ^ 2 * a * (1-a) ∧
    (1 - ((1 / 2 : ℝ) + epsilon * a)) ^ 2 - (1 / 4 : ℝ) +
        a * epsilon * (1 - epsilon) = -epsilon ^ 2 * a * (1-a) := by
  constructor <;> ring

/-- Any common accepted report bounds the multiplicative parameter ratio. -/
theorem acceptance_ratio {a b epsilon q : ℝ} (he : 0 < epsilon)
    (ha : Accepted a epsilon q) (hb : Accepted b epsilon q) :
    b * (1-epsilon) ≤ a * (1+epsilon) := by
  apply (mul_le_mul_right he).mp
  have hsq : 0 ≤ (q - (1 / 2 : ℝ)) ^ 2 := sq_nonneg _
  rcases ha with ⟨ha0, ha1⟩
  rcases hb with ⟨hb0, hb1⟩
  nlinarith

/-- A factor-two gap separates the exact acceptance sets. -/
theorem no_common_report_at_factor_two {a b epsilon q : ℝ}
    (ha : 0 < a) (he : 0 < epsilon) (he4 : epsilon ≤ (1 / 4 : ℝ))
    (hab : 2 * a ≤ b) : ¬ (Accepted a epsilon q ∧ Accepted b epsilon q) := by
  intro h
  have hr := acceptance_ratio he h.1 h.2
  have hp : 0 ≤ 1-epsilon := by linarith
  have hm := mul_le_mul_of_nonneg_right hab hp
  have hs : 0 ≤ a * ((1 / 4 : ℝ)-epsilon) :=
    mul_nonneg (le_of_lt ha) (by linarith)
  nlinarith

/-- Finite exact adjacent-minimum identity for a sequence with a declared mode.
The hypotheses are local monotonicity on either side; no nonnegativity is
needed for this finite algebraic identity. -/
theorem adjacent_min_sum (a : ℕ → ℝ) (n m : ℕ) (hm : m ≤ n)
    (hup : ∀ i, i < m → a i ≤ a (i+1))
    (hdown : ∀ i, m ≤ i → i < n → a (i+1) ≤ a i) :
    (∑ i ∈ range n, min (a i) (a (i+1))) =
      (∑ i ∈ range (n+1), a i) - a m := by
  induction n with
  | zero =>
      have hm0 : m = 0 := by omega
      subst m
      simp
  | succ n ih =>
      by_cases hm' : m ≤ n
      · have hdown' : ∀ i, m ≤ i → i < n → a (i+1) ≤ a i := by
          intro i hmi hin
          exact hdown i hmi (by omega)
        have hprev := ih hm' hdown'
        rw [sum_range_succ, hprev, min_eq_right (hdown n hm' (by omega))]
        simp only [sum_range_succ]
        ring
      · have heq : m = n+1 := by omega
        subst m
        have heach : (∑ i ∈ range (n+1), min (a i) (a (i+1))) =
            ∑ i ∈ range (n+1), a i := by
          apply sum_congr rfl
          intro i hi
          exact min_eq_left (hup i (mem_range.mp hi))
        rw [heach]
        simp only [sum_range_succ]
        ring

#print axioms own_report_margin
#print axioms acceptance_ratio
#print axioms no_common_report_at_factor_two
#print axioms adjacent_min_sum

end
end SparsePriorGeometry
