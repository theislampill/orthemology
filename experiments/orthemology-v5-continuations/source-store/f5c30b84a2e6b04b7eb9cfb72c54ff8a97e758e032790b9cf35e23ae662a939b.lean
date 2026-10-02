import EmpiricalEndpointLaw
noncomputable section
namespace IndependentEndpointLawControls
open Orthemology.Tranche2 Orthemology.Tranche3 Orthemology.Tranche3.EndpointBridge
open MeasureTheory Filter Set
open scoped ENNReal

theorem endpoint_report_has_no_strict_zero_margin (e q : ℝ) (h : LiteralRepairGood 0 e q) :
    excessZero 0 e q=0 := by
  rw [(zero_weight_unique e q).mp h]
  norm_num [excessZero]

theorem boundary_report_fails_every_positive_weight (a e : ℝ)
    (ha : 0<a) (he0 : 0<e) (he1 : e≤1/4) : ¬ LiteralRepairGood a e (1/2) := by
  intro h
  have := (positive_weight_punctured_cell a e (1/2) ha he0 he1 h).1
  linarith

theorem wrong_raw_path_is_not_correct_at_zero :
    ¬ LiteralRepairGood 0 (1/4) (empiricalRepair (1/4) 0 (true,())) := by
  rw [zero_weight_unique]
  norm_num [empiricalRepair,empiricalWeight,rationalCount]

theorem actual_endpoint_false_is_constant :
    ∀ᵐ ω ∂auditSourceLaw 0 (by norm_num) (by norm_num), ∀ n, ω n=false := by
  exact auditSource_endpoint_constant false

theorem actual_endpoint_true_is_constant :
    ∀ᵐ ω ∂auditSourceLaw 1 (by norm_num) (by norm_num), ∀ n, ω n=true := by
  exact auditSource_endpoint_constant true

theorem same_always_emitting_policy_has_endpoint_zero_cost (b : Bool) :
    (∫⁻ ω, ∑' n, (EmpiricalFailure (endpointWeight b) (1/4) n).indicator 1 ω
      ∂auditSourceLaw (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b))=0 :=
  endpoint_empirical_expected_failure_zero b (1/4) (by norm_num) (by norm_num)
end IndependentEndpointLawControls
