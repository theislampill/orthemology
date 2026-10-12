/- An actual-E-only, syntactically index-dependent family. This is an input-
   scope discriminator, not an instance in which rigidity is necessary. -/
import FullESectionApplication
import TypeSubstitutionControls
namespace RigidityInitiality.FullE.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl SourceRigidity
open HasEDependentSubstitutionControls (extId)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def iterateAt (n : Poly) : Poly := .app (.app n ident) ident
def family : Ty := .identity extId (iterateAt (.var 0)) (iterateAt (.var 0))
def step : Poly := abstract (abstract ident)

theorem extId_subst (σ : Nat → Poly) : subst σ extId = extId := by
  simp only [extId, subst, N_subst, psub]

theorem family_at (n : Poly) : inst family n = .identity extId (iterateAt n) (iterateAt n) := by
  simp only [family, inst, subst, extId_subst, iterateAt, psub, cons]

theorem iterate_typed {Γ : Tel} {n : Poly} (hc : CtxE Γ) (hn : HasE Γ n N) :
    HasE Γ (iterateAt n) extId := by
  have hi := Structural.has_closed HasEDependentSubstitutionControls.extensional_image hc
  have hE := has_form hi
  exact fold_has hc hE hn (.i hE (form_arr hE hE)) hi

/-- The family varies with n in its actual identity endpoints. -/
theorem family_reflexive {Γ : Tel} {n : Poly} (hc : CtxE Γ) (hn : HasE Γ n N) :
    HasE Γ ident (inst family n) := by
  rw [family_at]
  have hi := iterate_typed hc hn
  exact identityIntro_raw (.identity (has_form hi) hi hi) hi hi (.refl _)

theorem family_formed : FormE [N] family := by
  have hc := CtxE.ext CtxE.nil (N_form .nil)
  have hn : HasE [N] (.var 0) N := .var (N_form hc) .zero
  exact .identity (has_form (iterate_typed hc hn)) (iterate_typed hc hn) (iterate_typed hc hn)

/-- Literal variation, not only dependence in a displayed comment. -/
theorem family_distinct_instances : inst family zero ≠ inst family (.app succPoly zero) := by
  rw [family_at, family_at]
  intro h
  have e : zero = .app succPoly zero := by
    have hp := (Ty.identity.inj h).2.1
    exact (Poly.app.inj (Poly.app.inj hp).1).1
  have hsize := congrArg sizeOf e
  have hlt : sizeOf zero < sizeOf (Poly.app succPoly zero) := by simp
  omega

theorem family_seed : HasE [] ident (inst family zero) := family_reflexive .nil (zero_has_N .nil)

theorem family_step : HasE [] step (dependentStepType family) := by
  have hc := CtxE.ext CtxE.nil (N_form .nil)
  have hn : HasE [N] (.var 0) N := .var (N_form hc) .zero
  have hsn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) (succ_has_NT hc) hn
  have hq := successorFamily_form CtxE.nil family_formed
  have hi : HasE [N] ident (successorFamily family) := by
    have h := family_reflexive hc hsn
    simpa only [family_at, successorFamily, family, subst, extId_subst, iterateAt, psub, cons] using h
  have hbody := has_wk hi hc family_formed
  apply HasE.piIntro (.pi (N_form .nil) (form_arr family_formed hq))
  · exact .piIntro (form_arr family_formed hq) hbody (scoped_abstract trivial)
  · exact scoped_abstract (scoped_abstract trivial)

/-- The predecessor's original Form-family premise is provably impossible. -/
theorem family_not_original : ¬ Form [N] family := by
  intro hP
  have h := RigidityInitiality.form_inst_source Ctx.nil hP (SourceRigidity.zero_has_N Ctx.nil)
  rw [family_at] at h
  cases h with
  | identity _ hx _ => exact HasEDependentSubstitutionControls.no_original_image _ hx

theorem seed_not_original (p : Poly) : ¬ Has [] p (inst family zero) := by
  intro hp
  have hf := P01AC.has_form hp
  rw [family_at] at hf
  cases hf with
  | identity _ hx _ => exact HasEDependentSubstitutionControls.no_original_image _ hx

theorem step_not_original (s : Poly) : ¬ Has [] s (dependentStepType family) := by
  intro hs
  have hf := P01AC.has_form hs
  cases hf with
  | pi _ hbody => cases hbody with
    | pi hP _ => exact family_not_original hP

/-- A genuine application of the full-E theorem outside old premise scope.
Rigidity is bound; the result makes no claim to a closed rigidity witness. -/
theorem actual_only_rigidity_implication :
    HasE [] (abstract (sectionPoly (pren Nat.succ ident) (pren Nat.succ step)))
      (arr Rigidity (.pi N family)) :=
  rigidity_implies_section .nil family_formed family_seed family_step

/-- This control is easy enough to admit a separate section without R.
Its role is scope discrimination, never necessity of rigidity. -/
theorem control_has_direct_section : HasE [] (abstract ident) (.pi N family) := by
  have hc := CtxE.ext CtxE.nil (N_form .nil)
  have hi := family_reflexive hc (HasE.var (N_form hc) Lookup.zero)
  apply HasE.piIntro (.pi (N_form .nil) family_formed) ?_
    (scoped_abstract (show Scoped 1 ident from trivial))
  simpa only [family_at] using hi

#print axioms family_formed
#print axioms family_distinct_instances
#print axioms family_not_original
#print axioms seed_not_original
#print axioms step_not_original
#print axioms actual_only_rigidity_implication
#print axioms control_has_direct_section
end RigidityInitiality.FullE.Controls
