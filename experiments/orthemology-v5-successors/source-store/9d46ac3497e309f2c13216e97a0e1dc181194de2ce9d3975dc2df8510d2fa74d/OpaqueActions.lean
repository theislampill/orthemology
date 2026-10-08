import OpaqueSearch
import RandomizedFinite
import Availability

/-! Command-complete adaptive lower bound. An action is arbitrary caller data
(e.g. selected path, full command, fresh nonce). `support` extracts only its
selected labels. History retains the complete action and complete observation.
Replies may depend on that entire history, not just an attempt index. -/
namespace CoveringKernel.Actions
open Finset MeasureTheory
variable {α Action Obs : Type*} [Fintype α] [DecidableEq α]

abbrev Policy (Action Obs : Type*) := List (Action × Obs) → Action

def history (π : Policy Action Obs)
    (reply : List (Action × Obs) → Action → Obs) : ℕ → List (Action × Obs)
  | 0 => []
  | n+1 => let h := history π reply n; (π h, reply h (π h)) :: h

def spine (π : Policy Action Obs) (failed : List (Action × Obs) → Action → Obs)
    (n : ℕ) : Action := π (history π failed n)

def portfolio (support : Action → Finset α) (π : Policy Action Obs)
    (failed : List (Action × Obs) → Action → Obs) (N : ℕ) : Finset (Finset α) :=
  (range N).image (fun n => support (spine π failed n))

def SuccessWithin (support : Action → Finset α) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (T : Finset α) (N : ℕ) : Prop :=
  ∃ n < N, Disjoint (support (π (history π (observe T) n))) T

/-- Only failure prefixes that are still compatible with T are constrained.
Nothing is assumed about a reply after a success, or an unreachable history.
Every coordinate of the observation, including cancellation, must agree. -/
def Opaque (support : Action → Finset α) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (k : ℕ) : Prop :=
  ∀ T : Finset α, T.card = k → ∀ n,
    (∀ i ≤ n, ¬Disjoint (support (spine π failed i)) T) →
    observe T (history π failed n) (spine π failed n) =
      failed (history π failed n) (spine π failed n)

omit [Fintype α] [DecidableEq α] in
theorem common_history_of_spine_failure
    (support : Action → Finset α) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (k : ℕ)
    (hop : Opaque support π observe failed k)
    (T : Finset α) (hT : T.card = k) (N : ℕ)
    (hbad : ∀ i < N, ¬Disjoint (support (spine π failed i)) T) :
    history π (observe T) N = history π failed N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    have heq := ih (fun i hi => hbad i (by omega))
    have hr := hop T hT N (fun i hi => hbad i (by omega))
    simp only [spine] at hr
    simp only [history, heq]
    rw [hr]

omit [Fintype α] [DecidableEq α] in
theorem actual_failure_history_and_spine
    (support : Action → Finset α) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (k : ℕ)
    (hop : Opaque support π observe failed k)
    (T : Finset α) (hT : T.card = k) (N : ℕ)
    (hbad : ∀ i < N, ¬Disjoint (support (π (history π (observe T) i))) T) :
    history π (observe T) N = history π failed N ∧
      ∀ i < N, ¬Disjoint (support (spine π failed i)) T := by
  induction N with
  | zero => exact ⟨rfl, by omega⟩
  | succ N ih =>
    obtain ⟨heq, hprev⟩ := ih (fun i hi => hbad i (by omega))
    have hlast : ¬Disjoint (support (spine π failed N)) T := by
      simpa [spine, heq] using hbad N (by omega)
    have hsp : ∀ i < N+1, ¬Disjoint (support (spine π failed i)) T := by
      intro i hi
      by_cases hin : i < N
      · exact hprev i hin
      · have hieq : i = N := by omega
        simpa [hieq] using hlast
    refine ⟨?_, hsp⟩
    have hr := hop T hT N (fun i hi => hsp i (by omega))
    simp only [spine] at hr
    simp only [history, heq]
    rw [hr]

omit [Fintype α] in
theorem success_iff_portfolio
    (support : Action → Finset α) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (k : ℕ)
    (hop : Opaque support π observe failed k)
    (T : Finset α) (hT : T.card = k) (N : ℕ) :
    SuccessWithin support π observe T N ↔
      ∃ P ∈ portfolio support π failed N, Disjoint P T := by
  classical
  constructor
  · intro hs
    by_contra hn
    have hbad : ∀ i < N, ¬Disjoint (support (spine π failed i)) T := by
      intro i hi hd
      exact hn ⟨_, mem_image.mpr ⟨i, mem_range.mpr hi, rfl⟩, hd⟩
    obtain ⟨i, hi, hd⟩ := hs
    have heq := common_history_of_spine_failure support π observe failed k hop T hT i
      (fun j hj => hbad j (by omega))
    rw [heq] at hd
    exact hbad i hi hd
  · intro hs
    by_contra hn
    have hbad : ∀ i < N, ¬Disjoint (support (π (history π (observe T) i))) T := by
      intro i hi hd
      exact hn ⟨i, hi, hd⟩
    obtain ⟨_, hsp⟩ := actual_failure_history_and_spine support π observe failed k hop T hT N hbad
    obtain ⟨P, hP, hd⟩ := hs
    obtain ⟨i, hi, rfl⟩ := mem_image.mp hP
    exact hsp i (mem_range.mp hi) hd

theorem deterministic_cap_lower_bound
    (F : Finset (Finset α)) (support : Action → Finset α)
    (admitted : ∀ a, support a ∈ F) (π : Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (q k N : ℕ)
    (hu : CoveringKernel.Uniform q F) (hop : Opaque support π observe failed k)
    (hcap : ∀ T : Finset α, T.card = k → SuccessWithin support π observe T N) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  have hpU : CoveringKernel.Uniform q (portfolio support π failed N) := by
    intro P hP
    obtain ⟨i, _, rfl⟩ := mem_image.mp hP
    exact hu _ (admitted _)
  have hpA : CoveringKernel.Available k (portfolio support π failed N) := by
    intro T hT
    exact (success_iff_portfolio support π observe failed k hop T hT N).mp (hcap T hT)
  have hcard : (portfolio support π failed N).card ≤ N := by
    simpa [portfolio] using card_image_le (s := range N)
      (f := fun n => support (spine π failed n))
  exact (coveringNumber_le_portfolio_card q k _ hpU hpA).trans hcard

variable {Ω : Type*} [MeasurableSpace Ω]

/-- Arbitrary random full-command choices. The law μ and every world observation
function are fixed before a seed is drawn; only the policy depends on the seed. -/
theorem randomized_ae_cap_lower_bound
    (F : Finset (Finset α)) (support : Action → Finset α)
    (admitted : ∀ a, support a ∈ F)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (q k N : ℕ)
    (hu : CoveringKernel.Uniform q F) (hop : ∀ ω, Opaque support (π ω) observe failed k)
    (hcap : ∀ T : Finset α, T.card = k →
      ∀ᵐ ω ∂μ, SuccessWithin support (π ω) observe T N) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  let W := {T : Finset α // T.card = k}
  obtain ⟨ω, hω⟩ := RandomizedFinite.exists_coin_success_all μ
    (fun (T : W) ω => SuccessWithin support (π ω) observe T.val N)
    (fun T => hcap T.val T.property)
  exact deterministic_cap_lower_bound F support admitted (π ω) observe failed q k N
    hu (hop ω) (fun T hT => hω ⟨T,hT⟩)

/-- A genuinely fixed root map and actual-root fault set defeat a too-small
almost-sure cap, even with arbitrary full-command actions and reply histories. -/
theorem randomized_below_cover_fixed_root_world
    (F : Finset (Finset α)) (support : Action → Finset α)
    (admitted : ∀ a, support a ∈ F)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hu : CoveringKernel.Uniform q F)
    (hop : ∀ ω, Opaque support (π ω) observe failed (B+c-1))
    (hsmall : N < coveringNumber α (Fintype.card α-q) (B+c-1)) :
    ∃ A : Finset α, A.card = c ∧
      ∃ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A ∧ S.card = B ∧
        ¬ (∀ᵐ ω ∂μ,
          SuccessWithin support (π ω) observe (AttributionKernel.taintedLabels A S) N) := by
  classical
  have hbad : ∃ T : Finset α, T.card = B+c-1 ∧
      ¬ (∀ᵐ ω ∂μ, SuccessWithin support (π ω) observe T N) := by
    by_contra h
    push_neg at h
    have hl := randomized_ae_cap_lower_bound F support admitted μ π observe failed
      q (B+c-1) N hu hop h
    omega
  obtain ⟨T, hT, hfail⟩ := hbad
  obtain ⟨A, hA, S, hSr, hS, hST⟩ :=
    AttributionKernel.maximal_taint_realizable B c hB hc T hT
  exact ⟨A, hA, S, hSr, hS, hST ▸ hfail⟩

#print axioms success_iff_portfolio
#print axioms deterministic_cap_lower_bound
#print axioms randomized_ae_cap_lower_bound
#print axioms randomized_below_cover_fixed_root_world
end CoveringKernel.Actions
