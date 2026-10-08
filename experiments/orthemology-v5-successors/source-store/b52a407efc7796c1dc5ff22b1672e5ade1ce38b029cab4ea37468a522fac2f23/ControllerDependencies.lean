import DirectEndpoint
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr

namespace DirectControllerDependencyAudit
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

elab "audit_direct_compiler" : command => do
  let env ← getEnv
  let deps := collect env [``OrthemicCertificate.Direct.compile] {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s =>
    s.startsWith "Classical" || s == "sorryAx" ||
    (s.splitOn "winningRegion").length > 1 || (s.splitOn "computedRegion").length > 1 ||
    s.startsWith "HiddenParity.Sufficiency.chooseTarget" ||
    s.startsWith "HiddenParity.Sufficiency.cycleAction" ||
    s.startsWith "HiddenParity.Sufficiency.empiricalReject" ||
    s.startsWith "HiddenParity.Stage.markovTargetStates" ||
    s.startsWith "Fintype.equivFin" || s.startsWith "Real.instDecidable" ||
    s.startsWith "OrthemicCertificate.Direct.submitted_certified" ||
    s.startsWith "OrthemicCertificate.check_sound"
  let redirects := deps.toList.filterMap fun name =>
    (getImplementedBy? env name).map fun target => (name.toString,target.toString)
  let externals := deps.toList.filter fun name => isExtern env name
  logInfo m!"Direct compiler transitive definition/opaque/implemented_by count: {names.length}"
  logInfo m!"Direct compiler dependencies: {names}"
  logInfo m!"Implemented-by redirections: {redirects}"
  logInfo m!"Trusted external primitive leaves: {externals}"
  unless banned.isEmpty do throwError "Forbidden direct compiler dependencies: {banned}"
  logInfo "PASS: direct compiler uses submitted witnesses, sorted cycles and rational tests; no old solver, classical selection, real comparison, success field or fairness oracle."
audit_direct_compiler
end DirectControllerDependencyAudit
