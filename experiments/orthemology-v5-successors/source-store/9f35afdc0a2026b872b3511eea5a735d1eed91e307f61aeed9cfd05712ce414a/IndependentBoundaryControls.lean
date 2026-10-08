/- Independent discriminators for the exact normalization boundary. -/
import PolymorphicNormalizationBoundary
import AuditSupport
namespace IndependentBoundaryControls
open OrthemologyV2 OrthemologyV3 P01D P01Source P01NormalizationBoundary

/-- Evaluation equality does not identify application syntax with an opaque atom. -/
theorem matching_is_not_opaque : p ≠ Poly.atom t := by
  intro h
  cases h

theorem matching_and_opaque_evaluate (η : Env) : eval p η = eval (.atom t) η := rfl

/-- The wrapper introduces precisely the normality obstruction of its argument. -/
theorem wrapper_normal_iff (q : Term) : Normal (wrapper q) ↔ Normal q := by
  constructor
  · exact wrapper_normal
  · intro h u hs
    obtain ⟨q',hq,he⟩ := wrapper_step hs
    exact h q' hq

/-- The older discarded expansion does have a normal reduct: mere non-SN
is not the new conclusion. This uses the same full contextual Step. -/
theorem discarded_identity_has_normal_reduct :
    ∃ n, Red (discard .i omega) n ∧ Normal n := by
  refine ⟨.i, Red.one (.k .i omega), ?_⟩
  intro u h
  cases h
end IndependentBoundaryControls

#print axioms IndependentBoundaryControls.matching_is_not_opaque
#print axioms IndependentBoundaryControls.matching_and_opaque_evaluate
#print axioms IndependentBoundaryControls.wrapper_normal_iff
#print axioms IndependentBoundaryControls.discarded_identity_has_normal_reduct
#print IndependentBoundaryControls.matching_is_not_opaque
#print IndependentBoundaryControls.matching_and_opaque_evaluate
#print IndependentBoundaryControls.wrapper_normal_iff
#print IndependentBoundaryControls.discarded_identity_has_normal_reduct

#ortho_audit IndependentBoundaryControls.matching_is_not_opaque
#ortho_audit IndependentBoundaryControls.matching_and_opaque_evaluate
#ortho_audit IndependentBoundaryControls.wrapper_normal_iff
#ortho_audit IndependentBoundaryControls.discarded_identity_has_normal_reduct
