import IndependentMixedControls
import ExtensionalSubstitutionControl
namespace HasEMixedReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
open HasEDependentSubstitutionControls
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem proofId_form : FormE [] proofId :=
  .identity (ClosedProofCanonicalisation.formed extensional_image)
    extensional_image extensional_image

def genuineCtx : Tel := [proofId]
theorem genuine_ctx : CtxE genuineCtx := .ext .nil proofId_form

def genuineImage : Ty := .identity (wk proofId) (.var 0) (.var 0)
theorem genuine_image_form : FormE genuineCtx genuineImage := by
  have hf := form_wk proofId_form CtxE.nil proofId_form
  exact .identity hf (.var hf .zero) (.var hf .zero)

-- The target telescope and replacement type genuinely require actual E evidence.
theorem target_not_original : ¬ Ctx genuineCtx := by
  intro hc
  cases hc with
  | ext _ hf =>
    cases hf with
    | identity _ hi _ => exact no_original_image _ hi

theorem dependent_e_only_transport : HasE genuineCtx (.atom .i)
    (tsubst (fun _ => genuineImage)
      (.identity (.all (endTy 1)) (.atom .i) (.atom .i))) :=
  has_closed_tsubst all_ext_input genuine_ctx (fun _ => genuine_image_form)

theorem transported_result_not_original (p : Poly) :
    ¬ Has genuineCtx p (tsubst (fun _ => genuineImage)
      (.identity (.all (endTy 1)) (.atom .i) (.atom .i))) := by
  intro hp
  exact target_not_original (P01AC.form_ctx (P01AC.has_form hp))

theorem image_genuinely_term_dependent :
    subst (cons (.atom .i) Poly.var) genuineImage ≠ genuineImage := by decide

theorem image_not_a_parameter (n : Nat) : genuineImage ≠ Ty.param n := by
  intro h
  cases h

-- The newer declaration now depends on the older E-only variable.
def dependentGenuineCtx : Tel := genuineImage :: genuineCtx
theorem dependent_genuine_ctx : CtxE dependentGenuineCtx :=
  .ext genuine_ctx genuine_image_form

def dependentGenuineImage : Ty := .identity (wk genuineImage) (.var 0) (.var 0)
theorem dependent_genuine_image_form : FormE dependentGenuineCtx dependentGenuineImage := by
  have hf := form_wk genuine_image_form genuine_ctx genuine_image_form
  exact .identity hf (.var hf .zero) (.var hf .zero)

theorem dependent_telescope_transport : HasE dependentGenuineCtx (.atom .i)
    (tsubst (fun _ => dependentGenuineImage)
      (.identity (.all (endTy 1)) (.atom .i) (.atom .i))) :=
  has_closed_tsubst all_ext_input dependent_genuine_ctx (fun _ => dependent_genuine_image_form)

theorem dependent_target_not_original : ¬ Ctx dependentGenuineCtx := by
  intro hc
  cases hc with
  | ext hc _ => exact target_not_original hc

theorem dependent_target_result_not_original (p : Poly) (A : Ty) :
    ¬ Has dependentGenuineCtx p A := by
  intro hp
  exact dependent_target_not_original (P01AC.form_ctx (P01AC.has_form hp))

#print axioms dependent_telescope_transport
#print axioms dependent_target_result_not_original
#print axioms dependent_e_only_transport
#print axioms target_not_original
#print axioms transported_result_not_original
end HasEMixedReview
