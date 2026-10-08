import ExtensionalRepairTheorems
import Lean.Util.CollectAxioms
import Lean.Elab.Command
open Lean Elab Command

/- Every actual compiled declaration in the fresh namespace is audited.
   Constants include definitions, constructors, recursors and theorems; the
   counts are kept separate instead of calling all constants theorems. -/
run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let mut constants := 0
  let mut theorems := 0
  for (n, info) in env.constants.toList do
    if `P01AC.ExtensionalRepair |>.isPrefixOf n then
      constants := constants + 1
      if info.isTheorem then theorems := theorems + 1
      let axs ← Lean.collectAxioms n
      for a in axs do
        unless allowed.contains a do throwError "Unapproved axiom {a} in {n}"
      logInfo m!"DECLARATION {n}; theorem={info.isTheorem}; axioms={axs}"
  unless constants == 156 do
    throwError "Expected exactly 156 frozen namespace declarations, got {constants}"
  logInfo m!"COMBINED_AXIOM_AUDIT_PASS: constants={constants}; theorems={theorems}"

run_cmd do
  let decisive : Array Name := #[
    `P01AC.Intensional.separation_no_has,
    `P01AC.Intensional.separation_no_hasPlus,
    `P01AC.Intensional.closed_typed_identity_iff,
    `P01AC.ExtensionalRepair.has_sound,
    `P01AC.ExtensionalRepair.form_sound,
    `P01AC.ExtensionalRepair.context_sound,
    `P01AC.ExtensionalRepair.pointwise_evidence_has,
    `P01AC.ExtensionalRepair.separation_has,
    `P01AC.ExtensionalRepair.closed_raw_identity_conversion,
    `P01AC.ExtensionalRepair.raw_separation_no_has,
    `P01AC.ExtensionalRepair.strict_typed_identity_extension]
  for n in decisive do
    unless (← getConstInfo n).isTheorem do throwError "Expected a theorem: {n}"
  logInfo "DECISIVE_THEOREM_KIND_PASS: 11 actual theorem declarations"
