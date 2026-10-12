import JointSigmaExtraction
import JointExtractionControls
import Lean

namespace JointCompletion.DependentExtraction.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.Intensional.Plus (PolyConvPlus)
open JointCompletion.Controls (newMotive newMotive_subst)
open JointCompletion.ExtractionInput (control control_has)
open ClosedScalarInstances (scalarLeft)
set_option maxRecDepth 32768
set_option maxHeartbeats 16000000

/-- Both genuinely dependent in the numeric index and genuinely newly formed. -/
def fiber : Ty := .sigma (.identity N (.var 0) (inputNumeral 2)) (wk newMotive)
def fiberAt (n : Poly) : Ty := .sigma (.identity N n (inputNumeral 2)) newMotive
def evidence : Poly := pairPoly (.atom .i) (.atom .i)
def package : Poly := pairPoly control evidence

theorem fiber_inst (n : Poly) : inst fiber n = fiberAt n := by
  simp [fiber, fiberAt, inst, subst, P01AC.BooleanPrimitive.N_subst, psub, cons,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped (P01AC.EffectiveCompleteness.inputNumeral_has 2)),
    wk, newMotive_subst]

theorem fiber_form : FormJ [N] fiber := by
  have cN : CtxJ [N] := .ext .nil (Structural.form_nat .nil)
  have hn : HasJ [N] (.var 0) N := .var (Structural.form_nat cN) .zero
  have hk : HasJ [N] (inputNumeral 2) N :=
    closed_has (.hasBase (EffectiveNumerals.old_numeral_has 2)) cN
  have hi := FormJ.identity (Structural.form_nat cN) hn hk
  exact .sigma hi (Structural.form_wk JointCompletion.Controls.new_motive_at_N cN hi)

theorem fiberAt_form (n : Poly) (hn : HasJ [] n N) : FormJ [] (fiberAt n) :=
  fiber_inst n ▸ Structural.form_inst .nil fiber_form hn

theorem evidence_has : HasJ [] evidence (inst fiber control) := by
  rw [fiber_inst]
  have hi : HasJ [] (.atom .i) (.identity N control (inputNumeral 2)) :=
    canonicity_at_count control_has EffectiveNumerals.Controls.control_iteration
  apply HasJ.sigmaIntro (fiberAt_form control control_has)
    (show FormJ [] (inst newMotive (.atom .i)) by
      simpa only [inst, newMotive_subst] using JointCompletion.Controls.new_motive_form Ctx.nil) hi
  simpa only [inst, newMotive_subst] using JointCompletion.Controls.new_motive_reentry

theorem package_has : HasJ [] package (.sigma N fiber) :=
  .sigmaIntro (.sigma (Structural.form_nat .nil) fiber_form)
    (Structural.form_inst .nil fiber_form control_has) control_has evidence_has

/-- This particular inhabited fiber is unavailable even as old-E formation. -/
theorem fiberAt_two_not_old :
    ¬ P01AC.ExtensionalRepair.FormE [] (fiberAt (inputNumeral 2)) := by
  intro h
  have hn := EffectiveNumerals.old_numeral_has 2
  have hI : P01AC.ExtensionalRepair.FormE [] (.identity N (inputNumeral 2) (inputNumeral 2)) :=
    .identity (RigidityInitiality.FullE.N_form .nil) hn hn
  have hi : P01AC.ExtensionalRepair.HasE [] (.atom .i)
      (.identity N (inputNumeral 2) (inputNumeral 2)) :=
    .identityIntro hI hn hn (.refl _)
  cases h with
  | sigma _ hB =>
      have hc := P01AC.ExtensionalRepair.Structural.form_inst .nil hB hi
      apply JointCompletion.Controls.new_motive_not_old
      simpa only [inst, newMotive_subst] using hc

theorem fiber_not_old : ¬ P01AC.ExtensionalRepair.FormE [N] fiber := by
  intro h
  apply fiberAt_two_not_old
  rw [← fiber_inst]
  exact P01AC.ExtensionalRepair.Structural.form_inst .nil h
    (EffectiveNumerals.old_numeral_has 2)

theorem package_type_not_old :
    ¬ P01AC.ExtensionalRepair.FormE [] (.sigma N fiber) := by
  intro h
  cases h with | sigma _ hP => exact fiber_not_old hP

theorem package_type_uninhabited_old (p : Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [] p (.sigma N fiber) :=
  fun h => package_type_not_old (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h)

/-- Dependency is real: returning numeral one would leave an empty Joint fiber. -/
theorem wrong_index_uninhabited (p : Poly) :
    ¬ HasJ [] p (fiberAt (inputNumeral 1)) := by
  intro h
  have hS := Structural.has_form h
  have hId := HasJ.sigmaFst (form_sigma_inv hS).1 hS h
  have impossible := identity_implies_count_eq
    (.hasBase (EffectiveNumerals.old_numeral_has 1))
    (.hasBase (EffectiveNumerals.old_numeral_has 2))
    (ClosedChurchIdentity.numeral_observation 1)
    (ClosedChurchIdentity.numeral_observation 2) hId
  cases impossible

theorem package_first : PolyConvPlus (fstPoly package) control := by
  apply ClosedScalarInstances.generic_conversion_reflect
  simpa only [package, JointCompletion.eval_fst, JointCompletion.eval_pair] using
    OpenTermStandardness.fst_pair
      (ImportedOpenTermTransport.interp control OpenTermStandardness.T.var)
      (ImportedOpenTermTransport.interp evidence OpenTermStandardness.T.var)

theorem package_iteration : PolyConvPlus (scalarLeft (fstPoly package)) (iterationPoly 2) :=
  ((PolyConvPlus.app (.app package_first (.refl _)) (.refl _))).trans
    EffectiveNumerals.Controls.control_iteration

theorem package_extracts_two : (extractSigma fiber package package_has).count = 2 :=
  extractSigma_unique package_has package_iteration

theorem preserved_fiber_at_two :
    HasJ [] (sndPoly package) (fiberAt (inputNumeral 2)) := by
  have h := (extractSigma fiber package package_has).fiber_has
  simpa only [package_extracts_two, fiber_inst] using h

#eval @decide _ (decideTypedIdentity control_has (.hasBase (EffectiveNumerals.old_numeral_has 2)))
#eval @decide _ (decideTypedIdentity control_has (.hasBase (EffectiveNumerals.old_numeral_has 1)))
#print axioms fiberAt_two_not_old
#print axioms fiber_not_old
#print axioms package_type_uninhabited_old
#print axioms wrong_index_uninhabited
#eval (extractSigma fiber package package_has).count
#print axioms fiber_form
#print axioms package_has
#print axioms package_extracts_two
#print axioms preserved_fiber_at_two
end JointCompletion.DependentExtraction.Controls

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``JointCompletion.DependentExtraction.identity_of_observation,
      ``JointCompletion.DependentExtraction.canonicity_at_count,
      ``JointCompletion.DependentExtraction.extracted_identity,
      ``JointCompletion.DependentExtraction.identity_implies_count_eq,
      ``JointCompletion.DependentExtraction.identity_iff_extracted_count,
      ``JointCompletion.DependentExtraction.decideTypedIdentity,
      ``JointCompletion.DependentExtraction.transport_source,
      ``JointCompletion.DependentExtraction.transport_erased,
      ``JointCompletion.DependentExtraction.extractSigma,
      ``JointCompletion.DependentExtraction.extractSigma_unique,
      ``JointCompletion.DependentExtraction.extracted_continuation,
      ``JointCompletion.DependentExtraction.Controls.package_has,
      ``JointCompletion.DependentExtraction.Controls.wrong_index_uninhabited,
      ``JointCompletion.DependentExtraction.Controls.package_type_uninhabited_old,
      ``JointCompletion.DependentExtraction.Controls.package_extracts_two,
      ``JointCompletion.DependentExtraction.Controls.preserved_fiber_at_two] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    logInfo m!"PASS {target}: only standard logical axioms."
  for target in [``JointCompletion.DependentExtraction.identity_of_observation,
      ``JointCompletion.DependentExtraction.canonicity_at_count,
      ``JointCompletion.DependentExtraction.transport_source,
      ``JointCompletion.DependentExtraction.transport_erased] do
    let (_, source) := ((Lean.CollectAxioms.collect target).run env).run {}
    for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
        ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction] do
      if source.visited.contains forbidden then
        throwError "Semantic shortcut in source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: no semantic typing shortcut."
