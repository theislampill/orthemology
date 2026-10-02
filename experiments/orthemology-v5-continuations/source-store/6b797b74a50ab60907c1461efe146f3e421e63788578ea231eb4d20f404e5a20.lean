import FinitePrefixBoundary
import PatternAdditivity

open Set MeasureTheory
open scoped NNReal ENNReal
namespace OrthemologyMeasure
open P02A2 P02A2.Q8Measure

variable {X : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]

theorem positive_add (μ ν : Measure X) : positive (μ+ν) = positive μ ∪ positive ν := by
  ext x
  change (0 < (μ+ν) {x}) ↔ (0 < μ {x} ∨ 0 < ν {x})
  rw [Measure.add_apply]
  exact add_pos_iff

theorem mass_add (μ ν : Measure X) [IsFiniteMeasure μ] [IsFiniteMeasure ν] :
    mass (μ+ν) = mass μ + mass ν := by
  let C := positive μ ∪ positive ν
  have hc : C.Countable := (positive_countable μ).union (positive_countable ν)
  rw [mass_eq_countable_superset (μ+ν) hc (by rw [positive_add])]
  rw [Measure.add_apply]
  rw [← mass_eq_countable_superset μ hc subset_union_left,
      ← mass_eq_countable_superset ν hc subset_union_right]

theorem mass_smul (μ : Measure X) (r : ℝ≥0) : mass (r • μ) = (r : ℝ≥0∞) * mass μ := by
  by_cases hr : r = 0
  · simp [hr, mass]
  · have hp : positive (r • μ) = positive μ := by
      simpa [observedSupport, Measure.map_id] using observedSupport_smul μ r hr id
    unfold mass
    rw [hp, Measure.coe_nnreal_smul_apply]

theorem fairCantor_mass_zero : mass fairCantor = 0 := by
  have hp : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [fairCantor_singleton_zero]
    simp
  simp [mass, hp]

theorem truncatedLaw_mass_one (N : ℕ) : mass (truncatedLaw N) = 1 :=
  countable_carrier_mass_one (truncatedLaw N) (Set.finite_range (extendBits N)).countable
    (by rw [measure_compl (Set.finite_range (extendBits N)).measurableSet (measure_ne_top _ _),
            measure_univ, truncatedLaw_finite_carrier]; simp) (measure_univ)

noncomputable def prefixMixture (N : ℕ) (r : ℝ≥0) : Measure Cantor :=
  r • fairCantor + (1-r) • truncatedLaw N

instance prefixMixture_finite (N : ℕ) (r : ℝ≥0) : IsFiniteMeasure (prefixMixture N r) := by
  unfold prefixMixture
  infer_instance

theorem prefixMixture_probability (N : ℕ) (r : ℝ≥0) (hr : r ≤ 1) :
    IsProbabilityMeasure (prefixMixture N r) := by
  constructor
  simp only [prefixMixture, Measure.add_apply, Measure.coe_nnreal_smul_apply,
    measure_univ, mul_one, ← ENNReal.coe_add]
  norm_cast
  exact add_tsub_cancel_of_le hr

theorem prefixMixture_defect (N : ℕ) (r : ℝ≥0) (hr : r ≤ 1) :
    defect (prefixMixture N r) = r := by
  rw [defect, prefixMixture, mass_add, mass_smul, mass_smul,
      fairCantor_mass_zero, truncatedLaw_mass_one]
  simp only [mul_zero, mul_one, zero_add, ENNReal.coe_toReal]
  rw [NNReal.coe_sub hr]
  simp

/-- The full closed unit interval of defects is compatible with exactly the
same finite-prefix data through any prescribed horizon. -/
theorem prefixMixture_prefix_law (N k : ℕ) (hk : k ≤ N)
    (r : ℝ≥0) (hr : r ≤ 1) :
    (prefixMixture N r).map (prefixBits k) = fairCantor.map (prefixBits k) := by
  rw [prefixMixture, Measure.map_add _ _ (prefixBits_measurable k),
      Measure.map_smul, Measure.map_smul, finite_prefix_laws_equal N k hk,
      ← add_smul, add_tsub_cancel_of_le hr, one_smul]

end OrthemologyMeasure
#print axioms OrthemologyMeasure.prefixMixture_defect
#print axioms OrthemologyMeasure.prefixMixture_prefix_law
