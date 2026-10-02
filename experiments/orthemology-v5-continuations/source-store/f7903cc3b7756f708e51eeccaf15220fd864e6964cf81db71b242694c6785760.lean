import Mathlib
import Mathlib.Probability.ProductMeasure

open MeasureTheory ProbabilityTheory Set
open scoped BigOperators

namespace Orthemology.Tranche2

/-- Marginals of the actual product experiment, derived from finite cylinders. -/
theorem infinite_product_coordinate_law {ι Y : Type*} [MeasurableSpace Y]
    (ν : ι → Measure Y) [∀ i, IsProbabilityMeasure (ν i)] (i : ι) :
    (Measure.infinitePi ν).map (fun ω => ω i) = ν i := by
  classical
  ext s hs
  rw [Measure.map_apply (measurable_pi_apply i) hs]
  have hset : (fun ω : ι → Y => ω i) ⁻¹' s =
      Set.pi ({i} : Finset ι) (fun _ => s) := by
    ext ω
    simp
  rw [hset, Measure.infinitePi_pi ν (fun _ _ => hs)]
  simp

/-- The actual coordinate family of the product experiment is independent;
this does not assume independence as an unconnected sensor premise. -/
theorem infinite_product_coordinates_independent {ι Y : Type*} [MeasurableSpace Y]
    (ν : ι → Measure Y) [∀ i, IsProbabilityMeasure (ν i)] :
    iIndepFun (fun i (ω : ι → Y) => ω i) (Measure.infinitePi ν) := by
  classical
  rw [iIndepFun_iff_measure_inter_preimage_eq_mul]
  intro I sets hsets
  have hset : (⋂ i ∈ I, (fun ω : ι → Y => ω i) ⁻¹' sets i) =
      Set.pi (I : Set ι) sets := by
    ext ω
    simp
  rw [hset,Measure.infinitePi_pi ν hsets]
  apply Finset.prod_congr rfl
  intro i hi
  rw [← Measure.map_apply (measurable_pi_apply i) (hsets i hi),
    infinite_product_coordinate_law ν i]

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.infinite_product_coordinate_law
#print axioms Orthemology.Tranche2.infinite_product_coordinates_independent
