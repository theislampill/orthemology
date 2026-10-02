import FiniteLikelihood
import Mathlib.Order.Filter.IsBounded

/-!
# Arbitrary prefix-sampling clocks and finite action likelihood scores

From the actual iid observation stacks we derive a common almost-sure event on
which every family of unbounded prefix clocks has the claimed drift. No assumed
convergence endpoint, stopping-time condition, or future-choice oracle is used.
-/

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped Topology

namespace Orthemology.Tranche2

variable {A Y Ω : Type*} [Fintype A] [Fintype Y]

lemma finite_sum_tendsto_atTop_of_one (f : A → ℕ → ℝ)
    (hbdd : ∀ a, BddBelow (Set.range (f a))) (a₀ : A)
    (h₀ : Tendsto (f a₀) atTop atTop) :
    Tendsto (fun n => ∑ a, f a n) atTop atTop := by
  classical
  choose b hb using hbdd
  let c : ℝ := ∑ a ∈ Finset.univ.erase a₀, b a
  have hsum : ∀ n, f a₀ n + c ≤ ∑ a, f a n := by
    intro n
    have hle : c ≤ ∑ a ∈ Finset.univ.erase a₀, f a n := by
      exact Finset.sum_le_sum (fun a _ => hb a (Set.mem_range_self n))
    have hsplit : f a₀ n + ∑ a ∈ Finset.univ.erase a₀, f a n = ∑ a, f a n :=
      Finset.add_sum_erase Finset.univ (fun a => f a n) (Finset.mem_univ a₀)
    rw [← hsplit]
    exact add_le_add_left hle _
  have ht : Tendsto (fun n => f a₀ n + c) atTop atTop := h₀.atTop_add tendsto_const_nhds
  exact tendsto_atTop_mono hsum ht

section Probability

variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]

/-- A common probability-one event validates all prefix clocks at once. -/
theorem sampled_logScore_tendsto_atTop (p q : A → Y → ℝ)
    (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (hq : ∀ a y, 0 < q a y)
    (hpsum : ∀ a, ∑ y, p a y = 1) (hqsum : ∀ a, ∑ y, q a y = 1)
    (hX : ∀ a n, Measurable (X a n))
    (hindep : ∀ a, Pairwise (fun i j => IndepFun (X a i) (X a j) μ))
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = p a y) :
    ∀ᵐ ω ∂μ, ∀ N : A → ℕ → ℕ,
      (∃ a, p a ≠ q a ∧ Tendsto (N a) atTop atTop) →
      Tendsto (fun t => ∑ a, ∑ i ∈ Finset.range (N a t),
        logScore (p a) (q a) (X a i ω)) atTop atTop := by
  classical
  have haction : ∀ a, ∀ᵐ ω ∂μ,
      p a ≠ q a → Tendsto
        (fun n : ℕ => ∑ i ∈ Finset.range n, logScore (p a) (q a) (X a i ω))
        atTop atTop := by
    intro a
    by_cases heq : p a = q a
    · exact Filter.Eventually.of_forall (fun _ hne => False.elim (hne heq))
    · filter_upwards [logScore_sum_tendsto_atTop (p a) (q a) (X a)
        (hp a) (hq a) (hpsum a) (hqsum a) heq (hX a) (hindep a)
        (hident a) (hLaw a)] with ω hω
      exact fun _ => hω
  have hall : ∀ᵐ ω ∂μ, ∀ a, p a ≠ q a → Tendsto
      (fun n : ℕ => ∑ i ∈ Finset.range n, logScore (p a) (q a) (X a i ω))
      atTop atTop := ae_all_iff.mpr haction
  filter_upwards [hall] with ω hω
  intro N hinfo
  obtain ⟨a₀, hneq, hcount⟩ := hinfo
  apply finite_sum_tendsto_atTop_of_one
    (fun a t => ∑ i ∈ Finset.range (N a t), logScore (p a) (q a) (X a i ω))
    ?_ a₀ ((hω a₀ hneq).comp hcount)
  intro a
  by_cases heq : p a = q a
  · refine ⟨0, ?_⟩
    rintro z ⟨t, rfl⟩
    simp [← heq, logScore_self (p a) (hp a)]
  · obtain ⟨b, hb⟩ := bddBelow_range_of_tendsto_atTop_atTop (hω a heq)
    refine ⟨b, ?_⟩
    rintro z ⟨t, rfl⟩
    exact hb (Set.mem_range_self (N a t))

/-- Jointly independent actual action/sample coordinates imply the required
within-action iid-stack independence. Cross-action independence is stronger than
needed for the pathwise drift, but matches the fresh-sampling interpretation. -/
theorem sampled_logScore_tendsto_of_joint_independent (p q : A → Y → ℝ)
    (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (hq : ∀ a y, 0 < q a y)
    (hpsum : ∀ a, ∑ y, p a y = 1) (hqsum : ∀ a, ∑ y, q a y = 1)
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : A × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = p a y) :
    ∀ᵐ ω ∂μ, ∀ N : A → ℕ → ℕ,
      (∃ a, p a ≠ q a ∧ Tendsto (N a) atTop atTop) →
      Tendsto (fun t => ∑ a, ∑ i ∈ Finset.range (N a t),
        logScore (p a) (q a) (X a i ω)) atTop atTop := by
  apply sampled_logScore_tendsto_atTop p q X hp hq hpsum hqsum hX ?_ hident hLaw
  intro a i j hij
  exact hindep.indepFun (show (a,i) ≠ (a,j) by
    intro h
    exact hij (congrArg Prod.snd h))

end Probability
end Orthemology.Tranche2
