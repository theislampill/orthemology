import ScopeControls
open Lean in
run_cmd do
  let env ← getEnv
  let targets := #[`CodedScope.primrec_checkScope, `CodedScope.computable_checkScope,
    `CodedScope.checkScope_exact, `CodedScope.no_poly_encodes_zero]
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for target in targets do
    let (_, collected) := ((CollectAxioms.collect target).run env).run {}
    for ax in collected.axioms do
      unless allowed.contains ax do throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"AUDIT {target}: {collected.axioms}"
