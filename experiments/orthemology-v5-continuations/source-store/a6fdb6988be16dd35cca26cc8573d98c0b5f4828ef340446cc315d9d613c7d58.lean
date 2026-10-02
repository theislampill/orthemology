import CompactObservationBoundary

noncomputable section
open MeasureTheory Filter Set
open scoped Topology

namespace Orthemology.Tranche2.CompactBoundaryControls

def reciprocal (n : ℕ) : ℝ := 1 / ((n : ℝ)+1)
lemma reciprocal_pos (n : ℕ) : 0 < reciprocal n := by unfold reciprocal; positivity
lemma reciprocal_le_one (n : ℕ) : reciprocal n ≤ 1 := by
  unfold reciprocal
  exact (div_le_iff₀ (by positivity)).mpr (by simp)
lemma reciprocal_tendsto : Tendsto reciprocal atTop (𝓝 0) :=
  tendsto_one_div_add_atTop_nhds_zero_nat

lemma eventually_in_shrinking_target (θ : ℕ) :
    ∀ᶠ n in atTop, reciprocal n ∈ Ioc 0 (reciprocal θ) := by
  have hh : ∀ᶠ n in atTop, reciprocal n < reciprocal θ :=
    reciprocal_tendsto (Iio_mem_nhds (reciprocal_pos θ))
  exact hh.mono (fun n hn => ⟨reciprocal_pos n, hn.le⟩)

lemma no_common_shrinking_target : ¬∃ a : ℝ, ∀ θ : ℕ, a ∈ Ioc 0 (reciprocal θ) := by
  rintro ⟨a,ha⟩
  have hpos := (ha 0).1
  have hle : a ≤ 0 := ge_of_tendsto reciprocal_tendsto
    (Filter.Eventually.of_forall (fun n => (ha n).2))
  linarith

lemma target_not_closed : ¬IsClosed (Ioc (0 : ℝ) 1) := by
  intro hclosed
  have hz := hclosed.mem_of_tendsto reciprocal_tendsto
    (Filter.Eventually.of_forall (fun n => (show reciprocal n ∈ Ioc 0 1 from
      ⟨reciprocal_pos n,reciprocal_le_one n⟩)))
  exact (lt_irrefl 0) hz.1

/-- Removing closedness fails despite genuine compact confinement, identical
nonzero probability laws and exact eventual membership in each fixed target. -/
theorem nonclosed_compact_confinement_counterexample :
    IsCompact (Icc (0 : ℝ) 1) ∧
    (∀ᵐ _ω ∂(Measure.dirac () : Measure Unit), ∀ᶠ n in atTop, reciprocal n ∈ Icc 0 1) ∧
    (∀ θ : ℕ, ∀ᵐ _ω ∂(Measure.dirac () : Measure Unit),
      ∀ᶠ n in atTop, reciprocal n ∈ Ioc 0 (reciprocal θ)) ∧
    ¬∃ a ∈ Icc (0 : ℝ) 1, ∀ θ : ℕ, a ∈ Ioc 0 (reciprocal θ) := by
  refine ⟨isCompact_Icc, ?_, ?_, ?_⟩
  · exact Filter.Eventually.of_forall (fun _ => Filter.Eventually.of_forall
      (fun n => ⟨(reciprocal_pos n).le,reciprocal_le_one n⟩))
  · intro θ
    exact Filter.Eventually.of_forall (fun _ => eventually_in_shrinking_target θ)
  · rintro ⟨a,_,ha⟩
    exact no_common_shrinking_target ⟨a,ha⟩

lemma naturals_not_compact : ¬IsCompact (Set.univ : Set ℕ) := by
  rw [isCompact_iff_finite]
  exact Set.infinite_univ

/-- Removing compactness fails with closed targets and identical nonzero laws. -/
theorem noncompact_closed_targets_counterexample :
    (∀ θ : ℕ, IsClosed (Ici θ)) ∧
    (∀ θ : ℕ, ∀ᵐ _ω ∂(Measure.dirac () : Measure Unit), ∀ᶠ n in atTop, n ∈ Ici θ) ∧
    ¬∃ a : ℕ, ∀ θ : ℕ, a ∈ Ici θ := by
  refine ⟨fun _ => isClosed_Ici, ?_, ?_⟩
  · intro θ
    exact Filter.Eventually.of_forall (fun _ => eventually_ge_atTop θ)
  · rintro ⟨a,ha⟩
    have hh := ha (a+1)
    exact Nat.not_succ_le_self a hh

#print axioms nonclosed_compact_confinement_counterexample
#print axioms noncompact_closed_targets_counterexample
#print axioms target_not_closed
#print axioms naturals_not_compact
end Orthemology.Tranche2.CompactBoundaryControls
