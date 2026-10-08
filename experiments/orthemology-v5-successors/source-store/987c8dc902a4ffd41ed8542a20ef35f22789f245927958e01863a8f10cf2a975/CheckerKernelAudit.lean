import CheckerControls
import verification.KernelAudit
open Lean Elab Command
open EffectiveKernelAudit

run_cmd do
  let env ← getEnv
  let ns := `P01AC.RestrictedIdentityV2
  let mut roots : Array Name := #[]
  let mut theoremCount := 0
  let mut runtimeAuxiliaries := 0
  for (n, info) in env.constants.toList do
    if ns.isPrefixOf n then
      if info.isUnsafe || info.isPartial then
        runtimeAuxiliaries := runtimeAuxiliaries + 1
        logInfo m!"V2_NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
      else
        roots := roots.push n
        if info.isTheorem then theoremCount := theoremCount + 1
  let (reachable, axes) ← auditClosure roots
  logInfo m!"V2_KERNEL_AUDIT_PASS safeRoots={roots.size}; namespaceTheorems={theoremCount}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_safe_closure P01AC.RestrictedIdentityV2.nat_polynomial_eq_of_positive_eval
#audit_safe_closure P01AC.RestrictedIdentityV2.normalise_correct
#audit_safe_closure P01AC.RestrictedIdentityV2.normalise_supported
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_fragmentValid
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_F_identity
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_G_identity
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_semantic_witness
#audit_safe_closure P01AC.RestrictedIdentityV2.verifyCertificate
#audit_safe_closure P01AC.RestrictedIdentityV2.finite_certificate_complete
