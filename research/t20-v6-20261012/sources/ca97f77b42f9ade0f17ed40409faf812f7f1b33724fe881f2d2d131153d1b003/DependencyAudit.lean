import Lean
import ComputationLaws
open Lean Elab Command
partial def initialityAncestors (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    for k in ci.getUsedConstantsAsSet.toList do initialityAncestors env k
run_cmd do
  let env ← getEnv
  for root in [`RigidityInitiality.dependent_action,
      `RigidityInitiality.dependent_action_converted_left,
      `RigidityInitiality.section_zero_law,
      `RigidityInitiality.section_successor_law] do
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
