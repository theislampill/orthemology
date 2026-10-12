import ProofUniquenessControls
import Lean
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let positive := [``JointCompletion.ProofUniqueness.canonical_identity,
    ``JointCompletion.ProofUniqueness.identity_contract,
    ``JointCompletion.ProofUniqueness.identity_proof_unique,
    ``P01AC.ExtensionalRepair.ProofUniqueness.canonical_identity,
    ``P01AC.ExtensionalRepair.ProofUniqueness.identity_contract,
    ``P01AC.ExtensionalRepair.ProofUniqueness.identity_proof_unique,
    ``JointCompletion.ProofUniqueness.Controls.original_bound_proofs_identical,
    ``JointCompletion.ProofUniqueness.Controls.new_bound_proofs_identical,
    ``JointCompletion.ProofUniqueness.Controls.typed_observer_constant,
    ``JointCompletion.ProofUniqueness.Controls.labelled_has]
  let negative := [``JointCompletion.ProofUniqueness.Controls.bound_proofs_not_raw,
    ``JointCompletion.ProofUniqueness.Controls.new_carrier_not_old,
    ``JointCompletion.ProofUniqueness.Controls.numeric_observer_same_count,
    ``JointCompletion.ProofUniqueness.Controls.distinct_labels_not_identical]
  for target in positive ++ negative do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    if positive.contains target then
      for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
          ``P01AC.ExtensionalRepair.fundamental,
          ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction,
          ``HenkinSoundness.fundamental] do
        if report.visited.contains forbidden then
          throwError "Semantic shortcut in source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: dependency boundary checked."
  for target in [``JointCompletion.ProofUniqueness.identity_contract,
      ``P01AC.ExtensionalRepair.ProofUniqueness.identity_contract] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    unless report.visited.contains ``JointCompletion.HasJ.j ||
        report.visited.contains ``P01AC.ExtensionalRepair.HasE.j do
      throwError "Missing source J dependence in {target}"
  logInfo "PASS: source proof contraction uses actual J."

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for moduleName in env.header.moduleNames do
    logInfo m!"IMPORTED {moduleName}"
