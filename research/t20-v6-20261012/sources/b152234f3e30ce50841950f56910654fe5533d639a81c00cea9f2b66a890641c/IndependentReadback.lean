import P01CanonicalCarrierProjection
import Lean
open Lean Elab Command
set_option pp.universes true
set_option format.width 120
elab "#independent_kind " n:ident : command => do
  let env ← getEnv
  let some c := env.checked.get.find? n.getId | throwError "unchecked target"
  let kind := match c with
    | .thmInfo _ => "theorem"
    | .defnInfo _ => "def"
    | _ => "other"
  logInfo m!"KIND {n.getId} {kind}"
  let axioms ← Lean.collectAxioms n.getId
  for a in axioms do
    unless a == `propext || a == `Classical.choice || a == `Quot.sound do
      throwError "unexpected axiom: {a}"

#eval IO.println "TARGET_BEGIN P01DF.carrierCode"
#independent_kind P01DF.carrierCode
#check P01DF.carrierCode
#print axioms P01DF.carrierCode
#eval IO.println "TARGET_END P01DF.carrierCode"
#eval IO.println "TARGET_BEGIN P01DF.carrier_code_ext"
#independent_kind P01DF.carrier_code_ext
#check P01DF.carrier_code_ext
#print axioms P01DF.carrier_code_ext
#eval IO.println "TARGET_END P01DF.carrier_code_ext"
#eval IO.println "TARGET_BEGIN P01DF.raw_carrier_is_top"
#independent_kind P01DF.raw_carrier_is_top
#check P01DF.raw_carrier_is_top
#print axioms P01DF.raw_carrier_is_top
#eval IO.println "TARGET_END P01DF.raw_carrier_is_top"
#eval IO.println "TARGET_BEGIN P01DF.carrierFamily"
#independent_kind P01DF.carrierFamily
#check P01DF.carrierFamily
#print axioms P01DF.carrierFamily
#eval IO.println "TARGET_END P01DF.carrierFamily"
#eval IO.println "TARGET_BEGIN P01DF.raw_pi_carrier_square"
#independent_kind P01DF.raw_pi_carrier_square
#check P01DF.raw_pi_carrier_square
#print axioms P01DF.raw_pi_carrier_square
#eval IO.println "TARGET_END P01DF.raw_pi_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.sigma_carrier_square"
#independent_kind P01DF.sigma_carrier_square
#check P01DF.sigma_carrier_square
#print axioms P01DF.sigma_carrier_square
#eval IO.println "TARGET_END P01DF.sigma_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.raw_sigma_carrier_square"
#independent_kind P01DF.raw_sigma_carrier_square
#check P01DF.raw_sigma_carrier_square
#print axioms P01DF.raw_sigma_carrier_square
#eval IO.println "TARGET_END P01DF.raw_sigma_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.raw_identity_carrier_square"
#independent_kind P01DF.raw_identity_carrier_square
#check P01DF.raw_identity_carrier_square
#print axioms P01DF.raw_identity_carrier_square
#eval IO.println "TARGET_END P01DF.raw_identity_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.projectedBody"
#independent_kind P01DF.projectedBody
#check P01DF.projectedBody
#print axioms P01DF.projectedBody
#eval IO.println "TARGET_END P01DF.projectedBody"
#eval IO.println "TARGET_BEGIN P01DF.syntax_pi_carrier_square"
#independent_kind P01DF.syntax_pi_carrier_square
#check P01DF.syntax_pi_carrier_square
#print axioms P01DF.syntax_pi_carrier_square
#eval IO.println "TARGET_END P01DF.syntax_pi_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.syntax_sigma_carrier_square"
#independent_kind P01DF.syntax_sigma_carrier_square
#check P01DF.syntax_sigma_carrier_square
#print axioms P01DF.syntax_sigma_carrier_square
#eval IO.println "TARGET_END P01DF.syntax_sigma_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.syntax_identity_carrier_square"
#independent_kind P01DF.syntax_identity_carrier_square
#check P01DF.syntax_identity_carrier_square
#print axioms P01DF.syntax_identity_carrier_square
#eval IO.println "TARGET_END P01DF.syntax_identity_carrier_square"
#eval IO.println "TARGET_BEGIN P01DF.canonical_pi_admission"
#independent_kind P01DF.canonical_pi_admission
#check P01DF.canonical_pi_admission
#print axioms P01DF.canonical_pi_admission
#eval IO.println "TARGET_END P01DF.canonical_pi_admission"
#eval IO.println "TARGET_BEGIN P01DF.canonical_sigma_admission"
#independent_kind P01DF.canonical_sigma_admission
#check P01DF.canonical_sigma_admission
#print axioms P01DF.canonical_sigma_admission
#eval IO.println "TARGET_END P01DF.canonical_sigma_admission"
#eval IO.println "TARGET_BEGIN P01DF.canonical_identity_admission"
#independent_kind P01DF.canonical_identity_admission
#check P01DF.canonical_identity_admission
#print axioms P01DF.canonical_identity_admission
#eval IO.println "TARGET_END P01DF.canonical_identity_admission"
#eval IO.println "TARGET_BEGIN P01DF.arrow_carrier_inclusion"
#independent_kind P01DF.arrow_carrier_inclusion
#check P01DF.arrow_carrier_inclusion
#print axioms P01DF.arrow_carrier_inclusion
#eval IO.println "TARGET_END P01DF.arrow_carrier_inclusion"
#eval IO.println "TARGET_BEGIN P01DF.arbitrary_arrow_reverse_projection_fails"
#independent_kind P01DF.arbitrary_arrow_reverse_projection_fails
#check P01DF.arbitrary_arrow_reverse_projection_fails
#print axioms P01DF.arbitrary_arrow_reverse_projection_fails
#eval IO.println "TARGET_END P01DF.arbitrary_arrow_reverse_projection_fails"
#eval IO.println "TARGET_BEGIN P01DF.canonical_identity_inclusion"
#independent_kind P01DF.canonical_identity_inclusion
#check P01DF.canonical_identity_inclusion
#print axioms P01DF.canonical_identity_inclusion
#eval IO.println "TARGET_END P01DF.canonical_identity_inclusion"
#eval IO.println "TARGET_BEGIN P01DF.arbitrary_identity_forward_projection_fails"
#independent_kind P01DF.arbitrary_identity_forward_projection_fails
#check P01DF.arbitrary_identity_forward_projection_fails
#print axioms P01DF.arbitrary_identity_forward_projection_fails
#eval IO.println "TARGET_END P01DF.arbitrary_identity_forward_projection_fails"
