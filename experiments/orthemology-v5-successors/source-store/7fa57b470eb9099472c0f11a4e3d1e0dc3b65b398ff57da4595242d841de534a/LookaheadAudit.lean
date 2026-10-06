import LookaheadBoundary
import KernelAudit
import RuntimeAudit

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  let mut theoremCount := 0
  let mut runtimeAux := 0
  for (n, info) in env.constants.toList do
    if `EffectiveRenewal.Lookahead |>.isPrefixOf n then
      if info.isTheorem then theoremCount := theoremCount + 1
      if info.isUnsafe || info.isPartial then
        runtimeAux := runtimeAux + 1
        logInfo m!"LOOKAHEAD_COMPILER_AUXILIARY {n}"
      else roots := roots.push n
  let (count, axes) ← RenewalVerification.auditClosure roots
  logInfo m!"LOOKAHEAD_KERNEL_AUDIT_PASS safeRoots={roots.size}; theoremDeclarations={theoremCount}; compilerAuxiliaries={runtimeAux}; reachable={count}; axioms={axes}"

#audit_renewal_closure EffectiveRenewal.Lookahead.finite_lookahead_boundary
#audit_renewal_closure EffectiveRenewal.Lookahead.one_step_recursive_witness_failure
#audit_renewal_closure EffectiveRenewal.Lookahead.lookahead_plan_contract_run
#audit_renewal_runtime EffectiveRenewal.Lookahead.lookaheadCheck
#audit_renewal_runtime EffectiveRenewal.Lookahead.lookaheadPlan
#audit_renewal_runtime EffectiveRenewal.Lookahead.supplement
