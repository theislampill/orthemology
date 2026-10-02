import ChainPhysicalBudget

namespace IndependentChainControls
open Orthemology.Tranche3
open scoped BigOperators

def rank (p : Bool) : ℕ := if p then 1 else 0
def edge (p q : Bool) : Prop := p = true ∧ q = false
def localCost (p : Bool) : ℝ := if p then 2 else 3
lemma edge_rank (p q : Bool) (h : edge p q) : rank q < rank p := by
  rcases h with ⟨rfl,rfl⟩
  norm_num [rank]

noncomputable def budget := phaseChainBudget rank edge edge_rank localCost

theorem no_self_edge (p : Bool) : ¬ edge p p := by
  intro h
  have hh:=edge_rank p p h
  exact (Nat.lt_irrefl _) hh

theorem leaf_budget : budget false = 3 := by
  rw [budget,phaseChainBudget_eq]
  simp [phaseContinuationBudget,localCost,edge]

theorem root_budget : budget true = 5 := by
  rw [budget,phaseChainBudget_eq]
  have hf : phaseChainBudget rank edge edge_rank localCost false = 3 := leaf_budget
  norm_num [phaseContinuationBudget,localCost,edge,hf]

theorem coarse_rank_budget : budget true ≤ 10 := by
  have h:=phaseChainBudget_le_rank_bound rank edge edge_rank localCost 5 (by norm_num)
    (by intro p; cases p <;> norm_num [localCost]) true
  norm_num [budget,rank] at h ⊢
  exact h

theorem strict_improvement : budget true < 10 := by rw [root_budget]; norm_num

theorem local_supersolution_least (b : Bool → ℝ)
    (hl : ∀ p, localCost p ≤ b p)
    (he : ∀ p q, edge p q → localCost p + b q ≤ b p) : budget true ≤ b true :=
  phaseChainBudget_le_supersolution rank edge edge_rank localCost b hl he true

theorem no_rank_for_self_reset : ¬ ∃ r : Unit → ℕ, ∀ p q : Unit, True → r q < r p := by
  rintro ⟨r,hr⟩
  exact (Nat.lt_irrefl _) (hr () () trivial)

theorem no_rank_for_cycle : ¬ ∃ r : Bool → ℕ,
    r false < r true ∧ r true < r false := by
  rintro ⟨r,hl,hr⟩
  omega

end IndependentChainControls
