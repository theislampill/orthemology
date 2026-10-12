import TransformControls
import TypeScopeControls
import TermTypeControls
open Lean in
run_cmd do
  let env ← getEnv
  let targets := #[`CodedPolyTransformations.primrec_abstractCode,
    `CodedPolyTransformations.abstractCode_exact, `CodedPolyTransformations.primrec_substituteCode,
    `CodedPolyTransformations.substituteCode_exact, `CodedPolyTransformations.finiteEnv_pup,
    `CodedPolyTransformations.primrec_liftEnvCode, `CodedPolyTransformations.lifted_substituteCode_exact,
    `CodedPolyTransformations.primrec_checkTyScope, `CodedPolyTransformations.checkTyScope_exact,
    `CodedPolyTransformations.primrec_substTyCode, `CodedPolyTransformations.substTyCode_exact,
    `CodedPolyTransformations.instTyCode_exact, `CodedPolyTransformations.wkTyCode_exact]
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for target in targets do
    let (_, collected) := ((CollectAxioms.collect target).run env).run {}
    for ax in collected.axioms do
      unless allowed.contains ax do throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"AUDIT {target}: {collected.axioms}"
