import LookaheadBoundary
import RuntimeAudit

namespace IndependentLookaheadChecks
open EffectiveRenewal EffectiveRenewal.Lookahead

example (h : Word → Nat) : prefixScan h [] 0 = lookCheck h [] := rfl
example : boundedSelect (fun _ => true) [] = none := rfl
example (h : Word → Nat) : lookaheadPlan h 0 = [] :=
  List.length_eq_zero_iff.mp (lookaheadPlan_spec h 0).1
example (h : Word → Nat) (n : Nat) (hn : 0 < n) : lookaheadPlan h n ≠ [] := by
  intro he
  have hl := (lookaheadPlan_spec h n).1
  simp [he] at hl
  omega

-- For h=1, every PROPER prefix of a base-admitted word has a base child.
-- Consequently an L_1 rejection of such a word really occurs at the final check.
theorem proper_prefix_has_base_step (s : Word) (hs : diagonalTree s)
    (k : Nat) (hk : k < s.length) : lookCheck (fun _ => 1) (takeWord s k) = true := by
  apply (lookCheck_spec _ _).mpr
  refine ⟨takeWord s (k + 1), ?_, ?_, ?_⟩
  · simp only [takeWord_eq_take]
    exact List.take_prefix_take_left (Nat.le_succ k)
  · simp [takeWord_eq_take, List.length_take, Nat.min_eq_left (Nat.le_of_lt hk),
      Nat.min_eq_left (Nat.succ_le_of_lt hk)]
  · rw [takeWord_eq_take]
    exact diagonalTree_prefix_closed (List.take_prefix _ _) hs

theorem final_check_alone_can_fail :
    ∃ s, diagonalTree s ∧ (∀ k < s.length, lookCheck (fun _ => 1) (takeWord s k) = true) ∧
      lookCheck (fun _ => 1) s = false := by
  obtain ⟨s, hs, hn⟩ := final_prefix_check_is_substantive
  refine ⟨s, hs, fun k hk => proper_prefix_has_base_step s hs k hk, ?_⟩
  cases hlast : lookCheck (fun _ => 1) s with
  | false => rfl
  | true =>
    exfalso
    apply hn
    apply (lookaheadTree_iff _ s).mpr
    refine ⟨hs, ?_⟩
    intro k hk
    rcases lt_or_eq_of_le hk with hk | rfl
    · exact proper_prefix_has_base_step s hs k hk
    · simpa [takeWord_eq_take] using hlast

-- A concrete root-sensitive, branch-sensitive callback is a native instance.
def branchDemand (s : Word) : Nat := if s.isEmpty then 3 else if s.headD false then 2 else 0
def branchPlan : Nat → Word := lookaheadPlan branchDemand
#audit_renewal_runtime IndependentLookaheadChecks.branchPlan
#eval (List.range 4).map (fun n => let s := branchPlan n; (s.length, lookaheadCheck branchDemand s))
#eval supplement branchDemand []
#eval boundedSelect (fun _ => true) [[true], [false]]
#eval binaryWords 2
end IndependentLookaheadChecks
