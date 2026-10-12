import ClosedScalarInstances
import OriginalWNoninhabitation

/- Consequence of the inherited closed-instance construction and new exact
   nonderivability theorem. No source rule or proof-search algorithm is added. -/
namespace ClosedInstanceBoundary
open P01AC P01D
open P01AC.ExtensionalRepair (HasE)
open P01AC.EffectiveCompleteness (N)
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3 Leaf A End)

def AllClosedInstances : Prop :=
  ∀ (n : Poly), HasE [] n N →
    HasE [] (.app c3 n)
      (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n)

theorem all_closed_instances : AllClosedInstances :=
  fun _ hn => ClosedScalarInstances.closed_scalar_instance_exact hn

theorem closed_instance_rule_not_admissible :
    ¬ (AllClosedInstances → ∃ p : Poly, HasE [] p (W FullPER.Application.originalQ)) := by
  intro rule
  obtain ⟨p, hp⟩ := rule all_closed_instances
  exact HomogeneousOriginalW.original_W_uninhabited p hp

#print axioms all_closed_instances
#print axioms closed_instance_rule_not_admissible
end ClosedInstanceBoundary
