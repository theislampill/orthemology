import CountableHistoryTower
import Mathlib.MeasureTheory.Integral.Lebesgue.Add
import Mathlib.Algebra.Order.Floor.Div

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
namespace HiddenParity.Cost

/-- Nonnegative geometric telescoping without subtracting infinite values. -/
theorem shifted_pow_eq_geometric_sum (c : ℝ≥0∞) (n : ℕ) :
    (1+c)^n=1+c*∑ k∈Finset.range n,(1+c)^k := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [pow_succ,Finset.sum_range_succ,ih]
      ring

/-- Exact tail-sum representation for the exponential of a natural duration. -/
theorem shifted_pow_eq_tail_sum (c : ℝ≥0∞) (n : ℕ) :
    (1+c)^n=1+∑' k:ℕ, c*(1+c)^k*(if k<n then 1 else 0) := by
  rw [shifted_pow_eq_geometric_sum]
  congr 1
  rw [tsum_eq_sum (s := Finset.range n) (by intro k hk;simp only [Finset.mem_range,not_lt] at hk;simp [not_lt.mpr hk])]
  simp only [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k hk
  simp only [if_pos (Finset.mem_range.mp hk),mul_one]

/-- A natural-valued duration with geometric tail has the corresponding
nonnegative exponential bound. No independence or integrability is assumed. -/
theorem geometric_tail_nat_pow_bound {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (L : Ω → ℕ) (hL : Measurable L)
    (c q : ℝ≥0∞)
    (htail : ∀ k:ℕ, μ {ω | k<L ω}≤q^k) :
    (∫⁻ ω,(1+c)^(L ω) ∂μ)≤1+c*(1-(1+c)*q)⁻¹ := by
  have hm (k:ℕ) : MeasurableSet {ω | k<L ω} :=
    (measurableSet_lt measurable_const measurable_id).preimage hL
  have hi (k:ℕ) : Measurable (fun ω => if k<L ω then (1:ℝ≥0∞) else 0) :=
    measurable_const.piecewise (hm k) measurable_const
  have hterm (k:ℕ) : Measurable (fun ω => c*(1+c)^k*(if k<L ω then 1 else 0)) :=
    measurable_const.mul (hi k)
  rw [show (∫⁻ ω,(1+c)^(L ω) ∂μ)=(∫⁻ ω,1+∑' k:ℕ,c*(1+c)^k*(if k<L ω then 1 else 0) ∂μ)
    from lintegral_congr (fun ω => shifted_pow_eq_tail_sum c (L ω))]
  rw [lintegral_add_left measurable_const,lintegral_const,measure_univ,one_mul,lintegral_tsum
    (fun k => (hterm k).aemeasurable)]
  calc
    1+∑' k:ℕ,∫⁻ ω,c*(1+c)^k*(if k<L ω then 1 else 0) ∂μ
      ≤1+∑' k:ℕ,c*(1+c)^k*q^k := by
        apply add_le_add_left
        apply ENNReal.tsum_le_tsum
        intro k
        rw [lintegral_const_mul _ (hi k)]
        have he : (∫⁻ ω,if k<L ω then (1:ℝ≥0∞) else 0 ∂μ)=μ {ω | k<L ω} := by
          simpa only [Set.indicator,Pi.one_apply,one_mul] using lintegral_indicator_const (μ := μ) (hm k) 1
        rw [he]
        exact mul_le_mul_left' (htail k) _
    _ =1+c*(1-(1+c)*q)⁻¹ := by
      simp_rw [mul_assoc,← mul_pow]
      rw [ENNReal.tsum_mul_left,ENNReal.tsum_geometric]

/-- The exact factor-two geometric MGF scale, expressed as a positive base
rather than logarithms: a=2/(1+q). -/
theorem geometric_tail_nat_factor_two {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (L : Ω → ℕ) (hL : Measurable L)
    (q : ℝ) (hq : 0≤q) (hq1 : q<1)
    (htail : ∀ k:ℕ, μ {ω | k<L ω}≤ENNReal.ofReal (q^k)) :
    (∫⁻ ω,ENNReal.ofReal (2/(1+q))^(L ω) ∂μ)≤2 := by
  let c := (1-q)/(1+q)
  have hden : 0<1+q := by linarith
  have hc : 0<c := div_pos (by linarith) hden
  have ha : 0≤2/(1+q) := by positivity
  have he : (1:ℝ≥0∞)+ENNReal.ofReal c=ENNReal.ofReal (2/(1+q)) := by
    rw [← ENNReal.ofReal_one,← ENNReal.ofReal_add (by norm_num) hc.le]
    congr 1
    dsimp [c]
    field_simp
    ring
  have hr : (1:ℝ≥0∞)-(1+ENNReal.ofReal c)*ENNReal.ofReal q=ENNReal.ofReal c := by
    rw [he,← ENNReal.ofReal_mul ha,← ENNReal.ofReal_one,
      ← ENNReal.ofReal_sub 1 (mul_nonneg ha hq)]
    congr 1
    dsimp [c]
    field_simp
    ring
  rw [← he]
  apply (geometric_tail_nat_pow_bound μ L hL (ENNReal.ofReal c) (ENNReal.ofReal q)
    (by intro k;simpa only [ENNReal.ofReal_pow hq] using htail k)).trans_eq
  rw [hr,ENNReal.mul_inv_cancel (ENNReal.ofReal_ne_zero_iff.mpr hc) ENNReal.ofReal_ne_top]
  norm_num

/-- A geometric block-survival tail controls the rounded-up interval length at
the same factor-two base. This is the scalar step needed before an adaptive
full-history product argument, without any claim of independent intervals. -/
theorem geometric_block_tail_factor_two {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (L : Ω → ℕ) (hL : Measurable L)
    (D : ℕ) (hD : 0<D) (q : ℝ) (hq : 0≤q) (hq1 : q<1)
    (htail : ∀ k:ℕ,μ {ω | k*D<L ω}≤ENNReal.ofReal (q^k)) :
    (∫⁻ ω,ENNReal.ofReal (2/(1+q))^(L ω ⌈/⌉ D) ∂μ)≤2 := by
  apply geometric_tail_nat_factor_two μ (fun ω => L ω ⌈/⌉ D)
    ((measurable_of_countable (fun n:ℕ => n ⌈/⌉ D)).comp hL) q hq hq1
  intro k
  have he : {ω | k<L ω ⌈/⌉ D}={ω | k*D<L ω} := by
    ext ω
    simp only [Set.mem_setOf_eq,← not_le,ceilDiv_le_iff_le_mul hD,Nat.mul_comm D k]
  rw [he]
  exact htail k

end HiddenParity.Cost
