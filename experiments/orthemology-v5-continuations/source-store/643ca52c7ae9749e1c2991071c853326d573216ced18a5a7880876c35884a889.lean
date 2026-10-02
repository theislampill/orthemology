import EmpiricalExpectedCost
noncomputable section
namespace IndependentContinuumControls
open Orthemology.Tranche2 Orthemology.Tranche3
open MeasureTheory Filter Set
open scoped ENNReal BigOperators

theorem plugin_oracle_exact_margin (a e : ℝ) :
    excessZero a e (1/2+a*e) = -a*(1-a)*e^2 ∧
    excessOne a e (1/2+a*e) = -a*(1-a)*e^2 := by
  constructor <;> simp only [excessZero,excessOne] <;> ring

theorem no_strict_margin_at_zero (e : ℝ) : excessZero 0 e (1/2)=0 := by norm_num [excessZero]

theorem no_strict_margin_at_one (e : ℝ) : excessOne 1 e (1/2+e)=0 := by unfold excessOne; ring

theorem empirical_always_emits_rational_coherent (e : ℚ) (he0 : 0≤e) (he1 : e≤1/4)
    (n : ℕ) (w : Bits (n+1)) :
    ∃ q : ℚ, q=empiricalRepair e n w ∧ 0≤q ∧ q≤1 :=
  ⟨_,rfl,empiricalRepair_coherent e he0 he1 n w⟩

theorem first_report_is_wrong_with_probability_one (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) :
    auditSourceLaw a ha0.le ha1.le (EmpiricalFailure a e 0)=1 := by
  apply le_antisymm (by simpa using (measure_mono (Set.subset_univ (EmpiricalFailure a e 0)) (μ := auditSourceLaw a ha0.le ha1.le)))
  have h:=empirical_failure_probability_lower a ha0 ha1 e he0 he1 0
  have he : ENNReal.ofReal (1-a)+ENNReal.ofReal a=1 := by
    rw [←ENNReal.ofReal_add (by linarith : 0≤1-a) ha0.le]
    norm_num
  simpa only [Nat.zero_add,pow_one,he] using h

theorem zero_disturbance_is_always_weakly_good (a : ℝ) (n : ℕ) (w : Bits (n+1)) :
    LiteralRepairGood a 0 (empiricalRepair 0 n w) := by
  norm_num [LiteralRepairGood,empiricalRepair,excessZero,excessOne]
  ring_nf
  norm_num

theorem two_bits_centered_moments :
    centeredMoment 2 2 (1/2)=1/2 ∧ centeredMoment 2 4 (1/2)=1/2 := by
  constructor
  · rw [(centered_moments 2 (1/2)).2.1]; norm_num
  · rw [(centered_moments 2 (1/2)).2.2]; norm_num

theorem missing_cross_terms_give_wrong_fourth :
    centeredMoment 2 4 (1/2) ≠ 2*(1/2:ℝ)*(1-1/2)*(1-3*(1/2)*(1-1/2)) := by
  rw [two_bits_centered_moments.2]
  norm_num

theorem large_disturbance_can_break_coherence :
    ¬ (empiricalRepair 1 0 (true,()) ≤ 1) := by
  norm_num [empiricalRepair,empiricalWeight,rationalCount]

theorem convergent_estimate_alone_has_no_vanishing_disturbance_guarantee
    (e : ℝ) (he : 0<e) :
    0 < excessZero (1/2) e (1/2+e*(1/2+e)) := by
  rw [excessZero_expand]
  nlinarith [sq_nonneg (e*(1/2+e)),sq_pos_of_pos he]

theorem finite_upper_is_parameterwise (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) :
    (∫⁻ ω, ∑' n, (EmpiricalFailure a e n).indicator 1 ω
      ∂auditSourceLaw a ha0.le ha1.le) < ⊤ :=
  (empirical_expected_failure_upper a ha0 ha1 e he0 he1).trans_lt ENNReal.ofReal_lt_top
end IndependentContinuumControls
