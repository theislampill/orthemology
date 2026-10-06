/- Additional independent review gate. The accepted predecessor auditor is not changed.
   Only the pinned standard identity wrapper is allowed as a reachable opaque.
   This catches source-level partial definitions whose public name is a safe opaque. -/
import verification.KernelAudit
open Lean Elab Command
namespace UnaryIndependentAudit

def auditOpaqueBoundary (roots : Array Name) : CommandElabM Nat := do
  let env ← getEnv
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
        let info ← match env.checked.get.find? n with
          | some info => pure info
          | none => throwError "MISSING_CHECKED_DECLARATION {n}"
        if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_BOUNDARY {n}"
        match info with
        | .opaqueInfo _ =>
          unless n == `Lean.opaqueId do throwError "UNAPPROVED_OPAQUE_BOUNDARY {n}"
        | _ => pure ()
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then todo := value.getUsedConstants.toList ++ todo
        match info with
        | .inductInfo v => todo := v.ctors ++ todo
        | .recInfo v => for rule in v.rules do todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
  unless todo.isEmpty do throwError "INCOMPLETE_OPAQUE_BOUNDARY_AUDIT"
  return count

elab "#audit_unary_opaque_boundary " n:ident : command => do
  let count ← auditOpaqueBoundary #[n.getId]
  logInfo m!"OPAQUE_BOUNDARY_PASS root={n.getId}; closure={count}; allowed=[Lean.opaqueId]"
end UnaryIndependentAudit
