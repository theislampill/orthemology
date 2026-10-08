import IndexedCompletionForgetting

set_option autoImplicit false

namespace IndexedCompletion

open Set Filter
open scoped Topology

universe u
variable {X : ℕ → Type u}
variable [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)]

/-- Ordinary real-valued diameter convergence; below-coordinate range padding is immaterial to the limit. -/
def DiameterShrinking (f : Bonding X) : Prop :=
  ∀ i, Tendsto (fun j => Metric.diam (extensionRange f i j)) atTop (𝓝 0)

omit [∀ i, Nonempty (X i)] in
/-- Compactness ensures all diameters are genuinely bounded, avoiding Mathlib's unbounded-diameter convention. -/
theorem coordinate_forgetting_iff_diameter (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    CoordinateForgetting f ↔ DiameterShrinking f := by
  constructor
  · intro hd i
    apply Metric.tendsto_atTop.mpr
    intro ε hε
    obtain ⟨N, hN⟩ := hd i (ε / 2) (half_pos hε)
    refine ⟨max i N, fun j hj => ?_⟩
    have hij : i ≤ j := (le_max_left i N).trans hj
    have hNj : N ≤ j := (le_max_right i N).trans hj
    have hdiam : Metric.diam (extensionRange f i j) ≤ ε / 2 := by
      apply Metric.diam_le_of_forall_dist_le (half_pos hε).le
      rw [extensionRange_of_le f i j hij]
      rintro _ ⟨u, rfl⟩ _ ⟨v, rfl⟩
      exact (hN j hNj hij u v).le
    rw [Real.dist_eq, sub_zero, abs_of_nonneg Metric.diam_nonneg]
    exact hdiam.trans_lt (half_lt_self hε)
  · intro hd i ε hε
    obtain ⟨N, hN⟩ := Metric.tendsto_atTop.mp (hd i) ε hε
    refine ⟨N, fun j hj hij u v => ?_⟩
    have hdiam : Metric.diam (extensionRange f i j) < ε := by
      have h := hN j hj
      rwa [Real.dist_eq, sub_zero, abs_of_nonneg Metric.diam_nonneg] at h
    apply lt_of_le_of_lt _ hdiam
    apply Metric.dist_le_diam_of_mem (extensionRange_closed f hf i j).isCompact.isBounded
    · rw [extensionRange_of_le f i j hij]
      exact ⟨u, rfl⟩
    · rw [extensionRange_of_le f i j hij]
      exact ⟨v, rfl⟩

/-- Full nonuniform repair, including actual diameter limits and fixed-horizon forgetting. -/
theorem nonuniform_four_way (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    (AllSingleton f ↔ UniqueRealization f) ∧
    (UniqueRealization f ↔ DiameterShrinking f) ∧
    (DiameterShrinking f ↔ HorizonForgetting f) := by
  have hc := nonuniform_completion_equivalences f hf
  have hd := coordinate_forgetting_iff_diameter f hf
  exact ⟨hc.1, hc.1.symm.trans (hc.2.1.trans hd), hd.symm.trans hc.2.2⟩

end IndexedCompletion
