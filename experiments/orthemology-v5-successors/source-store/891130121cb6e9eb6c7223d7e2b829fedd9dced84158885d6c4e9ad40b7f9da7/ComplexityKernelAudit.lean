/- Independent successor audit over checked kernel declarations.
   It reuses the predecessor's type/value closure walk, not compiler IR.
   Both semantic namespaces are roots; compiler runtime auxiliaries are reported
   separately and never counted as checked proof dependencies. -/
import EffectivePartialObserver
import verification.KernelAudit

open Lean Elab Command
namespace ComplexityKernelAudit
open EffectiveKernelAudit

/-- Exact reviewed declarations authored in the two successor files. -/
def successorAuthored : Array Name := #[
  `P01AC.IdentityComplexity.related_same_index,
  `P01AC.IdentityComplexity.same_index_related,
  `P01AC.IdentityComplexity.related_iff_same_index,
  `P01AC.IdentityComplexity.canonical,
  `P01AC.IdentityComplexity.canonical_self,
  `P01AC.IdentityComplexity.CanonicalTests,
  `P01AC.IdentityComplexity.endpoint_valid_iff_canonical_tests,
  `P01AC.IdentityComplexity.identity_valid_iff_canonical_tests,
  `P01AC.IdentityComplexity.semantic_proof_exists_iff_canonical_tests,
  `P01AC.IdentityComplexity.numericSucc,
  `P01AC.IdentityComplexity.repeated_step_numeral,
  `P01AC.IdentityComplexity.universalTester,
  `P01AC.IdentityComplexity.universalTester_has,
  `P01AC.IdentityComplexity.universal_target_formed,
  `P01AC.IdentityComplexity.universal_target_closed,
  `P01AC.IdentityComplexity.universal_target_scope,
  `P01AC.IdentityComplexity.universalTester_observation,
  `P01AC.IdentityComplexity.universal_endpoint_valid_iff_total,
  `P01AC.IdentityComplexity.original_universal_identity_iff_total,
  `P01AC.IdentityComplexity.raw_no_normal_form_excludes_zero,
  `P01AC.IdentityComplexity.numeral_marker_free,
  `P01AC.IdentityComplexity.erased_no_normal_form_excludes_zero,
  `P01AC.IdentityComplexity.pure_universal_observation_erasure,
  `P01AC.IdentityComplexity.original_universal_identity_iff_total_of_no_normal_form]

def successorTheorems : Array Name := #[
  `P01AC.IdentityComplexity.related_same_index,
  `P01AC.IdentityComplexity.same_index_related,
  `P01AC.IdentityComplexity.related_iff_same_index,
  `P01AC.IdentityComplexity.canonical_self,
  `P01AC.IdentityComplexity.endpoint_valid_iff_canonical_tests,
  `P01AC.IdentityComplexity.identity_valid_iff_canonical_tests,
  `P01AC.IdentityComplexity.semantic_proof_exists_iff_canonical_tests,
  `P01AC.IdentityComplexity.repeated_step_numeral,
  `P01AC.IdentityComplexity.universalTester_has,
  `P01AC.IdentityComplexity.universal_target_formed,
  `P01AC.IdentityComplexity.universal_target_closed,
  `P01AC.IdentityComplexity.universal_target_scope,
  `P01AC.IdentityComplexity.universalTester_observation,
  `P01AC.IdentityComplexity.universal_endpoint_valid_iff_total,
  `P01AC.IdentityComplexity.original_universal_identity_iff_total,
  `P01AC.IdentityComplexity.raw_no_normal_form_excludes_zero,
  `P01AC.IdentityComplexity.numeral_marker_free,
  `P01AC.IdentityComplexity.erased_no_normal_form_excludes_zero,
  `P01AC.IdentityComplexity.pure_universal_observation_erasure,
  `P01AC.IdentityComplexity.original_universal_identity_iff_total_of_no_normal_form]

elab "#audit_complexity_safe_closure " n:ident : command => do
  let (count, axes) ← auditClosure #[n.getId]
  logInfo m!"COMPLEXITY_SAFE_CLOSURE_PASS {n.getId}; declarations={count}; axioms={axes}"

run_cmd do
  let env ← getEnv
  for n in successorAuthored do
    let some info := env.checked.get.find? n | throwError "MISSING_SUCCESSOR_DECLARATION {n}"
    unless info.isDefinition || info.isTheorem do throwError "WRONG_SUCCESSOR_KIND {n}"
    if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_SUCCESSOR_ROOT {n}"
  for n in successorTheorems do
    let some info := env.checked.get.find? n | throwError "MISSING_SUCCESSOR_THEOREM {n}"
    unless info.isTheorem do throwError "WRONG_SUCCESSOR_THEOREM_KIND {n}"
  let mut allRoots : Array Name := #[]
  for ns in #[`P01AC.EffectiveCompleteness, `P01AC.IdentityComplexity] do
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
          logInfo m!"COMPLEXITY_NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
        else
          roots := roots.push n
          let axes ← Lean.collectAxioms n
          for a in axes do
            unless permittedAxioms.contains a do
              throwError "UNAPPROVED_COMPLEXITY_COLLECTED_AXIOM {a} in {n}"
          logInfo m!"COMPLEXITY_COMPILED_DECLARATION {n}; theorem={info.isTheorem}; axioms={axes}"
    let (reachable, axes) ← auditClosure roots
    logInfo m!"COMPLEXITY_NAMESPACE_AUDIT_PASS {ns}; namespaceDeclarations={count}; namespaceTheorems={theoremCount}; safeRoots={roots.size}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"
    allRoots := allRoots ++ roots
  let (reachable, axes) ← auditClosure allRoots
  logInfo m!"COMPLEXITY_KERNEL_AUDIT_PASS: successorAuthoredDeclarations={successorAuthored.size}; successorAuthoredTheorems={successorTheorems.size}; predecessorAuthoredDeclarations={authored.size}; predecessorAuthoredTheorems={authoredTheorems.size}; combinedSafeRoots={allRoots.size}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_complexity_safe_closure P01AC.IdentityComplexity.related_iff_same_index
#audit_complexity_safe_closure P01AC.IdentityComplexity.endpoint_valid_iff_canonical_tests
#audit_complexity_safe_closure P01AC.IdentityComplexity.semantic_proof_exists_iff_canonical_tests
#audit_complexity_safe_closure P01AC.IdentityComplexity.original_universal_identity_iff_total
#audit_complexity_safe_closure P01AC.IdentityComplexity.original_universal_identity_iff_total_of_no_normal_form
end ComplexityKernelAudit
