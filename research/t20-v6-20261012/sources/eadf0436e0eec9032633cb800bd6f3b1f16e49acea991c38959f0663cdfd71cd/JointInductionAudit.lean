import JointInductionControls
import JointInductionRawBoundary
import Lean

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let positive := [``JointCompletion.InductionComputation.rigidity_in_context,
    ``JointCompletion.InductionComputation.induction_section,
    ``JointCompletion.InductionComputation.induction_value,
    ``JointCompletion.InductionComputation.induction_zero,
    ``JointCompletion.InductionComputation.induction_successor,
    ``JointCompletion.InductionComputation.comparison_formed,
    ``JointCompletion.InductionComputation.induction_extensionality,
    ``JointCompletion.InductionComputation.Controls.new_family_section,
    ``JointCompletion.InductionComputation.Controls.new_family_zero,
    ``JointCompletion.InductionComputation.Controls.new_family_successor,
    ``JointCompletion.InductionComputation.RawBoundary.successor_typed_identity]
  let negative := [``JointCompletion.InductionComputation.Controls.family_not_old,
    ``JointCompletion.InductionComputation.Controls.seed_not_old,
    ``JointCompletion.InductionComputation.Controls.step_not_old,
    ``JointCompletion.InductionComputation.RawBoundary.successor_not_raw]
  for target in positive ++ negative do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    if positive.contains target then
      for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
          ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction,
          ``CompletionIndependence.InductionModel.fundamental,
          ``HenkinSoundness.fundamental] do
        if report.visited.contains forbidden then
          throwError "Semantic shortcut in source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: allowed axioms and declared source/negative scope."
