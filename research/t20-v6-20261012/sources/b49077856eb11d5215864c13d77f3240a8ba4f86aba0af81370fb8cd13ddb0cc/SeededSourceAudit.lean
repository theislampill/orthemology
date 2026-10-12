import SeededSourceControls
import Lean
open Lean Elab Command

/-- Body-only traversal, credited to the retained FiniteRawObstruction dependency audit.
Inductive declaration types are deliberately terminal. -/
private def valueDependencies (env : Environment) (todo : List Name)
    (seen : NameSet) : Nat → Option NameSet
  | 0 => none
  | n + 1 => match todo with
    | [] => some seen
    | name :: rest =>
      if seen.contains name then valueDependencies env rest seen n
      else
        let more := match env.find? name with
          | some info => match info.value? true with
            | some e => e.getUsedConstants.toList
            | none => []
          | none => []
        valueDependencies env (more ++ rest) (seen.insert name) n

run_cmd do
  let env ← getEnv
  let targets := [``SeededSource.sampler_has, ``SeededSource.sampler_hasE,
    ``SeededSource.sampler_hasJ, ``SeededSource.cubePR_denote,
    ``SeededSource.sampler_observes, ``SeededSource.finite_sampler_observes,
    ``SeededSource.runSource_typed, ``SeededSource.runSource_observes,
    ``SeededSource.Controls.joint_counts, ``SeededSource.Controls.fixture_source_joint,
    ``SeededSource.Controls.fixture_source_history, ``SeededSource.Controls.fixture_closed]
  for target in targets do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
        ``P01AC.ExtensionalRepair.fundamental, ``P01AC.fundamental,
        ``JointCompletion.dependent_induction, ``JointCompletion.sigma_elimination,
        ``HenkinSoundness.fundamental] do
      if report.visited.contains forbidden then
        throwError "Forbidden semantic/completion dependency in {target}: {forbidden}"
    logInfo m!"PASS {target}: allowed standard axioms and source dependency boundary."
  let (_, typing) := ((Lean.CollectAxioms.collect ``SeededSource.sampler_has).run env).run {}
  unless typing.visited.contains ``P01AC.BooleanPrimitive.PR.compile_has do
    throwError "Missing actual original Has compiler."
  let some bodyDeps := valueDependencies env [``SeededSource.sampler_hasJ] {} 200000
    | throwError "Body traversal exhausted."
  for forbidden in [``JointCompletion.HasJ.natInduction, ``JointCompletion.HasJ.sigmaElim] do
    if bodyDeps.contains forbidden then
      throwError "Sampler construction uses completion constructor {forbidden}"
  unless bodyDeps.contains ``JointCompletion.HasJ.hasBase do
    throwError "Missing hasBase inclusion."
  logInfo "PASS original Has sampler is included into HasJ without a completion constructor."
  for moduleName in env.header.moduleNames do
    logInfo m!"IMPORTED {moduleName}"
