import CompactBoundaryControls

open MeasureTheory Filter Set
open scoped Topology
open Orthemology.Tranche2.CompactBoundaryControls

namespace CompactConclusionAudit

theorem closed_reciprocal_targets_eventually_met (θ : ℕ) :
    IsClosed (Icc (0 : ℝ) (reciprocal θ)) ∧
    ∀ᶠ n in atTop, reciprocal n ∈ Icc 0 (reciprocal θ) := by
  refine ⟨isClosed_Icc, ?_⟩
  exact (eventually_in_shrinking_target θ).mono (fun n hn => ⟨hn.1.le,hn.2⟩)

theorem unique_common_closed_target (a : ℝ) :
    (∀ θ : ℕ, a ∈ Icc 0 (reciprocal θ)) ↔ a = 0 := by
  constructor
  · intro h
    have hle : a ≤ 0 := ge_of_tendsto reciprocal_tendsto
      (Eventually.of_forall (fun n => (h n).2))
    exact le_antisymm hle (h 0).1
  · intro h
    subst a
    exact fun θ => ⟨le_rfl,(reciprocal_pos θ).le⟩

/-- Compactness can provide a common point that the observed sequence never
selects; the arbitrary-family conclusion is an existence statement. -/
theorem no_observed_output_common (n : ℕ) :
    ¬ ∀ θ : ℕ, reciprocal n ∈ Icc 0 (reciprocal θ) := by
  intro h
  have hz := (unique_common_closed_target (reciprocal n)).mp h
  have hp := reciprocal_pos n
  linarith

theorem no_uniform_simultaneous_tail :
    ¬ ∀ᶠ n in atTop, ∀ θ : ℕ, reciprocal n ∈ Icc 0 (reciprocal θ) := by
  intro h
  obtain ⟨n,hn⟩ := h.exists
  exact no_observed_output_common n hn

#print axioms closed_reciprocal_targets_eventually_met
#print axioms unique_common_closed_target
#print axioms no_observed_output_common
#print axioms no_uniform_simultaneous_tail
end CompactConclusionAudit
