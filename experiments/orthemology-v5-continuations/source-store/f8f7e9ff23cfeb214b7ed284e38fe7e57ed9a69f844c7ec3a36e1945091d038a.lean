import RecordedCharge

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

/-- Actual recorded charges inherit the finite tree bound and its infinite
consequences. Only a pointwise one-observation domination is required. -/
theorem recorded_nat_charge_transfer
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y) (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (cost : Phase → Θ → ℕ) (g : RecordedState (Obs := Obs) → ℕ)
    (hcharge : ∀ s y, g (recordedUpdate stay next π s y) ≤ cost s.1.1 (π s.1.1 s.1.2))
    (p : Phase) (C : ℝ)
    (hbudget : ∀ n, resetCost K stay next π (fun q a => (cost q a : ℝ)) θ n p [] ≤ C) :
    let s₀ : RecordedState (Obs := Obs) := (⟨p,[]⟩,none)
    let μ := markovTrajectory (recordedTransitionKernel K stay next π hK hNorm θ) s₀
    (∫⁻ x, ∑' n, (g (x n) : ℝ≥0∞) ∂μ) ≤ ENNReal.ofReal (C + g s₀) ∧
      ∀ᵐ x ∂μ, ∀ᶠ n in atTop, g (x n) = 0 := by
  let s₀ : RecordedState (Obs := Obs) := (⟨p,[]⟩,none)
  let μ := markovTrajectory (recordedTransitionKernel K stay next π hK hNorm θ) s₀
  have hC : 0 ≤ C := by simpa only [resetCost] using hbudget 0
  have hfinite : ∀ n, (∫⁻ x, pathCharge (fun s => (g s : ℝ≥0∞)) 0 n x ∂μ) ≤
      ENNReal.ofReal (C + g s₀) := by
    intro n
    cases n with
    | zero => simp [pathCharge]
    | succ n =>
      rw [markovTrajectory_expected_charge]
      have hb := recorded_expected_charge_bound K stay next π hK hNorm θ (fun s => (g s : ℝ≥0∞))
        (fun s => (cost s.1 (π s.1 s.2) : ℝ≥0∞))
        (fun s y => by
          change (g (recordedUpdate stay next π s y) : ℝ≥0∞) ≤ (cost s.1.1 (π s.1.1 s.1.2) : ℝ≥0∞)
          exact_mod_cast hcharge s y) n s₀
      have he := markovExpectedCharge_eq_resetFuture K stay next π
        (fun q a => (cost q a : ℝ)) hK hNorm (fun q a => Nat.cast_nonneg _) θ n s₀.1
      simp only [ENNReal.ofReal_natCast] at he
      have hr := resetCost_eq_mass_future K stay next π (fun q a => (cost q a : ℝ)) θ n p []
      simp only [dHistoryMass, one_mul] at hr
      rw [he] at hb
      have hreal := ENNReal.ofReal_le_ofReal (hbudget n)
      rw [hr] at hreal
      calc
        _ ≤ (g s₀ : ℝ≥0∞) + ENNReal.ofReal (resetFutureCost K stay next π
            (fun q a => (cost q a : ℝ)) θ n s₀.1) := hb
        _ ≤ (g s₀ : ℝ≥0∞) + ENNReal.ofReal C := add_le_add_left hreal _
        _ = ENNReal.ofReal (C + g s₀) := by
          rw [ENNReal.ofReal_add hC (Nat.cast_nonneg _), ENNReal.ofReal_natCast, add_comm]
  exact ⟨trajectory_total_charge_bound μ (fun s => (g s : ℝ≥0∞)) _ hfinite,
    (trajectory_nat_charge_eventually_zero μ g _ hfinite).2⟩

omit [Fintype Phase] [Fintype Θ] in
lemma resetCost_zero
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (θ : Θ)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) :
    resetCost K stay next π (fun _ _ => 0) θ n p h = 0 := by
  induction n generalizing p h with
  | zero => rfl
  | succ n ih => simp only [resetCost, ih, mul_zero, zero_mul, zero_add, ite_self, Finset.sum_const_zero]

end Orthemology.Tranche2
