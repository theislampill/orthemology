import FullEComputationLaws
import TypeSubstitutionControls
namespace FullEIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open RigidityInitiality SourceRigidity
open HasEDependentSubstitutionControls (extId proofId)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Independent E-only, constant-family scope control. No necessity of R claimed. -/
def constantFamily : Ty := wk proofId
def constantStep : Poly := abstract ident

theorem proofId_subst (σ : Nat → Poly) : subst σ proofId = proofId := by
  simp only [proofId, extId, subst, N_subst, psub]

theorem family_eq : constantFamily = proofId := proofId_subst _
theorem family_at (n : Poly) : inst constantFamily n = proofId := by
  rw [family_eq]
  exact proofId_subst _
theorem family_successor : successorFamily constantFamily = constantFamily := by
  rw [family_eq]
  exact proofId_subst _

theorem seed : HasE [] ident proofId :=
  HasEDependentSubstitutionControls.substituted_dependent_branch

theorem family_formed : FormE [N] constantFamily :=
  RigidityInitiality.FullE.form_wk (RigidityInitiality.FullE.has_form seed) .nil (RigidityInitiality.FullE.N_form .nil)

theorem family_not_original : ¬ Form [N] constantFamily := by
  intro h
  have hf := RigidityInitiality.form_inst_source Ctx.nil h (inputNumeral_has 0)
  rw [family_at] at hf
  exact HasETypeSubstitutionControls.beyond_original_image_not_formed hf

theorem seed_not_original (p : Poly) : ¬ Has [] p (inst constantFamily zero) := by
  rw [family_at]
  exact HasEDependentSubstitutionControls.substituted_result_not_original p

theorem step : HasE [] constantStep (dependentStepType constantFamily) := by
  have hc := CtxE.ext CtxE.nil (RigidityInitiality.FullE.N_form .nil)
  have hPi := FormE.pi (RigidityInitiality.FullE.N_form .nil) (RigidityInitiality.FullE.form_arr family_formed family_formed)
  have hi : HasE [N] ident (arr constantFamily constantFamily) :=
    .i family_formed (RigidityInitiality.FullE.form_arr family_formed family_formed)
  have h := HasE.piIntro hPi hi (scoped_abstract (RigidityInitiality.FullE.has_scoped hi))
  simpa only [constantStep, dependentStepType, family_successor] using h

theorem step_not_original (p : Poly) : ¬ Has [] p (dependentStepType constantFamily) := by
  intro hp
  have hf := P01AC.has_form hp
  cases hf with
  | pi _ hbody =>
    cases hbody with
    | pi hP _ => exact family_not_original hP

/-- Invokes the new uniform theorem on a seed and step unavailable to old Has. -/
theorem fullE_scope_implication :
    HasE [] (abstract (sectionPoly (pren Nat.succ ident) (pren Nat.succ constantStep)))
      (arr Rigidity (.pi N constantFamily)) :=
  RigidityInitiality.FullE.rigidity_implies_section .nil family_formed ((family_at zero).symm ▸ seed) step

/-- This particular constant family has a direct section; R is not essential to it. -/
theorem direct_constant_section : HasE [] (abstract ident) (.pi N constantFamily) := by
  have hi := RigidityInitiality.FullE.has_wk seed CtxE.nil (RigidityInitiality.FullE.N_form .nil)
  exact .piIntro (.pi (RigidityInitiality.FullE.N_form .nil) family_formed) hi
    (scoped_abstract (RigidityInitiality.FullE.has_scoped hi))

/-- Existing zero law applies to the E-only input without assuming R. -/
theorem zero_control : HasE [] ident
    (.identity (inst constantFamily zero) (sectionBody ident constantStep zero) ident) :=
  RigidityInitiality.FullE.section_zero_law .nil family_formed ((family_at zero).symm ▸ seed) step

/-- The generic statement is exercised at arbitrary E-typed numeral and R evidence. -/
theorem conditional_successor_control {r n : Poly}
    (hr : HasE [] r Rigidity) (hn : HasE [] n N) :
    ∃ e, HasE [] e (.identity (inst constantFamily (.app succPoly n))
      (sectionBody ident constantStep (.app succPoly n))
      (.app (.app constantStep n) (sectionBody ident constantStep n))) :=
  RigidityInitiality.FullE.section_successor_law .nil family_formed ((family_at zero).symm ▸ seed) step hr hn

#print axioms fullE_scope_implication
#print axioms family_not_original
#print axioms step_not_original
#print axioms direct_constant_section
#print axioms conditional_successor_control
end FullEIndependentReview
