import FullPER
import Lean.Util.CollectAxioms

/- Environment inspection only: this command adds no axiom or mathematical theorem. -/
open Lean in
run_cmd do
  let env ← getEnv
  let (_, s) := ((Lean.CollectAxioms.collect `FullPER.has_sound).run env).run {}
  let excluded : Array Name := #[`P01AC.F, `P01AC.G, `P01AC.predicates,
    `P01AC.fundamental, `P01AC.has_sound, `P01AC.form_sound,
    `P01AC.ExtensionalRepair.fundamental, `P01AC.ExtensionalRepair.has_sound,
    `P01AC.ExtensionalRepair.form_sound, `P01R.finite_fundamental]
  for n in excluded do
    if s.visited.contains n then
      throwError "Inherited semantic dependency found: {n}"
    else
      logInfo m!"Excluded dependency: {n}"
  logInfo m!"Whole-model axiom dependencies: {s.axioms}"
