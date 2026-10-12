import JointRegularity
import JointSoundness
import OpenDevelopments
import ClosedChurchIdentity

namespace JointCompletion.EffectiveNumerals
open OrthemologyV2 P01D P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv iter UniformIter)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft scalarRight)
open OpenDevelopments (run readIteration)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Joint soundness retains full open-carrier Church membership for every
closed Joint numeral, including inputs obtained through the completion rules. -/
theorem closed_church {n : Poly} (hn : HasJ [] n N) :
    OpenTermStandardness.Church (interp n T.var) := by
  rw [ClosedScalarInstances.interp_closed (Structural.has_scoped hn) _ FullPER.zeroEnv]
  exact JointCompletion.fundamental hn FullPER.Application.emptyEnv _ _
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩

theorem closed_uniform_iteration {n : Poly} (hn : HasJ [] n N) :
    UniformIter (interp n T.var) := OpenTermStandardness.church_standard _ (closed_church hn)

/-- The retained exact complete-development strategy terminates on the applied
observation. No normalization statement about unapplied n is made. -/
theorem applied_development_terminates {n : Poly} (hn : HasJ [] n N) :
    ∃ k r, run r (interp (scalarLeft n) T.var) = iter (.var 1) (.var 0) k := by
  obtain ⟨k,hk⟩ := closed_uniform_iteration hn
  obtain ⟨r,hr⟩ := OpenDevelopments.development_complete (OpenDevelopments.iter_normal k)
    (hk (.var 1) (.var 0))
  exact ⟨k,r,hr⟩

theorem applied_readback_exists {n : Poly} (hn : HasJ [] n N) :
    ∃ r, (readIteration (run r (interp (scalarLeft n) T.var))).isSome = true := by
  obtain ⟨k,r,hr⟩ := applied_development_terminates hn
  exact ⟨r, hr ▸ OpenDevelopments.readIteration_iter k⟩

/-- The same executable Nat.find/run/readIteration search used by the retained
E extractor. Only its erased termination certificate now accepts Joint typing. -/
def extractIteration (n : Poly) (hn : HasJ [] n N) :
    { k : Nat // PolyConvPlus (scalarLeft n) (iterationPoly k) } := by
  have h := applied_readback_exists hn
  let r := Nat.find h
  let result := (readIteration (run r (interp (scalarLeft n) T.var))).get (Nat.find_spec h)
  refine ⟨result.val, ClosedScalarInstances.generic_conversion_reflect ?_⟩
  rw [ClosedScalarInstances.iteration_interp]
  have hc := OpenDevelopments.run_conv r (interp (scalarLeft n) T.var)
  rw [result.property] at hc
  exact hc

/-- The extension leaves the old executable extractor literally unchanged. -/
theorem extractIteration_oldE (n : Poly) (hn : P01AC.ExtensionalRepair.HasE [] n N) :
    extractIteration n (.hasBase hn) = OpenDevelopments.extractIteration n hn := rfl

/-- The extracted count is unique among all source-applied iteration certificates. -/
theorem extractIteration_unique {n : Poly} (hn : HasJ [] n N) {k : Nat}
    (hk : PolyConvPlus (scalarLeft n) (iterationPoly k)) :
    (extractIteration n hn).val = k := by
  have he := ImportedOpenTermTransport.source_plus_sound (extractIteration n hn).property T.var
  have ho := ImportedOpenTermTransport.source_plus_sound hk T.var
  rw [ClosedScalarInstances.iteration_interp] at he ho
  exact OpenDevelopments.iter_conv_injective (he.symm.trans ho)

theorem extractIteration_uniform (n : Poly) (hn : HasJ [] n N) :
    ∀ f a, Conv ((interp n T.var).app f |>.app a)
      (iter f a (extractIteration n hn).val) := by
  obtain ⟨k,hk⟩ := closed_uniform_iteration hn
  have he := ImportedOpenTermTransport.source_plus_sound (extractIteration n hn).property T.var
  rw [ClosedScalarInstances.iteration_interp] at he
  have eq := OpenDevelopments.iter_conv_injective ((hk (.var 1) (.var 0)).symm.trans he)
  exact eq ▸ hk

/-- The representative is an original-source numeral, hence also old E typed. -/
theorem old_numeral_has (k : Nat) : P01AC.ExtensionalRepair.HasE [] (inputNumeral k) N :=
  P01AC.ExtensionalRepair.has_inclusion (P01AC.EffectiveCompleteness.inputNumeral_has k)

/-- Literal generic-open source observations agree with the recovered numeral. -/
theorem recovered_observation (n : Poly) (hn : HasJ [] n N) :
    PolyConvPlus (scalarLeft n) (scalarLeft (inputNumeral (extractIteration n hn).val)) :=
  (extractIteration n hn).property.trans (ClosedChurchIdentity.numeral_observation _).symm

/-- Source-faithful equivalence after any supplied source iterator and seed.
This is applied observational conservativity, not raw conversion n = numeral. -/
theorem recovered_source_applications (n : Poly) (hn : HasJ [] n N) (f a : Poly) :
    PolyConvPlus (.app (.app n f) a)
      (.app (.app (inputNumeral (extractIteration n hn).val) f) a) := by
  have h := P01AC.ExtensionalRepair.Structural.polyConvPlus_subst
    (recovered_observation n hn) (cons a (cons f Poly.var))
  simpa only [scalarLeft, psub, cons,
    P01AC.BooleanPrimitive.psub_closed (Structural.has_scoped hn),
    P01AC.BooleanPrimitive.psub_closed
      (P01AC.has_scoped (P01AC.EffectiveCompleteness.inputNumeral_has _))] using h

/-- The same old numeral agrees uniformly on every open-carrier pair of inputs. -/
theorem recovered_open_applications (n : Poly) (hn : HasJ [] n N) (f a : T) :
    Conv ((interp n T.var).app f |>.app a)
      ((interp (inputNumeral (extractIteration n hn).val) T.var).app f |>.app a) := by
  let k := (extractIteration n hn).val
  have h1 := Conv.app (ImportedOpenTermTransport.interp_abstraction_beta
    (abstract (iterationPoly k)) T.var f) (Conv.refl a)
  have h2 := ImportedOpenTermTransport.interp_abstraction_beta
    (iterationPoly k) (OpenTermStandardness.cons f T.var) a
  have num : Conv ((interp (inputNumeral k) T.var).app f |>.app a) (iter f a k) :=
    h1.trans ((ClosedChurchIdentity.interp_iteration k _ _ _) ▸ h2)
  exact (extractIteration_uniform n hn f a).trans num.symm

/-- Explicit closed-N observational conservativity of Joint over old E. The
representative's index is returned by the checked executable extractor. -/
theorem closed_N_observational_conservativity (n : Poly) (hn : HasJ [] n N) :
    P01AC.ExtensionalRepair.HasE [] (inputNumeral (extractIteration n hn).val) N ∧
    (∀ f a : Poly, PolyConvPlus (.app (.app n f) a)
      (.app (.app (inputNumeral (extractIteration n hn).val) f) a)) ∧
    (∀ f a : T, Conv ((interp n T.var).app f |>.app a)
      ((interp (inputNumeral (extractIteration n hn).val) T.var).app f |>.app a)) :=
  ⟨old_numeral_has _, recovered_source_applications n hn, recovered_open_applications n hn⟩

#print axioms closed_church
#print axioms applied_development_terminates
#print axioms extractIteration
#print axioms extractIteration_oldE
#print axioms extractIteration_unique
#print axioms extractIteration_uniform
#print axioms recovered_source_applications
#print axioms recovered_open_applications
#print axioms closed_N_observational_conservativity
end JointCompletion.EffectiveNumerals
