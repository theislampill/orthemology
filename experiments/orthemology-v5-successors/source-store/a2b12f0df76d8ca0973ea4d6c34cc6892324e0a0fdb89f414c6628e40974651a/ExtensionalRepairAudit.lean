import ExtensionalRepairTheorems
import Lean.Util.CollectAxioms
import Lean.Elab.Command

open Lean Elab Command
set_option pp.fullNames true

/- Counts inspect actual compiled inductive declarations, not textual estimates. -/
run_cmd do
  let counts : Array (Name × Nat) := #[
    (`P01AC.Ctx, 2), (`P01AC.Form, 7), (`P01AC.Has, 18),
    (`P01AC.Intensional.Plus.CtxPlus, 2), (`P01AC.Intensional.Plus.FormPlus, 7),
    (`P01AC.Intensional.Plus.HasPlus, 18),
    (`P01AC.ExtensionalRepair.CtxE, 2), (`P01AC.ExtensionalRepair.FormE, 7),
    (`P01AC.ExtensionalRepair.HasE, 20),
    (`P01DF.PolyConv, 7), (`P01AC.Intensional.Plus.PolyConvPlus, 8)]
  for (n, expected) in counts do
    let .inductInfo v ← getConstInfo n | throwError "Not an inductive: {n}"
    unless v.ctors.length == expected do
      throwError "Wrong constructor count for {n}: {v.ctors.length}"
    logInfo m!"CONSTRUCTOR_COUNT {n} = {v.ctors.length}\nCONSTRUCTORS {v.ctors}"

/- The source schemas, their conclusions, and key dependent helper signatures. -/
run_cmd do
  let checks : Array Name := #[
    `P01AC.ExtensionalRepair.HasE.piExt,
    `P01AC.ExtensionalRepair.HasE.allExt,
    `P01AC.ExtensionalRepair.schema_pi_body_instantiate_shift,
    `P01AC.ExtensionalRepair.schema_eval_application,
    `P01AC.ExtensionalRepair.schema_pi_types_scoped,
    `P01AC.ExtensionalRepair.fundamental_identity_intro_plus,
    `P01AC.ExtensionalRepair.fundamental_pi_ext,
    `P01AC.ExtensionalRepair.fundamental_all_ext,
    `P01AC.ExtensionalRepair.context_sound,
    `P01AC.ExtensionalRepair.form_sound,
    `P01AC.ExtensionalRepair.has_sound,
    `P01AC.ExtensionalRepair.fundamental,
    `P01AC.ExtensionalRepair.unary_fundamental,
    `P01AC.ExtensionalRepair.strong_diagonal,
    `P01AC.ExtensionalRepair.two_sided_invariance,
    `P01AC.ExtensionalRepair.plus_ctx_inclusion,
    `P01AC.ExtensionalRepair.plus_form_inclusion,
    `P01AC.ExtensionalRepair.plus_has_inclusion,
    `P01AC.ExtensionalRepair.ctx_inclusion,
    `P01AC.ExtensionalRepair.form_inclusion,
    `P01AC.ExtensionalRepair.has_inclusion,
    `P01AC.ExtensionalRepair.pointwise_conversion,
    `P01AC.ExtensionalRepair.bracket_I_exact,
    `P01AC.ExtensionalRepair.pointwise_evidence_has,
    `P01AC.ExtensionalRepair.arrow_identity_has,
    `P01AC.ExtensionalRepair.separation_has,
    `P01AC.ExtensionalRepair.closed_raw_identity_conversion,
    `P01AC.ExtensionalRepair.raw_separation_form,
    `P01AC.ExtensionalRepair.raw_separation_no_has,
    `P01AC.ExtensionalRepair.separation_not_polyConvPlus,
    `P01AC.ExtensionalRepair.preserved_old_noninhabitation,
    `P01AC.ExtensionalRepair.strict_typed_identity_extension,
    `P01AC.ExtensionalRepair.separation_proof_erases,
    `P01AC.Intensional.separation_no_has,
    `P01AC.Intensional.separation_no_hasPlus]
  for n in checks do
    let info ← getConstInfo n
    logInfo m!"DECLARATION {n}\nTYPE {info.type}"

/- Audit every declaration belonging to the new namespace, including helpers
   and generated recursors, transitively. Only ordinary Lean foundations pass. -/
run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let mut checked := 0
  for (n, _) in env.constants.toList do
    if `P01AC.ExtensionalRepair |>.isPrefixOf n then
      let axs ← Lean.collectAxioms n
      for a in axs do
        unless allowed.contains a do
          throwError "Unapproved transitive axiom {a} in {n}"
      checked := checked + 1
      logInfo m!"TRANSITIVE_AXIOMS {n}: {axs}"
  unless checked > 50 do
    throwError "Unexpectedly incomplete namespace audit: {checked} declarations"
  logInfo m!"AUDIT_PASS: {checked} namespace declarations transitively checked; no sorryAx or new assumptions."
