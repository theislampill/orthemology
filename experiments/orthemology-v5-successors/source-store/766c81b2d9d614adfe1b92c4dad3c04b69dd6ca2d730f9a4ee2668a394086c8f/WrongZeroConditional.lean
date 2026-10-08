import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example : identityCheck (.ifZero (.constant 0) (.constant 5) (.constant 11) : Expr 0) (.constant 11) = true := by decide
