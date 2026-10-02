import ResetFutureCost
import MarkovCharge
import Mathlib.MeasureTheory.Integral.Lebesgue.Countable

noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

/-- Exact one-step expectation under the actual state transition measure. -/
theorem resetTransition_lintegral
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (s : ResetState (Obs := Obs)) (f : ResetState (Obs := Obs) → ℝ≥0∞) :
    (∫⁻ t, f t ∂resetTransitionKernel K stay next π hK hNorm θ s) =
      ∑ y : Obs s.1 (π s.1 s.2), ENNReal.ofReal (K s.1 θ (π s.1 s.2) y) *
        f (resetUpdate stay next π s y) := by
  letI : MeasurableSpace (Obs s.1 (π s.1 s.2)) := ⊤
  letI : MeasurableSingletonClass (Obs s.1 (π s.1 s.2)) := ⟨fun _ => trivial⟩
  change (∫⁻ t, f t ∂(resetTransitionPMF K stay next π hK hNorm θ s).toMeasure) = _
  unfold resetTransitionPMF
  rw [← PMF.toMeasure_map (resetUpdate stay next π s) (observationPMF K hK hNorm θ s.1 (π s.1 s.2)) (measurable_of_finite _), lintegral_map (measurable_of_countable _) (measurable_of_finite _)]
  rw [lintegral_fintype]
  apply Finset.sum_congr rfl
  intro y _
  rw [PMF.toMeasure_apply_singleton _ y (measurableSet_singleton y)]
  exact mul_comm _ _

omit [Fintype Phase] [Fintype Θ] in
lemma resetFutureCost_nonneg
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ)
    (hK : ∀ p η a y, 0 ≤ K p η a y) (hcost : ∀ p a, 0 ≤ cost p a)
    (θ : Θ) (n : ℕ) (s : ResetState (Obs := Obs)) :
    0 ≤ resetFutureCost K stay next π cost θ n s := by
  induction n generalizing s with
  | zero => exact le_rfl
  | succ n ih =>
    exact add_nonneg (hcost _ _)
      (Finset.sum_nonneg (fun y _ => mul_nonneg (hK _ _ _ _) (ih _)))

/-- The finite Markov expectation is exactly the previously checked real-valued
future cost. The PMF and kernel laws discharge this equality internally. -/
theorem markovExpectedCharge_eq_resetFuture
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1) (hcost : ∀ p a, 0 ≤ cost p a)
    (θ : Θ) (n : ℕ) (s : ResetState (Obs := Obs)) :
    markovExpectedCharge (resetTransitionKernel K stay next π hK hNorm θ)
      (fun s => ENNReal.ofReal (cost s.1 (π s.1 s.2))) n s =
      ENNReal.ofReal (resetFutureCost K stay next π cost θ n s) := by
  induction n generalizing s with
  | zero => simp [markovExpectedCharge, resetFutureCost]
  | succ n ih =>
    simp only [markovExpectedCharge, ih, resetFutureCost]
    rw [resetTransition_lintegral]
    rw [ENNReal.ofReal_add (hcost _ _) (Finset.sum_nonneg (fun y _ =>
      mul_nonneg (hK _ _ _ _) (resetFutureCost_nonneg K stay next π cost hK hcost θ n _)))]
    congr 1
    rw [ENNReal.ofReal_sum_of_nonneg (fun y _ =>
      mul_nonneg (hK _ _ _ _) (resetFutureCost_nonneg K stay next π cost hK hcost θ n _))]
    apply Finset.sum_congr rfl
    intro y _
    rw [ENNReal.ofReal_mul (hK _ _ _ _)]

/-- End-to-end finite-prefix law binding: actual infinite trajectory expectation
at an equal-weight phase start equals the finite Hellinger-budget recurrence. -/
theorem trajectory_expected_charge_eq_resetCost
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1) (hcost : ∀ p a, 0 ≤ cost p a)
    (θ : Θ) (n : ℕ) (p : Phase) :
    (∫⁻ x, pathCharge (fun s => ENNReal.ofReal (cost s.1 (π s.1 s.2))) 0 n x
      ∂markovTrajectory (resetTransitionKernel K stay next π hK hNorm θ) ⟨p,[]⟩) =
      ENNReal.ofReal (resetCost K stay next π cost θ n p []) := by
  rw [markovTrajectory_expected_charge, markovExpectedCharge_eq_resetFuture K stay next π cost hK hNorm hcost]
  rw [resetCost_eq_mass_future]
  simp only [dHistoryMass, one_mul]

end Orthemology.Tranche2
