import CertificatePath
import Lean.Util.FoldConsts

/-! Conservative transitive definition-body closure for the path predicate and
its executable decider. Theorem proof bodies are excluded because proofs erase.
Imported modules do not count as execution dependencies merely by import. -/
namespace PathDependencyAudit
open Lean Elab Command

partial def collect (env : Environment) (pending : List Name) (seen : NameSet) : NameSet :=
  match pending with
  | [] => seen
  | name :: rest =>
    if seen.contains name then collect env rest seen
    else
      let seen := seen.insert name
      let next := match env.find? name with
        | some (.defnInfo d) => d.value.getUsedConstants.toList
        | some (.opaqueInfo d) => d.value.getUsedConstants.toList
        | _ => []
      collect env (next ++ rest) seen

elab "audit_path_dependencies" : command => do
  let env ← getEnv
  let deps := collect env
    [``OrthemicCertificate.Path.Valid, ``OrthemicCertificate.Path.instDecidableValid] {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s =>
    s.startsWith "HiddenParity" || s.startsWith "Classical" || s == "sorryAx" ||
    s.startsWith "OrthemicCertificate.Path.exists" ||
    s.startsWith "OrthemicCertificate.Path.valid_sound" ||
    s.startsWith "OrthemicCertificate.Path.prefix_to_visited"
  logInfo m!"Path definition-body dependency count: {names.length}"
  logInfo m!"Path definition-body dependencies: {names}"
  unless banned.isEmpty do
    throwError "Unexpected semantic, classical, or proof-construction dependencies: {banned}"
  logInfo "PASS: no inherited solver/reachability, classical choice, or path-existence proof in the transitive checker definition-body closure."

audit_path_dependencies
end PathDependencyAudit
