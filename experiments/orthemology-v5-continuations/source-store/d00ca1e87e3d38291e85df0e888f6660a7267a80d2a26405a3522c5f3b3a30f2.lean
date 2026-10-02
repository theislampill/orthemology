import ArbitraryPattern
import Q8Measure

open Set MeasureTheory Filter
namespace OrthemologyMeasure

noncomputable def spike {X : Type*} (x : X) : X → Bool :=
  membershipPattern (fun i => {i}) x

theorem spike_measurable {X : Type*} [MeasurableSpace X] [MeasurableSingletonClass X] :
    Measurable (spike (X := X)) :=
  arbitraryPattern_measurable fun i => measurableSet_singleton i

theorem spike_ne_zero {X : Type*} (x : X) : spike x ≠ (fun _ => false) := by
  intro h
  have hx := congrFun h x
  simp [spike, membershipPattern] at hx

theorem spike_coordinate_ae {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (i : X) (hi : μ {i} = 0) :
    (fun x => spike x i) =ᵐ[μ] (fun _ => false) := by
  rw [Filter.EventuallyEq, ae_iff]
  have he : {x | ¬spike x i = false} = {i} := by
    ext x
    simp [spike, membershipPattern]
  rw [he]
  exact hi

open P02A2.Q8Measure

theorem fairCantor_singleton_zero (x : Cantor) : fairCantor {x} = 0 := by
  have he : law (fun _ => true) = fairCantor := by
    have hs : switched (fun _ => true) = id := by
      funext y n
      simp [switched]
    rw [law, hs, Measure.map_id]
  rw [← he]
  exact eventually_singleton_zero (fun _ => true) 0 (by intros; rfl) x

/-- A concrete nonatomic source: equal product laws need not imply that two
uncountably indexed Boolean functions agree at even one source point. -/
theorem spike_law_dirac : fairCantor.map (spike (X := Cantor)) =
    Measure.dirac (fun _ : Cantor => false) := by
  have he := product_map_congr_coordinate_ae fairCantor spike_measurable
    (measurable_const : Measurable (fun _ : Cantor => fun _ : Cantor => false))
    (fun i => spike_coordinate_ae fairCantor i (fairCantor_singleton_zero i))
  simpa [Measure.map_const] using he

theorem spike_not_ae_zero :
    ¬ (spike (X := Cantor) =ᵐ[fairCantor] (fun _ => fun _ => false)) := by
  intro h
  obtain ⟨x, hx⟩ := h.exists
  exact spike_ne_zero x hx

/-- The all-zero singleton is not an observable event in this uncountable
product sigma-algebra. It cannot be smuggled in as a measurable decoder. -/
theorem zero_pattern_not_measurable :
    ¬ MeasurableSet ({fun _ : Cantor => false} : Set (Cantor → Bool)) := by
  intro hS
  have he : (spike (X := Cantor)) ⁻¹' {fun _ : Cantor => false} = ∅ := by
    ext x
    simp [spike_ne_zero]
  have hm := Measure.map_apply (μ := fairCantor) spike_measurable hS
  rw [spike_law_dirac, he, measure_empty] at hm
  have hd : Measure.dirac (fun _ : Cantor => false) {fun _ : Cantor => false} = 1 :=
    Measure.dirac_apply_of_mem rfl
  rw [hd] at hm
  exact one_ne_zero hm

end OrthemologyMeasure
#print axioms OrthemologyMeasure.spike_law_dirac
#print axioms OrthemologyMeasure.spike_not_ae_zero

#print axioms OrthemologyMeasure.zero_pattern_not_measurable
