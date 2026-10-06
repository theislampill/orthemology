import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example (e f : Expr 2) (h : identityCheck e f = true) : Has [] (.atom .i) (.identity (Curried 2) e.closed f.closed) := (identityCheck_iff_F_identity e f).mp h
