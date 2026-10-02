import P02A2.MeasureCore
import Mathlib

/-! UNEXECUTED countable mixture proof candidates, not kernel claims. -/
namespace P02A2
open Set MeasureTheory
open scoped NNReal ENNReal
variable {X : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]

noncomputable def mixture (w : ℕ → ℝ≥0) (μ : ℕ → Measure X) : Measure X :=
  Measure.sum (fun i => w i • μ i)

noncomputable def commonPositive (μ : ℕ → Measure X) : Set X := ⋃ i, positive (μ i)

theorem commonPositive_countable (μ : ℕ → Measure X) [∀ i, IsFiniteMeasure (μ i)] :
    (commonPositive μ).Countable := Set.countable_iUnion (fun i => positive_countable (μ i))

theorem component_positive_subset_common (μ : ℕ → Measure X) (i : ℕ) :
    positive (μ i) ⊆ commonPositive μ := subset_iUnion (fun j => positive (μ j)) i

theorem mixture_positive_subset_common (w : ℕ → ℝ≥0) (μ : ℕ → Measure X) :
    positive (mixture w μ) ⊆ commonPositive μ := by
  intro x hx
  by_contra hnot
  have hz : ∀ i, μ i {x} = 0 := by
    intro i
    apply null_singleton_of_not_positive
    intro hi
    exact hnot (mem_iUnion.mpr ⟨i,hi⟩)
  have hzero : mixture w μ {x} = 0 := by
    simp [mixture, Measure.sum_apply, hz, measurableSet_singleton]
  exact (ne_of_gt hx) hzero

theorem mass_mixture (w : ℕ → ℝ≥0) (μ : ℕ → Measure X)
    [∀ i, IsFiniteMeasure (μ i)] :
    mass (mixture w μ) = ∑' i, (w i : ℝ≥0∞) * mass (μ i) := by
  have hC := commonPositive_countable μ
  letI : SFinite (mixture w μ) := by unfold mixture; infer_instance
  rw [mass_eq_countable_superset (mixture w μ) hC (mixture_positive_subset_common w μ)]
  unfold mixture
  rw [Measure.sum_apply _ hC.measurableSet]
  apply tsum_congr
  intro i
  rw [Measure.smul_apply]
  change (w i : ℝ≥0∞) * μ i (commonPositive μ) = (w i : ℝ≥0∞) * mass (μ i)
  rw [mass_eq_countable_superset (μ i) hC (component_positive_subset_common μ i)]

theorem mixture_total (w : ℕ → ℝ≥0) (μ : ℕ → Measure X)
    (hμ : ∀ i, μ i univ = 1) (hw : (∑' i, (w i : ℝ≥0∞)) = 1) :
    mixture w μ univ = 1 := by
  simpa [mixture, Measure.sum_apply, hμ, ENNReal.smul_def, smul_eq_mul] using hw
end P02A2
