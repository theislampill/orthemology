import ClosedScalarInstances
import Lean.Util.CollectAxioms

/- Dependency inspection is not a theorem or evaluator oracle. -/
open Lean in
run_cmd do
  let env ← getEnv
  let (_, s) := ((Lean.CollectAxioms.collect
    `ClosedScalarInstances.closed_scalar_instance_exact).run env).run {}
  let excluded : Array Name := #[`P01AC.F, `P01AC.G, `P01AC.predicates,
    `P01AC.fundamental, `P01AC.has_sound, `P01AC.form_sound,
    `P01AC.ExtensionalRepair.fundamental, `P01AC.ExtensionalRepair.unary_fundamental,
    `P01AC.ExtensionalRepair.has_sound, `P01AC.ExtensionalRepair.form_sound,
    `P01AC.EffectiveCompleteness.semantic_church_standardness,
    `P01AC.ExtensionalRepair.ClosedProofCanonicalisation.canonical_identity,
    `P01R.finite_fundamental]
  for n in excluded do
    if s.visited.contains n then
      throwError "Unexpected inherited semantic dependency: {n}"
    else
      logInfo m!"Excluded dependency: {n}"
  let required : Array Name := #[`FullPER.fundamental,
    `OpenTermStandardness.church_standard,
    `ClosedScalarInstances.generic_conversion_reflect,
    `P01AC.ExtensionalRepair.ClosedProofCanonicalisation.has_scope,
    `P01AC.Intensional.Plus.PolyConvPlus.bridge,
    `P01AC.ExtensionalRepair.HasE.conv,
    `P01AC.ExtensionalRepair.HasE.identityIntro,
    `P01AC.ExtensionalRepair.HasE.piIntro,
    `P01AC.ExtensionalRepair.HasE.allIntro]
  for n in required do
    if !s.visited.contains n then
      throwError "Missing expected constructive dependency: {n}"
    else
      logInfo m!"Required dependency: {n}"
  logInfo m!"Source-instance axiom dependencies: {s.axioms}"
