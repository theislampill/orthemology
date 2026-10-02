import UninformativeAuditControl
noncomputable section
open MeasureTheory ProbabilityTheory Finset Filter
open scoped BigOperators
namespace Orthemology.Tranche3.ReceiptAudit
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding
open FiniteAuditRepair

/-- The entire action laws coincide, including with arbitrary common private seed. -/
theorem identical_action_laws {R : Type*} [MeasurableSpace R]
    (ρ : Measure R) (π : R → History Bool Bool → Bool) :
    actionLaw π ρ (uninformativeKernel false) (uninformative_nonneg false) (uninformative_normalized false) false =
    actionLaw π ρ (uninformativeKernel true) (uninformative_nonneg true) (uninformative_normalized true) false := rfl

/-- The public menu is unrestricted, so licensing is not the obstruction. -/
theorem no_shared_measurable_policy {R : Type*} [MeasurableSpace R]
    (ρ : Measure R) [IsProbabilityMeasure ρ] :
    ¬ ∃ π : R → History Bool Bool → Bool,
      Measurable (fun z : R × History Bool Bool => π z.1 z.2) ∧
      ∀ θ ∈ (Finset.univ : Finset Bool),
        ∀ᵐ x ∂actionLaw π ρ (uninformativeKernel θ) (uninformative_nonneg θ) (uninformative_normalized θ) false,
          ∀ᶠ n in atTop, x n ∈ literalGood θ := by
  rintro ⟨π,hπ,he⟩
  apply uninformative_no_shared_policy ρ
  refine ⟨π,hπ,?_,he⟩
  intro r h _ _
  exact Finset.mem_univ _

/-- Each declared target is nonempty and individually satisfied by its matching report. -/
theorem individual_targets_feasible (θ : Bool) : θ ∈ literalGood θ := by
  simp [literalGood_exact]

/-- With a common target, uninformative observations alone cause no obstruction. -/
theorem common_target_winning :
    RecursiveWinning uninformativeKernel (fun _ : Bool => ({false} : Finset Bool)) publicMenu Finset.univ := by
  apply RecursiveWinning.intro Finset.univ (by simp) (fun _ => [false])
  · intro θ hθ; simp
  · intro θ hθ a ha; exact Finset.mem_univ a
  · intro θ hθ a ha y hy hn
    exact (hn (uninformative_support_stays Finset.univ a y)).elim
  · intro θ hθ
    right
    constructor
    · simp
    · intro η hη heq
      simp
end Orthemology.Tranche3.ReceiptAudit
set_option pp.universes true
set_option pp.explicit true
#print Orthemology.Tranche3.FiniteAuditRepair.uninformativeKernel
#print Orthemology.Tranche3.FiniteAuditRepair.literalGood
#print Orthemology.Tranche3.FiniteAuditRepair.publicMenu
#check Orthemology.Tranche3.FiniteAuditRepair.uninformative_not_winning
#check Orthemology.Tranche3.FiniteAuditRepair.uninformative_no_shared_policy
#print axioms Orthemology.Tranche3.FiniteAuditRepair.uninformative_support_stays
#print axioms Orthemology.Tranche3.FiniteAuditRepair.uninformative_not_winning
#print axioms Orthemology.Tranche3.FiniteAuditRepair.uninformative_no_shared_policy
#check Orthemology.Tranche3.ReceiptAudit.identical_action_laws
#check Orthemology.Tranche3.ReceiptAudit.no_shared_measurable_policy
#check Orthemology.Tranche3.ReceiptAudit.common_target_winning
#print axioms Orthemology.Tranche3.ReceiptAudit.identical_action_laws
#print axioms Orthemology.Tranche3.ReceiptAudit.no_shared_measurable_policy
#print axioms Orthemology.Tranche3.ReceiptAudit.individual_targets_feasible
#print axioms Orthemology.Tranche3.ReceiptAudit.common_target_winning
