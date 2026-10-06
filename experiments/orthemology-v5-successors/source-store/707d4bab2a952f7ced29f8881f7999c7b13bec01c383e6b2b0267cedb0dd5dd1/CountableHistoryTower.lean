import ActualGeneratedSliceTail
import Mathlib.MeasureTheory.Integral.Lebesgue.Add

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators Function
namespace HiddenParity.Cost

variable {Ω ι : Type*} [MeasurableSpace Ω] [Countable ι]

/-- Countable full-history atoms give a direct nonnegative tower inequality.
No independence and no a-priori integrability of the accumulated product is
assumed. This also allows an infinite-start atom refined by the prior cost. -/
theorem countable_history_weighted_bound (μ : Measure Ω)
    (key : Ω → ι) (hkey : ∀ i, MeasurableSet {ω | key ω=i})
    (factor : Ω → ℝ≥0∞) (hf : Measurable factor)
    (past : ι → ℝ≥0∞) (K : ℝ≥0∞)
    (hbound : ∀ i, (∫⁻ ω in {ω | key ω=i},factor ω ∂μ)≤K*μ {ω | key ω=i}) :
    (∫⁻ ω,past (key ω)*factor ω ∂μ)≤K*(∫⁻ ω,past (key ω) ∂μ) := by
  classical
  have hu : (⋃ i, {ω | key ω=i})=Set.univ := by ext ω;simp
  have hd : Pairwise (Disjoint on (fun i => {ω | key ω=i})) := by
    intro i j hij
    apply Set.disjoint_left.mpr
    intro ω hi hj
    exact hij (hi.symm.trans hj)
  have split (f : Ω → ℝ≥0∞) : (∫⁻ ω,f ω ∂μ)=∑' i,∫⁻ ω in {ω | key ω=i},f ω ∂μ := by
    rw [← setLIntegral_univ,← hu]
    exact lintegral_iUnion hkey hd f
  rw [split (fun ω => past (key ω)*factor ω),split (fun ω => past (key ω)),← ENNReal.tsum_mul_left]
  apply ENNReal.tsum_le_tsum
  intro i
  have h1 : (∫⁻ ω in {ω | key ω=i},past (key ω)*factor ω ∂μ)=
      past i*(∫⁻ ω in {ω | key ω=i},factor ω ∂μ) := by
    rw [← lintegral_const_mul _ hf]
    apply setLIntegral_congr_fun (hkey i)
    filter_upwards [] with ω hω
    rw [hω]
  have h2 : (∫⁻ ω in {ω | key ω=i},past (key ω) ∂μ)=past i*μ {ω | key ω=i} := by
    rw [← setLIntegral_const]
    apply setLIntegral_congr_fun (hkey i)
    filter_upwards [] with ω hω
    rw [hω]
  rw [h1,h2]
  simpa only [mul_assoc,mul_left_comm K (past i)] using mul_le_mul_left' (hbound i) (past i)

/-- Product of arbitrary dependent factors with uniformly bounded conditional
full-history expectations. The `past` equation is the precise requirement that
all earlier interval lengths are already known at the next start. -/
theorem countable_history_product_bound (μ : Measure Ω) [IsProbabilityMeasure μ]
    (factor : ℕ → Ω → ℝ≥0∞) (hf : ∀ i, Measurable (factor i))
    (key : ℕ → Ω → ι) (hkey : ∀ n i, MeasurableSet {ω | key n ω=i})
    (past : ℕ → ι → ℝ≥0∞) (K : ℝ≥0∞)
    (hpast : ∀ n ω, (∏ j∈Finset.range n,factor j ω)=past n (key n ω))
    (hbound : ∀ n i, (∫⁻ ω in {ω | key n ω=i},factor n ω ∂μ)≤K*μ {ω | key n ω=i})
    (J : ℕ) :
    (∫⁻ ω,∏ j∈Finset.range J,factor j ω ∂μ)≤K^J := by
  induction J with
  | zero => simp
  | succ J ih =>
      simp only [Finset.prod_range_succ]
      have hb := countable_history_weighted_bound μ (key J) (hkey J) (factor J) (hf J) (past J) K (hbound J)
      simp only [← hpast] at hb
      exact hb.trans (by simpa only [pow_succ,mul_comm] using mul_le_mul_left' ih K)

end HiddenParity.Cost
