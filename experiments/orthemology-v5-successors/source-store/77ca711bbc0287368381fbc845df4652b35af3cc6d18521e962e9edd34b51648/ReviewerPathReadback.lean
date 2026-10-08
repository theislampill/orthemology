import CertificatePath
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr

#print OrthemicCertificate.Path
#print OrthemicCertificate.Path.valid_sound
#print OrthemicCertificate.Path.exists_simple
#print OrthemicCertificate.Path.exists_valid
#print axioms OrthemicCertificate.Path.edgesDecidable
#print axioms OrthemicCertificate.Path.instDecidableValid
#print axioms OrthemicCertificate.Path.valid_sound
#print axioms OrthemicCertificate.Path.exists_simple
#print axioms OrthemicCertificate.Path.exists_valid

namespace ReviewerPathDependencies
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
elab "audit_independent_path" : command => do
  let env ← getEnv
  let deps := collect env [``OrthemicCertificate.Path.instDecidableValid] {}
  let names := deps.toList.map Name.toString
  let banned := names.filter fun s => s.startsWith "HiddenParity" || s.startsWith "Classical" || s == "sorryAx"
  let replacements := deps.toList.filterMap fun n => (getImplementedBy? env n).map fun i => (n.toString,i.toString)
  logInfo m!"PATH_CHECKER_CLOSURE {names}"
  logInfo m!"PATH_IMPLEMENTED_BY {replacements}"
  unless banned.isEmpty do throwError "Forbidden dependency: {banned}"
  logInfo "PASS independent path definition/opaque/implemented_by closure"
audit_independent_path
end ReviewerPathDependencies
