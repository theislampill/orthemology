import FiniteSidecarControls
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
  let constructive := [``FiniteSidecar.table_typed, ``FiniteSidecar.table_observes,
    ``FiniteSidecar.controller_hasE, ``FiniteSidecar.controller_hasJ,
    ``FiniteSidecar.finite_controller_observes, ``FiniteSidecar.runSource_typed,
    ``FiniteSidecar.runSource_observes, ``FiniteSidecar.runCodes_bounded,
    ``FiniteSidecar.proof_slot_cannot_separate, ``FiniteSidecar.common_alphabet_attains]
  let separation := [``FiniteSidecar.encoded_identity_iff,
    ``FiniteSidecar.finite_fibre_lower_bound, ``FiniteSidecar.common_alphabet_exact,
    ``FiniteSidecar.runSource_branch_identities, ``FiniteSidecar.Controls.four_required,
    ``FiniteSidecar.Controls.two_tags_cannot_hide_four]
  for target in constructive ++ separation do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    if constructive.contains target then
      for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
          ``P01AC.ExtensionalRepair.fundamental, ``P01AC.fundamental,
          ``JointCompletion.dependent_induction, ``JointCompletion.sigma_elimination,
          ``HenkinSoundness.fundamental] do
        if report.visited.contains forbidden then
          throwError "Forbidden semantic/completion dependency in {target}: {forbidden}"
    logInfo m!"PASS {target}: dependency boundary checked."
  let (_, typing) := ((Lean.CollectAxioms.collect ``FiniteSidecar.controller_hasE).run env).run {}
  unless typing.visited.contains ``P01AC.BooleanPrimitive.PR.compile_has do
    throwError "Controller did not use the actual existing typed PR compiler."
  let (_, erasure) := ((Lean.CollectAxioms.collect ``FiniteSidecar.proof_slot_cannot_separate).run env).run {}
  unless erasure.visited.contains ``JointCompletion.HasJ.j do
    throwError "Proof-slot boundary did not use actual source J."
  let some bodyDeps := valueDependencies env [``FiniteSidecar.controller_hasJ] {} 200000
    | throwError "Declaration-body traversal exhausted its bound."
  for forbidden in [``JointCompletion.HasJ.natInduction, ``JointCompletion.HasJ.sigmaElim] do
    if bodyDeps.contains forbidden then
      throwError "Controller construction uses a completion rule: {forbidden}"
  unless bodyDeps.contains ``JointCompletion.HasJ.hasBase do
    throwError "Missing original-source inclusion into Joint."
  logInfo "PASS: original typed compiler; controller hasBase inclusion uses no completion constructor; proof-slot equality uses source J."
  for moduleName in env.header.moduleNames do
    logInfo m!"IMPORTED {moduleName}"
