import IndependentBoundaries
import FiniteSidecarControls
import Lean
open Lean Elab Command

-- Value-only reachability does not traverse inductive metadata to unrelated constructors.
partial def auditValueDeps (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    if let some v := ci.value? true then
      for dep in v.getUsedConstants do
        auditValueDeps env dep

run_cmd do
  let env ← getEnv
  let positive := [``FiniteSidecar.table_typed, ``FiniteSidecar.table_observes,
    ``FiniteSidecar.controller_has, ``FiniteSidecar.controller_hasE,
    ``FiniteSidecar.controller_hasJ, ``FiniteSidecar.finite_controller_observes,
    ``FiniteSidecar.runSource_typed, ``FiniteSidecar.runSource_observes,
    ``FiniteSidecar.runCodes_bounded, ``FiniteSidecar.proof_slot_cannot_separate,
    ``FiniteSidecar.common_alphabet_attains,
    ``FiniteSidecar.Controls.four_required,
    ``FiniteSidecar.IndependentReview.empty_controller_defaults,
    ``FiniteSidecar.IndependentReview.escaping_observes]
  let bounded := [``FiniteSidecar.encoded_identity_iff,
    ``FiniteSidecar.finite_fibre_lower_bound, ``FiniteSidecar.common_alphabet_exact,
    ``FiniteSidecar.runSource_branch_identities,
    ``FiniteSidecar.IndependentReview.same_data_no_proof_observer]
  for target in positive ++ bounded do
    let (_, ax) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in ax.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    let visited := (auditValueDeps env target).run {} |>.snd
    if positive.contains target then
      for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
          ``P01AC.ExtensionalRepair.fundamental, ``P01AC.fundamental,
          ``HenkinSoundness.fundamental] do
        if visited.contains forbidden then
          throwError "Forbidden proof-value dependency in {target}: {forbidden}"
    if [``FiniteSidecar.controller_has, ``FiniteSidecar.controller_hasE,
        ``FiniteSidecar.controller_hasJ].contains target then
      for forbidden in [``JointCompletion.HasJ.natInduction, ``JointCompletion.HasJ.sigmaElim] do
        if visited.contains forbidden then
          throwError "Controller uses a completion constructor: {forbidden}"
    logInfo m!"PASS {target} allowed axioms and bounded value dependencies"
  let compiled := (auditValueDeps env ``FiniteSidecar.controller_has).run {} |>.snd
  unless compiled.contains ``P01AC.BooleanPrimitive.PR.compile_has do
    throwError "Missing original PR typing construction"
  let proofs := (auditValueDeps env ``FiniteSidecar.proof_slot_cannot_separate).run {} |>.snd
  for required in [``JointCompletion.ProofUniqueness.identity_proof_unique,
      ``JointCompletion.RecursorUniqueness.arrow_congr, ``JointCompletion.HasJ.j] do
    unless proofs.contains required do
      throwError "Missing inherited source proof-uniqueness/J path: {required}"
  logInfo "PASS actual compiler, proof uniqueness, and J paths"
  for n in env.header.moduleNames do
    let p ← findOLean n
    logInfo m!"IMPORT_OBJECT {n} {p}"
