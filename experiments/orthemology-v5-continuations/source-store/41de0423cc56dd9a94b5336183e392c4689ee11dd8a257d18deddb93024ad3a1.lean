import GeneralPointTransport

namespace PriorNonconvexity
noncomputable section
open MeasureTheory Set SparsePriorBayes GeneralPointTransport EndpointProcess
open CriticalPairProcess RelativeContamination ConcreteSparsePrior
open scoped ENNReal

def minusPrior (a : ℕ → ℝ) (e : ℝ) : Measure ℝ := pointPrior (scaleSupport (1-e) a)
def plusPrior (a : ℕ → ℝ) (e : ℝ) : Measure ℝ := pointPrior (scaleSupport (1+e) a)

def mixture (a : ℕ → ℝ) (e : ℝ) (theta : ℝ≥0∞) : Measure ℝ :=
  theta • minusPrior a e+(1-theta) • plusPrior a e

lemma balanced_prior_split (a : ℕ → ℝ) {e : ℝ} (he : 0<e) (he4 : e≤1/4) :
    pairPrior a e=ENNReal.ofReal (1/2:ℝ) • minusPrior a e+
      ENNReal.ofReal (1/2:ℝ) • plusPrior a e := by
  have hcm : 1-e≠0 := by linarith
  have hcp : 1+e≠0 := by linarith
  apply Measure.ext
  intro A hA
  simp only [pairPrior,minusPrior,plusPrior,pointPrior,Measure.sum_apply _ hA,
    Measure.add_apply,Measure.smul_apply,smul_eq_mul,pairLaw,
    priorWeight_scale a hcm,priorWeight_scale a hcp,scaleSupport]
  simp_rw [mul_add]
  rw [ENNReal.tsum_add]
  simp_rw [mul_left_comm (ENNReal.ofReal (priorWeight a 1 _)) (ENNReal.ofReal (1/2:ℝ))]
  rw [ENNReal.tsum_mul_left,ENNReal.tsum_mul_left]

lemma minus_probability (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {e : ℝ} (he4 : e≤1/4) : IsProbabilityMeasure (minusPrior a e) := by
  have hc : 0<1-e := by linarith
  exact pointPrior_probability _ (scale_pos a hp hc) (scale_sep a hs hc.le)

lemma plus_probability (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {e : ℝ} (he : 0<e) : IsProbabilityMeasure (plusPrior a e) := by
  have hc : 0<1+e := by linarith
  exact pointPrior_probability _ (scale_pos a hp hc) (scale_sep a hs hc.le)

lemma mixture_probability (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {e : ℝ} (he : 0<e) (he4 : e≤1/4)
    (theta : ℝ≥0∞) (ht : theta≤1) : IsProbabilityMeasure (mixture a e theta) := by
  letI := minus_probability a hp hs he4
  letI := plus_probability a hp hs he
  constructor
  simp [mixture,add_tsub_cancel_of_le ht]

/-- Both strictly positive mixture coefficients preserve the universal paired
obstruction, including policies redesigned for the unequal prior odds. -/
theorem every_policy_infinite_mixture {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (he : 0<e) (he4 : e≤1/4) (theta : ℝ≥0∞) (ht0 : 0<theta) (ht1 : theta<1)
    (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ w, totalFailures e r w ∂experimentLaw (mixture a e theta) ν)=⊤ := by
  have hbad := CriticalPairProcess.every_policy_infinite a e hp hh hs he he4 ν r hr
  rw [balanced_prior_split a he he4,count_mixture _ _ ν e r hr] at hbad
  unfold mixture
  rw [count_mixture _ _ ν e r hr]
  by_contra hfin
  let Eminus := ∫⁻ w, totalFailures e r w ∂experimentLaw (minusPrior a e) ν
  let Eplus := ∫⁻ w, totalFailures e r w ∂experimentLaw (plusPrior a e) ν
  change theta*Eminus+(1-theta)*Eplus≠⊤ at hfin
  change ENNReal.ofReal (1/2:ℝ)*Eminus+ENNReal.ofReal (1/2:ℝ)*Eplus=⊤ at hbad
  have hm : Eminus≠⊤ := by
    intro hm
    rw [hm,ENNReal.mul_top (ne_of_gt ht0),top_add] at hfin
    exact hfin rfl
  have hp' : Eplus≠⊤ := by
    intro hp'
    rw [hp',ENNReal.mul_top (ne_of_gt (tsub_pos_iff_lt.mpr ht1)),add_top] at hfin
    exact hfin rfl
  have hc : ENNReal.ofReal (1/2:ℝ)<⊤ := ENNReal.ofReal_lt_top
  have hf : ENNReal.ofReal (1/2:ℝ)*Eminus+ENNReal.ofReal (1/2:ℝ)*Eplus<⊤ :=
    ENNReal.add_lt_top.mpr ⟨ENNReal.mul_lt_top hc (lt_top_iff_ne_top.mpr hm),
      ENNReal.mul_lt_top hc (lt_top_iff_ne_top.mpr hp')⟩
  rw [hbad] at hf
  exact (lt_irrefl _ hf)

def FiniteBudget {Z : Type*} [MeasurableSpace Z] (ν : Measure Z) (e : ℝ) (μ : Measure ℝ) : Prop :=
  ∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
    (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
    (∫⁻ w, totalFailures e r w ∂experimentLaw μ ν)<⊤

/-- Two successful priors, normalized at their own scales, have no successful
proper mixture in the same reporting experiment. -/
theorem finite_endpoints_infinite_interior {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (he : 0<e) (he4 : e≤1/4) (hhplus : ∀ i, (1+e)*a i≤1/2)
    (hS : Summable (fun i : ℕ => (a (i+1)/a i)*Real.log (a i/a (i+1)))) :
    FiniteBudget ν e (minusPrior a e) ∧ FiniteBudget ν e (plusPrior a e) ∧
    (∀ theta : ℝ≥0∞, 0<theta → theta<1 →
      ∀ r : ReportFamily Z, (∀ n w, Measurable (r n w)) →
        (∫⁻ w, totalFailures e r w ∂experimentLaw (mixture a e theta) ν)=⊤) := by
  have hcm : 0<1-e := by linarith
  have hcp : 0<1+e := by linarith
  have hhm : ∀ i, scaleSupport (1-e) a i≤1/2 := by
    intro i
    dsimp [scaleSupport]
    have h := mul_nonneg he.le (hp i).le
    nlinarith [hh i]
  have hSm : Summable (fun i : ℕ =>
      (scaleSupport (1-e) a (i+1)/scaleSupport (1-e) a i)*
        Real.log (scaleSupport (1-e) a i/scaleSupport (1-e) a (i+1))) := by
    simpa only [spacing_scale a (ne_of_gt hcm)] using hS
  have hSp : Summable (fun i : ℕ =>
      (scaleSupport (1+e) a (i+1)/scaleSupport (1+e) a i)*
        Real.log (scaleSupport (1+e) a i/scaleSupport (1+e) a (i+1))) := by
    simpa only [spacing_scale a (ne_of_gt hcp)] using hS
  refine ⟨?_,?_,?_⟩
  · exact exists_finite_pointPrior _ (scale_pos a hp hcm) hhm (scale_sep a hs hcm.le) ν e he he4 hSm
  · exact exists_finite_pointPrior _ (scale_pos a hp hcp) hhplus (scale_sep a hs hcp.le) ν e he he4 hSp
  · intro theta ht0 ht1 r hr
    exact every_policy_infinite_mixture a hp hh hs ν e he he4 theta ht0 ht1 r hr

/-- A concrete nonvacuous support, uniformly small enough for both scaled sides. -/
def smallQuadratic : ℕ → ℝ := scaleSupport (1/2) quadraticSupport

lemma smallQuadratic_pos : ∀ i, 0<smallQuadratic i :=
  scale_pos quadraticSupport quadraticSupport_pos (by norm_num)

lemma smallQuadratic_quarter (i : ℕ) : smallQuadratic i≤1/4 := by
  have h := quadraticSupport_half i
  dsimp [smallQuadratic,scaleSupport]
  linarith

lemma smallQuadratic_sep : ∀ i, smallQuadratic (i+1)≤smallQuadratic i/2 :=
  scale_sep quadraticSupport quadraticSupport_sep (by norm_num)

lemma smallQuadratic_spacing : Summable (fun i : ℕ =>
    (smallQuadratic (i+1)/smallQuadratic i)*Real.log (smallQuadratic i/smallQuadratic (i+1))) := by
  have hS : Summable (fun i : ℕ => (quadraticSupport (i+1)/quadraticSupport i)*
      Real.log (quadraticSupport i/quadraticSupport (i+1))) := by simpa using quadraticSupport_spacing_summable
  simpa only [smallQuadratic,spacing_scale quadraticSupport (by norm_num : (1/2:ℝ)≠0)] using hS

/-- Concrete same-interface nonconvexity for every fixed independent seed law. -/
theorem concrete_nonconvexity {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4) :
    FiniteBudget ν e (minusPrior smallQuadratic e) ∧ FiniteBudget ν e (plusPrior smallQuadratic e) ∧
    (∀ theta : ℝ≥0∞, 0<theta → theta<1 →
      ∀ r : ReportFamily Z, (∀ n w, Measurable (r n w)) →
        (∫⁻ w, totalFailures e r w ∂experimentLaw (mixture smallQuadratic e theta) ν)=⊤) := by
  apply finite_endpoints_infinite_interior smallQuadratic smallQuadratic_pos
    (fun i => (smallQuadratic_quarter i).trans (by norm_num)) smallQuadratic_sep ν e he he4
  · intro i
    have hprod := mul_le_mul he4 (smallQuadratic_quarter i) (smallQuadratic_pos i).le (by norm_num : (0:ℝ)≤1/4)
    nlinarith [smallQuadratic_quarter i]
  · exact smallQuadratic_spacing

#print axioms balanced_prior_split
#print axioms mixture_probability
#print axioms every_policy_infinite_mixture
#print axioms finite_endpoints_infinite_interior
#print axioms smallQuadratic_spacing
#print axioms concrete_nonconvexity
end
end PriorNonconvexity
