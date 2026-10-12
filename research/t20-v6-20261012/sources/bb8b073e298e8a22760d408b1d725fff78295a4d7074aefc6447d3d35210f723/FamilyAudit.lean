import FamilyControls
open Lean in
run_cmd do
  let env ← getEnv
  let targets := #[`SourceFamilyComputability.encode_app,
    `SourceFamilyComputability.encode_pi, `SourceFamilyComputability.encode_identity,
    `SourceFamilyComputability.inputNumeral_succ,
    `SourceFamilyComputability.primrec_encode_programType,
    `SourceFamilyComputability.computable_encode_programType,
    `SourceFamilyComputability.codedHolds_not_re,
    `SourceFamilyComputability.codedFormedHolds_not_re,
    `SourceFamilyComputability.family_zero_ne_one]
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for target in targets do
    let (_, collected) := ((CollectAxioms.collect target).run env).run {}
    for ax in collected.axioms do
      unless allowed.contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"AUDIT {target}: {collected.axioms}"
  let executables := #[`SourceFamilyComputability.leaf, `SourceFamilyComputability.node,
    `SourceFamilyComputability.appCode, `SourceFamilyComputability.piCode,
    `SourceFamilyComputability.identityCode, `SourceFamilyComputability.numeralCode]
  for target in executables do
    let (_, collected) := ((CollectAxioms.collect target).run env).run {}
    for name in collected.visited do
      if let some info := env.find? name then
        if info.isUnsafe || info.isPartial then
          throwError "Unsafe or partial dependency {name} in {target}"
    logInfo m!"EXECUTABLE {target}: no unsafe or partial dependencies"
