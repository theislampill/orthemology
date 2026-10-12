import JointNumeralExtraction
import JointExtractionInput
import DomainControls

namespace JointCompletion.EffectiveNumerals.Controls
open OrthemologyV2 OrthemologyV3 P01D P01AC
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T iter)
open OpenDevelopments (run)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft)
open JointCompletion.ExtractionInput (control control_has)
set_option maxRecDepth 32768
set_option maxHeartbeats 16000000

/-- A concrete finite development of the input built with both new rules.
The equality is reduced by the kernel, not accepted from an external evaluator. -/
theorem control_development :
    run 33 (interp (scalarLeft control) T.var) = iter (.var 1) (.var 0) 2 := by
  simp [ExtractionInput.control, ExtractionInput.seed, ExtractionInput.seedPair,
    ExtractionInput.step, RigidityInitiality.sectionPoly, RigidityInitiality.sectionBody,
    RigidityInitiality.totalStep, RigidityInitiality.totalSeed, RigidityInitiality.nextIndex,
    RigidityInitiality.uncurriedStep, SourceRigidity.zero, P01AC.BooleanPrimitive.succPoly,
    P01AC.BooleanPrimitive.succBody, inputNumeral, iterationPoly, scalarLeft, P01D.abstract,
    P01D.freeZero, P01D.drop, P01D.pren, P01D.psub, P01D.fstPoly, P01D.sndPoly,
    P01D.pairPoly, interp, ImportedOpenTermTransport.poly, OpenTermStandardness.eval,
    ImportedOpenTermTransport.embed, run, OpenDevelopments.dev, iter]

theorem control_iteration : PolyConvPlus (scalarLeft control) (iterationPoly 2) := by
  apply ClosedScalarInstances.generic_conversion_reflect
  rw [ClosedScalarInstances.iteration_interp]
  have h := OpenDevelopments.run_conv 33 (interp (scalarLeft control) T.var)
  rw [control_development] at h
  exact h

theorem control_extracts_two : (extractIteration control control_has).val = 2 :=
  extractIteration_unique control_has control_iteration

/-- The numerically extracted old-E representative for this genuinely new
construction is literal inputNumeral 2. -/
theorem control_old_E_representative :
    P01AC.ExtensionalRepair.HasE [] (inputNumeral 2) N ∧
    ∀ f a : Poly, PolyConvPlus (.app (.app control f) a)
      (.app (.app (inputNumeral 2) f) a) := by
  refine ⟨old_numeral_has 2, ?_⟩
  intro f a
  simpa only [control_extracts_two] using recovered_source_applications control control_has f a

/-- Completion retains the existing counterexample to strong normalization:
an admitted closed N term may contain a discarded divergent subterm. -/
theorem admitted_non_SN : ∃ n : Poly, HasJ [] n N ∧
    ¬ StronglyNormalising (eval n zeroEnv) :=
  ⟨OpenDevelopments.DomainControls.padded 2,
    .hasBase (OpenDevelopments.DomainControls.padded_has 2),
    OpenDevelopments.DomainControls.padded_not_SN 2⟩

/- These evaluate the computable extractor with all proof arguments erased. -/
#eval (extractIteration (inputNumeral 0) (.hasBase (old_numeral_has 0))).val
#eval (extractIteration (inputNumeral 2) (.hasBase (old_numeral_has 2))).val
#eval (extractIteration control control_has).val
#eval (extractIteration (OpenDevelopments.DomainControls.padded 2)
  (.hasBase (OpenDevelopments.DomainControls.padded_has 2))).val

#print axioms control_development
#print axioms control_extracts_two
#print axioms control_old_E_representative
#print axioms admitted_non_SN
end JointCompletion.EffectiveNumerals.Controls
