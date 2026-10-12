import FamilyAudit
open Lean in
run_cmd do
  let env ← getEnv
  for name in env.header.moduleNames do
    logInfo m!"DEPENDENCY {name}"
