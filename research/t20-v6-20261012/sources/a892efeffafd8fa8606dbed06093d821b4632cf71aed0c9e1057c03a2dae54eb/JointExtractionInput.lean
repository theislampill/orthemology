/- A finite, closed natural-number input that traverses both actual Joint rules,
   including a Sigma whose second component is not formed in unchanged HasE. -/
import JointRegularity
import JointControls

namespace JointCompletion.ExtractionInput
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.EffectiveCompleteness (N inputNumeral inputNumeral_has)
open P01AC.BooleanPrimitive (N_subst succPoly)
open SourceRigidity (zero)
open RigidityInitiality (dependentStepType sectionPoly)
open JointCompletion.Controls (newMotive newMotive_subst)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The second component uses endpoint typing available only after completion. -/
def inputSigma : Ty := .sigma N newMotive

def seedPair : Poly := pairPoly zero (.atom .i)

def seed : Poly := fstPoly seedPair

/-- The induction step ignores the index and applies Church successor. -/
def step : Poly := abstract succPoly

/-- Two iterations starting at the Sigma-elimination-derived zero. -/
def control : Poly := .app (sectionPoly seed step) (inputNumeral 2)

theorem inputSigma_form : FormJ [] inputSigma :=
  .sigma (Structural.form_nat .nil) Controls.new_motive_at_N

theorem inputSigma_not_old : ¬ P01AC.ExtensionalRepair.FormE [] inputSigma := by
  intro h
  cases h with
  | sigma _ hB => exact Controls.new_motive_at_N_not_old hB

/-- Even the completed Sigma input itself has no unchanged-HasE typing. -/
theorem inputSigma_uninhabited_old (p : Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [] p inputSigma :=
  fun h => inputSigma_not_old (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h)

/-- The proof component re-enters elimination with a genuinely new motive. -/
theorem seedPair_has : HasJ [] seedPair inputSigma := by
  apply HasJ.sigmaIntro inputSigma_form
    (show FormJ [] (inst newMotive zero) by
      simpa only [inst, newMotive_subst] using Controls.new_motive_form Ctx.nil)
    (.hasBase (RigidityInitiality.FullE.zero_has_N .nil))
  simpa only [inst, newMotive_subst] using Controls.new_motive_reentry

/-- This is actual Sigma elimination, with a new-type branch context. -/
theorem seed_has : HasJ [] seed N := by
  have cN : CtxJ [N] := .ext .nil (Structural.form_nat .nil)
  have cB : CtxJ [newMotive, N] := .ext cN Controls.new_motive_at_N
  have cS : CtxJ [inputSigma] := .ext .nil inputSigma_form
  have hd : HasJ [newMotive, N] (.var 1) (SigmaCompletion.branchType N) :=
    .var (Structural.form_nat cB) (.succ .zero)
  exact HasJ.sigmaElim .nil (Structural.form_nat .nil) Controls.new_motive_at_N
    (Structural.form_nat cS) hd seedPair_has

theorem step_has : HasJ [] step (dependentStepType N) := by
  have cN : P01AC.ExtensionalRepair.CtxE [N] :=
    .ext .nil (RigidityInitiality.FullE.N_form .nil)
  have hs := RigidityInitiality.FullE.succ_has_NT cN
  have hf : P01AC.ExtensionalRepair.FormE [] (.pi N (arr N N)) :=
    .pi (RigidityInitiality.FullE.N_form .nil)
      (RigidityInitiality.FullE.form_arr (RigidityInitiality.FullE.N_form cN)
        (RigidityInitiality.FullE.N_form cN))
  exact .hasBase (.piIntro hf hs
    (scoped_abstract (RigidityInitiality.FullE.has_scoped hs)))

/-- The seed is the preceding completed Sigma elimination, not an old-E premise. -/
theorem section_has : HasJ [] (sectionPoly seed step) (.pi N N) :=
  .natInduction .nil (Structural.form_nat (.ext .nil (Structural.form_nat .nil)))
    seed_has step_has

theorem control_has : HasJ [] control N :=
  .piElim (Structural.has_form section_has) (Structural.form_nat .nil)
    section_has (.hasBase (P01AC.ExtensionalRepair.has_inclusion (inputNumeral_has 2)))

theorem control_closed : Scoped 0 control := Structural.has_scoped control_has

#print axioms inputSigma_not_old
#print axioms inputSigma_uninhabited_old
#print axioms seedPair_has
#print axioms seed_has
#print axioms section_has
#print axioms control_has
#print axioms control_closed
end JointCompletion.ExtractionInput
