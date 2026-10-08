import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example : verifyCertificate (.constant 0 : Expr 0) (.constant 1) (makeCertificate (.constant 0)) = true := by decide
