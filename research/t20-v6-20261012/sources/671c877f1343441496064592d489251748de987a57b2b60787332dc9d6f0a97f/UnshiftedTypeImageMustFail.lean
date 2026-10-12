import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty} {A : Ty}
 (h : Structural.MixedSubstitution Γ Δ σ τ) (hc : CtxE Δ)
 (ha : FormE Δ (mixed σ τ A)) :
 Structural.MixedSubstitution (A :: Γ) (mixed σ τ A :: Δ) (pup σ) τ := by
 exact h.lift hc ha
end HasEMixedReviewReject
