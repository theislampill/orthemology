import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example : coeffEqual (normalise (fun _ => false) (.variable ⟨0, by decide⟩ : Expr 1)) [(fun _ => 1, 1)] = true := by decide
