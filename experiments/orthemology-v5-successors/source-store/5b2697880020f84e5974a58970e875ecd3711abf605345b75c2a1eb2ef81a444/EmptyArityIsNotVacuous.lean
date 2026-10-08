import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
example : Valid (Root.equal (r := 0) (.constant 2) (.constant 2)) (.old (.constant 0)) := by rw [root_equal_zero_iff]; intro v; simp [Arithmetic.denote, Arithmetic.toExpr, Expr.denote]
