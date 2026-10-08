/- Reusable, bounded checked-value closure inspection. This inventories runtime
   replacement metadata, but deliberately does not certify native compiler/FFI code. -/
import UnaryOpaqueBoundaryAudit
import Lean.Compiler.ImplementedByAttr
import Lean.Compiler.ExternAttr
import Lean.Compiler.NoncomputableAttr
open Lean Elab Command
namespace UnaryIndependentAudit

def describeExtern : ExternEntry → String
  | .adhoc backend => s!"adhoc:{backend}"
  | .inline backend pattern => s!"inline:{backend}:{pattern}"
  | .standard backend fn => s!"standard:{backend}:{fn}"
  | .foreign backend fn => s!"foreign:{backend}:{fn}"

def inventoryRuntimeBoundary (label : String) (roots : Array Name)
    (authoredPrefixes : Array Name) : CommandElabM Unit := do
  let boundaryCount ← auditOpaqueBoundary roots
  let env ← getEnv
  let mut todo := roots.toList
  let mut seen : NameSet := {}
  let mut replacements := 0
  let mut externals := 0
  let mut markedNoncomputable := 0
  for _ in [:200000] do
    match todo with
    | [] => break
    | n :: tail =>
      todo := tail
      unless seen.contains n do
        seen := seen.insert n
        let info ← match env.checked.get.find? n with
          | some info => pure info
          | none => throwError "MISSING_CHECKED_DECLARATION {n}"
        let own := authoredPrefixes.any (·.isPrefixOf n)
        let replacement := Compiler.getImplementedBy? env n
        let external := getExternAttrData? env n
        let noncomp := isNoncomputable env n
        if own && (replacement.isSome || external.isSome || noncomp) then
          throwError "AUTHORED_RUNTIME_OVERRIDE_OR_NONCOMPUTABLE {n}"
        if let some target := replacement then
          replacements := replacements + 1
          let targetInfo ← match env.checked.get.find? target with
            | some info => pure info
            | none => throwError "MISSING_RUNTIME_REPLACEMENT {target}"
          logInfo m!"RUNTIME_IMPLEMENTED_BY {label}: {n} -> {target}; targetUnsafe={targetInfo.isUnsafe}; targetPartial={targetInfo.isPartial}"
        if let some data := external then
          externals := externals + 1
          logInfo m!"RUNTIME_EXTERN {label}: {n}; entries={data.entries.map describeExtern}"
        if noncomp then
          markedNoncomputable := markedNoncomputable + 1
          logInfo m!"RUNTIME_NONCOMPUTABLE_TAG {label}: {n}"
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then todo := value.getUsedConstants.toList ++ todo
        match info with
        | .inductInfo v => todo := v.ctors ++ todo
        | .recInfo v => for rule in v.rules do todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
  unless todo.isEmpty do throwError "INCOMPLETE_RUNTIME_BOUNDARY_INVENTORY"
  logInfo m!"RUNTIME_BOUNDARY_INVENTORY_PASS {label}: roots={roots.size}; checkedTypeValueClosure={boundaryCount}; implementedBy={replacements}; extern={externals}; noncomputableTags={markedNoncomputable}; authoredOverride=0; nativeCompilerAndFFIUnverified=true"
end UnaryIndependentAudit
