import AuxiliaryCodeCore
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (n, _) in env.constants.toList do
    if ("encodableStepCert".isPrefixOf (n.getString!)) || (n.getString! == "encode") then
      logInfo m!"{n}"
