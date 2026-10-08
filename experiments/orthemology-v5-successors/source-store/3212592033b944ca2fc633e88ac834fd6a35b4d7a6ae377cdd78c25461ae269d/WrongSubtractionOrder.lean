import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
example : reverseSubPR.denote (cons 2 (cons 5 (fun _ => 0))) = 0 := by rw [reverseSubPR_denote]; rfl
