import ClusterGeometry

namespace ClusterConcentration
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord CentredBernoulli EmpiricalGeometry EndpointProcess
open scoped ENNReal

/-- A finite-word MGF tail bound, with its event implication exposed. -/
lemma finite_mgf_tail (n : ℕ) {a t d : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (ht : |t|≤1) (P : (Fin n → Bool) → Prop) [DecidablePred P]
    (hP : ∀ w, P w → d≤t*centredSum n a w) :
    (∑ w : Fin n → Bool, realWeight n a w * (if P w then (1:ℝ) else 0)) ≤
      Real.exp (-d+(n:ℝ)*t^2*a*(1-a)) := by
  classical
  have hind (w : Fin n → Bool) :
      (if P w then (1:ℝ) else 0) ≤ Real.exp (-d)*Real.exp (t*centredSum n a w) := by
    split_ifs with h
    · rw [← Real.exp_add]
      exact Real.one_le_exp_iff.mpr (by linarith [hP w h])
    · positivity
  have hsum := Finset.sum_le_sum (fun w (_ : w ∈ (Finset.univ : Finset (Fin n → Bool))) =>
    mul_le_mul_of_nonneg_left (hind w) (realWeight_nonneg n ha ha1 w))
  have heq : (∑ w : Fin n → Bool, realWeight n a w *
      (Real.exp (-d)*Real.exp (t*centredSum n a w))) =
      Real.exp (-d)*(∑ w : Fin n → Bool, realWeight n a w * Real.exp (t*centredSum n a w)) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w hw
    ring
  rw [heq] at hsum
  have hb := hsum.trans (mul_le_mul_of_nonneg_left (word_mgf_upper n ha ha1 ht) (Real.exp_pos _).le)
  rwa [← Real.exp_add] at hb

def upperTail (n : ℕ) (a b : ℝ) : ℝ := by
  classical
  exact ∑ w : Fin n → Bool, realWeight n a w * (if b≤empiricalMean n w then 1 else 0)

def lowerTail (n : ℕ) (a b : ℝ) : ℝ := by
  classical
  exact ∑ w : Fin n → Bool, realWeight n a w * (if empiricalMean n w≤b then 1 else 0)

/-- The upper error exponent is linear in the threshold, not its square. -/
theorem upper_tail_bound (n : ℕ) (hn : 0<n) {a b : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (hab : a≤(4/5)*b) :
    upperTail n a b ≤ Real.exp (-((n:ℝ)*b/100)) := by
  classical
  have hn0 : (0:ℝ)≤n := Nat.cast_nonneg n
  have h := finite_mgf_tail n ha ha1 (by norm_num [abs_le] : |(1/10:ℝ)|≤1)
    (fun w => b≤empiricalMean n w) (d := (n:ℝ)*(b-a)/10) (by
      intro w hw
      rw [centredSum_eq n hn a w]
      have h := mul_le_mul_of_nonneg_left hw hn0
      nlinarith)
  apply h.trans
  apply Real.exp_le_exp.mpr
  have hb : 0≤b := by linarith
  have h1 := mul_nonneg hn0 (show 0≤(4/5)*b-a by linarith)
  have h2 := mul_nonneg hn0 (sq_nonneg a)
  have h3 := mul_nonneg hn0 hb
  nlinarith

/-- A lower-tail error after the positive empirical floor has decayed is
exponentially small in n times the true parameter. -/
theorem lower_tail_bound (n : ℕ) (hn : 0<n) {a b : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (hba : b≤(4/5)*a) :
    lowerTail n a b ≤ Real.exp (-((n:ℝ)*a/100)) := by
  classical
  have hn0 : (0:ℝ)≤n := Nat.cast_nonneg n
  have h := finite_mgf_tail n ha ha1 (by norm_num [abs_le] : |(-1/10:ℝ)|≤1)
    (fun w => empiricalMean n w≤b) (d := (n:ℝ)*(a-b)/10) (by
      intro w hw
      rw [centredSum_eq n hn a w]
      have h := mul_le_mul_of_nonneg_left hw hn0
      nlinarith)
  apply h.trans
  apply Real.exp_le_exp.mpr
  have h1 := mul_nonneg hn0 (show 0≤(4/5)*a-b by linarith)
  have h2 := mul_nonneg hn0 (sq_nonneg a)
  nlinarith

lemma word_indicator_ofReal (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (P : (Fin n → Bool) → Prop) [DecidablePred P] :
    (∑ w : Fin n → Bool, weight n a w * (if P w then (1:ℝ≥0∞) else 0)) =
      ENNReal.ofReal (∑ w : Fin n → Bool, realWeight n a w * (if P w then (1:ℝ) else 0)) := by
  classical
  rw [ENNReal.ofReal_sum_of_nonneg (by
    intro w hw
    apply mul_nonneg (realWeight_nonneg n ha ha1 w)
    split_ifs <;> norm_num)]
  apply Finset.sum_congr rfl
  intro w hw
  split_ifs <;> simp [weight_eq_ofReal]

/-- The tail bound is transported to the actual infinite uniform innovations. -/
theorem actual_upper_tail_bound (n : ℕ) (hn : 0<n) {a b : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (hab : a≤(4/5)*b) :
    (∫⁻ u, (if b≤empiricalMean n (observedWord n a u) then (1:ℝ≥0∞) else 0) ∂innovationLaw) ≤
      ENNReal.ofReal (Real.exp (-((n:ℝ)*b/100))) := by
  classical
  rw [lintegral_prefix_function n ha ha1 (fun w => if b≤empiricalMean n w then (1:ℝ≥0∞) else 0),word_indicator_ofReal n ha ha1]
  exact ENNReal.ofReal_le_ofReal (upper_tail_bound n hn ha ha1 hab)

theorem actual_lower_tail_bound (n : ℕ) (hn : 0<n) {a b : ℝ}
    (ha : 0≤a) (ha1 : a≤1) (hba : b≤(4/5)*a) :
    (∫⁻ u, (if empiricalMean n (observedWord n a u)≤b then (1:ℝ≥0∞) else 0) ∂innovationLaw) ≤
      ENNReal.ofReal (Real.exp (-((n:ℝ)*a/100))) := by
  classical
  rw [lintegral_prefix_function n ha ha1 (fun w => if empiricalMean n w≤b then (1:ℝ≥0∞) else 0),word_indicator_ofReal n ha ha1]
  exact ENNReal.ofReal_le_ofReal (lower_tail_bound n hn ha ha1 hba)

/-- An actual finite count, on the same experiment and positive report clock. -/
def finiteFailures {Z : Type*} (e : ℝ) (r : ReportFamily Z) (N : ℕ)
    (w : (ℝ × Z) × Innovations) : ℝ≥0∞ :=
  ∑ t ∈ Finset.range N, stageFailure e r (t+1) w

theorem actual_finite_count_eq {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) (N : ℕ) :
    (∫⁻ w, finiteFailures e r N w ∂experimentLaw μ ν) =
      ∑ t ∈ Finset.range N, BayesBridge.productRisk (t+1) μ ν e (r (t+1)) := by
  unfold finiteFailures
  rw [lintegral_finset_sum _ (fun t ht => stageFailure_measurable e r hr (t+1))]
  apply Finset.sum_congr rfl
  intro t ht
  exact expected_stage_eq μ ν hs e r hr (t+1)

#print axioms finite_mgf_tail
#print axioms upper_tail_bound
#print axioms lower_tail_bound
#print axioms actual_upper_tail_bound
#print axioms actual_lower_tail_bound
#print axioms actual_finite_count_eq
end
end ClusterConcentration
