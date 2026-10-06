import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example (e f : Expr 2) : identityCheck e f = true ↔ FragmentValid e f := identityCheck_iff_fragmentValid e f
example (e f : Expr 0) : (∃ c, verifyCertificate e f c = true) ↔ FragmentValid e f := finite_certificate_complete e f
