import AuditContractBinding
import ProductObservationLaw
import BinaryConstructiveRepair
import Mathlib.Probability.StrongLaw

open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology BigOperators
open Orthemology.Tranche2

namespace Orthemology.Tranche3

/-- Every opportunity emits a coherent plug-in report; no hidden weight
is read. This policy differs from the confidence-certified abstaining policy. -/
def empiricalWeight (n : ℕ) (w : Bits (n+1)) : ℚ :=
  (rationalCount (n+1) w : ℚ)/(n+1)
def empiricalRepair (e : ℚ) (n : ℕ) (w : Bits (n+1)) : ℚ :=
  1/2+e*empiricalWeight n w

def bitValue (b : Bool) : ℝ := if b then 1 else 0

lemma count_prefix_real : ∀ n (ω : ℕ → Bool),
    (rationalCount n (observedPrefix n ω) : ℝ) = ∑ i ∈ Finset.range n, bitValue (ω i) := by
  intro n
  induction n with
  | zero => intro ω; simp [rationalCount,observedPrefix]
  | succ n ih =>
      intro ω
      simp only [rationalCount,observedPrefix,Finset.sum_range_succ]
      push_cast
      rw [ih]
      cases hb : ω n <;> simp [bitValue,hb,add_comm]

lemma empiricalWeight_mem (n : ℕ) (w : Bits (n+1)) :
    0 ≤ empiricalWeight n w ∧ empiricalWeight n w ≤ 1 := by
  have hd : (0:ℚ)<n+1 := by positivity
  constructor
  · unfold empiricalWeight; positivity
  · unfold empiricalWeight
    apply (div_le_one hd).mpr
    exact_mod_cast rationalCount_le (n+1) w

lemma empiricalRepair_coherent (e : ℚ) (he0 : 0 ≤ e) (he1 : e ≤ 1/4)
    (n : ℕ) (w : Bits (n+1)) : 0 ≤ empiricalRepair e n w ∧ empiricalRepair e n w ≤ 1 := by
  have hw := empiricalWeight_mem n w
  have h0 := mul_nonneg he0 hw.1
  have h1 := mul_le_mul_of_nonneg_left hw.2 he0
  unfold empiricalRepair
  constructor <;> linarith

lemma source_bit_expectation (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    (∫ ω, bitValue (ω 0) ∂auditSourceLaw a ha0 ha1)=a := by
  rw [← integral_map (measurable_pi_apply 0).aemeasurable
    (measurable_of_countable bitValue).aestronglyMeasurable]
  rw [auditSourceLaw,infinite_product_coordinate_law,
    integral_fintype bitValue Integrable.of_finite]
  simp [bitValue,Measure.real,sourceCoin_singleton,coinMass,ENNReal.toReal_ofReal ha0,smul_eq_mul]

/-- The empirical parameter converges under the actual constructed source law. -/
theorem empiricalWeight_converges (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    ∀ᵐ ω ∂auditSourceLaw a ha0 ha1,
      Tendsto (fun n => (empiricalWeight n (observedPrefix (n+1) ω):ℝ)) atTop (𝓝 a) := by
  have hm : Measurable bitValue := measurable_of_countable _
  have hi : Integrable (fun ω : ℕ → Bool => bitValue (ω 0)) (auditSourceLaw a ha0 ha1) := by
    have hh : Integrable bitValue ((auditSourceLaw a ha0 ha1).map (fun ω => ω 0)) := Integrable.of_finite
    exact hh.comp_measurable (measurable_pi_apply 0)
  have hind := infinite_product_coordinates_independent (fun _ : ℕ => sourceCoinMeasure a ha0 ha1)
  have hid : ∀ n, IdentDistrib (fun ω : ℕ → Bool => ω n) (fun ω : ℕ → Bool => ω 0)
      (auditSourceLaw a ha0 ha1) (auditSourceLaw a ha0 ha1) := by
    intro n
    constructor
    · exact (measurable_pi_apply n).aemeasurable
    · exact (measurable_pi_apply 0).aemeasurable
    · rw [auditSourceLaw,infinite_product_coordinate_law,infinite_product_coordinate_law]
  have hs := strong_law_ae_real (fun n (ω : ℕ → Bool) => bitValue (ω n)) hi
    (fun i j hne => (hind.indepFun hne).comp hm hm) (fun n => (hid n).comp hm)
  rw [source_bit_expectation] at hs
  filter_upwards [hs] with ω hω
  have hh := hω.comp (tendsto_add_atTop_nat 1)
  convert hh using 1
  funext n
  simp only [empiricalWeight]
  push_cast
  rw [count_prefix_real]
  simp only [Function.comp_apply, Nat.cast_add, Nat.cast_one]

/-- Interior weights have a positive repair margin. Empirical convergence
therefore yields eventual strict all-truth repair, with no abstention. -/
theorem interior_empirical_strict_restoration (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) :
    ∀ᵐ ω ∂auditSourceLaw a ha0.le ha1.le, ∀ᶠ n in atTop,
      excessZero a e (empiricalRepair e n (observedPrefix (n+1) ω)) < 0 ∧
      excessOne a e (empiricalRepair e n (observedPrefix (n+1) ω)) < 0 := by
  have he0' : (0:ℝ)<e := by exact_mod_cast he0
  have he1' : (e:ℝ)≤1/4 := by
    have hh : (e:ℝ)≤((1/4:ℚ):ℝ) := by exact_mod_cast he1
    norm_num at hh ⊢
    exact hh
  have hapos : 0 < 1-a := sub_pos.mpr ha1
  have hc : 0<a*(1-a)*(e:ℝ)/4 := by positivity
  filter_upwards [empiricalWeight_converges a ha0.le ha1.le] with ω hω
  have hz := (hω.sub_const a).abs
  simp only [sub_self,abs_zero] at hz
  have ha := hz.eventually (gt_mem_nhds hc)
  apply ha.mono
  intro n hn
  have hg := approximate_parameter_strict_repair a e
    (empiricalWeight n (observedPrefix (n+1) ω)) ha0 ha1 he0' he1' hn.le
  have hq : (empiricalRepair e n (observedPrefix (n+1) ω):ℝ)=
      1/2+(empiricalWeight n (observedPrefix (n+1) ω):ℝ)*(e:ℝ) := by
    simp only [empiricalRepair]
    push_cast
    ring
  rw [hq]
  unfold excessZero excessOne
  constructor <;> linarith [hg.1,hg.2]

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.empiricalWeight_converges
#print axioms Orthemology.Tranche3.interior_empirical_strict_restoration
