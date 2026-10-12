import DependentBranchApplication
import IdentityControls

namespace HasEDependentSubstitutionControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N)
open P01AC.ExtensionalRepair.Structural
open ClosedChurchIdentity.Controls
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def extId : Ty := .identity N (.atom .i) (.atom P01R.skk)
def proofFamily : Ty := .identity (wk extId) (.var 0) (.var 0)
def proofId : Ty := .identity extId (.atom .i) (.atom .i)

/-- Retained actual-E extensional identity between raw-nonconvertible endpoints. -/
theorem extensional_image : HasE [] (.atom .i) extId := source_equal_raw_distinct.1

/-- This control really cannot supply an original Has substitution image;
    the exclusion uses the retained original identity-conversion theorem. -/
theorem no_original_image (p : Poly) : ¬ Has [] p extId := by
  intro hp
  exact P01Source.I_SKK_not_convertible (P01AC.Intensional.closed_identity_conversion hp)

theorem proofFamily_at (p : Poly) : inst proofFamily p = .identity extId p p := by
  simp only [proofFamily, inst, subst, subst_wk_cancel, subst_id, psub, cons]

theorem image_proof : HasE [] (.atom .i) (inst proofFamily (.atom .i)) := by
  rw [proofFamily_at]
  have hA := ClosedProofCanonicalisation.formed extensional_image
  exact .identityIntro (.identity hA extensional_image extensional_image)
    extensional_image extensional_image (.refl _)

/-- A genuinely dependent source telescope: its newer declaration is the
    self-identity of the older proof variable. Both typed images are actual E. -/
theorem dependent_images : TypedSubstitution [proofFamily, extId] []
    (cons (.atom .i) (cons (.atom .i) Poly.var)) :=
  TypedSubstitution.pair .nil extensional_image image_proof

theorem open_dependent_branch : HasE [proofFamily, extId] (.var 0) (wk proofFamily) := by
  have hA := ClosedProofCanonicalisation.formed extensional_image
  have cA := CtxE.ext CtxE.nil hA
  have hwA := Structural.form_wk hA .nil hA
  have x : HasE [extId] (.var 0) (wk extId) := .var hwA .zero
  have hB : FormE [extId] proofFamily := .identity hwA x x
  exact .var (Structural.form_wk hB cA hB) .zero

/-- Actual simultaneous dependent substitution, rather than reconstructing
    the desired target by another proof. The first image is excluded from Has. -/
theorem substituted_dependent_branch : HasE [] (.atom .i) proofId := by
  have q := Structural.has_subst open_dependent_branch CtxE.nil dependent_images
  simpa only [subst_wk_cancel, proofFamily_at, proofId, cons, psub] using q

/-- Even the result's formation is genuinely beyond original Has, because
    forming the identity at extId there would require an original image. -/
theorem substituted_result_not_original (p : Poly) : ¬ Has [] p proofId := by
  intro hp
  have hf := P01AC.has_form hp
  cases hf with
  | identity _ hx _ => exact no_original_image _ hx

#print axioms extensional_image
#print axioms no_original_image
#print axioms substituted_dependent_branch
#print axioms substituted_result_not_original
end HasEDependentSubstitutionControls
