import JointRecursorControls
import Lean

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let positive := [``JointCompletion.RecursorUniqueness.arrow_congr,
    ``JointCompletion.RecursorUniqueness.comparison_at,
    ``JointCompletion.RecursorUniqueness.successor_law_at,
    ``JointCompletion.RecursorUniqueness.section_value,
    ``JointCompletion.RecursorUniqueness.dependent_step_congr,
    ``JointCompletion.RecursorUniqueness.section_at_variable,
    ``JointCompletion.RecursorUniqueness.compare_algebra_values,
    ``JointCompletion.RecursorUniqueness.comparison_seed,
    ``JointCompletion.RecursorUniqueness.comparison_step,
    ``JointCompletion.RecursorUniqueness.recursor_unique,
    ``JointCompletion.RecursorUniqueness.recursor_unique_generic_laws,
    ``JointCompletion.RecursorUniqueness.shifted_successor_at_variable,
    ``JointCompletion.RecursorUniqueness.successor_law_formed,
    ``JointCompletion.RecursorUniqueness.canonical_successor_laws,
    ``JointCompletion.RecursorUniqueness.unique_to_canonical,
    ``JointCompletion.RecursorUniqueness.Controls.direct_zero,
    ``JointCompletion.RecursorUniqueness.Controls.direct_successor_laws,
    ``JointCompletion.RecursorUniqueness.Controls.new_family_uniqueness,
    ``JointCompletion.RecursorUniqueness.Controls.new_family_varies]
  let negative := [``JointCompletion.RecursorUniqueness.Controls.new_family_not_old,
    ``JointCompletion.RecursorUniqueness.Controls.no_old_seed,
    ``JointCompletion.RecursorUniqueness.Controls.no_old_step]
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
          throwError "Semantic shortcut in positive source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: allowed axioms and source/negative scope."
  let (_, congruence) := ((Lean.CollectAxioms.collect ``JointCompletion.RecursorUniqueness.arrow_congr).run env).run {}
  unless congruence.visited.contains ``JointCompletion.HasJ.j do
    throwError "Missing actual source J in congruence."
  let (_, step) := ((Lean.CollectAxioms.collect ``JointCompletion.RecursorUniqueness.comparison_step).run env).run {}
  unless step.visited.contains ``JointCompletion.RecursorUniqueness.arrow_congr do
    throwError "Comparison step did not use common-operation congruence."
  let (_, unique) := ((Lean.CollectAxioms.collect ``JointCompletion.RecursorUniqueness.recursor_unique).run env).run {}
  for required in [``JointCompletion.HasJ.natInduction, ``JointCompletion.HasJ.piExt,
      ``JointCompletion.RecursorUniqueness.comparison_seed,
      ``JointCompletion.RecursorUniqueness.comparison_step] do
    unless unique.visited.contains required do
      throwError "Missing required source construction in uniqueness: {required}"
  logInfo "PASS actual-source constructor and comparison-congruence dependency controls."
