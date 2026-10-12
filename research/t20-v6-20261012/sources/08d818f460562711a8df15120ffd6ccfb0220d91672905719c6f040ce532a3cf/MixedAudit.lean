import MixedControls
open Lean in
run_cmd do
  let env ← getEnv
  let targets := #[`CodedMixedTransformations.primrec_mixedCode,
    `CodedMixedTransformations.mixedCode_exact, `CodedMixedTransformations.tinstCode_exact,
    `CodedMixedTransformations.tsubstImagesCode_exact, `CodedMixedTransformations.primrec_twkCode,
    `CodedMixedTransformations.twkCode_exact, `CodedMixedTransformations.primrec_instantiateTypeCode,
    `CodedMixedTransformations.instantiateTypeCode_exact, `CodedMixedTransformations.primrec_finCode,
    `CodedMixedTransformations.finCode_exact, `CodedMixedTransformations.primrec_finSupportCode,
    `CodedMixedTransformations.finSupportCode_exact]
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for target in targets do
    let (_, collected) := ((CollectAxioms.collect target).run env).run {}
    for ax in collected.axioms do
      unless allowed.contains ax do throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"AUDIT {target}: {collected.axioms}"
