import RestrictedCompiler
import verification.KernelAudit
open Lean Elab Command
open EffectiveKernelAudit

run_cmd do
  let env ← getEnv
  let ns := `P01AC.RestrictedIdentity
  let mut roots : Array Name := #[]
  let mut theorems := 0
  let mut runtimeAuxiliaries := 0
  for (n, info) in env.constants.toList do
    if ns.isPrefixOf n then
      if info.isUnsafe || info.isPartial then
        runtimeAuxiliaries := runtimeAuxiliaries + 1
        logInfo m!"RESTRICTED_NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
      else
        roots := roots.push n
        if info.isTheorem then theorems := theorems + 1
  let (reachable, axes) ← auditClosure roots
  logInfo m!"RESTRICTED_KERNEL_AUDIT_PASS safeRoots={roots.size}; theorems={theorems}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_safe_closure P01AC.RestrictedIdentity.Expr.toPR_denote
#audit_safe_closure P01AC.RestrictedIdentity.Expr.closed_has
#audit_safe_closure P01AC.RestrictedIdentity.fragment_valid_iff_denote
#audit_safe_closure P01AC.RestrictedIdentity.fragment_F_identity_iff_denote
#audit_safe_closure P01AC.RestrictedIdentity.fragment_G_identity_iff_denote
#audit_safe_closure P01AC.RestrictedIdentity.fragment_semantic_witness_iff_denote
