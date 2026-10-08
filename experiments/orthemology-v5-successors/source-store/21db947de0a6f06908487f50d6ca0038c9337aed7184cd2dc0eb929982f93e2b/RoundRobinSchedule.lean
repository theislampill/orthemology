import AdaptiveMarkovRecurrentGraph

noncomputable section
open Filter

namespace HiddenParity.Sufficiency
variable {S A : Type*} [DecidableEq S] [DecidableEq A]

/-- Number of departures from a specified state before time n. -/
def visitsBefore (x : ℕ → S) (s : S) : ℕ → ℕ
  | 0 => 0
  | n+1 => visitsBefore x s n + if x n = s then 1 else 0

theorem visitsBefore_mono (x : ℕ → S) (s : S) : Monotone (visitsBefore x s) := by
  apply monotone_nat_of_le_succ
  intro n
  exact Nat.le_add_right _ _

theorem visitsBefore_le_time (x : ℕ → S) (s : S) (n : ℕ) : visitsBefore x s n ≤ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [visitsBefore]; split_ifs <;> omega

theorem recurrent_state_unbounded_visits (x : ℕ → S) (s : S)
    (hRec : ∃ᶠ n in atTop, x n = s) : ∀ k, ∃ n, k ≤ visitsBefore x s n := by
  intro k
  induction k with
  | zero => exact ⟨0, le_refl _⟩
  | succ k ih =>
      obtain ⟨n, hn⟩ := ih
      obtain ⟨m, hmn, hm⟩ := frequently_atTop.mp hRec n
      have hc := visitsBefore_mono x s hmn
      refine ⟨m+1, ?_⟩
      simp only [visitsBefore, if_pos hm]
      omega

/-- Every visit index is attained at an actual departure from a recurrent state. -/
theorem recurrent_state_consumes_visit (x : ℕ → S) (s : S)
    (hRec : ∃ᶠ n in atTop, x n = s) (k : ℕ) :
    ∃ n, x n = s ∧ visitsBefore x s n = k := by
  obtain ⟨n, hn⟩ := recurrent_state_unbounded_visits x s hRec (k+1)
  have hex : ∃ n, k < visitsBefore x s n := ⟨n, by omega⟩
  have hfirst := Nat.find_spec hex
  have hne : Nat.find hex ≠ 0 := by
    intro hz; rw [hz] at hfirst; change k < 0 at hfirst; omega
  obtain ⟨m, hm⟩ := Nat.exists_eq_succ_of_ne_zero hne
  have hbefore := Nat.find_min hex (show m < Nat.find hex by omega)
  rw [hm, visitsBefore] at hfirst
  by_cases ha : x m = s
  · rw [if_pos ha] at hfirst; exact ⟨m, ha, by omega⟩
  · rw [if_neg ha] at hfirst; omega

/-- Cycle through an explicitly finite nonempty menu; the fallback is unreachable
at retained states but makes the observed-history policy total. -/
def cycleAction (F : Finset A) (fallback : A) (n : ℕ) : A :=
  if h : F.Nonempty then
    ((Fintype.equivFin F).symm ⟨n % Fintype.card F,
      Nat.mod_lt _ (by simpa using Finset.card_pos.mpr h)⟩).val
  else fallback

theorem cycleAction_mem (F : Finset A) (fallback : A) (h : F.Nonempty) (n : ℕ) :
    cycleAction F fallback n ∈ F := by
  simp only [cycleAction, dif_pos h]
  exact Subtype.property _

theorem cycleAction_at_index (F : Finset A) (fallback : A) (a : F) (k : ℕ) :
    cycleAction F fallback (k * Fintype.card F + (Fintype.equivFin F a).val) = a.val := by
  have hn : F.Nonempty := ⟨a.val, a.property⟩
  simp only [cycleAction, dif_pos hn]
  have hi : (k * Fintype.card F + (Fintype.equivFin F a).val) % Fintype.card F =
      (Fintype.equivFin F a).val := by
    rw [Nat.mul_add_mod_self_right]
    exact Nat.mod_eq_of_lt (Fintype.equivFin F a).isLt
  have hfin : (⟨(k * Fintype.card F + (Fintype.equivFin F a).val) % Fintype.card F,
      Nat.mod_lt _ (by simpa using Finset.card_pos.mpr hn)⟩ : Fin (Fintype.card F)) =
      Fintype.equivFin F a := Fin.ext hi
  rw [hfin, Equiv.symm_apply_apply]

/-- Pathwise fair cycling is proved from the actual visit counter, without any
probabilistic or fairness hypothesis beyond recurrence of the source state. -/
theorem cycle_every_action_recurrent (x : ℕ → S) (s : S) (F : Finset A) (fallback : A)
    (hRec : ∃ᶠ n in atTop, x n = s) (a : F) :
    ∃ᶠ n in atTop, x n = s ∧ cycleAction F fallback (visitsBefore x s n) = a.val := by
  apply frequently_atTop.mpr
  intro N
  let j := (N+1) * Fintype.card F + (Fintype.equivFin F a).val
  obtain ⟨n, hn, hc⟩ := recurrent_state_consumes_visit x s hRec j
  have hpos : 0 < Fintype.card F := by simpa using Finset.card_pos.mpr (show F.Nonempty from ⟨a.val,a.property⟩)
  have hj : N ≤ j := by dsimp [j]; nlinarith
  have hjn : j ≤ n := hc ▸ visitsBefore_le_time x s n
  refine ⟨n, hj.trans hjn, hn, ?_⟩
  rw [hc]
  exact cycleAction_at_index F fallback a (N+1)

end HiddenParity.Sufficiency
