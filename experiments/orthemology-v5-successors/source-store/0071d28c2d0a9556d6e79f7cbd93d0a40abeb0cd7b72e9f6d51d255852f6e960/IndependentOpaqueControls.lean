import UnaryWitnesses
import UnaryExpressivity
import UnaryOpaqueBoundaryAudit
open Lean Elab Command UnaryIndependentAudit
run_cmd do
  let env ← getEnv
  let mut roots : Array Name := #[]
  for (n,info) in env.constants.toList do
    if `P01AC.UnaryIdentity |>.isPrefixOf n then
      unless info.isUnsafe || info.isPartial do roots := roots.push n
  let count ← auditOpaqueBoundary roots
  logInfo m!"ALL_UNARY_SAFE_ROOTS_OPAQUE_BOUNDARY_PASS roots={roots.size}; closure={count}; allowed=[Lean.opaqueId]"
#audit_unary_opaque_boundary P01AC.UnaryIdentity.normalise
#audit_unary_opaque_boundary P01AC.UnaryIdentity.distinguishingInput
#audit_unary_opaque_boundary P01AC.UnaryIdentity.Expr.closed
