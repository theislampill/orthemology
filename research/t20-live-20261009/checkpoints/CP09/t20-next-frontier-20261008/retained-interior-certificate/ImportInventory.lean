import Mathlib.Data.Fintype.Card
import Mathlib.Order.Monotone.Basic
import Lean.Elab.Tactic.Omega

run_cmd do
  for n in (← Lean.getEnv).header.moduleNames do
    Lean.logInfo s!"IMPORT {n}"
