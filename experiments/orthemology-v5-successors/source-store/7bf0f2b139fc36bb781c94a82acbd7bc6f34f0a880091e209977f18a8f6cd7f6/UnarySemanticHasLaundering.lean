import UnaryExpressions
namespace P01AC.UnaryIdentity.NegativeControls
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
-- A semantic polynomial witness is not a current-Has inhabitant.
example (e f : Expr) (h : ∀ n, e.denote n = f.denote n) :
    ∃ w : Poly, Has [] w (.identity (arr N N) e.closed f.closed) := by
  exact (semantic_witness_iff_denote e f).mpr h
end P01AC.UnaryIdentity.NegativeControls
