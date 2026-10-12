import ZeroOnlyControl
import Lean
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for m in env.header.moduleNames do
    logInfo m!"PRESERVE_IMPORT {m}"
