import ClusterWidthBoundary
import ConcreteSparsePrior

/-! A new actual-process negative theorem for critical-width paired clusters.
The positive classification and continuous-strip instantiation retain their
separately stated ordinary scope. -/
namespace CriticalPairProcess
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord BayesBridge EndpointProcess
open SparsePriorBayes ClusterWidthBoundary
open scoped ENNReal

def pairLaw (a e : ℝ) : Measure ℝ :=
  ENNReal.ofReal (1/2:ℝ) • Measure.dirac ((1-e)*a) +
    ENNReal.ofReal (1/2:ℝ) • Measure.dirac ((1+e)*a)

instance pairLaw_probability (a e : ℝ) : IsProbabilityMeasure (pairLaw a e) := by
  constructor
  norm_num [pairLaw,Measure.add_apply,Measure.smul_apply,measure_univ]
  rw [← ENNReal.ofReal_add (by norm_num) (by norm_num)]
  norm_num

def pairPrior (a : ℕ → ℝ) (e : ℝ) : Measure ℝ :=
  Measure.sum (fun i => ENNReal.ofReal (priorWeight a 1 i) • pairLaw (a i) e)

instance pairPrior_probability (a : ℕ → ℝ) (e : ℝ)
    (hp : ∀ i, 0<a i) (hs : ∀ i, a (i+1)≤a i/2) : IsProbabilityMeasure (pairPrior a e) := by
  constructor
  unfold pairPrior
  rw [Measure.sum_apply _ MeasurableSet.univ]
  simp only [Measure.smul_apply,smul_eq_mul,measure_univ,mul_one]
  have hw : Summable (fun i => priorWeight a 1 i) :=
    (power_weights_summable hp hs (by norm_num : (0:ℝ)<1)).div_const (normalizer a 1)
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun i => (priorWeight_pos (by norm_num) hp hs i).le) hw,
    priorWeight_sum_one (by norm_num) hp hs]
  norm_num

lemma pair_parameters_unit {a e : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) :
    (0≤(1-e)*a ∧ (1-e)*a≤1) ∧ (0≤(1+e)*a ∧ (1+e)*a≤1) := by
  have hmul := mul_le_mul he4 ha2 ha.le (by norm_num : (0:ℝ)≤1/4)
  have hpa : 0≤e*a := mul_nonneg he.le ha.le
  constructor <;> constructor <;> nlinarith

lemma pairPrior_supported (a : ℕ → ℝ) (e : ℝ)
    (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (he : 0<e) (he4 : e≤1/4) : ∀ᵐ x ∂pairPrior a e, 0≤x ∧ x≤1 := by
  rw [ae_iff]
  have hset : {x : ℝ | ¬(0≤x ∧ x≤1)}=(Icc 0 1)ᶜ := by ext x;simp
  rw [hset,pairPrior,Measure.sum_apply _ measurableSet_Icc.compl]
  apply ENNReal.tsum_eq_zero.mpr
  intro i
  obtain ⟨hl,hu⟩ := pair_parameters_unit (hp i) (hh i) he he4
  simp [Measure.smul_apply,pairLaw,Measure.add_apply,hl,hu]

lemma pairLaw_lintegral (a e : ℝ) (f : ℝ → ℝ≥0∞) :
    (∫⁻ x, f x ∂pairLaw a e) = ENNReal.ofReal (1/2:ℝ)*f ((1-e)*a)+
      ENNReal.ofReal (1/2:ℝ)*f ((1+e)*a) := by
  simp [pairLaw,lintegral_add_measure,lintegral_smul_measure,lintegral_dirac]

lemma pairPrior_lintegral (a : ℕ → ℝ) (e : ℝ) (f : ℝ → ℝ≥0∞) :
    (∫⁻ x, f x ∂pairPrior a e) =
      ∑' i, ENNReal.ofReal (priorWeight a 1 i)*(∫⁻ x, f x ∂pairLaw (a i) e) := by
  unfold pairPrior
  rw [lintegral_sum_measure]
  apply tsum_congr
  intro i
  rw [lintegral_smul_measure,smul_eq_mul]

/-- Every zero-word report misses one critical-width member. -/
theorem zero_pair_lower {a e q : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) (n : ℕ) :
    ENNReal.ofReal (1/2:ℝ)*ENNReal.ofReal ((1-(1+e)*a)^n) ≤
      weightedFailure (pairLaw a e) (fun x => ENNReal.ofReal ((1-x)^n)) e q := by
  classical
  unfold weightedFailure
  rw [pairLaw_lintegral]
  by_cases hl : Accepted ((1-e)*a) e q
  · have hu : ¬Accepted ((1+e)*a) e q := by
      intro hu
      exact critical_pair_incompatible ha he he4 (le_refl e) ⟨hl,hu⟩
    simp [failureIndicator,hl,hu]
  · have hunit := pair_parameters_unit ha ha2 he he4
    have hbase : 1-(1+e)*a≤1-(1-e)*a := by nlinarith [mul_nonneg he.le ha.le]
    have hpow := pow_le_pow_left₀ (show 0≤1-(1+e)*a by linarith [hunit.2.2]) hbase n
    have hm := mul_le_mul_left' (ENNReal.ofReal_le_ofReal hpow) (ENNReal.ofReal (1/2:ℝ))
    simp only [failureIndicator,hl,↓reduceIte,mul_one]
    exact hm.trans (le_add_right le_rfl)

/-- The bound sums over the actual fixed parameter mixture, not freshly
resampled receipt parameters. -/
theorem zero_prior_lower (a : ℕ → ℝ) (e q : ℝ)
    (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (he : 0<e) (he4 : e≤1/4) (n : ℕ) :
    (∑' i, ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
      ENNReal.ofReal ((1-(1+e)*a i)^n)) ≤
      weightedFailure (pairPrior a e) (fun x => ENNReal.ofReal ((1-x)^n)) e q := by
  unfold weightedFailure
  rw [pairPrior_lintegral]
  apply ENNReal.tsum_le_tsum
  intro i
  rw [mul_assoc]
  exact mul_le_mul_left' (zero_pair_lower (hp i) (hh i) he he4 n) _


lemma positive_geometric_sum {u : ℝ} (hu : 0<u) (hu1 : u<1) :
    (∑' n : ℕ, ENNReal.ofReal ((1-u)^(n+1)))=ENNReal.ofReal ((1-u)/u) := by
  have hnorm : ‖1-u‖<1 := by rw [Real.norm_eq_abs,abs_of_pos (by linarith : 0<1-u)];linarith
  have hs : Summable (fun n : ℕ => (1-u)^(n+1)) := by
    simp_rw [pow_succ]
    exact (summable_geometric_of_norm_lt_one hnorm).mul_right (1-u)
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun n => pow_nonneg (by linarith) _) hs]
  congr 1
  simp_rw [pow_succ]
  rw [tsum_mul_right,tsum_geometric_of_norm_lt_one hnorm]
  field_simp

lemma pair_cost_lower {a e Z : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) (hZ : 0<Z) :
    3/(20*Z) ≤ (a/Z)*(1/2)*((1-(1+e)*a)/((1+e)*a)) := by
  have h1e : 0<1+e := by linarith
  have hprod := mul_le_mul he4 ha2 ha.le (by norm_num : (0:ℝ)≤1/4)
  have heq : (a/Z)*(1/2)*((1-(1+e)*a)/((1+e)*a)) =
      (1-(1+e)*a)/(2*(1+e)*Z) := by
    field_simp
    ring
  rw [heq]
  apply (div_le_div_iff₀ (by positivity : 0<20*Z) (by positivity : 0<2*(1+e)*Z)).mpr
  have hcore : (3:ℝ)*2*(1+e)≤20*(1-(1+e)*a) := by nlinarith
  have hmul := mul_le_mul_of_nonneg_right hcore hZ.le
  nlinarith

/-- An evaluated lifetime lower cost for EACH component, before summing the
infinitely many components. No parameter-dependent policy is substituted. -/
theorem component_lifetime_lower (a : ℕ → ℝ) (e : ℝ)
    (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (he : 0<e) (he4 : e≤1/4) (i : ℕ) :
    ENNReal.ofReal (3/(20*normalizer a 1)) ≤
      ∑' n : ℕ, ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
        ENNReal.ofReal ((1-(1+e)*a i)^(n+1)) := by
  have hu : 0<(1+e)*a i := mul_pos (by linarith) (hp i)
  have hprod := mul_le_mul he4 (hh i) (hp i).le (by norm_num : (0:ℝ)≤1/4)
  have hu1 : (1+e)*a i<1 := by nlinarith [hh i]
  have hZ := normalizer_pos (a := a) (by norm_num : (0:ℝ)<1) hp hs
  rw [ENNReal.tsum_mul_left,positive_geometric_sum hu hu1]
  have hw : priorWeight a 1 i=a i/normalizer a 1 := by simp [priorWeight]
  rw [hw,← ENNReal.ofReal_mul (div_nonneg (hp i).le hZ.le),← ENNReal.ofReal_mul (mul_nonneg (div_nonneg (hp i).le hZ.le) (by norm_num))]
  exact ENNReal.ofReal_le_ofReal (pair_cost_lower (hp i) (hh i) he he4 hZ)

/-- Universal prefix lower bound after adjoining any fixed independent seed. -/
theorem prefix_risk_lower {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (e : ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (he : 0<e) (he4 : e≤1/4) (ν : Measure Z) [IsProbabilityMeasure ν]
    (n : ℕ) (r : (Fin n → Bool) → Z → ℝ) :
    (∑' i, ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
      ENNReal.ofReal ((1-(1+e)*a i)^n)) ≤ risk n (pairPrior a e) ν e r := by
  let c : ℝ≥0∞ := ∑' i, ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
    ENNReal.ofReal ((1-(1+e)*a i)^n)
  have hpoint (z : Z) := zero_prior_lower a e (r (fun _ => false) z) hp hh he he4 n
  have h : c≤∫⁻ z, weightedFailure (pairPrior a e)
      (fun x => ENNReal.ofReal ((1-x)^n)) e (r (fun _ => false) z) ∂ν := by
    calc
      c=∫⁻ _z : Z, c ∂ν := by simp
      _≤_ := lintegral_mono hpoint
  have hw := EndpointAtoms.fixed_word_le_risk n (pairPrior a e) ν e r (fun _ => false)
  simp only [weight_zero] at hw
  exact h.trans hw

/-- Every measurable full-history real-report policy has infinite actual
positive-time expected count under the critical paired-cluster prior. -/
theorem every_policy_infinite {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (e : ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (he : 0<e) (he4 : e≤1/4)
    (ν : Measure Z) [IsProbabilityMeasure ν] (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ w, totalFailures e r w ∂experimentLaw (pairPrior a e) ν)=⊤ := by
  letI : IsProbabilityMeasure (pairPrior a e) := pairPrior_probability a e hp hs
  rw [actual_expectation_eq_risk_series (pairPrior a e) ν
    (pairPrior_supported a e hp hh he he4) e r hr]
  have hlower : (∑' n : ℕ, ∑' i, ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
      ENNReal.ofReal ((1-(1+e)*a i)^(n+1))) ≤
      ∑' n : ℕ, productRisk (n+1) (pairPrior a e) ν e (r (n+1)) := by
    apply ENNReal.tsum_le_tsum
    intro n
    rw [productRisk_eq_bayesRisk _ _ _ _ _ (hr (n+1)),bayesRisk_eq_risk _ _ _ _ _ (hr (n+1))]
    exact prefix_risk_lower a e hp hh he he4 ν (n+1) (r (n+1))
  rw [ENNReal.tsum_comm] at hlower
  have hinf : (⊤ : ℝ≥0∞) ≤ ∑' i, ∑' n : ℕ,
      ENNReal.ofReal (priorWeight a 1 i)*ENNReal.ofReal (1/2:ℝ)*
        ENNReal.ofReal ((1-(1+e)*a i)^(n+1)) := by
    have hZ := normalizer_pos (a := a) (by norm_num : (0:ℝ)<1) hp hs
    have hc : ENNReal.ofReal (3/(20*normalizer a 1))≠0 := ne_of_gt (ENNReal.ofReal_pos.mpr (by positivity))
    rw [← ENNReal.tsum_const_eq_top_of_ne_zero (α := ℕ) hc]
    exact ENNReal.tsum_le_tsum (component_lifetime_lower a e hp hh hs he he4)
  exact top_le_iff.mp (hinf.trans hlower)

#print axioms positive_geometric_sum
#print axioms pair_cost_lower
#print axioms component_lifetime_lower
#print axioms prefix_risk_lower
#print axioms every_policy_infinite
#print axioms pairPrior_probability
#print axioms pairPrior_supported
#print axioms zero_pair_lower
#print axioms zero_prior_lower
end
end CriticalPairProcess
