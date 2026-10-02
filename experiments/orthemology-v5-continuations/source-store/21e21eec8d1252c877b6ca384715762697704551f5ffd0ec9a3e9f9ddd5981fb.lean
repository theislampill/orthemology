import CentredBernoulli

namespace EmpiricalGeometry
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge CentredBernoulli
open scoped ENNReal

/-- The literal quadratic acceptance inequalities contain a variance-scaled
neighborhood of the true Bernoulli mean. -/
lemma accepted_of_relative_error {a e h : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (he : 0<e) (he4 : e≤1/4) (herr : |h-a|≤e*a*(1-a)/2) :
    Accepted a e (1/2+e*h) := by
  have hb : 0≤1-a := by linarith
  let v := a*(1-a)
  have hv : 0≤v := by dsimp [v];positivity
  have hva : v≤a := by dsimp [v];nlinarith
  have hv1 : v≤1 := hva.trans ha1
  have hd : -e*v/2≤h-a ∧ h-a≤e*v/2 := by
    constructor <;> dsimp [v] <;> nlinarith [(abs_le.mp herr).1,(abs_le.mp herr).2]
  have heV : e*v/2≤v/8 := by nlinarith
  have hlo : a-v/8≤h := by linarith [hd.1]
  have hup : h≤a+v/8 := by linarith [hd.2]
  have hh0 : 0≤h := by linarith
  have hsq : h^2≤(a+v/8)^2 := by nlinarith [sq_nonneg (a+v/8-h)]
  have hstrong : h^2-a≤-v/2 := by
    have hvdef : v=a-a^2 := by dsimp [v];ring
    nlinarith [mul_nonneg (show 0≤1-a by linarith) hv,
      mul_nonneg hv (show 0≤1-v by linarith)]
  have hD0 : D0 a e (1/2+e*h) = e*(h-a)+e^2*(h^2-a) := by unfold D0;ring
  have hD1 : D1 a e (1/2+e*h) = e*(a-h)+e^2*(h^2-a) := by unfold D1;ring
  have hp := mul_le_mul_of_nonneg_left hstrong (sq_nonneg e)
  have hplus := mul_le_mul_of_nonneg_left hd.2 he.le
  have hminus := mul_le_mul_of_nonneg_left hd.1 he.le
  constructor
  · rw [hD0];nlinarith
  · rw [hD1];nlinarith

def empiricalMean (n : ℕ) (word : Fin n → Bool) : ℝ :=
  (∑ i, if word i then (1:ℝ) else 0)/(n:ℝ)

def empiricalReport (n : ℕ) (e : ℝ) (word : Fin n → Bool) : ℝ :=
  1/2+e*empiricalMean n word

lemma centredSum_eq (n : ℕ) (hn : 0<n) (a : ℝ) (word : Fin n → Bool) :
    centredSum n a word = (n:ℝ)*(empiricalMean n word-a) := by
  have hn0 : (n:ℝ)≠0 := by exact_mod_cast (ne_of_gt hn)
  unfold centredSum empiricalMean
  have h : ∀ i : Fin n, (if word i then 1-a else -a) = (if word i then (1:ℝ) else 0)-a := by
    intro i;split <;> ring
  simp_rw [h]
  rw [Finset.sum_sub_distrib]
  simp
  field_simp

lemma not_accepted_deviation {n : ℕ} (hn : 0<n) {a e : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (he : 0<e) (he4 : e≤1/4) (word : Fin n → Bool)
    (hbad : ¬ Accepted a e (empiricalReport n e word)) :
    (n:ℝ)*e*a*(1-a)/2 < |centredSum n a word| := by
  have hnot : ¬ |empiricalMean n word-a|≤e*a*(1-a)/2 := by
    intro h
    exact hbad (accepted_of_relative_error ha ha1 he he4 h)
  have hd := lt_of_not_ge hnot
  have hnpos : (0:ℝ)<n := by exact_mod_cast hn
  have h := mul_lt_mul_of_pos_left hd hnpos
  rw [centredSum_eq n hn a word,abs_mul,abs_of_pos hnpos]
  convert h using 1 <;> ring

end
end EmpiricalGeometry
