import OpaqueSearch
import RandomizedFinite

namespace CoveringKernel
open MeasureTheory
variable {α Ω : Type*} [Fintype α] [DecidableEq α] [MeasurableSpace Ω]

/-- Fixed maximal bad sets index worlds, independently of the coin outcome.
Each complete seed selects an ordinary deterministic policy on the same family. -/
theorem randomized_ae_cap_lower_bound {F : Finset (Finset α)} {O : Type*}
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy F O)
    (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (q k N : ℕ)
    (hu : Uniform q F) (hop : Opaque k observe failedReply)
    (hcap : ∀ T : Finset α, T.card = k →
      ∀ᵐ ω ∂μ, SuccessWithin (π ω) observe T N) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  let W := {T : Finset α // T.card = k}
  obtain ⟨ω, hω⟩ := RandomizedFinite.exists_coin_success_all μ
    (fun (T : W) ω => SuccessWithin (π ω) observe T.val N)
    (fun T => hcap T.val T.property)
  exact deterministic_cap_lower_bound (π ω) observe failedReply q k N hu hop
    (fun T hT => hω ⟨T, hT⟩)

/-- One fixed bad set defeats any smaller cap on a non-null set of seeds.
This conclusion does not select the bad set after drawing coins. -/
theorem randomized_below_cover_fixed_failure {F : Finset (Finset α)} {O : Type*}
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy F O)
    (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (q k N : ℕ)
    (hu : Uniform q F) (hop : Opaque k observe failedReply)
    (hsmall : N < coveringNumber α (Fintype.card α-q) k) :
    ∃ T : Finset α, T.card = k ∧
      ¬ (∀ᵐ ω ∂μ, SuccessWithin (π ω) observe T N) := by
  classical
  by_contra h
  push_neg at h
  have hl := randomized_ae_cap_lower_bound μ π observe failedReply q k N hu hop h
  omega

#print axioms randomized_ae_cap_lower_bound
#print axioms randomized_below_cover_fixed_failure
end CoveringKernel
