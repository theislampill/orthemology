import Lean
import SourceUniqueness
open Lean Elab Command
partial def initialityAncestors (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    for k in ci.getUsedConstantsAsSet.toList do initialityAncestors env k
run_cmd do
  let env ← getEnv
  for root in [`RigidityInitiality.rec_family_form,
      `RigidityInitiality.rec_zero_seed, `RigidityInitiality.rec_step_point,
      `RigidityInitiality.rec_total_step_has, `RigidityInitiality.recursor_unique_source,
      `RigidityInitiality.section_application_beta] do
    let (_, names) := (initialityAncestors env root).run {}
    logInfo m!"ANCESTORS {root}: {names.toList}"
    let bad := names.toList.filter fun n =>
      n.toString.startsWith "FullPER." ||
      n.toString.startsWith "HomogeneousOriginal" ||
      n.toString.startsWith "GenericFoldTransport." ||
      n.toString.startsWith "RigidityDiscriminator." ||
      n.toString == "SourceFoldContract.SourceNaturality" ||
      n.toString.startsWith "SourceRigidity.q_"
    unless bad.isEmpty do throwError m!"Forbidden source theorem ancestry: {bad}"
    logInfo m!"PASS source-only ancestry for {root}"
