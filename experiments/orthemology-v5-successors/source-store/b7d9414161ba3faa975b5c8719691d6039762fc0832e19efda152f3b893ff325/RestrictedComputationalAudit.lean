import IdentityChecker
import verification.KernelAudit
open Lean Elab Command
open EffectiveKernelAudit

-- This is an additional conservative type/value closure check. No reliance on
-- merely searching source text for forbidden strings.
run_cmd do
  let env ← getEnv
  let roots := #[`P01AC.RestrictedIdentityV2.identityCheck,
    `P01AC.RestrictedIdentityV2.verifyCertificate,
    `P01AC.RestrictedIdentityV2.makeCertificate]
  let forbidden := #[`Classical.choice, `Classical.propDecidable, `Classical.decEq,
    `P01AC.RestrictedIdentityV2.polynomial, `P01AC.RestrictedIdentityV2.exponentFinsupp]
  let mut todo := roots.toList
  let mut seen : NameSet := {}
  let mut count := 0
  for _ in [:200000] do
    match todo with
    | [] => break
    | n :: tail =>
      todo := tail
      unless seen.contains n do
        seen := seen.insert n
        count := count + 1
        if forbidden.contains n then throwError "FORBIDDEN_COMPUTATIONAL_CLOSURE {n}"
        let info ← match env.checked.get.find? n with
          | some info => pure info
          | none => throwError "MISSING_CHECKED_DECLARATION {n}"
        if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_DEPENDENCY {n}"
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then todo := value.getUsedConstants.toList ++ todo
        match info with
        | .inductInfo v => todo := v.ctors ++ todo
        | .recInfo v => for rule in v.rules do todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
  unless todo.isEmpty do throwError "INCOMPLETE_AUDIT"
  logInfo m!"INDEPENDENT_COMPUTABLE_CLOSURE_PASS declarations={count}; no classical choice or abstract polynomial dependency"
  let (n, axes) ← auditClosure roots
  logInfo m!"INDEPENDENT_CHECKER_SAFE_CLOSURE declarations={n}; axioms={axes}"

#audit_safe_closure P01AC.RestrictedIdentityV2.nat_polynomial_eq_of_positive_eval
#audit_safe_closure P01AC.RestrictedIdentityV2.normalise_correct
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_fragmentValid
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_F_identity
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_G_identity
#audit_safe_closure P01AC.RestrictedIdentityV2.identityCheck_iff_semantic_witness
#audit_safe_closure P01AC.RestrictedIdentityV2.finite_certificate_complete
