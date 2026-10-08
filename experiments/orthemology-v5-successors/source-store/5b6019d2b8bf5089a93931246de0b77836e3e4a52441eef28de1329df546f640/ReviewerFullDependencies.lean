import CertificateComposition
import CertificateBinding
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr
import Lean.Compiler.ExternAttr

namespace ReviewerFullDependencies
open Lean Elab Command Lean.Compiler
partial def collect (env : Environment) (pending : List Name) (seen : NameSet) : NameSet :=
  match pending with
  | [] => seen
  | n :: rest =>
    if seen.contains n then collect env rest seen
    else
      let extra := match getImplementedBy? env n with | some i => [i] | none => []
      let next := match env.find? n with
        | some (.defnInfo d) => d.value.getUsedConstants.toList
        | some (.opaqueInfo d) => d.value.getUsedConstants.toList
        | _ => []
      collect env (extra ++ next ++ rest) (seen.insert n)
elab "audit_independent_full_checker" : command => do
  let env ← getEnv
  let deps := collect env [``OrthemicCertificate.check, ``OrthemicCertificate.bodyCheck,
    ``OrthemicCertificate.queryLookup, ``OrthemicCertificate.Input.sameInput,
    ``OrthemicCertificate.merge, ``OrthemicCertificate.linkParent,
    ``OrthemicCertificate.checkedMerge, ``OrthemicCertificate.checkedLinkParent,
    ``OrthemicCertificate.boundCheck] {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s => s.startsWith "HiddenParity" || s.startsWith "Classical" ||
    s == "sorryAx" || s.startsWith "Finset.powerset" || s.startsWith "List.powerset" ||
    s.startsWith "Multiset.powerset" || s.startsWith "OrthemicCertificate.region_has_certificate" ||
    s.startsWith "OrthemicCertificate.check_sound" || s.startsWith "OrthemicCertificate.Path.exists"
  let replacements := deps.toList.filterMap fun n => (getImplementedBy? env n).map fun i => (n.toString,i.toString)
  let externals := deps.toList.filterMap fun n =>
    if isExtern env n then some (n.toString,(getExternNameFor env `c n).getD "backend-specific") else none
  logInfo m!"CHECKER_CLOSURE_COUNT {names.length}"
  logInfo m!"CHECKER_CLOSURE {names}"
  logInfo m!"CHECKER_IMPLEMENTED_BY {replacements}"
  logInfo m!"TRUSTED_EXTERN_PRIMITIVES {externals}"
  unless banned.isEmpty do throwError "Forbidden dependency: {banned}"
  logInfo "PASS independent checker definition/opaque/implemented_by closure"
audit_independent_full_checker
end ReviewerFullDependencies
