import TypeSubstitutionApplications
namespace HasEMixedReviewReject
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
example {Γ Δ : Tel} {p : Poly} {A : Ty} {σ : Nat → Poly} {τ : Nat → Ty}
 (hp : HasE Γ p A) (hc : P01AC.Ctx Δ) (h : P01AC.MixedSubstitution Γ Δ σ τ) :
 P01AC.Has Δ (psub σ p) (mixed σ τ A) := by
 exact P01AC.has_mixed hp hc h
end HasEMixedReviewReject
