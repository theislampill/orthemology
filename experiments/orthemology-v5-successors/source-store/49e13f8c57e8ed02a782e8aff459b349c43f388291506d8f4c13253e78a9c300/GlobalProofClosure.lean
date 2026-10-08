import Lean.Elab.Command
import Lean.Util.CollectAxioms
open Lean Elab Command

/- New integration-only traversal. The inherited full-project auditor already
used a one-million-step bound. The preserved smaller lane auditors are unchanged.
This is a logical proof audit. Reachable safe opaque constants are inventoried
explicitly, as in the preserved inherited audit. Computational unknown-opaque
rejection remains in the separately replayed strict lane auditors.
Types, kernel values, inductive constructors and recursor right-hand sides are
all followed. Every proof root is selected separately by module identity. -/
namespace RecoveredIntegrationAudit

def allowedAxioms : Array Name := #[`propext, `Classical.choice, `Quot.sound]

def auditFullProofClosure (roots : Array Name) : CommandElabM (Nat × Array Name) := do
  let env ← getEnv
  let mut pending := roots.toList
  let mut seen : NameSet := {}
  let mut count := 0
  let mut axioms : Array Name := #[]
  let mut opaques : Array Json := #[]
  for _ in [:1000000] do
    match pending with
    | [] => break
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        seen := seen.insert name
        count := count + 1
        let some info := env.checked.get.find? name |
          throwError "INTEGRATION_UNCHECKED_DECLARATION {name}"
        if info.isUnsafe || info.isPartial then
          throwError "INTEGRATION_UNSAFE_OR_PARTIAL {name}"
        if info.isAxiom then
          unless allowedAxioms.contains name do
            throwError "INTEGRATION_UNAPPROVED_AXIOM {name}"
          axioms := axioms.push name
        match info with
        | .opaqueInfo _ =>
          let moduleName := match env.getModuleIdxFor? name with
            | some idx => env.header.moduleNames[idx.toNat]!.toString
            | none => "current-module"
          opaques := opaques.push <| Json.mkObj [
            ("name", toJson name.toString), ("module", toJson moduleName),
            ("kernelValueAvailable", toJson (info.value? true).isSome),
            ("scope", toJson "logical proof closure only; no executable-totality claim")]
        | _ => pure ()
        pending := info.type.getUsedConstants.toList ++ pending
        if let some value := info.value? true then
          pending := value.getUsedConstants.toList ++ pending
        match info with
        | .inductInfo value => pending := value.ctors ++ pending
        | .recInfo value =>
          for rule in value.rules do pending := rule.rhs.getUsedConstants.toList ++ pending
        | _ => pure ()
  unless pending.isEmpty do throwError "INTEGRATION_AUDIT_INCOMPLETE"
  liftIO <| IO.FS.writeFile "logical-opaque-inventory.json" (Json.pretty (toJson opaques))
  return (count, axioms)

elab "#audit_integration_proof " root:ident : command => do
  let (count, axioms) ← auditFullProofClosure #[root.getId]
  logInfo m!"INTEGRATION_PROOF_CLOSURE_PASS root={root.getId}; closure={count}; axioms={axioms}"
end RecoveredIntegrationAudit
