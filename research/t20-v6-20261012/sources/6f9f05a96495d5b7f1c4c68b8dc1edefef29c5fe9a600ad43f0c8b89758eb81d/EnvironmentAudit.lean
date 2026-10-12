import ZeroOnlyControl
import Lean
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for n in env.header.moduleNames do
    let p ← findOLean n
    logInfo m!"IMPORT_OBJECT {n} {p}"
