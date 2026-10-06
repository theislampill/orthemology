import PolynomialTestBoundary
import verification.KernelAudit
open Lean Elab Command
open EffectiveKernelAudit

run_cmd do
  let env ← getEnv
  let ns := `P01AC.PolynomialTestBoundary
  let mut roots : Array Name := #[]
  let mut theorems := 0
  let mut runtimeAuxiliaries := 0
  for (n, info) in env.constants.toList do
    if ns.isPrefixOf n then
      if info.isUnsafe || info.isPartial then
        runtimeAuxiliaries := runtimeAuxiliaries + 1
        logInfo m!"POLYNOMIAL_TEST_NONPROOF_RUNTIME_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
      else
        roots := roots.push n
        if info.isTheorem then theorems := theorems + 1
  let (reachable, axes) ← auditClosure roots
  logInfo m!"POLYNOMIAL_TEST_KERNEL_AUDIT_PASS safeRoots={roots.size}; theorems={theorems}; nonproofRuntimeAuxiliaries={runtimeAuxiliaries}; reachableCheckedDeclarations={reachable}; axioms={axes}; unsafeOrPartialDependencies=0"

#audit_safe_closure P01AC.PolynomialTestBoundary.equalPR_denote
#audit_safe_closure P01AC.PolynomialTestBoundary.Root.closed_has
#audit_safe_closure P01AC.PolynomialTestBoundary.Root.closed_obs
#audit_safe_closure P01AC.PolynomialTestBoundary.valid_iff_denote
#audit_safe_closure P01AC.PolynomialTestBoundary.F_identity_iff_denote
#audit_safe_closure P01AC.PolynomialTestBoundary.G_identity_iff_denote
#audit_safe_closure P01AC.PolynomialTestBoundary.semantic_witness_iff_denote
#audit_safe_closure P01AC.PolynomialTestBoundary.root_equal_zero_iff
