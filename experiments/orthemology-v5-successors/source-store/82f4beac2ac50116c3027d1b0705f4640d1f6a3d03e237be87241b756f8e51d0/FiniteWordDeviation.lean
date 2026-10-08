import CentredBernoulli

noncomputable section
open MeasureTheory Set
open scoped BigOperators ENNReal

namespace HiddenParity.Exponential
open CentredBernoulli

lemma exp_pair_dominates_one_le {y b t : ℝ} (ht : 0 ≤ t) (hy : b ≤ |y|) :
    1 ≤ Real.exp (-t*b) * (Real.exp (t*y) + Real.exp ((-t)*y)) := by
  rcases le_abs.mp hy with h | h
  · have he : 1 ≤ Real.exp (-t*b) * Real.exp (t*y) := by
      rw [← Real.exp_add]
      have hx : 0 ≤ -t*b+t*y := by nlinarith
      simpa using Real.exp_le_exp.mpr hx
    nlinarith [Real.exp_pos (-t*b), Real.exp_pos ((-t)*y)]
  · have he : 1 ≤ Real.exp (-t*b) * Real.exp ((-t)*y) := by
      rw [← Real.exp_add]
      have hx : 0 ≤ -t*b+(-t)*y := by nlinarith
      simpa using Real.exp_le_exp.mpr hx
    nlinarith [Real.exp_pos (-t*b), Real.exp_pos (t*y)]

def realDeviation (n : ℕ) (p η : ℝ) : ℝ := by
  classical
  exact ∑ w : Fin n → Bool, realWeight n p w *
    (if (n:ℝ)*η ≤ |centredSum n p w| then 1 else 0)

/-- An explicit elementary exponential bound. The rate is deliberately weaker
than sharp Hoeffding and uses the retained, already checked Bernoulli MGF. -/
theorem realDeviation_le (n : ℕ) {p η : ℝ}
    (hp : 0 ≤ p) (hp1 : p ≤ 1) (hη : 0 ≤ η) (hη1 : η ≤ 1) :
    realDeviation n p η ≤ 2 * Real.exp (-((n:ℝ)*η^2/2)) := by
  classical
  have ht : |η| ≤ 1 := by simpa [abs_of_nonneg hη] using hη1
  have htn : |-η| ≤ 1 := by simpa using ht
  have hpoint : ∀ w : Fin n → Bool,
      (if (n:ℝ)*η ≤ |centredSum n p w| then (1:ℝ) else 0) ≤
      Real.exp (-η*((n:ℝ)*η)) *
        (Real.exp (η*centredSum n p w) + Real.exp ((-η)*centredSum n p w)) := by
    intro w
    split
    · exact exp_pair_dominates_one_le hη ‹_›
    · positivity
  have hsum := Finset.sum_le_sum (fun w (_ : w ∈ (Finset.univ : Finset (Fin n → Bool))) =>
    mul_le_mul_of_nonneg_left (hpoint w) (realWeight_nonneg n hp hp1 w))
  have heq : (∑ w : Fin n → Bool, realWeight n p w *
      (Real.exp (-η*((n:ℝ)*η)) *
        (Real.exp (η*centredSum n p w) + Real.exp ((-η)*centredSum n p w)))) =
      Real.exp (-η*((n:ℝ)*η)) *
       ((∑ w : Fin n → Bool, realWeight n p w * Real.exp (η*centredSum n p w)) +
        (∑ w : Fin n → Bool, realWeight n p w * Real.exp ((-η)*centredSum n p w))) := by
    simp_rw [mul_add]
    rw [Finset.sum_add_distrib]
    congr 1 <;> rw [Finset.mul_sum] <;> apply Finset.sum_congr rfl <;> intros <;> ring
  rw [heq] at hsum
  have hplus := word_mgf_upper n hp hp1 ht
  have hminus := word_mgf_upper n hp hp1 htn
  simp only [neg_sq] at hminus
  have hbound := hsum.trans
    (mul_le_mul_of_nonneg_left (add_le_add hplus hminus) (Real.exp_pos _).le)
  change realDeviation n p η ≤ _ at hbound
  have hvar : p*(1-p) ≤ 1/2 := by nlinarith [sq_nonneg (p-1/2)]
  have hnη : 0 ≤ (n:ℝ)*η^2 := by positivity
  have hexp : -η*((n:ℝ)*η)+(n:ℝ)*η^2*p*(1-p) ≤ -((n:ℝ)*η^2/2) := by
    have := mul_le_mul_of_nonneg_left hvar hnη
    nlinarith
  calc
    realDeviation n p η ≤ _ := hbound
    _ = 2 * Real.exp (-η*((n:ℝ)*η)+(n:ℝ)*η^2*p*(1-p)) := by
      rw [← two_mul, ← mul_assoc, mul_comm (Real.exp _) 2, mul_assoc, ← Real.exp_add]
    _ ≤ _ := mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr hexp) (by norm_num)

#print axioms realDeviation_le
end HiddenParity.Exponential
