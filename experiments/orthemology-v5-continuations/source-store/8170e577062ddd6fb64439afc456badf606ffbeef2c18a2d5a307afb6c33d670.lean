import EmpiricalGeometry

namespace EmpiricalChernoff
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge CentredBernoulli EmpiricalGeometry
open scoped ENNReal

lemma exp_pair_dominates_one {y b t : ℝ} (ht : 0≤t) (hy : b < |y|) :
    1≤Real.exp (-t*b)*(Real.exp (t*y)+Real.exp ((-t)*y)) := by
  rcases lt_abs.mp hy with h|h
  · have he : 1≤Real.exp (-t*b)*Real.exp (t*y) := by
      rw [← Real.exp_add]
      have hxy : 0≤-t*b+t*y := by nlinarith
      simpa using Real.exp_le_exp.mpr hxy
    nlinarith [Real.exp_pos (-t*b),Real.exp_pos ((-t)*y)]
  · have he : 1≤Real.exp (-t*b)*Real.exp ((-t)*y) := by
      rw [← Real.exp_add]
      have hxy : 0≤-t*b+(-t)*y := by nlinarith
      simpa using Real.exp_le_exp.mpr hxy
    nlinarith [Real.exp_pos (-t*b),Real.exp_pos (t*y)]

def realError (n : ℕ) (a e : ℝ) : ℝ := by
  classical
  exact ∑ word : Fin n → Bool, realWeight n a word *
    (if Accepted a e (empiricalReport n e word) then 0 else 1)

def error (n : ℕ) (a e : ℝ) : ℝ≥0∞ :=
  ∑ word : Fin n → Bool, weight n a word * failureIndicator e (empiricalReport n e word) a

lemma realError_nonneg (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (e : ℝ) :
    0≤realError n a e := by
  classical
  apply Finset.sum_nonneg
  intro word hword
  apply mul_nonneg (realWeight_nonneg n ha ha1 word)
  split <;> norm_num

lemma error_eq_ofReal (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (e : ℝ) :
    error n a e = ENNReal.ofReal (realError n a e) := by
  classical
  unfold error realError
  rw [ENNReal.ofReal_sum_of_nonneg (by
    intro word hword
    apply mul_nonneg (realWeight_nonneg n ha ha1 word)
    split <;> norm_num)]
  apply Finset.sum_congr rfl
  intro word hword
  by_cases h : Accepted a e (empiricalReport n e word)
  · simp [failureIndicator,h]
  · simp [failureIndicator,h,weight_eq_ofReal]

/-- Direct finite-word Chernoff estimate for the literal empirical report. -/
theorem realError_upper (n : ℕ) (hn : 0<n) {a e : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (he : 0<e) (he4 : e≤1/4) :
    realError n a e ≤ 2*Real.exp (-((n:ℝ)*e^2*a*(1-a)/16)) := by
  classical
  let t := e/4
  let b := (n:ℝ)*e*a*(1-a)/2
  have ht0 : 0≤t := by dsimp [t];positivity
  have ht : |t|≤1 := by rw [abs_of_nonneg ht0];dsimp [t];linarith
  have htn : |-t|≤1 := by simpa using ht
  have hpoint : ∀ word : Fin n → Bool,
      (if Accepted a e (empiricalReport n e word) then (0:ℝ) else 1) ≤
        Real.exp (-t*b)*(Real.exp (t*centredSum n a word)+Real.exp ((-t)*centredSum n a word)) := by
    intro word
    split
    · positivity
    · exact exp_pair_dominates_one ht0 (not_accepted_deviation hn ha ha1 he he4 word ‹_›)
  have hsum := Finset.sum_le_sum (fun word (_ : word ∈ (Finset.univ : Finset (Fin n → Bool))) =>
    mul_le_mul_of_nonneg_left (hpoint word) (realWeight_nonneg n ha ha1 word))
  have heq : (∑ word : Fin n → Bool, realWeight n a word *
      (Real.exp (-t*b)*(Real.exp (t*centredSum n a word)+Real.exp ((-t)*centredSum n a word)))) =
      Real.exp (-t*b)*((∑ word : Fin n → Bool, realWeight n a word * Real.exp (t*centredSum n a word)) +
        (∑ word : Fin n → Bool, realWeight n a word * Real.exp ((-t)*centredSum n a word))) := by
    simp_rw [mul_add]
    rw [Finset.sum_add_distrib]
    congr 1 <;> rw [Finset.mul_sum] <;> apply Finset.sum_congr rfl <;> intros <;> ring
  rw [heq] at hsum
  have hp := word_mgf_upper n ha ha1 ht
  have hm := word_mgf_upper n ha ha1 htn
  simp only [neg_sq] at hm
  have hbound := hsum.trans (mul_le_mul_of_nonneg_left (add_le_add hp hm) (Real.exp_pos _).le)
  change realError n a e ≤ _ at hbound
  have heq2 : Real.exp (-t*b)*(Real.exp ((n:ℝ)*t^2*a*(1-a))+
      Real.exp ((n:ℝ)*t^2*a*(1-a))) = 2*Real.exp (-((n:ℝ)*e^2*a*(1-a)/16)) := by
    rw [← two_mul,← mul_assoc,mul_comm (Real.exp (-t*b)) 2,mul_assoc,← Real.exp_add]
    congr 1
    dsimp [t,b]
    ring
  rwa [heq2] at hbound

theorem error_upper (n : ℕ) (hn : 0<n) {a e : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (he : 0<e) (he4 : e≤1/4) :
    error n a e ≤ ENNReal.ofReal (2*Real.exp (-((n:ℝ)*e^2*a*(1-a)/16))) := by
  rw [error_eq_ofReal n ha ha1 e]
  exact ENNReal.ofReal_le_ofReal (realError_upper n hn ha ha1 he he4)

end
end EmpiricalChernoff
