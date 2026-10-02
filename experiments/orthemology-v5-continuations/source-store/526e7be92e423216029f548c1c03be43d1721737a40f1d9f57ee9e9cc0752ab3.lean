import EndpointProcess
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge
open EmpiricalGeometry EmpiricalChernoff EmpiricalEndpoints EndpointProcess PriorSufficiency
open scoped ENNReal
noncomputable section

/-- Threshold equality at a zero-probability innovation is not a pathwise
endpoint-zero statement. Its probability is exactly zero. -/
example : bit 0 0 = true := by norm_num [bit]
example : uniformLaw (bitEvent 0 true) = 0 := by
  rw [uniform_bitEvent_mass (by norm_num) (by norm_num)]
  norm_num [ENNReal.ofReal_div_of_pos]

/-- Conditional iid holds at separated, nonconsecutive receipt indices. -/
example : innovationLaw {u | ∀ i ∈ ({1,7} : Finset ℕ), bit (1/4) (u i)=true} = 1/16 := by
  rw [finite_receipt_mass (by norm_num) (by norm_num)]
  norm_num
  apply (ENNReal.toReal_eq_toReal_iff' (ENNReal.pow_ne_top ENNReal.ofReal_ne_top) (by simp)).mp
  norm_num

example : wordEvent 2 (1/4) (fun _ => true) ≠ wordEvent 2 (1/4) (fun _ => false) := by
  intro h
  have hm := congrArg (fun s => innovationLaw s) h
  dsimp only at hm
  rw [wordEvent_mass 2 (by norm_num) (by norm_num),wordEvent_mass 2 (by norm_num) (by norm_num)] at hm
  norm_num [ENNReal.ofReal_div_of_pos] at hm
  have hh := congrArg ENNReal.toReal hm
  norm_num at hh

theorem actual_empirical_left_endpoint {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω
      ∂experimentLaw (Measure.dirac 0) ν) = 0 := by
  rw [actual_expectation_eq_risk_series _ ν (by simp) e _ (fun n w => measurable_const)]
  simp_rw [empirical_productRisk_eq]
  simp [error_at_zero]

theorem actual_empirical_right_endpoint {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω
      ∂experimentLaw (Measure.dirac 1) ν) = 0 := by
  rw [actual_expectation_eq_risk_series _ ν (by simp) e _ (fun n w => measurable_const)]
  simp_rw [empirical_productRisk_eq]
  have hz : ∀ n : ℕ, error (n+1) 1 e=0 := fun n => error_at_one _ (by omega) e
  simp [hz]

/-- Full ordered words remain available to policies. Equal counts do not force
equal report values. -/
example : (fun w : Fin 2 → Bool => if w 0 then (3/4:ℝ) else 1/2) ![true,false] ≠
    (fun w : Fin 2 → Bool => if w 0 then (3/4:ℝ) else 1/2) ![false,true] := by norm_num

/-- Integrating conditional word masses over a one-time latent draw differs
from independently remixing the parameter at every receipt. -/
example : (∫⁻ a, weight 2 a (fun _ => true)
    ∂((1/2:ℝ≥0∞) • Measure.dirac (1/4:ℝ) + (1/2:ℝ≥0∞) • Measure.dirac (3/4:ℝ))) = 5/16 := by
  rw [lintegral_add_measure]
  norm_num [ENNReal.ofReal_div_of_pos]
  have h0 : (2:ℝ≥0∞)⁻¹ * 16⁻¹ ≠ ⊤ := ENNReal.mul_ne_top (by simp) (by simp)
  have h1 : (2:ℝ≥0∞)⁻¹ * (9/16) ≠ ⊤ :=
    ENNReal.mul_ne_top (by simp) (ENNReal.mul_ne_top (by norm_num) (by simp))
  have h2 : (5/16:ℝ≥0∞) ≠ ⊤ := ENNReal.mul_ne_top (by norm_num) (by simp)
  apply (ENNReal.toReal_eq_toReal_iff' (ENNReal.add_ne_top.mpr ⟨h0,h1⟩) h2).mp
  rw [ENNReal.toReal_add h0 h1]
  norm_num
example : (5/16:ℝ≥0∞) ≠ (1/2)*(1/2) := by
  intro h
  have hh := congrArg ENNReal.toReal h
  norm_num at hh

/-- The initial report is not included in the positive-time theorem. -/
example : error 0 1 (1/4)=1 := by
  norm_num [error,weight,empiricalReport,empiricalMean,failureIndicator,Accepted,D0,D1]

#print axioms actual_empirical_left_endpoint
#print axioms actual_empirical_right_endpoint
#synth IsProbabilityMeasure (experimentLaw (Measure.dirac (1/2:ℝ)) (Measure.dirac ()))
