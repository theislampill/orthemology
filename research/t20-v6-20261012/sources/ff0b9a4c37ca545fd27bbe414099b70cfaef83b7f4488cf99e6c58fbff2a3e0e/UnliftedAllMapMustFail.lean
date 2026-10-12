import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
 (h : Structural.MixedSubstitution Γ Δ σ τ) (hc : CtxE Δ) :
 Structural.MixedSubstitution (twkTel Γ) (twkTel Δ) σ τ := by
 exact h.twk hc
end HasEMixedReviewReject
