import Lean
import OpenDevelopments
import ScalarCertificates
import NonstandardRejection
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for target in [``OpenDevelopments.development_complete,
      ``OpenDevelopments.closed_HasE_development_terminates,
      ``OpenDevelopments.extractIteration,
      ``OpenDevelopments.extractIteration_uniform,
      ``ScalarCertificates.checkedScalar,
      ``ScalarCertificates.checkedIteration,
      ``ScalarCertificates.checkedSourceInstance,
      ``NonstandardRejection.checked_non_iteration_refutes] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS allowed axioms for {target}: {state.axioms}"
  let (_, strategy) := ((Lean.CollectAxioms.collect ``OpenDevelopments.development_complete).run env).run {}
  for forbidden in [``FullPER.fundamental, ``OpenTermStandardness.church_standard,
      ``P01Candidates.finite_SN, ``ClosedScalarInstances.closed_scalar_instance_exact] do
    if strategy.visited.contains forbidden then
      throwError "Open strategy unexpectedly depends on {forbidden}"
  for needed in [``OpenDevelopments.par_develop, ``OpenDevelopments.conv_chain] do
    unless strategy.visited.contains needed do throwError "Strategy omitted {needed}"
  let (_, extract) := ((Lean.CollectAxioms.collect ``OpenDevelopments.extractIteration).run env).run {}
  for needed in [``Nat.find, ``OpenDevelopments.readIteration, ``OpenDevelopments.run,
      ``OpenDevelopments.closed_HasE_readback_exists,
      ``ClosedScalarInstances.generic_conversion_reflect] do
    unless extract.visited.contains needed do throwError "Extractor omitted {needed}"
  let (_, certificate) := ((Lean.CollectAxioms.collect ``ScalarCertificates.checkedSourceInstance).run env).run {}
  for forbidden in [``FullPER.fundamental, ``OpenTermStandardness.church_standard,
      ``ClosedScalarInstances.source_uniform_iteration,
      ``ClosedScalarInstances.closed_scalar_conversion,
      ``ClosedScalarInstances.closed_scalar_instance,
      ``ClosedScalarInstances.closed_scalar_instance_exact,
      ``OpenDevelopments.extractIteration, ``Classical.choice] do
    if certificate.visited.contains forbidden then
      throwError "Finite certificate path unexpectedly depends on {forbidden}"
  for needed in [``ScalarCertificates.replayTo, ``ScalarCertificates.replay,
      ``ScalarCertificates.stepAt, ``ScalarCertificates.root,
      ``ClosedScalarInstances.generic_conversion_reflect,
      ``P01AC.ExtensionalRepair.HasE.conv,
      ``P01AC.ExtensionalRepair.HasE.identityIntro,
      ``P01AC.ExtensionalRepair.HasE.piIntro,
      ``P01AC.ExtensionalRepair.HasE.allIntro] do
    unless certificate.visited.contains needed do throwError "Certificate omitted {needed}"
  let (_, rejection) := ((Lean.CollectAxioms.collect ``NonstandardRejection.checked_non_iteration_refutes).run env).run {}
  for needed in [``ScalarCertificates.replayTo, ``NonstandardRejection.normalB_sound,
      ``OpenDevelopments.normal_unique, ``ClosedScalarInstances.source_uniform_iteration] do
    unless rejection.visited.contains needed do throwError "Negative certificate omitted {needed}"
  logInfo "PASS: strategy is triangle/cofinality; executable search uses Nat.find; certificate source replay is independent of semantic standardness and the closed-instance theorem."
