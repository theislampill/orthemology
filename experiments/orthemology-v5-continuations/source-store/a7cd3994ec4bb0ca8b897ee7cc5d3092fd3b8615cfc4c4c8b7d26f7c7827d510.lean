import Mathlib

/-!
P02 separate research candidate. NOT EXECUTED.
Target: Lean 4.19.0, mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b.
These are only the small genuine-measure prerequisites named below.
No claim that the full U05, CV-R or CV-C obligation is formalised here.
-/
namespace P02
open Set MeasureTheory
open scoped ENNReal

variable {α : Type*} [MeasurableSpace α] [MeasurableSingletonClass α]

/-- Positive singleton mass; not the topological support or general measure atoms. -/
def positiveSingletons (μ : Measure α) : Set α := {x | 0 < μ {x}}

noncomputable def pointMass (μ : Measure α) : ℝ≥0∞ := μ (positiveSingletons μ)
noncomputable def singletonDefect (μ : Measure α) : ℝ≥0∞ := 1 - pointMass μ

theorem positiveSingletons_countable (μ : Measure α) [IsFiniteMeasure μ] :
    (positiveSingletons μ).Countable := by
  simpa only [positiveSingletons] using
    (Measure.countable_meas_pos_of_disjoint_iUnion (μ := μ)
      (As := fun x : α => ({x} : Set α))
      (fun x => measurableSet_singleton x)
      (fun x y hxy => disjoint_singleton.mpr hxy))

theorem positiveSingletons_measurable (μ : Measure α) [IsFiniteMeasure μ] :
    MeasurableSet (positiveSingletons μ) :=
  (positiveSingletons_countable μ).measurableSet

theorem positiveSingleton_mem_of_null_compl (μ : Measure α) {x : α} {A : Set α}
    (hx : x ∈ positiveSingletons μ) (hA : μ Aᶜ = 0) : x ∈ A := by
  by_contra hnot
  have hs : ({x} : Set α) ⊆ Aᶜ := by
    intro y hy
    have hyx : y = x := by simpa only [mem_singleton_iff] using hy
    subst y
    exact hnot
  have hz : μ ({x} : Set α) = 0 := measure_mono_null hs hA
  exact (ne_of_gt hx) hz

theorem positiveSingletons_subset_conull_intersection (μ : Measure α)
    {ι : Type*} (A : ι → Set α) (hA : ∀ i, μ (A i)ᶜ = 0) :
    positiveSingletons μ ⊆ ⋂ i, A i := by
  intro x hx
  exact mem_iInter.mpr (fun i => positiveSingleton_mem_of_null_compl μ hx (hA i))

end P02
