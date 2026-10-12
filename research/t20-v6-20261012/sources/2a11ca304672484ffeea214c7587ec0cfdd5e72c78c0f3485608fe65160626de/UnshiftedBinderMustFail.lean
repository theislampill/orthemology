import HasEDependentSubstitution
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
example {Γ Δ : Tel} {σ : Nat → Poly} {A B : Ty} {b : Poly}
    (hΔ : CtxE Δ) (hσ : Structural.TypedSubstitution Γ Δ σ)
    (hA : FormE Δ (subst σ A)) (hb : HasE (A :: Γ) b B) :
    HasE (subst σ A :: Δ) (psub (pup σ) b) (subst (pup σ) B) :=
  Structural.has_subst hb (.ext hΔ hA) hσ
