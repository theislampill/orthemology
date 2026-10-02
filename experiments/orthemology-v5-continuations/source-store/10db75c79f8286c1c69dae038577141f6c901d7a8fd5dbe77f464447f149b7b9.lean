import P02A2.MeasureCore
import Mathlib

/-! UNEXECUTED actual-measure fibre and atom-mass candidates. No disintegration
axiom is used: only positive measurable fibres are normalised. -/
namespace P02A2
open Set MeasureTheory Function
open scoped ENNReal
variable {X Y : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]
  [MeasurableSpace Y] [MeasurableSingletonClass Y]

theorem positive_fibre (μ : Measure X) [IsFiniteMeasure μ] (h : X → Y) (y : Y)
    (hw : μ (h ⁻¹' {y}) ≠ 0) :
    positive (fibreLaw μ h y) = positive μ ∩ h ⁻¹' {y} := by
  ext x
  change (0 < fibreLaw μ h y {x}) ↔ x ∈ positive μ ∧ h x ∈ ({y} : Set Y)
  rw [fibre_eval μ h y (measurableSet_singleton x)]
  by_cases hx : h x ∈ ({y} : Set Y)
  · have hI : ({x} : Set X) ∩ h ⁻¹' {y} = {x} := by
      exact inter_eq_left.mpr (by simpa using hx)
    rw [hI]
    constructor
    · intro hp
      refine ⟨?_, hx⟩
      change 0 < μ {x}
      by_contra hn
      have hz : μ {x} = 0 := le_antisymm (not_lt.mp hn) (zero_le _)
      simpa [hz] using hp
    · rintro ⟨hp, _⟩
      exact ENNReal.mul_pos_iff.mpr ⟨ENNReal.inv_pos.mpr (measure_ne_top μ _), hp⟩
  · have hI : ({x} : Set X) ∩ h ⁻¹' {y} = ∅ := by
      ext z
      simp only [mem_inter_iff, mem_singleton_iff, mem_preimage, mem_empty_iff_false,
        iff_false, not_and]
      intro hz
      subst z
      exact hx
    simp [hI, hx]

theorem weighted_fibre_mass (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) (y : Y) (hw : μ (h ⁻¹' {y}) ≠ 0) :
    μ (h ⁻¹' {y}) * mass (fibreLaw μ h y) = μ (positive μ ∩ h ⁻¹' {y}) := by
  unfold mass
  rw [positive_fibre μ h y hw,
    fibre_eval μ h y ((positive_measurable μ).inter (hh (measurableSet_singleton y)))]
  rw [inter_assoc, inter_self, ← mul_assoc,
    ENNReal.mul_inv_cancel hw (measure_ne_top μ _), one_mul]

theorem positive_fibre_partition (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) :
    (⋃ y : positive (μ.map h), positive μ ∩ h ⁻¹' {y.val}) = positive μ := by
  ext x
  constructor
  · intro hx
    rcases mem_iUnion.mp hx with ⟨y, hy⟩
    exact hy.1
  · intro hx
    exact mem_iUnion.mpr ⟨⟨h x, positive_maps_positive μ hh hx⟩, hx, by simp⟩

theorem mass_as_sum_weighted_fibres (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) :
    mass μ = ∑' y : positive (μ.map h), μ.map h {y.val} * mass (fibreLaw μ h y.val) := by
  classical
  letI : Countable (positive (μ.map h)) := (positive_countable (μ.map h)).to_subtype
  have hd : Pairwise (Disjoint on fun y : positive (μ.map h) =>
      positive μ ∩ h ⁻¹' {y.val}) := by
    intro y z hyz
    apply Set.disjoint_left.mpr
    rintro x hx hy
    have he : y.val = z.val := (mem_singleton_iff.mp hx.2).symm.trans
      (mem_singleton_iff.mp hy.2)
    exact hyz (Subtype.ext he)
  calc
    mass μ = μ (⋃ y : positive (μ.map h), positive μ ∩ h ⁻¹' {y.val}) := by
      rw [positive_fibre_partition μ hh]; rfl
    _ = ∑' y : positive (μ.map h), μ (positive μ ∩ h ⁻¹' {y.val}) :=
      measure_iUnion hd (fun y => (positive_measurable μ).inter (hh (measurableSet_singleton y.val)))
    _ = _ := by
      apply tsum_congr
      intro y
      rw [map_singleton μ hh]
      have hw : μ (h ⁻¹' {y.val}) ≠ 0 := by
        rw [← map_singleton μ hh]
        exact ne_of_gt y.property
      exact (weighted_fibre_mass μ hh y.val hw).symm

noncomputable def diffuseMass (μ : Measure X) : ℝ≥0∞ := μ (positive μ)ᶜ

theorem mass_add_diffuseMass (μ : Measure X) [SFinite μ] :
    mass μ + diffuseMass μ = μ univ := by
  have hp := positive_measurable μ
  simpa only [mass, diffuseMass, union_compl_self] using
    (measure_union (μ := μ) disjoint_compl_right hp.compl).symm

theorem defect_eq_diffuse_toReal (μ : Measure X) [IsProbabilityMeasure μ] :
    defect μ = (diffuseMass μ).toReal := by
  have h := congrArg ENNReal.toReal (mass_add_diffuseMass μ)
  rw [ENNReal.toReal_add (show mass μ ≠ ∞ from measure_ne_top μ _)
    (show diffuseMass μ ≠ ∞ from measure_ne_top μ _)] at h
  simp only [measure_univ, ENNReal.toReal_one] at h
  unfold defect
  linarith


theorem weighted_fibre_diffuse (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) (y : Y) (hw : μ (h ⁻¹' {y}) ≠ 0) :
    μ (h ⁻¹' {y}) * diffuseMass (fibreLaw μ h y) =
      μ ((positive μ)ᶜ ∩ h ⁻¹' {y}) := by
  unfold diffuseMass
  rw [positive_fibre μ h y hw,
    fibre_eval μ h y (((positive_measurable μ).inter (hh (measurableSet_singleton y))).compl)]
  have he : (positive μ ∩ h ⁻¹' {y})ᶜ ∩ h ⁻¹' {y} =
      (positive μ)ᶜ ∩ h ⁻¹' {y} := by ext x; simp only [mem_inter_iff, mem_compl_iff]; tauto
  rw [he, ← mul_assoc, ENNReal.mul_inv_cancel hw (measure_ne_top μ _), one_mul]

theorem diffuse_fibre_identity (μ : Measure X) [IsFiniteMeasure μ]
    {h : X → Y} (hh : Measurable h) :
    diffuseMass μ = diffuseMass (μ.map h) +
      ∑' y : positive (μ.map h), μ.map h {y.val} * diffuseMass (fibreLaw μ h y.val) := by
  classical
  let C := h ⁻¹' positive (μ.map h)
  let E := fun y : positive (μ.map h) => (positive μ)ᶜ ∩ h ⁻¹' {y.val}
  letI : Countable (positive (μ.map h)) := (positive_countable (μ.map h)).to_subtype
  have hC : MeasurableSet C := (positive_measurable (μ.map h)).preimage hh
  have he : (⋃ y, E y) = C \ positive μ := by
    ext x
    simp only [E, C, mem_iUnion, mem_inter_iff, mem_compl_iff, mem_preimage,
      mem_singleton_iff, mem_diff]
    constructor
    · rintro ⟨y, hn, heq⟩
      exact ⟨heq ▸ y.property, hn⟩
    · rintro ⟨hc, hn⟩
      exact ⟨⟨h x, hc⟩, hn, rfl⟩
  have hd : Pairwise (Disjoint on E) := by
    intro y z hyz
    apply Set.disjoint_left.mpr
    rintro x hx hz
    apply hyz
    apply Subtype.ext
    exact (mem_singleton_iff.mp hx.2).symm.trans (mem_singleton_iff.mp hz.2)
  have hm : ∀ y, MeasurableSet (E y) := fun y =>
    (positive_measurable μ).compl.inter (hh (measurableSet_singleton y.val))
  have hSC : positive μ ⊆ C := positive_subset_preimage μ hh
  have hp : (positive μ)ᶜ = Cᶜ ∪ (⋃ y, E y) := by
    rw [he]
    ext x
    simp only [mem_compl_iff, mem_union, mem_diff]
    constructor
    · intro hn; by_cases hc : x ∈ C
      · exact Or.inr ⟨hc, hn⟩
      · exact Or.inl hc
    · rintro (hc | ⟨_,hn⟩)
      · intro hs; exact hc (hSC hs)
      · exact hn
  have hdis : Disjoint Cᶜ (⋃ y, E y) := by
    rw [he]
    exact Set.disjoint_left.mpr (by intro x hx hy; exact hx hy.1)
  unfold diffuseMass
  rw [hp, measure_union hdis (MeasurableSet.iUnion hm), measure_iUnion hd hm,
    Measure.map_apply hh (positive_measurable (μ.map h)).compl]
  congr 1
  apply tsum_congr
  intro y
  rw [map_singleton μ hh]
  exact (weighted_fibre_diffuse μ hh y.val (by
    rw [← map_singleton μ hh]; exact ne_of_gt y.property)).symm

theorem defect_fibre_identity (μ : Measure X) [IsProbabilityMeasure μ]
    {h : X → Y} (hh : Measurable h) :
    defect μ = defect (μ.map h) +
      ∑' y : positive (μ.map h), (μ.map h {y.val}).toReal * defect (fibreLaw μ h y.val) := by
  classical
  haveI : IsProbabilityMeasure (μ.map h) := ⟨by
    rw [Measure.map_apply hh MeasurableSet.univ]; simp⟩
  have hf : ∀ y : positive (μ.map h), μ (h ⁻¹' {y.val}) ≠ 0 := by
    intro y; rw [← map_singleton μ hh]; exact ne_of_gt y.property
  haveI : ∀ y : positive (μ.map h), IsProbabilityMeasure (fibreLaw μ h y.val) :=
    fun y => ⟨fibre_total μ y.val (hf y)⟩
  have hterm : ∀ y : positive (μ.map h),
      μ.map h {y.val} * diffuseMass (fibreLaw μ h y.val) ≠ ∞ := by
    intro y
    rw [map_singleton μ hh, weighted_fibre_diffuse μ hh y.val (hf y)]
    exact measure_ne_top μ _
  have hsum : (∑' y : positive (μ.map h),
      μ.map h {y.val} * diffuseMass (fibreLaw μ h y.val)) ≠ ∞ := by
    have he := diffuse_fibre_identity μ hh
    have hn : diffuseMass μ ≠ ∞ := measure_ne_top μ _
    rw [he] at hn
    exact (ENNReal.add_ne_top.mp hn).2
  rw [defect_eq_diffuse_toReal μ, defect_eq_diffuse_toReal (μ.map h)]
  have he := congrArg ENNReal.toReal (diffuse_fibre_identity μ hh)
  rw [ENNReal.toReal_add (show diffuseMass (μ.map h) ≠ ∞ from measure_ne_top (μ.map h) _) hsum,
    ENNReal.tsum_toReal_eq hterm] at he
  rw [he]
  congr 1
  apply tsum_congr
  intro y
  rw [ENNReal.toReal_mul, defect_eq_diffuse_toReal (fibreLaw μ h y.val)]

end P02A2
