import UnaryExpressions
namespace P01AC.UnaryIdentity.NegativeControls
open P01AC.BooleanPrimitive P01AC.RestrictedIdentity P01AC.PolynomialTestBoundary
/-- Deliberately wrong: choosePR receives THEN before ELSE. -/
def inverted : PR 1 := ternary choosePR
  (binary equalPR (UnaryIdentity.Expr.add .variable (.constant 1)).toPR
    (UnaryIdentity.Expr.constant 3).toPR)
  (UnaryIdentity.Expr.mul .variable (.constant 3)).toPR
  (UnaryIdentity.Expr.add .variable (.constant 8)).toPR
-- Actual value is 9; the correct unequal branch would return 11.
example : inverted.denote (fun _ => 3) = 11 := by rfl
end P01AC.UnaryIdentity.NegativeControls
