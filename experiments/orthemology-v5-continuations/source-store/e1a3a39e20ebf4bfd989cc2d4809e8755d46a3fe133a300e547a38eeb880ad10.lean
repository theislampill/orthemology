import ProductObservationLaw
import FourBitFraming

namespace Orthemology.RationalLaw
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators
open P02A2.Q8Measure
open Orthemology.Tranche2

/-- Injective deterministic selection retains the exact original fair infinite-product law. -/
theorem fair_reindex_law (f : ℕ → ℕ) (hf : Function.Injective f) :
    fairCantor.map (fun x n => x (f n)) = fairCantor := by
  have hm : Measurable (fun (x : Cantor) n => x (f n)) :=
    measurable_pi_lambda _ (fun n => measurable_pi_apply (f n))
  have hi := (infinite_product_coordinates_independent (fun _ : ℕ => fairBit)).precomp hf
  apply Measure.eq_infinitePi
  intro s t ht
  rw [Measure.map_apply hm (MeasurableSet.pi (Finset.countable_toSet _) ht)]
  have he : (fun (x : Cantor) n => x (f n)) ⁻¹' Set.pi (s : Set ℕ) t =
      ⋂ n ∈ s, (fun x : Cantor => x (f n)) ⁻¹' t n := by ext x; simp
  rw [he]
  change (Measure.infinitePi (fun _ : ℕ => fairBit)) _ = _
  rw [hi.measure_inter_preimage_eq_mul s ht]
  apply Finset.prod_congr rfl
  intro i hi
  rw [← Measure.map_apply (measurable_pi_apply (f i)) (ht i hi)]
  exact congrArg (fun μ : Measure Bool => μ (t i))
    (infinite_product_coordinate_law (fun _ : ℕ => fairBit) (f i))

theorem fair_decimateFour_law : fairCantor.map Orthemology.RuntimeBridge.decimateFour = fairCantor :=
  fair_reindex_law (fun n => 4*n) (by intro i j h; change 4*i=4*j at h; omega)

theorem fair_decimateFour_preimage (E : Set Cantor) (hE : MeasurableSet E) :
    fairCantor (Orthemology.RuntimeBridge.decimateFour ⁻¹' E) = fairCantor E := by
  rw [← Measure.map_apply (by exact measurable_pi_lambda _ (fun n => measurable_pi_apply (4*n))) hE,
    fair_decimateFour_law]

end Orthemology.RationalLaw
