import GlobalParitySufficiency

namespace Orthemology.RuntimeBridge.Clock
open Filter
open Orthemology.Tranche2.RecurrentSupport
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic
open scoped ENNReal BigOperators

/-- The physical-to-logical clock covers every logical step and never moves
backwards. This is exactly the clock induced by positive finite block lengths. -/
structure PositiveStutter where
  logicalAt : ℕ → ℕ
  monotone : Monotone logicalAt
  onto : Function.Surjective logicalAt

/-- Infinite occurrence is unchanged by positive finite stuttering. -/
theorem recurrent_iff (c : PositiveStutter) {A : Type*} (x : ℕ → A) (a : A) :
    (∃ᶠ t in atTop, x (c.logicalAt t) = a) ↔ (∃ᶠ n in atTop, x n = a) := by
  constructor
  · intro h
    apply frequently_atTop.mpr
    intro N
    obtain ⟨T,hT⟩ := c.onto N
    obtain ⟨t,ht,ha⟩ := frequently_atTop.mp h T
    exact ⟨c.logicalAt t, hT ▸ c.monotone ht, ha⟩
  · intro h
    apply frequently_atTop.mpr
    intro T
    obtain ⟨n,hn,ha⟩ := frequently_atTop.mp h (c.logicalAt T+1)
    obtain ⟨t,ht⟩ := c.onto n
    have hTt : T ≤ t := by
      by_contra hnle
      have hl : t ≤ T := by omega
      have hle := c.monotone hl
      omega
    exact ⟨t,hTt,ht ▸ ha⟩

theorem recurrent_set_exact {A : Type*} [Fintype A] [DecidableEq A]
    (c : PositiveStutter) (x : ℕ → A) :
    recurrentSet (fun t => x (c.logicalAt t)) = recurrentSet x := by
  ext a
  simp only [mem_recurrentSet, Recurs, recurrent_iff]

/-- The accepted minimum-recurrent-priority event is preserved. Waiting must
carry the original state/action priority, including the acceptance tick. -/
theorem parity_exact {A : Type*} [Fintype A] [DecidableEq A]
    (c : PositiveStutter) (priority : A → ℕ) (x : ℕ → A) :
    ParitySuccess priority (fun t => x (c.logicalAt t)) ↔ ParitySuccess priority x := by
  unfold ParitySuccess
  rw [recurrent_set_exact]

/-- A nonnegative lifetime charge multiplied by deterministic positive block
lengths is precisely the repeated holding charge when indexed by block/tick.
This identity does not claim an acquisition or wall-clock expectation bound. -/
theorem block_charge_exact (duration : ℕ → ℕ) (cost : ℕ → ℝ≥0∞) :
    (∑' n, ∑ _i : Fin (duration n), cost n) = ∑' n, (duration n : ℝ≥0∞) * cost n := by
  congr 1
  funext n
  simp

end Orthemology.RuntimeBridge.Clock
