import PolicySynthesisReduction
import Lean.Elab.Command
import Lean.Meta.Basic
import Lean.Compiler.ImplementedByAttr
import Lean.Compiler.ExternAttr

/- Erased-expression dependency inspection, separate from the full kernel
proof audit. It follows values while excluding proof and type arguments, as
erased in executable code. This is not an independent compiler-correctness
proof and does not certify the native replacement/optimisation pipeline. -/
namespace PolicySynthesisRuntimeVerification
open Lean Meta Elab Command

partial def valueConstants (e : Expr) : MetaM (Array Name) := do
  if ← isProof e then return #[]
  if ← isType e then return #[]
  match e with
  | .const n _ => return #[n]
  | .app f a => return (← valueConstants f) ++ (← valueConstants a)
  | .lam n ty body bi =>
    withLocalDecl n bi ty fun x => valueConstants (body.instantiate1 x)
  | .letE n ty val body _ =>
    let ds ← valueConstants val
    withLetDecl n ty val fun x => return ds ++ (← valueConstants (body.instantiate1 x))
  | .mdata _ body => valueConstants body
  | .proj _ _ body => valueConstants body
  | _ => return #[]

def permittedOpaques : Array Name := #[`Lean.opaqueId]

def runtimeClosure (roots : Array Name) : CommandElabM Nat := do
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
        if #[`Classical.choice, `Classical.propDecidable, `Classical.decEq, `sorryAx].contains n then
          throwError "NONCOMPUTABLE_RUNTIME_DEPENDENCY {n}"
        let info ← match env.checked.get.find? n with
          | some info => pure info
          | none => throwError "MISSING_RUNTIME_DECLARATION {n}"
        if info.isUnsafe || info.isPartial then throwError "UNSAFE_SOURCE_VALUE_DEPENDENCY {n}"
        if info.isAxiom then throwError "UNAPPROVED_RUNTIME_AXIOM {n}"
        match info with
        | .opaqueInfo _ =>
          unless permittedOpaques.contains n do throwError "UNCLASSIFIED_OPAQUE_RUNTIME_DEPENDENCY {n}"
          logInfo m!"CLASSIFIED_STANDARD_OPAQUE_RUNTIME {n}"
        | _ => pure ()
        if let some impl := Lean.Compiler.getImplementedBy? env n then
          if `PolicySynthesis |>.isPrefixOf n then throwError "AUTHORED_RUNTIME_REPLACEMENT {n} -> {impl}"
          logInfo m!"INHERITED_IMPLEMENTED_BY_BOUNDARY {n} -> {impl}"
        if (Lean.getExternAttrData? env n).isSome then
          if `PolicySynthesis |>.isPrefixOf n then throwError "AUTHORED_EXTERN_BOUNDARY {n}"
          logInfo m!"INHERITED_EXTERN_BOUNDARY {n}"
        if let some value := info.value? true then
          let ds ← liftTermElabM <| valueConstants value
          todo := ds.toList ++ todo
  unless todo.isEmpty do throwError "INCOMPLETE_RUNTIME_AUDIT"
  return count

elab "#audit_policy_runtime " n:ident : command => do
  let count ← runtimeClosure #[n.getId]
  logInfo m!"ERASED_VALUE_CLOSURE_PASS {n.getId}; declarations={count}; no computational classical choice, admitted term, unsafe/partial source value, or unclassified opaque dependency; native attributes separately inventoried"

#audit_policy_runtime PolicySynthesis.synthesisCheck
#audit_policy_runtime PolicySynthesis.componentCheck
#audit_policy_runtime PolicySynthesis.blockSnapshots
#audit_policy_runtime PolicySynthesis.progressCut
#audit_policy_runtime PolicySynthesis.natChecker
#audit_policy_runtime PolicySynthesis.specializeIndex
end PolicySynthesisRuntimeVerification
