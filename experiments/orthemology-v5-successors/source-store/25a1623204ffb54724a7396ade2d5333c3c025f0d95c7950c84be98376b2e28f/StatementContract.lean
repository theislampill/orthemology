import LiteralScalarFusion
namespace ScalarFusionStatementContract
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.ExactScalarFusion
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity.IntensionalBoundary

example : p = variableExpr.closed := rfl
example : q = redundantExpr.closed := rfl
example : literalB = .identity (arr N N) variableExpr.closed redundantExpr.closed := rfl
example : c3 = abstract (abstract (abstract (.atom .i))) := rfl
example : W q = .pi N (.all (.pi (arr (.param 0) (.param 0)) (.pi (.param 0)
    (.identity (.param 0)
      (.app (.app (.var 2) (.var 1)) (.var 0))
      (.app (.app (.app redundantExpr.closed (.var 2)) (.var 1)) (.var 0)))))) := rfl

example :
    ((∃ r, HasE [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed)) ↔
      HasE [] (.atom .i) (.identity (arr N N) variableExpr.closed redundantExpr.closed)) ∧
    ((∃ r, HasE [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed)) ↔
      ∃ h, HasE [] h (W redundantExpr.closed)) ∧
    ((∃ r, HasE [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed)) ↔
      HasE [] (abstract (abstract (abstract (.atom .i)))) (W redundantExpr.closed)) :=
  literal_four_way_iff
end ScalarFusionStatementContract
