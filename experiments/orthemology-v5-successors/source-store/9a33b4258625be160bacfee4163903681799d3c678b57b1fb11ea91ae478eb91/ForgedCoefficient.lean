import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example : coeffEqual ([(fun _ : Fin 1 => 0, 5)] : Sparse 1) [(fun _ => 0, 4)] = true := by decide
