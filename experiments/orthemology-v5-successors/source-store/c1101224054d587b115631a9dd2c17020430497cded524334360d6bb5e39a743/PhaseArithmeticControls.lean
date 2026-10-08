import HiddenChangePhaseArithmetic

open Filter HiddenChange

namespace HiddenChangePhaseArithmeticControls

-- Both literal residues occur above every bound.
example (M : ℕ) : ∃ b, M ≤ b ∧ b % 2 = 0 :=
  exists_mod_two_barrier M 0
example (M : ℕ) : ∃ b, M ≤ b ∧ b % 2 = 1 :=
  exists_mod_two_barrier M 1

-- The public theorem requires no information about the finite prefix.
example (p : ℕ → ℕ) (N K : ℕ) (σ : Fin 2)
    (hstep : ∀ t, N ≤ t → p (t+1) = p t ∨ p (t+1) = p t+1)
    (hstop : ∀ t, N ≤ t → K ≤ p t → p t % 2 = σ.val → p (t+1) = p t) :
    ∃ r, ∀ᶠ t in atTop, p t = r :=
  phase_mod_two_eventually_constant p N K σ hstep hstop

-- Constant phases satisfy the hypotheses, including below the stop threshold.
example (c N K : ℕ) (σ : Fin 2) :
    ∃ r, ∀ᶠ t in atTop, (fun _ : ℕ => c) t = r := by
  apply phase_mod_two_eventually_constant (fun _ => c) N K σ
  · intro t ht
    exact Or.inl rfl
  · intro t ht hK hmod
    rfl

#check HiddenChange.phase_mod_two_eventually_constant
#print axioms HiddenChange.exists_mod_two_barrier
#print axioms HiddenChange.phase_mod_two_eventually_constant

end HiddenChangePhaseArithmeticControls

namespace HiddenChangePhaseArithmeticNegativeControls

-- Removing the stop premise permits unbounded unit-step growth.
example : ∀ t : ℕ, (t+1) = t ∨ (t+1) = t+1 := by
  intro t
  exact Or.inr rfl

example : ¬ ∃ r : ℕ, ∀ᶠ t : ℕ in atTop, t = r := by
  rintro ⟨r, hr⟩
  obtain ⟨N, hN⟩ := eventually_atTop.mp hr
  have h₀ := hN N le_rfl
  have h₁ := hN (N+1) (by omega)
  omega

-- Allowing a jump of two can skip every stop phase of literal residue one.
example : ∀ t : ℕ, (2*t) % 2 = (1 : Fin 2).val → 2*(t+1) = 2*t := by
  intro t ht
  norm_num at ht

example : ¬ ∃ r : ℕ, ∀ᶠ t : ℕ in atTop, 2*t = r := by
  rintro ⟨r, hr⟩
  obtain ⟨N, hN⟩ := eventually_atTop.mp hr
  have h₀ := hN N le_rfl
  have h₁ := hN (N+1) (by omega)
  omega

end HiddenChangePhaseArithmeticNegativeControls
