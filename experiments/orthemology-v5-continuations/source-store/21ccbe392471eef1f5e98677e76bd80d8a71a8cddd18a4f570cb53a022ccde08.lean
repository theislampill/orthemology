import MealyRefinement

/-! An all-size lower-bound family. The positive chain is indexed by remaining
zero-output countdown time, which reverses the positive-state numbering in the
ordinary source family. `none` is its state zero. -/

namespace Orthemology.Frontier.Mealy

/-- A zero-output budget is consumed at most one per input tick. -/
theorem output_zeros_of_budget {S : Type*} (M : Mealy S) (budget : S → ℕ)
    (step : ∀ s, 0 < budget s → ∀ b,
      M.out s b = false ∧ budget s - 1 ≤ budget (M.next s b))
    (s : S) (u : List Bool) (hu : u.length ≤ budget s) :
    M.outputWord s u = List.replicate u.length false := by
  induction u generalizing s with
  | nil => rfl
  | cons b bs ih =>
    have hpos : 0 < budget s := by simp only [List.length_cons] at hu; omega
    obtain ⟨hout, hbudget⟩ := step s hpos b
    have htail : bs.length ≤ budget (M.next s b) := by
      simp only [List.length_cons] at hu
      omega
    simp only [outputWord, hout, ih _ htail, List.length_cons, List.replicate_succ]

abbrev SharpState (n : ℕ) := Option (Fin (n+1))

def sharpFamily (n : ℕ) : Mealy (SharpState n) where
  out s _ := match s with
    | none => false
    | some k => decide (k.val = 0)
  next s b := match s with
    | none => if b then some ⟨n, by omega⟩ else none
    | some k => if hk : k.val = 0 then none else some ⟨k.val-1, by omega⟩

def sharpBudget (n : ℕ) : SharpState n → ℕ
  | none => n+1
  | some k => k.val

theorem sharp_budget_step (n : ℕ) (s : SharpState n) (hs : 0 < sharpBudget n s)
    (b : Bool) :
    (sharpFamily n).out s b = false ∧
      sharpBudget n s - 1 ≤ sharpBudget n ((sharpFamily n).next s b) := by
  cases s with
  | none => cases b <;> simp [sharpFamily, sharpBudget]
  | some k =>
    have hk : k.val ≠ 0 := by simpa [sharpBudget] using (Nat.ne_of_gt hs)
    have hk0 : k ≠ 0 := by
      intro h
      apply hk
      simp [h]
    simp [sharpFamily, sharpBudget, hk, hk0]

theorem sharp_none_zeros (n : ℕ) (u : List Bool) (hu : u.length ≤ n+1) :
    (sharpFamily n).outputWord none u = List.replicate u.length false :=
  output_zeros_of_budget _ _ (sharp_budget_step n) _ _ hu

/-- The positive countdown follows its fixed prefix before returning to state zero. -/
theorem sharp_countdown_output (n k : ℕ) (hk : k ≤ n)
    (u : List Bool) (hu : k+1 ≤ u.length) :
    (sharpFamily n).outputWord (some ⟨k, by omega⟩) u =
      List.replicate k false ++ true :: (sharpFamily n).outputWord none (u.drop (k+1)) := by
  induction k generalizing u with
  | zero =>
    cases u with
    | nil => simp at hu
    | cons b bs => simp [sharpFamily, outputWord]
  | succ k ih =>
    cases u with
    | nil => simp at hu
    | cons b bs =>
      have hk' : k ≤ n := by omega
      have hu' : k+1 ≤ bs.length := by
        simp only [List.length_cons] at hu
        omega
      have hrec := ih hk' bs hu'
      simpa [sharpFamily, outputWord, List.replicate_succ] using congrArg (List.cons false) hrec

theorem sharp_initial_output_fixed (n : ℕ) (u : List Bool) (hu : u.length = 2*n+2) :
    (sharpFamily n).outputWord (some ⟨n, by omega⟩) u =
      List.replicate n false ++ true :: List.replicate (n+1) false := by
  rw [sharp_countdown_output n n le_rfl u (by omega)]
  have hlen : (u.drop (n+1)).length = n+1 := by simp [hu]; omega
  rw [sharp_none_zeros n _ (by omega), hlen]

/-- The distinguished state survives every refinement through `2m-2`, where `m=n+2`. -/
theorem sharp_survives (n : ℕ) :
    ((sharpFamily n).approx (2*n+2)).rel (some ⟨n, by omega⟩) (some ⟨n, by omega⟩) := by
  apply (approx_iff_words _ _ _ _).mpr
  intro u v hu hv
  exact (sharp_initial_output_fixed n u hu).trans (sharp_initial_output_fixed n v hv).symm

/-- Waiting forever in state zero produces only zeros. -/
theorem sharp_none_false_input (n j : ℕ) :
    (sharpFamily n).outputWord none (List.replicate j false) = List.replicate j false := by
  induction j with
  | zero => rfl
  | succ j ih => simpa [List.replicate_succ, outputWord, sharpFamily] using congrArg (List.cons false) ih

/-- Entering the positive chain produces a one after exactly `n+2` ticks. -/
theorem sharp_none_enter_input (n : ℕ) :
    (sharpFamily n).outputWord none (true :: List.replicate (n+1) false) =
      false :: (List.replicate n false ++ [true]) := by
  change false :: (sharpFamily n).outputWord (some ⟨n, by omega⟩) _ = _
  rw [sharp_countdown_output n n le_rfl _ (by simp)]
  simp [outputWord]

/-- The next refinement deletes the distinguished state, so the universal upper bound is attained. -/
theorem sharp_fails (n : ℕ) :
    ¬ ((sharpFamily n).approx (2*n+3)).rel (some ⟨n, by omega⟩) (some ⟨n, by omega⟩) := by
  intro h
  let u := List.replicate (n+1) false ++ List.replicate (n+2) false
  let v := List.replicate (n+1) false ++ (true :: List.replicate (n+1) false)
  have hu : u.length = 2*n+3 := by simp [u]; omega
  have hv : v.length = 2*n+3 := by simp [v]; omega
  have heq := (approx_iff_words _ _ _ _).mp h u v hu hv
  rw [sharp_countdown_output n n le_rfl u (by omega),
    sharp_countdown_output n n le_rfl v (by omega)] at heq
  have htail := (List.cons.inj (List.append_cancel_left heq)).2
  have hdropu : u.drop (n+1) = List.replicate (n+2) false := by simp [u]
  have hdropv : v.drop (n+1) = true :: List.replicate (n+1) false := by simp [v]
  rw [hdropu, hdropv, sharp_none_false_input, sharp_none_enter_input] at htail
  have hmem : true ∈ false :: (List.replicate n false ++ [true]) := by simp
  rw [← htail] at hmem
  simp at hmem

theorem sharp_state_card (n : ℕ) : Nat.card (SharpState n) = n+2 := by
  simp [SharpState, Nat.card_eq_fintype_card]

/-- All `m≥2` sizes attain the exact `2m-1` distinguishing horizon. -/
theorem sharp_family_all_sizes (n : ℕ) :
    Nat.card (SharpState n) = n+2 ∧
    ((sharpFamily n).approx (2 * Nat.card (SharpState n) - 2)).rel
      (some ⟨n, by omega⟩) (some ⟨n, by omega⟩) ∧
    ¬ ((sharpFamily n).approx (2 * Nat.card (SharpState n) - 1)).rel
      (some ⟨n, by omega⟩) (some ⟨n, by omega⟩) := by
  rw [sharp_state_card]
  refine ⟨rfl, ?_, ?_⟩
  · have heq : 2 * (n+2) - 2 = 2*n+2 := by omega
    rw [heq]
    exact sharp_survives n
  · have heq : 2 * (n+2) - 1 = 2*n+3 := by omega
    rw [heq]
    exact sharp_fails n

def oneStateSharp : Mealy Unit where
  out _ b := b
  next _ _ := ()

theorem one_state_sharp :
    (oneStateSharp.approx 0).rel () () ∧ ¬ (oneStateSharp.approx 1).rel () () := by
  simp only [approx, refine, PER.universal, oneStateSharp]
  decide

/-- For every positive state count there is an actual binary Mealy machine attaining `2m-1`. -/
theorem sharp_every_cardinality (m : ℕ) (hm : 0 < m) :
    ∃ (S : Type) (inst : Fintype S) (M : Mealy S) (s : S),
      @Fintype.card S inst = m ∧ (M.approx (2*m-2)).rel s s ∧
        ¬ (M.approx (2*m-1)).rel s s := by
  by_cases hm1 : m = 1
  · subst m
    exact ⟨Unit, inferInstance, oneStateSharp, (), rfl, one_state_sharp⟩
  · let n := m-2
    have hn : n+2 = m := by dsimp [n]; omega
    refine ⟨SharpState n, inferInstance, sharpFamily n, some ⟨n, by omega⟩, ?_, ?_, ?_⟩
    · simpa [SharpState] using hn
    · have heq : 2*m-2 = 2*n+2 := by omega
      rw [heq]
      exact sharp_survives n
    · have heq : 2*m-1 = 2*n+3 := by omega
      rw [heq]
      exact sharp_fails n

end Orthemology.Frontier.Mealy
