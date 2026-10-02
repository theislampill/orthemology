import ResetHellinger
import Mathlib.MeasureTheory.OuterMeasure.BorelCantelli
import Mathlib.MeasureTheory.Integral.Lebesgue.Countable
import Mathlib.Data.ENNReal.BigOperators

noncomputable section
open MeasureTheory Filter
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Ω : Type*} [MeasurableSpace Ω]

/-- A uniform finite-horizon bound on sums of event probabilities entails finite
expected event count and eventual avoidance. No independence is required here. -/
theorem finite_budget_eventually_avoids (μ : Measure Ω) (bad : ℕ → Set Ω)
    (C : ℝ) (hBudget : ∀ n, (∑ i ∈ Finset.range n, μ (bad i)) ≤ ENNReal.ofReal C) :
    (∑' i, μ (bad i)) ≤ ENNReal.ofReal C ∧
      ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, ω ∉ bad n := by
  have ht := ENNReal.tsum_le_of_sum_range_le hBudget
  exact ⟨ht, ae_eventually_not_mem (ne_of_lt (ht.trans_lt ENNReal.ofReal_lt_top))⟩

/-- The expectation of the total nonnegative event count is the sum of event
probabilities. The right side is the actual measure, not an assumed convergence
value. -/
theorem expected_event_count_eq_tsum (μ : Measure Ω) (bad : ℕ → Set Ω)
    (hm : ∀ n, MeasurableSet (bad n)) :
    (∫⁻ ω, ∑' n, (bad n).indicator (fun _ => (1 : ℝ≥0∞)) ω ∂μ) = ∑' n, μ (bad n) := by
  rw [lintegral_tsum (fun n => (measurable_const.indicator (hm n)).aemeasurable)]
  apply tsum_congr
  intro n
  exact lintegral_indicator_one (hm n)

/-- Finite-prefix semantic interface: if an infinite realization has the actual
finite-tree cost as an upper bound for its prefix event probabilities, the
checked tree budget transfers to its infinite path law. This explicitly does
not construct the infinite realization or assert its cylinder-law contract. -/
theorem finite_tree_budget_transfer (μ : Measure Ω) (bad : ℕ → Set Ω)
    (treeCost : ℕ → ℝ) (C : ℝ)
    (hLaw : ∀ n, (∑ i ∈ Finset.range n, μ (bad i)) ≤ ENNReal.ofReal (treeCost n))
    (hTree : ∀ n, treeCost n ≤ C) :
    (∑' i, μ (bad i)) ≤ ENNReal.ofReal C ∧
      ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, ω ∉ bad n :=
  finite_budget_eventually_avoids μ bad C
    (fun n => (hLaw n).trans (ENNReal.ofReal_le_ofReal (hTree n)))

end Orthemology.Tranche2
