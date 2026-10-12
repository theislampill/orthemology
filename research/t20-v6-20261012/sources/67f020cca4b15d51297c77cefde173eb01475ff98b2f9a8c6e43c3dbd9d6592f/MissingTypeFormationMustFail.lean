import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
 (ht : ∀ n, TyScoped Δ.length (τ n))
 (hl : ∀ {n A}, Lookup Γ n A → HasE Δ (σ n) (mixed σ τ A)) :
 Structural.MixedSubstitution Γ Δ σ τ := ⟨ht, hl⟩
end HasEMixedReviewReject
