import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ : Tel} {τ : Nat → Ty}
 (ht : ∀ n, FormE Δ (τ n)) : TypeSubstitution Γ Δ τ := by
 exact TypeSubstitution.empty ht
end HasEMixedReviewReject
