import CertificateBinding
import CertificateComposition
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr

/-! Evaluated-dependency audit follows ordinary definition bodies, opaque bodies,
and implemented_by redirections. The proof graph is not a runtime graph.
Imported trusted Lean/Mathlib primitives may have external implementations; the
names of those leaves are reported rather than falsely claiming binary proof. -/
namespace CheckerDependencyAudit
open Lean Elab Command Compiler

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
      let redirects := (getImplementedBy? env name).toList
      collect env (redirects ++ next ++ rest) seen

elab "audit_checker_dependencies" : command => do
  let env ← getEnv
  let deps := collect env [``OrthemicCertificate.bodyCheck, ``OrthemicCertificate.queryLookup,
    ``OrthemicCertificate.check, ``OrthemicCertificate.boundCheck,
    ``OrthemicCertificate.checkedMerge, ``OrthemicCertificate.checkedLinkParent] {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s =>
    s.startsWith "HiddenParity" || s.startsWith "Classical" || s == "sorryAx" ||
    (s.splitOn "winningRegion").length > 1 || (s.splitOn "computedRegion").length > 1 || (s.splitOn "chooseTarget").length > 1 ||
    (s.splitOn "powerset").length > 1 || s.startsWith "OrthemicCertificate.Path.exists" ||
    s.startsWith "OrthemicCertificate.Path.valid_sound" ||
    s.startsWith "OrthemicCertificate.Path.prefix_to_visited"
  let redirects := deps.toList.filterMap fun name =>
    (getImplementedBy? env name).map fun target => (name.toString,target.toString)
  let externals := deps.toList.filter fun name => isExtern env name
  logInfo m!"Checker transitive definition/opaque/implemented_by dependency count: {names.length}"
  logInfo m!"Checker dependencies: {names}"
  logInfo m!"Implemented-by redirections: {redirects}"
  logInfo m!"Trusted external primitive leaves: {externals}"
  unless banned.isEmpty do throwError "Forbidden checker dependency: {banned}"
  logInfo "PASS: submitted-data checker has no inherited solver, powerset, opaque target, semantic decision, or classical-choice dependency."

audit_checker_dependencies
end CheckerDependencyAudit
