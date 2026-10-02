import Mathlib.MeasureTheory.Measure.Typeclasses.SFinite
import Mathlib.MeasureTheory.Measure.Map
import Mathlib.Tactic

open Set Filter MeasureTheory
open scoped ENNReal Topology

namespace OrthemologyMeasure

variable {Ω α : Type*} [MeasurableSpace Ω] [MeasurableSpace α]
variable (μ : Measure Ω)

/-- Positive point support, not the class of arbitrary measure-theoretic atoms. -/
def positivePoints (ν : Measure α) : Set α := {y | 0 < ν {y}}

theorem positivePoints_countable (ν : Measure α) [SFinite ν]
    [MeasurableSingletonClass α] : (positivePoints ν).Countable := by
  simpa [positivePoints] using
    (Measure.countable_meas_level_set_pos (μ := ν) (g := id) measurable_id)

/-- The event that the realised observation has positive singleton mass. -/
def positiveEvent (Y : Ω → α) : Set Ω :=
  {ω | 0 < μ (Y ⁻¹' {Y ω})}

theorem positiveEvent_measurable [SFinite μ] [MeasurableSingletonClass α]
    {Y : Ω → α} (hY : Measurable Y) : MeasurableSet (positiveEvent μ Y) := by
  have hc : ({y : α | 0 < μ (Y ⁻¹' {y})} : Set α).Countable := by
    simpa using (Measure.countable_meas_level_set_pos (μ := μ) (g := Y) hY)
  exact hY hc.measurableSet

/-- Coherent refinement preserves containment of positive-cell events. -/
theorem positiveEvent_refinement {Y Z : Ω → α} {h : α → α}
    (coherent : ∀ ω, Y ω = h (Z ω)) :
    positiveEvent μ Z ⊆ positiveEvent μ Y := by
  intro ω hω
  change 0 < μ (Z ⁻¹' {Z ω}) at hω
  change 0 < μ (Y ⁻¹' {Y ω})
  apply lt_of_lt_of_le hω
  apply measure_mono
  intro ξ hξ
  change Z ξ = Z ω at hξ
  change Y ξ = Y ω
  rw [coherent ξ, coherent ω, hξ]

def fullObservation (Y : ℕ → Ω → α) (ω : Ω) : ℕ → α := fun n => Y n ω

theorem full_cell_eq_iInter (Y : ℕ → Ω → α) (ω : Ω) :
    fullObservation Y ⁻¹' {fullObservation Y ω} =
      ⋂ n, (Y n ⁻¹' {Y n ω}) := by
  ext ξ
  simp only [mem_preimage, mem_singleton_iff, mem_iInter]
  exact funext_iff

theorem positiveEvent_full_subset (Y : ℕ → Ω → α) (n : ℕ) :
    positiveEvent μ (fullObservation Y) ⊆ positiveEvent μ (Y n) := by
  intro ω hω
  change 0 < μ (fullObservation Y ⁻¹' {fullObservation Y ω}) at hω
  change 0 < μ (Y n ⁻¹' {Y n ω})
  apply lt_of_lt_of_le hω
  apply measure_mono
  intro ξ hξ
  change fullObservation Y ξ = fullObservation Y ω at hξ
  exact congrFun hξ n

/-- This measurable decomposition gives the residual without algebraic placeholder masses. -/
theorem residual_mass_identity [SFinite μ] [MeasurableSingletonClass α]
    (Y : ℕ → Ω → α) (hY : ∀ n, Measurable (Y n)) :
    μ (⋂ n, positiveEvent μ (Y n)) =
      μ (positiveEvent μ (fullObservation Y)) +
      μ ((⋂ n, positiveEvent μ (Y n)) \ positiveEvent μ (fullObservation Y)) := by
  have hf : Measurable (fullObservation Y) := measurable_pi_lambda _ hY
  have hm := positiveEvent_measurable μ hf
  have hs : positiveEvent μ (fullObservation Y) ⊆ ⋂ n, positiveEvent μ (Y n) := by
    exact subset_iInter fun n => positiveEvent_full_subset μ Y n
  have hi : (⋂ n, positiveEvent μ (Y n)) ∩ positiveEvent μ (fullObservation Y) =
      positiveEvent μ (fullObservation Y) := inter_eq_right.mpr hs
  have he := measure_diff_add_inter (μ := μ) (⋂ n, positiveEvent μ (Y n)) hm
  rw [hi, add_comm] at he
  exact he.symm

end OrthemologyMeasure

#print axioms OrthemologyMeasure.positivePoints_countable
#print axioms OrthemologyMeasure.positiveEvent_measurable
#print axioms OrthemologyMeasure.positiveEvent_refinement
#print axioms OrthemologyMeasure.full_cell_eq_iInter
#print axioms OrthemologyMeasure.positiveEvent_full_subset
#print axioms OrthemologyMeasure.residual_mass_identity
