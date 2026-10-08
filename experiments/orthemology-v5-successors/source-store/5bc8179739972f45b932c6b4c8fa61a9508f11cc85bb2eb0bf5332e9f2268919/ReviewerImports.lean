import RationalFixtures
open Lean Elab Command
run_cmd do
  for name in (← getEnv).header.moduleNames do
    logInfo m!"REVIEW_IMPORT {name}"
