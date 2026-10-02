import StackActionLaw
import RecurrentSupport

namespace HiddenParity.Adaptive
open Filter
open Orthemology.Tranche2.PolicyEmbedding

universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [DecidableEq A] [Inhabited Y]

/-- Number of samples already consumed from a pair's tape. -/
def countBefore (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) (n : ℕ) : ℕ :=
  actionCount a (stackHistoryTrajectory π z n)

@[simp] theorem countBefore_zero (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) :
    countBefore π z a 0 = 0 := rfl

theorem countBefore_succ (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) (n : ℕ) :
    countBefore π z a (n+1) = countBefore π z a n +
      if stackActionTrajectory π z n = a then 1 else 0 := by
  simp [countBefore, stackHistoryTrajectory, observedHistory, actionCount_cons, stackActionTrajectory]

theorem countBefore_mono (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) :
    Monotone (countBefore π z a) := by
  apply monotone_nat_of_le_succ
  intro n
  rw [countBefore_succ]
  exact Nat.le_add_right _ _

theorem countBefore_le_time (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) (n : ℕ) :
    countBefore π z a n ≤ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [countBefore_succ]
      split_ifs <;> omega

/-- Infinitely many selected occurrences imply an unbounded actual sample count. -/
theorem recurrent_action_unbounded_count
    (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A)
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a) :
    ∀ k : ℕ, ∃ n, k ≤ countBefore π z a n := by
  intro k
  induction k with
  | zero => exact ⟨0, le_refl _⟩
  | succ k ih =>
      obtain ⟨n, hn⟩ := ih
      obtain ⟨m, hmn, hm⟩ := frequently_atTop.mp hRec n
      refine ⟨m+1, ?_⟩
      have hc := countBefore_mono π z a hmn
      rw [countBefore_succ, if_pos hm]
      omega

/-- Every deterministic tape index is eventually consumed, exactly once at a
selected occurrence. No chosen-count iid claim is used. -/
theorem recurrent_action_consumes_every_index
    (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A)
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a) (k : ℕ) :
    ∃ n, stackActionTrajectory π z n = a ∧ countBefore π z a n = k := by
  obtain ⟨n, hn⟩ := recurrent_action_unbounded_count π z a hRec (k+1)
  have hex : ∃ n, k < countBefore π z a n := ⟨n, by omega⟩
  have hfirst := Nat.find_spec hex
  have hne : Nat.find hex ≠ 0 := by
    intro hz
    rw [hz, countBefore_zero] at hfirst
    omega
  obtain ⟨m, hm⟩ := Nat.exists_eq_succ_of_ne_zero hne
  have hbefore : ¬ k < countBefore π z a m := Nat.find_min hex (by omega)
  rw [hm, countBefore_succ] at hfirst
  by_cases ha : stackActionTrajectory π z m = a
  · rw [if_pos ha] at hfirst
    exact ⟨m, ha, by omega⟩
  · rw [if_neg ha] at hfirst
    omega

/-- The actual receipt read from the selected pair's next unused tape cell. -/
def stackReceipt (π : R → History A Y → A) (z : R × FlatStack A Y) (n : ℕ) : Y :=
  z.2 (stackActionTrajectory π z n, countBefore π z (stackActionTrajectory π z n) n)

/-- A recurrent tape symbol is observed infinitely often if its pair is selected
infinitely often, even with arbitrary adaptive gaps between selections. -/
theorem recurrent_action_observes_recurrent_symbol
    (π : R → History A Y → A) (z : R × FlatStack A Y) (a : A) (y : Y)
    (hRec : ∃ᶠ n in atTop, stackActionTrajectory π z n = a)
    (hTape : ∃ᶠ k in atTop, z.2 (a,k) = y) :
    ∃ᶠ n in atTop, stackActionTrajectory π z n = a ∧ stackReceipt π z n = y := by
  apply frequently_atTop.mpr
  intro N
  obtain ⟨k, hk, hy⟩ := frequently_atTop.mp hTape N
  obtain ⟨n, hn, hc⟩ := recurrent_action_consumes_every_index π z a hRec k
  have hkn : k ≤ n := by rw [← hc]; exact countBefore_le_time π z a n
  refine ⟨n, hk.trans hkn, hn, ?_⟩
  simp only [stackReceipt, hn, hc, hy]

/-- Observable next-history receipt; the default is unreachable on actual runs. -/
def historyReceipt (d : A) (H : ℕ → History A Y) (n : ℕ) : Y :=
  ((H (n+1)).headD (d,default)).2

theorem stackReceipt_eq_historyReceipt
    (π : R → History A Y → A) (z : R × FlatStack A Y) (d : A) (n : ℕ) :
    stackReceipt π z n = historyReceipt d (stackHistoryTrajectory π z) n := by
  simp [stackReceipt, historyReceipt, stackHistoryTrajectory, observedHistory, feedback,
    stackActionTrajectory, countBefore]

end HiddenParity.Adaptive
