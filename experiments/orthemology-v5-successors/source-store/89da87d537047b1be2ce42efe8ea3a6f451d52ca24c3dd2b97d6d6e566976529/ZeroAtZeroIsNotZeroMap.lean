import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example : zeroTest ([(fun _ : Fin 1 => 1, 1)] : Sparse 1) = true := by decide
