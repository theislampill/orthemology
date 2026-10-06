import RandomizedSearch
import Availability

/-! Direct bridge to the accepted one-unknown-root-class model. Each lower-bound
bad-label set is realized by one static class and exactly B actual bad roots.
No root map depends on the coin outcome in the randomized conclusion. -/
namespace CoveringKernel
open Finset MeasureTheory
variable {α : Type*} [Fintype α] [DecidableEq α]

theorem available_source_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hk : B+c-1 ≤ Fintype.card α)
    (F : Finset (Finset α)) :
    AttributionKernel.Available B c (F : Set (Finset α)) ↔ Available (B+c-1) F := by
  exact AttributionKernel.available_iff B c hB hc hcm hk (F : Set (Finset α))

theorem source_cover_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hk : B+c-1 ≤ Fintype.card α)
    (F : Finset (Finset α)) :
    AttributionKernel.Available B c (F : Set (Finset α)) ↔
      Covers (B+c-1) (complements F) :=
  (available_source_iff B c hB hc hcm hk F).trans (complement_portfolio_iff _ F)

theorem deterministic_below_cover_fixed_root_world
    {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hu : Uniform q F)
    (hop : Opaque (B+c-1) observe failedReply)
    (hsmall : N < coveringNumber α (Fintype.card α-q) (B+c-1)) :
    ∃ A : Finset α, A.card = c ∧
      ∃ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A ∧ S.card = B ∧
        ¬ SuccessWithin π observe (AttributionKernel.taintedLabels A S) N := by
  classical
  have hbad : ∃ T : Finset α, T.card = B+c-1 ∧ ¬SuccessWithin π observe T N := by
    by_contra h
    push_neg at h
    have hl := deterministic_cap_lower_bound π observe failedReply q (B+c-1) N hu hop h
    omega
  obtain ⟨T, hT, hfail⟩ := hbad
  obtain ⟨A, hA, S, hSr, hS, hST⟩ :=
    AttributionKernel.maximal_taint_realizable B c hB hc T hT
  exact ⟨A, hA, S, hSr, hS, hST ▸ hfail⟩

/-- Upper bound covers every actual fault set of size at most B, including
nonmaximal bad-label sets, under every compatible class map. -/
theorem root_world_cap_attained (B c q : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hq : q ≤ Fintype.card α)
    (hk : B+c-1 ≤ Fintype.card α-q) (O : Type*) :
    ∃ F : Finset (Finset α), Uniform q F ∧ ∃ π : Policy F O,
      ∀ observe : Finset α → ℕ → Path F → O,
      ∀ A : Finset α, A.card = c →
      ∀ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A → S.card ≤ B →
        SuccessWithin π observe (AttributionKernel.taintedLabels A S)
          (coveringNumber α (Fintype.card α-q) (B+c-1)) := by
  obtain ⟨F, hu, ha, hsize⟩ := minimal_portfolio_attained q (B+c-1) hq hk
  have hne := available_nonempty (B+c-1) F (by omega) ha
  have hsource := (available_source_iff B c hB hc hcm (by omega) F).mpr ha
  refine ⟨F, hu, enumeratePolicy F hne O, ?_⟩
  intro observe A hA S hSr hS
  obtain ⟨P, hP, hd⟩ := hsource A hA S hSr hS
  rw [← hsize]
  exact enumerating_policy_hit F hne observe (AttributionKernel.taintedLabels A S)
    ⟨P, hP, (AttributionKernel.disjoint_image_iff A P S).mp hd⟩

variable {Ω : Type*} [MeasurableSpace Ω]

theorem randomized_root_world_ae_cap_lower_bound
    {F : Finset (Finset α)} {O : Type*}
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy F O)
    (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hu : Uniform q F)
    (hop : Opaque (B+c-1) observe failedReply)
    (hcap : ∀ A : Finset α, A.card = c →
      ∀ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A → S.card ≤ B →
        ∀ᵐ ω ∂μ, SuccessWithin (π ω) observe (AttributionKernel.taintedLabels A S) N) :
    coveringNumber α (Fintype.card α-q) (B+c-1) ≤ N := by
  apply randomized_ae_cap_lower_bound μ π observe failedReply q (B+c-1) N hu hop
  intro T hT
  obtain ⟨A, hA, S, hSr, hS, hST⟩ :=
    AttributionKernel.maximal_taint_realizable B c hB hc T hT
  simpa [hST] using hcap A hA S hSr (by omega)

/-- The selected A and S are outside the almost-everywhere quantifier. -/
theorem randomized_below_cover_fixed_root_world
    {F : Finset (Finset α)} {O : Type*}
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy F O)
    (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hu : Uniform q F)
    (hop : Opaque (B+c-1) observe failedReply)
    (hsmall : N < coveringNumber α (Fintype.card α-q) (B+c-1)) :
    ∃ A : Finset α, A.card = c ∧
      ∃ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A ∧ S.card = B ∧
        ¬ (∀ᵐ ω ∂μ,
          SuccessWithin (π ω) observe (AttributionKernel.taintedLabels A S) N) := by
  obtain ⟨T, hT, hfail⟩ :=
    randomized_below_cover_fixed_failure μ π observe failedReply q (B+c-1) N hu hop hsmall
  obtain ⟨A, hA, S, hSr, hS, hST⟩ :=
    AttributionKernel.maximal_taint_realizable B c hB hc T hT
  exact ⟨A, hA, S, hSr, hS, hST ▸ hfail⟩

#print axioms available_source_iff
#print axioms source_cover_iff
#print axioms deterministic_below_cover_fixed_root_world
#print axioms root_world_cap_attained
#print axioms randomized_root_world_ae_cap_lower_bound
#print axioms randomized_below_cover_fixed_root_world
end CoveringKernel
