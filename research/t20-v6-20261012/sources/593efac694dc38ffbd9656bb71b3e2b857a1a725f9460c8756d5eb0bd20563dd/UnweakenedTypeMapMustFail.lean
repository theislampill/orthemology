import HasEDependentSubstitution
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
example {Γ Δ : Tel} {σ : Nat → Poly}
    (hσ : Structural.TypedSubstitution Γ Δ σ) :
    Structural.TypedSubstitution (twkTel Γ) (twkTel Δ) σ := hσ
