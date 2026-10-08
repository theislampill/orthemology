/- Inspect the checked compiled environment, not source words or compiler IR.
   Reachability follows types and kernel values. Mutual-block metadata, native
   compiler replacement tables, and similarly named compiler auxiliaries are
   deliberately not treated as proof dependencies. -/
import EffectiveRuleBoundary
import Lean.Util.CollectAxioms
import Lean.Elab.Command

open Lean Elab Command
namespace EffectiveKernelAudit

def permittedAxioms : Array Name := #[`propext, `Classical.choice, `Quot.sound]

/-- Bounded work-list traversal. Exhausting the generous fuel is an audit error,
    never a successful incomplete result. The checker itself is not a proof root. -/
def auditClosure (roots : Array Name) : CommandElabM (Nat × Array Name) := do
  let env ← getEnv
  let mut todo := roots.toList
  let mut seen : NameSet := {}
  let mut axes : Array Name := #[]
  let mut count := 0
  let mut opaques : Array Name := #[]
  for _ in [:200000] do
    match todo with
    | [] => break
    | n :: tail =>
      todo := tail
      unless seen.contains n do
        seen := seen.insert n
        count := count + 1
        let info ← match env.checked.get.find? n with
          | some info => pure info
          | none => throwError "MISSING_CHECKED_DECLARATION {n}"
        if info.isUnsafe then throwError "UNSAFE_KERNEL_DEPENDENCY {n}"
        if info.isPartial then throwError "PARTIAL_KERNEL_DEPENDENCY {n}"
        if info.isAxiom then
          unless permittedAxioms.contains n do
            throwError "UNAPPROVED_KERNEL_AXIOM {n}"
          axes := axes.push n
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then
          todo := value.getUsedConstants.toList ++ todo
        match info with
        | .opaqueInfo _ => opaques := opaques.push n
        | .inductInfo v => todo := v.ctors ++ todo
        | .recInfo v =>
          for rule in v.rules do
            todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
  unless todo.isEmpty do throwError "KERNEL_AUDIT_FUEL_EXHAUSTED"
  logInfo m!"REACHABLE_OPAQUE_DECLARATIONS {opaques}"
  return (count, axes)

elab "#audit_safe_closure " n:ident : command => do
  let (count, axes) ← auditClosure #[n.getId]
  logInfo m!"SAFE_CLOSURE_PASS {n.getId}; declarations={count}; axioms={axes}"

/-- Frozen list of all authored declarations, independently extracted and reviewed. -/
def authored : Array Name := #[
  `P01AC.EffectiveCompleteness.NBody,
  `P01AC.EffectiveCompleteness.N,
  `P01AC.EffectiveCompleteness.orbitLink,
  `P01AC.EffectiveCompleteness.marker_normal,
  `P01AC.EffectiveCompleteness.marker_injective,
  `P01AC.EffectiveCompleteness.marker_conv_injective,
  `P01AC.EffectiveCompleteness.graph_application,
  `P01AC.EffectiveCompleteness.semantic_church_standardness,
  `P01AC.EffectiveCompleteness.C,
  `P01AC.EffectiveCompleteness.rawStep,
  `P01AC.EffectiveCompleteness.testerBody,
  `P01AC.EffectiveCompleteness.tester,
  `P01AC.EffectiveCompleteness.constantRaw,
  `P01AC.EffectiveCompleteness.N_form,
  `P01AC.EffectiveCompleteness.C_form,
  `P01AC.EffectiveCompleteness.rawStep_scoped,
  `P01AC.EffectiveCompleteness.rawStep_has,
  `P01AC.EffectiveCompleteness.app_has,
  `P01AC.EffectiveCompleteness.tester_has,
  `P01AC.EffectiveCompleteness.constantRaw_has,
  `P01AC.EffectiveCompleteness.iterationPoly,
  `P01AC.EffectiveCompleteness.inputNumeral,
  `P01AC.EffectiveCompleteness.iteration_scoped,
  `P01AC.EffectiveCompleteness.inputNumeral_has,
  `P01AC.EffectiveCompleteness.eval_iteration,
  `P01AC.EffectiveCompleteness.inputNumeral_applied,
  `P01AC.EffectiveCompleteness.stepTerm,
  `P01AC.EffectiveCompleteness.rawStep_application,
  `P01AC.EffectiveCompleteness.eval_rawStep,
  `P01AC.EffectiveCompleteness.tester_application,
  `P01AC.EffectiveCompleteness.constantRaw_application,
  `P01AC.EffectiveCompleteness.numericB,
  `P01AC.EffectiveCompleteness.numeral,
  `P01AC.EffectiveCompleteness.numericB_normal,
  `P01AC.EffectiveCompleteness.numeral_normal,
  `P01AC.EffectiveCompleteness.numeral_injective,
  `P01AC.EffectiveCompleteness.numeral_conversion_iff,
  `P01AC.EffectiveCompleteness.numeric_outputs_separate,
  `P01AC.EffectiveCompleteness.Represents,
  `P01AC.EffectiveCompleteness.run,
  `P01AC.EffectiveCompleteness.iteration_representation,
  `P01AC.EffectiveCompleteness.observation_representation,
  `P01AC.EffectiveCompleteness.EndpointValid,
  `P01AC.EffectiveCompleteness.IdentityValid,
  `P01AC.EffectiveCompleteness.identity_valid_iff_endpoint_valid,
  `P01AC.EffectiveCompleteness.identity_unary_iff_endpoint_valid,
  `P01AC.EffectiveCompleteness.canonical_observation,
  `P01AC.EffectiveCompleteness.endpoint_valid_iff_observations,
  `P01AC.EffectiveCompleteness.original_identity_iff_run_zero,
  `P01AC.EffectiveCompleteness.target_formed,
  `P01AC.EffectiveCompleteness.target_closed,
  `P01AC.EffectiveCompleteness.typed_constant_family_distinct,
  `P01AC.EffectiveCompleteness.semantic_proof_exists_iff_valid,
  `P01AC.EffectiveCompleteness.target_scope_bundle,
  `P01AC.EffectiveCompleteness.infinite_typed_family,
  `P01AC.EffectiveCompleteness.hasE_identity_implies_valid,
  `P01AC.EffectiveCompleteness.current_identity_implies_valid,
  `P01AC.EffectiveCompleteness.hasE_target_implies_run_zero,
  `P01AC.EffectiveCompleteness.current_target_implies_run_zero]

def authoredTheorems : Array Name := #[
  `P01AC.EffectiveCompleteness.marker_normal,
  `P01AC.EffectiveCompleteness.marker_injective,
  `P01AC.EffectiveCompleteness.marker_conv_injective,
  `P01AC.EffectiveCompleteness.graph_application,
  `P01AC.EffectiveCompleteness.semantic_church_standardness,
  `P01AC.EffectiveCompleteness.N_form,
  `P01AC.EffectiveCompleteness.C_form,
  `P01AC.EffectiveCompleteness.rawStep_scoped,
  `P01AC.EffectiveCompleteness.rawStep_has,
  `P01AC.EffectiveCompleteness.app_has,
  `P01AC.EffectiveCompleteness.tester_has,
  `P01AC.EffectiveCompleteness.constantRaw_has,
  `P01AC.EffectiveCompleteness.iteration_scoped,
  `P01AC.EffectiveCompleteness.inputNumeral_has,
  `P01AC.EffectiveCompleteness.eval_iteration,
  `P01AC.EffectiveCompleteness.inputNumeral_applied,
  `P01AC.EffectiveCompleteness.rawStep_application,
  `P01AC.EffectiveCompleteness.eval_rawStep,
  `P01AC.EffectiveCompleteness.tester_application,
  `P01AC.EffectiveCompleteness.constantRaw_application,
  `P01AC.EffectiveCompleteness.numericB_normal,
  `P01AC.EffectiveCompleteness.numeral_normal,
  `P01AC.EffectiveCompleteness.numeral_injective,
  `P01AC.EffectiveCompleteness.numeral_conversion_iff,
  `P01AC.EffectiveCompleteness.numeric_outputs_separate,
  `P01AC.EffectiveCompleteness.iteration_representation,
  `P01AC.EffectiveCompleteness.observation_representation,
  `P01AC.EffectiveCompleteness.identity_valid_iff_endpoint_valid,
  `P01AC.EffectiveCompleteness.identity_unary_iff_endpoint_valid,
  `P01AC.EffectiveCompleteness.canonical_observation,
  `P01AC.EffectiveCompleteness.endpoint_valid_iff_observations,
  `P01AC.EffectiveCompleteness.original_identity_iff_run_zero,
  `P01AC.EffectiveCompleteness.target_formed,
  `P01AC.EffectiveCompleteness.target_closed,
  `P01AC.EffectiveCompleteness.typed_constant_family_distinct,
  `P01AC.EffectiveCompleteness.semantic_proof_exists_iff_valid,
  `P01AC.EffectiveCompleteness.target_scope_bundle,
  `P01AC.EffectiveCompleteness.infinite_typed_family,
  `P01AC.EffectiveCompleteness.hasE_identity_implies_valid,
  `P01AC.EffectiveCompleteness.current_identity_implies_valid,
  `P01AC.EffectiveCompleteness.hasE_target_implies_run_zero,
  `P01AC.EffectiveCompleteness.current_target_implies_run_zero]

run_cmd do
  let env ← getEnv
  for n in authored do
    let some info := env.checked.get.find? n | throwError "MISSING_AUTHORED_DECLARATION {n}"
    unless info.isDefinition || info.isTheorem do throwError "WRONG_AUTHORED_KIND {n}"
    if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_AUTHORED_ROOT {n}"
  for n in authoredTheorems do
    let some info := env.checked.get.find? n | throwError "MISSING_AUTHORED_THEOREM {n}"
    unless info.isTheorem do throwError "WRONG_THEOREM_KIND {n}"
  let mut roots : Array Name := #[]
  let mut declarationCount := 0
  let mut theoremCount := 0
  let mut runtimeAuxiliaries := 0
  for (n, info) in env.constants.toList do
    if `P01AC.EffectiveCompleteness |>.isPrefixOf n then
      declarationCount := declarationCount + 1
      if info.isTheorem then theoremCount := theoremCount + 1
      if info.isUnsafe || info.isPartial then
        -- These are merely reported here. If reachable from any safe root,
        -- auditClosure below rejects them. Authored unsafe roots are rejected above.
        runtimeAuxiliaries := runtimeAuxiliaries + 1
        logInfo m!"NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
      else
        roots := roots.push n
        let axes ← Lean.collectAxioms n
        for a in axes do
          unless permittedAxioms.contains a do throwError "UNAPPROVED_COLLECTED_AXIOM {a} in {n}"
        logInfo m!"COMPILED_DECLARATION {n}; theorem={info.isTheorem}; axioms={axes}"
  let (reachable, axes) ← auditClosure roots
  logInfo m!"EFFECTIVE_KERNEL_AUDIT_PASS: namespaceDeclarations={declarationCount}; namespaceTheorems={theoremCount}; authoredDeclarations={authored.size}; authoredTheorems={authoredTheorems.size}; safeRoots={roots.size}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_safe_closure P01AC.EffectiveCompleteness.semantic_church_standardness
#audit_safe_closure P01AC.EffectiveCompleteness.original_identity_iff_run_zero
#audit_safe_closure P01AC.EffectiveCompleteness.semantic_proof_exists_iff_valid
#audit_safe_closure P01AC.EffectiveCompleteness.current_target_implies_run_zero
#audit_safe_closure P01AC.EffectiveCompleteness.hasE_target_implies_run_zero
end EffectiveKernelAudit
