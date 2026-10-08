import PhaseStabilization

open Filter

namespace HiddenChange

/-- The literal parity enumeration reaches either selected mode above any
natural phase bound. No ordering of an abstract cycle is used. -/
theorem exists_mod_two_barrier (M : ℕ) (σ : Fin 2) :
    ∃ b, M ≤ b ∧ b % 2 = σ.val := by
  have hσ := σ.isLt
  refine ⟨2 * M + σ.val, ?_, ?_⟩ <;> omega

/-- A zero/one-increment phase cannot cross a sufficiently late phase whose
literal remainder modulo two is the non-rejectable mode. Consequently the
natural-valued phase eventually stays constant. -/
theorem phase_mod_two_eventually_constant (p : ℕ → ℕ) (N K : ℕ) (σ : Fin 2)
    (hstep : ∀ t, N ≤ t → p (t+1) = p t ∨ p (t+1) = p t+1)
    (hstop : ∀ t, N ≤ t → K ≤ p t → p t % 2 = σ.val → p (t+1) = p t) :
    ∃ r, ∀ᶠ t in Filter.atTop, p t = r := by
  obtain ⟨b, hb, hmod⟩ := exists_mod_two_barrier (max K (p N)) σ
  have hBound : ∀ t, N ≤ t → p t ≤ b := by
    intro t ht
    induction t, ht using Nat.le_induction with
    | base => exact (le_max_right _ _).trans hb
    | succ t ht ih =>
        by_cases he : p t = b
        · have hK : K ≤ p t := by omega
          have hm : p t % 2 = σ.val := by simpa only [he] using hmod
          have hs := hstop t ht hK hm
          omega
        · have hs := hstep t ht
          omega
  apply HiddenParity.PhaseArithmetic.bounded_tail_eventually_constant p N b hBound
  intro t ht
  have hs := hstep t ht
  omega

end HiddenChange
