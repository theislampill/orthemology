import ActualTargetPolicy

namespace HiddenParity.Sufficiency.Controls
open HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding

/-- Departure counts include the original state, exclude the most recent receipt,
and count visits by source state rather than by physical clock. -/
theorem observed_departure_count_control :
    historyVisits (0 : Fin 2) 0 ([(0,0),(0,1),(0,1)] : History (Fin 1) (Fin 2)) = 1 ∧
    historyVisits (0 : Fin 2) 1 ([(0,0),(0,1),(0,1)] : History (Fin 1) (Fin 2)) = 2 ∧
    observedState (0 : Fin 2) ([(0,0),(0,1),(0,1)] : History (Fin 1) (Fin 2)) = 0 := by decide

theorem initial_departure_count_control :
    historyVisits (0 : Fin 2) 0 ([] : History (Fin 1) (Fin 2)) = 0 ∧
    historyVisits (0 : Fin 2) 0 ([(0,1)] : History (Fin 1) (Fin 2)) = 1 := by decide

abbrev S := Fin 1
abbrev A := Fin 2
abbrev M := Fin 1

def oneStateKernel : RationalKernel M (S × A) S where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp

def menu (_ : Finset M) (_ : S) : Finset A := Finset.univ

def priority (_ : M) (e : S × A) : ℕ := if e.2 = 0 then 2 else 3

theorem all_pairs_qualifying :
    MarkovQualifying oneStateKernel Prod.fst Finset.univ priority 0 Finset.univ Finset.univ := by
  refine ⟨by decide, by decide, by decide, ?_⟩
  intro σ _ _
  fin_cases σ
  exact ⟨2, by decide, by decide⟩

/-- This is a constructed real history/seed policy, not an auxiliary chain. Its
second action has odd priority 3 and recurs forever, yet minimum parity is even. -/
noncomputable def actualWinningPolicy :
    WinningPolicy (R := Unit) oneStateKernel menu priority (0,0) Finset.univ 0 :=
  matchingTargetWinningPolicy oneStateKernel menu Finset.univ (by decide) priority 0
    Finset.univ Finset.univ all_pairs_qualifying (by intro σ _; fin_cases σ; intro e _; rfl)
    (by intros; simp [menu]) 0 0 (by decide) (0,0)

theorem actual_policy_is_semantic_winning :
    SemanticWinning (R := Unit) oneStateKernel menu priority (0,0) Finset.univ 0 :=
  ⟨actualWinningPolicy⟩

end HiddenParity.Sufficiency.Controls
