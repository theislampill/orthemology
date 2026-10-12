import Lean
import Application

/- Kernel-environment dependency audit. This command checks proof dependencies;
   it contributes no axiom or theorem to the model. -/
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let blocked := [``P01AC.F, ``P01AC.G, ``P01AC.predicates,
    ``P01R.finite_fundamental,
    ``P01AC.form_sound, ``P01AC.has_sound, ``P01AC.fundamental,
    ``P01AC.ExtensionalRepair.form_sound,
    ``P01AC.ExtensionalRepair.has_sound,
    ``P01AC.ExtensionalRepair.fundamental,
    ``P01AC.ExtensionalRepair.unary_fundamental]
  for target in [``FullPER.form_sound, ``FullPER.has_sound,
      ``FullPER.fundamental, ``FullPER.formation_coherent,
      ``FullPER.Application.no_closed_bottom,
      ``FullPER.Application.scalar_target_valid] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for old in blocked do
      if state.visited.contains old then
        throwError "Forbidden inherited F/G dependency {old} in {target}"
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS: {target}; no inherited F/G interpretation or soundness dependency; axioms {state.axioms}"

#check @FullPER.fundamental
#check @FullPER.formation_per
#check @FullPER.formation_coherent
#check @FullPER.Application.scalar_target_fundamental
