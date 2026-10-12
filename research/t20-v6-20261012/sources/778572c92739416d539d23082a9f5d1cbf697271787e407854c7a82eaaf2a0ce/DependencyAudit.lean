import Lean
import ClosedScalarInstances

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let blocked := [``P01AC.F, ``P01AC.G, ``P01AC.predicates,
    ``P01R.finite_fundamental,
    ``P01AC.form_sound, ``P01AC.has_sound, ``P01AC.fundamental,
    ``P01AC.ExtensionalRepair.form_sound,
    ``P01AC.ExtensionalRepair.has_sound,
    ``P01AC.ExtensionalRepair.fundamental,
    ``P01AC.ExtensionalRepair.unary_fundamental,
    ``P01AC.EffectiveCompleteness.semantic_church_standardness,
    ``P01AC.ExtensionalRepair.ClosedProofCanonicalisation.proof_raw_conversion,
    ``P01AC.ExtensionalRepair.ClosedProofCanonicalisation.canonical_identity,
    ``P01AC.ExtensionalRepair.ExactScalarFusion.forward_fixed]
  for target in [``ClosedScalarInstances.generic_conversion_reflect,
      ``ClosedScalarInstances.source_uniform_iteration,
      ``ClosedScalarInstances.closed_scalar_conversion,
      ``ClosedScalarInstances.scalar_endpoints,
      ``ClosedScalarInstances.scalar_identity,
      ``ClosedScalarInstances.closed_scalar_instance,
      ``ClosedScalarInstances.closed_scalar_instance_exact] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for old in blocked do
      if state.visited.contains old then
        throwError "Forbidden inherited semantic/canonicalisation dependency {old} in {target}"
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    if target != ``ClosedScalarInstances.generic_conversion_reflect then
      unless state.visited.contains ``FullPER.fundamental do
        throwError "Missing actual new full-PER soundness dependency in {target}"
    logInfo m!"PASS {target}: no inherited F/G, old standardness, proof canonicalisation or conditional forward dependency; axioms {state.axioms}"
  let (_, finalState) := ((Lean.CollectAxioms.collect
    ``ClosedScalarInstances.closed_scalar_instance_exact).run env).run {}
  for required in [``P01AC.ExtensionalRepair.ClosedProofCanonicalisation.has_scope,
      ``P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed,
      ``ClosedScalarInstances.generic_conversion_reflect,
      ``OpenTermStandardness.church_standard,
      ``P01AC.ExtensionalRepair.HasE.conv,
      ``P01AC.ExtensionalRepair.HasE.identityIntro,
      ``P01AC.ExtensionalRepair.HasE.piIntro,
      ``P01AC.ExtensionalRepair.HasE.allIntro] do
    unless finalState.visited.contains required do
      throwError "Missing required dependency {required}"
  logInfo "PASS: final source derivability consumes actual scope, formation, open standardness, reification, and original HasE rules."

#check @ClosedScalarInstances.source_uniform_iteration
#check @ClosedScalarInstances.closed_scalar_instance_exact
