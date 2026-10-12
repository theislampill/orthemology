import PhaseStabilization

noncomputable section
open Filter HiddenParity.Sufficiency HiddenParity.PhaseArithmetic

namespace IndependentPhaseReview

def B : Finset Bool := Finset.univ
def falseIndex : ℕ := (Fintype.equivFin B ⟨false, by simp [B]⟩).val
def skipPhase (n : ℕ) : ℕ := n * Fintype.card B + falseIndex

/-- The counterexample uses the retained enumeration itself, not an assumed
ordering of Bool's finite enumeration. -/
theorem skip_always_selects_false (n : ℕ) :
    cycleAction B true (skipPhase n) = false := by
  exact cycleAction_at_index B true ⟨false, by simp [B]⟩ n

theorem skip_has_two_step_increments (n : ℕ) : skipPhase (n+1) = skipPhase n + 2 := by
  simp [skipPhase, B, Nat.add_mul]
  omega

theorem skipping_barrier_is_not_stable :
    ¬ ∃ j, ∀ᶠ n in atTop, skipPhase n = j := by
  rintro ⟨j,hj⟩
  obtain ⟨N,hN⟩ := eventually_atTop.mp hj
  have h0 := hN N le_rfl
  have h1 := hN (N+1) (by omega)
  have hs := skip_has_two_step_increments N
  omega

/-- A fixed wrong-model phase meets the actual stabilization interface. The
interface promises constancy, not correctness of the final model. -/
theorem stable_phase_may_select_wrong_model :
    (∃ j, ∀ᶠ n : ℕ in atTop, falseIndex = j) ∧
    cycleAction B true falseIndex ≠ true := by
  constructor
  · apply cycling_phase_eventually_constant (fun _ => falseIndex) 0 0 B true true
      (by simp [B])
    · intro n hn
      exact Or.inl rfl
    · intro n hn hk hc
      rfl
  · have h := skip_always_selects_false 0
    simpa [skipPhase] using h

/-- Boundedness without monotonicity does not imply eventual constancy. -/
theorem bounded_oscillation_is_not_stable :
    (∀ n : ℕ, n % 2 ≤ 1) ∧ ¬ ∃ j, ∀ᶠ n in atTop, n % 2 = j := by
  constructor
  · intro n
    omega
  · rintro ⟨j,hj⟩
    obtain ⟨N,hN⟩ := eventually_atTop.mp hj
    have h0 := hN N le_rfl
    have h1 := hN (N+1) (by omega)
    omega

/-- Even an infinite mode type is admitted; permanent absence is an explicit
allowed conclusion. -/
theorem permanent_none_is_admitted :
    (∀ᶠ n : ℕ in atTop, (none : Option ℕ) = none) ∨
      ∃ e, ∀ᶠ n : ℕ in atTop, (none : Option ℕ) = some e := by
  apply persistent_option_eventually_stable (fun _ => (none : Option ℕ)) 0
  intro n hn e he
  cases he

theorem changing_present_mode_is_not_stable :
    ¬ ((∀ᶠ n : ℕ in atTop, (some n : Option ℕ) = none) ∨
      ∃ e, ∀ᶠ n : ℕ in atTop, (some n : Option ℕ) = some e) := by
  intro h
  rcases h with h | ⟨e,he⟩
  · obtain ⟨N,hN⟩ := eventually_atTop.mp h
    have hn := hN N le_rfl
    cases hn
  · obtain ⟨N,hN⟩ := eventually_atTop.mp he
    have h0 := Option.some.inj (hN N le_rfl)
    have h1 := Option.some.inj (hN (N+1) (by omega))
    omega

/-- The arithmetic premises permit a jump at any prescribed physical time. -/
theorem arbitrarily_late_unit_jump (D : ℕ) :
    let p : ℕ → ℕ := fun n => if n ≤ D then 0 else 1
    (∀ n, p (n+1) = p n ∨ p (n+1) = p n + 1) ∧ p D = 0 ∧ p (D+1) = 1 := by
  dsimp
  constructor
  · intro n
    split_ifs <;> omega
  · simp

#print axioms skip_always_selects_false
#print axioms skip_has_two_step_increments
#print axioms skipping_barrier_is_not_stable
#print axioms stable_phase_may_select_wrong_model
#print axioms bounded_oscillation_is_not_stable
#print axioms permanent_none_is_admitted
#print axioms changing_present_mode_is_not_stable
#print axioms arbitrarily_late_unit_jump

end IndependentPhaseReview
