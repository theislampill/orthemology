import HasEDependentSubstitution
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
example {Γ Δ : Tel} {σ : Nat → Poly} {p : Poly} {A : Ty}
    (hΔ : CtxE Δ) (hp : HasE Γ p A) (hs : ScopedSub Γ.length Δ.length σ) :
    HasE Δ (psub σ p) (subst σ A) :=
  Structural.has_subst hp hΔ hs
