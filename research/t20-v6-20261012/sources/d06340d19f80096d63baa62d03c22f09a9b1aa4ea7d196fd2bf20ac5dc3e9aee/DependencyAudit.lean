import OpenDevelopments
import ScalarCertificates
import Lean.Util.CollectAxioms

/- A transitive declaration-dependency inspection, not a proof oracle. -/
open Lean in
run_cmd do
  let env ← getEnv
  let (_, s) := ((Lean.CollectAxioms.collect
    `ScalarCertificates.checkedSourceInstance).run env).run {}
  let excluded : Array Name := #[`FullPER.fundamental,
    `OpenTermStandardness.church_standard,
    `P01AC.EffectiveCompleteness.semantic_church_standardness,
    `ClosedScalarInstances.closed_scalar_conversion,
    `ClosedScalarInstances.source_uniform_iteration,
    `ClosedScalarInstances.closed_scalar_instance_exact,
    `P01AC.ExtensionalRepair.ClosedProofCanonicalisation.canonical_identity,
    `OpenDevelopments.extractIteration,
    `P01AC.ExtensionalRepair.fundamental,
    `P01AC.ExtensionalRepair.unary_fundamental]
  for n in excluded do
    if s.visited.contains n then
      throwError "Unexpected semantic/search dependency in positive replay: {n}"
    logInfo m!"Excluded replay dependency: {n}"
  let required : Array Name := #[`ClosedScalarInstances.generic_conversion_reflect,
    `P01AC.Intensional.Plus.PolyConvPlus.bridge,
    `P01AC.ExtensionalRepair.HasE.conv,
    `P01AC.ExtensionalRepair.HasE.identityIntro,
    `P01AC.ExtensionalRepair.HasE.piIntro,
    `P01AC.ExtensionalRepair.HasE.allIntro]
  for n in required do
    if !s.visited.contains n then
      throwError "Missing actual source replay dependency: {n}"
    logInfo m!"Required replay dependency: {n}"
  logInfo m!"Positive replay axioms: {s.axioms}"

open Lean in
run_cmd do
  let env ← getEnv
  let (_, s) := ((Lean.CollectAxioms.collect
    `OpenDevelopments.extractIteration).run env).run {}
  let required : Array Name := #[`Nat.find,
    `OpenDevelopments.readIteration, `OpenDevelopments.run,
    `OpenDevelopments.dev, `OpenDevelopments.development_complete,
    `FullPER.fundamental, `OpenTermStandardness.church_standard,
    `ClosedScalarInstances.generic_conversion_reflect]
  for n in required do
    if !s.visited.contains n then
      throwError "Missing extraction/termination dependency: {n}"
    logInfo m!"Required extraction dependency: {n}"
  logInfo m!"Extraction axioms, including erased termination proof: {s.axioms}"
