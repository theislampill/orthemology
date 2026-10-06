import OpaqueActions

/-! A deliberately small target-coordinate bridge, not a full physical protocol.
In a canonical withheld-effect world, a failed attempt preserves this coordinate
and a successful repair hit sets it true. A lower bound on target achievement
therefore requires an initially defective coordinate. -/
namespace CoveringKernel.RepairState

def after (initial : Bool) (hit : ℕ → Prop) [DecidablePred hit] : ℕ → Bool
  | 0 => initial
  | n+1 => if hit n then true else after initial hit n

theorem after_true_iff (initial : Bool) (hit : ℕ → Prop) [DecidablePred hit] (N : ℕ) :
    after initial hit N = true ↔ initial = true ∨ ∃ i < N, hit i := by
  induction N with
  | zero => simp [after]
  | succ N ih =>
    by_cases hN : hit N
    · simp only [after, if_pos hN, true_iff]
      exact Or.inr ⟨N, by omega, hN⟩
    · rw [after, if_neg hN, ih]
      constructor
      · intro h
        rcases h with h | ⟨i, hi, hh⟩
        · exact Or.inl h
        · exact Or.inr ⟨i, by omega, hh⟩
      · intro h
        rcases h with h | ⟨i, hi, hh⟩
        · exact Or.inl h
        · have hiN : i < N := by
            by_contra hn
            have heq : i = N := by omega
            exact hN (heq ▸ hh)
          exact Or.inr ⟨i, hiN, hh⟩

theorem defective_start_iff_hit (hit : ℕ → Prop) [DecidablePred hit] (N : ℕ) :
    after false hit N = true ↔ ∃ i < N, hit i := by
  simpa using after_true_iff false hit N

theorem correct_start_already_done (hit : ℕ → Prop) [DecidablePred hit] :
    after true hit 0 = true := rfl

theorem correct_start_persists (hit : ℕ → Prop) [DecidablePred hit] (N : ℕ) :
    after true hit N = true := (after_true_iff true hit N).mpr (Or.inl rfl)

variable {α Action Obs : Type*} [Fintype α] [DecidableEq α]

/- Defective-start application to the complete-action trace. In an initially
correct world the intervention-hit count is not a target-achievement lower bound. -/
omit [Fintype α] in
theorem defective_start_iff_successWithin
    (support : Action → Finset α) (π : Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (T : Finset α) (N : ℕ) :
    after false (fun i => Disjoint (support (π (Actions.history π (observe T) i))) T) N = true ↔
      Actions.SuccessWithin support π observe T N :=
  defective_start_iff_hit _ N

#print axioms after_true_iff
#print axioms defective_start_iff_successWithin
#print axioms correct_start_already_done
end CoveringKernel.RepairState
