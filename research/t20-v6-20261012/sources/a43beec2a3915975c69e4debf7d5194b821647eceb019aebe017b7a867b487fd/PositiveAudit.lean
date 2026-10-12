import PositiveTransfer
import Lean

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``RigidityInitiality.FullE.PositiveCompletion.section_implies_rigidE,
      ``RigidityInitiality.FullE.PositiveCompletion.induction_only_rigidity,
      ``RigidityInitiality.FullE.PositiveCompletion.induction_only_compiler_identity,
      ``P01AC.ExtensionalRepair.ExactScalarFusion.SelectiveCompletion.induction_only_fixed_scalar] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for forbidden in [``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction,
        ``CompletionIndependence.InductionModel.fundamental,
        ``FullPER.fundamental, ``HenkinSoundness.fundamental] do
      if report.visited.contains forbidden then
        throwError "Forbidden semantic dependency in {target}: {forbidden}"
    logInfo m!"PASS {target}: no semantic completion/fundamental theorem or new axiom; Sigma is disabled by the source judgment index."
