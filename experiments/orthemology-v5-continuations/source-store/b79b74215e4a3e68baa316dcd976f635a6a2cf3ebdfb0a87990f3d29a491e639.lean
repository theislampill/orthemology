import TaggedRows

open Set MeasureTheory
open scoped NNReal ENNReal
namespace OrthemologyTagged
open P02A2 P02A2.Q8Measure

theorem tag_mass (μ : Measure Cantor) [IsFiniteMeasure μ] (i : ℕ) :
    mass (μ.map (tag i)) = mass μ := by
  have hback : (μ.map (tag i)).map (tail i) = μ := by
    rw [Measure.map_map (tail_measurable i) (tag_measurable i)]
    have he : tail i ∘ tag i = id := by funext y; exact tail_tag i y
    rw [he, Measure.map_id]
  apply le_antisymm
  · have h := mass_map_mono (μ.map (tag i)) (tail_measurable i)
    rw [hback] at h
    exact h
  · exact mass_map_mono μ (tag_measurable i)

noncomputable def weight (i : ℕ) : ℝ≥0 := (1/2)^(i+1)

theorem weights_sum : (∑' i, (weight i : ℝ≥0∞)) = 1 := by
  have h := ENNReal.tsum_geometric_add_one (1/2 : ℝ≥0∞)
  norm_num [weight, ENNReal.coe_pow, ENNReal.inv_pow] at h ⊢
  exact h.trans (ENNReal.inv_mul_cancel (by norm_num) (by norm_num))

theorem weight_ne_zero (i : ℕ) : weight i ≠ 0 := by
  unfold weight
  positivity

theorem tagged_mass {rows : ℕ → Cantor → Cantor}
    (hrows : ∀ i, Measurable (rows i)) :
    mass (fairCantor.map (tagged rows)) =
      ∑' i, (weight i : ℝ≥0∞) * mass (fairCantor.map (rows i)) := by
  rw [tagged_mixture_law hrows]
  change mass (mixture weight (fun i => (fairCantor.map (rows i)).map (tag i))) = _
  rw [mass_mixture]
  apply tsum_congr
  intro i
  rw [tag_mass]

theorem weighted_full_mass_iff (a : ℕ → ℝ≥0) (m : ℕ → ℝ≥0∞)
    (ha : (∑' i, (a i : ℝ≥0∞)) = 1) (hapos : ∀ i, a i ≠ 0)
    (hm : ∀ i, m i ≤ 1) :
    (∑' i, (a i : ℝ≥0∞) * m i) = 1 ↔ ∀ i, m i = 1 := by
  have hle : ∀ i, (a i : ℝ≥0∞) * m i ≤ a i := by
    intro i
    simpa using mul_le_mul_left' (hm i) (a i : ℝ≥0∞)
  constructor
  · intro hsum i
    by_contra hne
    have hi : m i < 1 := lt_of_le_of_ne (hm i) hne
    have hmul : (a i : ℝ≥0∞) * m i < a i := by
      simpa using ENNReal.mul_lt_mul_left' (by exact_mod_cast hapos i)
        (ENNReal.coe_ne_top) hi
    have hfinite : (∑' j, (a j : ℝ≥0∞) * m j) ≠ ∞ := by rw [hsum]; exact ENNReal.one_ne_top
    have hlt := ENNReal.tsum_lt_tsum hfinite hle hmul
    rw [hsum, ha] at hlt
    exact (lt_irrefl 1) hlt
  · intro h
    simpa only [h, mul_one] using ha

theorem defect_zero_iff_mass_one (μ : Measure Cantor) : defect μ = 0 ↔ mass μ = 1 := by
  constructor
  · intro h
    have ht : (mass μ).toReal = 1 := by unfold defect at h; linarith
    exact (ENNReal.toReal_eq_one_iff _).mp ht
  · intro h
    simp [defect, h]

/-- The universal row condition is expressed by the actual fair-source output
law, not an abstract mixture substituted for a missing observer semantics. -/
theorem tagged_zero_defect_iff {rows : ℕ → Cantor → Cantor}
    (hrows : ∀ i, Measurable (rows i)) :
    defect (fairCantor.map (tagged rows)) = 0 ↔
      ∀ i, defect (fairCantor.map (rows i)) = 0 := by
  have hprob : ∀ i, (fairCantor.map (rows i)) univ = 1 := by
    intro i
    rw [Measure.map_apply (hrows i) MeasurableSet.univ]
    simp
  rw [defect_zero_iff_mass_one, tagged_mass hrows,
      weighted_full_mass_iff weight (fun i => mass (fairCantor.map (rows i)))
        weights_sum weight_ne_zero (fun i => (positive_le_total _).trans_eq (hprob i))]
  exact forall_congr' fun i => (defect_zero_iff_mass_one _).symm

end OrthemologyTagged
#print axioms OrthemologyTagged.tagged_mass
#print axioms OrthemologyTagged.tagged_zero_defect_iff
