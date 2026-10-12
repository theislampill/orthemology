import Lean
import UniformSection
open Lean Elab Command
partial def initialityAncestors (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    for k in ci.getUsedConstantsAsSet.toList do initialityAncestors env k
run_cmd do
  let env ← getEnv
  for root in [`RigidityInitiality.dependent_section_from_rigidity,
      `RigidityInitiality.dependent_section_explicit,
      `RigidityInitiality.dependent_section_curried,
      `RigidityInitiality.section_has, `RigidityInitiality.rigidity_implies_section] do
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
