import Mathlib.MeasureTheory.Measure.Typeclasses.SFinite
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.MeasureTheory.Measure.Map
import Mathlib.MeasureTheory.Measure.Restrict
import Mathlib.Tactic

/-! New, UNEXECUTED proof candidates at the exact 4.19.0/c44... pin.
Theorems below are actual-measure prerequisites, not kernel evidence.
Real-valued defect identities additionally require finiteness before toReal. -/
namespace P02A2
open Set MeasureTheory
open scoped ENNReal
variable {X Y : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]

noncomputable def positive (μ : Measure X) : Set X := {x | 0 < μ {x}}
noncomputable def mass (μ : Measure X) : ℝ≥0∞ := μ (positive μ)
noncomputable def defect (μ : Measure X) : ℝ := 1 - (mass μ).toReal

theorem positive_countable (μ : Measure X) [SFinite μ] : (positive μ).Countable := by
  simpa only [positive] using
    (Measure.countable_meas_pos_of_disjoint_iUnion (μ := μ)
      (As := fun x : X => ({x} : Set X))
      (fun x => measurableSet_singleton x)
      (fun x y hxy => disjoint_singleton.mpr hxy))

theorem positive_measurable (μ : Measure X) [SFinite μ] :
    MeasurableSet (positive μ) := (positive_countable μ).measurableSet

theorem positive_le_total (μ : Measure X) : mass μ ≤ μ univ :=
  measure_mono (subset_univ _)

theorem positive_mem_conull (μ : Measure X) {x : X} {A : Set X}
    (hx : x ∈ positive μ) (hA : μ Aᶜ = 0) : x ∈ A := by
  by_contra h
  have hs : ({x} : Set X) ⊆ Aᶜ := by simpa using h
  exact (ne_of_gt hx) (measure_mono_null hs hA)

theorem positive_subset_inter (μ : Measure X) {ι : Type*} (A : ι → Set X)
    (hA : ∀ i, μ (A i)ᶜ = 0) : positive μ ⊆ ⋂ i, A i := by
  intro x hx
  exact mem_iInter.mpr (fun i => positive_mem_conull μ hx (hA i))

theorem mass_le_conull_inter (μ : Measure X) {ι : Type*} (A : ι → Set X)
    (hA : ∀ i, μ (A i)ᶜ = 0) : mass μ ≤ μ (⋂ i, A i) :=
  measure_mono (positive_subset_inter μ A hA)
-- Mathlib evaluates arbitrary sets through outer measure. An event-probability
-- interpretation of this last inequality still requires measurable intersection.

theorem null_singleton_of_not_positive (μ : Measure X) {x : X}
    (hx : x ∉ positive μ) : μ {x} = 0 := by
  exact le_antisymm (not_lt.mp hx) (zero_le _)

theorem singleton_complement_conull (μ : Measure X) {x : X}
    (hx : x ∉ positive μ) : μ (({x} : Set X)ᶜ)ᶜ = 0 := by
  simpa only [compl_compl] using null_singleton_of_not_positive μ hx

theorem attaining_family (μ : Measure X) :
    (⋂ x : {x // x ∉ positive μ}, ({x.val} : Set X)ᶜ) = positive μ := by
  classical
  ext x
  constructor
  · intro hx
    by_contra hn
    have h := mem_iInter.mp hx ⟨x, hn⟩
    exact h (by simp)
  · intro hx
    apply mem_iInter.mpr
    intro y hxy
    have he : x = y.val := by simpa using hxy
    exact y.property (he ▸ hx)

theorem countable_null (μ : Measure X) {C : Set X} (hC : C.Countable)
    (hz : ∀ x ∈ C, μ {x} = 0) : μ C = 0 := by
  letI : Countable C := hC.to_subtype
  have hU : (⋃ x : C, ({x.val} : Set X)) = C := by ext x; simp
  rw [← hU]
  exact measure_iUnion_null (fun x => hz x.val x.property)

theorem countable_sdiff_positive_null (μ : Measure X) {C : Set X}
    (hC : C.Countable) : μ (C \ positive μ) = 0 := by
  apply countable_null μ (hC.mono diff_subset)
  intro x hx
  exact null_singleton_of_not_positive μ hx.2

theorem mass_eq_countable_superset (μ : Measure X) [SFinite μ]
    {C : Set X} (hC : C.Countable) (hSC : positive μ ⊆ C) : mass μ = μ C := by
  have hI : C ∩ positive μ = positive μ := inter_eq_right.mpr hSC
  have h := measure_inter_add_diff (μ := μ) C (positive_measurable μ)
  rw [hI, countable_sdiff_positive_null μ hC, add_zero] at h
  exact h

theorem countable_carrier_mass_one (μ : Measure X) [SFinite μ]
    {C : Set X} (hC : C.Countable) (hCfull : μ Cᶜ = 0) (hTotal : μ univ = 1) :
    mass μ = 1 := by
  have hSC : positive μ ⊆ C := fun _ hx => positive_mem_conull μ hx hCfull
  rw [mass_eq_countable_superset μ hC hSC]
  have hU := measure_union (μ := μ) disjoint_compl_right hC.measurableSet.compl
  simpa [union_compl_self, hCfull, hTotal] using hU.symm

section Map
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

theorem map_singleton (μ : Measure X) {h : X → Y} (hh : Measurable h) (y : Y) :
    μ.map h {y} = μ (h ⁻¹' {y}) := Measure.map_apply hh (measurableSet_singleton y)

theorem positive_maps_positive (μ : Measure X) {h : X → Y} (hh : Measurable h)
    {x : X} (hx : x ∈ positive μ) : h x ∈ positive (μ.map h) := by
  change 0 < μ.map h {h x}
  rw [map_singleton μ hh]
  exact lt_of_lt_of_le hx (measure_mono (by
    intro z hz
    exact congrArg h (mem_singleton_iff.mp hz)))

theorem positive_subset_preimage (μ : Measure X) {h : X → Y} (hh : Measurable h) :
    positive μ ⊆ h ⁻¹' positive (μ.map h) := by
  intro x hx
  exact positive_maps_positive μ hh hx

theorem mass_map_mono (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) : mass μ ≤ mass (μ.map h) := by
  unfold mass
  rw [Measure.map_apply hh (positive_measurable (μ.map h))]
  exact measure_mono (positive_subset_preimage μ hh)

noncomputable def fibreLaw (μ : Measure X) (h : X → Y) (y : Y) : Measure X :=
  (μ (h ⁻¹' {y}))⁻¹ • μ.restrict (h ⁻¹' {y})

theorem fibre_eval (μ : Measure X) (h : X → Y) (y : Y)
    {B : Set X} (hB : MeasurableSet B) :
    fibreLaw μ h y B = (μ (h ⁻¹' {y}))⁻¹ * μ (B ∩ h ⁻¹' {y}) := by
  simp only [fibreLaw, Measure.smul_apply, smul_eq_mul, Measure.restrict_apply hB]

theorem fibre_total (μ : Measure X) [IsFiniteMeasure μ] {h : X → Y}
    (y : Y) (hw : μ (h ⁻¹' {y}) ≠ 0) : fibreLaw μ h y univ = 1 := by
  rw [fibre_eval μ h y MeasurableSet.univ, univ_inter]
  exact ENNReal.inv_mul_cancel hw (measure_ne_top μ _)
end Map
end P02A2
