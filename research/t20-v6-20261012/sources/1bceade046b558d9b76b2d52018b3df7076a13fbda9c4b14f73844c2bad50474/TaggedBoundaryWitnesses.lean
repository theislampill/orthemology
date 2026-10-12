import Pi3Law

namespace IndependentTaggedAudit
open Set MeasureTheory
open scoped ENNReal NNReal
open OrthemologyTagged P02A2.Q8Measure P02A2

/-- The selector events cover almost every input, but never all inputs. -/
theorem no_pointwise_selector_cover : ¬ ∀ x : Cantor, ∃ i, x ∈ tagEvent i := by
  intro h
  obtain ⟨i,hi⟩ := h allTrue
  exact allTrue_not_tag i hi

/-- Reusing the final prefix coordinate as the first tail bit conditions that bit. -/
theorem unshifted_prefix_coordinate_not_fair :
    fairCantor ({x : Cantor | x 0 = true} ∩ tagEvent 0) = 0 := by
  have he : ({x : Cantor | x 0 = true} ∩ tagEvent 0) = ∅ := by
    apply Set.eq_empty_iff_forall_not_mem.mpr
    intro x hx
    have hz := ((tagEvent_spec 0 x).mp hx.2).2
    simp_all
  rw [he, measure_empty]

/-- A zero-weight row can have deficient mass without affecting weighted full mass. -/
theorem zero_weight_hides_bad_row :
    (∑' i : ℕ, ((if i = 0 then 1 else 0 : ℝ≥0) : ℝ≥0∞) *
      (if i = 0 then 1 else 0 : ℝ≥0∞)) = 1 ∧
    ¬ ∀ i : ℕ, (if i = 0 then 1 else 0 : ℝ≥0∞) = 1 := by
  constructor
  · rw [tsum_eq_single 0]
    · norm_num
    · intro i hi
      simp [hi]
  · intro h
    have := h 1
    norm_num at this

def differentWitness (_ : Unit) (i s _t : ℕ) : Prop := s = i
instance differentWitness_decidable (a : Unit) (i s t : ℕ) : Decidable (differentWitness a i s t) :=
  inferInstanceAs (Decidable (s = i))

/-- Each row may need its own witness; moving exists s outside forall i is false. -/
theorem row_witnesses_need_not_be_uniform :
    defect (pi3Law differentWitness ()) = 0 ∧
    ¬ ∃ s, ∀ i t, differentWitness () i s t := by
  constructor
  · apply (pi3_zero_defect_iff differentWitness ()).mpr
    exact fun i => ⟨i,fun _ => rfl⟩
  · rintro ⟨s,hs⟩
    have h0 := hs 0 0
    have h1 := hs 1 0
    change s = 0 at h0
    change s = 1 at h1
    omega

def halfRows (i : ℕ) (x : Cantor) : Cantor := if i = 0 then (fun _ => false) else x

theorem halfRows_measurable (i : ℕ) : Measurable (halfRows i) := by
  unfold halfRows
  by_cases h : i = 0
  · simp only [h, if_true]
    exact measurable_const
  · simp only [h, if_false]
    exact measurable_id

theorem fair_atomic_mass_zero : mass fairCantor = 0 := by
  have he : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [OrthemologyMeasure.fairCantor_singleton_zero]
    simp only [lt_self_iff_false]
  simp [mass, he]

theorem halfRows_mass (i : ℕ) : mass (fairCantor.map (halfRows i)) = if i = 0 then 1 else 0 := by
  classical
  by_cases h : i = 0
  · have hi : halfRows i = (fun _ : Cantor => fun _ : ℕ => false) := by
      funext x n
      simp [halfRows, h]
    have he : fairCantor.map (halfRows i) = Measure.dirac (fun _ : ℕ => false) := by
      rw [hi, Measure.map_const]
      simp
    rw [he, if_pos h]
    exact countable_carrier_mass_one _ (C := {fun _ : ℕ => false}) (Set.countable_singleton _) (by simp) (by simp)
  · have hi : halfRows i = id := by
      funext x n
      simp [halfRows, h]
    rw [hi, Measure.map_id, if_neg h]
    exact fair_atomic_mass_zero

/-- A non-endpoint actual tagged law has exactly the selector-zero mass. -/
theorem tagged_mixed_mass_half : mass (fairCantor.map (tagged halfRows)) = (1/2 : ℝ≥0∞) := by
  rw [tagged_mass halfRows_measurable]
  simp_rw [halfRows_mass]
  rw [tsum_eq_single 0]
  · norm_num [weight]
  · intro i hi
    simp [hi]

theorem tagged_mixed_defect_half : defect (fairCantor.map (tagged halfRows)) = (1/2 : ℝ) := by
  rw [defect, tagged_mixed_mass_half]
  norm_num

#print axioms no_pointwise_selector_cover
#print axioms unshifted_prefix_coordinate_not_fair
#print axioms zero_weight_hides_bad_row
#print axioms row_witnesses_need_not_be_uniform
#print axioms tagged_mixed_mass_half
#print axioms tagged_mixed_defect_half
end IndependentTaggedAudit
