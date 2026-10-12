import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ Ξ : Tel} {τ : Nat → Ty} {δ : Nat → Poly}
 (h : TypeSubstitution Γ Δ τ) (hc : CtxE Ξ) (g : TypedSubstitution Δ Ξ δ) :
 Structural.MixedSubstitution Γ Ξ δ τ := by
 exact h.thenTerm hc g
end HasEMixedReviewReject
