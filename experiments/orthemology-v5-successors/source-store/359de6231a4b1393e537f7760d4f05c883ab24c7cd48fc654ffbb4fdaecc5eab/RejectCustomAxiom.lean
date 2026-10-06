import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
axiom fake : False
theorem bad : False := fake
#audit_safe_closure bad
