import IndependentChecks
import Lean
open Lean Elab Command in
run_cmd do
  for n in (← getEnv).header.moduleNames do
    logInfo m!"PRESERVE_IMPORT {n}"
