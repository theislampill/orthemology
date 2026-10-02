import BayesBridge

namespace CentredBernoulli
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge
open scoped ENNReal

lemma exp_quadratic_upper {x : ℝ} (hx : |x|≤1) : Real.exp x ≤ 1+x+x^2 := by
  have h := (abs_le.mp (Real.abs_exp_sub_one_sub_id_le hx)).2
  linarith

/-- The variance-sensitive centered Bernoulli MGF bound follows from the genuine
quadratic remainder estimate for the real exponential, with no probability axiom. -/
lemma one_mgf_upper {a t : ℝ} (ha : 0≤a) (ha1 : a≤1) (ht : |t|≤1) :
    (1-a)*Real.exp (-t*a) + a*Real.exp (t*(1-a)) ≤ Real.exp (t^2*a*(1-a)) := by
  have hb : 0≤1-a := by linarith
  have h0 : |-t*a|≤1 := by
    rw [abs_mul,abs_neg,abs_of_nonneg ha]
    exact (mul_le_mul_of_nonneg_right ht ha).trans (by nlinarith)
  have h1 : |t*(1-a)|≤1 := by
    rw [abs_mul,abs_of_nonneg hb]
    exact (mul_le_mul_of_nonneg_right ht hb).trans (by nlinarith)
  calc
    _ ≤ (1-a)*(1+(-t*a)+(-t*a)^2) + a*(1+t*(1-a)+(t*(1-a))^2) :=
      add_le_add (mul_le_mul_of_nonneg_left (exp_quadratic_upper h0) hb)
        (mul_le_mul_of_nonneg_left (exp_quadratic_upper h1) ha)
    _ = 1+t^2*a*(1-a) := by ring
    _ ≤ _ := by linarith [Real.add_one_le_exp (t^2*a*(1-a))]

def realWeight (n : ℕ) (a : ℝ) (word : Fin n → Bool) : ℝ :=
  ∏ i, if word i then a else 1-a

def centredSum (n : ℕ) (a : ℝ) (word : Fin n → Bool) : ℝ :=
  ∑ i, if word i then 1-a else -a

lemma realWeight_nonneg (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (word : Fin n → Bool) :
    0≤realWeight n a word := by
  apply Finset.prod_nonneg
  intro i hi
  split <;> linarith

lemma weight_eq_ofReal (n : ℕ) (a : ℝ) (word : Fin n → Bool) :
    weight n a word = ENNReal.ofReal (realWeight n a word) := rfl

lemma word_mgf_product (n : ℕ) (a t : ℝ) (word : Fin n → Bool) :
    realWeight n a word * Real.exp (t*centredSum n a word) =
      ∏ i, (if word i then a else 1-a) * Real.exp (t*(if word i then 1-a else -a)) := by
  unfold realWeight centredSum
  rw [Finset.mul_sum,Real.exp_sum,Finset.prod_mul_distrib]

lemma word_mgf_exact (n : ℕ) (a t : ℝ) :
    ∑ word : Fin n → Bool, realWeight n a word * Real.exp (t*centredSum n a word) =
      ((1-a)*Real.exp (-t*a) + a*Real.exp (t*(1-a)))^n := by
  simp_rw [word_mgf_product]
  rw [← Fintype.prod_sum (fun (_i : Fin n) (b : Bool) =>
    (if b then a else 1-a) * Real.exp (t*(if b then 1-a else -a)))]
  simp [mul_neg,neg_mul,add_comm]

lemma word_mgf_upper (n : ℕ) {a t : ℝ} (ha : 0≤a) (ha1 : a≤1) (ht : |t|≤1) :
    ∑ word : Fin n → Bool, realWeight n a word * Real.exp (t*centredSum n a word) ≤
      Real.exp ((n:ℝ)*t^2*a*(1-a)) := by
  rw [word_mgf_exact]
  have hb : 0≤1-a := by linarith
  have hm : 0≤(1-a)*Real.exp (-t*a) + a*Real.exp (t*(1-a)) := by positivity
  have h := pow_le_pow_left₀ hm (one_mgf_upper ha ha1 ht) n
  rw [← Real.exp_nat_mul] at h
  convert h using 1 <;> congr 1 <;> ring

end
end CentredBernoulli
