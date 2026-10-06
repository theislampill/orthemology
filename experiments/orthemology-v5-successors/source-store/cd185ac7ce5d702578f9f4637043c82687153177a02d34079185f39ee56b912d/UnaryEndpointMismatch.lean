import UnaryExpressions
namespace P01AC.UnaryIdentity.NegativeControls
open OrthemologyV2 OrthemologyV3 P01D P01R
-- Literal compiler binding cannot be manufactured for arbitrary raw endpoints.
example : LiteralEndpoints (.constant 0) (.constant 0) (.atom .k) (.atom .i) := by
  exact ⟨rfl, rfl⟩
end P01AC.UnaryIdentity.NegativeControls
