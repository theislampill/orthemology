/- Kernel type/value closure audit for the Boolean source extension. -/
import EffectiveBooleanInterfaces
import EffectiveBooleanControls
import verification.KernelAudit
open Lean Elab Command
namespace BooleanKernelAudit
open EffectiveKernelAudit

def authoredBoolean : Array Name := #[`P01AC.BooleanIdentity.B,
  `P01AC.BooleanIdentity.pick,
  `P01AC.BooleanIdentity.observe,
  `P01AC.BooleanIdentity.choiceLink,
  `P01AC.BooleanIdentity.choices_separate,
  `P01AC.BooleanIdentity.pick_conv_injective,
  `P01AC.BooleanIdentity.boolean_graph,
  `P01AC.BooleanIdentity.boolean_standardness,
  `P01AC.BooleanIdentity.boolean_same_choice_related,
  `P01AC.BooleanIdentity.boolean_observation,
  `P01AC.BooleanIdentity.boolean_related_iff_observation,
  `P01AC.BooleanIdentity.B_form,
  `P01AC.BooleanIdentity.unique_boolean,
  `P01AC.BooleanIdentity.CB,
  `P01AC.BooleanIdentity.BoolValid,
  `P01AC.BooleanIdentity.observationAt,
  `P01AC.BooleanIdentity.BoolTests,
  `P01AC.BooleanIdentity.output_self,
  `P01AC.BooleanIdentity.bool_valid_iff_tests,
  `P01AC.BooleanIdentity.Mismatch,
  `P01AC.BooleanIdentity.invalid_iff_mismatch,
  `P01AC.BooleanPrimitive.NatObs,
  `P01AC.BooleanPrimitive.NatObs.of_conv,
  `P01AC.BooleanPrimitive.canonical_obs,
  `P01AC.BooleanPrimitive.eval_closed,
  `P01AC.BooleanPrimitive.psub_closed,
  `P01AC.BooleanPrimitive.closed_has,
  `P01AC.BooleanPrimitive.N_subst,
  `P01AC.BooleanPrimitive.B_subst,
  `P01AC.BooleanPrimitive.S,
  `P01AC.BooleanPrimitive.S_form,
  `P01AC.BooleanPrimitive.succBody,
  `P01AC.BooleanPrimitive.succPoly,
  `P01AC.BooleanPrimitive.succ_has,
  `P01AC.BooleanPrimitive.succTerm,
  `P01AC.BooleanPrimitive.succ_application,
  `P01AC.BooleanPrimitive.succ_obs,
  `P01AC.BooleanPrimitive.NatCtx,
  `P01AC.BooleanPrimitive.natctx_formed,
  `P01AC.BooleanPrimitive.nat_lookup_eq,
  `P01AC.BooleanPrimitive.natvar,
  `P01AC.BooleanPrimitive.recImages,
  `P01AC.BooleanPrimitive.recStepBody,
  `P01AC.BooleanPrimitive.recStep,
  `P01AC.BooleanPrimitive.recPoly,
  `P01AC.BooleanPrimitive.recStep_has,
  `P01AC.BooleanPrimitive.recPoly_has,
  `P01AC.BooleanPrimitive.PR,
  `P01AC.BooleanPrimitive.PR.denote,
  `P01AC.BooleanPrimitive.PR.compile,
  `P01AC.BooleanPrimitive.PR.compile_has,
  `P01AC.BooleanPrimitive.recStep_application,
  `P01AC.BooleanPrimitive.EnvNat,
  `P01AC.BooleanPrimitive.recPoly_obs,
  `P01AC.BooleanPrimitive.PR.compile_obs,
  `P01AC.BooleanPrimitive.choicePoly,
  `P01AC.BooleanPrimitive.choiceTerm,
  `P01AC.BooleanPrimitive.choice_has,
  `P01AC.BooleanPrimitive.choice_application,
  `P01AC.BooleanPrimitive.discriminatorStep,
  `P01AC.BooleanPrimitive.discriminatorBody,
  `P01AC.BooleanPrimitive.zeroDiscriminator,
  `P01AC.BooleanPrimitive.discriminatorTerm,
  `P01AC.BooleanPrimitive.discriminator_has,
  `P01AC.BooleanPrimitive.discriminator_application,
  `P01AC.BooleanPrimitive.discriminator_obs,
  `P01AC.BooleanPrimitive.simulator,
  `P01AC.BooleanPrimitive.simFamily,
  `P01AC.BooleanPrimitive.constantChoice,
  `P01AC.BooleanPrimitive.inputs,
  `P01AC.BooleanPrimitive.simulator_has,
  `P01AC.BooleanPrimitive.simFamily_has,
  `P01AC.BooleanPrimitive.constantChoice_has,
  `P01AC.BooleanPrimitive.simFamily_obs,
  `P01AC.BooleanPrimitive.constantChoice_obs,
  `P01AC.BooleanPrimitive.sim_valid_iff_all_zero,
  `P01AC.BooleanIdentity.IdentityValid,
  `P01AC.BooleanIdentity.identity_valid_iff_endpoint_valid,
  `P01AC.BooleanIdentity.identity_unary_iff_endpoint_valid,
  `P01AC.BooleanIdentity.semantic_proof_exists_iff_valid,
  `P01AC.BooleanIdentity.current_identity_implies_valid,
  `P01AC.BooleanIdentity.identity_formed,
  `P01AC.BooleanIdentity.identity_invalid_iff_mismatch,
  `P01AC.BooleanIdentity.family_closed,
  `P01AC.BooleanIdentity.family_identity_formed,
  `P01AC.BooleanIdentity.family_identity_scope,
  `P01AC.BooleanIdentity.original_identity_iff_all_zero,
  `P01AC.BooleanIdentity.original_F_identity_iff_all_zero,
  `P01AC.BooleanIdentity.family_semantic_proof_exists_iff_all_zero,
  `P01AC.BooleanIdentity.current_family_identity_implies_all_zero,
  `P01AC.BooleanControls.plus,
  `P01AC.BooleanControls.trianglePlus,
  `P01AC.BooleanControls.firstInput,
  `P01AC.BooleanControls.always_zero_valid,
  `P01AC.BooleanControls.first_input_invalid,
  `P01AC.BooleanControls.explicit_mismatch,
  `P01AC.BooleanControls.zeroArityComposition,
  `P01AC.BooleanControls.parameterOverwrite]

def authoredBooleanTheorems : Array Name := #[`P01AC.BooleanIdentity.choices_separate,
  `P01AC.BooleanIdentity.pick_conv_injective,
  `P01AC.BooleanIdentity.boolean_graph,
  `P01AC.BooleanIdentity.boolean_standardness,
  `P01AC.BooleanIdentity.boolean_same_choice_related,
  `P01AC.BooleanIdentity.boolean_observation,
  `P01AC.BooleanIdentity.boolean_related_iff_observation,
  `P01AC.BooleanIdentity.B_form,
  `P01AC.BooleanIdentity.unique_boolean,
  `P01AC.BooleanIdentity.output_self,
  `P01AC.BooleanIdentity.bool_valid_iff_tests,
  `P01AC.BooleanIdentity.invalid_iff_mismatch,
  `P01AC.BooleanPrimitive.NatObs.of_conv,
  `P01AC.BooleanPrimitive.canonical_obs,
  `P01AC.BooleanPrimitive.eval_closed,
  `P01AC.BooleanPrimitive.psub_closed,
  `P01AC.BooleanPrimitive.closed_has,
  `P01AC.BooleanPrimitive.N_subst,
  `P01AC.BooleanPrimitive.B_subst,
  `P01AC.BooleanPrimitive.S_form,
  `P01AC.BooleanPrimitive.succ_has,
  `P01AC.BooleanPrimitive.succ_application,
  `P01AC.BooleanPrimitive.succ_obs,
  `P01AC.BooleanPrimitive.natctx_formed,
  `P01AC.BooleanPrimitive.nat_lookup_eq,
  `P01AC.BooleanPrimitive.natvar,
  `P01AC.BooleanPrimitive.recStep_has,
  `P01AC.BooleanPrimitive.recPoly_has,
  `P01AC.BooleanPrimitive.PR.compile_has,
  `P01AC.BooleanPrimitive.recStep_application,
  `P01AC.BooleanPrimitive.recPoly_obs,
  `P01AC.BooleanPrimitive.PR.compile_obs,
  `P01AC.BooleanPrimitive.choice_has,
  `P01AC.BooleanPrimitive.choice_application,
  `P01AC.BooleanPrimitive.discriminator_has,
  `P01AC.BooleanPrimitive.discriminator_application,
  `P01AC.BooleanPrimitive.discriminator_obs,
  `P01AC.BooleanPrimitive.simulator_has,
  `P01AC.BooleanPrimitive.simFamily_has,
  `P01AC.BooleanPrimitive.constantChoice_has,
  `P01AC.BooleanPrimitive.simFamily_obs,
  `P01AC.BooleanPrimitive.constantChoice_obs,
  `P01AC.BooleanPrimitive.sim_valid_iff_all_zero,
  `P01AC.BooleanIdentity.identity_valid_iff_endpoint_valid,
  `P01AC.BooleanIdentity.identity_unary_iff_endpoint_valid,
  `P01AC.BooleanIdentity.semantic_proof_exists_iff_valid,
  `P01AC.BooleanIdentity.current_identity_implies_valid,
  `P01AC.BooleanIdentity.identity_formed,
  `P01AC.BooleanIdentity.identity_invalid_iff_mismatch,
  `P01AC.BooleanIdentity.family_closed,
  `P01AC.BooleanIdentity.family_identity_formed,
  `P01AC.BooleanIdentity.family_identity_scope,
  `P01AC.BooleanIdentity.original_identity_iff_all_zero,
  `P01AC.BooleanIdentity.original_F_identity_iff_all_zero,
  `P01AC.BooleanIdentity.family_semantic_proof_exists_iff_all_zero,
  `P01AC.BooleanIdentity.current_family_identity_implies_all_zero,
  `P01AC.BooleanControls.always_zero_valid,
  `P01AC.BooleanControls.first_input_invalid,
  `P01AC.BooleanControls.explicit_mismatch]

elab "#audit_boolean_safe_closure " n:ident : command => do
  let (count, axes) ← auditClosure #[n.getId]
  logInfo m!"BOOLEAN_SAFE_CLOSURE_PASS {n.getId}; declarations={count}; axioms={axes}"

run_cmd do
  let env ← getEnv
  for n in authoredBoolean do
    let some info := env.checked.get.find? n | throwError "MISSING_BOOLEAN_DECLARATION {n}"
    if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_BOOLEAN_ROOT {n}"
  for n in authoredBooleanTheorems do
    let some info := env.checked.get.find? n | throwError "MISSING_BOOLEAN_THEOREM {n}"
    unless info.isTheorem do throwError "WRONG_BOOLEAN_THEOREM_KIND {n}"
  let mut allRoots : Array Name := #[]
  for ns in #[`P01AC.BooleanIdentity, `P01AC.BooleanPrimitive, `P01AC.BooleanControls] do
    let mut roots : Array Name := #[]
    let mut count := 0
    let mut theoremCount := 0
    let mut runtimeAuxiliaries := 0
    for (n, info) in env.constants.toList do
      if ns.isPrefixOf n then
        count := count + 1
        if info.isTheorem then theoremCount := theoremCount + 1
        if info.isUnsafe || info.isPartial then
          runtimeAuxiliaries := runtimeAuxiliaries + 1
          logInfo m!"BOOLEAN_NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
        else
          roots := roots.push n
          let axes ← Lean.collectAxioms n
          for a in axes do
            unless permittedAxioms.contains a do
              throwError "UNAPPROVED_BOOLEAN_COLLECTED_AXIOM {a} in {n}"
          logInfo m!"BOOLEAN_COMPILED_DECLARATION {n}; theorem={info.isTheorem}; axioms={axes}"
    let (reachable, axes) ← auditClosure roots
    logInfo m!"BOOLEAN_NAMESPACE_AUDIT_PASS {ns}; namespaceDeclarations={count}; namespaceTheorems={theoremCount}; safeRoots={roots.size}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"
    allRoots := allRoots ++ roots
  let (reachable, axes) ← auditClosure allRoots
  logInfo m!"BOOLEAN_KERNEL_AUDIT_PASS: authoredDeclarations={authoredBoolean.size}; authoredTheorems={authoredBooleanTheorems.size}; safeRoots={allRoots.size}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_boolean_safe_closure P01AC.BooleanIdentity.invalid_iff_mismatch
#audit_boolean_safe_closure P01AC.BooleanPrimitive.PR.compile_has
#audit_boolean_safe_closure P01AC.BooleanPrimitive.PR.compile_obs
#audit_boolean_safe_closure P01AC.BooleanIdentity.original_identity_iff_all_zero
#audit_boolean_safe_closure P01AC.BooleanIdentity.family_semantic_proof_exists_iff_all_zero
end BooleanKernelAudit
