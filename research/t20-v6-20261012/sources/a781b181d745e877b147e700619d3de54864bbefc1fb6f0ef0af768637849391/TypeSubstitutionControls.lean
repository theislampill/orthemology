/- Discriminating controls for target-term-dependent and genuinely E-only
   replacement types, using the same unchanged source judgements. -/
import TypeSubstitutionApplications
import ExtensionalSubstitutionControl
namespace HasETypeSubstitutionControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem arrow_formed {Γ : Tel} {A B : Ty} (hA : FormE Γ A) (hB : FormE Γ B) :
    FormE Γ (arr A B) := .pi hA (Structural.form_wk hB (Structural.form_ctx hA) hA)

def sourceType : Ty := .all (arr (.param 1) (.param 1))
def sourcePoly : Poly := .atom .i

theorem source_typing : HasE [] sourcePoly sourceType := by
  have hf : FormE [] (arr (.param 1) (.param 1)) := arrow_formed (.param .nil) (.param .nil)
  exact .allIntro (.all .nil hf) (.i (.param .nil) hf)

def dependentImage : Ty := .identity .raw (.var 0) (.var 0)
def dependentTypes : Nat → Ty := cons dependentImage Ty.param

theorem dependent_context : CtxE [.raw] := .ext .nil (.raw .nil)

theorem dependent_image_formed : FormE [.raw] dependentImage := by
  have hx : HasE [.raw] (.var 0) .raw := .var (.raw dependent_context) .zero
  exact .identity (.raw dependent_context) hx hx

theorem dependent_images_formed : ∀ n, FormE [.raw] (dependentTypes n) := by
  intro n
  cases n with
  | zero => exact dependent_image_formed
  | succ n => exact .param dependent_context

/-- The image has a real free target variable and crosses both All and Pi.
The target is obtained by general type substitution of the source derivation. -/
theorem dependent_type_instance : HasE [.raw] sourcePoly
    (.all (.pi dependentImage (.identity .raw (.var 1) (.var 1)))) := by
  exact has_closed_tsubst source_typing dependent_context dependent_images_formed

/-- Omitting the term lift would capture the old free variable. -/
theorem wrong_unlifted_codomain :
    tsubst dependentTypes sourceType ≠
      .all (.pi dependentImage (.identity .raw (.var 0) (.var 0))) := by
  intro h
  cases h

def closeTerm : Nat → Poly := cons (.atom .i) Poly.var

theorem close_term_typed : TypedSubstitution [.raw] [] closeTerm :=
  TypedSubstitution.single .nil (.rawAtom (.raw .nil))

def closedImage : Ty := .identity .raw (.atom .i) (.atom .i)

/-- This result invokes the actual dependent term theorem after type transport.
The final type has replaced both endpoints of the injected type image. -/
theorem type_then_term_result : HasE [] sourcePoly (.all (arr closedImage closedImage)) := by
  have h := has_type_then_term source_typing dependent_context
    (TypeSubstitution.empty dependent_images_formed) CtxE.nil close_term_typed
  exact h

/-- Simply retaining τ after applying the term map gives a different raw type. -/
theorem unchanged_type_images_wrong :
    mixed closeTerm dependentTypes sourceType ≠
      mixed closeTerm (fun n => subst closeTerm (dependentTypes n)) sourceType := by
  intro h
  cases h

open HasEDependentSubstitutionControls (proofId extId)

/-- This replacement type's formation itself requires genuine actual-E typing. -/
theorem beyond_original_image_formed : FormE [] proofId :=
  ClosedProofCanonicalisation.formed
    HasEDependentSubstitutionControls.substituted_dependent_branch

theorem beyond_original_image_not_formed : ¬ Form [] proofId := by
  intro h
  cases h with
  | identity _ hx _ => exact HasEDependentSubstitutionControls.no_original_image _ hx

/-- Replacing a free parameter by the E-only type uses no term substitution. -/
theorem beyond_original_type_instance : HasE [] sourcePoly (.all (arr proofId proofId)) := by
  have ht : ∀ n, FormE [] (cons proofId Ty.param n) := by
    intro n
    cases n with
    | zero => exact beyond_original_image_formed
    | succ n => exact .param .nil
  have hh := has_closed_tsubst source_typing CtxE.nil ht
  simpa only [sourceType, tsubst, mixed, tup, cons, twk, trename, proofId,
    HasEDependentSubstitutionControls.extId, P01AC.EffectiveCompleteness.N,
    P01AC.EffectiveCompleteness.NBody, arr, wk, subst, psub, pup] using hh

/-- The substituted result cannot be recovered by silently using old Has. -/
theorem beyond_original_result_not_typed (p : Poly) :
    ¬ Has [] p (.all (arr proofId proofId)) := by
  intro hp
  have hf := P01AC.has_form hp
  cases hf with
  | all _ hB =>
    cases hB with
    | pi hA _ => exact beyond_original_image_not_formed hA

#print axioms dependent_type_instance
#print axioms type_then_term_result
#print axioms unchanged_type_images_wrong
#print axioms beyond_original_type_instance
#print axioms beyond_original_result_not_typed
end HasETypeSubstitutionControls
