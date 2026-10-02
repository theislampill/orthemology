import PatternBoundary

open Set MeasureTheory
open scoped ENNReal
namespace OrthemologyMeasure
open P02A2 P02A2.Q8Measure

def truncateBits (N : ℕ) (x : Cantor) (n : ℕ) : Bool := if n < N then x n else false

def prefixBits (N : ℕ) (x : Cantor) : Fin N → Bool := fun i => x i.val

def extendBits (N : ℕ) (x : Fin N → Bool) (n : ℕ) : Bool :=
  if h : n < N then x ⟨n,h⟩ else false

theorem truncateBits_measurable (N : ℕ) : Measurable (truncateBits N) := by
  apply measurable_pi_lambda
  intro n
  by_cases h : n < N
  · simpa [truncateBits, h] using (measurable_pi_apply n : Measurable (fun x : Cantor => x n))
  · simpa [truncateBits, h] using (measurable_const : Measurable (fun _ : Cantor => false))

theorem prefixBits_measurable (N : ℕ) : Measurable (prefixBits N) :=
  measurable_pi_lambda _ fun i => measurable_pi_apply i.val

theorem truncate_extend (N : ℕ) (x : Cantor) :
    truncateBits N x = extendBits N (prefixBits N x) := by
  funext n
  simp [truncateBits, extendBits, prefixBits]

noncomputable def truncatedLaw (N : ℕ) : Measure Cantor := fairCantor.map (truncateBits N)

instance truncatedLaw_probability (N : ℕ) : IsProbabilityMeasure (truncatedLaw N) := by
  constructor
  rw [truncatedLaw, Measure.map_apply (truncateBits_measurable N) MeasurableSet.univ]
  simp

theorem truncatedLaw_finite_carrier (N : ℕ) :
    truncatedLaw N (Set.range (extendBits N)) = 1 := by
  rw [truncatedLaw, Measure.map_apply (truncateBits_measurable N)
    (Set.finite_range (extendBits N)).measurableSet]
  have he : truncateBits N ⁻¹' Set.range (extendBits N) = univ := by
    ext x
    simp only [mem_preimage, mem_range, mem_univ, iff_true]
    exact ⟨prefixBits N x, (truncate_extend N x).symm⟩
  rw [he, measure_univ]

theorem truncatedLaw_defect_zero (N : ℕ) : defect (truncatedLaw N) = 0 := by
  have hm := countable_carrier_mass_one (truncatedLaw N)
    (Set.finite_range (extendBits N)).countable
    (by rw [measure_compl (Set.finite_range (extendBits N)).measurableSet (measure_ne_top _ _),
            measure_univ, truncatedLaw_finite_carrier]; simp) (measure_univ)
  simp [defect, hm]

theorem fairCantor_defect_one : defect fairCantor = 1 := by
  have hp : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [fairCantor_singleton_zero]
    simp
  simp [defect, mass, hp]

/-- Every prescribed finite observation horizon is exactly matched by a fully
atomic law, although the fair source has diffuse mass one. -/
theorem finite_prefix_laws_equal (N k : ℕ) (hk : k ≤ N) :
    (truncatedLaw N).map (prefixBits k) = fairCantor.map (prefixBits k) := by
  rw [truncatedLaw, Measure.map_map (prefixBits_measurable k) (truncateBits_measurable N)]
  congr 1
  funext x i
  simp [Function.comp_def, prefixBits, truncateBits, Nat.lt_of_lt_of_le i.isLt hk]

theorem probability_eventTV_le_one {X : Type*} [MeasurableSpace X]
    (μ ν : Measure X) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] : eventTV μ ν ≤ 1 := by
  apply (eventTV_le_iff μ ν 1).mpr
  intro s hs
  have hm0 := ENNReal.toReal_nonneg (a := μ s)
  have hn0 := ENNReal.toReal_nonneg (a := ν s)
  have hm1 : (μ s).toReal ≤ 1 := by
    simpa using ENNReal.toReal_mono (measure_ne_top μ univ) (measure_mono (subset_univ s))
  have hn1 : (ν s).toReal ≤ 1 := by
    simpa using ENNReal.toReal_mono (measure_ne_top ν univ) (measure_mono (subset_univ s))
  exact abs_sub_le_iff.mpr ⟨by linarith, by linarith⟩

theorem finite_prefix_full_TV_one (N : ℕ) : eventTV fairCantor (truncatedLaw N) = 1 := by
  apply le_antisymm (probability_eventTV_le_one _ _)
  have h := defect_eventTV_bound fairCantor (truncatedLaw N)
  simpa [fairCantor_defect_one, truncatedLaw_defect_zero] using h

end OrthemologyMeasure
#print axioms OrthemologyMeasure.finite_prefix_laws_equal
#print axioms OrthemologyMeasure.truncatedLaw_defect_zero
#print axioms OrthemologyMeasure.finite_prefix_full_TV_one
