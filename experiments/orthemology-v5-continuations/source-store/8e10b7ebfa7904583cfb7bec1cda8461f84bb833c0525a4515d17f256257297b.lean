import ResetExpectation
import FiniteBudgetAlmostSure

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {S : Type*} [MeasurableSpace S] [Countable S] [MeasurableSingletonClass S]

/-- Uniform actual finite-prefix charge bounds entail an expected total charge
bound. This is monotone convergence expressed as a nonnegative series. -/
theorem trajectory_total_charge_bound (μ : Measure (ℕ → S)) (c : S → ℝ≥0∞) (C : ℝ)
    (hFinite : ∀ n, (∫⁻ x, pathCharge c 0 n x ∂μ) ≤ ENNReal.ofReal C) :
    (∫⁻ x, ∑' n, c (x n) ∂μ) ≤ ENNReal.ofReal C := by
  rw [lintegral_tsum (fun n : ℕ => (show Measurable (fun x : ℕ → S => c (x n)) from by fun_prop).aemeasurable)]
  apply ENNReal.tsum_le_of_sum_range_le
  intro n
  have heq : (∑ i ∈ Finset.range n, ∫⁻ x, c (x i) ∂μ) = ∫⁻ x, pathCharge c 0 n x ∂μ := by
    rw [← lintegral_finset_sum (Finset.range n) (fun i _ => by fun_prop)]
    simp only [pathCharge, Nat.zero_add]
  rw [heq]
  exact hFinite n

/-- Each positive integer charge dominates its occurrence indicator; bounded
actual prefix expectation therefore gives eventual zero charge almost surely. -/
theorem trajectory_nat_charge_eventually_zero (μ : Measure (ℕ → S)) (c : S → ℕ) (C : ℝ)
    (hFinite : ∀ n, (∫⁻ x, pathCharge (fun s => (c s : ℝ≥0∞)) 0 n x ∂μ) ≤ ENNReal.ofReal C) :
    (∑' n, μ {x | 0 < c (x n)}) ≤ ENNReal.ofReal C ∧
      ∀ᵐ x ∂μ, ∀ᶠ n in atTop, c (x n) = 0 := by
  have hm : ∀ n, MeasurableSet {x : ℕ → S | 0 < c (x n)} := by
    intro n
    exact (measurableSet_lt measurable_const (by fun_prop))
  have hi : ∀ n, μ {x | 0 < c (x n)} ≤ ∫⁻ x, (c (x n) : ℝ≥0∞) ∂μ := by
    intro n
    rw [← lintegral_indicator_one (hm n)]
    apply lintegral_mono
    intro x
    by_cases hx : 0 < c (x n)
    · rw [Set.indicator_of_mem (show x ∈ {x : ℕ → S | 0 < c (x n)} from hx)]
      change (1 : ℝ≥0∞) ≤ (c (x n) : ℝ≥0∞)
      exact_mod_cast (Nat.succ_le_of_lt hx)
    · rw [Set.indicator_of_not_mem (show x ∉ {x : ℕ → S | 0 < c (x n)} from hx)]
      exact bot_le
  have hb : ∀ n, (∑ i ∈ Finset.range n, μ {x | 0 < c (x i)}) ≤ ENNReal.ofReal C := by
    intro n
    calc
      _ ≤ ∑ i ∈ Finset.range n, ∫⁻ x, (c (x i) : ℝ≥0∞) ∂μ :=
        Finset.sum_le_sum (fun i _ => hi i)
      _ = ∫⁻ x, pathCharge (fun s => (c s : ℝ≥0∞)) 0 n x ∂μ := by
        rw [← lintegral_finset_sum (Finset.range n) (fun i _ => by fun_prop)]
        simp only [pathCharge, Nat.zero_add]
      _ ≤ _ := hFinite n
  obtain ⟨hs, ha⟩ := finite_budget_eventually_avoids μ (fun n => {x | 0 < c (x n)}) C hb
  refine ⟨hs, ?_⟩
  filter_upwards [ha] with x hx
  filter_upwards [hx] with n hn
  simpa only [Set.mem_setOf_eq, not_lt, Nat.le_zero] using hn

end Orthemology.Tranche2
