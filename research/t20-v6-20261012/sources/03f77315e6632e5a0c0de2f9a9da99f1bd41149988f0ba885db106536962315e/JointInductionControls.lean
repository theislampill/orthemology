/- A genuinely new Joint, syntactically index-dependent family. This is an input-
   scope discriminator, not an instance in which rigidity is necessary. -/
import JointInductionLaws
import JointControls
namespace JointCompletion.InductionComputation.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl SourceRigidity
open JointCompletion.Controls (newMotive newMotive_subst)
open RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def iterateAt (n : Poly) : Poly := .app (.app n ident) ident
def family : Ty := .identity newMotive (iterateAt (.var 0)) (iterateAt (.var 0))
def step : Poly := abstract (abstract ident)

theorem family_at (n : Poly) : inst family n = .identity newMotive (iterateAt n) (iterateAt n) := by
  simp only [family, inst, subst, newMotive_subst, iterateAt, psub, cons]

theorem iterate_typed {Γ : Tel} {n : Poly} (hc : CtxJ Γ) (hn : HasJ Γ n N) :
    HasJ Γ (iterateAt n) newMotive := by
  have hi := JointCompletion.DependentExtraction.closed_has (JointCompletion.Controls.new_motive_reentry) hc
  have hE := has_form hi
  exact fold_has hc hE hn (.i hE (form_arr hE hE)) hi

/-- The family varies with n in its actual identity endpoints. -/
theorem family_reflexive {Γ : Tel} {n : Poly} (hc : CtxJ Γ) (hn : HasJ Γ n N) :
    HasJ Γ ident (inst family n) := by
  rw [family_at]
  have hi := iterate_typed hc hn
  exact identityIntro_raw (.identity (has_form hi) hi hi) hi hi (.refl _)

theorem family_formed : FormJ [N] family := by
  have hc := CtxJ.ext CtxJ.nil (N_form .nil)
  have hn : HasJ [N] (.var 0) N := .var (N_form hc) .zero
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

theorem family_seed : HasJ [] ident (inst family zero) := family_reflexive .nil (zero_has_N .nil)

theorem family_step : HasJ [] step (dependentStepType family) := by
  have hc := CtxJ.ext CtxJ.nil (N_form .nil)
  have hn : HasJ [N] (.var 0) N := .var (N_form hc) .zero
  have hsn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) (succ_has_NT hc) hn
  have hq := successorFamily_form CtxJ.nil family_formed
  have hi : HasJ [N] ident (successorFamily family) := by
    have h := family_reflexive hc hsn
    simpa only [family_at, successorFamily, family, inst, subst, newMotive_subst, iterateAt, psub, cons] using h
  have hbody := has_wk hi hc family_formed
  apply HasJ.piIntro (.pi (N_form .nil) (form_arr family_formed hq))
  · exact .piIntro (form_arr family_formed hq) hbody (scoped_abstract trivial)
  · exact scoped_abstract (scoped_abstract trivial)

/-- The family has no old-E formation, because that would form its newly
completed carrier in the empty context. -/
theorem family_not_old : ¬ P01AC.ExtensionalRepair.FormE [N] family := by
  intro hP
  have h := P01AC.ExtensionalRepair.Structural.form_inst CtxE.nil hP
    (RigidityInitiality.FullE.zero_has_N CtxE.nil)
  rw [family_at] at h
  cases h with
  | identity hA _ _ => exact JointCompletion.Controls.new_motive_not_old hA

theorem seed_not_old (p : Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [] p (inst family zero) := by
  intro hp
  have hf := P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed hp
  rw [family_at] at hf
  cases hf with
  | identity hA _ _ => exact JointCompletion.Controls.new_motive_not_old hA

theorem step_not_old (s : Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [] s (dependentStepType family) := by
  intro hs
  have hf := P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed hs
  cases hf with
  | pi _ hbody => cases hbody with
    | pi hP _ => exact family_not_old hP

theorem new_family_section : HasJ [] (sectionPoly ident step) (.pi N family) :=
  induction_section .nil family_formed family_seed family_step

theorem new_family_zero : HasJ [] ident
    (.identity (inst family zero) (.app (sectionPoly ident step) zero) ident) :=
  induction_zero .nil family_formed family_seed family_step

theorem new_family_successor : ∃ e, HasJ [] e
    (.identity (inst family (.app succPoly zero))
      (.app (sectionPoly ident step) (.app succPoly zero))
      (.app (.app step zero) (.app (sectionPoly ident step) zero))) :=
  induction_successor .nil family_formed family_seed family_step (zero_has_N .nil)

/-- This reflexive family also admits a direct section. The control is a scope
discriminator, not a minimality claim for the induction rule. -/
theorem direct_section : HasJ [] (abstract ident) (.pi N family) := by
  have hc := CtxJ.ext CtxJ.nil (N_form .nil)
  have hi := family_reflexive hc (HasJ.var (N_form hc) Lookup.zero)
  apply HasJ.piIntro (.pi (N_form .nil) family_formed) ?_
    (scoped_abstract (show Scoped 1 ident from trivial))
  simpa only [family_at] using hi

#print axioms family_formed
#print axioms family_distinct_instances
#print axioms family_not_old
#print axioms seed_not_old
#print axioms step_not_old
#print axioms new_family_section
#print axioms new_family_zero
#print axioms new_family_successor
end JointCompletion.InductionComputation.Controls
