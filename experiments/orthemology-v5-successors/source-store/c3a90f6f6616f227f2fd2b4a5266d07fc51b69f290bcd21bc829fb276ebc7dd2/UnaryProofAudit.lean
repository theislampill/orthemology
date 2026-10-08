import UnaryWitnesses
import UnaryExpressivity
import verification.KernelAudit
open Lean Elab Command EffectiveKernelAudit

run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  let mut proofCount := 0
  let mut runtimeAuxiliaries := 0
  for (n, info) in env.constants.toList do
    if `P01AC.UnaryIdentity |>.isPrefixOf n then
      if info.isTheorem then
        proofCount := proofCount + 1
        roots := roots.push n
      else if info.isUnsafe || info.isPartial then
        runtimeAuxiliaries := runtimeAuxiliaries + 1
      else
        roots := roots.push n
  unless proofCount > 0 do throwError "NO_AUTHORED_THEOREMS"
  let (count, axes) ← auditClosure roots
  logInfo m!"UNARY_ALL_SAFE_ROOTS_PASS roots={roots.size}; theorems={proofCount}; closure={count}; axioms={axes}; separately_excluded_nonproof_runtime_auxiliaries={runtimeAuxiliaries}"

#audit_safe_closure P01AC.UnaryIdentity.eval_eq_iff_polyEqual_of_bound
#audit_safe_closure P01AC.UnaryIdentity.canonical_description_unique
#audit_safe_closure P01AC.UnaryIdentity.normalise_eq_iff_denote
#audit_safe_closure P01AC.UnaryIdentity.identityCheck_iff_G_identity
#audit_safe_closure P01AC.UnaryIdentity.finite_certificate_complete
#audit_safe_closure P01AC.UnaryIdentity.distinguishingInput_none_iff_valid
#audit_safe_closure P01AC.UnaryIdentity.negative_certificate_complete
#audit_safe_closure P01AC.UnaryIdentity.expressible_iff_eventually_polynomial
#audit_safe_closure P01AC.UnaryIdentity.truncated_predecessor_not_expressible
