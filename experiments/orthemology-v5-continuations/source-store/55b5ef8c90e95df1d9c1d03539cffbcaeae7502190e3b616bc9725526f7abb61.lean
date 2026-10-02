import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic

namespace Orthemology.IntegerBudget

lemma two_pow_le_exp_nat (k : ℕ) : (2 : ℝ)^k ≤ Real.exp (k : ℝ) := by
  have h : (2 : ℝ) ≤ Real.exp 1 := by
    have := Real.add_one_le_exp (1 : ℝ)
    linarith
  calc
    (2 : ℝ)^k ≤ (Real.exp 1)^k := pow_le_pow_left₀ (by norm_num) h k
    _ = Real.exp (k : ℝ) := by rw [← Real.exp_nat_mul]; simp

/-- Exact dyadic witnesses bound an exponential tail term; this is arithmetic,
not a claim that any stochastic model satisfies the supplied tail premise. -/
theorem dyadic_tail (A δ x : ℝ) (k : ℕ)
    (hA : 0 ≤ A) (hδ : 0 ≤ δ)
    (hw : 2*A ≤ δ*(2:ℝ)^k) (hx : (k:ℝ) ≤ x) :
    A * Real.exp (-x) ≤ δ/2 := by
  have hpow : (2:ℝ)^k ≤ Real.exp x :=
    (two_pow_le_exp_nat k).trans (Real.exp_le_exp.mpr hx)
  have hmain : 2*A ≤ δ * Real.exp x :=
    hw.trans (mul_le_mul_of_nonneg_left hpow hδ)
  have he := Real.exp_pos (-x)
  have hm := mul_le_mul_of_nonneg_right hmain he.le
  have hexp : Real.exp x * Real.exp (-x) = 1 := by
    rw [← Real.exp_add]; simp
  nlinarith [show δ * Real.exp x * Real.exp (-x) = δ by rw [mul_assoc, hexp, mul_one]]

/-- Confidence bound from the two explicitly supplied real tail terms and
integer dyadic witnesses. No controller, probability law or cost theorem is
introduced as an axiom: their numerical tail consequence is a visible premise. -/
theorem confidence_from_witnesses
    (bad A δ c D r lam T : ℝ) (N J k ell : ℕ)
    (hA : 0 ≤ A) (hδ : 0 ≤ δ) (hD : 0 < D) (hT : 0 ≤ T)
    (hlam : r/2 ≤ lam)
    (hw₁ : 2*A ≤ δ*(2:ℝ)^k)
    (hw₂ : 2 ≤ δ*(2:ℝ)^ell)
    (hN : (k:ℝ) ≤ c*N)
    (hbudget : 2*D*((J:ℝ)+ell) ≤ r*T)
    (htail : bad ≤ A*Real.exp (-(c*N)) +
      (2:ℝ)^J * Real.exp (-(lam*T/D))) : bad ≤ δ := by
  have hfirst := dyadic_tail A δ (c*N) k hA hδ hw₁ hN
  have hprod : (r/2)*T ≤ lam*T := mul_le_mul_of_nonneg_right hlam hT
  have htime : ((J:ℝ)+(ell:ℝ))*D ≤ lam*T := by nlinarith
  have hx : ((J+ell:ℕ):ℝ) ≤ lam*T/D := by
    rw [le_div_iff₀ hD]
    simpa only [Nat.cast_add] using htime
  have hp : 0 ≤ (2:ℝ)^J := by positivity
  have hw : 2*(2:ℝ)^J ≤ δ*(2:ℝ)^(J+ell) := by
    have hh := mul_le_mul_of_nonneg_left hw₂ hp
    rw [pow_add]
    nlinarith
  have hsecond := dyadic_tail ((2:ℝ)^J) δ (lam*T/D) (J+ell) hp hδ hw hx
  linarith

#print axioms two_pow_le_exp_nat
#print axioms dyadic_tail
#print axioms confidence_from_witnesses
end Orthemology.IntegerBudget
