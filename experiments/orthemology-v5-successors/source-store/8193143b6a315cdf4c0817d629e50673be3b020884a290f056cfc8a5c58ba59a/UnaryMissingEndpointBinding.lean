import UnaryExpressions
namespace P01AC.UnaryIdentity.NegativeControls
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
-- Source equality does not establish identity of separately supplied endpoints.
example (e f : Expr) (p q : Poly) :
    (∀ ρ, F (.identity (arr N N) p q) ρ zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := by
  exact bound_F_identity_iff_denote e f p q
end P01AC.UnaryIdentity.NegativeControls
