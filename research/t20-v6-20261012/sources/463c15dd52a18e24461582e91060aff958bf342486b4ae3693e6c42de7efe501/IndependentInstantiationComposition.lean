import IndependentDependentTarget
import IndependentJConversion
namespace HasEMixedReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem top_in_dependent_e_context : HasE dependentGenuineCtx (.atom .i)
    (arr dependentGenuineImage dependentGenuineImage) := by
  have hp := end_i (ctx_twk dependent_genuine_ctx) 0
  exact has_tinst hp dependent_genuine_image_form

theorem all_elim_in_dependent_e_context : HasE dependentGenuineCtx (.atom .i)
    (arr dependentGenuineImage dependentGenuineImage) := by
  have hb := end_form (ctx_twk dependent_genuine_ctx) 0
  have hp := end_i (ctx_twk dependent_genuine_ctx) 0
  have hf := FormE.all dependent_genuine_ctx hb
  exact allElim_formed (HasE.allIntro hf hp) dependent_genuine_image_form

theorem composed_mixed_maps : Structural.MixedSubstitution sourceCtx []
    (fun _ => .atom .i) (fun _ => .identity .raw (.atom .i) (.atom .i)) := by
  have ht : TypedSubstitution rawCtx [] (cons (.atom .i) Poly.var) :=
    TypedSubstitution.single .nil (.rawAtom (.raw .nil))
  exact nonrenaming_mixed_map.comp CtxE.nil (ht.toMixed .nil)

theorem composed_mixed_result : HasE []
    (.app (.app (.atom .k) (jPoly (.atom .i) (.atom .i) (.atom .i))) (.atom .i))
    (.identity .raw (.atom .i) (.atom .i)) :=
  has_mixed conv_j_input .nil composed_mixed_maps

#print axioms top_in_dependent_e_context
#print axioms all_elim_in_dependent_e_context
#print axioms composed_mixed_maps
#print axioms composed_mixed_result
end HasEMixedReview
