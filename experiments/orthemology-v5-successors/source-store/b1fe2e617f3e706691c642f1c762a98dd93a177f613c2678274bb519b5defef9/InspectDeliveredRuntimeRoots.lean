import UnaryWitnesses
import UnaryExpressivity
import IdentityChecker
import RuntimeBoundaryInventory
open Lean Elab Command UnaryIndependentAudit
run_cmd do
  inventoryRuntimeBoundary "Sixteenth" #[`P01AC.UnaryIdentity.normalise,
    `P01AC.UnaryIdentity.identityCheck, `P01AC.UnaryIdentity.verifyCertificate,
    `P01AC.UnaryIdentity.makeCertificate, `P01AC.UnaryIdentity.distinguishingInput,
    `P01AC.UnaryIdentity.verifyNegative, `P01AC.UnaryIdentity.Expr.denote,
    `P01AC.UnaryIdentity.Expr.substitute, `P01AC.UnaryIdentity.Expr.toPR,
    `P01AC.UnaryIdentity.Expr.body, `P01AC.UnaryIdentity.Expr.closed,
    `P01AC.UnaryIdentity.Expr.reify] #[`P01AC.UnaryIdentity]
  inventoryRuntimeBoundary "Fifteenth" #[`P01AC.RestrictedIdentityV2.identityCheck,
    `P01AC.RestrictedIdentityV2.verifyCertificate,
    `P01AC.RestrictedIdentityV2.makeCertificate] #[`P01AC.RestrictedIdentityV2]
