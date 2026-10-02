import RecordedTransition
import TrajectoryBudget

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

/-- Pointwise charge of the actual recorded outcome is dominated by the old
controller's planned charge. Finite fresh-kernel integration preserves it. -/
theorem recorded_one_step_bound
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y) (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (g : RecordedState (Obs := Obs) → ℝ≥0∞) (c f : ResetState (Obs := Obs) → ℝ≥0∞)
    (hcharge : ∀ s y, g (recordedUpdate stay next π s y) ≤ c s.1)
    (s : RecordedState (Obs := Obs)) :
    (∫⁻ t, g t + f t.1 ∂recordedTransitionKernel K stay next π hK hNorm θ s) ≤
      c s.1 + ∫⁻ t, f t ∂resetTransitionKernel K stay next π hK hNorm θ s.1 := by
  rw [recordedTransition_lintegral, resetTransition_lintegral]
  have hsum : (∑ y : Obs s.1.1 (π s.1.1 s.1.2),
      ENNReal.ofReal (K s.1.1 θ (π s.1.1 s.1.2) y)) = 1 := by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun y _ => hK _ _ _ y), hNorm, ENNReal.ofReal_one]
  simp only [mul_add, Finset.sum_add_distrib, recordedUpdate]
  apply add_le_add_right
  calc
    _ ≤ ∑ y : Obs s.1.1 (π s.1.1 s.1.2), ENNReal.ofReal (K s.1.1 θ (π s.1.1 s.1.2) y) * c s.1 :=
      Finset.sum_le_sum (fun y _ => mul_le_mul_left' (hcharge s y) _)
    _ = c s.1 := by rw [← Finset.sum_mul, hsum, one_mul]

/-- The recorded process inherits the old finite controller budget with one
explicit initial-record charge. No record is lost on reset. -/
theorem recorded_expected_charge_bound
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y) (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (g : RecordedState (Obs := Obs) → ℝ≥0∞) (c : ResetState (Obs := Obs) → ℝ≥0∞)
    (hcharge : ∀ s y, g (recordedUpdate stay next π s y) ≤ c s.1)
    (n : ℕ) (s : RecordedState (Obs := Obs)) :
    markovExpectedCharge (recordedTransitionKernel K stay next π hK hNorm θ) g (n+1) s ≤
      g s + markovExpectedCharge (resetTransitionKernel K stay next π hK hNorm θ) c n s.1 := by
  induction n generalizing s with
  | zero => simp [markovExpectedCharge]
  | succ n ih =>
    rw [markovExpectedCharge]
    calc
      _ ≤ g s + ∫⁻ t, g t + markovExpectedCharge (resetTransitionKernel K stay next π hK hNorm θ) c n t.1
          ∂recordedTransitionKernel K stay next π hK hNorm θ s :=
        add_le_add_left (lintegral_mono (fun t => ih t)) _
      _ ≤ g s + (c s.1 + ∫⁻ t,
          markovExpectedCharge (resetTransitionKernel K stay next π hK hNorm θ) c n t
          ∂resetTransitionKernel K stay next π hK hNorm θ s.1) :=
        add_le_add_left (recorded_one_step_bound K stay next π hK hNorm θ g c _ hcharge s) _
      _ = _ := rfl

end Orthemology.Tranche2
