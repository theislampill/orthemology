import Lean
import RigidityDiscriminator
open Lean Elab Command
partial def ancestors (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    for k in ci.getUsedConstantsAsSet.toList do
      ancestors env k
run_cmd do
  let env ← getEnv
  for root in [`RigidityDiscriminator.peano_rigidity, `RigidityDiscriminator.rigidity_valid,
      `RigidityDiscriminator.rigidity_uninhabited] do
    let (_, names) := (ancestors env root).run {}
    logInfo m!"ANCESTORS {root}: {names.toList}"
    if root != `RigidityDiscriminator.rigidity_uninhabited then
      let bad := names.toList.filter fun n =>
        n.toString.startsWith "HomogeneousOriginal" ||
        n.toString == "FullPER.Application.original_endpoints" ||
        n.toString == "FullPER.Application.originalIdentity_valid" ||
        n.toString.startsWith "SourceFoldContract" ||
        n.toString.startsWith "SourceRigidity.q_"
      unless bad.isEmpty do throwError m!"Forbidden semantic ancestry: {bad}"
      logInfo m!"PASS generic semantic ancestry for {root}"
