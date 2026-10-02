import FiniteAuditRepair
noncomputable section
namespace IndependentFiniteAuditControls
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche3
open AuditControlBridge FiniteAuditRepair CanonicalMicro
open MeasureTheory
open scoped ENNReal

def lagPolicy (h : History Bool Bool) : Bool := (h.headD (false,false)).2

theorem action_zero_precedes_first_bit (ω : ℕ → Bool) : auditActions lagPolicy ω 0=false := rfl

theorem action_one_uses_acquired_bit (ω : ℕ → Bool) : auditActions lagPolicy ω 1=ω 0 := rfl

theorem generic_past_only (ω ω' : ℕ → Bool) (n : ℕ) (h : ∀ k<n,ω k=ω' k) :
    auditActions lagPolicy ω n=auditActions lagPolicy ω' n := auditActions_uses_only_past _ _ _ _ h

theorem no_current_bit_access_at_initial_action :
    auditActions lagPolicy (fun _ => false) 0=auditActions lagPolicy (fun _ => true) 0 := rfl

theorem actual_source_action_law_for_concrete_policy :
    (auditSourceLaw (1/4) (by norm_num) (by norm_num)).map (auditActions lagPolicy) =
      actionLaw (ignoreSeed lagPolicy) (Measure.dirac ())
        (actionBlindKernel (1/4)) (actionBlindKernel_nonneg (1/4) (by norm_num) (by norm_num))
        (actionBlindKernel_normalized (1/4)) false :=
  auditActions_law_eq_canonical _ _ _ _ _ _

theorem report_labels_are_literal_scores :
    literalGood false={false} ∧ literalGood true={true} := ⟨literalGood_exact _,literalGood_exact _⟩

theorem static_obstruction_covers_all_real_reports :
    ¬∃ q : ℝ,LiteralRepairGood (1/4) (1/4) q ∧ LiteralRepairGood (3/4) (1/4) q := no_static_common_literal_repair

theorem fixed_expected_score_gains (θ : Bool) :
    excessZero (weight θ) (1/4) (report θ)=-(3/256) ∧
    excessOne (weight θ) (1/4) (report θ)=-(3/256) := (matching_report_losses θ).2.2

theorem every_observation_retains_both_models (a y : Bool) :
    supportUpdate kernels Finset.univ a y=Finset.univ := support_stays _ _ _

theorem all_reports_licensed (B : Finset Bool) (a : Bool) : a∈publicMenu B := Finset.mem_univ _
end IndependentFiniteAuditControls
