import SignedService
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr

namespace SignedDependencyAudit
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
      collect env ((getImplementedBy? env name).toList ++ next ++ rest) seen

elab "audit_signed_dependencies" : command => do
  let env ← getEnv
  let roots := [``OrthemicCertificate.Signed.astDomain,
    ``OrthemicCertificate.Signed.positiveFormula,
    ``OrthemicCertificate.Signed.rejectCheck,
    ``OrthemicCertificate.Signed.refute,
    ``OrthemicCertificate.Signed.negativeCheck,
    ``OrthemicCertificate.Signed.negativeCandidate,
    ``OrthemicCertificate.Signed.solve]
  let formulaDeps := collect env [``OrthemicCertificate.Signed.positiveFormula,
    ``OrthemicCertificate.Signed.Atom.eval] {}
  let aggregateNames := ["OrthemicCertificate.check", "OrthemicCertificate.bodyCheck",
    "OrthemicCertificate.queryLookup", "OrthemicCertificate.BodyValid",
    "OrthemicCertificate.Layout", "OrthemicCertificate.Node.Valid",
    "OrthemicCertificate.Node.KeysValid", "OrthemicCertificate.Node.PairsValid",
    "OrthemicCertificate.Component.Valid", "OrthemicCertificate.Witness.Valid",
    "OrthemicCertificate.Path.Valid", "OrthemicCertificate.Path.Edges",
    "OrthemicCertificate.Input.Valid", "OrthemicCertificate.Input.inputCheck",
    "OrthemicCertificate.Input.shapeCheck", "OrthemicCertificate.Input.Shape",
    "OrthemicCertificate.Input.MenuValid", "OrthemicCertificate.Input.RowsValid"]
  let aggregates := formulaDeps.toList.map Name.toString |>.filter aggregateNames.contains
  unless aggregates.isEmpty do
    throwError "Aggregate predicate hidden in formula construction/evaluation: {aggregates}"
  logInfo "PASS: formula construction and atomic evaluation do not call any aggregate positive checker or inherited validity predicate."
  let deps := collect env roots {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s =>
    s.startsWith "HiddenParity" || s.startsWith "Classical" || s == "sorryAx" ||
    (s.splitOn "winningRegion").length > 1 || (s.splitOn "computedRegion").length > 1 ||
    (s.splitOn "chooseTarget").length > 1 ||
    s.startsWith "OrthemicCertificate.Path.exists" ||
    s.startsWith "OrthemicCertificate.Path.valid_sound" ||
    s.startsWith "OrthemicCertificate.Path.prefix_to_visited"
  let redirects := deps.toList.filterMap fun name =>
    (getImplementedBy? env name).map fun target => (name.toString,target.toString)
  let externals := deps.toList.filter fun name => isExtern env name
  logInfo m!"Signed service definition/opaque/implemented_by dependency count: {names.length}"
  logInfo m!"Signed service dependencies: {names}"
  logInfo m!"Implemented-by redirections: {redirects}"
  logInfo m!"Trusted external primitive leaves: {externals}"
  unless banned.isEmpty do throwError "Forbidden signed service dependency: {banned}"
  logInfo "PASS: executable signed service has no inherited solver, semantic decision, opaque target selector or classical-choice dependency."

audit_signed_dependencies
end SignedDependencyAudit
