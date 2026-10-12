import Lean
import UniquenessIndependence
open Lean Elab Command
partial def initialityAncestors (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    for k in ci.getUsedConstantsAsSet.toList do initialityAncestors env k
run_cmd do
  let env ← getEnv
  for root in [`RigidityInitiality.appE_arrow, `RigidityInitiality.composeE] do
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

run_cmd do
  let env ← getEnv
  for (root, required) in [(`RigidityInitiality.internal_uniqueness_uninhabited,
      `RigidityDiscriminator.rigidity_uninhabited),
      (`RigidityInitiality.internal_uniqueness_negation_uninhabited,
      `RigidityDiscriminator.no_internal_negation)] do
    let (_, names) := (initialityAncestors env root).run {}
    unless names.contains required do throwError m!"Missing transfer ancestry {required}"
    logInfo m!"PASS exact independence transfer {root} through {required}"
