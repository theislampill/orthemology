import BridgeControls
open Lean Elab Command
run_cmd do
  for name in (← getEnv).header.moduleNames do
    logInfo m!"KERNEL_IMPORT {name}"
