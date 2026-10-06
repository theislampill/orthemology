import PolicySynthesisReduction
import Lean.Util.CollectAxioms
import Lean.Elab.Command

/- The traversal follows the inspected Fifteenth kernel-closure audit method,
with roots and namespace specific to this isolated package. It examines checked
constant types and kernel values rather than scanning source strings. -/
namespace PolicySynthesisVerification
open Lean Elab Command

-- Only the standard identity constant is an allowed opaque kernel boundary.
-- Lean source `partial def` can otherwise appear safe/total at ConstantInfo.
def permittedOpaques : Array Name := #[`Lean.opaqueId]

def permittedAxioms : Array Name := #[`propext, `Classical.choice, `Quot.sound]

def auditClosure (roots : Array Name) : CommandElabM (Nat × Array Name) := do
  let env ← getEnv
  let mut todo := roots.toList
  let mut seen : NameSet := {}
  let mut axes : Array Name := #[]
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
        if info.isUnsafe then throwError "UNSAFE_KERNEL_DEPENDENCY {n}"
        if info.isPartial then throwError "PARTIAL_KERNEL_DEPENDENCY {n}"
        match info with
        | .opaqueInfo _ =>
          unless permittedOpaques.contains n do throwError "UNCLASSIFIED_OPAQUE_KERNEL_DEPENDENCY {n}"
          logInfo m!"CLASSIFIED_STANDARD_OPAQUE {n}"
        | _ => pure ()
        if info.isAxiom then
          unless permittedAxioms.contains n do throwError "UNAPPROVED_KERNEL_AXIOM {n}"
          axes := axes.push n
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then todo := value.getUsedConstants.toList ++ todo
        match info with
        | .inductInfo v => todo := v.ctors ++ todo
        | .recInfo v => for rule in v.rules do todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
  unless todo.isEmpty do throwError "INCOMPLETE_KERNEL_AUDIT"
  return (count, axes)

elab "#audit_policy_closure " n:ident : command => do
  let (count, axes) ← auditClosure #[n.getId]
  logInfo m!"KERNEL_CLOSURE_PASS {n.getId}; declarations={count}; axioms={axes}"

run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  let mut theorems := 0
  let mut auxiliary := 0
  for (n, info) in env.constants.toList do
    if `PolicySynthesis |>.isPrefixOf n then
      if info.isTheorem then theorems := theorems + 1
      if info.isUnsafe || info.isPartial then
        auxiliary := auxiliary + 1
        logInfo m!"NONPROOF_COMPILER_AUXILIARY {n}; unsafe={info.isUnsafe}; partial={info.isPartial}"
      else
        roots := roots.push n
        let axes ← Lean.collectAxioms n
        for a in axes do
          unless permittedAxioms.contains a do throwError "UNAPPROVED_COLLECTED_AXIOM {a} in {n}"
  let (count, axes) ← auditClosure roots
  logInfo m!"PACKAGE_KERNEL_AUDIT_PASS safeRoots={roots.size}; theoremDeclarations={theorems}; compilerAuxiliaries={auxiliary}; reachable={count}; axioms={axes}"

#audit_policy_closure PolicySynthesis.policy_synthesis_reduction
#audit_policy_closure PolicySynthesis.synthesisCheck_primrec
#audit_policy_closure PolicySynthesis.synthesis_computablePath_iff
#audit_policy_closure PolicySynthesis.component_computablePath_iff
#audit_policy_closure PolicySynthesis.total_checker_code_family
end PolicySynthesisVerification
