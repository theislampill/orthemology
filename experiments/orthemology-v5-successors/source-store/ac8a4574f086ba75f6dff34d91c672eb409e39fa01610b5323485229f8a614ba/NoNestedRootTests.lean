import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
def bad : Root 1 := .equal (.equal (.constant 0) (.constant 0)) (.constant 1)
