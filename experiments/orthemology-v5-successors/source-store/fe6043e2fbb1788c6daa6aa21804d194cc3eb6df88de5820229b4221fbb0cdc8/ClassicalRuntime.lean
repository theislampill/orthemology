import UnaryWitnesses
import UnaryExpressivity
import verification.KernelAudit
open Lean Elab Command EffectiveKernelAudit

noncomputable def reviewClassicalRuntime : Nat := Classical.choice (show Nonempty Nat from ⟨0⟩)

run_cmd do
  let env ← getEnv
  let roots := #[`reviewClassicalRuntime]
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
  unless todo.isEmpty do throwError "INCOMPLETE_COMPUTATIONAL_AUDIT"
  logInfo m!"UNARY_COMPUTATIONAL_CLOSURE_PASS roots={roots.size}; declarations={count}; no classical choice, classical decider, abstract polynomial, unsafe or partial dependency"
  let (n, axes) ← auditClosure roots
  logInfo m!"UNARY_RUNTIME_SAFE_CLOSURE declarations={n}; axioms={axes}"
